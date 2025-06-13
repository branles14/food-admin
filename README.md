# Food Admin

Food Admin is a simple project for tracking food inventory and containers.
It helps you manage which products you own and where they are stored.

## Features

The project uses MongoDB to store product and container information.

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

## Prerequisites

- Python 3
 - Docker (used to run MongoDB)

## Setup

1. Clone this repository.
2. Run `python3 scripts/setup.py` to install dependencies and create the
   systemd service.
3. Start the service with `python3 scripts/startup.py`. This launches the
   FastAPI app via `uvicorn` and prints the service status.
4. If needed, inspect the service with `sudo systemctl status foodadmin`.
5. Visit `http://localhost:3000/health` to verify the database connection.
6. (Optional) Seed example data with `python3 seeds.py`.
7. Retrieve the current inventory with `curl http://localhost:3000/containers`.

### Startup script

Use `python3 scripts/setup.py` once to configure the environment and service.
Afterwards `python3 scripts/startup.py` simply starts the systemd service
which runs `uvicorn` in the background.


## Disclaimer

Nutritional information is provided as-is and may not always be accurate. Verify
with official sources.

## License

This project is licensed under the [MIT License](LICENSE).
