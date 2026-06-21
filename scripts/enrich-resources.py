#!/usr/bin/env python3
"""Enrich a resources CSV to publication-ready narrative depth (Kentucky parity).

Usage:
  python3 scripts/enrich-resources.py data/ohio-resources.csv
  python3 scripts/enrich-resources.py data/ohio-resources.csv --write-json data/enrichments/ohio-enriched.json
  python3 scripts/enrich-resources.py --check-only data/ohio-resources.csv
"""
from __future__ import annotations

import csv
import json
import statistics
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "lib"))
from resource_enricher import enrich_row  # noqa: E402

ENRICHMENT_FIELDS = (
    "description",
    "description_es",
    "eligibility",
    "eligibility_es",
    "notes",
    "notes_es",
    "hours",
    "tags",
    "services",
)

GENERIC_PATTERNS = (
    "Contact program for current intake",
    "contact program for current eligibility",
)


def check_quality(rows: list[dict[str, str]]) -> int:
    desc_lens = [len(r.get("description", "")) for r in rows]
    median = statistics.median(desc_lens) if desc_lens else 0
    generic_desc = sum(
        1 for r in rows if any(p.lower() in (r.get("description") or "").lower() for p in GENERIC_PATTERNS)
    )
    missing_es = sum(1 for r in rows if not (r.get("description_es") or "").strip())
    print(f"Quality check ({len(rows)} rows):")
    print(f"  description median: {median:.0f} chars")
    print(f"  generic description rows: {generic_desc}")
    print(f"  missing description_es: {missing_es}")
    ok = median >= 350 and generic_desc == 0 and missing_es == 0
    print("  PASS" if ok else "  FAIL — run without --check-only to enrich")
    return 0 if ok else 1


def main() -> None:
    args = sys.argv[1:]
    check_only = "--check-only" in args
    if check_only:
        args.remove("--check-only")

    if not args or args[0].startswith("-"):
        print("Usage: python3 scripts/enrich-resources.py [--check-only] <csv-path> [--write-json path]")
        sys.exit(1)

    csv_path = Path(args[0]).resolve()
    json_path = None
    if "--write-json" in args:
        idx = args.index("--write-json")
        json_path = Path(args[idx + 1]).resolve()

    with csv_path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys()) if rows else []

    if check_only:
        sys.exit(check_quality(rows))

    enrichments: dict[str, dict[str, str]] = {}
    enriched_rows = []
    for row in rows:
        enriched = enrich_row(row)
        enriched_rows.append(enriched)
        patch = {k: enriched[k] for k in ENRICHMENT_FIELDS if enriched.get(k) != row.get(k)}
        if patch:
            enrichments[row["id"]] = patch

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(enriched_rows)

    if json_path:
        json_path.parent.mkdir(parents=True, exist_ok=True)
        json_path.write_text(json.dumps(enrichments, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    desc_lens = [len(r["description"]) for r in enriched_rows]
    print(f"Enriched {len(enriched_rows)} rows in {csv_path}")
    print(f"  description median: {statistics.median(desc_lens):.0f} chars (mean {statistics.mean(desc_lens):.0f})")
    print(f"  rows patched: {len(enrichments)}")
    if json_path:
        print(f"  audit JSON: {json_path}")
    sys.exit(check_quality(enriched_rows))


if __name__ == "__main__":
    main()
