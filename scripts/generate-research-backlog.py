#!/usr/bin/env python3
"""Generate prioritized research backlog CSVs from coverage gaps.

Usage:
  python3 scripts/generate-research-backlog.py
"""

from __future__ import annotations

import csv
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.coverage_goals import build_coverage, iter_county_category_gaps  # noqa: E402

PHASE1_PATH = ROOT / "data" / "research-backlog-phase1.csv"
PHASE2_PATH = ROOT / "data" / "research-backlog-phase2.csv"


def write_backlog(path: Path, rows: list[dict[str, str]]) -> None:
    fieldnames = [
        "state",
        "county",
        "category",
        "category_label",
        "tier",
        "phase",
        "strategy",
        "sources",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    coverage = build_coverage()
    phase1 = iter_county_category_gaps(coverage, tier="A")
    phase2 = iter_county_category_gaps(coverage, tier="B")

    write_backlog(PHASE1_PATH, phase1)
    write_backlog(PHASE2_PATH, phase2)

    print(f"Generated: {date.today().isoformat()}")
    print(f"Phase 1 (Tier A gaps): {len(phase1)} rows → {PHASE1_PATH}")
    print(f"Phase 2 (Tier B gaps): {len(phase2)} rows → {PHASE2_PATH}")
    if phase1:
        sample = phase1[0]
        print(
            f"First task: {sample['state']} / {sample['county']} / {sample['category_label']}"
        )


if __name__ == "__main__":
    main()
