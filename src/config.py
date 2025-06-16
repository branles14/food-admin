from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def get_data_dir() -> Path:
    """Return the directory for persistent data."""
    data_dir = Path(os.environ.get("DATA_DIR", "./data"))
    return data_dir


def get_backup_dir() -> Path:
    """Return the directory where backups should be stored."""
    backup_dir = Path(os.environ.get("BACKUP_DIR", "./backups"))
    return backup_dir


def get_inventory_database_url() -> str:
    """Return the configured inventory data file."""
    default_path = get_data_dir() / "inventory.jsonl"
    return os.environ.get(
        "INVENTORY_DATABASE_URL",
        os.environ.get("DATABASE_URL", str(default_path)),
    )


def get_product_database_url() -> str:
    """Return the configured products data file."""
    default_path = get_data_dir() / "products.jsonl"
    return os.environ.get("PRODUCT_DATABASE_URL", str(default_path))


def get_database_url() -> str:
    """Backward compatibility shim for inventory DB."""
    return get_inventory_database_url()
