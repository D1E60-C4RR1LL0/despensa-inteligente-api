"""HTTP/database integration checks for supplier lifecycle and referential integrity."""

import pytest


def test_supplier_lifecycle_preserves_omitted_fields(authorized_client):
    payload = {
        "nombre": "Proveedor ciclo", "contacto": "Contacto inicial",
        "telefono": "123456789", "email": "supplier@example.com", "direccion": "Calle 10",
    }
    created = authorized_client.post("/proveedores/", json=payload)
    assert created.status_code == 200
    supplier_id = created.json()["id"]
    path = f"/proveedores/{supplier_id}"
    assert any(item["id"] == supplier_id for item in authorized_client.get("/proveedores/").json())
    assert authorized_client.get(path).json()["email"] == payload["email"]

    updated = authorized_client.put(path, json={"contacto": "Nuevo contacto"})
    assert updated.status_code == 200
    persisted = authorized_client.get(path).json()
    assert persisted["contacto"] == "Nuevo contacto"
    assert all(persisted[key] == value for key, value in payload.items() if key != "contacto")

    assert authorized_client.delete(path).status_code == 204
    assert authorized_client.get(path).status_code == 404


@pytest.mark.parametrize("method", ["get", "put", "delete"])
def test_missing_supplier_returns_404(authorized_client, method):
    kwargs = {"json": {"contacto": "Sin destino"}} if method == "put" else {}
    response = authorized_client.request(method, "/proveedores/999999", **kwargs)
    assert response.status_code == 404
    assert response.json()["detail"] == "Proveedor no encontrado"


def test_supplier_with_products_cannot_be_deleted(authorized_client, test_producto):
    path = f"/proveedores/{test_producto.proveedor_id}"
    response = authorized_client.delete(path)
    assert response.status_code == 400
    assert "productos asociados" in response.json()["detail"]
    assert authorized_client.get(path).status_code == 200
    assert authorized_client.get(f"/productos/{test_producto.id}").status_code == 200


def test_invalid_supplier_email_does_not_create_record(authorized_client):
    response = authorized_client.post("/proveedores/", json={
        "nombre": "Correo invalido", "email": "not-an-email",
    })
    assert response.status_code == 422
    assert all(item["nombre"] != "Correo invalido"
               for item in authorized_client.get("/proveedores/").json())
