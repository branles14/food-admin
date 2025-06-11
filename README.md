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
2. Install dependencies with `npm install`.
3. Copy `.env.example` to `.env` and update `MONGODB_URI`.
4. Start the application using `npm start`.
5. Visit `http://localhost:3000/health` to verify the database connection.
6. (Optional) Seed example data with `npm run seed`.

### Startup script

If you don't have a MongoDB instance available, run `npm run startup`. This
command launches an in-memory MongoDB server using a Python helper script and
then starts the application.

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
