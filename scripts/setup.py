#!/usr/bin/env python3
"""Setup script to install dependencies and configure the service."""
import os
import shutil
import subprocess
import textwrap
import importlib
from pathlib import Path
import sys

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from src import config

SERVICE_FILE = "/etc/systemd/system/foodadmin.service"


def ensure_dependencies() -> None:
    """Install required Python packages."""
    try:
        importlib.import_module("fastapi")
        importlib.import_module("uvicorn")
        importlib.import_module("dotenv")
        importlib.import_module("httpx")
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
    """Create the JSONL data file if needed."""
    path = Path(db_url)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)


def create_service() -> None:
    """Create or update the systemd service file."""
    expected_exec = (
        "/usr/bin/python3 -m uvicorn src.api.app:app --host 0.0.0.0" " --port ${PORT}"
    )
    action = "Created"
    if os.path.isfile(SERVICE_FILE):
        subprocess.run(["sudo", "systemctl", "stop", "foodadmin"], check=False)
        subprocess.run(["sudo", "systemctl", "disable", "foodadmin"], check=False)
        subprocess.run(["sudo", "rm", "-f", SERVICE_FILE])
        action = "Updated"

    service_content = textwrap.dedent(
        f"""
    [Unit]
    Description=Food Admin Database Service
    After=network.target

    [Service]
    Type=simple
    WorkingDirectory={PROJECT_DIR}
    ExecStart={expected_exec}
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
    print(f"{action} systemd service at {SERVICE_FILE}")


def main() -> None:
    ensure_env_file()
    ensure_dependencies()

    db_url = config.get_database_url()
    init_database(db_url)
    create_service()

    # fmt: off
    print(
        "Setup complete. Run `python3 scripts/startup.py` "
        "to start the service."
    )
    # fmt: on


if __name__ == "__main__":
    main()
