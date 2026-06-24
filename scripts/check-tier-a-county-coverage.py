#!/usr/bin/env python3
"""Scorecard for county×Tier A coverage goals (primary north-star metric).

Usage:
  python3 scripts/check-tier-a-county-coverage.py
  python3 scripts/check-tier-a-county-coverage.py --json data/coverage-scorecard.json
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from lib.coverage_goals import (  # noqa: E402
    TIER_A_SLOT_FILL_FLOOR,
    TIER_A_SLOT_FILL_TARGET_90D,
    build_coverage,
    compute_scorecard,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Tier A county×category coverage scorecard")
    parser.add_argument(
        "--json",
        type=Path,
        default=ROOT / "data" / "coverage-scorecard.json",
        help="Write scorecard JSON",
    )
    parser.add_argument(
        "--fail-below-floor",
        action="store_true",
        help="Exit 1 if fill rate is below the regression floor",
    )
    args = parser.parse_args()

    coverage = build_coverage()
    scorecard = compute_scorecard(coverage)
    scorecard["generated"] = date.today().isoformat()

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(scorecard, indent=2), encoding="utf-8")

    print("# Tier A county×category coverage scorecard")
    print(f"Date: {scorecard['generated']}")
    print(f"Status: {scorecard['status']}")
    print(
        f"Tier A slot fill: {scorecard['tier_a_fill_pct']}% "
        f"({scorecard['tier_a_filled']:,} / {scorecard['tier_a_slots']:,})"
    )
    print(f"Counties with full Tier A (8/8): {scorecard['full_tier_a_counties']}")
    print(f"Weak counties (≤3 Tier A): {scorecard['weak_counties']}")
    print()
    print("Targets:")
    targets = scorecard["targets"]
    print(f"  Floor (no regression): {targets['floor_pct']}%")
    print(f"  90-day target: {targets['target_90d_pct']}%")
    print(f"  Stretch: {targets['stretch_pct']}%")
    print(f"  Full Tier A counties (90d): {targets['full_tier_a_counties_90d']}")
    print(f"  Weak counties (90d): ≤{targets['weak_counties_90d']}")
    print()
    print("By state:")
    for state, data in scorecard["by_state"].items():
        pct = round(100.0 * float(data["tier_a_fill_rate"]), 1)
        print(
            f"  {state}: {pct}% fill | full Tier A: {data['full_tier_a_counties']} | "
            f"weak: {data['weak_counties']}"
        )
    print()
    print(f"Wrote {args.json}")

    if args.fail_below_floor and float(scorecard["tier_a_fill_rate"]) < TIER_A_SLOT_FILL_FLOOR:
        sys.exit(1)
    if float(scorecard["tier_a_fill_rate"]) < TIER_A_SLOT_FILL_TARGET_90D:
        sys.exit(0)


if __name__ == "__main__":
    main()
