from src.services import product_service


def test_create_list_update_delete_product(db_conn):
    data = {
        "name": "Cheese",
        "upc": "123",
        "uuid": "uuid1",
        "nutrition": {"calories": 50},
    }
    created = product_service.create_product(db_conn, data)
    assert created["name"] == "Cheese"
    assert created["nutrition"] == {"calories": 50}

    products = product_service.list_products(db_conn)
    assert len(products) == 1

    updated = product_service.update_product(
        db_conn, created["id"], {"name": "Cheddar"}
    )
    assert updated["name"] == "Cheddar"

    result = product_service.delete_product(db_conn, created["id"])
    assert result is True
    assert product_service.list_products(db_conn) == []
