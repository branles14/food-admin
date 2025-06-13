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
