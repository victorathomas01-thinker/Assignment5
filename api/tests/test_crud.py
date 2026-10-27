"""Tests for the 20 added endpoints and database error handling."""
import pytest


@pytest.mark.parametrize(
    "table, payload, patch, key, expected",
    [
        ("sandwiches", {"sandwich_name": "Turkey", "price": 7.50}, {"price": 8.75}, "price", 8.75),
        ("resources", {"item": "Bread", "amount": 30}, {"amount": 25}, "amount", 25),
    ],
)
def test_basic_crud(client, table, payload, patch, key, expected):
    assert client.get(f"/{table}/").json() == []
    response = client.post(f"/{table}/", json=payload)
    assert response.status_code == 201, response.text
    item_id = response.json()["id"]
    assert client.get(f"/{table}/{item_id}").json()[key] == payload[key]
    assert len(client.get(f"/{table}/").json()) == 1
    response = client.put(f"/{table}/{item_id}", json=patch)
    assert response.status_code == 200, response.text
    assert response.json()[key] == expected
    assert client.delete(f"/{table}/{item_id}").status_code == 204
    assert client.get(f"/{table}/{item_id}").status_code == 404
    assert client.put(f"/{table}/{item_id}", json=patch).status_code == 404
    assert client.delete(f"/{table}/{item_id}").status_code == 404


def make_related_records(client):
    sandwich = client.post("/sandwiches/", json={"sandwich_name": "Veggie", "price": 5.95}).json()
    resource = client.post("/resources/", json={"item": "Lettuce", "amount": 50}).json()
    order = client.post("/orders/", json={"customer_name": "Ada", "description": "No mayo"}).json()
    return sandwich["id"], resource["id"], order["id"]


def test_recipes_crud(client):
    sandwich_id, resource_id, _ = make_related_records(client)
    data = {"sandwich_id": sandwich_id, "resource_id": resource_id, "amount": 2}
    created = client.post("/recipes/", json=data)
    assert created.status_code == 201, created.text
    recipe_id = created.json()["id"]
    assert created.json()["sandwich"]["sandwich_name"] == "Veggie"
    assert created.json()["resource"]["item"] == "Lettuce"
    assert client.get(f"/recipes/{recipe_id}").json()["resource_id"] == resource_id
    assert len(client.get("/recipes/").json()) == 1
    updated = client.put(f"/recipes/{recipe_id}", json={"amount": 3})
    assert updated.status_code == 200, updated.text
    assert updated.json()["amount"] == 3
    assert client.delete(f"/recipes/{recipe_id}").status_code == 204
    assert client.get(f"/recipes/{recipe_id}").status_code == 404
    assert client.put(f"/recipes/{recipe_id}", json={"amount": 4}).status_code == 404
    assert client.delete(f"/recipes/{recipe_id}").status_code == 404


def test_order_details_crud(client):
    sandwich_id, _, order_id = make_related_records(client)
    data = {"order_id": order_id, "sandwich_id": sandwich_id, "amount": 2}
    created = client.post("/order_details/", json=data)
    assert created.status_code == 201, created.text
    detail_id = created.json()["id"]
    assert created.json()["sandwich_id"] == sandwich_id
    assert client.get(f"/order_details/{detail_id}").json()["order_id"] == order_id
    assert len(client.get("/order_details/").json()) == 1
    updated = client.put(f"/order_details/{detail_id}", json={"amount": 3})
    assert updated.status_code == 200, updated.text
    assert updated.json()["amount"] == 3
    assert client.get(f"/orders/{order_id}").json()["order_details"][0]["amount"] == 3
    assert client.delete(f"/order_details/{detail_id}").status_code == 204
    assert client.get(f"/order_details/{detail_id}").status_code == 404
    assert client.put(f"/order_details/{detail_id}", json={"amount": 4}).status_code == 404
    assert client.delete(f"/order_details/{detail_id}").status_code == 404


def test_duplicate_unique_values_return_conflict(client):
    data = {"sandwich_name": "Cheese", "price": 5.00}
    assert client.post("/sandwiches/", json=data).status_code == 201
    assert client.post("/sandwiches/", json=data).status_code == 409
    assert client.get("/sandwiches/").status_code == 200  # transaction rolled back
    resource = {"item": "Tomato", "amount": 20}
    assert client.post("/resources/", json=resource).status_code == 201
    assert client.post("/resources/", json=resource).status_code == 409


def test_foreign_key_conflict_and_validation(client):
    assert client.post("/recipes/", json={"sandwich_id": 999, "resource_id": 888, "amount": 1}).status_code == 409
    assert client.post("/order_details/", json={"order_id": 999, "sandwich_id": 888, "amount": 1}).status_code == 409
    assert client.post("/sandwiches/", json={"sandwich_name": "Bad", "price": -1}).status_code == 422
    sandwich_id, resource_id, order_id = make_related_records(client)
    assert client.post("/recipes/", json={"sandwich_id": sandwich_id, "resource_id": resource_id, "amount": 1}).status_code == 201
    # Parent cannot be deleted while a dependent recipe still refers to it.
    assert client.delete(f"/resources/{resource_id}").status_code == 409
    assert client.get(f"/resources/{resource_id}").status_code == 200
    assert client.post("/order_details/", json={"order_id": order_id, "sandwich_id": sandwich_id, "amount": 1}).status_code == 201


def test_api_docs_expose_all_five_tables(client):
    schema = client.get("/openapi.json").json()
    ids = {
        "orders": "order", "sandwiches": "sandwich", "resources": "resource",
        "recipes": "recipe", "order_details": "order_detail",
    }
    for table, singular in ids.items():
        assert set(schema["paths"][f"/{table}/"].keys()) == {"get", "post"}
        assert set(schema["paths"][f"/{table}/{{{singular}_id}}"].keys()) == {"get", "put", "delete"}


def test_editing_relationships_and_unique_name_conflicts(client):
    sandwich_id, resource_id, order_id = make_related_records(client)
    other_sandwich = client.post("/sandwiches/", json={"sandwich_name": "Ham", "price": 6.50}).json()
    other_resource = client.post("/resources/", json={"item": "Cheese", "amount": 10}).json()
    another_order = client.post("/orders/", json={"customer_name": "Lin"}).json()
    recipe = client.post("/recipes/", json={"sandwich_id": sandwich_id, "resource_id": resource_id, "amount": 2}).json()
    detail = client.post("/order_details/", json={"sandwich_id": sandwich_id, "order_id": order_id, "amount": 1}).json()

    changed_recipe = client.put(
        f'/recipes/{recipe["id"]}',
        json={"sandwich_id": other_sandwich["id"], "resource_id": other_resource["id"]},
    )
    assert changed_recipe.status_code == 200, changed_recipe.text
    assert changed_recipe.json()["sandwich"]["sandwich_name"] == "Ham"
    assert changed_recipe.json()["resource"]["item"] == "Cheese"

    changed_detail = client.put(
        f'/order_details/{detail["id"]}',
        json={"order_id": another_order["id"], "sandwich_id": other_sandwich["id"]},
    )
    assert changed_detail.status_code == 200, changed_detail.text
    assert changed_detail.json()["sandwich"]["sandwich_name"] == "Ham"
    assert changed_detail.json()["order_id"] == another_order["id"]

    # Violating a unique constraint returns 409 and leaves the old value intact.
    rejected = client.put(f'/sandwiches/{sandwich_id}', json={"sandwich_name": "Ham"})
    assert rejected.status_code == 409
    assert client.get(f'/sandwiches/{sandwich_id}').json()["sandwich_name"] == "Veggie"
    rejected = client.put(f'/recipes/{recipe["id"]}', json={"resource_id": 123456})
    assert rejected.status_code == 409
    assert client.get(f'/recipes/{recipe["id"]}').json()["resource_id"] == other_resource["id"]
