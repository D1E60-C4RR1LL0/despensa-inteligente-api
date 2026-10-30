"""Sample Docker CLI statistics and verify effective Compose resource limits."""

from datetime import datetime, timezone
from decimal import Decimal
import json
import re
import subprocess
import threading

SERVICES = ("db", "migrate", "api")


def memory_bytes(value):
    if isinstance(value, int):
        return value
    match = re.fullmatch(r"([0-9.]+)\s*([KMGT]?i?B|[kmgt]?)", str(value).strip())
    if not match:
        raise ValueError("Unidad de memoria no reconocida")
    amount, unit = match.groups()
    units = {"": 1, "B": 1}
    for power, prefix in enumerate("KMGT", 1):
        units[prefix + "B"] = 1000 ** power
        units[prefix + "iB"] = units[prefix.lower()] = 1024 ** power
    return int(Decimal(amount) * units[unit])


def declared_limits(service, require_limits=True):
    limits = {
        "nano_cpus": int(Decimal(str(service.get("cpus", 0))) * 1_000_000_000),
        "memory_bytes": memory_bytes(service.get("mem_limit", 0)),
    }
    if require_limits and any(value <= 0 for value in limits.values()):
        raise ValueError("Compose debe declarar limites positivos antes del despliegue")
    return limits


def verify_limits(expected, actual, require_limits=True):
    if require_limits and any(expected[key] <= 0 for key in ("nano_cpus", "memory_bytes")):
        raise ValueError("Cada servicio debe declarar limites positivos de CPU y memoria")
    if any(expected[key] != actual[key] for key in ("nano_cpus", "memory_bytes")):
        raise ValueError("Docker no aplica los limites declarados en Compose")
    if actual["oom_killed"] or actual["restart_count"]:
        raise ValueError("Se detecto OOM o reinicio durante la validacion")


class ResourceMonitor:
    def __init__(self, project):
        self.project = project
        self.phase = "startup"
        self.samples = []
        self.errors = []
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=True)

    @staticmethod
    def _docker(*args):
        result = subprocess.run(
            ["docker", *args], capture_output=True, text=True,
            encoding="utf-8", errors="replace", timeout=15,
        )
        if result.returncode:
            raise RuntimeError("No se pudo consultar la telemetria Docker")
        return result.stdout

    def _capture(self):
        listing = self._docker(
            "ps", "--no-trunc", "--filter", "label=com.docker.compose.project=" + self.project,
            "--filter", "status=running", "--format",
            '{{.ID}} {{.Label "com.docker.compose.service"}}',
        )
        services = dict(line.split(" ", 1) for line in listing.splitlines() if line.strip())
        services = {key: value for key, value in services.items() if value in SERVICES}
        if not services:
            return
        stats = self._docker("stats", "--no-stream", "--no-trunc", "--format", "{{json .}}",
                             *services)
        for line in stats.splitlines():
            row = json.loads(line)
            container = row.get("ID") or row["Container"]
            service = services.get(container)
            usage = memory_bytes(row["MemUsage"].split("/")[0].strip())
            if not service or usage == 0:
                continue
            self.samples.append({
                "service": service, "phase": self.phase,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "cpu_percent": float(row["CPUPerc"].rstrip("%")), "memory_bytes": usage,
            })

    def _run(self):
        while not self.stop_event.is_set():
            try:
                self._capture()
            except Exception as error:
                self.errors.append(type(error).__name__)
            self.stop_event.wait(1)

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join(timeout=35)
        if self.thread.is_alive():
            raise RuntimeError("No se pudo finalizar el muestreo de recursos")

    def report(self):
        summary = {}
        for service in SERVICES:
            samples = [sample for sample in self.samples if sample["service"] == service]
            summary[service] = {
                "sample_count": len(samples),
                "max_sampled_memory_mib": round(max(s["memory_bytes"] for s in samples) / 1024**2, 2)
                                          if samples else None,
                "max_sampled_cpu_percent": max(s["cpu_percent"] for s in samples) if samples else None,
            }
        return {"method": "docker stats --no-stream; approximately every 2-3 seconds",
                "services": summary, "sampling_errors": self.errors, "samples": self.samples}
