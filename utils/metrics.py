
from time import perf_counter

from fastapi import FastAPI, Request, Response
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)


HTTP_REQUESTS = Counter(
    "http_requests_total",
    "Total de solicitudes HTTP",
    ["method", "route", "status"],
)

HTTP_DURATION = Histogram(
    "http_request_duration_seconds",
    "Duracion de las solicitudes HTTP en segundos",
    ["method", "route"],
)


def configure_metrics(app: FastAPI):

    # registrar las metricas de cada solicitud
    @app.middleware("http")
    async def monitor_requests(request: Request, call_next):

        if request.url.path in {"/metrics", "/metrics/inventario"}:
            return await call_next(request)

        start = perf_counter()
        status_code = 500

        try:
            response = await call_next(request)
            status_code = response.status_code
            return response

        finally:
            duration = perf_counter() - start

            route = request.scope.get("route")
            route_path = getattr(route, "path", None)
            
            if route_path is None:
                if request.url.path in {
                    "/openapi.json", 
                    "/docs", 
                    "/docs/oauth2-redirect", 
                    "/redoc",
                }:
                    route_path = request.url.path
                else:
                    route_path = "unmatched"
                    
            method = request.method
            if method not in {
                "GET", "POST", "PUT", "PATCH",
                "DELETE", "HEAD", "OPTIONS"
            }:
                method = "OTHER"

            HTTP_REQUESTS.labels(
                method=method,
                route=route_path,
                status=str(status_code),
            ).inc()

            HTTP_DURATION.labels(
                method=method,
                route=route_path,
            ).observe(duration)

    # exponer las metricas para prometheus
    @app.get("/metrics", include_in_schema=False)
    async def metrics():
        return Response(
            content=generate_latest(),
            headers={"Content-Type": CONTENT_TYPE_LATEST},
        )
