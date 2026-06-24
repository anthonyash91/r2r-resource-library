"""Parse West Virginia DoHS county field offices from the official locator page."""

from __future__ import annotations

import re
import urllib.request
from html import unescape

DOHS_LOCATOR = "https://dhhr.wv.gov/Pages/Field-Offices.aspx"
WV_PATH = "https://wvpath.wv.gov"
DOHS_HELP = "1-877-716-1212"


def fetch_field_offices_html() -> str:
    req = urllib.request.Request(DOHS_LOCATOR, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as response:
        return response.read().decode("utf-8", errors="replace")


def _parse_address_line(addr_line: str) -> tuple[str, str]:
    """Return (street_address, city) from 'Street, City, WV ZIP'."""
    cleaned = unescape(addr_line.replace("\xa0", " ").strip())
    match = re.match(r"^(.*?),\s*([^,]+),\s*WV\s*\d{5}", cleaned)
    if match:
        return match.group(1).strip(), match.group(2).strip()
    return cleaned, ""


def parse_dohs_offices(html: str, official: list[str]) -> dict[str, dict]:
    """Extract primary DoHS Family Assistance office per county from field offices HTML."""
    by_county: dict[str, dict] = {}
    official_set = set(official)

    for title, block in re.findall(
        r"<h3>([^<]*County DoHS Office)</h3>(.*?)(?=<h3>|<div class=\"groupheader|$)",
        html,
        re.S,
    ):
        if "Child Support" in title:
            continue
        county_match = re.match(r"([A-Za-z .'-]+)\s+County DoHS Office", title.strip())
        if not county_match:
            continue
        county = county_match.group(1).strip()
        if county not in official_set:
            continue

        addr_match = re.search(r"Physical Address:\s*</b>([^<]+)", block, re.I)
        phone_match = re.search(r"Phone:\s*</b>([^<]+)", block, re.I)
        if not addr_match:
            continue

        address, city = _parse_address_line(addr_match.group(1))
        phone = unescape(phone_match.group(1).replace("\xa0", " ").strip()) if phone_match else DOHS_HELP

        by_county[county] = {
            "county": county,
            "city": city,
            "address": address,
            "phone": phone,
            "website": WV_PATH,
            "source": DOHS_LOCATOR,
        }

    return by_county


def fetch_all_county_dohs(official: list[str]) -> dict[str, dict]:
    html = fetch_field_offices_html()
    return parse_dohs_offices(html, official)
