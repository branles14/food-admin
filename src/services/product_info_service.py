from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from src.utils.nutrition import filter_nutrition

import shortuuid

from src.db import JsonlDB


def _normalize(row: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if row is None:
        return None
    data = dict(row)
    if "nutrition" in data and data["nutrition"] is not None:
        data["nutrition"] = json.loads(json.dumps(data["nutrition"]))
    return data


def _next_id(rows: List[Dict[str, Any]]) -> int:
    return max((r.get("id", 0) for r in rows), default=0) + 1


def create_product_info(db: JsonlDB, data: Dict[str, Any]) -> Dict[str, Any]:
    rows = db.read_all()
    item = {
        "id": _next_id(rows),
        "name": data.get("name"),
        "upc": data.get("upc"),
        "uuid": data.get("uuid", shortuuid.uuid()),
        "nutrition": filter_nutrition(data.get("nutrition")),
    }
    rows.append(item)
    db.write_all(rows)
    return _normalize(item)


def get_product_info_by_id(db: JsonlDB, id_: Any) -> Optional[Dict[str, Any]]:
    rows = db.read_all()
    for row in rows:
        if row.get("id") == int(id_):
            return _normalize(row)
    return None


def get_product_info_by_upc(db: JsonlDB, upc: str) -> Optional[Dict[str, Any]]:
    rows = db.read_all()
    for row in rows:
        if row.get("upc") == upc:
            return _normalize(row)
    return None


def list_product_info(db: JsonlDB) -> List[Dict[str, Any]]:
    return [_normalize(row) for row in db.read_all()]


def update_product_info(
    db: JsonlDB, id_: Any, data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    rows = db.read_all()
    updated = None
    for row in rows:
        if row.get("id") == int(id_):
            row_update = data.copy()
            if "nutrition" in row_update:
                row_update["nutrition"] = filter_nutrition(row_update["nutrition"])
            row.update(row_update)
            updated = row
            break
    if updated is None:
        return None
    db.write_all(rows)
    return _normalize(updated)


def delete_product_info(db: JsonlDB, id_: Any) -> bool:
    rows = db.read_all()
    new_rows = [row for row in rows if row.get("id") != int(id_)]
    if len(new_rows) == len(rows):
        return False
    db.write_all(new_rows)
    return True
