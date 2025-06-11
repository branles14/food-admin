#!/usr/bin/env python3
"""Start the Food Admin service."""
import subprocess
import sys


def main() -> None:
    result = subprocess.run(['sudo', 'systemctl', 'start', 'foodadmin'])
    sys.exit(result.returncode)


if __name__ == '__main__':
    main()
