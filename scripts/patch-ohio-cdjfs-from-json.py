#!/usr/bin/env python3
"""Patch Ohio CDJFS stub rows in data/ohio-resources.csv from synced JSON.

Updates address, city, phone, website, and region for county JFS financial-assistance
rows that are missing contact fields or match a county in the sync file.

Usage:
  python3 scripts/sync-county-benefits-offices.py --state ohio
  python3 scripts/patch-ohio-cdjfs-from-json.py
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "ohio-resources.csv"
JSON_PATH = ROOT / "scripts" / "data" / "ohio-cdjfs-offices.json"

JFS_NAME = re.compile(r"^(.+?) County Job and Family Services$")


def load_offices() -> dict[str, dict]:
    offices = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    return {office["county"]: office for office in offices}


def main() -> None:
    if not JSON_PATH.exists():
        raise SystemExit(f"Missing {JSON_PATH}; run sync-county-benefits-offices.py --state ohio first")

    by_county = load_offices()
    with CSV_PATH.open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit(f"No rows in {CSV_PATH}")

    fieldnames = list(rows[0].keys())
    patched = 0

    for row in rows:
        if row.get("category") != "financial-assistance":
            continue
        if (row.get("coverage") or "").strip() == "statewide":
            continue
        name_match = JFS_NAME.match(row.get("name", "").strip())
        if not name_match:
            continue
        county = name_match.group(1)
        office = by_county.get(county)
        if not office or not office.get("address"):
            continue

        city = office.get("city") or row.get("city") or county
        changed = False
        updates = {
            "address": office.get("address", ""),
            "city": city,
            "phone": office.get("phone", ""),
            "website": office.get("website") or row.get("website", ""),
            "region": f"{city} / {county} County",
        }
        for field, value in updates.items():
            if value and row.get(field, "") != value:
                row[field] = value
                changed = True
        if changed:
            patched += 1

    with CSV_PATH.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Patched {patched} Ohio CDJFS rows in {CSV_PATH.name}")


if __name__ == "__main__":
    main()
