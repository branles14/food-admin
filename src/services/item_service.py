from __future__ import annotations

import json
from typing import Any, Dict, List, Optional
from uuid import uuid4
from sqlite3 import Connection

from . import product_info_service


def _normalize(prod_conn: Connection, row: Optional[Any]) -> Optional[Dict[str, Any]]:
    if row is None:
        return None
    data = dict(row)
    product_id = data.pop("product_id", None)
    if product_id is not None:
        data["product_info"] = product_info_service.get_product_info_by_id(
            prod_conn, product_id
        )
    if "tags" in data and data["tags"] is not None:
        data["tags"] = json.loads(data["tags"])
    if "uuid" in data:
        data["uuid"] = data["uuid"]
    return data


def create_item(
    inv_conn: Connection, prod_conn: Connection, data: Dict[str, Any]
) -> Dict[str, Any]:
    data = data.copy()
    product = data.get("product")
    if isinstance(product, dict):
        product_id = int(product.get("id"))
    elif product is not None:
        product_id = int(product)
    else:
        product_id = None
    data.setdefault("uuid", str(uuid4()))
    tag_value = data.get("tags")
    tags = json.dumps(tag_value) if tag_value is not None else None
    cur = inv_conn.execute(
        (
            "INSERT INTO inventory (product_id, quantity, opened, remaining, "
            "uuid, expiration_date, location, tags, container_weight)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        ),
        (
            product_id,
            data.get("quantity"),
            data.get("opened"),
            data.get("remaining"),
            data.get("uuid"),
            data.get("expiration_date"),
            data.get("location"),
            tags,
            data.get("container_weight"),
        ),
    )
    inv_conn.commit()
    return get_item_by_id(inv_conn, prod_conn, cur.lastrowid)


def get_item_by_id(
    inv_conn: Connection,
    prod_conn: Connection,
    id_: Any,
) -> Optional[Dict[str, Any]]:
    cur = inv_conn.execute("SELECT * FROM inventory WHERE id = ?", (int(id_),))
    row = cur.fetchone()
    return _normalize(prod_conn, row)


def list_items(inv_conn: Connection, prod_conn: Connection) -> List[Dict[str, Any]]:
    cur = inv_conn.execute("SELECT * FROM inventory")
    return [_normalize(prod_conn, row) for row in cur.fetchall()]


def update_item(
    inv_conn: Connection, prod_conn: Connection, id_: Any, data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    fields = []
    values = []
    if "product" in data:
        prod = data["product"]
        if isinstance(prod, dict):
            prod = prod.get("id")
        fields.append("product_id = ?")
        values.append(int(prod) if prod is not None else None)
    if "quantity" in data:
        fields.append("quantity = ?")
        values.append(data["quantity"])
    if "opened" in data:
        fields.append("opened = ?")
        values.append(data["opened"])
    if "remaining" in data:
        fields.append("remaining = ?")
        values.append(data["remaining"])
    if "uuid" in data:
        fields.append("uuid = ?")
        values.append(data["uuid"])
    if "expiration_date" in data:
        fields.append("expiration_date = ?")
        values.append(data["expiration_date"])
    if "location" in data:
        fields.append("location = ?")
        values.append(data["location"])
    if "tags" in data:
        fields.append("tags = ?")
        tag_value = data.get("tags")
        values.append(json.dumps(tag_value) if tag_value is not None else None)
    if "container_weight" in data:
        fields.append("container_weight = ?")
        values.append(data["container_weight"])
    if not fields:
        return get_item_by_id(inv_conn, prod_conn, id_)
    values.append(int(id_))
    inv_conn.execute(
        f"UPDATE inventory SET {', '.join(fields)} WHERE id = ?",
        values,
    )
    inv_conn.commit()
    return get_item_by_id(inv_conn, prod_conn, id_)


def delete_item(inv_conn: Connection, id_: Any) -> bool:
    cur = inv_conn.execute("DELETE FROM inventory WHERE id = ?", (int(id_),))
    inv_conn.commit()
    return cur.rowcount == 1
