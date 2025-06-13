#!/usr/bin/env python3
"""Setup script to install dependencies and configure the service."""
import os
import shutil
import subprocess
import sys
from pathlib import Path
import textwrap
import importlib

from src import config

from src.db import get_db

PROJECT_DIR = Path(__file__).resolve().parents[1]
SERVICE_FILE = "/etc/systemd/system/foodadmin.service"


def ensure_dependencies() -> None:
    """Install required Python packages."""
    try:
        importlib.import_module("fastapi")
        importlib.import_module("uvicorn")
        importlib.import_module("dotenv")
        importlib.import_module("sqlalchemy")
    except Exception:
        print("Installing Python dependencies...")
        result = subprocess.run(
            [
                "sudo",
                sys.executable,
                "-m",
                "pip",
                "install",
                "-r",
                str(PROJECT_DIR / "requirements.txt"),
            ]
        )
        if result.returncode != 0:
            sys.exit(result.returncode)


def ensure_env_file() -> None:
    """Create .env from example if missing."""
    env = PROJECT_DIR / ".env"
    example = PROJECT_DIR / ".env.example"
    if not env.exists() and example.exists():
        shutil.copy(example, env)
        print("Created .env from .env.example")


def init_database(db_url: str) -> None:
    """Create the SQLite database file and directory if needed."""
    if not db_url.startswith("sqlite:///"):
        return

    path = Path(db_url[len("sqlite:///"):])
    path.parent.mkdir(parents=True, exist_ok=True)
    os.environ["DATABASE_URL"] = db_url
    get_db().close()


def create_service() -> None:
    """Create the systemd service file if it does not exist."""
    if os.path.isfile(SERVICE_FILE):
        return

    service_content = textwrap.dedent(
        f"""
    [Unit]
    Description=Food Admin Service
    After=network.target

    [Service]
    Type=simple
    WorkingDirectory={PROJECT_DIR}
    ExecStart=/usr/bin/python3 -m src.cli.main
    Restart=always
    EnvironmentFile={PROJECT_DIR / '.env'}

    [Install]
    WantedBy=multi-user.target
    """
    )

    with open("foodadmin.service", "w") as f:
        f.write(service_content)
    subprocess.run(["sudo", "mv", "foodadmin.service", SERVICE_FILE])
    subprocess.run(["sudo", "systemctl", "daemon-reload"])
    subprocess.run(["sudo", "systemctl", "enable", "foodadmin"])
    print("Created systemd service at", SERVICE_FILE)


def main() -> None:
    ensure_env_file()
    ensure_dependencies()

    db_url = config.get_database_url()
    init_database(db_url)
    create_service()

    print("Setup complete. Run `python3 scripts/startup.py` to start the service.")


if __name__ == "__main__":
    main()
