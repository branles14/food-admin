"""Command line interface for food-admin."""

from __future__ import annotations

import argparse
import os
from typing import Any, Dict

import uvicorn

from src.db import get_db
from src.services import container_service
from src.api.app import app


def serve(_: argparse.Namespace) -> None:
    """Run the FastAPI server."""
    port = int(os.environ.get("PORT", 3000))
    uvicorn.run("src.api.app:app", host="0.0.0.0", port=port)


def add_container(args: argparse.Namespace) -> None:
    conn = get_db()
    data: Dict[str, Any] = {
        "product": args.product,
        "quantity": args.quantity,
        "opened": args.opened,
        "remaining": args.remaining,
    }
    container = container_service.create_container(conn, data)
    print(container)


def update_container(args: argparse.Namespace) -> None:
    conn = get_db()
    data: Dict[str, Any] = {}
    if args.product is not None:
        data["product"] = args.product
    if args.quantity is not None:
        data["quantity"] = args.quantity
    if args.opened is not None:
        data["opened"] = args.opened
    if args.remaining is not None:
        data["remaining"] = args.remaining
    container = container_service.update_container(conn, args.id, data)
    print(container)


def delete_container(args: argparse.Namespace) -> None:
    conn = get_db()
    success = container_service.delete_container(conn, args.id)
    print({"deleted": success})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Food Admin CLI")
    sub = parser.add_subparsers(dest="command")

    serve_cmd = sub.add_parser("serve", help="Run the API server")
    serve_cmd.set_defaults(func=serve)

    add_cmd = sub.add_parser("add", help="Add a container")
    add_cmd.add_argument("--product", required=False)
    add_cmd.add_argument("--quantity", type=int, required=False)
    add_cmd.add_argument("--opened", action="store_true")
    add_cmd.add_argument("--remaining", type=float, required=False)
    add_cmd.set_defaults(func=add_container)

    upd_cmd = sub.add_parser("update", help="Update a container")
    upd_cmd.add_argument("id")
    upd_cmd.add_argument("--product")
    upd_cmd.add_argument("--quantity", type=int)
    upd_cmd.add_argument("--opened", type=bool)
    upd_cmd.add_argument("--remaining", type=float)
    upd_cmd.set_defaults(func=update_container)

    del_cmd = sub.add_parser("delete", help="Delete a container")
    del_cmd.add_argument("id")
    del_cmd.set_defaults(func=delete_container)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        serve(args)
        return
    args.func(args)


if __name__ == "__main__":  # pragma: no cover
    main()
