"""Helpers for validating nutrition data."""

from __future__ import annotations

from typing import Any, Dict, Optional

# Supported nutrient keys including micronutrients
NUTRIENT_FIELDS = {
    "serving_size",
    "calories",
    "total_fat",
    "saturated_fat",
    "trans_fat",
    "cholesterol",
    "sodium",
    "total_carbohydrate",
    "dietary_fiber",
    "sugars",
    "added_sugars",
    "protein",
    "vitamin_d",
    "vitamin_e",
    "niacin",
    "calcium",
    "iron",
    "potassium",
    "vitamin_a",
    "vitamin_c",
    "vitamin_k",
    "thiamin_b1",
    "riboflavin_b2",
    "vitamin_b6",
    "vitamin_b12",
    "folate",
    "biotin",
    "pantothenic_acid",
    "phosphorus",
    "magnesium",
    "selenium",
    "manganese",
    "molybdenum",
    "iodine",
    "zinc",
    "copper",
    "chromium",
}


def filter_nutrition(info: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Return a dictionary containing only supported nutrient keys."""
    if info is None:
        return None
    return {k: v for k, v in info.items() if k in NUTRIENT_FIELDS}
