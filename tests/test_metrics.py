
from datetime import datetime, timedelta
import secrets

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from prometheus_client.parser import text_string_to_metric_families

from config.database import Base
from models import (
    User,
    Categoria,
    Producto,
    Stock,
    Ubicacion,
    TipoMovimiento,
    MovimientoInventario,
)
from utils.inventory_metrics import inventory_metrics
from utils.utils import get_password_hash


# obtener el valor de una metrica
def metric_value(content, name, labels=None, default=None):
    labels = labels or {}

    for family in text_string_to_metric_families(content):
        for sample in family.samples:
            if sample.name == name and sample.labels == labels:
                return sample.value

    return default


# comprobar las metricas http
def test_http_metrics(client):
    before = client.get("/metrics").text

    assert client.get("/openapi.json").status_code == 200
    assert client.get("/ruta-inexistente-e3").status_code == 404

    response = client.get("/metrics")
    assert response.status_code == 200

    after = response.text

    for route, status in [
        ("/openapi.json", "200"),
        ("unmatched", "404")
    ]:
        labels = {
            "method": "GET",
            "route": route,
            "status": status
        }

        previous = metric_value(
            before, "http_requests_total", labels, 0
        )

        current = metric_value(
            after, "http_requests_total", labels
        )

        assert current == previous + 1

    labels = {
        "method": "GET",
        "route": "/openapi.json"
    }

    assert metric_value(
        after, "http_request_duration_seconds_count", labels
    ) == metric_value(
        before, "http_request_duration_seconds_count", labels, 0
    ) + 1


# comprobar las metricas del inventario
def test_inventory_metrics():
    engine = create_engine("sqlite:///:memory:")

    try:
        Base.metadata.create_all(engine)

        with Session(engine) as db:

            categoria = Categoria(nombre="Alimentos")
            despensa = Ubicacion(nombre="Despensa")
            cocina = Ubicacion(nombre="Cocina")

            entrada = TipoMovimiento(
                codigo="ENT",
                nombre="Entrada",
                afecta_stock="entrada"
            )

            salida = TipoMovimiento(
                codigo="SAL",
                nombre="Salida",
                afecta_stock="salida"
            )

            usuario = User(
                username="test_metrics",
                first_name="Test",
                last_name="Metrics",
                email="metrics@example.com",
                hashed_password=get_password_hash(
                    secrets.token_urlsafe(24)
                ),
                role="user"
            )

            db.add_all([
                categoria, despensa, cocina,
                entrada, salida, usuario
            ])

            db.flush()

            productos = {}

            for nombre, minimo, activo in [
                ("Arroz", 3, True),
                ("Leche", 5, True),
                ("Huevos", 6, True),
                ("Aceite", 3, True),
                ("Inactivo", 5, False)
            ]:
                producto = Producto(
                    codigo=nombre.upper(),
                    nombre=nombre,
                    categoria_id=categoria.id,
                    stock_minimo=minimo,
                    activo=activo
                )

                db.add(producto)
                productos[nombre] = producto

            db.flush()

            # registrar existencias en distintas ubicaciones
            for nombre, ubicacion, cantidad in [
                ("Arroz", despensa, 4),
                ("Arroz", cocina, 6),
                ("Leche", cocina, 2),
                ("Aceite", despensa, 3)
            ]:
                db.add(Stock(
                    producto_id=productos[nombre].id,
                    ubicacion_id=ubicacion.id,
                    cantidad=cantidad
                ))

            ahora = datetime.now()

            # registrar movimientos dentro de las ultimas 24 horas
            for tipo, cantidad, fecha in [
                (entrada, 4, ahora),
                (entrada, 6, ahora),
                (entrada, 6, ahora),
                (entrada, 3, ahora),
                (salida, 4, ahora),
                (entrada, 2, ahora - timedelta(hours=25))
            ]:
                db.add(MovimientoInventario(
                    producto_id=productos["Arroz"].id,
                    tipo_movimiento_id=tipo.id,
                    usuario_id=usuario.id,
                    cantidad=cantidad,
                    fecha=fecha
                ))

            db.commit()

            response = inventory_metrics(db)
            content = response.body.decode("utf-8")

            assert metric_value(
                content, "inventory_database_up"
            ) == 1

            assert metric_value(
                content, "inventory_products_active"
            ) == 4

            assert metric_value(
                content, "inventory_products_low_stock"
            ) == 2

            assert metric_value(
                content, "inventory_products_out_of_stock"
            ) == 1

            for tipo, total in [
                ("entrada", 4),
                ("salida", 1),
                ("ninguno", 0),
                ("otro", 0)
            ]:
                assert metric_value(
                    content,
                    "inventory_movements_last_24h",
                    {"tipo": tipo}
                ) == total

    finally:
        engine.dispose()


# comprobar el comportamiento ante un error de base de datos
def test_inventory_database_failure():
    engine = create_engine("sqlite:///:memory:")

    try:
        # no crear las tablas para provocar un error de consulta
        with Session(engine) as db:
            response = inventory_metrics(db)
            content = response.body.decode("utf-8")

            assert metric_value(
                content, "inventory_database_up"
            ) == 0

            assert metric_value(
                content, "inventory_products_active"
            ) is None

            assert metric_value(
                content, "inventory_products_low_stock"
            ) is None

            assert metric_value(
                content, "inventory_products_out_of_stock"
            ) is None

    finally:
        engine.dispose()
