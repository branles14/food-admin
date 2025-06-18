from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

import shortuuid

from src.db import JsonlDB
from . import product_info_service


def _normalize(row: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if row is None:
        return None
    data = json.loads(json.dumps(row))  # deep copy
    return data


def _next_id(rows: List[Dict[str, Any]]) -> int:
    return max((r.get("id", 0) for r in rows), default=0) + 1


def _find_item(
    items: List[Dict[str, Any]], product_id: str
) -> Optional[Dict[str, Any]]:
    for row in items:
        if row.get("product_id") == product_id:
            return row
    return None


def create_item(
    inv_db: JsonlDB, prod_db: JsonlDB, data: Dict[str, Any]
) -> Dict[str, Any]:
    items = inv_db.read_all()
    data = data.copy()

    product = data.get("product")
    upc = data.get("upc")
    name = data.get("name")
    container_info = data.get("container_info")
    nutrition = data.get("nutrition")
    tags = data.get("tags")

    if isinstance(product, dict):
        prod_id = product.get("product_id") or product.get("id")
        if prod_id is not None:
            info = product_info_service.get_product_info_by_id(prod_db, prod_id)
            if info is None:
                raise ValueError("Product not found")
            product_id = info["product_id"]
            upc = upc or info.get("upc")
            name = name or info.get("name")
            container_info = container_info or info.get("container_info")
            nutrition = nutrition or info.get("nutrition")
            tags = tags or info.get("tags")
        else:
            product_id = None
            upc = upc or product.get("upc")
            name = name or product.get("name")
            container_info = container_info or product.get("container_info")
            nutrition = nutrition or product.get("nutrition")
            tags = tags or product.get("tags")
    elif product is not None:
        product_id = str(product)
        info = product_info_service.get_product_info_by_id(prod_db, product_id)
        if info is None:
            raise ValueError("Product not found")
        upc = upc or info.get("upc")
        name = name or info.get("name")
        container_info = container_info or info.get("container_info")
        nutrition = nutrition or info.get("nutrition")
        tags = tags or info.get("tags")
    else:
        product_id = None

    if product_id is None:
        if not upc:
            raise ValueError("UPC required for new item")
        existing = product_info_service.get_product_info_by_upc(prod_db, upc)
        if existing:
            product_id = existing["product_id"]
            name = name or existing.get("name")
            container_info = container_info or existing.get("container_info")
            nutrition = nutrition or existing.get("nutrition")
            tags = tags or existing.get("tags")
        else:
            if not name:
                raise ValueError("Name required for unknown UPC")
            new_prod = product_info_service.create_product_info(
                prod_db,
                {
                    "name": name,
                    "upc": upc,
                    "container_info": container_info,
                    "nutrition": nutrition,
                    "tags": tags,
                },
            )
            product_id = new_prod["product_id"]
            container_info = new_prod.get("container_info")
            nutrition = new_prod.get("nutrition")
            tags = new_prod.get("tags")

    unit_weight = data.get("weight_g")
    if unit_weight is None and container_info:
        net = container_info.get("net_weight_g")
        empty = container_info.get("empty_container_weight_g")
        if net is not None and empty is not None:
            unit_weight = net + empty

    quantity = int(data.get("quantity", 1))

    item = _find_item(items, product_id)
    if item is None:
        item = {
            "id": _next_id(items),
            "product_id": product_id,
            "name": name,
            "upc": upc,
            "tags": tags,
            "container_info": container_info,
            "nutrition": nutrition,
            "units": [],
        }
        items.append(item)

    units = item.setdefault("units", [])
    for i in range(quantity):
        units.append(
            {
                "uuid": (
                    data.get("uuid", shortuuid.uuid()) if i == 0 else shortuuid.uuid()
                ),
                "opened": data.get("opened", False),
                "weight_g": unit_weight,
                "expiration_date": data.get("expiration_date"),
            }
        )
    inv_db.write_all(items)
    return _normalize(item)


def list_items(inv_db: JsonlDB) -> List[Dict[str, Any]]:
    return [_normalize(row) for row in inv_db.read_all()]


def get_item_by_id(inv_db: JsonlDB, id_: Any) -> Optional[Dict[str, Any]]:
    items = inv_db.read_all()
    for row in items:
        if row.get("id") == int(id_):
            return _normalize(row)
    return None


def get_item_by_unit_uuid(inv_db: JsonlDB, uuid: str) -> Optional[Dict[str, Any]]:
    items = inv_db.read_all()
    for row in items:
        for unit in row.get("units", []):
            if str(unit.get("uuid")) == str(uuid):
                return _normalize(row)
    return None
