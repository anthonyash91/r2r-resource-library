#!/usr/bin/env python3
"""Append Phase 3b gap-fill rows to data/kentucky-resources.csv."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "kentucky-resources.csv"
LOG_PATH = ROOT / "data" / "kentucky-research-log.csv"
DATE = "2026-06-23"

COLUMNS = [
    "id",
    "name",
    "category",
    "region",
    "description",
    "description_es",
    "address",
    "city",
    "phone",
    "email",
    "website",
    "eligibility",
    "eligibility_es",
    "notes",
    "notes_es",
    "hours",
    "tags",
    "services",
    "county",
    "served_counties",
    "coverage",
    "intake_signals",
]

LOG_COLUMNS = [
    "source_url",
    "source_type",
    "date_accessed",
    "confidence",
    "notes",
    "id_reference",
]

ENTRIES: list[dict[str, str]] = []


def add(**kw: str) -> None:
    ENTRIES.append(kw)


def main() -> None:
    from phase3b_gapfill import register_phase3b_kentucky

    with CSV_PATH.open(encoding="utf-8") as f:
        existing = list(csv.DictReader(f))

    register_phase3b_kentucky(add, entries=existing)

    next_id = max(int(row["id"]) for row in existing if row["id"].isdigit()) + 1
    log_rows = []

    for entry in ENTRIES:
        row = {col: entry.get(col, "") for col in COLUMNS}
        row["id"] = str(next_id)
        row.setdefault("intake_signals", "accepts_criminal_record|walk_in_ok")
        existing.append(row)
        log_rows.append(
            {
                "source_url": entry["_source"],
                "source_type": entry["_source_type"],
                "date_accessed": DATE,
                "confidence": entry["_confidence"],
                "notes": f"Phase 3b gap-fill id {next_id}: {entry['name']}",
                "id_reference": str(next_id),
            }
        )
        next_id += 1

    with CSV_PATH.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(existing)

    log_exists = LOG_PATH.is_file()
    with LOG_PATH.open("a" if log_exists else "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=LOG_COLUMNS, quoting=csv.QUOTE_MINIMAL)
        if not log_exists:
            writer.writeheader()
        writer.writerows(log_rows)

    print(f"Appended {len(ENTRIES)} Kentucky gap-fill rows ({CSV_PATH.name} now {len(existing)} rows)")


if __name__ == "__main__":
    main()
