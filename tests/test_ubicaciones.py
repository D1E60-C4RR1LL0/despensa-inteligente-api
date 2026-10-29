"""HTTP/database integration checks for locations and inventory references."""

import pytest


def test_location_lifecycle_preserves_omitted_fields(authorized_client):
    payload = {"nombre": "Bodega ciclo", "direccion": "Calle 20", "tipo": "almacen"}
    created = authorized_client.post("/ubicaciones/", json=payload)
    assert created.status_code == 200
    location_id = created.json()["id"]
    path = f"/ubicaciones/{location_id}"
    assert any(item["id"] == location_id for item in authorized_client.get("/ubicaciones/").json())

    assert authorized_client.put(path, json={"activo": False}).status_code == 200
    persisted = authorized_client.get(path).json()
    assert persisted["activo"] is False
    assert all(persisted[key] == value for key, value in payload.items())
    assert authorized_client.put(path, json={"nombre": "Bodega renombrada"}).status_code == 200
    assert authorized_client.get(path).json()["nombre"] == "Bodega renombrada"
    assert authorized_client.delete(path).status_code == 204
    assert authorized_client.get(path).status_code == 404


@pytest.mark.parametrize("method", ["get", "put", "delete"])
def test_missing_location_returns_404(authorized_client, method):
    kwargs = {"json": {"activo": False}} if method == "put" else {}
    response = authorized_client.request(method, "/ubicaciones/999999", **kwargs)
    assert response.status_code == 404
    assert response.json()["detail"] == "Ubicación no encontrada"


def test_duplicate_location_creation_and_rename_are_rejected(authorized_client, test_ubicacion):
    duplicate = authorized_client.post("/ubicaciones/", json={"nombre": test_ubicacion.nombre})
    assert duplicate.status_code == 400
    other = authorized_client.post("/ubicaciones/", json={"nombre": "Bodega distinta"})
    assert other.status_code == 200
    path = f"/ubicaciones/{other.json()['id']}"
    assert authorized_client.put(path, json={"nombre": test_ubicacion.nombre}).status_code == 400
    assert authorized_client.get(path).json()["nombre"] == "Bodega distinta"


def test_location_with_stock_cannot_be_deleted(authorized_client, test_stock):
    path = f"/ubicaciones/{test_stock.ubicacion_id}"
    response = authorized_client.delete(path)
    assert response.status_code == 400
    assert "stock asociado" in response.json()["detail"]
    assert authorized_client.get(path).status_code == 200


def test_location_history_is_preserved_after_stock_is_removed(
    authorized_client, test_producto, test_ubicacion, test_tipo_movimiento,
):
    movement = authorized_client.post("/movimientos/", json={
        "cantidad": 5, "referencia": "HISTORIA-UBICACION",
        "tipo_movimiento_id": test_tipo_movimiento.id,
        "producto_id": test_producto.id, "ubicacion_destino_id": test_ubicacion.id,
    })
    assert movement.status_code == 200
    stocks = authorized_client.get("/stocks/", params={
        "producto_id": test_producto.id, "ubicacion_id": test_ubicacion.id,
    }).json()
    assert len(stocks) == 1
    assert authorized_client.delete(f"/stocks/{stocks[0]['id']}").status_code == 204
    response = authorized_client.delete(f"/ubicaciones/{test_ubicacion.id}")
    assert response.status_code == 400
    assert "movimientos de inventario" in response.json()["detail"]
    assert authorized_client.get(f"/movimientos/{movement.json()['id']}").status_code == 200
