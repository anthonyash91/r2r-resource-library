#!/usr/bin/env python3
"""Patch served_counties and Kentucky DCBS contact fields in existing CSVs."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PURCHASE = "Ballard|Calloway|Carlisle|Fulton|Graves|Hickman|Livingston|Marshall|McCracken"

LAWO_SERVED = (
    "Allen|Ashland|Auglaize|Champaign|Clark|Crawford|Darke|Defiance|Erie|Fulton|Greene|"
    "Hancock|Hardin|Henry|Huron|Logan|Lucas|Marion|Mercer|Miami|Montgomery|Ottawa|Paulding|"
    "Preble|Putnam|Richland|Sandusky|Seneca|Shelby|Van Wert|Williams|Wood|Wyandot"
)
LASCO_SERVED = (
    "Adams|Athens|Belmont|Brown|Butler|Carroll|Champaign|Clark|Clermont|Clinton|Coshocton|"
    "Fairfield|Fayette|Franklin|Gallia|Greene|Guernsey|Hamilton|Harrison|Highland|Hocking|"
    "Jackson|Jefferson|Knox|Lawrence|Licking|Madison|Meigs|Miami|Monroe|Morgan|Muskingum|"
    "Noble|Perry|Pickaway|Pike|Ross|Scioto|Vinton|Warren|Washington"
)


def patch_ohio(rows: list[dict]) -> int:
    changed = 0
    for row in rows:
        name = row.get("name", "")
        if name == "Legal Aid of Western Ohio (LAWO)" and row.get("served_counties") != LAWO_SERVED:
            row["served_counties"] = LAWO_SERVED
            changed += 1
        if name == "Legal Aid of Southeast and Central Ohio (LASCO)" and row.get("served_counties") != LASCO_SERVED:
            row["served_counties"] = LASCO_SERVED
            changed += 1
    return changed


def patch_kentucky(rows: list[dict], offices: dict[str, dict]) -> int:
    changed = 0
    purchase_names = (
        "Four Rivers Behavioral Health — Paducah",
        "Kentucky Career Center — Paducah / West Kentucky",
    )
    for row in rows:
        if row.get("name") in purchase_names and row.get("served_counties") != PURCHASE:
            row["served_counties"] = PURCHASE
            changed += 1
        if "DCBS" not in row.get("name", ""):
            continue
        match = re.search(r"DCBS — ([A-Za-z .'-]+) County Family Support", row.get("name", ""))
        if not match:
            continue
        county = match.group(1)
        office = offices.get(county)
        if not office or not office.get("address"):
            continue
        city = office.get("city") or row.get("city") or county
        updates = {
            "address": office.get("address", ""),
            "city": city,
            "phone": office.get("phone", "") or row.get("phone", ""),
            "region": f"{city} / {county} County",
        }
        for field, value in updates.items():
            if value and row.get(field, "") != value:
                row[field] = value
                changed += 1
    return changed


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    ohio_path = ROOT / "data" / "ohio-resources.csv"
    ky_path = ROOT / "data" / "kentucky-resources.csv"
    ky_json = ROOT / "scripts" / "data" / "kentucky-dcbs-offices.json"

    ohio_rows = list(csv.DictReader(ohio_path.open(encoding="utf-8")))
    ky_rows = list(csv.DictReader(ky_path.open(encoding="utf-8")))
    offices = {office["county"]: office for office in json.loads(ky_json.read_text(encoding="utf-8"))}

    oh = patch_ohio(ohio_rows)
    ky = patch_kentucky(ky_rows, offices)
    write_csv(ohio_path, ohio_rows)
    write_csv(ky_path, ky_rows)
    print(f"Patched {oh} Ohio field updates and {ky} Kentucky field updates")


if __name__ == "__main__":
    main()
