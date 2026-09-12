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