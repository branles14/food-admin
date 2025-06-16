import os
import sqlite3
import sys
from typing import Generator

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.db import _init_db


@pytest.fixture()
def db_conn() -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    _init_db(conn)
    try:
        yield conn
    finally:
        conn.close()
