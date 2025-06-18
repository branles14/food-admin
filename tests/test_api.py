from fastapi.testclient import TestClient

from src.api.app import (
    app,
    inventory_conn as app_inventory_conn,
    product_conn as app_product_conn,
)
from src.services import inventory_service, product_info_service


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
            "nutrition": {"serving": {"calories": 50}},
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
    assert client.get("/inventory").json() == {"message": "Inventory empty"}

    app.dependency_overrides.clear()


def test_create_item_requires_upc_via_api(inventory_db, product_db):
    app.dependency_overrides[app_inventory_conn] = lambda: inventory_db
    app.dependency_overrides[app_product_conn] = lambda: product_db
    client = TestClient(app)

    resp = client.post("/inventory", json={"product": "1", "quantity": 1})
    assert resp.status_code == 400

    app.dependency_overrides.clear()


def test_create_item_with_upc_lookup_via_api(inventory_db, product_db):
    app.dependency_overrides[app_inventory_conn] = lambda: inventory_db
    app.dependency_overrides[app_product_conn] = lambda: product_db
    client = TestClient(app)

    prod = product_info_service.create_product_info(
        product_db, {"name": "Apple", "upc": "222"}
    )

    resp = client.post("/inventory", json={"upc": prod["upc"], "quantity": 1})
    assert resp.status_code == 201
    assert resp.json()["product_info"]["id"] == prod["id"]

    app.dependency_overrides.clear()


def test_create_item_with_quantity_two_via_api(inventory_db, product_db):
    app.dependency_overrides[app_inventory_conn] = lambda: inventory_db
    app.dependency_overrides[app_product_conn] = lambda: product_db
    client = TestClient(app)

    prod = product_info_service.create_product_info(
        product_db, {"name": "Peanut Butter", "upc": "051500245453"}
    )

    resp = client.post("/inventory", json={"upc": prod["upc"], "quantity": 2})
    assert resp.status_code == 201
    data = resp.json()
    assert data["quantity"] == 2
    assert data["product_info"]["id"] == prod["id"]

    app.dependency_overrides.clear()


def test_create_item_unknown_upc_needs_name_via_api(inventory_db, product_db):
    app.dependency_overrides[app_inventory_conn] = lambda: inventory_db
    app.dependency_overrides[app_product_conn] = lambda: product_db
    client = TestClient(app)

    resp = client.post("/inventory", json={"upc": "999", "quantity": 1})
    assert resp.status_code == 400

    app.dependency_overrides.clear()


def test_inventory_empty_when_file_missing(inventory_db, product_db):
    app.dependency_overrides[app_inventory_conn] = lambda: inventory_db
    app.dependency_overrides[app_product_conn] = lambda: product_db
    inventory_db.path.unlink()
    client = TestClient(app)
    resp = client.get("/inventory")
    assert resp.status_code == 200
    assert resp.json() == {"message": "Inventory empty"}
    prod = product_info_service.create_product_info(
        product_db, {"name": "Rice", "upc": "333"}
    )
    resp = client.post(
        "/inventory",
        json={"product": prod["id"], "quantity": 1},
    )
    assert resp.status_code == 201
    assert inventory_db.path.exists()
    app.dependency_overrides.clear()


def test_inventory_empty_when_file_has_brackets(inventory_db, product_db):
    app.dependency_overrides[app_inventory_conn] = lambda: inventory_db
    app.dependency_overrides[app_product_conn] = lambda: product_db
    inventory_db.path.write_text("[]\n")
    client = TestClient(app)
    resp = client.get("/inventory")
    assert resp.status_code == 200
    assert resp.json() == {"message": "Inventory empty"}
    app.dependency_overrides.clear()


def test_create_item_defaults_via_api(inventory_db, product_db):
    app.dependency_overrides[app_inventory_conn] = lambda: inventory_db
    app.dependency_overrides[app_product_conn] = lambda: product_db
    client = TestClient(app)

    prod = product_info_service.create_product_info(
        product_db,
        {"name": "Egg", "upc": "444"},
    )

    resp = client.post("/inventory", json={"product": prod["id"]})
    assert resp.status_code == 201
    data = resp.json()
    assert data["quantity"] == 1
    assert bool(data["opened"]) is False
    assert len(data["uuid"]) <= 22

    app.dependency_overrides.clear()


def test_uuid_routes(inventory_db, product_db):
    app.dependency_overrides[app_inventory_conn] = lambda: inventory_db
    app.dependency_overrides[app_product_conn] = lambda: product_db
    client = TestClient(app)

    prod = product_info_service.create_product_info(
        product_db,
        {"name": "Juice", "upc": "555"},
    )

    item = inventory_service.create_item(
        inventory_db,
        product_db,
        {"product": prod["id"], "uuid": "abc"},
    )

    resp = client.get(f"/inventory/uuid/{item['uuid']}")
    assert resp.status_code == 200
    assert resp.json()["id"] == item["id"]

    resp = client.patch(
        f"/inventory/uuid/{item['uuid']}",
        json={"quantity": 7},
    )
    assert resp.status_code == 200
    assert resp.json()["quantity"] == 7

    resp = client.delete(f"/inventory/uuid/{item['uuid']}")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Item deleted"

    app.dependency_overrides.clear()


def test_consume_route(inventory_db, product_db):
    app.dependency_overrides[app_inventory_conn] = lambda: inventory_db
    app.dependency_overrides[app_product_conn] = lambda: product_db
    client = TestClient(app)

    prod = product_info_service.create_product_info(
        product_db,
        {"name": "Soup", "upc": "666"},
    )

    item = inventory_service.create_item(
        inventory_db,
        product_db,
        {"product": prod["id"], "remaining": 1.0},
    )

    resp = client.post(
        f"/inventory/{item['id']}/consume",
        json={"amount": 0.5},
    )
    assert resp.status_code == 200
    assert resp.json()["remaining"] == 0.5

    app.dependency_overrides.clear()
