"""The inventory endpoints must reject anonymous reads and writes."""

import pytest


@pytest.mark.parametrize("resource,payload", [
    ("stocks", {"cantidad": 1, "producto_id": 1, "ubicacion_id": 1}),
    ("proveedores", {"nombre": "Sin permiso"}),
    ("ubicaciones", {"nombre": "Sin permiso"}),
])
@pytest.mark.parametrize("method,suffix", [
    ("get", "/"), ("get", "/1"), ("post", "/"), ("put", "/1"), ("delete", "/1"),
])
def test_inventory_requires_authentication(client, resource, payload, method, suffix):
    kwargs = {"json": payload} if method in {"post", "put"} else {}
    response = client.request(method, f"/{resource}{suffix}", **kwargs)
    assert response.status_code == 401
