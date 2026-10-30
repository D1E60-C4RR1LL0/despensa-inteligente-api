"""Deploy the validated API image to an isolated, temporary Compose environment."""

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import secrets
import subprocess
import sys
from tempfile import TemporaryDirectory
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.audit_docker import request
from scripts.init_compose_env import create_env
from scripts.measure_resources import ResourceMonitor, SERVICES, declared_limits, verify_limits
from scripts.capacity_workload import PROFILES, run_workload, seed_inventory


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", required=True)
    parser.add_argument("--expected-image-id", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--environment", required=True)
    parser.add_argument("--output", type=Path, required=True)
    resources = parser.add_mutually_exclusive_group()
    resources.add_argument("--baseline-resources", action="store_true",
                        help="Measure a local baseline with a temporary unlimited-resources override")
    resources.add_argument("--capacity-profile", choices=PROFILES,
                           help="Run the fixed concurrent workload with a bounded API resource budget")
    args = parser.parse_args()
    report = {
        "status": "failure", "environment": args.environment,
        "lifecycle": "ephemeral", "commit": args.commit,
        "ref": os.environ.get("GITHUB_REF", "local"),
        "event": os.environ.get("GITHUB_EVENT_NAME", "local"),
        "run_url": (os.environ.get("GITHUB_SERVER_URL", "https://github.com") + "/"
                    + os.environ["GITHUB_REPOSITORY"] + "/actions/runs/"
                    + os.environ["GITHUB_RUN_ID"])
                   if os.environ.get("GITHUB_RUN_ID") else None,
        "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
        "image": args.image, "expected_image_id": args.expected_image_id,
        "started_at": timestamp(), "checks": {}, "cleanup": "not_needed",
        "resource_mode": "baseline" if args.baseline_resources else "bounded",
    }
    stage = "image_identity"

    def docker(*command):
        result = subprocess.run(
            ["docker", *command], cwd=ROOT, capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=240,
        )
        if result.returncode:
            raise RuntimeError("Fallo en docker " + command[0])
        return result.stdout.strip()

    try:
        if args.baseline_resources and os.environ.get("GITHUB_ACTIONS") == "true":
            raise ValueError("El modo base de medicion no esta permitido en CI")
        if not re.fullmatch(r"[0-9a-f]{40}", args.commit):
            raise ValueError("El commit debe ser un SHA completo")
        if not re.fullmatch(r"sha256:[0-9a-f]{64}", args.expected_image_id):
            raise ValueError("El identificador esperado debe ser SHA-256")
        image = json.loads(docker("image", "inspect", args.image))[0]
        report["image_id"] = image["Id"]
        if image["Id"] != args.expected_image_id:
            raise ValueError("La imagen recibida no coincide con el build validado")
        revision = (image["Config"].get("Labels") or {}).get("org.opencontainers.image.revision")
        if revision != args.commit:
            raise ValueError("La revision de la imagen no coincide con el commit")
        report["checks"]["build_identity"] = True

        scratch = ROOT / ".pytest_cache"
        scratch.mkdir(exist_ok=True)
        if not scratch.resolve().is_relative_to(ROOT):
            raise RuntimeError("La carpeta temporal debe permanecer dentro del proyecto")
        project = "inventory-deploy-" + secrets.token_hex(6)
        report["project"] = project
        with TemporaryDirectory(prefix="deployment-", dir=scratch) as temporary:
            env_file = Path(temporary) / ".env.deploy"
            create_env(env_file)
            values = dict(line.split("=", 1) for line in env_file.read_text(encoding="utf-8").splitlines()
                          if line and not line.startswith("#"))
            env = {key: value for key, value in os.environ.items() if key not in values}
            env.update(API_IMAGE=args.image, API_PORT="0")
            for key in ("COMPOSE_PROFILES", "COMPOSE_FILE", "COMPOSE_PROJECT_NAME"):
                env.pop(key, None)
            files = ["--file", str(ROOT / "docker-compose.yml")]
            if args.baseline_resources:
                override = Path(temporary) / "resources-baseline.json"
                override.write_text(json.dumps({"services": {
                    service: {"cpus": 0, "mem_limit": 0} for service in SERVICES
                }}), encoding="utf-8")
                files.extend(["--file", str(override)])
            elif args.capacity_profile:
                override = Path(temporary) / "capacity-profile.json"
                override.write_text(json.dumps({"services": {
                    "api": PROFILES[args.capacity_profile]
                }}), encoding="utf-8")
                files.extend(["--file", str(override)])
                report["capacity_profile"] = args.capacity_profile

            def compose(*command):
                result = subprocess.run(
                    ["docker", "compose", "--project-name", project,
                     "--env-file", str(env_file), *files,
                     *command], cwd=ROOT, env=env, capture_output=True, text=True,
                    encoding="utf-8", errors="replace", timeout=240,
                )
                if result.returncode:
                    message = result.stdout + result.stderr
                    for key in ("MYSQL_PASSWORD", "MYSQL_ROOT_PASSWORD", "JWT_SECRET_KEY",
                                "COMPOSE_DATABASE_URL"):
                        message = message.replace(values[key], "<redacted>")
                    print(message, file=sys.stderr)
                    raise RuntimeError("Fallo en docker compose " + command[0])
                return result.stdout.strip()

            def inspect(service, field):
                container = compose("ps", "--all", "--quiet", service)
                return docker("inspect", "--format", field, container)

            monitor = ResourceMonitor(project)
            monitor.start()
            try:
                stage = "compose_startup"
                configuration = json.loads(compose("config", "--format", "json"))
                expected_limits = {service: declared_limits(configuration["services"][service],
                                                            require_limits=not args.baseline_resources)
                                   for service in SERVICES}
                report["cleanup"] = "pending"
                print("Desplegando imagen validada con Compose...", flush=True)
                compose("up", "--detach", "--no-build", "--wait", "--wait-timeout", "180")
                if any(inspect(service, "{{.Image}}") != args.expected_image_id
                       for service in ("api", "migrate")):
                    raise ValueError("Los contenedores no utilizan la imagen validada")
                if inspect("migrate", "{{.State.ExitCode}}") != "0":
                    raise RuntimeError("Las migraciones no terminaron correctamente")
                if any(inspect(service, "{{.State.Health.Status}}") != "healthy"
                       for service in ("api", "db")):
                    raise RuntimeError("API y MySQL deben estar saludables")
                report["checks"].update(container_identity=True, migrations=True, healthy=True)

                stage = "functional_validation"
                monitor.phase = "functional"
                base = "http://" + compose("port", "api", "8000")
                if "/login" not in request(base, "/openapi.json")["paths"]:
                    raise RuntimeError("La API no expone el contrato esperado")
                password = secrets.token_urlsafe(32)
                user = request(base, "/signup", {
                    "username": "deployment_check", "email": "deployment@example.com",
                    "first_name": "Deployment", "last_name": "Check", "password": password,
                })
                if user["role"] != "user":
                    raise RuntimeError("El registro no crea un usuario normal")
                login = request(base, "/login", {
                    "username": "deployment_check", "password": password,
                }, form=True)
                token = login["access_token"]
                if not token or login["token_type"] != "bearer":
                    raise RuntimeError("El inicio de sesion no devuelve un token valido")
                category = request(base, "/categorias/", {
                    "nombre": "Validacion despliegue", "descripcion": "Dato temporal",
                }, token=token)
                categories = request(base, "/categorias/", token=token)
                if not any(item["id"] == category["id"] for item in categories):
                    raise RuntimeError("No se pudo leer el dato creado mediante la API")
                report["checks"].update(openapi=True, signup=True, login=True, database_read_write=True)

                stage = "resource_validation"
                monitor.phase = "operations"
                durations = []
                workload_started = time.perf_counter()
                for _ in range(10):
                    for path in ("/productos/", "/stocks/", "/stocks/alertas", "/productos/lista-compras"):
                        started = time.perf_counter()
                        result = request(base, path, token=token)
                        if not isinstance(result, list):
                            raise RuntimeError("Una operacion del perfil funcional no devolvio una lista")
                        durations.append((time.perf_counter() - started) * 1000)
                    time.sleep(0.2)
                report["resource_workload"] = {
                    "requests": len(durations), "successful": len(durations),
                    "elapsed_seconds": round(time.perf_counter() - workload_started, 3),
                    "mean_latency_ms": round(sum(durations) / len(durations), 3),
                    "max_latency_ms": round(max(durations), 3),
                }
                if args.capacity_profile:
                    stage = "capacity_validation"
                    monitor.phase = "capacity_seed"
                    products = seed_inventory(base, token, category["id"])
                    report["capacity_workload"] = run_workload(base, token, products, monitor)
                    if report["capacity_workload"]["errors"]:
                        raise RuntimeError("El perfil de capacidad contiene errores HTTP o de datos")
                    report["checks"]["capacity_workload"] = True
                report["effective_limits"] = {}
                for service in SERVICES:
                    data = inspect(service, '{{.HostConfig.NanoCpus}}|{{.HostConfig.Memory}}|'
                                           '{{.State.OOMKilled}}|{{.RestartCount}}').split("|")
                    actual = {"nano_cpus": int(data[0]), "memory_bytes": int(data[1]),
                              "oom_killed": data[2] == "true", "restart_count": int(data[3])}
                    verify_limits(expected_limits[service], actual,
                                  require_limits=not args.baseline_resources)
                    report["effective_limits"][service] = {"declared": expected_limits[service],
                                                          "actual": actual}
                report["checks"]["resource_limits"] = True
                report["validated_at"] = timestamp()
            finally:
                try:
                    monitor.stop()
                    report["resource_measurements"] = monitor.report()
                finally:
                    try:
                        # Only this randomly named deployment project owns these resources.
                        compose("down", "--volumes", "--remove-orphans")
                        report["cleanup"] = "success"
                    except Exception:
                        report["cleanup"] = "failure"
                        raise
                if "validated_at" in report and (
                    report["resource_measurements"]["sampling_errors"] or any(
                        report["resource_measurements"]["services"][service]["sample_count"] == 0
                        for service in ("db", "api")
                    )
                ):
                    raise RuntimeError("No se obtuvo una medicion valida de API y MySQL")
        report["status"] = "success"
    except Exception as error:
        report["failed_stage"] = stage
        report["error_type"] = type(error).__name__
        print("Despliegue fallido en " + stage + ": " + type(error).__name__, file=sys.stderr)
    finally:
        report["finished_at"] = timestamp()
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, indent=2))
        if os.environ.get("GITHUB_STEP_SUMMARY"):
            with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as summary:
                summary.write(
                    "### Despliegue simulado\n\n"
                    f"- Estado: `{report['status']}`\n"
                    f"- Ambiente: `{args.environment}`\n"
                    f"- Commit: `{args.commit}`\n"
                    f"- Imagen: `{report.get('image_id', 'no verificada')}`\n"
                    f"- Limpieza: `{report['cleanup']}`\n\n"
                    "El entorno es temporal y se elimina al terminar.\n"
                )
    return 0 if report["status"] == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
