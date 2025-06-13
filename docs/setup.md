# Setup Guide

1. Clone the repository.
2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   ```
3. Install dependencies (includes a pinned httpx version):
   ```bash
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and adjust paths if necessary. The defaults place the SQLite database under `data/`.
5. Run the setup script to create or update the database and systemd service:
   ```bash
   python3 scripts/setup.py
   ```
6. Start the service:
   ```bash
   python3 scripts/startup.py
   ```
7. Verify the API is running at [http://localhost:3000/health](http://localhost:3000/health).

## Scheduled Backups

Automate database backups by running `scripts/backup.py` through cron. The script relies on the `DATA_DIR`, `DATABASE_URL` and `BACKUP_DIR` environment variables which should mirror your `.env` configuration.

Example entry for a daily backup at 2 AM:

```cron
0 2 * * * cd /path/to/food-admin && /path/to/venv/bin/python scripts/backup.py
```

This keeps a timestamped copy of the SQLite database in `$BACKUP_DIR`.
