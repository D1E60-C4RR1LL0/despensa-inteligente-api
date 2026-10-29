import pytest


def test_read_stock_alertas(authorized_client, db_session, test_stock):
    test_stock.cantidad = test_stock.producto.stock_minimo
    db_session.commit()

    response = authorized_client.get("/stocks/alertas")

    assert response.status_code == 200

    data = response.json()

    assert len(data) >= 1
    assert any(
        stock["producto_id"] == test_stock.producto_id
        for stock in data
    )
    
def test_read_stock_alertas_no_incluye_productos_inactivos(
    authorized_client,
    db_session,
    test_stock
):
    test_stock.cantidad = test_stock.producto.stock_minimo
    test_stock.producto.activo = False
    db_session.commit()

    response = authorized_client.get("/stocks/alertas")

    assert response.status_code == 200

    data = response.json()

    assert not any(
        stock["producto_id"] == test_stock.producto_id
        for stock in data
    )


def test_stock_lifecycle_preserves_references(authorized_client, test_producto, test_ubicacion):
    payload = {"producto_id": test_producto.id, "ubicacion_id": test_ubicacion.id, "cantidad": 7.5}
    created = authorized_client.post("/stocks/", json=payload)
    assert created.status_code == 200
    path = f"/stocks/{created.json()['id']}"
    persisted = authorized_client.get(path)
    assert persisted.status_code == 200
    assert persisted.json()["producto"]["id"] == test_producto.id
    assert persisted.json()["ubicacion"]["id"] == test_ubicacion.id
    filtered = authorized_client.get("/stocks/", params={
        "producto_id": test_producto.id, "ubicacion_id": test_ubicacion.id,
    }).json()
    assert len(filtered) == 1 and filtered[0]["id"] == created.json()["id"]

    assert authorized_client.put(path, json={"cantidad": 12.25}).status_code == 200
    persisted = authorized_client.get(path).json()
    assert persisted["cantidad"] == 12.25
    assert persisted["producto_id"] == test_producto.id
    assert persisted["ubicacion_id"] == test_ubicacion.id
    assert authorized_client.delete(path).status_code == 204
    assert authorized_client.get(path).status_code == 404


@pytest.mark.parametrize("method", ["get", "put", "delete"])
def test_missing_stock_returns_404(authorized_client, method):
    kwargs = {"json": {"cantidad": 5}} if method == "put" else {}
    assert authorized_client.request(method, "/stocks/999999", **kwargs).status_code == 404


@pytest.mark.parametrize("field", ["producto_id", "ubicacion_id"])
def test_stock_creation_requires_existing_references(
    authorized_client, test_producto, test_ubicacion, field,
):
    payload = {"producto_id": test_producto.id, "ubicacion_id": test_ubicacion.id, "cantidad": 5}
    payload[field] = 999999
    assert authorized_client.post("/stocks/", json=payload).status_code == 404
    assert authorized_client.get("/stocks/").json() == []


def test_duplicate_stock_does_not_overwrite_quantity(authorized_client, test_stock):
    payload = {"producto_id": test_stock.producto_id,
               "ubicacion_id": test_stock.ubicacion_id, "cantidad": 999}
    assert authorized_client.post("/stocks/", json=payload).status_code == 400
    assert authorized_client.get(f"/stocks/{test_stock.id}").json()["cantidad"] == 100


def test_stock_can_move_to_an_existing_location(authorized_client, test_stock):
    other = authorized_client.post("/ubicaciones/", json={"nombre": "Destino valido"})
    assert other.status_code == 200
    path = f"/stocks/{test_stock.id}"
    assert authorized_client.put(path, json={"ubicacion_id": other.json()["id"]}).status_code == 200
    persisted = authorized_client.get(path).json()
    assert persisted["ubicacion_id"] == other.json()["id"]
    assert persisted["cantidad"] == 100


def test_stock_update_cannot_duplicate_product_and_location(authorized_client, test_stock):
    other = authorized_client.post("/ubicaciones/", json={"nombre": "Destino ocupado"})
    assert other.status_code == 200
    created = authorized_client.post("/stocks/", json={
        "producto_id": test_stock.producto_id, "ubicacion_id": other.json()["id"], "cantidad": 5,
    })
    assert created.status_code == 200
    path = f"/stocks/{test_stock.id}"
    assert authorized_client.put(path, json={"ubicacion_id": other.json()["id"]}).status_code == 400
    assert authorized_client.get(path).json()["ubicacion_id"] == test_stock.ubicacion_id


@pytest.mark.parametrize("field", ["producto_id", "ubicacion_id"])
def test_stock_update_rejects_missing_references_without_changing_stock(
    authorized_client, test_stock, field,
):
    path = f"/stocks/{test_stock.id}"
    original = authorized_client.get(path).json()
    response = authorized_client.put(path, json={field: 999999})
    assert response.status_code == 404
    assert authorized_client.get(path).json() == original
