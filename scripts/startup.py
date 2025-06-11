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
    """Install npm packages if node_modules does not exist."""
    if not os.path.isdir('node_modules'):
        print('Installing npm dependencies...')
        result = subprocess.run(['npm', 'install'])
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

    mongo_uri = os.environ.get('MONGODB_URI')
    if not mongo_uri:
        mongo_uri = get_dotenv_value('MONGODB_URI')
    memory_server = None

    try:
        if not mongo_uri or mongo_uri.startswith('your-'):
            memory_server = subprocess.Popen(
                ['node', 'scripts/memory_server.js'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            mongo_uri = memory_server.stdout.readline().strip()
            os.environ['MONGODB_URI'] = mongo_uri
            print(f"Started in-memory MongoDB at {mongo_uri}")

        server = subprocess.Popen(['node', 'index.js'], env=os.environ)
        exit_code = server.wait()
    finally:
        if memory_server:
            memory_server.terminate()
            memory_server.wait()
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
