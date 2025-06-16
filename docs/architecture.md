# Architecture

This project exposes both a REST API and a command line interface built on the same Python services.

- **API**: `src/api/app.py` uses FastAPI to provide HTTP endpoints for item operations.
- **CLI**: `src/cli/main.py` offers subcommands for adding, updating and deleting items as well as running the API server.
- **Services**: Code under `src/services` implements the business logic and directly reads and writes JSONL files defined in `src/db`.
- **Database**: Storage uses JSON Lines files by default and is configured through environment variables in `src/config.py`.

The structure keeps the core logic isolated so that the API and CLI share the same functions for consistent behaviour.
