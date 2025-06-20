# Food Admin

Food Admin is a simple project for tracking food inventory items.
It helps you manage which items you own, their remaining quantities, and nutritional values.
See the [docs](docs/) directory for an overview of the architecture, setup instructions and usage examples.

## Features

The project stores product and inventory data in simple JSON Lines files.
Product information entries are identified by UUID strings rather than numeric IDs.

`product-info.ndjson` acts purely as a reference database for fast entry. It
contains UPC lookups and common product details. When you create a new inventory
item the relevant fields are copied into `inventory.ndjson` so that each item is
self‑contained. After creation, API calls read only from `inventory.ndjson` and do
not require `product-info.ndjson` to be present.
An example of this workflow is shown in [docs/usage.md](docs/usage.md).

### Product Info
- `product_id` - unique product identifier (UUID string)
- `name` - product name
- `nutrition` - nutritional details, including vitamins and minerals
- `upc` - UPC identifier
- `tags` - labels like "frozen" or "canned"

### Inventory Item
- `product_id` - reference to catalog data
- `units` - list of physical units with their own weight and expiration
- `tags` - labels for categorization
- `container_weight` - weight of the empty container
- each item automatically receives a short UUID for use with QR code stickers or scanners

### Supported Nutrition Fields

The `nutrition` object accepts standard keys such as `calories`, `total_fat`,
and `protein`. It also supports micronutrients including:

`vitamin_a`, `vitamin_c`, `vitamin_k`, `thiamin_b1`, `riboflavin_b2`,
`vitamin_b6`, `vitamin_b12`, `folate`, `biotin`, `pantothenic_acid`,
`phosphorus`, `magnesium`, `selenium`, `manganese`, `molybdenum`, `iodine`,
`zinc`, `copper`, and `chromium`.

## Prerequisites

- Python 3.10 or newer

## Setup

1. Clone this repository.
2. Copy `.env.example` to `.env` and adjust the paths if desired. The default
   configuration stores data locally under the `data/` directory using JSONL
   files at `data/inventory.ndjson` and `data/product-info.ndjson`.
   An empty `inventory.ndjson` file is included so the service can start
   without creating it manually.
3. Run `python3 scripts/setup.py` to install dependencies and create or update
   the systemd service. The script also creates the data files if they do
   not exist. The `requirements.txt` file pins `httpx` to versions
   `>=0.27,<0.28` for compatibility.
4. Start the service with `python3 scripts/startup.py` to launch the FastAPI
   application.
5. Visit `http://localhost:3000/health` to verify the service is running.
6. Retrieve the current inventory with `curl http://localhost:3000/inventory`.
7. Run `python3 scripts/backup.py` to create a timestamped backup in the
   directory specified by `BACKUP_DIR`. See the [Backups section](docs/usage.md#backups)
   in the usage guide for more details. To automate backups with cron,
   follow the [scheduled backups instructions](docs/setup.md#scheduled-backups)
   in the setup guide.


## Running Tests

Unit tests are located under the `tests/` directory and use `pytest`. Install
pytest with `pip install pytest` if it is not already available and run:

```bash
pytest
```

### Environment variables

The `.env` file controls where data is stored and which port the service uses:

- `DATA_DIR` &mdash; directory for persistent data (defaults to `./data`)
- `BACKUP_DIR` &mdash; location for database backups (defaults to `./backups`)
- `PORT` &mdash; port number for the FastAPI application

### Startup script

Use `python3 scripts/setup.py` once to configure the environment and service.
Afterwards `python3 scripts/startup.py` simply starts the systemd service
which runs the API using uvicorn in the background.


## Disclaimer

Nutritional information is provided as-is and may not always be accurate. Verify
with official sources.

## License

This project is licensed under the [MIT License](LICENSE).
