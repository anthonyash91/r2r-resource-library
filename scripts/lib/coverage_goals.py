"""County×category coverage goals — shared by audit and CI scripts."""

from __future__ import annotations

import csv
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"

STATES = [
    ("Kentucky", "kentucky", "src/lib/kentucky/counties.ts", "kentucky-resources.csv"),
    ("Ohio", "ohio", "src/lib/ohio/counties.ts", "ohio-resources.csv"),
    ("Indiana", "indiana", "src/lib/indiana/counties.ts", "indiana-resources.csv"),
    ("Tennessee", "tennessee", "src/lib/tennessee/counties.ts", "tennessee-resources.csv"),
    ("Michigan", "michigan", "src/lib/michigan/counties.ts", "michigan-resources.csv"),
]

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

ALL_CATEGORIES = [
    "housing",
    "healthcare",
    "employment",
    "legal-aid",
    "financial-assistance",
    "substance-use-treatment",
    "probation-parole",
    "food-nutrition",
    "education",
    "veterans",
    "basic-needs",
    "id-documentation",
    "transportation",
    "peer-support",
    "family-children",
    "reentry-organizations",
    "state-agency",
]

TIER_A = frozenset(
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

TIER_B = frozenset(
    {
        "education",
        "veterans",
        "basic-needs",
        "id-documentation",
        "transportation",
        "peer-support",
        "family-children",
        "reentry-organizations",
    }
)

CATEGORY_LABELS = {
    "housing": "Housing",
    "healthcare": "Healthcare",
    "employment": "Employment",
    "legal-aid": "Legal Aid",
    "financial-assistance": "Financial Assistance",
    "substance-use-treatment": "Substance Use Treatment",
    "probation-parole": "Probation & Parole",
    "food-nutrition": "Food & Nutrition",
    "education": "Education",
    "veterans": "Veterans",
    "basic-needs": "Basic Needs",
    "id-documentation": "ID & Documentation",
    "transportation": "Transportation",
    "peer-support": "Peer Support",
    "family-children": "Family & Children",
    "reentry-organizations": "Reentry Organizations",
    "state-agency": "State Agency",
}

PHASE_1_CATEGORY_PRIORITY = [
    "housing",
    "substance-use-treatment",
    "healthcare",
    "employment",
    "probation-parole",
    "food-nutrition",
    "legal-aid",
    "financial-assistance",
]

PHASE_2_CATEGORY_PRIORITY = [
    "id-documentation",
    "transportation",
    "peer-support",
    "family-children",
    "veterans",
    "education",
    "basic-needs",
    "reentry-organizations",
]

RESEARCH_SOURCES: dict[str, str] = {
    "housing": "CoC/HUD; DOC reentry housing; state housing finance",
    "healthcare": "HRSA FQHC locator; state MH/SUD directory",
    "employment": "CareerOneStop LWDB; state workforce board",
    "legal-aid": "LSC map; state legal aid network",
    "financial-assistance": "County JFS/DCBS/DFR directory (verify pin exists)",
    "substance-use-treatment": "SAMHSA; FindHelpNow/state SUD directory",
    "probation-parole": "DOC/DRC regional supervision map",
    "food-nutrition": "Feeding America; SNAP outreach partners",
    "education": "Adult ed/ABLE; community college reentry",
    "veterans": "VA; county veterans service officer",
    "basic-needs": "211; United Way basic needs partners",
    "id-documentation": "Legal aid ID clinic; circuit clerk vital records",
    "transportation": "Transit authority voucher programs",
    "peer-support": "State peer certification roster",
    "family-children": "211; family reentry nonprofits",
    "reentry-organizations": "State reentry council; nonprofit coalitions",
    "state-agency": "State DOC/reentry navigation",
}

TIER_A_SLOT_FILL_FLOOR = 0.50
TIER_A_SLOT_FILL_TARGET_90D = 0.70
TIER_A_SLOT_FILL_STRETCH = 0.85
FULL_TIER_A_COUNTIES_TARGET_90D = 40
WEAK_COUNTY_DEPTH_MAX = 3
WEAK_COUNTIES_TARGET_90D = 60


def load_counties(relative_path: str) -> list[str]:
    path = ROOT / relative_path
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


def category_to_slug(value: str) -> str | None:
    slug = normalize_category(value)
    return slug if slug in ALL_CATEGORIES else None


def is_statewide_row(row: dict[str, str]) -> bool:
    coverage = (row.get("coverage") or "").strip()
    if coverage == "statewide":
        return True
    if coverage:
        return False
    tags = (row.get("tags") or "").split("|")
    return any(tag.strip().lower() == "statewide" for tag in tags)


def served_counties(row: dict[str, str]) -> list[str]:
    served_raw = (row.get("served_counties") or "").strip()
    if served_raw:
        return [part.strip() for part in served_raw.split("|") if part.strip()]
    county = (row.get("county") or "").strip()
    return [county] if county else []


@dataclass
class CountyCoverage:
    state: str
    county: str
    local_by_category: Counter[str] = field(default_factory=Counter)
    statewide_by_category: Counter[str] = field(default_factory=Counter)

    def local_count(self, category: str) -> int:
        return self.local_by_category.get(category, 0)

    def missing_tier_a(self) -> list[str]:
        return [cat for cat in sorted(TIER_A) if self.local_count(cat) == 0]

    def missing_tier_b(self) -> list[str]:
        return [cat for cat in sorted(TIER_B) if self.local_count(cat) == 0]

    def tier_a_depth(self) -> int:
        return sum(1 for cat in TIER_A if self.local_count(cat) > 0)

    def total_local(self) -> int:
        return sum(self.local_by_category.values())


def load_state_resources(state_name: str, csv_name: str) -> list[dict[str, str]]:
    path = DATA_DIR / csv_name
    rows: list[dict[str, str]] = []
    with path.open(encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            row["_state"] = state_name
            rows.append(row)
    return rows


def build_coverage() -> dict[str, dict[str, CountyCoverage]]:
    coverage: dict[str, dict[str, CountyCoverage]] = {}

    for state_name, _slug, counties_path, csv_name in STATES:
        counties = load_counties(counties_path)
        coverage[state_name] = {
            county: CountyCoverage(state=state_name, county=county) for county in counties
        }
        official = set(counties)

        for row in load_state_resources(state_name, csv_name):
            category = normalize_category(row.get("category", ""))
            if category not in ALL_CATEGORIES:
                continue

            if is_statewide_row(row):
                for county in counties:
                    coverage[state_name][county].statewide_by_category[category] += 1
                continue

            for county in served_counties(row):
                if county not in official:
                    continue
                coverage[state_name][county].local_by_category[category] += 1

    return coverage


def compute_scorecard(coverage: dict[str, dict[str, CountyCoverage]]) -> dict[str, object]:
    total_counties = sum(len(counties) for counties in coverage.values())
    tier_a_slots = total_counties * len(TIER_A)
    tier_a_filled = sum(
        1
        for counties in coverage.values()
        for data in counties.values()
        for cat in TIER_A
        if data.local_count(cat) > 0
    )
    tier_a_fill_rate = tier_a_filled / tier_a_slots if tier_a_slots else 0.0

    full_tier_a = sum(
        1 for counties in coverage.values() for data in counties.values() if data.tier_a_depth() == 8
    )
    weak_counties = sum(
        1
        for counties in coverage.values()
        for data in counties.values()
        if data.tier_a_depth() <= WEAK_COUNTY_DEPTH_MAX
    )

    by_state: dict[str, dict[str, float | int]] = {}
    for state_name, counties in coverage.items():
        state_slots = len(counties) * len(TIER_A)
        state_filled = sum(
            1
            for data in counties.values()
            for cat in TIER_A
            if data.local_count(cat) > 0
        )
        by_state[state_name] = {
            "counties": len(counties),
            "tier_a_fill_rate": round(state_filled / state_slots, 4) if state_slots else 0.0,
            "full_tier_a_counties": sum(1 for data in counties.values() if data.tier_a_depth() == 8),
            "weak_counties": sum(
                1 for data in counties.values() if data.tier_a_depth() <= WEAK_COUNTY_DEPTH_MAX
            ),
        }

    if tier_a_fill_rate < TIER_A_SLOT_FILL_FLOOR:
        status = "FAIL"
    elif tier_a_fill_rate < TIER_A_SLOT_FILL_TARGET_90D:
        status = "IN_PROGRESS"
    elif tier_a_fill_rate < TIER_A_SLOT_FILL_STRETCH:
        status = "ON_TRACK"
    else:
        status = "STRETCH_MET"

    return {
        "total_counties": total_counties,
        "tier_a_slots": tier_a_slots,
        "tier_a_filled": tier_a_filled,
        "tier_a_fill_rate": round(tier_a_fill_rate, 4),
        "tier_a_fill_pct": round(100.0 * tier_a_fill_rate, 1),
        "full_tier_a_counties": full_tier_a,
        "weak_counties": weak_counties,
        "targets": {
            "floor_pct": round(100.0 * TIER_A_SLOT_FILL_FLOOR, 1),
            "target_90d_pct": round(100.0 * TIER_A_SLOT_FILL_TARGET_90D, 1),
            "stretch_pct": round(100.0 * TIER_A_SLOT_FILL_STRETCH, 1),
            "full_tier_a_counties_90d": FULL_TIER_A_COUNTIES_TARGET_90D,
            "weak_counties_90d": WEAK_COUNTIES_TARGET_90D,
        },
        "by_state": by_state,
        "status": status,
    }


def category_gap_stats(
    coverage: dict[str, dict[str, CountyCoverage]],
) -> dict[str, dict[str, dict[str, int | float]]]:
    stats: dict[str, dict[str, dict[str, int | float]]] = {}
    for state_name, counties in coverage.items():
        stats[state_name] = {}
        total_counties = len(counties)
        for category in ALL_CATEGORIES:
            zero = sum(1 for data in counties.values() if data.local_count(category) == 0)
            stats[state_name][category] = {
                "zero_counties": zero,
                "zero_pct": round(100.0 * zero / total_counties, 1) if total_counties else 0.0,
                "counties_with_local": total_counties - zero,
            }
    return stats


def iter_county_category_gaps(
    coverage: dict[str, dict[str, CountyCoverage]],
    *,
    tier: str = "A",
) -> list[dict[str, str]]:
    categories = sorted(TIER_A if tier == "A" else TIER_B)
    priority_order = PHASE_1_CATEGORY_PRIORITY if tier == "A" else PHASE_2_CATEGORY_PRIORITY
    priority_rank = {cat: index for index, cat in enumerate(priority_order)}

    gaps: list[dict[str, str]] = []
    for state_name, counties in coverage.items():
        for county, data in counties.items():
            for category in categories:
                if data.local_count(category) > 0:
                    continue
                gaps.append(
                    {
                        "state": state_name,
                        "county": county,
                        "category": category,
                        "category_label": CATEGORY_LABELS[category],
                        "tier": tier,
                        "phase": "1" if tier == "A" else "2",
                        "strategy": "regional",
                        "sources": RESEARCH_SOURCES.get(category, ""),
                    }
                )

    gaps.sort(
        key=lambda row: (
            row["state"],
            priority_rank.get(row["category"], 99),
            row["county"],
        )
    )
    return gaps
