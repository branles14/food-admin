"""Database access helpers."""

from __future__ import annotations

from pathlib import Path
import sqlite3
from sqlite3 import Connection
from typing import Optional

from src import config

_inventory_conn: Optional[Connection] = None
_product_conn: Optional[Connection] = None


def _init_product_db(conn: Connection) -> None:
    """Create products table if it does not already exist."""

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            upc TEXT,
            uuid TEXT,
            nutrition TEXT
        )
    """
    )
    conn.commit()


def _init_inventory_db(conn: Connection) -> None:
    """Create containers table if it does not already exist."""

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS containers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER,
            quantity INTEGER,
            opened BOOLEAN,
            remaining REAL,
            uuid TEXT,
            expiration_date TEXT,
            location TEXT,
            tags TEXT,
            container_weight INTEGER
        )
    """
    )
    conn.commit()


def _connect(url: str) -> Connection:
    if url.startswith("sqlite:///"):
        start = len("sqlite:///")
        path = url[start:]
    else:
        path = url

    Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def get_inventory_db() -> Connection:
    """Return the inventory database connection."""

    global _inventory_conn
    if _inventory_conn is None:
        url = config.get_inventory_database_url()
        _inventory_conn = _connect(url)
        _init_inventory_db(_inventory_conn)
    return _inventory_conn


def get_product_db() -> Connection:
    """Return the products database connection."""

    global _product_conn
    if _product_conn is None:
        url = config.get_product_database_url()
        _product_conn = _connect(url)
        _init_product_db(_product_conn)
    return _product_conn


def _init_db(conn: Connection) -> None:
    """Initialize both tables on a single connection."""

    _init_product_db(conn)
    _init_inventory_db(conn)


def get_db() -> Connection:
    """Backward compatibility shim for inventory DB."""
    return get_inventory_db()
