# Food Admin

Food Admin is a simple project for tracking food inventory and containers.
It helps you manage which products you own and where they are stored.

## Features

The project uses SQLite to store product and container information.

### Product
- `name` - product name
- `nutrition` - nutritional details
- `upc` - UPC identifier
- `uuid` - unique identifier

### Container
- `product` - reference to a product
- `quantity` - how many units you own
- `opened` - whether the container has been opened
- `remaining` - amount left in the container
- `expiration_date` - when the item expires
- `location` - where the container is stored
- `tags` - labels for categorization
- `container_weight` - weight of the empty container

## Prerequisites

- Python 3

## Setup

1. Clone this repository.
2. Copy `.env.example` to `.env` and adjust the paths if desired. The default
   configuration stores data locally under the `data/` directory using a SQLite
   database at `data/inventory.db`.
3. Run `python3 scripts/setup.py` to install dependencies and create the
   systemd service. The script creates the SQLite database if it does not exist.
4. Start the service with `python3 scripts/startup.py` to launch the FastAPI
   app using `python -m src.cli.main`.
5. Visit `http://localhost:3000/health` to verify the service is running.
6. (Optional) Seed example data with `python3 seeds.py`.
7. Retrieve the current inventory with `curl http://localhost:3000/containers`.
8. Run `python3 scripts/backup.py` to create a timestamped backup in the
   directory specified by `BACKUP_DIR`.

## Running Tests

Unit tests are located under the `tests/` directory and use `pytest`. Install
pytest with `pip install pytest` if it is not already available and run:

```bash
pytest
```

### Environment variables

The `.env` file controls where data is stored and which port the service uses:

- `DATA_DIR` &mdash; directory for persistent data (defaults to `./data`)
- `DATABASE_URL` &mdash; SQLite connection string, e.g.
  `sqlite:///data/inventory.db`
- `BACKUP_DIR` &mdash; location for database backups (defaults to `./backups`)
- `PORT` &mdash; port number for the FastAPI application

### Startup script

Use `python3 scripts/setup.py` once to configure the environment and service.
Afterwards `python3 scripts/startup.py` simply starts the systemd service
which executes `python -m src.cli.main` in the background.


## Disclaimer

Nutritional information is provided as-is and may not always be accurate. Verify
with official sources.

## License

This project is licensed under the [MIT License](LICENSE).
