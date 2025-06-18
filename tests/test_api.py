from fastapi.testclient import TestClient

from src.api.app import (
    app,
    inventory_conn as app_inventory_conn,
    product_conn as app_product_conn,
)
from src.services import product_info_service


def setup_product(db):
    return product_info_service.create_product_info(
        db,
        {
            "name": "Bread",
            "upc": "111",
            "container_info": {"net_weight_g": 100, "empty_container_weight_g": 5},
        },
    )


def test_create_and_list(inventory_db, product_db):
    app.dependency_overrides[app_inventory_conn] = lambda: inventory_db
    app.dependency_overrides[app_product_conn] = lambda: product_db
    client = TestClient(app)

    prod = setup_product(product_db)
    resp = client.post(
        "/inventory",
        json={"product": prod["product_id"]},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["product_id"] == prod["product_id"]
    assert len(data["units"]) == 1

    resp = client.get("/inventory")
    assert resp.status_code == 200
    result = resp.json()
    assert len(result) == 1
    assert result[0]["product_id"] == prod["product_id"]

    app.dependency_overrides.clear()


def test_create_item_with_quantity(inventory_db, product_db):
    app.dependency_overrides[app_inventory_conn] = lambda: inventory_db
    app.dependency_overrides[app_product_conn] = lambda: product_db
    client = TestClient(app)

    prod = setup_product(product_db)
    resp = client.post(
        "/inventory",
        json={"product": prod["product_id"], "quantity": 2},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert len(data["units"]) == 2

    app.dependency_overrides.clear()
