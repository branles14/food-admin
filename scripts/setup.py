#!/usr/bin/env python3
"""Setup script to install dependencies, ensure MongoDB and configure the service."""
import os
import shutil
import subprocess
import sys
from pathlib import Path
import textwrap

PROJECT_DIR = Path(__file__).resolve().parents[1]
SERVICE_FILE = '/etc/systemd/system/foodadmin.service'


def get_dotenv_value(key: str) -> str:
    env_path = PROJECT_DIR / '.env'
    if not env_path.is_file():
        return ''
    with open(env_path) as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                k, v = line.split('=', 1)
                if k.strip() == key:
                    return v.strip()
    return ''


def ensure_dependencies() -> None:
    """Install required Python packages."""
    try:
        import flask  # type: ignore
        import pymongo  # type: ignore
        import dotenv  # type: ignore
    except Exception:
        print('Installing Python dependencies...')
        result = subprocess.run([
            'sudo',
            sys.executable,
            '-m',
            'pip',
            'install',
            '-r',
            str(PROJECT_DIR / 'requirements.txt'),
        ])
        if result.returncode != 0:
            sys.exit(result.returncode)


def ensure_env_file() -> None:
    """Create .env from example if missing."""
    env = PROJECT_DIR / '.env'
    example = PROJECT_DIR / '.env.example'
    if not env.exists() and example.exists():
        shutil.copy(example, env)
        print('Created .env from .env.example')


def install_docker() -> bool:
    """Install Docker using the official convenience script."""
    script = PROJECT_DIR / 'get-docker.sh'
    print('Docker is not installed. Attempting to install...')
    steps = [
        ['curl', '-fsSL', 'https://get.docker.com', '-o', str(script)],
        ['sudo', 'sh', str(script)],
    ]
    for cmd in steps:
        result = subprocess.run(cmd)
        if result.returncode != 0:
            return False
    script.unlink(missing_ok=True)
    return True


def ensure_docker_mongodb() -> bool:
    """Start a MongoDB Docker container if needed."""
    if not shutil.which('docker'):
        if not install_docker():
            return False

    container_name = 'fooddb'
    check = subprocess.run(
        ['docker', 'inspect', container_name],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if check.returncode != 0:
        print('Creating MongoDB Docker container...')
        result = subprocess.run(
            [
                'docker',
                'run',
                '--name',
                container_name,
                '-d',
                '-p',
                '27017:27017',
                'mongo:7',
            ],
            text=True,
            capture_output=True,
        )
        if result.returncode != 0:
            print(result.stdout.strip() or result.stderr.strip())
        return result.returncode == 0

    print('Starting existing MongoDB Docker container...')
    result = subprocess.run(
        ['docker', 'start', container_name], text=True, capture_output=True
    )
    if result.returncode != 0:
        print(result.stdout.strip() or result.stderr.strip())
    return result.returncode == 0


def ensure_mongodb() -> None:
    """Ensure MongoDB is running in a Docker container."""
    if ensure_docker_mongodb():
        return

    print('Failed to start MongoDB Docker container.')
    print('Please verify Docker is installed and the current user has permission to run Docker commands.')
    print('If Docker reports a permission error, add your user to the docker group:')
    print('  sudo usermod -aG docker $USER')
    print('After running the command, log out and back in, then re-run:')
    print('  python3 scripts/setup.py')


def create_service() -> None:
    """Create the systemd service file if it does not exist."""
    if os.path.isfile(SERVICE_FILE):
        return

    service_content = textwrap.dedent(f"""
    [Unit]
    Description=Food Admin Service
    After=network.target docker.service

    [Service]
    Type=simple
    WorkingDirectory={PROJECT_DIR}
    ExecStart=/usr/bin/python3 {PROJECT_DIR / 'app.py'}
    Restart=always
    EnvironmentFile={PROJECT_DIR / '.env'}

    [Install]
    WantedBy=multi-user.target
    """)

    with open('foodadmin.service', 'w') as f:
        f.write(service_content)
    subprocess.run(['sudo', 'mv', 'foodadmin.service', SERVICE_FILE])
    subprocess.run(['sudo', 'systemctl', 'daemon-reload'])
    subprocess.run(['sudo', 'systemctl', 'enable', 'foodadmin'])
    print('Created systemd service at', SERVICE_FILE)


def main() -> None:
    ensure_env_file()
    ensure_dependencies()

    mongo_uri = os.environ.get('MONGODB_URI') or get_dotenv_value('MONGODB_URI')
    if not mongo_uri or 'mongomock' in mongo_uri or mongo_uri.startswith('your-'):
        print('MONGODB_URI is not configured. Defaulting to mongodb://localhost:27017')
        mongo_uri = 'mongodb://localhost:27017'
        os.environ['MONGODB_URI'] = mongo_uri

    ensure_mongodb()
    create_service()

    print('Setup complete. Run `python3 scripts/startup.py` to start the service.')


if __name__ == '__main__':
    main()
