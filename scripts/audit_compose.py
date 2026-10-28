"""Verify Compose startup, persistence and migration failure in a disposable project."""

import argparse
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.audit_docker import request
from scripts.init_compose_env import create_env


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", help="Audit this existing image without rebuilding it")
    args = parser.parse_args()
    expected_image = None
    if args.image:
        result = subprocess.run(
            ["docker", "image", "inspect", "--format", "{{.Id}}", args.image],
            capture_output=True, text=True, check=True, timeout=30,
        )
        expected_image = result.stdout.strip()
    scratch = ROOT / ".pytest_cache"
    scratch.mkdir(exist_ok=True)
    if not scratch.resolve().is_relative_to(ROOT):
        raise RuntimeError("La carpeta temporal debe permanecer dentro del proyecto")
    project = "inventory-audit-" + secrets.token_hex(6)
    with TemporaryDirectory(prefix="compose-", dir=scratch) as temporary:
        directory = Path(temporary)
        env_file = directory / ".env.audit"
        create_env(env_file)
        values = dict(line.split("=", 1) for line in env_file.read_text(encoding="utf-8").splitlines()
                      if line and not line.startswith("#"))
        env = {k: v for k, v in os.environ.items() if k not in values}
        env["API_PORT"] = "0"
        env["API_IMAGE"] = args.image or "inventory-api:local"
        env.pop("COMPOSE_PROFILES", None)
        base = ["docker", "compose", "--project-name", project,
                "--env-file", str(env_file), "--file", str(ROOT / "docker-compose.yml")]

        def redact(message):
            for key in ("MYSQL_PASSWORD", "MYSQL_ROOT_PASSWORD", "JWT_SECRET_KEY",
                        "COMPOSE_DATABASE_URL"):
                message = message.replace(values[key], "<redacted>")
            return message

        def compose(*args, check=True, override=None):
            command = base + (["--file", str(override)] if override else []) + list(args)
            result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True,
                                    text=True, encoding="utf-8", errors="replace", timeout=240)
            if check and result.returncode:
                print(redact(result.stdout + result.stderr), file=sys.stderr)
                raise RuntimeError("Fallo en docker compose " + args[0])
            return result

        def inspect_service(service, field):
            container = compose("ps", "--all", "--quiet", service).stdout.strip()
            result = subprocess.run(
                ["docker", "inspect", "--format", field, container],
                capture_output=True, text=True, encoding="utf-8", errors="replace",
                check=True, timeout=30,
            )
            return result.stdout.strip()

        def api_url():
            address = compose("port", "api", "8000").stdout.strip()
            return "http://" + address

        def verify_image():
            api_image = inspect_service("api", "{{.Image}}")
            migration_image = inspect_service("migrate", "{{.Image}}")
            assert api_image == migration_image, "API y migraciones deben usar la misma imagen"
            if expected_image:
                assert api_image == expected_image, "La auditoria no utiliza la imagen solicitada"
            return api_image

        def login(base_url, password):
            result = request(base_url, "/login", {
                "username": "compose_audit", "password": password,
            }, form=True)
            assert result["token_type"] == "bearer"
            return result["access_token"]

        try:
            original = env_file.read_text(encoding="utf-8")
            env_file.write_text(original.replace(
                "JWT_SECRET_KEY=" + values["JWT_SECRET_KEY"], "JWT_SECRET_KEY="
            ), encoding="utf-8")
            missing = compose("config", "--quiet", check=False)
            assert missing.returncode != 0 and "JWT_SECRET_KEY" in missing.stderr
            env_file.write_text(original, encoding="utf-8")
            compose("config", "--quiet")

            print("Iniciando Compose con base vacia y migraciones...", flush=True)
            compose("up", "--detach", "--no-build" if args.image else "--build",
                    "--wait", "--wait-timeout", "180")
            tested_image = verify_image()
            base_url = api_url()
            assert "/login" in request(base_url, "/openapi.json")["paths"]
            password = secrets.token_urlsafe(32)
            user = request(base_url, "/signup", {
                "username": "compose_audit", "email": "compose_audit@example.com",
                "first_name": "Compose", "last_name": "Audit",
                "password": password, "role": "user",
            })
            assert user["username"] == "compose_audit"
            token = login(base_url, password)
            category = request(base_url, "/categorias/", {
                "nombre": "Persistencia Compose", "descripcion": "Dato de auditoria",
            }, token=token)
            for path in ("/productos/", "/stocks/", "/stocks/alertas", "/productos/lista-compras"):
                assert request(base_url, path, token=token) == []
            assert inspect_service("migrate", "{{.State.ExitCode}}") == "0"
            assert inspect_service("api", "{{.State.Health.Status}}") == "healthy"
            assert inspect_service("db", "{{.State.Health.Status}}") == "healthy"
            bindings = json.loads(inspect_service("db", "{{json .HostConfig.PortBindings}}"))
            assert not bindings, "MySQL no debe publicar un puerto en el host"
            schema = compose("exec", "-T", "api", "python", "-c", (
                "import models; from config.database import Base,engine; "
                "from alembic.autogenerate import compare_metadata; "
                "from alembic.migration import MigrationContext; "
                "from sqlalchemy import inspect,text; "
                "c=engine.connect(); "
                "assert compare_metadata(MigrationContext.configure(c),Base.metadata)==[]; "
                "assert len(Base.metadata.tables)==9; "
                "assert c.execute(text('SELECT version_num FROM alembic_version')).scalar_one()=='f3171e47e124'; "
                "print('9 tablas, revision correcta, 0 diferencias'); c.close()"
            )).stdout.strip()
            network = json.loads(inspect_service("api", "{{json .NetworkSettings.Networks}}"))
            volume = json.loads(inspect_service("db", "{{json .Mounts}}"))[0]["Name"]
            assert any(name.endswith("_backend") for name in network)

            print("Recreando contenedores y comprobando persistencia...", flush=True)
            compose("down")
            compose("up", "--detach", "--no-build", "--wait", "--wait-timeout", "180")
            assert verify_image() == tested_image
            base_url = api_url()
            token = login(base_url, password)
            categories = request(base_url, "/categorias/", token=token)
            assert any(item["id"] == category["id"] and item["nombre"] == category["nombre"]
                       for item in categories)
            assert json.loads(inspect_service("db", "{{json .Mounts}}"))[0]["Name"] == volume

            print("Comprobando bloqueo ante migracion fallida...", flush=True)
            compose("down")
            override = directory / "migration-failure.yml"
            override.write_text(
                'services:\n  migrate:\n    command: ["python", "-c", "raise SystemExit(7)"]\n',
                encoding="utf-8",
            )
            failed = compose("up", "--detach", "--no-build", "--wait", "--wait-timeout", "180",
                             check=False, override=override)
            assert failed.returncode != 0
            assert inspect_service("migrate", "{{.State.ExitCode}}") == "7"
            assert inspect_service("api", "{{.State.Running}}") == "false"
            print(json.dumps({
                "project": project, "image": env["API_IMAGE"], "image_id": tested_image,
                "requested_image_used": expected_image is not None,
                "missing_config_rejected": True,
                "startup_and_api_pass": True, "schema": schema,
                "db_port_not_published": True, "persistent_data_after_recreation": True,
                "migration_failure_blocks_api": True, "all_checks_pass": True,
            }, indent=2))
            return 0
        finally:
            # This random project and its volume belong exclusively to this audit.
            compose("down", "--volumes", "--remove-orphans")
            print("Proyecto Compose temporal y sus datos eliminados.", flush=True)


if __name__ == "__main__":
    sys.exit(main())
