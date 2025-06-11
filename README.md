# Food Admin

Food Admin is a simple project for tracking food inventory and containers.
It helps you manage which products you own and where they are stored.

## Features

The project uses MongoDB to store product and container information.

### Product
- `name` - product name
- `nutrition` - nutritional details
- `upc` - UPC identifier
- `uuid` - unique ID / QR code

### Container
- `product` - reference to a product
- `quantity` - how many units you own
- `opened` - whether the container has been opened
- `remaining` - amount left in the container

## Prerequisites

- Python 3
- MongoDB (the setup script will install and start `mongod` if needed)

## Setup

1. Clone this repository.
2. Run `python3 scripts/setup.py` to install dependencies, set up MongoDB and
   create the service. The script adds the official MongoDB 7.0 repository and
   ensures the `mongod` service is enabled and running.
3. Start the service with `python3 scripts/startup.py`.
4. Visit `http://localhost:3000/health` to verify the database connection.
5. (Optional) Seed example data with `python3 seeds.py`.
6. Retrieve the current inventory with `curl http://localhost:3000/containers`.

### Startup script

Use `python3 scripts/setup.py` once to configure the environment and service.
Afterwards `python3 scripts/startup.py` simply starts the systemd service.

### Generating and printing QR codes

Run `python3 scripts/generate_qrcodes.py` to create PNG QR codes for each
container UUID. The images are written to the `qrcodes/` directory. You can
print these files using any image viewer or the `lpr` command:

```bash
python3 scripts/generate_qrcodes.py
lpr qrcodes/<container-uuid>.png
```

Ensure your printer supports PNG images.

## Disclaimer

Nutritional information is provided as-is and may not always be accurate. Verify
with official sources.

## License

This project is licensed under the [MIT License](LICENSE).
