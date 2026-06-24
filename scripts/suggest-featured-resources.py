#!/usr/bin/env python3
"""Suggest featured resources to surface thin categories (item 6).

Picks one strong local/regional candidate per state×category where coverage is thin.

Usage:
  python3 scripts/suggest-featured-resources.py
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
OUTPUT = ROOT / "data" / "suggested-featured-resources.json"
sys.path.insert(0, str(ROOT / "scripts"))

from lib.coverage_goals import (  # noqa: E402
    CATEGORY_LABELS,
    STATES,
    TIER_B,
    build_coverage,
    category_gap_stats,
    is_statewide_row,
    normalize_category,
)


def load_csv_rows(csv_name: str) -> list[dict[str, str]]:
    path = DATA_DIR / csv_name
    with path.open(encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    coverage = build_coverage()
    gap_stats = category_gap_stats(coverage)

    thin_threshold_pct = 75.0
    suggestions: list[dict[str, str]] = []

    for state_name, _slug, _counties_path, csv_name in STATES:
        rows = load_csv_rows(csv_name)
        state_gaps = gap_stats[state_name]

        thin_categories = [
            category
            for category, stat in state_gaps.items()
            if float(stat["zero_pct"]) >= thin_threshold_pct and category in TIER_B
        ]
        thin_categories.sort(key=lambda cat: -float(state_gaps[cat]["zero_pct"]))

        for category in thin_categories[:6]:
            candidates = [
                row
                for row in rows
                if normalize_category(row.get("category", "")) == category
                and not is_statewide_row(row)
            ]
            if not candidates:
                candidates = [
                    row
                    for row in rows
                    if normalize_category(row.get("category", "")) == category
                ]
            if not candidates:
                continue

            pick = sorted(candidates, key=lambda row: (row.get("name") or "").lower())[0]
            suggestions.append(
                {
                    "state": state_name,
                    "category": category,
                    "category_label": CATEGORY_LABELS.get(category, category),
                    "resource_id": pick.get("id", ""),
                    "resource_name": pick.get("name", ""),
                    "coverage": pick.get("coverage", ""),
                    "county": pick.get("county", ""),
                    "rationale": (
                        f"Category empty in {state_gaps[category]['zero_pct']}% of counties; "
                        "feature for homepage/pathway visibility"
                    ),
                }
            )

    payload = {
        "generated": date.today().isoformat(),
        "thin_threshold_pct": thin_threshold_pct,
        "suggestions": suggestions,
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(f"Suggested {len(suggestions)} featured candidates → {OUTPUT}")
    for item in suggestions[:8]:
        print(f"  {item['state']} / {item['category_label']}: {item['resource_name'][:50]}")


if __name__ == "__main__":
    main()
