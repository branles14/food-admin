#!/bin/bash

# Load port from .env if available
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

PORT=3000
if [ -f "$ROOT_DIR/.env" ]; then
    env_port=$(grep -E '^PORT=' "$ROOT_DIR/.env" | cut -d '=' -f2)
    if [ -n "$env_port" ]; then
        PORT=$env_port
    fi
fi

BASE_URL="http://localhost:${PORT}"

# Add Jif Creamy Peanut Butter Pouch by UPC
echo "Adding peanut butter..."
pb_response=$(curl -s -X POST "${BASE_URL}/inventory" \
    -H 'Content-Type: application/json' \
    -d '{"upc": "051500245453"}')
echo "$pb_response"

# Ensure Premier Protein product exists in product-info database
if ! grep -q "643843717850" "$ROOT_DIR/data/product-info.ndjson"; then
    echo "Recording Premier Protein Banana Shake..."
    product_json=$(python3 - <<'PY'
import json
import shortuuid

nut = {
    "added_sugars": 0,
    "biotin": 8,
    "calcium": 650,
    "calories": 160,
    "cholesterol": 20,
    "chromium": 8,
    "copper": 0.25,
    "dietary_fiber": 1,
    "folate": 100,
    "iodine": 37,
    "iron": 1.8,
    "magnesium": 90,
    "manganese": 0.6,
    "molybdenum": 11,
    "niacin": 4,
    "pantothenic_acid": 1.3,
    "phosphorus": 550,
    "potassium": 180,
    "protein": 30,
    "riboflavin": 0.3,
    "saturated_fat": 1,
    "selenium": 14,
    "serving_size": 340,
    "sodium": 240,
    "sugars": 1,
    "thiamin": 0.3,
    "total_carbohydrate": 4,
    "total_fat": 3,
    "trans_fat": 0,
    "vitamin_a": 230,
    "vitamin_b12": 0.6,
    "vitamin_b6": 0.5,
    "vitamin_c": 40,
    "vitamin_d": 6,
    "vitamin_e": None,
    "vitamin_k": 30,
    "zinc": 2.8,
}

prod = {
    "name": "Premier Protein Banana Shake",
    "upc": "643843717850",
    "id": shortuuid.uuid(),
    "nutrition": nut,
}

print(json.dumps(prod))
PY
)
    echo "$product_json" >> "$ROOT_DIR/data/product-info.ndjson"
fi

# Add one unit of the Premier Protein Banana Shake by UPC
echo "Adding banana shake..."
shake_response=$(curl -s -X POST "${BASE_URL}/inventory" \
    -H 'Content-Type: application/json' \
    -d '{"upc": "643843717850"}')
echo "$shake_response"
