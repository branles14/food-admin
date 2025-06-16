"""JSONL database access helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from src import config


class JsonlDB:
    """Lightweight JSON Lines storage."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.touch()

    def read_all(self) -> List[Dict[str, Any]]:
        with self.path.open("r", encoding="utf-8") as f:
            return [json.loads(line) for line in f if line.strip()]

    def write_all(self, rows: List[Dict[str, Any]]) -> None:
        with self.path.open("w", encoding="utf-8") as f:
            for row in rows:
                f.write(json.dumps(row) + "\n")


_inventory_db: Optional[JsonlDB] = None
_product_db: Optional[JsonlDB] = None


def get_inventory_db() -> JsonlDB:
    """Return the inventory JSONL database."""

    global _inventory_db
    url = Path(config.get_inventory_database_url())
    if _inventory_db is None or _inventory_db.path != url:
        _inventory_db = JsonlDB(url)
    return _inventory_db


def get_product_db() -> JsonlDB:
    """Return the products JSONL database."""

    global _product_db
    url = Path(config.get_product_database_url())
    if _product_db is None or _product_db.path != url:
        _product_db = JsonlDB(url)
    return _product_db


def get_db() -> JsonlDB:
    """Backward compatibility shim for inventory DB."""
    return get_inventory_db()
