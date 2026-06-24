#!/usr/bin/env python3
"""Audit per-county resource coverage for Phase 3b gap-fill.

Usage:
  python3 scripts/check-county-coverage.py data/{state-slug}-resources.csv src/lib/{state-slug}/counties.ts
  python3 scripts/check-county-coverage.py data/{state-slug}-resources.csv src/lib/{state-slug}/counties.ts --tier-a
  python3 scripts/check-county-coverage.py data/{state-slug}-resources.csv src/lib/{state-slug}/counties.ts --report

Statewide rows do not count toward per-county pins.
"""
from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

TIER_A_CORE = frozenset(
    {
        "housing",
        "healthcare",
        "employment",
        "legal-aid",
        "financial-assistance",
        "substance-use-treatment",
        "probation-parole",
        "food-nutrition",
    }
)

CATEGORY_MINIMUMS: dict[str, int] = {
    "housing": 20,
    "healthcare": 20,
    "employment": 15,
    "probation-parole": 10,
    "legal-aid": 12,
    "education": 12,
    "veterans": 10,
    "basic-needs": 10,
    "substance-use-treatment": 6,
    "financial-assistance": 6,
    "food-nutrition": 4,
    "id-documentation": 4,
    "peer-support": 4,
    "transportation": 3,
    "family-children": 3,
    "state-agency": 4,
    "reentry-organizations": 5,
}

COALITION_MAX_PCT = 25.0
THIN_COUNTY_WARN = 10

DISPLAY_TO_SLUG = {
    "Housing": "housing",
    "Healthcare": "healthcare",
    "Employment": "employment",
    "Legal Aid": "legal-aid",
    "Financial Assistance": "financial-assistance",
    "Substance Use Treatment": "substance-use-treatment",
    "Probation & Parole": "probation-parole",
    "Food & Nutrition": "food-nutrition",
    "State Agency": "state-agency",
    "Reentry Organizations": "reentry-organizations",
    "Education": "education",
    "Basic Needs": "basic-needs",
    "ID & Documentation": "id-documentation",
    "Transportation": "transportation",
    "Peer Support": "peer-support",
    "Family & Children": "family-children",
    "Veterans": "veterans",
}


def load_counties_from_ts(path: Path) -> list[str]:
    counties: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r'\s+"([A-Za-z][A-Za-z .\'-]+)",\s*$', line)
        if match:
            counties.append(match.group(1))
    if not counties:
        raise SystemExit(f"No counties parsed from {path}")
    return counties


def normalize_category(value: str) -> str:
    raw = (value or "").strip()
    if raw in DISPLAY_TO_SLUG:
        return DISPLAY_TO_SLUG[raw]
    return raw.lower().replace(" ", "-")


def is_statewide_row(row: dict[str, str]) -> bool:
    coverage = (row.get("coverage") or "").strip()
    if coverage == "statewide":
        return True
    if coverage:
        return False
    tags = (row.get("tags") or "").split("|")
    return any(tag.strip().lower() == "statewide" for tag in tags)


def county_pin_details(csv_path: Path) -> dict[str, dict[str, set[str] | int]]:
    details: dict[str, dict[str, set[str] | int]] = defaultdict(
        lambda: {"count": 0, "categories": set()}
    )
    with csv_path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if is_statewide_row(row):
                continue
            served_raw = (row.get("served_counties") or "").strip()
            county = (row.get("county") or "").strip()
            targets = (
                [part.strip() for part in served_raw.split("|") if part.strip()]
                if served_raw
                else ([county] if county else [])
            )
            category = normalize_category(row.get("category", ""))
            for target in targets:
                details[target]["count"] = int(details[target]["count"]) + 1
                cats = details[target]["categories"]
                assert isinstance(cats, set)
                cats.add(category)
    return details


def pinned_counties(csv_path: Path) -> Counter[str]:
    details = county_pin_details(csv_path)
    return Counter({county: int(data["count"]) for county, data in details.items()})


def audit_pins(official: list[str], pinned: Counter[str]) -> tuple[int, list[str], list[tuple[str, int]]]:
    covered = [county for county in official if pinned.get(county, 0) > 0]
    uncovered = [county for county in official if pinned.get(county, 0) == 0]
    thin = sorted((county, pinned[county]) for county in official if pinned.get(county, 0) == 1)
    return len(covered), uncovered, thin


def audit_tier_a(official: list[str], details: dict[str, dict[str, set[str] | int]]) -> tuple[int, list[tuple[str, int, list[str]]]]:
    weak: list[tuple[str, int, list[str]]] = []
    strong = 0
    for county in official:
        data = details.get(county, {"count": 0, "categories": set()})
        cats = data["categories"]
        assert isinstance(cats, set)
        core = sorted(cats & TIER_A_CORE)
        count = int(data["count"])
        if len(core) >= 3:
            strong += 1
        else:
            weak.append((county, count, core))
    weak.sort(key=lambda item: (item[1], item[0]))
    return strong, weak


def infer_state_slug(csv_path: Path) -> str:
    stem = csv_path.stem
    if stem.endswith("-resources"):
        return stem[: -len("-resources")]
    return stem


def count_rows_and_categories(csv_path: Path) -> tuple[int, Counter[str]]:
    counts: Counter[str] = Counter()
    row_count = 0
    with csv_path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row_count += 1
            counts[normalize_category(row.get("category", ""))] += 1
    return row_count, counts


def run_enrich_check(csv_path: Path) -> tuple[bool, str]:
    script = Path(__file__).resolve().parent / "enrich-resources.py"
    if not script.is_file():
        return True, "skipped (enrich-resources.py not found)"
    try:
        result = subprocess.run(
            [sys.executable, str(script), "--check-only", str(csv_path)],
            capture_output=True,
            text=True,
            timeout=120,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, f"error running enrich check: {exc}"
    output = (result.stdout or "") + (result.stderr or "")
    passed = result.returncode == 0
    summary = "PASS" if passed else "FAIL"
    if not passed and output.strip():
        last_lines = "\n".join(output.strip().splitlines()[-3:])
        summary = f"{summary} ({last_lines})"
    return passed, summary


def category_minimums_report(counts: Counter[str], total_rows: int) -> tuple[list[str], bool]:
    lines: list[str] = []
    all_met = True
    for slug, minimum in sorted(CATEGORY_MINIMUMS.items()):
        actual = counts.get(slug, 0)
        ok = actual >= minimum
        if not ok:
            all_met = False
        lines.append(f"- {slug}: {actual} / {minimum} — {'OK' if ok else 'BELOW'}")
    coalition = counts.get("reentry-organizations", 0)
    coalition_pct = 100.0 * coalition / total_rows if total_rows else 0.0
    coalition_ok = coalition_pct <= COALITION_MAX_PCT or coalition == 0
    if not coalition_ok:
        all_met = False
    lines.append(
        f"- reentry-organizations share: {coalition_pct:.1f}% "
        f"({'OK' if coalition_ok else f'ABOVE {COALITION_MAX_PCT:.0f}% limit'})"
    )
    return lines, all_met


def build_verdict(
    pin_pct: float,
    uncovered: list[str],
    tier_pct: float,
    thin: list[tuple[str, int]],
    extra: list[str],
    categories_ok: bool,
    enrich_ok: bool,
) -> str:
    blockers: list[str] = []
    if pin_pct < 90.0:
        blockers.append("pins <90%")
    if tier_pct < 50.0:
        blockers.append("Tier A <50%")
    if len(thin) > THIN_COUNTY_WARN:
        blockers.append(f">{THIN_COUNTY_WARN} thin counties")
    if extra:
        blockers.append("data hygiene errors")
    if not categories_ok:
        blockers.append("category minimums unmet")
    if not enrich_ok:
        blockers.append("enrich check failed")
    if uncovered:
        blockers.append("uncovered counties")
    return "COMPLETE" if not blockers else "ANOTHER PASS NEEDED"


def print_coverage_report(
    csv_path: Path,
    counties_path: Path,
    official: list[str],
    pinned: Counter[str],
    details: dict[str, dict[str, set[str] | int]],
    covered_count: int,
    uncovered: list[str],
    thin: list[tuple[str, int]],
    extra: list[str],
    strong: int,
    weak: list[tuple[str, int, list[str]]],
) -> int:
    row_count, cat_counts = count_rows_and_categories(csv_path)
    pin_pct = 100.0 * covered_count / len(official) if official else 0.0
    tier_pct = 100.0 * strong / len(official) if official else 0.0
    pin_status = "PASS" if pin_pct >= 90.0 else "FAIL"
    tier_status = "PASS" if tier_pct >= 50.0 else "WARN"
    state_slug = infer_state_slug(csv_path)
    state_label = state_slug.replace("-", " ").title()
    enrich_ok, enrich_summary = run_enrich_check(csv_path)
    cat_lines, categories_ok = category_minimums_report(cat_counts, row_count)
    verdict = build_verdict(
        pin_pct, uncovered, tier_pct, thin, extra, categories_ok, enrich_ok
    )

    thin_list = ", ".join(county for county, _ in thin) if thin else "none"
    weak_sample = weak[:10]
    weak_line = (
        "; ".join(f"{county} ({count} pins, core={cats or 'none'})" for county, count, cats in weak_sample)
        if weak_sample
        else "none"
    )

    print(f"# Post-research coverage report — {state_label}")
    print(f"Date: {date.today().isoformat()}")
    print(f"Row count: {row_count}")
    print()
    print(f"Pin coverage: {covered_count}/{len(official)} counties ({pin_pct:.1f}%) — {pin_status} (target ≥90%)")
    print(f"Thin counties (1 pin): {len(thin)} — {thin_list}")
    print()
    print(
        f"Tier A core (≥3 of 8): {strong}/{len(official)} counties ({tier_pct:.1f}%) — "
        f"{tier_status} (stretch ≥50%)"
    )
    print(f"Tier A weak sample: {weak_line}")
    print()
    print("Data hygiene:")
    print(f"- Unknown county names: {', '.join(extra) if extra else 'none'}")
    print("- Wrong-state counties in served_counties: review manually if audit flags unknown names")
    print(f"- enrich-resources --check-only: {enrich_summary}")
    print()
    print("Category minimums (17 slugs, program-level rows):")
    for line in cat_lines:
        print(line)
    print()
    print(f"Verdict: **{verdict}**")
    if verdict == "ANOTHER PASS NEEDED":
        print()
        print("Criteria for COMPLETE: pins ≥90%, no jail-county gaps, Tier A ≥50% OR documented gap,")
        print("enrich check passes, no data hygiene blockers, category minimums met.")
    return 0 if verdict == "COMPLETE" else 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit county resource coverage")
    parser.add_argument("csv_path", type=Path)
    parser.add_argument("counties_path", type=Path)
    parser.add_argument(
        "--tier-a",
        action="store_true",
        help="Also report Tier A core category depth (≥3 core categories per county)",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Print structured post-research coverage report with verdict (includes Tier A)",
    )
    args = parser.parse_args()

    if args.report:
        args.tier_a = True

    if not args.csv_path.is_file():
        raise SystemExit(f"CSV not found: {args.csv_path}")
    if not args.counties_path.is_file():
        raise SystemExit(f"Counties file not found: {args.counties_path}")

    official = load_counties_from_ts(args.counties_path)
    details = county_pin_details(args.csv_path)
    pinned = Counter({county: int(data["count"]) for county, data in details.items()})
    official_set = set(official)

    covered_count, uncovered, thin = audit_pins(official, pinned)
    pct = 100.0 * covered_count / len(official) if official else 0.0
    pin_status = "PASS" if pct >= 90.0 else "FAIL"

    if not args.report:
        print(f"CSV: {args.csv_path}")
        print(f"Counties: {covered_count}/{len(official)} pinned ({pct:.1f}%) — {pin_status} (target ≥90%)")
        print(f"Thin (1 pin): {len(thin)}")
        if uncovered:
            print(f"Uncovered ({len(uncovered)}): {', '.join(uncovered)}")
        if thin and len(thin) <= 25:
            print("Thin counties:", ", ".join(f"{county} ({count})" for county, count in thin))
        elif thin:
            print(
                "Thin counties (first 25):",
                ", ".join(f"{county} ({count})" for county, count in thin[:25]),
                "...",
            )

    exit_code = 0 if pct >= 90.0 else 1

    if args.tier_a and not args.report:
        strong, weak = audit_tier_a(official, details)
        tier_pct = 100.0 * strong / len(official) if official else 0.0
        tier_status = "PASS" if tier_pct >= 50.0 else "WARN"
        print()
        print(
            f"Tier A core (≥3 of 8): {strong}/{len(official)} counties ({tier_pct:.1f}%) — {tier_status} (stretch ≥50%)"
        )
        print(f"Tier A weak: {len(weak)} counties")
        if weak:
            sample = weak[:12]
            print(
                "Weak Tier A sample:",
                "; ".join(f"{county} ({count} pins, core={cats or 'none'})" for county, count, cats in sample),
            )

    extra = sorted(set(pinned) - official_set)
    if extra and not args.report:
        print(f"Warning: pins for unknown county names: {', '.join(extra)}")

    if args.report:
        strong, weak = audit_tier_a(official, details)
        sys.exit(
            print_coverage_report(
                args.csv_path,
                args.counties_path,
                official,
                pinned,
                details,
                covered_count,
                uncovered,
                thin,
                extra,
                strong,
                weak,
            )
        )

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
