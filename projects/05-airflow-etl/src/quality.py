"""Dependency-free quality checks suitable for reuse in pipeline tasks."""
from __future__ import annotations

from collections import Counter
from typing import Iterable, Mapping


def check_required_fields(rows: Iterable[Mapping], required: set[str]) -> dict:
    rows = list(rows)
    missing = Counter()
    for row in rows:
        for field in required:
            if row.get(field) in (None, ""):
                missing[field] += 1
    return {"row_count": len(rows), "missing_by_field": dict(missing)}


def assert_minimum_rows(actual: int, minimum: int) -> None:
    if actual < minimum:
        raise ValueError(f"Freshness/volume check failed: {actual} rows; expected at least {minimum}")
