"""A bounded, repeatable HTTP workload for disposable Compose deployments."""

from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import math
from statistics import mean, median
import time

from scripts.audit_docker import request

PROFILES = {
    "standard": {"cpus": 0.5, "mem_limit": "192m"},
    "expanded": {"cpus": 1.0, "mem_limit": "384m"},
}
PATHS = ("/productos/", "/stocks/", "/stocks/alertas", "/productos/lista-compras")
CASE = {"products": 24, "stock_per_product": 2, "minimum_stock": 5,
        "requests": 2400, "concurrency": 8, "warmup_requests": 16,
        "paths": list(PATHS), "model": "closed-loop, fixed requests, no retries"}
CASE_DIGEST = hashlib.sha256(json.dumps(CASE, sort_keys=True).encode()).hexdigest()


def seed_inventory(base, token, category_id):
    location = request(base, "/ubicaciones/", {"nombre": "Capacity location"}, token=token)
    products = set()
    for index in range(CASE["products"]):
        product = request(base, "/productos/", {
            "codigo": f"capacity-{index:03}", "nombre": f"Capacity product {index:03}",
            "categoria_id": category_id, "stock_minimo": CASE["minimum_stock"], "activo": True,
        }, token=token)
        request(base, "/stocks/", {"producto_id": product["id"],
                "ubicacion_id": location["id"], "cantidad": CASE["stock_per_product"]}, token=token)
        products.add(product["id"])
    return products


def validate_response(path, rows, products):
    if not isinstance(rows, list) or len(rows) != len(products):
        raise ValueError("La consulta no conserva el conjunto completo de inventario")
    key = "id" if path == "/productos/" else "producto_id"
    if {row[key] for row in rows} != products:
        raise ValueError("La consulta no devuelve los productos esperados")
    if path == "/productos/":
        valid = all(row["activo"] and row["stock_minimo"] == CASE["minimum_stock"] for row in rows)
    elif path == "/productos/lista-compras":
        valid = all(row["stock_actual"] == CASE["stock_per_product"]
                    and row["stock_minimo"] == CASE["minimum_stock"]
                    and row["cantidad_sugerida"] == CASE["minimum_stock"] - CASE["stock_per_product"]
                    for row in rows)
    else:
        valid = all(row["cantidad"] == CASE["stock_per_product"] for row in rows)
    if not valid:
        raise ValueError("La respuesta modifica el estado esperado del inventario")


def summarize(durations, errors, elapsed):
    ordered = sorted(durations)
    if not ordered or elapsed <= 0:
        raise ValueError("La medicion debe contener solicitudes y tiempo positivo")
    return {"requests": len(ordered), "successful": len(ordered) - sum(errors.values()),
            "errors": sum(errors.values()), "error_types": dict(errors),
            "elapsed_seconds": round(elapsed, 6),
            "requests_per_second": round(len(ordered) / elapsed, 3),
            "mean_latency_ms": round(mean(ordered), 3),
            "p50_latency_ms": round(median(ordered), 3),
            "p95_latency_ms": round(ordered[math.ceil(len(ordered) * 0.95) - 1], 3),
            "max_latency_ms": round(ordered[-1], 3)}


def run_workload(base, token, products, monitor):
    monitor.phase = "capacity_warmup"
    for index in range(CASE["warmup_requests"]):
        path = PATHS[index % len(PATHS)]
        validate_response(path, request(base, path, token=token), products)

    def operation(index):
        path = PATHS[index % len(PATHS)]
        started = time.perf_counter()
        error = None
        try:
            validate_response(path, request(base, path, token=token), products)
        except Exception as exception:
            # Retain counts, never HTTP bodies or authorization headers.
            error = type(exception).__name__
        return (time.perf_counter() - started) * 1000, error

    monitor.phase = "capacity_measured"
    started = time.perf_counter()
    with ThreadPoolExecutor(max_workers=CASE["concurrency"]) as executor:
        results = list(executor.map(operation, range(CASE["requests"])))
    elapsed = time.perf_counter() - started
    errors = Counter(error for _, error in results if error)
    return {"case": CASE, "case_sha256": CASE_DIGEST,
            **summarize([duration for duration, _ in results], errors, elapsed)}
