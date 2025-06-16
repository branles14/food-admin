#!/bin/bash

# Load port from .env if available
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

if [ -f "$ROOT_DIR/.env" ]; then
    env_port=$(grep -E '^PORT=' "$ROOT_DIR/.env" | cut -d '=' -f2)
fi
if [ -z "$env_port" ]; then
    echo "Error: PORT not set in $ROOT_DIR/.env" >&2
    exit 1
fi
PORT=$env_port

BASE_URL="http://localhost:${PORT}"

# Add Jif Creamy Peanut Butter Pouch by UPC
echo "Adding peanut butter..."
pb_response=$(curl -s -X POST "${BASE_URL}/inventory" \
    -H 'Content-Type: application/json' \
    -d '{"upc": "051500245453"}')
echo "$pb_response"

# Add one unit of the Premier Protein Banana Shake with full info
echo "Adding banana shake..."
shake_response=$(curl -s -X POST "${BASE_URL}/inventory" \
    -H 'Content-Type: application/json' \
    -d '{
        "name": "Premier Protein Banana Shake",
        "upc": "643843717850",
        "nutrition": {
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
            "vitamin_e": null,
            "vitamin_k": 30,
            "zinc": 2.8
        }
    }')
echo "$shake_response"
