"""Compare two bounded API budgets using the same image, data and workload."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from statistics import median
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.capacity_workload import CASE, CASE_DIGEST, PROFILES
from scripts.measure_resources import SERVICES, declared_limits, verify_limits

ORDER = ("standard", "expanded", "expanded", "standard")


def compare(reports):
    if len(reports) != len(ORDER):
        raise ValueError("Se requieren dos repeticiones de cada presupuesto")
    reference = reports[0]
    for profile, report in zip(ORDER, reports):
        if (report["status"] != "success" or report["cleanup"] != "success"
            or report.get("capacity_profile") != profile or report["resource_mode"] != "bounded"
            or not all(report["checks"].get(key) for key in (
                "build_identity", "container_identity", "migrations", "healthy", "openapi", "signup",
                "login", "database_read_write", "resource_limits", "capacity_workload"))):
            raise ValueError("Una repeticion no cumple las comprobaciones de despliegue/capacidad")
        if (report["commit"] != reference["commit"]
            or report["image_id"] != reference["image_id"]
            or report["expected_image_id"] != report["image_id"]):
            raise ValueError("La comparacion debe utilizar el mismo commit e imagen")
        workload = report["capacity_workload"]
        if (workload["case"] != CASE or workload["case_sha256"] != CASE_DIGEST
            or workload["requests"] != CASE["requests"] or workload["successful"] != CASE["requests"]
            or workload["errors"] != 0):
            raise ValueError("La carga o los resultados no son comparables")
        if report["resource_measurements"]["sampling_errors"]:
            raise ValueError("La medicion de recursos contiene errores")
        for service in SERVICES:
            limits = report["effective_limits"][service]
            expected = declared_limits(PROFILES[profile]) if service == "api" else reference["effective_limits"][service]["declared"]
            verify_limits(expected, limits["actual"])
            if expected != limits["declared"]:
                raise ValueError("Se modificaron recursos fuera del perfil previsto")
        for service in ("api", "db"):
            if report["resource_measurements"]["services"][service]["sample_count"] <= 0:
                raise ValueError("Faltan muestras de los servicios permanentes")
    groups = {}
    for profile in PROFILES:
        workloads = [r["capacity_workload"] for r in reports if r["capacity_profile"] == profile]
        groups[profile] = {"api_limits": PROFILES[profile], "repetitions": len(workloads),
            "median_requests_per_second": round(median(w["requests_per_second"] for w in workloads), 3),
            "median_p95_latency_ms": round(median(w["p95_latency_ms"] for w in workloads), 3),
            "successful_requests": sum(w["successful"] for w in workloads), "errors": 0}
    base, expanded = groups["standard"], groups["expanded"]
    return {"profiles": groups,
            "observed_throughput_ratio_expanded_over_standard": round(
                expanded["median_requests_per_second"] / base["median_requests_per_second"], 3),
            "scope": "Observed vertical budget comparison on one host; not maximum capacity, SLA or autoscaling"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for option in ("image", "expected-image-id", "commit", "environment"):
        parser.add_argument("--" + option, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    report = {"status": "failure", "commit": args.commit, "expected_image_id": args.expected_image_id,
              "started_at": datetime.now(timezone.utc).isoformat(), "order": ORDER, "runs": []}
    directory = args.output.parent / (args.output.stem + "-runs")
    directory.mkdir(parents=True, exist_ok=True)
    try:
        for index, profile in enumerate(ORDER, 1):
            output = directory / f"{index}-{profile}.json"
            # Remove only this exact report file to avoid accepting a previous run after a failure.
            output.unlink(missing_ok=True)
            print(f"Comparando capacidad: {index}/4, {profile}", flush=True)
            result = subprocess.run([
                sys.executable, str(ROOT / "scripts/deploy_simulated.py"), "--image", args.image,
                "--expected-image-id", args.expected_image_id, "--commit", args.commit,
                "--environment", args.environment, "--capacity-profile", profile,
                "--output", str(output.resolve()),
            ], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
            # The child owns cleanup and persists its failure report; do not terminate it mid-cleanup.
            if output.exists():
                report["runs"].append(json.loads(output.read_text(encoding="utf-8")))
            if result.returncode:
                raise RuntimeError("Una repeticion fallo; revisar su informe individual")
        report["comparison"] = compare(report["runs"])
        report["status"] = "success"
    except Exception as error:
        report["error_type"] = type(error).__name__
    finally:
        report["finished_at"] = datetime.now(timezone.utc).isoformat()
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(json.dumps({key: value for key, value in report.items() if key != "runs"}, indent=2))
    return 0 if report["status"] == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())
