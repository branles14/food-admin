"""Database access helpers."""

from __future__ import annotations

from pathlib import Path
import sqlite3
from sqlite3 import Connection
from typing import Optional

from src import config

_conn: Optional[Connection] = None


def _init_db(conn: Connection) -> None:
    """Create tables if they do not already exist."""

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


def get_db() -> Connection:
    """Return an SQLite database connection."""

    global _conn
    if _conn is not None:
        return _conn

    url = config.get_database_url()
    if url.startswith("sqlite:///"):
        path = url[len("sqlite:///") :]
    else:
        path = url

    Path(path).parent.mkdir(parents=True, exist_ok=True)

    _conn = sqlite3.connect(path, check_same_thread=False)
    _conn.row_factory = sqlite3.Row
    _init_db(_conn)
    return _conn
