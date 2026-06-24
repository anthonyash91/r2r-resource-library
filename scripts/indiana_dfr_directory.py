"""Parse Indiana DFR county office addresses from the official FSSA PDF."""

from __future__ import annotations

import io
import re
import urllib.request

from county_list_utils import load_counties_from_ts, normalize_county_name

PDF_URL = "https://www.in.gov/fssa/dfr/files/DFR_Map_and_County_List.pdf"
COUNTY_HEADER = re.compile(r"^([A-Z][A-Z \xa0.]+) COUNTY\s*$", re.M)
ADDRESS_LINE = re.compile(r"^(.+,\s*IN\s*\d{5}(?:-\d{4})?)\s*$", re.I)


def fetch_pdf_text() -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise SystemExit(
            "pypdf is required for Indiana DFR PDF sync: pip3 install -r scripts/requirements-data.txt"
        ) from exc

    request = urllib.request.Request(PDF_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        reader = PdfReader(io.BytesIO(response.read()))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def _normalize_header(label: str, official: list[str]) -> str | None:
    cleaned = re.sub(r"\s+", " ", label.strip()).title()
    cleaned = cleaned.replace("La Porte", "LaPorte").replace("De Kalb", "DeKalb")
    if cleaned.lower().replace(".", "") == "st joseph":
        cleaned = "St. Joseph"
    if cleaned == "St. Joseph":
        cleaned = "St. Joseph"
    return normalize_county_name(cleaned, official)


def parse_dfr_from_pdf(text: str, official: list[str]) -> dict[str, dict]:
    lines = [line.strip() for line in text.splitlines()]
    by_county: dict[str, dict] = {}
    index = 0
    while index < len(lines):
        match = COUNTY_HEADER.match(lines[index])
        if not match:
            index += 1
            continue
        county = _normalize_header(match.group(1), official)
        index += 1
        block: list[str] = []
        while index < len(lines) and not COUNTY_HEADER.match(lines[index]):
            if lines[index]:
                block.append(lines[index])
            index += 1
        if not county or county not in official:
            continue
        address = ""
        city = ""
        street_parts: list[str] = []
        for line in block:
            if line.lower().startswith("office hours"):
                break
            address_match = ADDRESS_LINE.match(line)
            if address_match:
                address = ", ".join(street_parts + [address_match.group(1)]) if street_parts else address_match.group(1)
                city_match = re.search(r",\s*([^,]+),\s*IN\s*\d", address)
                if city_match:
                    city = city_match.group(1).strip()
                break
            if not line.lower().endswith("office") and "office" not in line.lower()[:12]:
                street_parts.append(line.rstrip(","))
        by_county[county] = {
            "county": county,
            "city": city,
            "address": address,
            "phone": "800-403-0864",
            "website": "https://www.in.gov/fssa/dfr/ebt-hoosier-works-card/find-my-local-dfr-office/",
            "source": PDF_URL,
        }
    return by_county
