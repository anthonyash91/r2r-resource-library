"""Parse Wisconsin DHS Eligibility Management county pages for benefits office pins."""

from __future__ import annotations

import re
import time
import urllib.request
from html import unescape

WI_EM_BASE = "https://www.dhs.wisconsin.gov/em"
ACCESS_WI = "https://access.wi.gov"


def county_slug(county: str) -> str:
    return county.lower().replace(".", "").replace(" ", "-")


def fetch_county_page(slug: str) -> str:
    url = f"{WI_EM_BASE}/{slug}.htm"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_em_office(html: str, county: str) -> dict:
    text = unescape(re.sub(r"<[^>]+>", "\n", html))
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    address = ""
    city = ""
    phone = ""

    for line in lines:
        if re.search(rf"\b{re.escape(county)}\b", line, re.I) and re.search(r"\bWI\s+\d{5}", line):
            if len(line) > len(address):
                address = line
        if not phone:
            match = re.search(r"\b(888|877|855|800|608|414|715|920|262)-[\d-]{7,}\b", line)
            if match:
                phone = match.group(0)

    if address:
        city_match = re.search(r",\s*([^,]+),\s*WI\s+\d{5}", address)
        if city_match:
            city = city_match.group(1).strip()
        street = address.split(",")[0].strip()
        if street and street != address:
            address = street

    consortium_phones = re.findall(r"\b888[-\d]{10}\b", text)
    for candidate in consortium_phones:
        if candidate != phone:
            phone = phone or candidate
            break

    return {
        "county": county,
        "city": city,
        "address": address,
        "phone": phone or "1-800-362-3002",
        "website": ACCESS_WI,
        "source": f"{WI_EM_BASE}/{county_slug(county)}.htm",
    }


def fetch_all_county_offices(official: list[str], *, delay_s: float = 0.15) -> dict[str, dict]:
    by_county: dict[str, dict] = {}
    for county in official:
        slug = county_slug(county)
        try:
            html = fetch_county_page(slug)
            by_county[county] = parse_em_office(html, county)
        except Exception:
            by_county[county] = {
                "county": county,
                "city": "",
                "address": "",
                "phone": "1-800-362-3002",
                "website": ACCESS_WI,
                "source": ACCESS_WI,
            }
        time.sleep(delay_s)
    return by_county
