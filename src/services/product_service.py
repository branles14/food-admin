from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from sqlite3 import Connection


def _normalize(row: Optional[Any]) -> Optional[Dict[str, Any]]:
    if row is None:
        return None
    data = dict(row)
    if "nutrition" in data and data["nutrition"] is not None:
        data["nutrition"] = json.loads(data["nutrition"])
    return data


def create_product(conn: Connection, data: Dict[str, Any]) -> Dict[str, Any]:
    nutrition_value = data.get("nutrition")
    nutrition = json.dumps(nutrition_value) if nutrition_value else None
    # fmt: off
    query = (
        "INSERT INTO products (name, upc, uuid, nutrition) "
        "VALUES (?, ?, ?, ?)"
    )
    # fmt: on
    cur = conn.execute(
        query,
        (
            data.get("name"),
            data.get("upc"),
            data.get("uuid"),
            nutrition,
        ),
    )
    conn.commit()
    return get_product_by_id(conn, cur.lastrowid)


def get_product_by_id(conn: Connection, id_: Any) -> Optional[Dict[str, Any]]:
    cur = conn.execute("SELECT * FROM products WHERE id = ?", (int(id_),))
    row = cur.fetchone()
    return _normalize(row)


def list_products(conn: Connection) -> List[Dict[str, Any]]:
    cur = conn.execute("SELECT * FROM products")
    return [_normalize(row) for row in cur.fetchall()]


def update_product(
    conn: Connection, id_: Any, data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    fields = []
    values = []
    if "name" in data:
        fields.append("name = ?")
        values.append(data["name"])
    if "upc" in data:
        fields.append("upc = ?")
        values.append(data["upc"])
    if "uuid" in data:
        fields.append("uuid = ?")
        values.append(data["uuid"])
    if "nutrition" in data:
        fields.append("nutrition = ?")
        # fmt: off
        values.append(
            json.dumps(data["nutrition"]) if data["nutrition"] else None
        )
        # fmt: on
    if not fields:
        return get_product_by_id(conn, id_)
    values.append(int(id_))
    conn.execute(
        f"UPDATE products SET {', '.join(fields)} WHERE id = ?",
        values,
    )
    conn.commit()
    return get_product_by_id(conn, id_)


def delete_product(conn: Connection, id_: Any) -> bool:
    cur = conn.execute("DELETE FROM products WHERE id = ?", (int(id_),))
    conn.commit()
    return cur.rowcount == 1
