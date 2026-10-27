"""Original Orders functionality remains available."""


def test_orders_crud(client):
    assert client.get("/orders/").json() == []
    created = client.post("/orders/", json={"customer_name": "John Doe", "description": "Lunch"})
    assert created.status_code == 201
    order = created.json()
    assert order["customer_name"] == "John Doe"
    assert order["order_date"] is not None
    assert client.get(f'/orders/{order["id"]}').status_code == 200
    updated = client.put(f'/orders/{order["id"]}', json={"description": "Afternoon snack"})
    assert updated.status_code == 200
    assert updated.json()["description"] == "Afternoon snack"
    deleted = client.delete(f'/orders/{order["id"]}')
    assert deleted.status_code == 204
    assert deleted.content == b""
    assert client.get(f'/orders/{order["id"]}').status_code == 404
