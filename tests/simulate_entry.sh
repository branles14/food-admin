#!/bin/bash

# Load port from .env if available
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

if [[ -f "$ROOT_DIR/.env" ]]; then
    env_port=$(grep -E '^PORT=' "$ROOT_DIR/.env" | cut -d '=' -f2)
fi
if [[ -z "$env_port" ]]; then
    echo "Error: PORT not set in $ROOT_DIR/.env" >&2
    exit 1
fi
PORT=$env_port

BASE_URL="http://localhost:${PORT}"

# Add Jif Creamy Peanut Butter Pouch by UPC
echo "Adding peanut butter to inventory using only UPC..."
pb_response=$(curl -s -X POST "${BASE_URL}/inventory" \
    -H 'Content-Type: application/json' \
    -d '{"upc": "051500245453"}')

if [[ $? == 0 ]]; then
    echo "$pb_response"
else
    echo "ERROR: Failed to add peanut butter"
    exit 1
fi

# Add one unit of the Premier Protein Banana Shake with full info
echo "Adding banana shake using full product details..."
shake_response=$(curl -s -X POST "${BASE_URL}/inventory" \
    -H 'Content-Type: application/json' \
    -d '{
        "name": "Premier Protein Banana Shake",
        "upc": "643843717850",
        "nutrition": {
            "serving": {"size_g": 340, "calories": 160},
            "macros": {
                "total_fat": 3,
                "saturated_fat": 1,
                "trans_fat": 0,
                "cholesterol": 20,
                "protein": 30,
                "total_carbohydrate": 4,
                "dietary_fiber": 1,
                "sugars": 1,
                "added_sugars": 0,
                "sodium": 240,
                "potassium": 180
            },
            "micronutrients": {
                "iron": 1.8,
                "calcium": 650,
                "vitamin_d": 6,
                "vitamin_e": null,
                "niacin": 4,
                "biotin": 8,
                "chromium": 8,
                "copper": 0.25,
                "folate": 100,
                "iodine": 37,
                "magnesium": 90,
                "manganese": 0.6,
                "molybdenum": 11,
                "pantothenic_acid": 1.3,
                "phosphorus": 550,
                "riboflavin": 0.3,
                "selenium": 14,
                "thiamin": 0.3,
                "vitamin_a": 230,
                "vitamin_b12": 0.6,
                "vitamin_b6": 0.5,
                "vitamin_c": 40,
                "vitamin_k": 30,
                "zinc": 2.8
            }
        },
        "tags": [
            "protein"
        ]
    }')

if [[ $? == 0 ]]; then
    echo "$shake_response"
else
    echo "ERROR: Failed to add banana shake"
    exit 1
fi
