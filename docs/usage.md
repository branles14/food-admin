# Using the API and CLI

## CLI

Run commands through the module `src.cli.main`:

```bash
python -m src.cli.main add --product 1 --quantity 2 --opened
python -m src.cli.main update 5 --no-opened
python -m src.cli.main delete 5
```

The `serve` subcommand starts the API server locally:

```bash
python -m src.cli.main serve
```

## API

With the server running, you can interact with the REST endpoints. Examples:

- List containers: `GET /containers`
- Create container:
  ```bash
  curl -X POST http://localhost:3000/containers \
    -H 'Content-Type: application/json' \
    -d '{"product": 1, "quantity": 1}'
  ```
- Update container:
  ```bash
  curl -X PATCH http://localhost:3000/containers/<id> \
    -H 'Content-Type: application/json' \
    -d '{"quantity": 3}'
  ```
- Delete container: `DELETE /containers/<id>`

The API also exposes a `/health` endpoint for a simple status check.
