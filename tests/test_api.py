from fastapi.testclient import TestClient

from src.api.app import app, db_conn as app_db_conn
from src.services import product_service


# reuse db_conn fixture from conftest


def test_container_api_crud(db_conn):
    # Override dependency to use in-memory db
    app.dependency_overrides[app_db_conn] = lambda: db_conn
    client = TestClient(app)

    # create product for container reference
    product = product_service.create_product(
        db_conn,
        {
            "name": "Bread",
            "upc": "111",
            "uuid": "uuid",
            "nutrition": {"cals": 50},
        },
    )

    # create container
    resp = client.post(
        "/containers",
        json={
            "product": product["id"],
            "quantity": 1,
            "tags": ["baked"],
            "container_weight": 100,
        },
    )
    assert resp.status_code == 201
    container = resp.json()
    assert container["product"]["id"] == product["id"]
    container_id = container["id"]

    # list containers
    resp = client.get("/containers")
    assert resp.status_code == 200
    assert len(resp.json()) == 1

    # update container
    resp = client.patch(
        f"/containers/{container_id}",
        json={"quantity": 2, "tags": ["baked", "fresh"]},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["quantity"] == 2
    assert data["tags"] == ["baked", "fresh"]

    # delete container
    resp = client.delete(f"/containers/{container_id}")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Container deleted"

    # verify deleted
    assert client.get("/containers").json() == []

    app.dependency_overrides.clear()
