#!/usr/bin/env python3
"""Fetch county benefits office data and write scripts/data/*-offices.json.

Ohio (CDJFS): ODJFS county directory PDF (primary) + PCSAO scrape + ohio-cdjfs-verified.json merge.
Stub locator URLs only when PDF parse misses a county.

Tennessee (TDHS): Official Family Assistance office locator HTML (95 counties).

Kentucky (DCBS): Official CHFS local office search (120 counties) + kentucky-dcbs-verified.json merge.

Indiana (DFR): Official FSSA DFR county office PDF (92 counties).

Michigan (MDHHS): Official County Composite Directory HTML (83 counties).

Usage:
  python3 scripts/sync-county-benefits-offices.py [--state ohio|tennessee|kentucky|indiana|michigan|all]
"""

from __future__ import annotations

import argparse
import json
import re
import time
import urllib.request
from html import unescape
from pathlib import Path

from county_list_utils import (
    KY_DCBS_LOCATOR,
    kentucky_dcbs_locator_url,
    load_counties_from_ts,
    normalize_county_name,
    ohio_jfs_directory_url,
)

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(__file__).resolve().parent / "data"

TN_LOCATOR = (
    "https://www.tn.gov/humanservices/for-families/"
    "supplemental-nutrition-assistance-program-snap/office-locator-family-assistance.html"
)
PCSAO_DIRECTORY = "https://pcsao.org/membership/agency-directory/"
OHIO_VERIFIED = DATA_DIR / "ohio-cdjfs-verified.json"
OHIO_OUTPUT = DATA_DIR / "ohio-cdjfs-offices.json"
TN_OUTPUT = DATA_DIR / "tn-tdhs-offices.json"
KY_VERIFIED = DATA_DIR / "kentucky-dcbs-verified.json"
KY_OUTPUT = DATA_DIR / "kentucky-dcbs-offices.json"
IN_DFR_OUTPUT = DATA_DIR / "indiana-dfr-offices.json"
MI_OUTPUT = DATA_DIR / "michigan-mdhhs-offices.json"
MI_DIRECTORY = (
    "https://mdhhs.michigan.gov/CompositeDirPub/CountyCompositeDirectory.aspx"
)


def _fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read().decode("utf-8", errors="replace")


def scrape_pcsao_jfs() -> list[dict]:
    try:
        html = _fetch(PCSAO_DIRECTORY)
    except OSError as exc:
        print(f"Warning: PCSAO scrape failed ({exc}); using cached data only")
        return []
    pattern = re.compile(
        r'organization-unit notranslate">([^<]*Job[^<]*Family Services[^<]*)</span>.*?'
        r'street-address notranslate">([^<]*)</span>\s*<span class="locality">([^<]*)</span>.*?'
        r'class="value">([^<]*)</span>.*?'
        r'href="(https?://[^"]+)"',
        re.S,
    )
    offices: list[dict] = []
    for match in pattern.finditer(html):
        name = unescape(match.group(1).replace("&#038;", "&"))
        if "Consolidated" in name:
            counties = ["Defiance", "Paulding"]
        else:
            county_match = re.match(r"([A-Za-z .'-]+) County", name)
            counties = [county_match.group(1)] if county_match else []
        if not counties:
            continue
        for county in counties:
            offices.append(
                {
                    "county": county,
                    "city": unescape(match.group(3).strip()),
                    "address": unescape(match.group(2).strip()),
                    "phone": unescape(match.group(4).strip()),
                    "website": match.group(5),
                    "source": PCSAO_DIRECTORY,
                }
            )
    return offices


def load_verified_ohio_extras() -> list[dict]:
    if not OHIO_VERIFIED.exists():
        return []
    raw = json.loads(OHIO_VERIFIED.read_text(encoding="utf-8"))
    offices: list[dict] = []
    for entry in raw:
        for county in entry.get("counties", []):
            offices.append(
                {
                    "county": county,
                    "city": entry.get("city", ""),
                    "address": entry.get("address", ""),
                    "phone": entry.get("phone", ""),
                    "website": entry.get("website", ""),
                    "source": entry.get("source", entry.get("website", PCSAO_DIRECTORY)),
                }
            )
    return offices


def _merge_office(existing: dict | None, office: dict) -> dict:
    county = office["county"]
    merged = dict(existing or {"county": county})
    for field in ("city", "address", "phone", "website", "source"):
        if office.get(field):
            merged[field] = office[field]
    merged["county"] = county
    return merged


def sync_ohio() -> list[dict]:
    from ohio_jfs_directory import fetch_pdf_text, parse_cdjfs_from_pdf

    official = load_counties_from_ts("src/lib/ohio/counties.ts")
    by_county: dict[str, dict] = {}

    try:
        pdf_text = fetch_pdf_text()
        for county, office in parse_cdjfs_from_pdf(pdf_text, official).items():
            by_county[county] = office
    except OSError as exc:
        print(f"Warning: Ohio JFS PDF fetch/parse failed ({exc}); using PCSAO/verified only")

    for office in scrape_pcsao_jfs():
        county = office["county"]
        if county not in official:
            continue
        by_county[county] = _merge_office(by_county.get(county), office)

    for office in load_verified_ohio_extras():
        county = office["county"]
        if county not in official:
            continue
        by_county[county] = _merge_office(by_county.get(county), office)

    for county in official:
        if county in by_county:
            if not by_county[county].get("website"):
                by_county[county]["website"] = ohio_jfs_directory_url(county)
            continue
        locator = ohio_jfs_directory_url(county)
        by_county[county] = {
            "county": county,
            "city": "",
            "address": "",
            "phone": "",
            "website": locator,
            "source": PCSAO_DIRECTORY,
        }

    result = [by_county[c] for c in official]
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    OHIO_OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    verified = sum(1 for o in result if o.get("address"))
    print(f"Wrote {OHIO_OUTPUT.name}: {len(result)} counties ({verified} with address/phone from primary source)")
    return result


def _parse_tn_offices(html: str, official: list[str]) -> dict[str, dict]:
    """Parse TDHS locator sections by county header (anchor ids are sometimes wrong on tn.gov)."""
    by_county: dict[str, dict] = {}
    header_pattern = re.compile(
        r'(?:<p>)?(?:<b>)?<a name="[^"]*" id="[^"]*" class="anchor"></a>(?:</b>)?'
        r"(?:<b[^>]*>)?([A-Z][A-Z\s\.]+COUNTY)(?:</b>)?</p>",
        re.I,
    )
    headers = list(header_pattern.finditer(html))
    for i, match in enumerate(headers):
        header = unescape(match.group(1).strip())
        county_raw = re.sub(r"\s+COUNTY$", "", header, flags=re.I).strip()
        county_raw = re.sub(r"\s+", " ", county_raw).title()
        county_raw = (
            county_raw.replace("Dekalb", "DeKalb")
            .replace("Mcminn", "McMinn")
            .replace("Mcnairy", "McNairy")
        )
        county = normalize_county_name(county_raw, official)
        if not county:
            print(f"Warning: unrecognized TDHS header {header!r}")
            continue
        end = headers[i + 1].start() if i + 1 < len(headers) else match.start() + 4000
        chunk = html[match.end() : end]
        city_match = re.search(r"([^<\n]+),\s*TN\s*\d{5}", chunk)
        city = unescape(city_match.group(1).strip()) if city_match else ""
        phone_match = re.search(r'Phone:\s*<a[^>]*>([^<]+)</a>', chunk, re.I)
        phone = unescape(re.sub(r"<[^>]+>", "", phone_match.group(1)).strip()) if phone_match else ""
        address_parts: list[str] = []
        for para in re.findall(r"<p>(.*?)</p>", chunk, re.S | re.I):
            if para.strip().startswith("<a href"):
                continue
            lines = [
                unescape(re.sub(r"<[^>]+>", "", part)).strip()
                for part in re.split(r"<br\s*/>", para)
            ]
            for line in lines:
                line = re.sub(r"\*Updated as of[^*]+\*,?\s*", "", line).strip()
                if not line:
                    continue
                lower = line.lower()
                if lower.startswith("dist.") or lower.startswith("office hours") or lower.startswith("phone:"):
                    continue
                if lower.startswith("fax:") or "field management" in lower or line.startswith("- Services"):
                    break
                if re.search(r",\s*TN\s*\d{5}", line):
                    break
                if line.endswith(" Office") and not any(ch.isdigit() for ch in line):
                    continue
                address_parts.append(line)
            if address_parts:
                break
        address = ", ".join(dict.fromkeys(address_parts))
        address = re.sub(r",\s*,", ",", address)
        by_county[county] = {
            "county": county,
            "city": city,
            "address": address,
            "phone": phone,
            "source": TN_LOCATOR,
        }
    return by_county


def sync_tennessee() -> list[dict]:
    official = load_counties_from_ts("src/lib/tennessee/counties.ts")
    html = _fetch(TN_LOCATOR)
    by_county = _parse_tn_offices(html, official)

    missing = [c for c in official if c not in by_county]
    for county in missing:
        by_county[county] = {
            "county": county,
            "city": "",
            "address": "",
            "phone": "",
            "source": TN_LOCATOR,
        }

    result = [by_county[c] for c in official]
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    TN_OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with_address = sum(1 for o in result if o.get("address"))
    print(
        f"Wrote {TN_OUTPUT.name}: {len(result)} counties "
        f"({with_address} with address from locator)"
    )
    if missing:
        print(f"  Missing from locator HTML: {missing}")
    return result


def _parse_ky_family_support(html: str) -> dict | None:
    """Extract first Family Support office block from a county DCBS page."""
    start = html.lower().find("family support")
    if start < 0:
        return None
    chunk = html[start : start + 3500]
    address_match = re.search(r'<div id="address">(.*?)</div>', chunk, re.S | re.I)
    phone_match = re.search(r'<div id="phone">(.*?)</div>', chunk, re.S | re.I)
    if not address_match:
        return None
    addr_html = address_match.group(1)
    phone = unescape(re.sub(r"<[^>]+>", "", phone_match.group(1)).strip()) if phone_match else ""
    parts = [
        unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", part))).strip()
        for part in re.split(r"<br\s*/?>", addr_html)
        if part.strip()
    ]
    parts = [part for part in parts if part and part not in ("&nbsp;", "\xa0")]
    city = ""
    for part in parts:
        city_match = re.search(r"^([^,]+),\s*KY\s*\d", part)
        if city_match:
            city = city_match.group(1).strip()
            break
    street_parts = [part.rstrip(",") for part in parts if not re.search(r",\s*KY\s*\d", part)]
    return {
        "city": city,
        "address": ", ".join(street_parts),
        "phone": phone,
    }


def _load_ky_county_options(html: str) -> list[tuple[str, str]]:
    options: list[tuple[str, str]] = []
    for select_match in re.finditer(r'<select[^>]*name="county"[^>]*>(.*?)</select>', html, re.S | re.I):
        for value, label in re.findall(r'value="([^"]*)"[^>]*>([^<]*)', select_match.group(1)):
            county_match = re.search(r"county=(\d+)", value)
            if not county_match:
                continue
            options.append((county_match.group(1), label.strip()))
    return options


def load_verified_kentucky_extras() -> list[dict]:
    if not KY_VERIFIED.exists():
        return []
    raw = json.loads(KY_VERIFIED.read_text(encoding="utf-8"))
    offices: list[dict] = []
    for entry in raw:
        for county in entry.get("counties", []):
            offices.append(
                {
                    "county": county,
                    "city": entry.get("city", ""),
                    "address": entry.get("address", ""),
                    "phone": entry.get("phone", ""),
                    "source": entry.get("source", KY_DCBS_LOCATOR),
                }
            )
    return offices


def sync_kentucky() -> list[dict]:
    official = load_counties_from_ts("src/lib/kentucky/counties.ts")
    index_html = _fetch(KY_DCBS_LOCATOR)
    county_options = _load_ky_county_options(index_html)
    if not county_options:
        raise SystemExit("No Kentucky county options found on DCBS locator page")

    by_county: dict[str, dict] = {}
    for county_id, label in county_options:
        county = normalize_county_name(label.title(), official)
        if not county:
            print(f"Warning: unrecognized DCBS county label {label!r}")
            continue
        url = kentucky_dcbs_locator_url(county_id)
        try:
            page_html = _fetch(url)
        except OSError as exc:
            print(f"Warning: failed to fetch {county} ({exc})")
            by_county[county] = {
                "county": county,
                "city": "",
                "address": "",
                "phone": "",
                "source": url,
            }
            continue
        parsed = _parse_ky_family_support(page_html)
        by_county[county] = {
            "county": county,
            "city": parsed.get("city", "") if parsed else "",
            "address": parsed.get("address", "") if parsed else "",
            "phone": parsed.get("phone", "") if parsed else "",
            "source": url,
        }
        time.sleep(0.05)

    for office in load_verified_kentucky_extras():
        county = office["county"]
        if county not in official:
            continue
        current = by_county.get(county, {"county": county, "source": office.get("source", KY_DCBS_LOCATOR)})
        for field in ("city", "address", "phone", "source"):
            if office.get(field):
                current[field] = office[field]
        by_county[county] = current

    missing = [county for county in official if county not in by_county]
    for county in missing:
        by_county[county] = {
            "county": county,
            "city": "",
            "address": "",
            "phone": "",
            "source": KY_DCBS_LOCATOR,
        }

    result = [by_county[county] for county in official]
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    KY_OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with_address = sum(1 for office in result if office.get("address"))
    print(
        f"Wrote {KY_OUTPUT.name}: {len(result)} counties "
        f"({with_address} with address from CHFS locator)"
    )
    if missing:
        print(f"  Missing from locator scrape: {missing}")
    return result


def sync_indiana() -> list[dict]:
    from indiana_dfr_directory import fetch_pdf_text, parse_dfr_from_pdf

    official = load_counties_from_ts("src/lib/indiana/counties.ts")
    text = fetch_pdf_text()
    by_county = parse_dfr_from_pdf(text, official)
    missing = [county for county in official if county not in by_county]
    for county in missing:
        by_county[county] = {
            "county": county,
            "city": "",
            "address": "",
            "phone": "800-403-0864",
            "website": "https://www.in.gov/fssa/dfr/ebt-hoosier-works-card/find-my-local-dfr-office/",
            "source": "https://www.in.gov/fssa/dfr/ebt-hoosier-works-card/find-my-local-dfr-office/",
        }
    result = [by_county[county] for county in official]
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    IN_DFR_OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with_address = sum(1 for office in result if office.get("address"))
    print(
        f"Wrote {IN_DFR_OUTPUT.name}: {len(result)} counties "
        f"({with_address} with address from FSSA PDF)"
    )
    if missing:
        print(f"  Missing from PDF parse: {missing}")
    return result


def sync_michigan() -> list[dict]:
    from michigan_mdhhs_directory import fetch_directory_html, parse_mdhhs_offices

    official = load_counties_from_ts("src/lib/michigan/counties.ts")
    html = fetch_directory_html()
    by_county = parse_mdhhs_offices(html, official)
    missing = [county for county in official if county not in by_county]
    for county in missing:
        by_county[county] = {
            "county": county,
            "city": "",
            "address": "",
            "phone": "1-844-464-3447",
            "website": "https://newmibridges.michigan.gov/s/isd-landing-page?language=en_US",
            "source": MI_DIRECTORY,
        }
    result = [by_county[county] for county in official]
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    MI_OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with_address = sum(1 for office in result if office.get("address"))
    print(
        f"Wrote {MI_OUTPUT.name}: {len(result)} counties "
        f"({with_address} with address from MDHHS directory)"
    )
    if missing:
        print(f"  Missing from directory scrape: {missing}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync county benefits office JSON data")
    parser.add_argument(
        "--state",
        choices=("ohio", "tennessee", "kentucky", "indiana", "michigan", "all"),
        default="all",
        help="Which state to sync (default: all)",
    )
    args = parser.parse_args()
    if args.state in ("ohio", "all"):
        sync_ohio()
    if args.state in ("tennessee", "all"):
        sync_tennessee()
    if args.state in ("kentucky", "all"):
        sync_kentucky()
    if args.state in ("indiana", "all"):
        sync_indiana()
    if args.state in ("michigan", "all"):
        sync_michigan()


if __name__ == "__main__":
    main()
