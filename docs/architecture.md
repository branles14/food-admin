# Architecture

This project exposes both a REST API and a command line interface built on the same Python services.

- **API**: `src/api/app.py` uses FastAPI to provide HTTP endpoints for container operations.
- **CLI**: `src/cli/main.py` offers subcommands for adding, updating and deleting containers as well as running the API server.
- **Services**: Code under `src/services` implements the business logic and directly interfaces with the SQLite database defined in `src/db`.
- **Database**: Storage uses SQLite by default and is configured through environment variables in `src/config.py`.

The structure keeps the core logic isolated so that the API and CLI share the same functions for consistent behaviour.
