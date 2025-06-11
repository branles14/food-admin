#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys


def get_dotenv_value(key: str) -> str:
    """Return value for key from .env file if present."""
    if not os.path.isfile('.env'):
        return ''
    with open('.env') as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                k, v = line.split('=', 1)
                if k.strip() == key:
                    return v.strip()
    return ''


def ensure_dependencies():
    """Install required Python packages when missing."""
    try:
        import flask  # type: ignore
        import pymongo  # type: ignore
        import dotenv  # type: ignore
    except Exception:
        print('Installing Python dependencies...')
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        if result.returncode != 0:
            sys.exit(result.returncode)


def ensure_env_file():
    """Create .env from example if it doesn't exist."""
    if not os.path.isfile('.env') and os.path.isfile('.env.example'):
        shutil.copy('.env.example', '.env')
        print('Created .env from .env.example')


def main():
    ensure_env_file()
    ensure_dependencies()

    mongo_uri = os.environ.get('MONGODB_URI') or get_dotenv_value('MONGODB_URI')
    if not mongo_uri or mongo_uri.startswith('your-'):
        mongo_uri = 'mongomock://localhost'
        os.environ['MONGODB_URI'] = mongo_uri
        print('Using in-memory MongoDB')

    server = subprocess.Popen([sys.executable, 'app.py'], env=os.environ)
    exit_code = server.wait()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
