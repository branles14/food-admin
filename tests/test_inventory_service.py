import pytest
from src.services import inventory_service, product_info_service


def setup_product(db):
    return product_info_service.create_product_info(
        db,
        {
            "name": "Milk",
            "upc": "456",
            "container_info": {"net_weight_g": 100, "empty_container_weight_g": 10},
            "nutrition": {"serving": {"size_g": 240, "calories": 100}},
        },
    )


def test_create_and_group_units(inventory_db, product_db):
    prod = setup_product(product_db)
    item1 = inventory_service.create_item(
        inventory_db,
        product_db,
        {"product": prod["product_id"], "opened": True},
    )
    assert len(item1["units"]) == 1
    assert item1["units"][0]["weight_g"] == 110

    item2 = inventory_service.create_item(
        inventory_db,
        product_db,
        {"product": prod["product_id"], "expiration_date": "2025-01-01"},
    )
    assert item2["id"] == item1["id"]
    assert len(item2["units"]) == 2

    items = inventory_service.list_items(inventory_db)
    assert len(items) == 1
    assert len(items[0]["units"]) == 2


def test_quantity_parameter(inventory_db, product_db):
    prod = setup_product(product_db)
    item = inventory_service.create_item(
        inventory_db,
        product_db,
        {"product": prod["product_id"], "quantity": 2},
    )
    assert len(item["units"]) == 2
    for unit in item["units"]:
        assert unit["weight_g"] == 110
