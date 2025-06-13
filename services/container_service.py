from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import uuid4

from db import get_db
from . import product_service


def _normalize(row: Optional[Any]) -> Optional[Dict[str, Any]]:
    if row is None:
        return None
    data = dict(row)
    product_id = data.pop("product_id", None)
    if product_id is not None:
        data["product"] = product_service.get_product_by_id(product_id)
    if "uuid" in data:
        data["uuid"] = data["uuid"]
    return data


def create_container(data: Dict[str, Any]) -> Dict[str, Any]:
    conn = get_db()
    data = data.copy()
    product = data.get("product")
    if isinstance(product, dict):
        product_id = int(product.get("id"))
    elif product is not None:
        product_id = int(product)
    else:
        product_id = None
    data.setdefault("uuid", str(uuid4()))
    cur = conn.execute(
        "INSERT INTO containers (product_id, quantity, opened, remaining, uuid) VALUES (?, ?, ?, ?, ?)",
        (
            product_id,
            data.get("quantity"),
            data.get("opened"),
            data.get("remaining"),
            data.get("uuid"),
        ),
    )
    conn.commit()
    return get_container_by_id(cur.lastrowid)


def get_container_by_id(id_: Any) -> Optional[Dict[str, Any]]:
    conn = get_db()
    cur = conn.execute("SELECT * FROM containers WHERE id = ?", (int(id_),))
    row = cur.fetchone()
    return _normalize(row)


def list_containers() -> List[Dict[str, Any]]:
    conn = get_db()
    cur = conn.execute("SELECT * FROM containers")
    return [_normalize(row) for row in cur.fetchall()]


def update_container(id_: Any, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    conn = get_db()
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
    if not fields:
        return get_container_by_id(id_)
    values.append(int(id_))
    conn.execute(f"UPDATE containers SET {', '.join(fields)} WHERE id = ?", values)
    conn.commit()
    return get_container_by_id(id_)


def delete_container(id_: Any) -> bool:
    conn = get_db()
    cur = conn.execute("DELETE FROM containers WHERE id = ?", (int(id_),))
    conn.commit()
    return cur.rowcount == 1
