# Architecture

This project exposes a REST API built on lightweight Python services.

- **API**: `src/api/app.py` uses FastAPI to provide HTTP endpoints for item operations.
- **Services**: Code under `src/services` implements the business logic and directly reads and writes JSONL files defined in `src/db`.
- **Database**: Storage uses JSON Lines files by default and is configured through environment variables in `src/config.py`.

The structure keeps the core logic isolated so that the API remains lightweight and easy to maintain.
