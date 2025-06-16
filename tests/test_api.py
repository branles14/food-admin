from fastapi.testclient import TestClient

from src.api.app import (
    app,
    inventory_conn as app_inventory_conn,
    product_conn as app_product_conn,
)
from src.services import item_service, product_info_service


# reuse JSONL fixtures from conftest


def test_product_api_crud(inventory_db, product_db):
    # Override dependencies to use in-memory db
    app.dependency_overrides[app_inventory_conn] = lambda: inventory_db
    app.dependency_overrides[app_product_conn] = lambda: product_db
    client = TestClient(app)

    # create product info for reference
    prod_info = product_info_service.create_product_info(
        product_db,
        {
            "name": "Bread",
            "upc": "111",
            "uuid": "uuid",
            "nutrition": {"cals": 50},
        },
    )

    # create inventory product
    resp = client.post(
        "/inventory",
        json={
            "product": prod_info["id"],
            "quantity": 1,
            "tags": ["baked"],
            "container_weight": 100,
        },
    )
    assert resp.status_code == 201
    item = resp.json()
    assert item["product_info"]["id"] == prod_info["id"]
    item_id = item["id"]

    # list products
    resp = client.get("/inventory")
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    # update container
    resp = client.patch(
        f"/inventory/{item_id}",
        json={"quantity": 2, "tags": ["baked", "fresh"]},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["quantity"] == 2
    assert data["tags"] == ["baked", "fresh"]

    # delete product
    resp = client.delete(f"/inventory/{item_id}")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Item deleted"

    # verify deleted
    assert client.get("/inventory").json() == []

    app.dependency_overrides.clear()
