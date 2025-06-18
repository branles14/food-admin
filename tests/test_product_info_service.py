from src.services import product_info_service


from src.services import product_info_service


def test_create_list_update_delete_product(product_db):
    data = {
        "name": "Cheese",
        "upc": "123",
        "uuid": "uuid1",
        "nutrition": {"calories": 50},
        "tags": ["favorite"],
    }
    created = product_info_service.create_product_info(product_db, data)
    assert created["name"] == "Cheese"
    assert created["nutrition"] == {"calories": 50}
    assert created["tags"] == ["favorite"]

    products = product_info_service.list_product_info(product_db)
    assert len(products) == 1

    updated = product_info_service.update_product_info(
        product_db, created["id"], {"name": "Cheddar", "tags": ["canned"]}
    )
    assert updated["name"] == "Cheddar"
    assert updated["tags"] == ["canned"]

    result = product_info_service.delete_product_info(product_db, created["id"])
    assert result is True
    assert product_info_service.list_product_info(product_db) == []


def test_create_product_with_extra_nutrients(product_db):
    data = {
        "name": "Spinach",
        "upc": "999",
        "nutrition": {
            "calories": 23,
            "vitamin_a": 140,
            "vitamin_c": 28,
            "vitamin_k": 500,
            "unknown": 1,
        },
    }
    created = product_info_service.create_product_info(product_db, data)
    nutrition = created["nutrition"]
    assert "unknown" not in nutrition
    assert nutrition["vitamin_a"] == 140
    assert nutrition["vitamin_c"] == 28

    updated = product_info_service.update_product_info(
        product_db,
        created["id"],
        {"nutrition": {"vitamin_a": 150, "zinc": 2}},
    )
    assert updated["nutrition"] == {"vitamin_a": 150, "zinc": 2}


def test_product_key_order(product_db):
    data = {
        "name": "Juice",
        "upc": "321",
        "nutrition": {"calories": 80},
        "tags": ["cold"],
    }
    product_info_service.create_product_info(product_db, data)
    record = product_db.read_all()[0]
    assert list(record.keys()) == ["name", "upc", "id", "nutrition", "tags"]
