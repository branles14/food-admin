#!/usr/bin/env python3
"""Create a timestamped backup of the JSONL data files."""
from __future__ import annotations

import shutil
import sys
from datetime import datetime
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from src import config


def main() -> None:
    db_path = Path(config.get_database_url())
    prod_path = Path(config.get_product_database_url())
    if not db_path.exists() or not prod_path.exists():
        raise SystemExit("Data files do not exist")

    backup_dir = config.get_backup_dir()
    backup_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    inv_backup = backup_dir / f"inventory_{timestamp}.jsonl"
    prod_backup = backup_dir / f"products_{timestamp}.jsonl"
    shutil.copy2(db_path, inv_backup)
    shutil.copy2(prod_path, prod_backup)
    print(f"Backup written to {inv_backup} and {prod_backup}")


if __name__ == "__main__":
    main()
