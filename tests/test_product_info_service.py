from src.services import product_info_service


def test_create_list_update_delete_product(db_conn):
    data = {
        "name": "Cheese",
        "upc": "123",
        "uuid": "uuid1",
        "nutrition": {"calories": 50},
    }
    created = product_info_service.create_product_info(db_conn, data)
    assert created["name"] == "Cheese"
    assert created["nutrition"] == {"calories": 50}

    products = product_info_service.list_product_info(db_conn)
    assert len(products) == 1

    updated = product_info_service.update_product_info(
        db_conn, created["id"], {"name": "Cheddar"}
    )
    assert updated["name"] == "Cheddar"

    result = product_info_service.delete_product_info(db_conn, created["id"])
    assert result is True
    assert product_info_service.list_product_info(db_conn) == []
