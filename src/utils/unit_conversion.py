"""Simple helpers for unit conversion."""

from __future__ import annotations

import re


def to_grams(size: str) -> float:
    """Convert a size string to grams when possible."""
    size = size.strip().lower()
    match = re.match(r"([0-9]*\.?[0-9]+)\s*(\w+)", size)
    if not match:
        raise ValueError(f"Unrecognized size: {size}")
    value = float(match.group(1))
    unit = match.group(2)
    if unit in {"g", "gram", "grams"}:
        grams = value
    elif unit in {"kg", "kilogram", "kilograms"}:
        grams = value * 1000
    elif unit in {"oz", "ounce", "ounces"}:
        grams = value * 28.3495
    elif unit in {"lb", "pound", "lbs", "pounds"}:
        grams = value * 453.592
    else:
        raise ValueError(f"Unsupported unit: {unit}")
    return grams


def format_metric(size: str) -> str:
    """Return a metric string in grams from the given size."""
    grams = round(to_grams(size))
    return f"{grams} g"
