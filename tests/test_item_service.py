import pytest

from src.services import inventory_service, product_info_service


def setup_product(db):
    return product_info_service.create_product_info(
        db,
        {
            "name": "Milk",
            "upc": "456",
            "uuid": "uuid2",
            "nutrition": {"serving": {"size_g": 240, "calories": 100}},
        },
    )


def test_create_list_update_delete_item(inventory_db, product_db):
    prod_info = setup_product(product_db)

    item = inventory_service.create_item(
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

    products = inventory_service.list_items(inventory_db, product_db)
    assert len(products) == 1

    updated = inventory_service.update_item(
        inventory_db,
        product_db,
        item["id"],
        {"remaining": 0.5, "tags": ["dairy", "open"], "container_weight": 250},
    )
    assert updated["remaining"] == 0.5
    assert updated["tags"] == ["dairy", "open"]
    assert updated["container_weight"] == 250

    result = inventory_service.delete_item(inventory_db, item["id"])
    assert result is True
    assert inventory_service.list_items(inventory_db, product_db) == []


def test_update_item_all_fields(inventory_db, product_db):
    prod1 = setup_product(product_db)
    prod2 = product_info_service.create_product_info(
        product_db,
        {"name": "Yogurt", "upc": "789", "uuid": "uuid3", "nutrition": None},
    )

    item = inventory_service.create_item(
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

    updated = inventory_service.update_item(
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


def test_create_item_requires_upc(inventory_db, product_db):
    with pytest.raises(ValueError):
        inventory_service.create_item(
            inventory_db,
            product_db,
            {"product": "1", "quantity": 1},
        )


def test_create_item_with_upc_lookup(inventory_db, product_db):
    prod = setup_product(product_db)
    item = inventory_service.create_item(
        inventory_db,
        product_db,
        {"upc": prod["upc"], "quantity": 1},
    )
    assert item["product_info"]["id"] == prod["id"]


def test_create_item_unknown_upc_needs_name(inventory_db, product_db):
    with pytest.raises(ValueError):
        inventory_service.create_item(
            inventory_db,
            product_db,
            {"upc": "999", "quantity": 1},
        )


def test_create_item_defaults(inventory_db, product_db):
    prod_info = setup_product(product_db)
    item = inventory_service.create_item(
        inventory_db,
        product_db,
        {"product": prod_info["id"]},
    )
    assert item["quantity"] == 1
    assert bool(item["opened"]) is False
    assert len(item["uuid"]) <= 22


def test_uuid_helpers(inventory_db, product_db):
    prod_info = setup_product(product_db)
    uuid = "item-uuid"
    item = inventory_service.create_item(
        inventory_db,
        product_db,
        {"product": prod_info["id"], "uuid": uuid, "quantity": 1},
    )

    fetched = inventory_service.get_item_by_uuid(inventory_db, product_db, uuid)
    assert fetched["id"] == item["id"]

    updated = inventory_service.update_item_by_uuid(
        inventory_db,
        product_db,
        uuid,
        {"quantity": 3},
    )
    assert updated["quantity"] == 3

    deleted = inventory_service.delete_item_by_uuid(inventory_db, uuid)
    assert deleted is True
    assert inventory_service.get_item_by_uuid(inventory_db, product_db, uuid) is None


def test_consume_item(inventory_db, product_db):
    prod = setup_product(product_db)
    item = inventory_service.create_item(
        inventory_db,
        product_db,
        {"product": prod["id"], "remaining": 1.0},
    )

    updated = inventory_service.consume_item(inventory_db, product_db, item["id"], 0.25)
    assert updated["remaining"] == 0.75
    fetched = inventory_service.get_item_by_id(inventory_db, product_db, item["id"])
    assert fetched["remaining"] == 0.75


def test_create_item_adds_tags_to_new_product(inventory_db, product_db):
    tags = ["organic", "snack"]
    inventory_service.create_item(
        inventory_db,
        product_db,
        {"upc": "99999", "name": "Chips", "tags": tags},
    )

    prod_info = product_info_service.get_product_info_by_upc(product_db, "99999")
    assert prod_info["tags"] == tags
