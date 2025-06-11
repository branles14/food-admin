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

- Node.js and npm
- Running MongoDB instance
- Environment variables for MongoDB connection

## Setup

1. Clone this repository.
2. Run `npm run startup` to automatically install dependencies, create a
   `.env` file if needed and launch the application with an in-memory MongoDB
   instance when no `MONGODB_URI` is provided.
3. Visit `http://localhost:3000/health` to verify the database connection.
4. (Optional) Seed example data with `npm run seed`.

### Startup script

The `npm run startup` command can be used at any time. It installs missing
dependencies, copies `.env.example` to `.env` when necessary, starts an
in-memory MongoDB server if `MONGODB_URI` is undefined and then launches the
application.

### Generating and printing QR codes

Run `npm run generate-qr` to create PNG QR codes for each container UUID. The
images are written to the `qrcodes/` directory. You can print these files using
any image viewer or the `lpr` command:

```bash
npm run generate-qr
lpr qrcodes/<container-uuid>.png
```

Ensure your printer supports PNG images.

## Disclaimer

Nutritional information is provided as-is and may not always be accurate. Verify with official sources.

## License

This project is licensed under the [MIT License](LICENSE).
