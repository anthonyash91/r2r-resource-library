"""Parse MDHHS County Composite Directory for local benefits office pins."""

from __future__ import annotations

import re
import urllib.request
from html import unescape

MDHHS_DIRECTORY = (
    "https://mdhhs.michigan.gov/CompositeDirPub/CountyCompositeDirectory.aspx"
)
MI_BRIDGES = "https://newmibridges.michigan.gov/s/isd-landing-page?language=en_US"


def fetch_directory_html() -> str:
    req = urllib.request.Request(MDHHS_DIRECTORY, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_city_address(raw: str) -> tuple[str, str]:
    raw = re.sub(r"\s+", " ", raw).strip()
    match = re.search(r",\s*MI\s*(\d{5})?", raw)
    if not match:
        return raw, ""
    before = raw[: match.start()].strip().rstrip(",")
    if "," in before:
        parts = [part.strip() for part in before.split(",")]
        return ", ".join(parts[:-1]), parts[-1]
    tokens = before.rsplit(" ", 2)
    if len(tokens) >= 2 and tokens[-1][0].isupper():
        return " ".join(tokens[:-1]).strip(), tokens[-1].strip()
    return before, before


def parse_mdhhs_offices(html: str, official: list[str]) -> dict[str, dict]:
    from county_list_utils import normalize_county_name

    by_county: dict[str, dict] = {}
    for row in re.findall(r"<tr[^>]*>(.*?)</tr>", html, re.S | re.I):
        cells = re.findall(r"<td[^>]*>(.*?)</td>", row, re.S | re.I)
        if len(cells) < 5:
            continue
        county_raw = unescape(re.sub(r"<[^>]+>", " ", cells[0])).strip()
        county_match = re.match(r"\d+\s+(.+)", county_raw)
        if not county_match:
            continue
        county = normalize_county_name(county_match.group(1).strip(), official)
        if not county:
            continue
        address_raw = unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", cells[3]))).strip()
        phone = unescape(re.sub(r"<[^>]+>", " ", cells[4])).strip()
        phone = re.sub(r"\s+", " ", phone).strip()
        street, city = parse_city_address(address_raw)
        entry = {
            "county": county,
            "city": city,
            "address": street,
            "phone": phone,
            "website": MI_BRIDGES,
            "source": MDHHS_DIRECTORY,
        }
        if county not in by_county or entry.get("address"):
            by_county[county] = entry
    return by_county
