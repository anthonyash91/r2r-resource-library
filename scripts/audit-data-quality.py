#!/usr/bin/env python3
"""Data quality fixes and audits for coverage work (items 3–4).

Usage:
  python3 scripts/audit-data-quality.py              # report only
  python3 scripts/audit-data-quality.py --fix-categories
  python3 scripts/audit-data-quality.py --fix-statewide-portals
  python3 scripts/audit-data-quality.py --fix-statewide-served-counties
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
sys.path.insert(0, str(ROOT / "scripts"))

from lib.coverage_goals import (  # noqa: E402
    DISPLAY_TO_SLUG,
    STATES,
    category_to_slug,
    is_statewide_row,
    normalize_category,
)

STATEWIDE_PORTAL_PATTERN = re.compile(
    r"portal|benefits\.|211\b|kynect|findhelpnow|claimyourcash",
    re.IGNORECASE,
)

TIER_A_REGIONAL_CATEGORIES = frozenset(
    {"housing", "healthcare", "substance-use-treatment", "employment", "legal-aid"}
)


def csv_paths() -> list[Path]:
    return [DATA_DIR / csv_name for _n, _s, _c, csv_name in STATES]


def audit_categories(rows: list[dict[str, str]]) -> list[str]:
    issues: list[str] = []
    for index, row in enumerate(rows, start=2):
        raw = (row.get("category") or "").strip()
        if not raw:
            issues.append(f"line {index}: empty category ({row.get('name', '')[:40]})")
            continue
        if raw in DISPLAY_TO_SLUG:
            issues.append(f"line {index}: display category '{raw}' → use slug '{DISPLAY_TO_SLUG[raw]}'")
        elif category_to_slug(raw) is None:
            issues.append(f"line {index}: unknown category '{raw}'")
    return issues


def fix_categories(rows: list[dict[str, str]]) -> int:
    changed = 0
    for row in rows:
        raw = (row.get("category") or "").strip()
        slug = category_to_slug(raw)
        if slug and raw != slug:
            row["category"] = slug
            changed += 1
    return changed


def audit_statewide_portals(rows: list[dict[str, str]], source: str) -> list[str]:
    issues: list[str] = []
    for index, row in enumerate(rows, start=2):
        if normalize_category(row.get("category", "")) != "financial-assistance":
            continue
        name = row.get("name") or ""
        if STATEWIDE_PORTAL_PATTERN.search(name) and not is_statewide_row(row):
            issues.append(
                f"{source} line {index}: portal-like financial row not statewide — {name[:60]}"
            )
    return issues


def fix_statewide_portals(rows: list[dict[str, str]]) -> int:
    changed = 0
    for row in rows:
        if normalize_category(row.get("category", "")) != "financial-assistance":
            continue
        name = row.get("name") or ""
        if STATEWIDE_PORTAL_PATTERN.search(name) and not is_statewide_row(row):
            row["coverage"] = "statewide"
            row["county"] = ""
            row["served_counties"] = ""
            changed += 1
    return changed


def fix_statewide_served_counties(rows: list[dict[str, str]]) -> int:
    """Clear served_counties on statewide rows (county may remain as map/office pin)."""
    changed = 0
    for row in rows:
        if (row.get("coverage") or "").strip() != "statewide":
            continue
        if (row.get("served_counties") or "").strip():
            row["served_counties"] = ""
            changed += 1
    return changed


def audit_served_counties(rows: list[dict[str, str]], source: str) -> list[str]:
    issues: list[str] = []
    for index, row in enumerate(rows, start=2):
        coverage = (row.get("coverage") or "").strip()
        served_raw = (row.get("served_counties") or "").strip()
        served = [part.strip() for part in served_raw.split("|") if part.strip()] if served_raw else []
        category = normalize_category(row.get("category", ""))

        if coverage == "multi" and not served:
            issues.append(f"{source} line {index}: multi coverage but empty served_counties")

        if coverage == "statewide" and served:
            issues.append(
                f"{source} line {index}: statewide row has served_counties "
                f"({row.get('name', '')[:50]})"
            )

        if (
            category in TIER_A_REGIONAL_CATEGORIES
            and coverage == "single"
            and len(served) == 1
            and (row.get("name") or "").lower().count("region") > 0
        ):
            issues.append(
                f"{source} line {index}: regional name but single coverage — review served_counties"
            )
    return issues


def load_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    return fieldnames, rows


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Resource CSV data quality audit")
    parser.add_argument(
        "--fix-categories",
        action="store_true",
        help="Normalize display category names to slugs in CSVs",
    )
    parser.add_argument(
        "--fix-statewide-portals",
        action="store_true",
        help="Mark portal-like financial rows as coverage=statewide",
    )
    parser.add_argument(
        "--fix-statewide-served-counties",
        action="store_true",
        help="Clear served_counties on rows with coverage=statewide",
    )
    args = parser.parse_args()

    all_category_issues: list[str] = []
    all_portal_issues: list[str] = []
    all_served_issues: list[str] = []
    total_category_fixes = 0
    total_portal_fixes = 0
    total_served_fixes = 0

    for path in csv_paths():
        if not path.is_file():
            print(f"SKIP missing {path}")
            continue
        fieldnames, rows = load_csv(path)
        source = path.name

        if args.fix_categories:
            total_category_fixes += fix_categories(rows)
        if args.fix_statewide_portals:
            total_portal_fixes += fix_statewide_portals(rows)
        if args.fix_statewide_served_counties:
            total_served_fixes += fix_statewide_served_counties(rows)
        if args.fix_categories or args.fix_statewide_portals or args.fix_statewide_served_counties:
            write_csv(path, fieldnames, rows)

        all_category_issues.extend(audit_categories(rows))
        all_portal_issues.extend(audit_statewide_portals(rows, source))
        all_served_issues.extend(audit_served_counties(rows, source))

    print("# Data quality audit")
    print()
    print(f"Category slug issues: {len(all_category_issues)}")
    for issue in all_category_issues[:15]:
        print(f"  - {issue}")
    if len(all_category_issues) > 15:
        print(f"  ... and {len(all_category_issues) - 15} more")

    print()
    print(f"Statewide portal issues: {len(all_portal_issues)}")
    for issue in all_portal_issues[:10]:
        print(f"  - {issue}")

    print()
    print(f"served_counties review flags: {len(all_served_issues)}")
    for issue in all_served_issues[:10]:
        print(f"  - {issue}")
    if len(all_served_issues) > 10:
        print(f"  ... and {len(all_served_issues) - 10} more")

    if args.fix_categories:
        print()
        print(f"Fixed category slugs: {total_category_fixes}")
    if args.fix_statewide_portals:
        print(f"Fixed statewide portals: {total_portal_fixes}")
    if args.fix_statewide_served_counties:
        print(f"Cleared served_counties on statewide rows: {total_served_fixes}")


if __name__ == "__main__":
    main()
