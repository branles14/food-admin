from services import product_service, container_service


def run():
    product = product_service.create_product(
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
        }
    )

    container_service.create_container(
        {
            "product": product["id"],
            "quantity": 2,
            "opened": False,
            "remaining": 2,
        }
    )
    print("Seed data inserted")


if __name__ == "__main__":
    run()
