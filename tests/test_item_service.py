from src.services import item_service, product_info_service


def setup_product(db):
    return product_info_service.create_product_info(
        db,
        {
            "name": "Milk",
            "upc": "456",
            "uuid": "uuid2",
            "nutrition": {"calories": 100},
        },
    )


def test_create_list_update_delete_item(inventory_db, product_db):
    prod_info = setup_product(product_db)

    item = item_service.create_item(
        inventory_db,
        product_db,
        {
            "product": prod_info["id"],
            "quantity": 1,
            "opened": False,
            "remaining": 1.0,
            "expiration_date": "2025-01-01",
            "location": "pantry",
            "tags": ["dairy"],
            "container_weight": 200,
        },
    )
    assert item["product_info"]["id"] == prod_info["id"]
    assert item["quantity"] == 1
    assert item["tags"] == ["dairy"]
    assert item["container_weight"] == 200

    products = item_service.list_items(inventory_db, product_db)
    assert len(products) == 1

    updated = item_service.update_item(
        inventory_db,
        product_db,
        item["id"],
        {"remaining": 0.5, "tags": ["dairy", "open"], "container_weight": 250},
    )
    assert updated["remaining"] == 0.5
    assert updated["tags"] == ["dairy", "open"]
    assert updated["container_weight"] == 250

    result = item_service.delete_item(inventory_db, item["id"])
    assert result is True
    assert item_service.list_items(inventory_db, product_db) == []


def test_update_item_all_fields(inventory_db, product_db):
    prod1 = setup_product(product_db)
    prod2 = item_service.create_item(
        product_db,
        product_db,
        {"name": "Yogurt", "upc": "789", "uuid": "uuid3", "nutrition": None},
    )

    item = item_service.create_item(
        inventory_db,
        product_db,
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

    updated = item_service.update_item(
        inventory_db,
        product_db,
        item["id"],
        {
            "product": prod2["id"],
            "quantity": 2,
            "opened": True,
            "remaining": 0.5,
            "uuid": item["uuid"],
            "expiration_date": "2026-01-01",
            "location": "pantry",
            "tags": ["cultured"],
            "container_weight": 250,
        },
    )

    assert updated["product_info"]["id"] == prod2["id"]
    assert updated["quantity"] == 2
    assert bool(updated["opened"]) is True
    assert updated["remaining"] == 0.5
    assert updated["expiration_date"] == "2026-01-01"
    assert updated["location"] == "pantry"
    assert updated["tags"] == ["cultured"]
    assert updated["container_weight"] == 250
