# Using the API

## API

With the server running, you can interact with the REST endpoints. Examples:

- List items: `GET /inventory`
- Create item:
  ```bash
  curl -X POST http://localhost:3000/inventory \
    -H 'Content-Type: application/json' \
    -d '{"product": 1, "quantity": 1}'
  ```

The `product` value references data stored in `product-info.ndjson`. That file
is only used during item creation to populate the new entry. Once the item is
saved, all required fields are written to `inventory.ndjson` so the API no longer
relies on `product-info.ndjson`.

For example, if `product-info.ndjson` contains an entry:

```json
{"id": 1, "name": "Oat Milk", "upc": "012345"}
```

you can create an inventory item with:

```bash
curl -X POST http://localhost:3000/inventory \
  -H 'Content-Type: application/json' \
  -d '{"product": 1, "quantity": 2}'
```

The resulting item stores the name and UPC itself, so deleting the product info
later will not affect API responses.
- Update item:
  ```bash
  curl -X PATCH http://localhost:3000/inventory/<id> \
    -H 'Content-Type: application/json' \
    -d '{"quantity": 3}'
  ```
- Delete item: `DELETE /inventory/<id>`
- Get item by UUID: `GET /inventory/uuid/<uuid>`
- Update item by UUID:
  ```bash
  curl -X PATCH http://localhost:3000/inventory/uuid/<uuid> \
    -H 'Content-Type: application/json' \
    -d '{"quantity": 3}'
  ```
- Delete item by UUID: `DELETE /inventory/uuid/<uuid>`

You can print QR code stickers that encode the item's short UUID. Scanning one
opens `/inventory/uuid/<uuid>` in your client so you can view the item
instantly. After checking the details, you might issue a `PATCH` request to the
same URL to update the `remaining` weight if you consumed some of it.
- Consume amount from an item:
  ```bash
  curl -X POST http://localhost:3000/inventory/<id>/consume \
    -H 'Content-Type: application/json' \
    -d '{"amount": 0.5}'
  ```

The API also exposes a `/health` endpoint for a simple status check.

## Backups

The helper script `scripts/backup.py` creates a timestamped copy of the
JSONL data files. The destination directory is controlled by the
`BACKUP_DIR` environment variable which defaults to `./backups`.

Run the script whenever you want to capture a backup:

```bash
python3 scripts/backup.py
```
