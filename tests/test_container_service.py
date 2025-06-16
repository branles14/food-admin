from src.services import container_service, product_service


def setup_product(conn):
    return product_service.create_product(
        conn,
        {
            "name": "Milk",
            "upc": "456",
            "uuid": "uuid2",
            "nutrition": {"calories": 100},
        },
    )


def test_create_list_update_delete_container(db_conn):
    product = setup_product(db_conn)

    container = container_service.create_container(
        db_conn,
        db_conn,
        {
            "product": product["id"],
            "quantity": 1,
            "opened": False,
            "remaining": 1.0,
            "expiration_date": "2025-01-01",
            "location": "pantry",
            "tags": ["dairy"],
            "container_weight": 200,
        },
    )
    assert container["product"]["id"] == product["id"]
    assert container["quantity"] == 1
    assert container["tags"] == ["dairy"]
    assert container["container_weight"] == 200

    containers = container_service.list_containers(db_conn, db_conn)
    assert len(containers) == 1

    updated = container_service.update_container(
        db_conn,
        db_conn,
        container["id"],
        {"remaining": 0.5, "tags": ["dairy", "open"], "container_weight": 250},
    )
    assert updated["remaining"] == 0.5
    assert updated["tags"] == ["dairy", "open"]
    assert updated["container_weight"] == 250

    result = container_service.delete_container(db_conn, container["id"])
    assert result is True
    assert container_service.list_containers(db_conn, db_conn) == []


def test_update_container_all_fields(db_conn):
    prod1 = setup_product(db_conn)
    prod2 = product_service.create_product(
        db_conn,
        {"name": "Yogurt", "upc": "789", "uuid": "uuid3", "nutrition": None},
    )

    container = container_service.create_container(
        db_conn,
        db_conn,
        {
            "product": prod1["id"],
            "quantity": 1,
            "opened": False,
            "remaining": 1.0,
            "expiration_date": "2025-01-01",
            "location": "fridge",
            "tags": ["dairy"],
            "container_weight": 200,
        },
    )

    updated = container_service.update_container(
        db_conn,
        db_conn,
        container["id"],
        {
            "product": prod2["id"],
            "quantity": 2,
            "opened": True,
            "remaining": 0.5,
            "uuid": container["uuid"],
            "expiration_date": "2026-01-01",
            "location": "pantry",
            "tags": ["cultured"],
            "container_weight": 250,
        },
    )

    assert updated["product"]["id"] == prod2["id"]
    assert updated["quantity"] == 2
    assert bool(updated["opened"]) is True
    assert updated["remaining"] == 0.5
    assert updated["expiration_date"] == "2026-01-01"
    assert updated["location"] == "pantry"
    assert updated["tags"] == ["cultured"]
    assert updated["container_weight"] == 250
