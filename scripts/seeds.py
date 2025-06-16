from pathlib import Path
import sys

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from src.db import get_db
from src.services import item_service, product_info_service


def run() -> None:
    conn = get_db()
    product = product_info_service.create_item_info(
        conn,
        {
            "name": "Tomato Sauce",
            "upc": "012345678905",
            "uuid": "550e8400-e29b-41d4-a716-446655440000",
            "nutrition": {
                "calories": 80,
                "fat": 1,
                "protein": 2,
                "carbs": 15,
            },
        },
    )

    item_service.create_item(
        conn,
        {
            "product": product["id"],
            "quantity": 2,
            "opened": False,
            "remaining": 2,
        },
    )
    print("Seed data inserted")


if __name__ == "__main__":
    run()
