#!/usr/bin/env python3
import os
import subprocess
import sys


def main():
    mongo_uri = os.environ.get('MONGODB_URI')
    memory_server = None

    try:
        if not mongo_uri:
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
