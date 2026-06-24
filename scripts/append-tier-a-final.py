#!/usr/bin/env python3
"""Append Tier A final gap rows to state CSVs (dedupe by name)."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
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


def append_state(state: str, register_fn) -> int:
    csv_path = ROOT / "data" / f"{state}-resources.csv"
    log_path = ROOT / "data" / f"{state}-research-log.csv"
    entries: list[dict[str, str]] = []

    def add(**kw: str) -> None:
        entries.append(kw)

    with csv_path.open(encoding="utf-8") as handle:
        existing = list(csv.DictReader(handle))
    existing_names = {row["name"] for row in existing}
    register_fn(add)
    new_entries = [entry for entry in entries if entry["name"] not in existing_names]
    if not new_entries:
        return 0

    next_id = max(int(row["id"]) for row in existing if row["id"].isdigit()) + 1
    log_rows = []
    for entry in new_entries:
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
                "notes": f"Tier A final gap id {next_id}: {entry['name']}",
                "id_reference": str(next_id),
            }
        )
        next_id += 1

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=COLUMNS, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(existing)

    log_exists = log_path.is_file()
    with log_path.open("a" if log_exists else "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=LOG_COLUMNS, quoting=csv.QUOTE_MINIMAL)
        if not log_exists:
            writer.writeheader()
        writer.writerows(log_rows)

    print(f"Appended {len(new_entries)} rows to {csv_path.name}")
    return len(new_entries)


def main() -> None:
    from phase3b_gapfill import register_tier_a_tennessee_gaps

    append_state("tennessee", register_tier_a_tennessee_gaps)


if __name__ == "__main__":
    main()
