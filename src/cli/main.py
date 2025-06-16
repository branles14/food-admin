"""Command line interface for food-admin."""

from __future__ import annotations

import argparse
import json
import os
from typing import Any, Dict, Tuple

import uvicorn

from src.db import get_inventory_db, get_product_db
from uuid import uuid4

from src.services import item_service, product_info_service
from src.utils import unit_conversion


def serve(_: argparse.Namespace) -> None:
    """Run the FastAPI server."""
    port = int(os.environ.get("PORT", 3000))
    uvicorn.run("src.api.app:app", host="0.0.0.0", port=port)


def add_item(args: argparse.Namespace) -> None:
    inv_conn = get_inventory_db()
    prod_conn = get_product_db()

    upc = args.upc
    if upc is None and args.product_info is None:
        upc = input("UPC: ").strip()

    product = None
    if upc:
        product = product_info_service.get_product_info_by_upc(prod_conn, upc)
        if product is None:
            name = input("Product name: ")
            size_in = input("Package size: ")
            metric_size = unit_conversion.format_metric(size_in)
            serving_size = input("Serving size: ")

            def ask(prompt: str, parser: Tuple[type, ...] = (str,)) -> Any:
                val = input(f"{prompt}: ")
                if parser[0] is int and val:
                    return int(val)
                return val

            facts = {
                "serving_size": serving_size,
                "calories": ask("Calories", (int,)),
                "total_fat": ask("Total Fat"),
                "saturated_fat": ask("Saturated Fat"),
                "trans_fat": ask("Trans Fat"),
                "sodium": ask("Sodium"),
                "total_carbohydrate": ask("Total Carbohydrate"),
                "dietary_fiber": ask("Dietary Fiber"),
                "sugars": ask("Sugars"),
                "added_sugars": ask("Added Sugars"),
                "protein": ask("Protein"),
            }
            nutrition = {"package_size": metric_size, "facts": facts}
            product = product_info_service.create_product_info(
                prod_conn,
                {
                    "name": name,
                    "upc": upc,
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
            prod = item_service.create_item(inv_conn, prod_conn, data)
            outputs.append(prod)
            print(prod)
        return

    data: Dict[str, Any] = {
        "product": args.product_info,
        "quantity": args.quantity,
        "opened": args.opened,
        "remaining": args.remaining,
        "expiration_date": args.expiration_date,
        "location": args.location,
        "tags": args.tags.split(",") if args.tags else None,
        "container_weight": args.container_weight,
    }
    product = item_service.create_item(inv_conn, prod_conn, data)
    print(product)


def update_item(args: argparse.Namespace) -> None:
    inv_conn = get_inventory_db()
    prod_conn = get_product_db()
    data: Dict[str, Any] = {}
    if args.product_info is not None:
        data["product"] = args.product_info
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
    product = item_service.update_item(inv_conn, prod_conn, args.id, data)
    print(product)


def delete_item(args: argparse.Namespace) -> None:
    inv_conn = get_inventory_db()
    success = item_service.delete_item(inv_conn, args.id)
    print({"deleted": success})


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Food Admin CLI")
    sub = parser.add_subparsers(dest="command")

    serve_cmd = sub.add_parser("serve", help="Run the API server")
    serve_cmd.set_defaults(func=serve)

    add_cmd = sub.add_parser("add", help="Add an item")
    add_cmd.add_argument("--product-info", required=False)
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
    add_cmd.set_defaults(func=add_item)

    upd_cmd = sub.add_parser("update", help="Update an item")
    upd_cmd.add_argument("id")
    upd_cmd.add_argument("--product-info")
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
    upd_cmd.set_defaults(func=update_item)

    del_cmd = sub.add_parser("delete", help="Delete an item")
    del_cmd.add_argument("id")
    del_cmd.set_defaults(func=delete_item)

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
