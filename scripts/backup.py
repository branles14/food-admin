#!/usr/bin/env python3
"""Create a timestamped backup of the SQLite database."""
from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path

from src import config
from src.db import get_db


def main() -> None:
    db_url = config.get_database_url()
    if not db_url.startswith("sqlite:///"):
        raise SystemExit("Only SQLite backups are supported")

    db_path = Path(db_url[len("sqlite:///") :])
    if not db_path.exists():
        raise SystemExit(f"Database file {db_path} does not exist")

    backup_dir = config.get_backup_dir()
    backup_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = backup_dir / f"inventory_{timestamp}.db"
    shutil.copy2(db_path, backup_file)
    print(f"Backup written to {backup_file}")


if __name__ == "__main__":
    main()
