"""Parse IDHS Family Community Resource Center (FCRC) offices by county."""

from __future__ import annotations

import re
import urllib.request
from html import unescape

IDHS_LOCATOR = "https://www.dhs.state.il.us/page.aspx"
ABE_PORTAL = "https://abe.illinois.gov"
IDHS_HELP = "1-800-843-6154"


def idhs_county_param(county: str) -> str:
    """Map canonical county names to IDHS locator dropdown values."""
    if county == "St. Clair":
        return "St Clair"
    return county


def fetch_county_fcrc_html(county: str) -> str:
    param = idhs_county_param(county)
    query = f"county={param.replace(' ', '%20')}&module=12&OfficeType=5"
    url = f"{IDHS_LOCATOR}?{query}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=90) as response:
        return response.read().decode("utf-8", errors="replace")


def parse_office_list_html(html: str) -> list[dict]:
    """Parse all FCRC entries from an IDHS office locator results page."""
    offices: list[dict] = []
    for block in re.findall(r"<li>(.*?)</li>", html, re.S | re.I):
        if "Family Community Resource Center" not in block and "OfficeAddress" not in block:
            continue
        title_match = re.search(r"<h3[^>]*>(.*?)</h3>", block, re.S | re.I)
        if not title_match:
            continue
        title = unescape(re.sub(r"<[^>]+>", " ", title_match.group(1))).strip()
        if "Family Community Resource Center" not in title:
            continue

        addr_match = re.search(
            r"class=\"OfficeAddress\"[^>]*>(.*?)</p>", block, re.S | re.I
        )
        address = ""
        city = ""
        if addr_match:
            addr_html = addr_match.group(1)
            addr_lines = [
                unescape(re.sub(r"<[^>]+>", " ", line)).strip()
                for line in re.split(r"<br\s*/?>", addr_html, flags=re.I)
            ]
            addr_lines = [line for line in addr_lines if line]
            if addr_lines:
                if len(addr_lines) >= 2:
                    address = addr_lines[0]
                    city_line = addr_lines[-1]
                else:
                    city_line = addr_lines[0]
                    address = ""
                city_match = re.match(r"([^,]+),\s*IL\s*\d{5}", city_line)
                if city_match:
                    city = city_match.group(1).strip()
                    if not address and len(addr_lines) == 1:
                        street_match = re.match(r"^(.*?),\s*([^,]+),\s*IL", city_line)
                        if street_match:
                            address = street_match.group(1).strip()
                            city = street_match.group(2).strip()

        phone = ""
        tel_match = re.search(r"href=['\"]tel:[^'\"]*['\"][^>]*>([^<]+)</a>", block, re.I)
        if tel_match:
            phone = unescape(tel_match.group(1)).strip()
        if not phone:
            phone_match = re.search(r"Phone:\s*([^<\n]+)", block, re.I)
            if phone_match:
                phone = unescape(re.sub(r"<[^>]+>", "", phone_match.group(1))).strip()

        county_match = re.search(
            r"Family Community Resource Center in\s+(.+?)(?:\s+County|\s+-)", title, re.I
        )
        office_county = ""
        if county_match:
            office_county = county_match.group(1).strip()
            if office_county.lower().endswith(" county"):
                office_county = office_county[:-7].strip()

        offices.append(
            {
                "title": title,
                "office_county_label": office_county,
                "address": address,
                "city": city,
                "phone": phone,
            }
        )
    return offices


def parse_county_fcrc(county: str, html: str) -> dict | None:
    offices = parse_office_list_html(html)
    if not offices:
        return None

    # Prefer an office whose title matches the requested county.
    chosen = None
    for office in offices:
        label = office.get("office_county_label", "").lower()
        if label == county.lower() or label.replace(".", "") == county.lower().replace(".", ""):
            chosen = office
            break
    if not chosen:
        chosen = offices[0]

    return {
        "county": county,
        "city": chosen.get("city") or "",
        "address": chosen.get("address") or "",
        "phone": chosen.get("phone") or IDHS_HELP,
        "website": ABE_PORTAL,
        "source": f"{IDHS_LOCATOR}?county={idhs_county_param(county).replace(' ', '%20')}&module=12&OfficeType=5",
        "office_title": chosen.get("title", ""),
    }


def fetch_all_county_fcrcs(official: list[str]) -> dict[str, dict]:
    by_county: dict[str, dict] = {}
    for county in official:
        html = fetch_county_fcrc_html(county)
        office = parse_county_fcrc(county, html)
        if office:
            by_county[county] = office
    return by_county
