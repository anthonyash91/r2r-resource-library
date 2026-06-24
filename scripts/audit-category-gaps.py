#!/usr/bin/env python3
"""Audit per-county category coverage and write a content roadmap.

Counts local + regional resources only (excludes statewide rows), matching
county-scoped filter facets in the app.

Usage:
  python3 scripts/audit-category-gaps.py
  python3 scripts/audit-category-gaps.py --json data/category-gap-audit.json
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
DOCS_PATH = ROOT / "docs" / "content-roadmap-category-gaps.md"

STATES = [
    ("Kentucky", "kentucky", "src/lib/kentucky/counties.ts", "kentucky-resources.csv"),
    ("Ohio", "ohio", "src/lib/ohio/counties.ts", "ohio-resources.csv"),
    ("Indiana", "indiana", "src/lib/indiana/counties.ts", "indiana-resources.csv"),
    ("Tennessee", "tennessee", "src/lib/tennessee/counties.ts", "tennessee-resources.csv"),
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

# Minimum local/regional rows we want per county (content targets, not hard gates).
LOCAL_MINIMUMS: dict[str, int] = {
    "housing": 1,
    "healthcare": 1,
    "employment": 1,
    "legal-aid": 1,
    "financial-assistance": 1,
    "substance-use-treatment": 1,
    "probation-parole": 1,
    "food-nutrition": 1,
    "education": 1,
    "veterans": 1,
    "basic-needs": 1,
    "id-documentation": 1,
    "transportation": 1,
    "peer-support": 1,
    "family-children": 1,
    "reentry-organizations": 1,
    "state-agency": 1,
}


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

    def missing_local(self) -> list[str]:
        return [cat for cat in ALL_CATEGORIES if self.local_count(cat) == 0]

    def missing_tier_a(self) -> list[str]:
        return [cat for cat in sorted(TIER_A) if self.local_count(cat) == 0]

    def missing_tier_b(self) -> list[str]:
        return [cat for cat in sorted(TIER_B) if self.local_count(cat) == 0]

    def below_minimum(self) -> list[str]:
        return [
            cat
            for cat, minimum in LOCAL_MINIMUMS.items()
            if self.local_count(cat) < minimum
        ]

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


def worst_counties(
    coverage: dict[str, dict[str, CountyCoverage]], limit: int = 25
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for state_name, counties in coverage.items():
        for county, data in counties.items():
            rows.append(
                {
                    "state": state_name,
                    "county": county,
                    "tier_a_depth": data.tier_a_depth(),
                    "missing_tier_a": data.missing_tier_a(),
                    "missing_tier_b": data.missing_tier_b(),
                    "total_local": data.total_local(),
                }
            )
    rows.sort(key=lambda item: (item["tier_a_depth"], item["total_local"], item["county"]))
    return rows[:limit]


def roadmap_phases(
    gap_stats: dict[str, dict[str, dict[str, int | float]]],
) -> list[dict[str, object]]:
    """Suggest research phases by highest zero-county % within each tier."""
    phases: list[dict[str, object]] = []

    def top_gaps(state: str, categories: list[str], n: int = 4) -> list[tuple[str, float]]:
        ranked = sorted(
            ((cat, float(gap_stats[state][cat]["zero_pct"])) for cat in categories),
            key=lambda item: (-item[1], item[0]),
        )
        return [(cat, pct) for cat, pct in ranked if pct > 0][:n]

    for state_name, _slug, _path, _csv in STATES:
        tier_a_gaps = top_gaps(state_name, sorted(TIER_A))
        tier_b_gaps = top_gaps(state_name, sorted(TIER_B))
        phases.append(
            {
                "state": state_name,
                "phase_1_tier_a_gaps": tier_a_gaps,
                "phase_2_tier_b_gaps": tier_b_gaps,
            }
        )
    return phases


def render_markdown(
    coverage: dict[str, dict[str, CountyCoverage]],
    gap_stats: dict[str, dict[str, dict[str, int | float]]],
    worst: list[dict[str, object]],
    phases: list[dict[str, object]],
) -> str:
    total_counties = sum(len(counties) for counties in coverage.values())
    tier_a_zero_slots = sum(
        1
        for counties in coverage.values()
        for data in counties.values()
        for cat in TIER_A
        if data.local_count(cat) == 0
    )
    tier_a_slots = total_counties * len(TIER_A)
    tier_a_fill_pct = 100.0 * (tier_a_slots - tier_a_zero_slots) / tier_a_slots if tier_a_slots else 0

    lines: list[str] = [
        "# Content roadmap: per-county category gaps",
        "",
        f"Generated: {date.today().isoformat()}",
        "",
        "This audit measures **local + regional** resources per county (statewide-only rows",
        "are tracked separately and do not count toward county filter facets). Use it to",
        "priorize research where users would see empty or thin category options.",
        "",
        "## Executive summary",
        "",
        f"- **Counties audited:** {total_counties} across Kentucky, Ohio, Indiana, and Tennessee",
        f"- **Tier A local coverage:** {tier_a_fill_pct:.1f}% of county×category slots filled "
        f"({tier_a_slots - tier_a_zero_slots:,} / {tier_a_slots:,})",
        "- **Financial assistance** looks large in global totals because many counties have "
        "benefits enrollment touchpoints; at county scope it is usually **not** the dominant category.",
        "- **Biggest discoverability risk:** thin categories (transportation, family & children, "
        "peer support, ID & documentation) with high zero-county rates — users filtering by county "
        "may see no local options even when statewide help exists.",
        "",
        "## How to read this report",
        "",
        "| Term | Meaning |",
        "| --- | --- |",
        "| **Local/regional** | Resource serves the county and is not statewide-only |",
        "| **Tier A** | Housing, healthcare, employment, legal aid, financial assistance, "
        "substance use, probation/parole, food & nutrition |",
        "| **Tier B** | Education, veterans, basic needs, ID/docs, transportation, peer support, "
        "family & children, reentry organizations |",
        "| **Zero counties** | Counties with no local/regional resource in that category |",
        "",
        "## State × category gap matrix (zero counties)",
        "",
        "Sorted by zero-county % within each state (highest gap first).",
        "",
    ]

    for state_name, _slug, _path, _csv in STATES:
        county_count = len(coverage[state_name])
        lines.append(f"### {state_name} ({county_count} counties)")
        lines.append("")
        lines.append("| Category | Zero counties | % counties empty | Has local |")
        lines.append("| --- | ---: | ---: | ---: |")
        ranked = sorted(
            ALL_CATEGORIES,
            key=lambda cat: (-float(gap_stats[state_name][cat]["zero_pct"]), cat),
        )
        for category in ranked:
            stat = gap_stats[state_name][category]
            zero = int(stat["zero_counties"])
            if zero == 0:
                continue
            label = CATEGORY_LABELS[category]
            lines.append(
                f"| {label} | {zero} | {stat['zero_pct']}% | {stat['counties_with_local']} |"
            )
        lines.append("")

    lines.extend(
        [
            "## Cross-state priorities (where to research next)",
            "",
            "Categories with the highest average zero-county rate across all four states:",
            "",
        ]
    )

    avg_zero: list[tuple[str, float, list[tuple[str, float]]]] = []
    for category in ALL_CATEGORIES:
        pcts = [float(gap_stats[state][category]["zero_pct"]) for state, *_ in STATES]
        avg = sum(pcts) / len(pcts)
        by_state = [(state, float(gap_stats[state][category]["zero_pct"])) for state, *_ in STATES]
        avg_zero.append((category, avg, by_state))
    avg_zero.sort(key=lambda item: (-item[1], item[0]))

    lines.append("| Priority | Category | Avg % counties empty | Worst state |")
    lines.append("| ---: | --- | ---: | --- |")
    for index, (category, avg, by_state) in enumerate(avg_zero[:12], start=1):
        worst_state, worst_pct = max(by_state, key=lambda item: item[1])
        if avg <= 0:
            break
        lines.append(
            f"| {index} | {CATEGORY_LABELS[category]} | {avg:.1f}% | "
            f"{worst_state} ({worst_pct:.0f}%) |"
        )
    lines.append("")

    lines.extend(["## Phased content roadmap", ""])
    for phase in phases:
        state = str(phase["state"])
        lines.append(f"### {state}")
        lines.append("")
        lines.append("**Phase 1 — Tier A gaps (fill first):**")
        tier_a = phase["phase_1_tier_a_gaps"]
        if tier_a:
            for cat, pct in tier_a:
                lines.append(
                    f"- {CATEGORY_LABELS[cat]} — empty in **{pct:.0f}%** of counties; "
                    f"add county/regional providers or verify `served_counties` on existing rows."
                )
        else:
            lines.append("- No Tier A categories with universal gaps.")
        lines.append("")
        lines.append("**Phase 2 — Tier B depth:**")
        tier_b = phase["phase_2_tier_b_gaps"]
        if tier_b:
            for cat, pct in tier_b:
                lines.append(
                    f"- {CATEGORY_LABELS[cat]} — empty in **{pct:.0f}%** of counties."
                )
        else:
            lines.append("- Tier B reasonably distributed.")
        lines.append("")
        lines.append("**Phase 3 — Quality & deduplication:**")
        lines.append(
            "- Normalize `category` column to slugs only (`financial-assistance`, not display names)."
        )
        lines.append(
            "- Review financial-assistance rows: keep distinct county enrollment sites; "
            "merge true duplicates."
        )
        lines.append(
            "- Ensure statewide benefits portals stay `coverage=statewide` so they appear in "
            "the statewide results block, not as false local density."
        )
        lines.append("")
        lines.append("**Phase 4 — Featured & pathways curation:**")
        lines.append(
            "- Feature 1–2 resources per thin category per state so homepage/pathways surface "
            "non-financial needs."
        )
        lines.append(
            "- Use onboarding priority categories to steer recommendations — already balanced in app."
        )
        lines.append("")

    lines.extend(
        [
            "## Counties needing the most attention",
            "",
            "Lowest Tier A depth (fewest core categories with any local resource):",
            "",
            "| State | County | Tier A categories present | Missing Tier A | Local rows |",
            "| --- | --- | ---: | --- | ---: |",
        ]
    )
    for row in worst:
        missing = ", ".join(CATEGORY_LABELS[c] for c in row["missing_tier_a"]) or "—"
        lines.append(
            f"| {row['state']} | {row['county']} | {row['tier_a_depth']}/8 | "
            f"{missing} | {row['total_local']} |"
        )
    lines.append("")

    lines.extend(
        [
            "## Research playbooks by category",
            "",
            "| Category | What to add per gap county | Likely sources |",
            "| --- | --- | --- |",
            "| Housing | Transitional/recovery housing, shelter, reentry housing lists | CoC, HUD, DOC reentry centers |",
            "| Healthcare | FQHC, community mental health, MAT | HRSA, state MH directories |",
            "| Employment | LWDB/Workforce, fair-chance staffing, job training | CareerOneStop, state workforce |",
            "| Legal aid | Expungement clinics, civil legal aid office serving county | LSC, state legal aid maps |",
            "| Financial assistance | County DFR/DCBS/JFS office (if missing), utility assistance | State benefits office directories |",
            "| Substance use | Outpatient/MAT, recovery community orgs | SAMHSA, state SUD directories |",
            "| Probation & parole | Field office, community supervision contact | DOC / DRC regional maps |",
            "| Food & nutrition | Food bank partner, SNAP outreach site | Feeding America, state SNAP |",
            "| Transportation | Transit voucher programs, reentry ride programs | local transit authority |",
            "| ID & documentation | Vital records, ID voucher programs | circuit court clerk, legal aid |",
            "| Peer support | Certified peer orgs, recovery community centers | state peer certification lists |",
            "| Family & children | Visitation support, kinship, family reentry | United Way 211, CPS community partners |",
            "",
            "## Regenerating this report",
            "",
            "```bash",
            "python3 scripts/audit-category-gaps.py",
            "```",
            "",
        ]
    )

    return "\n".join(lines)


def build_json_payload(
    coverage: dict[str, dict[str, CountyCoverage]],
    gap_stats: dict[str, dict[str, dict[str, int | float]]],
    worst: list[dict[str, object]],
    phases: list[dict[str, object]],
) -> dict[str, object]:
    counties_payload: list[dict[str, object]] = []
    for state_name, counties in coverage.items():
        for county, data in counties.items():
            counties_payload.append(
                {
                    "state": state_name,
                    "county": county,
                    "tier_a_depth": data.tier_a_depth(),
                    "total_local": data.total_local(),
                    "missing_local": data.missing_local(),
                    "missing_tier_a": data.missing_tier_a(),
                    "missing_tier_b": data.missing_tier_b(),
                    "local_by_category": dict(data.local_by_category),
                    "statewide_by_category": dict(data.statewide_by_category),
                }
            )

    return {
        "generated": date.today().isoformat(),
        "gap_stats": gap_stats,
        "worst_counties": worst,
        "roadmap_phases": phases,
        "counties": counties_payload,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit per-county category gaps")
    parser.add_argument(
        "--json",
        type=Path,
        default=ROOT / "data" / "category-gap-audit.json",
        help="Write machine-readable audit JSON",
    )
    parser.add_argument(
        "--markdown",
        type=Path,
        default=DOCS_PATH,
        help="Write markdown roadmap",
    )
    args = parser.parse_args()

    coverage = build_coverage()
    gap_stats = category_gap_stats(coverage)
    worst = worst_counties(coverage)
    phases = roadmap_phases(gap_stats)

    markdown = render_markdown(coverage, gap_stats, worst, phases)
    args.markdown.parent.mkdir(parents=True, exist_ok=True)
    args.markdown.write_text(markdown, encoding="utf-8")

    payload = build_json_payload(coverage, gap_stats, worst, phases)
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    total_counties = sum(len(c) for c in coverage.values())
    print(f"Wrote {args.markdown}")
    print(f"Wrote {args.json}")
    print(f"Audited {total_counties} counties")


if __name__ == "__main__":
    main()
