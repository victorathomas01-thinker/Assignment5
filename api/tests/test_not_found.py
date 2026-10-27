import pytest


@pytest.mark.parametrize(
    "table",
    ["sandwiches", "resources", "recipes", "order_details"]
)
def test_missing_record_returns_404(client, table):
    response = client.get(f"/{table}/999999")
    assert response.status_code == 404
