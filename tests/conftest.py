import os
import sys
from typing import Generator

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.db import JsonlDB


@pytest.fixture()
def inventory_db(tmp_path) -> Generator[JsonlDB, None, None]:
    db = JsonlDB(tmp_path / "inventory.jsonl")
    yield db


@pytest.fixture()
def product_db(tmp_path) -> Generator[JsonlDB, None, None]:
    db = JsonlDB(tmp_path / "products.jsonl")
    yield db
