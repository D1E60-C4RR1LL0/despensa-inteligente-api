
import logging
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Response
from sqlalchemy import select, func, case, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from prometheus_client import (
    CollectorRegistry,
    Gauge,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

from config.database import get_db
from models.producto import Producto
from models.stock import Stock
from models.movimiento_inventario import MovimientoInventario
from models.tipo_movimiento import TipoMovimiento


router = APIRouter()
logger = logging.getLogger(__name__)


def collect_inventory_metrics(db: Session):

    # sumar el stock por producto
    stock_totals = (
        select(
            Stock.producto_id,
            func.sum(Stock.cantidad).label("cantidad")
        )
        .group_by(Stock.producto_id)
        .subquery()
    )

    cantidad = func.coalesce(stock_totals.c.cantidad, 0)
    minimo = func.coalesce(Producto.stock_minimo, 0)

    # contar productos activos segun su disponibilidad
    stock_query = (
        select(
            func.count(Producto.id),
            func.count(
                case(
                    (
                        and_(
                            cantidad > 0,
                            cantidad <= minimo
                        ),
                        1
                    )
                )
            ),
            func.count(
                case((cantidad <= 0, 1))
            )
        )
        .select_from(Producto)
        .outerjoin(
            stock_totals,
            stock_totals.c.producto_id == Producto.id
        )
        .where(Producto.activo.is_(True))
    )

    activos, stock_bajo, sin_stock = (
        db.execute(stock_query).one()
    )

    # consultar movimientos de las ultimas 24 horas
    ahora = datetime.now()
    desde = ahora - timedelta(hours=24)

    movement_query = (
        select(
            TipoMovimiento.afecta_stock,
            func.count(MovimientoInventario.id)
        )
        .select_from(MovimientoInventario)
        .join(
            TipoMovimiento,
            MovimientoInventario.tipo_movimiento_id
            == TipoMovimiento.id
        )
        .where(
            MovimientoInventario.fecha >= desde,
            MovimientoInventario.fecha <= ahora
        )
        .group_by(TipoMovimiento.afecta_stock)
    )

    movimientos = {
        "entrada": 0,
        "salida": 0,
        "ninguno": 0,
        "otro": 0
    }

    for tipo, total in db.execute(movement_query):
        categoria = tipo if tipo in movimientos else "otro"
        movimientos[categoria] += total

    return activos, stock_bajo, sin_stock, movimientos


@router.get("/metrics/inventario", include_in_schema=False)
def inventory_metrics(db: Session = Depends(get_db)):

    # crear un registro independiente para cada consulta
    registry = CollectorRegistry()

    database_up = Gauge(
        "inventory_database_up",
        "Estado de las consultas de inventario en la base de datos",
        registry=registry
    )

    try:
        activos, stock_bajo, sin_stock, movimientos = (
            collect_inventory_metrics(db)
        )

        database_up.set(1)

        Gauge(
            "inventory_products_active",
            "Cantidad de productos activos",
            registry=registry
        ).set(activos)

        Gauge(
            "inventory_products_low_stock",
            "Cantidad de productos activos con stock bajo",
            registry=registry
        ).set(stock_bajo)

        Gauge(
            "inventory_products_out_of_stock",
            "Cantidad de productos activos sin stock",
            registry=registry
        ).set(sin_stock)

        movement_metric = Gauge(
            "inventory_movements_last_24h",
            "Movimientos registrados en las ultimas 24 horas",
            ["tipo"],
            registry=registry
        )

        for tipo, total in movimientos.items():
            movement_metric.labels(tipo=tipo).set(total)

    except SQLAlchemyError:
        database_up.set(0)
        logger.warning(
            "No fue posible recopilar las metricas de inventario"
        )

    return Response(
        content=generate_latest(registry),
        headers={"Content-Type": CONTENT_TYPE_LATEST}
    )
