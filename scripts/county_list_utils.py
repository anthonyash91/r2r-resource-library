"""Load canonical county names from src/lib/{state}/counties.ts."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_counties_from_ts(relative_path: str) -> list[str]:
    path = ROOT / relative_path
    counties: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r'\s+"([A-Za-z][A-Za-z .\'-]+)",\s*$', line)
        if match:
            counties.append(match.group(1))
    if not counties:
        raise SystemExit(f"No counties parsed from {path}")
    return counties


def normalize_county_name(raw: str, official: list[str]) -> str | None:
    """Map scraped county label to canonical name from official list."""
    cleaned = raw.strip()
    if cleaned in official:
        return cleaned
    key = re.sub(r"[^a-z]", "", cleaned.lower())
    for name in official:
        if re.sub(r"[^a-z]", "", name.lower()) == key:
            return name
    return None


def ohio_jfs_directory_url(county: str) -> str:
    slug = county.lower().replace(" ", "-")
    return f"https://jfs.ohio.gov/about/local-agencies-directory/cdjfs-{slug}"


KY_DCBS_LOCATOR = "https://prd.webapps.chfs.ky.gov/Office_Phone/index.aspx"


def kentucky_dcbs_locator_url(county_id: str) -> str:
    return f"{KY_DCBS_LOCATOR}?county={county_id}"
