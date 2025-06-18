"""Helpers for validating nutrition data."""

from __future__ import annotations

from typing import Any, Dict, Optional

# Supported nutrient keys grouped by category
SERVING_FIELDS = {"size_g", "calories"}

MACRO_FIELDS = {
    "total_fat",
    "saturated_fat",
    "trans_fat",
    "cholesterol",
    "protein",
    "total_carbohydrate",
    "dietary_fiber",
    "sugars",
    "added_sugars",
    "sodium",
    "potassium",
}

MICRO_FIELDS = {
    "iron",
    "calcium",
    "vitamin_d",
    "vitamin_e",
    "niacin",
    "biotin",
    "chromium",
    "copper",
    "folate",
    "iodine",
    "magnesium",
    "manganese",
    "molybdenum",
    "pantothenic_acid",
    "phosphorus",
    "riboflavin",
    "selenium",
    "thiamin",
    "vitamin_a",
    "vitamin_b12",
    "vitamin_b6",
    "vitamin_c",
    "vitamin_k",
    "zinc",
}


def _filter_section(data: Dict[str, Any], allowed: set[str]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if k in allowed}


def filter_nutrition(info: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Normalize nutrition data into the new nested format."""
    if info is None:
        return None

    if any(k in info for k in ("serving", "macros", "micronutrients")):
        serving = _filter_section(info.get("serving", {}), SERVING_FIELDS)
        macros = _filter_section(info.get("macros", {}), MACRO_FIELDS)
        micros = _filter_section(info.get("micronutrients", {}), MICRO_FIELDS)
    else:
        serving = {}
        macros = {}
        micros = {}
        for key, value in info.items():
            if key in {"serving_size", "size_g"}:
                serving["size_g"] = value
            elif key == "calories":
                serving["calories"] = value
            elif key in MACRO_FIELDS:
                macros[key] = value
            elif key in MICRO_FIELDS:
                micros[key] = value
    result: Dict[str, Any] = {}
    if serving:
        result["serving"] = serving
    if macros:
        result["macros"] = macros
    if micros:
        result["micronutrients"] = micros
    return result or None
