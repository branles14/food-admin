from __future__ import annotations

import json
from typing import Any, Dict, List, Optional
from uuid import uuid4

from src.db import JsonlDB
from . import product_info_service


def _normalize(
    prod_db: JsonlDB, row: Optional[Dict[str, Any]]
) -> Optional[Dict[str, Any]]:
    if row is None:
        return None
    data = dict(row)
    product_id = data.pop("product_id", None)
    if product_id is not None:
        data["product_info"] = product_info_service.get_product_info_by_id(
            prod_db, product_id
        )
    if "tags" in data and data["tags"] is not None:
        data["tags"] = json.loads(json.dumps(data["tags"]))
    return data


def _next_id(rows: List[Dict[str, Any]]) -> int:
    return max((r.get("id", 0) for r in rows), default=0) + 1


def create_item(
    inv_db: JsonlDB, prod_db: JsonlDB, data: Dict[str, Any]
) -> Dict[str, Any]:
    items = inv_db.read_all()
    data = data.copy()
    product = data.get("product")
    upc = data.get("upc")
    name = data.get("name")
    if isinstance(product, dict):
        if product.get("id") is not None:
            product_id = int(product.get("id"))
            info = product_info_service.get_product_info_by_id(prod_db, product_id)
            if info is None:
                raise ValueError("Product not found")
            upc = upc or info.get("upc")
            name = name or info.get("name")
        else:
            product_id = None
            upc = upc or product.get("upc")
            name = name or product.get("name")
    elif product is not None:
        product_id = int(product)
        info = product_info_service.get_product_info_by_id(prod_db, product_id)
        if info is None:
            raise ValueError("Product not found")
        upc = upc or info.get("upc")
        name = name or info.get("name")
    else:
        product_id = None

    if product_id is None:
        if not upc:
            raise ValueError("UPC required for new item")
        existing = product_info_service.get_product_info_by_upc(prod_db, upc)
        if existing:
            product_id = existing["id"]
            name = name or existing.get("name")
        else:
            if not name:
                raise ValueError("Name required for unknown UPC")
            new_prod = product_info_service.create_product_info(
                prod_db, {"name": name, "upc": upc}
            )
            product_id = new_prod["id"]
    data.setdefault("uuid", str(uuid4()))
    item = {
        "id": _next_id(items),
        "product_id": product_id,
        "quantity": data.get("quantity"),
        "opened": data.get("opened"),
        "remaining": data.get("remaining"),
        "uuid": data.get("uuid"),
        "expiration_date": data.get("expiration_date"),
        "location": data.get("location"),
        "tags": data.get("tags"),
        "container_weight": data.get("container_weight"),
    }
    items.append(item)
    inv_db.write_all(items)
    return _normalize(prod_db, item)


def get_item_by_id(
    inv_db: JsonlDB, prod_db: JsonlDB, id_: Any
) -> Optional[Dict[str, Any]]:
    items = inv_db.read_all()
    for row in items:
        if row.get("id") == int(id_):
            return _normalize(prod_db, row)
    return None


def list_items(inv_db: JsonlDB, prod_db: JsonlDB) -> List[Dict[str, Any]]:
    return [_normalize(prod_db, row) for row in inv_db.read_all()]


def update_item(
    inv_db: JsonlDB, prod_db: JsonlDB, id_: Any, data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    items = inv_db.read_all()
    updated = None
    for row in items:
        if row.get("id") == int(id_):
            if "product" in data:
                prod = data["product"]
                if isinstance(prod, dict):
                    prod = prod.get("id")
                row["product_id"] = int(prod) if prod is not None else None
            if "quantity" in data:
                row["quantity"] = data["quantity"]
            if "opened" in data:
                row["opened"] = data["opened"]
            if "remaining" in data:
                row["remaining"] = data["remaining"]
            if "uuid" in data:
                row["uuid"] = data["uuid"]
            if "expiration_date" in data:
                row["expiration_date"] = data["expiration_date"]
            if "location" in data:
                row["location"] = data["location"]
            if "tags" in data:
                row["tags"] = data["tags"]
            if "container_weight" in data:
                row["container_weight"] = data["container_weight"]
            updated = row
            break
    if updated is None:
        return None
    inv_db.write_all(items)
    return _normalize(prod_db, updated)


def delete_item(inv_db: JsonlDB, id_: Any) -> bool:
    items = inv_db.read_all()
    new_items = [row for row in items if row.get("id") != int(id_)]
    if len(new_items) == len(items):
        return False
    inv_db.write_all(new_items)
    return True
