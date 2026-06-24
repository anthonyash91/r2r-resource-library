#!/usr/bin/env python3
"""Audit and normalize pipe-separated service strings in resource CSV files."""
from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
sys.path.insert(0, str(ROOT / "scripts"))

from lib.service_types import (  # noqa: E402
    CANONICAL_SERVICES,
    audit_services,
    normalize_services_field,
    unmapped_services,
)

DEFAULT_CSV_PATHS = [
    DATA_DIR / "kentucky-resources.csv",
    DATA_DIR / "ohio-resources.csv",
    DATA_DIR / "indiana-resources.csv",
    DATA_DIR / "tennessee-resources.csv",
]


def resolve_csv_paths(explicit: list[str] | None) -> list[Path]:
    if explicit:
        return [Path(p) for p in explicit]
    return DEFAULT_CSV_PATHS


def print_audit_report(report) -> None:
    print("Service type audit")
    print(f"  CSV files: {len(report.csv_paths)}")
    print(f"  Unique before: {report.unique_before}")
    print(f"  Unique after:  {report.unique_after}")
    print(f"  Canonical types in use: {report.canonical_types_used}")
    print(f"  Total canonical definitions: {len(CANONICAL_SERVICES)}")
    print(f"  Occurrences before: {report.total_occurrences_before}")
    print(f"  Occurrences after:  {report.total_occurrences_after}")
    if report.unmapped:
        print(f"\nUnmapped services ({len(report.unmapped)}):")
        for item in report.unmapped:
            print(f"  - {item}")
    if report.merges:
        print("\nTop merges:")
        for src, dst, count in report.merges[:25]:
            print(f"  {count:4d}  {src!r}  ->  {dst!r}")


def apply_normalization(csv_paths: list[Path]) -> list[str]:
    changed_files: list[str] = []
    for path in csv_paths:
        if not path.exists():
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames or "services" not in reader.fieldnames:
                continue
            fieldnames = reader.fieldnames
            rows = list(reader)

        file_changed = False
        for row in rows:
            raw = row.get("services") or ""
            normalized = normalize_services_field(raw)
            if normalized != raw:
                row["services"] = normalized
                file_changed = True

        if not file_changed:
            continue

        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        changed_files.append(str(path))

    return changed_files


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--audit",
        action="store_true",
        help="Print before/after summary and top merges",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Rewrite CSV services columns in place",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit 1 if any unmapped service strings remain",
    )
    parser.add_argument(
        "csv_paths",
        nargs="*",
        help="Optional CSV paths (defaults to all four state resource CSVs)",
    )
    args = parser.parse_args()

    if not (args.audit or args.apply or args.check):
        parser.error("Specify at least one of --audit, --apply, or --check")

    csv_paths = resolve_csv_paths(args.csv_paths or None)
    exit_code = 0

    if args.audit or args.check:
        report = audit_services(csv_paths)
        if args.audit:
            print_audit_report(report)
        if args.check and report.unmapped:
            if not args.audit:
                print(f"Unmapped services ({len(report.unmapped)}):")
                for item in report.unmapped:
                    print(f"  - {item}")
            exit_code = 1

    if args.apply:
        changed = apply_normalization(csv_paths)
        if changed:
            print("Normalized services in:")
            for path in changed:
                print(f"  {path}")
        else:
            print("No CSV changes needed.")
        if args.check:
            remaining = unmapped_services(csv_paths)
            if remaining:
                print(f"Unmapped after apply ({len(remaining)}):")
                for item in remaining:
                    print(f"  - {item}")
                exit_code = 1

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
