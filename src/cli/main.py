"""Command line interface for food-admin."""

from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict

import uvicorn

from src.db import get_inventory_db, get_product_db
from uuid import uuid4

from src.services import container_service, product_service
from src.utils import unit_conversion


def serve(_: argparse.Namespace) -> None:
    """Run the FastAPI server."""
    port = int(os.environ.get("PORT", 3000))
    uvicorn.run("src.api.app:app", host="0.0.0.0", port=port)


def add_container(args: argparse.Namespace) -> None:
    inv_conn = get_inventory_db()
    prod_conn = get_product_db()

    product = None
    if getattr(args, "upc", None):
        product = product_service.get_product_by_upc(prod_conn, args.upc)
        if product is None:
            name = input("Product name: ")
            size_in = input("Package size: ")
            metric_size = unit_conversion.format_metric(size_in)
            nutrition_raw = input("Nutrition facts JSON: ")
            nutrition = json.loads(nutrition_raw) if nutrition_raw else None
            nutrition = {"package_size": metric_size, "facts": nutrition}
            product = product_service.create_product(
                prod_conn,
                {
                    "name": name,
                    "upc": args.upc,
                    "uuid": str(uuid4()),
                    "nutrition": nutrition,
                },
            )
        qty_inp = input("Quantity: ")
        count = int(qty_inp) if qty_inp else 1
        outputs = []
        for _ in range(count):
            data: Dict[str, Any] = {
                "product": product["id"],
                "quantity": 1,
                "opened": False,
                "remaining": 1.0,
                "expiration_date": None,
                "location": None,
                "tags": None,
                "container_weight": None,
            }
            cont = container_service.create_container(inv_conn, prod_conn, data)
            outputs.append(cont)
            print(cont)
        return

    data: Dict[str, Any] = {
        "product": args.product,
        "quantity": args.quantity,
        "opened": args.opened,
        "remaining": args.remaining,
        "expiration_date": args.expiration_date,
        "location": args.location,
        "tags": args.tags.split(",") if args.tags else None,
        "container_weight": args.container_weight,
    }
    container = container_service.create_container(inv_conn, prod_conn, data)
    print(container)


def update_container(args: argparse.Namespace) -> None:
    inv_conn = get_inventory_db()
    prod_conn = get_product_db()
    data: Dict[str, Any] = {}
    if args.product is not None:
        data["product"] = args.product
    if args.quantity is not None:
        data["quantity"] = args.quantity
    if args.opened is not None:
        data["opened"] = args.opened
    if args.remaining is not None:
        data["remaining"] = args.remaining
    if args.expiration_date is not None:
        data["expiration_date"] = args.expiration_date
    if args.location is not None:
        data["location"] = args.location
    if args.tags is not None:
        data["tags"] = args.tags.split(",") if args.tags else None
    if args.container_weight is not None:
        data["container_weight"] = args.container_weight
    container = container_service.update_container(inv_conn, prod_conn, args.id, data)
    print(container)


def delete_container(args: argparse.Namespace) -> None:
    inv_conn = get_inventory_db()
    success = container_service.delete_container(inv_conn, args.id)
    print({"deleted": success})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Food Admin CLI")
    sub = parser.add_subparsers(dest="command")

    serve_cmd = sub.add_parser("serve", help="Run the API server")
    serve_cmd.set_defaults(func=serve)

    add_cmd = sub.add_parser("add", help="Add a container")
    add_cmd.add_argument("--product", required=False)
    add_cmd.add_argument("--quantity", type=int, required=False)
    add_cmd.add_argument("--upc", required=False)
    opened_grp = add_cmd.add_mutually_exclusive_group()
    opened_grp.add_argument("--opened", dest="opened", action="store_true")
    opened_grp.add_argument("--no-opened", dest="opened", action="store_false")
    add_cmd.set_defaults(opened=False)
    add_cmd.add_argument("--remaining", type=float, required=False)
    add_cmd.add_argument("--expiration-date", required=False)
    add_cmd.add_argument("--location", required=False)
    add_cmd.add_argument("--tags", required=False)
    add_cmd.add_argument("--container-weight", type=int, required=False)
    add_cmd.set_defaults(func=add_container)

    upd_cmd = sub.add_parser("update", help="Update a container")
    upd_cmd.add_argument("id")
    upd_cmd.add_argument("--product")
    upd_cmd.add_argument("--quantity", type=int)
    upd_opened = upd_cmd.add_mutually_exclusive_group()
    upd_opened.add_argument("--opened", dest="opened", action="store_true")
    upd_opened.add_argument("--no-opened", dest="opened", action="store_false")
    upd_cmd.set_defaults(opened=None)
    upd_cmd.add_argument("--remaining", type=float)
    upd_cmd.add_argument("--expiration-date")
    upd_cmd.add_argument("--location")
    upd_cmd.add_argument("--tags")
    upd_cmd.add_argument("--container-weight", type=int)
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
