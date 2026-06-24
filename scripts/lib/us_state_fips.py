"""US state FIPS codes and deployed-state discovery for map generation."""

from __future__ import annotations

import re
from pathlib import Path

# Census / plotly geojson county FIPS prefix → full state name (50 states + DC).
US_STATE_FIPS: dict[str, str] = {
    "01": "Alabama",
    "02": "Alaska",
    "04": "Arizona",
    "05": "Arkansas",
    "06": "California",
    "08": "Colorado",
    "09": "Connecticut",
    "10": "Delaware",
    "11": "District of Columbia",
    "12": "Florida",
    "13": "Georgia",
    "15": "Hawaii",
    "16": "Idaho",
    "17": "Illinois",
    "18": "Indiana",
    "19": "Iowa",
    "20": "Kansas",
    "21": "Kentucky",
    "22": "Louisiana",
    "23": "Maine",
    "24": "Maryland",
    "25": "Massachusetts",
    "26": "Michigan",
    "27": "Minnesota",
    "28": "Mississippi",
    "29": "Missouri",
    "30": "Montana",
    "31": "Nebraska",
    "32": "Nevada",
    "33": "New Hampshire",
    "34": "New Jersey",
    "35": "New Mexico",
    "36": "New York",
    "37": "North Carolina",
    "38": "North Dakota",
    "39": "Ohio",
    "40": "Oklahoma",
    "41": "Oregon",
    "42": "Pennsylvania",
    "44": "Rhode Island",
    "45": "South Carolina",
    "46": "South Dakota",
    "47": "Tennessee",
    "48": "Texas",
    "49": "Utah",
    "50": "Vermont",
    "51": "Virginia",
    "53": "Washington",
    "54": "West Virginia",
    "55": "Wisconsin",
    "56": "Wyoming",
}

US_STATE_NAME_TO_FIPS: dict[str, str] = {name: code for code, name in US_STATE_FIPS.items()}

REGISTRY_MARKER = "ONBOARDING_STATE_REGISTRY"
REGISTRY_NAME_PATTERN = re.compile(r'name:\s*"([^"]+)"')


def load_deployed_state_names(root: Path) -> list[str]:
    """Read deployed state names from src/lib/states/registry.ts."""
    registry_path = root / "src" / "lib" / "states" / "registry.ts"
    text = registry_path.read_text(encoding="utf-8")
    marker_index = text.find(REGISTRY_MARKER)
    if marker_index < 0:
        raise RuntimeError(f"{REGISTRY_MARKER} not found in {registry_path}")

    bracket_start = text.find("[", marker_index)
    if bracket_start < 0:
        raise RuntimeError(f"Could not find registry array in {registry_path}")

    depth = 0
    for index in range(bracket_start, len(text)):
        char = text[index]
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                registry_block = text[bracket_start : index + 1]
                break
    else:
        raise RuntimeError(f"Unclosed registry array in {registry_path}")

    names = REGISTRY_NAME_PATTERN.findall(registry_block)
    if not names:
        raise RuntimeError(f"No state names found in {registry_path}")
    return names


def load_deployed_state_fips(root: Path) -> dict[str, str]:
    """Return FIPS prefix → state name for every deployed onboarding state."""
    fips_by_code: dict[str, str] = {}
    missing: list[str] = []

    for name in load_deployed_state_names(root):
        code = US_STATE_NAME_TO_FIPS.get(name)
        if not code:
            missing.append(name)
            continue
        fips_by_code[code] = name

    if missing:
        raise RuntimeError(
            "No FIPS code for deployed state(s): "
            + ", ".join(missing)
            + ". Add to scripts/lib/us_state_fips.py if needed."
        )

    return fips_by_code
