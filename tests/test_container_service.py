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

    containers = container_service.list_containers(db_conn)
    assert len(containers) == 1

    updated = container_service.update_container(
        db_conn,
        container["id"],
        {"remaining": 0.5, "tags": ["dairy", "open"], "container_weight": 250},
    )
    assert updated["remaining"] == 0.5
    assert updated["tags"] == ["dairy", "open"]
    assert updated["container_weight"] == 250

    result = container_service.delete_container(db_conn, container["id"])
    assert result is True
    assert container_service.list_containers(db_conn) == []
