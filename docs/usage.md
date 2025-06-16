# Using the API and CLI

## CLI

Run commands through the module `src.cli.main`:

```bash
python -m src.cli.main add --product-info 1 --quantity 2 --opened
python -m src.cli.main update 5 --no-opened
python -m src.cli.main delete 5
```

The `serve` subcommand starts the API server locally:

```bash
python -m src.cli.main serve
```

## API

With the server running, you can interact with the REST endpoints. Examples:

- List items: `GET /inventory`
- Create item:
  ```bash
  curl -X POST http://localhost:3000/inventory \
    -H 'Content-Type: application/json' \
    -d '{"product": 1, "quantity": 1}'
  ```
 - Update item:
  ```bash
  curl -X PATCH http://localhost:3000/inventory/<id> \
    -H 'Content-Type: application/json' \
    -d '{"quantity": 3}'
  ```
- Delete item: `DELETE /inventory/<id>`

The API also exposes a `/health` endpoint for a simple status check.

## Backups

The helper script `scripts/backup.py` creates a timestamped copy of the
SQLite database. The destination directory is controlled by the
`BACKUP_DIR` environment variable which defaults to `./backups`.

Run the script whenever you want to capture a backup:

```bash
python3 scripts/backup.py
```
