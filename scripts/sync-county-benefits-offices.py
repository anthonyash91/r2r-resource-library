#!/usr/bin/env python3
"""Fetch county benefits office data and write scripts/data/*-offices.json.

Ohio (CDJFS): ODJFS county directory PDF (primary) + PCSAO scrape + ohio-cdjfs-verified.json merge.
Stub locator URLs only when PDF parse misses a county.

Tennessee (TDHS): Official Family Assistance office locator HTML (95 counties).

Kentucky (DCBS): Official CHFS local office search (120 counties) + kentucky-dcbs-verified.json merge.

Indiana (DFR): Official FSSA DFR county office PDF (92 counties).

Michigan (MDHHS): Official County Composite Directory HTML (83 counties).

Illinois (IDHS FCRC): Official DHS Office Locator by county (102 counties).

Virginia (LDSS): Official VDSS local agency directory (~121 local departments
covering all 133 localities; combined districts carry a "served" list).

Alabama (DHR): Official county office contact accordion page (67 counties).

Usage:
  python3 scripts/sync-county-benefits-offices.py [--state ohio|tennessee|kentucky|indiana|michigan|illinois|west-virginia|georgia|north-carolina|virginia|south-carolina|alabama|wisconsin|florida|mississippi|texas|all]
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
IL_OUTPUT = DATA_DIR / "illinois-idhs-offices.json"
WV_OUTPUT = DATA_DIR / "west-virginia-dohs-offices.json"
GA_OUTPUT = DATA_DIR / "georgia-dfcs-offices.json"
NC_DSS_LOCATOR = "https://www.ncdhhs.gov/divisions/social-services/local-dss-directory"
NC_OUTPUT = DATA_DIR / "north-carolina-dss-offices.json"
VA_LDSS_LOCATOR = "https://www.dss.virginia.gov/localagency/index.php"
VA_OUTPUT = DATA_DIR / "virginia-dss-offices.json"
AL_DHR_LOCATOR = "https://dhr.alabama.gov/county-office-contact/"
AL_OUTPUT = DATA_DIR / "alabama-dhr-offices.json"
SC_DSS_LOCATOR = "https://dss.sc.gov/contact-dss/"
SC_OUTPUT = DATA_DIR / "south-carolina-dss-offices.json"
WI_EM_LOCATOR = "https://www.dhs.wisconsin.gov/em/index.htm"
FL_OUTPUT = DATA_DIR / "florida-dcf-offices.json"
MS_OUTPUT = DATA_DIR / "mississippi-mdhs-offices.json"
MS_LOCATOR = "https://www.mdhs.ms.gov/contact/"
WI_OUTPUT = DATA_DIR / "wisconsin-dhs-offices.json"
TX_OUTPUT = DATA_DIR / "texas-hhsc-offices.json"

# South Carolina DSS county pages grouped by regional hub (46 counties).
SC_DSS_REGIONS: dict[str, list[str]] = {
    "upstate": [
        "Abbeville", "Anderson", "Cherokee", "Greenville", "Greenwood", "Laurens",
        "Newberry", "Oconee", "Pickens", "Spartanburg", "Union",
    ],
    "midlands": [
        "Aiken", "Bamberg", "Barnwell", "Chester", "Edgefield", "Fairfield", "Kershaw",
        "Lancaster", "Lexington", "McCormick", "Richland", "Saluda", "York",
    ],
    "lowcountry": [
        "Allendale", "Beaufort", "Berkeley", "Calhoun", "Charleston", "Colleton",
        "Dorchester", "Hampton", "Jasper", "Orangeburg",
    ],
    "pee-dee": [
        "Chesterfield", "Clarendon", "Darlington", "Dillon", "Florence", "Georgetown",
        "Horry", "Lee", "Marion", "Marlboro", "Sumter", "Williamsburg",
    ],
}

# Combined VDSS districts: one local department serves multiple localities
# (121 local departments cover 133 localities). Keys are substrings of the
# directory agency name, checked in order. Salem contracts with Roanoke County
# DSS (roanokecountyva.gov FAQ / 211virginia); the Shenandoah Valley DSS
# district (Augusta, Staunton, Waynesboro) lists two office cards.
VA_DSS_DISTRICTS: list[tuple[str, list[str]]] = [
    ("Alleghany-Covington", ["Alleghany", "Covington"]),
    ("Chesterfield/Colonial Heights", ["Chesterfield", "Colonial Heights"]),
    ("Fairfax County", ["Fairfax", "Fairfax City", "Falls Church"]),
    ("Greensville/Emporia", ["Greensville", "Emporia"]),
    ("Harrisonburg-Rockingham", ["Harrisonburg", "Rockingham"]),
    ("Henry-Martinsville", ["Henry", "Martinsville"]),
    ("Roanoke County", ["Roanoke", "Salem"]),
    ("Rockbridge-Buena Vista-Lexington", ["Rockbridge", "Buena Vista", "Lexington"]),
    ("Shenandoah Valley Dept. of Social Services (Waynesboro", ["Waynesboro"]),
    ("Shenandoah Valley", ["Augusta", "Staunton"]),
    ("York/Poquoson", ["York", "Poquoson"]),
]

# Verified when DFCS locator pages omit street data or use alternate slugs.
GA_DFCS_MANUAL_OVERRIDES: dict[str, dict[str, str]] = {
    "Forsyth": {
        "city": "Alpharetta",
        "address": "6435 Shiloh Road, Suite C",
        "phone": "770-781-6700",
        "source": "https://dfcs.georgia.gov/locations/forsyth-county-0",
    },
    "Fulton": {
        "city": "Atlanta",
        "address": "1249 Donald Lee Hollowell Parkway NW",
        "phone": "404-206-5300",
        "source": "https://dfcs.georgia.gov/press-releases/2025-08-04/fulton-county-dfcs-and-dcss-offices-consolidating",
    },
}
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


def sync_illinois() -> list[dict]:
    from illinois_idhs_directory import fetch_all_county_fcrcs

    official = load_counties_from_ts("src/lib/illinois/counties.ts")
    by_county = fetch_all_county_fcrcs(official)
    missing = [county for county in official if county not in by_county]
    for county in missing:
        by_county[county] = {
            "county": county,
            "city": "",
            "address": "",
            "phone": "1-800-843-6154",
            "website": "https://abe.illinois.gov",
            "source": "https://www.dhs.state.il.us/page.aspx?OfficeType=5&module=12",
        }
    result = [by_county[county] for county in official]
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    IL_OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with_address = sum(1 for office in result if office.get("address"))
    print(
        f"Wrote {IL_OUTPUT.name}: {len(result)} counties "
        f"({with_address} with address from IDHS FCRC locator)"
    )
    if missing:
        print(f"  Missing from locator parse: {missing}")
    return result


def sync_west_virginia() -> list[dict]:
    from west_virginia_dohs_directory import fetch_all_county_dohs

    official = load_counties_from_ts("src/lib/west-virginia/counties.ts")
    by_county = fetch_all_county_dohs(official)
    missing = [county for county in official if county not in by_county]
    for county in missing:
        by_county[county] = {
            "county": county,
            "city": "",
            "address": "",
            "phone": "1-877-716-1212",
            "website": "https://wvpath.wv.gov",
            "source": "https://dhhr.wv.gov/Pages/Field-Offices.aspx",
        }
    result = [by_county[county] for county in official]
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    WV_OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with_address = sum(1 for office in result if office.get("address"))
    print(
        f"Wrote {WV_OUTPUT.name}: {len(result)} counties "
        f"({with_address} with address from DoHS field office locator)"
    )
    if missing:
        print(f"  Missing from locator parse: {missing}")
    return result


def _parse_nc_dss_title(title_html: str) -> tuple[str, str, str]:
    """Extract address, city, phone from DSS directory popup HTML."""
    title = unescape(title_html)
    title = re.sub(r"<[^>]+>", "\n", title)
    title = unescape(title)
    lines = [line.strip() for line in title.split("\n") if line.strip()]
    phone = ""
    address = ""
    city = ""
    for line in lines:
        phone_match = re.search(
            r"(?:Phone|Main Number|Tel\.?)\s*#?\s*:?\s*([\d\-\(\)\s,]+)",
            line,
            re.I,
        )
        if phone_match and not phone:
            phone = re.sub(r"\s+", " ", phone_match.group(1).strip().rstrip(","))
        if re.search(r"\bNC\s+\d{5}", line):
            addr_line = re.sub(r"^[^:]+:\s*", "", line).strip()
            if addr_line and not address:
                address = addr_line.split("P.O.")[0].strip().rstrip(",")
                city_match = re.search(r",\s*([^,]+),\s*NC\s+\d{5}", addr_line)
                if city_match:
                    city = city_match.group(1).strip()
    return address, city, phone


def _parse_nc_dss_map(html: str, official: list[str]) -> dict[str, dict]:
    match = re.search(r'data-map="(\[.*?\])"', html)
    if not match:
        raise SystemExit("No NC DSS data-map JSON found on locator page")
    raw = match.group(1)
    raw = raw.replace("&quot;", '"').replace("&amp;", "&").replace("&#39;", "'")
    entries = json.loads(raw)
    by_county: dict[str, dict] = {}
    for item in entries:
        county = item.get("county", "").strip()
        if not county:
            continue
        address, city, phone = _parse_nc_dss_title(item.get("title", ""))
        url_path = item.get("url", "")
        source = (
            f"https://www.ncdhhs.gov{url_path}"
            if url_path.startswith("/")
            else url_path or NC_DSS_LOCATOR
        )
        by_county[county] = {
            "county": county,
            "city": city,
            "address": address,
            "phone": phone,
            "source": source,
        }
    for county in official:
        if county not in by_county:
            by_county[county] = {
                "county": county,
                "city": "",
                "address": "",
                "phone": "",
                "source": NC_DSS_LOCATOR,
            }
    return by_county


def sync_north_carolina() -> list[dict]:
    """Parse embedded county map data from NCDHHS Local DSS Directory."""
    official = load_counties_from_ts("src/lib/north-carolina/counties.ts")
    html = _fetch(NC_DSS_LOCATOR)
    by_county = _parse_nc_dss_map(html, official)

    existing: dict[str, dict] = {}
    if NC_OUTPUT.is_file():
        try:
            for row in json.loads(NC_OUTPUT.read_text(encoding="utf-8")):
                existing[row["county"]] = row
        except (json.JSONDecodeError, KeyError):
            pass

    result: list[dict] = []
    for county in official:
        parsed = by_county.get(county, {})
        prior = existing.get(county, {})
        for field in ("city", "address", "phone", "source"):
            if not parsed.get(field) and prior.get(field):
                parsed[field] = prior[field]
        parsed["county"] = county
        result.append(parsed)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    NC_OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with_address = sum(1 for office in result if office.get("address"))
    print(
        f"Wrote {NC_OUTPUT.name}: {len(result)} counties "
        f"({with_address} with address from DSS locator)"
    )
    return result


def sync_georgia() -> list[dict]:
    """Scrape DFCS county office pages for address data."""
    import time
    from html import unescape

    official = load_counties_from_ts("src/lib/georgia/counties.ts")

    def slug(county: str) -> str:
        return county.lower().replace(" ", "-")

    def parse_office(html: str, county: str, url: str) -> dict:
        line1 = re.search(r'class="address-line1">([^<]+)', html)
        locality = re.search(r'class="locality">([^<]+)', html)
        phone_m = re.search(r'Primary[^0-9]*\((\d{3})\)\s*(\d{3})-(\d{4})', html)
        street = unescape(line1.group(1).strip()) if line1 else ""
        city = unescape(locality.group(1).strip()) if locality else ""
        phone = (
            f"({phone_m.group(1)}) {phone_m.group(2)}-{phone_m.group(3)}"
            if phone_m
            else ""
        )
        return {
            "county": county,
            "city": city,
            "address": street,
            "phone": phone,
            "source": url,
        }

    by_county: dict[str, dict] = {}
    existing: dict[str, dict] = {}
    if GA_OUTPUT.is_file():
        try:
            for row in json.loads(GA_OUTPUT.read_text(encoding="utf-8")):
                existing[row["county"]] = row
        except (json.JSONDecodeError, KeyError):
            pass

    def location_urls(county: str) -> list[str]:
        base = slug(county)
        urls = [f"https://dfcs.georgia.gov/locations/{base}-county"]
        if county == "Forsyth":
            urls.insert(0, f"https://dfcs.georgia.gov/locations/{base}-county-0")
        return urls

    for i, county in enumerate(official):
        parsed: dict | None = None
        for url in location_urls(county):
            try:
                html = _fetch(url)
                candidate = parse_office(html, county, url)
                if candidate.get("address"):
                    parsed = candidate
                    break
            except OSError:
                continue
        if parsed is None:
            parsed = {
                "county": county,
                "city": "",
                "address": "",
                "phone": "",
                "source": location_urls(county)[0],
            }
        prior = existing.get(county, {})
        for field in ("city", "address", "phone", "source"):
            if not parsed.get(field) and prior.get(field):
                parsed[field] = prior[field]
        override = GA_DFCS_MANUAL_OVERRIDES.get(county)
        if override:
            parsed.update(override)
        by_county[county] = parsed
        if (i + 1) % 40 == 0:
            print(f"  Georgia DFCS: fetched {i + 1}/{len(official)}")
        time.sleep(0.12)

    result = [by_county[c] for c in official]
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    GA_OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with_address = sum(1 for o in result if o.get("address"))
    print(
        f"Wrote {GA_OUTPUT.name}: {len(result)} counties "
        f"({with_address} with address from DFCS locator)"
    )
    return result


def _va_agency_localities(name: str, official: list[str]) -> list[str]:
    """Map a VDSS directory agency name to the canonical localities it serves."""
    for key, localities in VA_DSS_DISTRICTS:
        if key in name:
            return list(localities)
    base = re.sub(
        r"\s+(?:Department|Dept\.?|Division)\s+of\s+"
        r"(?:Community and Human Services|Human Services|Family Services|Social Services)$",
        "",
        name,
        flags=re.I,
    )
    base = re.sub(r"\s+(?:Human|Social)\s+Services$", "", base, flags=re.I).strip()
    no_county = re.sub(r"\s+County$", "", base)
    for candidate in (base, no_county, re.sub(r"\s+City$", "", no_county)):
        match = normalize_county_name(candidate, official)
        if match:
            return [match]
    return []


def _parse_va_cards(html: str) -> list[dict]:
    """Parse agency cards from a VDSS local agency directory page."""
    cards: list[dict] = []
    for chunk in html.split('<div class="staff-card staff-card--advanced">')[1:]:
        heading = re.search(
            r'class="card-heading"(?: href="([^"]*)")?><span>([^<]+)</span>', chunk
        )
        if not heading:
            continue
        website = heading.group(1) or ""
        name = unescape(heading.group(2).strip())
        addr_match = re.search(r"</svg>\s*([^<]*?,\s*VA\s*\d{5}(?:-\d{4})?)", chunk)
        address = city = ""
        if addr_match:
            raw = re.sub(r"\s+", " ", unescape(addr_match.group(1))).strip()
            parts = re.match(r"(.*?),\s*([^,]+),\s*VA\s*\d{5}", raw)
            if parts:
                address = parts.group(1).strip().rstrip(",")
                city = parts.group(2).strip()
            else:
                address = raw
        phone_match = re.search(r'href="tel:([^"]+)"', chunk)
        phone = unescape(phone_match.group(1).strip()) if phone_match else ""
        cards.append(
            {
                "agency": name,
                "website": website,
                "address": address,
                "city": city,
                "phone": phone,
            }
        )
    return cards


def _al_county_from_slug(slug: str, official: list[str]) -> str | None:
    """Map accordion data-anchor-id slug to canonical county name."""
    slug = slug.strip().lower()
    for county in official:
        if county.lower().replace(".", "").replace(" ", "-") == slug.replace(".", ""):
            return county
        if county.lower().replace(" ", "-") == slug:
            return county
    if slug == "st-clair":
        return "St. Clair"
    if slug == "dekalb":
        return "DeKalb"
    return None


def _parse_al_dhr_panel(panel_html: str, county: str) -> dict:
    """Extract address, city, and benefits phone from one DHR accordion panel."""
    text = re.sub(r"<[^>]+>", "\n", panel_html)
    text = unescape(re.sub(r"\s+", " ", text))
    text = re.sub(r" +", " ", text)
    lines = [ln.strip() for ln in re.split(r"\n+", panel_html) if ln.strip()]
    plain = "\n".join(unescape(re.sub(r"<[^>]+>", "\n", panel_html)).split())

    phone = ""
    for label in ("Food Assistance", "Food Stamp", "Main Number", "Family and Child Services"):
        m = re.search(
            rf"{re.escape(label)}\s*\((\d{{3}})\)\s*(\d{{3}})-(\d{{4}})",
            plain,
            re.I,
        )
        if m:
            phone = f"({m.group(1)}) {m.group(2)}-{m.group(3)}"
            break

    address = ""
    city = ""
    street_m = re.search(
        r"(?:Street(?:\s+and\s+Mailing)?\s+Address|Street Address)\s*(?:<br\s*/?>\s*)*([^<\n]+?)\s*<br\s*/?>\s*([^<\n,]+),\s*AL\s*(\d{5})",
        panel_html,
        re.I | re.S,
    )
    if street_m:
        address = unescape(street_m.group(1).strip().rstrip(","))
        city = unescape(street_m.group(2).strip())
    else:
        addr_m = re.search(
            r"Address:.*?<br\s*/?>\s*([^<\n]+?)\s*<br\s*/?>\s*([^<\n,]+),\s*AL\s*(\d{5})",
            panel_html,
            re.I | re.S,
        )
        if addr_m:
            address = unescape(addr_m.group(1).strip().rstrip(","))
            city = unescape(addr_m.group(2).strip())

    return {
        "county": county,
        "city": city,
        "address": address,
        "phone": phone,
        "source": AL_DHR_LOCATOR,
    }


def sync_alabama() -> list[dict]:
    """Parse DHR county office accordion panels (67 counties)."""
    official = load_counties_from_ts("src/lib/alabama/counties.ts")
    html = _fetch(AL_DHR_LOCATOR)

    by_county: dict[str, dict] = {}
    for panel in re.finditer(
        r'data-anchor-id="([^"]+)"[\s\S]*?id="accordion-content-\1"[\s\S]*?'
        r'<div class="sow-accordion-panel-border">([\s\S]*?)</div>\s*</div>\s*</div>',
        html,
        re.I,
    ):
        slug = panel.group(1)
        county = _al_county_from_slug(slug, official)
        if not county:
            print(f"Warning: unrecognized DHR accordion slug {slug!r}")
            continue
        by_county[county] = _parse_al_dhr_panel(panel.group(2), county)

    existing: dict[str, dict] = {}
    if AL_OUTPUT.is_file():
        try:
            for row in json.loads(AL_OUTPUT.read_text(encoding="utf-8")):
                existing[row["county"]] = row
        except (json.JSONDecodeError, KeyError):
            pass

    result: list[dict] = []
    for county in official:
        parsed = by_county.get(county, {"county": county, "city": "", "address": "", "phone": "", "source": AL_DHR_LOCATOR})
        prior = existing.get(county, {})
        for field in ("city", "address", "phone", "source"):
            if not parsed.get(field) and prior.get(field):
                parsed[field] = prior[field]
        parsed["county"] = county
        result.append(parsed)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    AL_OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with_address = sum(1 for office in result if office.get("address"))
    print(
        f"Wrote {AL_OUTPUT.name}: {len(result)} counties "
        f"({with_address} with address from DHR directory)"
    )
    missing = [c for c in official if c not in by_county]
    if missing:
        print(f"  Not parsed from page: {missing}")
    return result


def sync_virginia() -> list[dict]:
    """Scrape the paginated VDSS local agency directory (one card per LDSS)."""
    official = load_counties_from_ts("src/lib/virginia/counties.ts")
    cards: list[dict] = []
    for page in range(1, 11):
        url = f"{VA_LDSS_LOCATOR}?showall=1&paginate=30&page={page}"
        parsed = _parse_va_cards(_fetch(url))
        if not parsed:
            break
        cards.extend(parsed)
        if len(parsed) < 30:
            break
        time.sleep(0.1)
    if not cards:
        raise SystemExit("No agency cards parsed from VDSS local agency directory")

    by_locality: dict[str, dict] = {}
    for card in cards:
        localities = _va_agency_localities(card["agency"], official)
        if not localities:
            print(f"Warning: unrecognized VDSS agency {card['agency']!r}")
            continue
        for locality in localities:
            if locality in by_locality:
                print(
                    f"Warning: {locality} mapped by both "
                    f"{by_locality[locality]['agency']!r} and {card['agency']!r}"
                )
            by_locality[locality] = {
                "county": locality,
                "served": localities,
                "agency": card["agency"],
                "city": card["city"],
                "address": card["address"],
                "phone": card["phone"],
                "website": card["website"],
                "source": VA_LDSS_LOCATOR,
            }

    existing: dict[str, dict] = {}
    if VA_OUTPUT.is_file():
        try:
            for row in json.loads(VA_OUTPUT.read_text(encoding="utf-8")):
                existing[row["county"]] = row
        except (json.JSONDecodeError, KeyError):
            pass

    missing = [locality for locality in official if locality not in by_locality]
    for locality in missing:
        by_locality[locality] = {
            "county": locality,
            "served": [locality],
            "agency": "",
            "city": "",
            "address": "",
            "phone": "",
            "website": "",
            "source": VA_LDSS_LOCATOR,
        }

    result: list[dict] = []
    for locality in official:
        entry = by_locality[locality]
        prior = existing.get(locality, {})
        for field in ("agency", "city", "address", "phone", "website"):
            if not entry.get(field) and prior.get(field):
                entry[field] = prior[field]
        result.append(entry)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    VA_OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with_address = sum(1 for office in result if office.get("address"))
    print(
        f"Wrote {VA_OUTPUT.name}: {len(result)} localities "
        f"({with_address} with address from VDSS directory)"
    )
    if missing:
        print(f"  Stubbed (not in directory): {missing}")
    return result


def _sc_county_slug(county: str) -> str:
    return county.lower().replace(" ", "-")


def _parse_sc_dss_page(html: str) -> dict:
    """Parse address and main phone from an SCDSS county contact page."""
    result: dict[str, str] = {"address": "", "city": "", "phone": ""}
    addr_m = re.search(
        r"<h[34][^>]*>.*?(?:Administration )?Address:.*?</h[34]>(.*?)(?:<div class=\"col-sm-7\">|</div>\s*</div>\s*<div)",
        html,
        re.S | re.I,
    )
    if addr_m:
        block = addr_m.group(1)
        # Use last <p> block with a street/city line (skip **NEW LOCATION** notices).
        paragraphs = re.findall(r"<p[^>]*>(.*?)</p>", block, re.S | re.I)
        lines: list[str] = []
        for para in paragraphs:
            raw = re.sub(r"<br\s*/?>", "\n", para, flags=re.I)
            for line in raw.split("\n"):
                clean = unescape(re.sub(r"<[^>]+>", "", line)).strip()
                if clean and not clean.startswith("**"):
                    lines.append(clean)
        street_lines = [ln for ln in lines if not re.match(r"^.+ County DSS$", ln, re.I)]
        if street_lines:
            city_m = re.match(r"([^,]+),", street_lines[-1])
            if city_m:
                result["city"] = city_m.group(1).strip()
            if len(street_lines) >= 2:
                result["address"] = street_lines[-2] if city_m else street_lines[-1]
            elif len(street_lines) == 1 and not city_m:
                result["address"] = street_lines[0]
    phone_m = re.search(
        r"\((\d{3})\)\s*(\d{3})-(\d{4})\s+Main",
        html,
        re.I,
    )
    if not phone_m:
        phone_m = re.search(r"\((\d{3})\)\s*(\d{3})-(\d{4})", html)
    if phone_m:
        result["phone"] = f"({phone_m.group(1)}) {phone_m.group(2)}-{phone_m.group(3)}"
    return result


def sync_south_carolina() -> list[dict]:
    """Scrape SCDSS county contact pages (Upstate, Midlands, Lowcountry, Pee Dee)."""
    official = load_counties_from_ts("src/lib/south-carolina/counties.ts")
    by_county: dict[str, dict] = {}

    existing: dict[str, dict] = {}
    if SC_OUTPUT.is_file():
        try:
            for row in json.loads(SC_OUTPUT.read_text(encoding="utf-8")):
                existing[row["county"]] = row
        except (json.JSONDecodeError, KeyError):
            pass

    for region, counties in SC_DSS_REGIONS.items():
        for i, county in enumerate(counties):
            slug = _sc_county_slug(county)
            url = f"https://dss.sc.gov/contact-dss/{region}-region/{slug}/"
            try:
                parsed = _parse_sc_dss_page(_fetch(url))
                parsed["county"] = county
                parsed["source"] = url
            except OSError:
                parsed = {
                    "county": county,
                    "city": "",
                    "address": "",
                    "phone": "",
                    "source": url,
                }
            prior = existing.get(county, {})
            for field in ("city", "address", "phone", "source"):
                if not parsed.get(field) and prior.get(field):
                    parsed[field] = prior[field]
            by_county[county] = parsed
            if (i + 1) % 12 == 0:
                print(f"  South Carolina DSS: fetched {region} {i + 1}/{len(counties)}")
            time.sleep(0.12)

    result = [by_county[c] for c in official if c in by_county]
    for county in official:
        if county not in by_county:
            result.append(
                {
                    "county": county,
                    "city": "",
                    "address": "",
                    "phone": "",
                    "source": SC_DSS_LOCATOR,
                }
            )

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SC_OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with_address = sum(1 for office in result if office.get("address"))
    print(
        f"Wrote {SC_OUTPUT.name}: {len(result)} counties "
        f"({with_address} with address from DSS locator)"
    )
    return result


def sync_wisconsin() -> list[dict]:
    """Fetch DHS Eligibility Management county pages (72 counties)."""
    from wisconsin_em_directory import ACCESS_WI, fetch_all_county_offices

    official = load_counties_from_ts("src/lib/wisconsin/counties.ts")

    existing: dict[str, dict] = {}
    if WI_OUTPUT.is_file():
        try:
            for row in json.loads(WI_OUTPUT.read_text(encoding="utf-8")):
                existing[row["county"]] = row
        except (json.JSONDecodeError, KeyError):
            pass

    fetched = fetch_all_county_offices(official)

    result: list[dict] = []
    for county in official:
        parsed = fetched.get(
            county,
            {
                "county": county,
                "city": "",
                "address": "",
                "phone": "1-800-362-3002",
                "website": ACCESS_WI,
                "source": WI_EM_LOCATOR,
            },
        )
        prior = existing.get(county, {})
        for field in ("city", "address", "phone", "source"):
            if not parsed.get(field) and prior.get(field):
                parsed[field] = prior[field]
        parsed["county"] = county
        if not parsed.get("website"):
            parsed["website"] = ACCESS_WI
        result.append(parsed)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    WI_OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with_address = sum(1 for office in result if office.get("address"))
    print(
        f"Wrote {WI_OUTPUT.name}: {len(result)} counties "
        f"({with_address} with address from DHS EM pages)"
    )
    return result


def sync_florida() -> list[dict]:
    """Refresh florida-dcf-offices.json from embedded DCF ACCESS directory."""
    import importlib.util

    bootstrap_path = ROOT / "scripts" / "_bootstrap_florida_pipeline.py"
    spec = importlib.util.spec_from_file_location("fl_bootstrap", bootstrap_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load Florida bootstrap: {bootstrap_path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.write_dcf_json()
    result = json.loads(FL_OUTPUT.read_text(encoding="utf-8"))
    with_address = sum(1 for office in result if office.get("address"))
    print(
        f"Wrote {FL_OUTPUT.name}: {len(result)} counties "
        f"({with_address} with address from DCF directory)"
    )
    return result


def sync_mississippi() -> list[dict]:
    """Validate and normalize mississippi-mdhs-offices.json for all 82 counties."""
    official = load_counties_from_ts("src/lib/mississippi/counties.ts")
    existing: dict[str, dict] = {}
    if MS_OUTPUT.is_file():
        try:
            for row in json.loads(MS_OUTPUT.read_text(encoding="utf-8")):
                existing[row["county"]] = row
        except (json.JSONDecodeError, KeyError):
            pass

    result: list[dict] = []
    for county in official:
        parsed = existing.get(county, {})
        prior = parsed if parsed else {
            "county": county,
            "city": "",
            "address": "",
            "phone": "1-800-948-4060",
            "source": MS_LOCATOR,
        }
        prior["county"] = county
        if not prior.get("source"):
            prior["source"] = MS_LOCATOR
        result.append(prior)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    MS_OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with_address = sum(1 for office in result if office.get("address"))
    print(
        f"Wrote {MS_OUTPUT.name}: {len(result)} counties "
        f"({with_address} with address from MDHS contact directory)"
    )
    return result


def sync_texas() -> list[dict]:
    """Validate and normalize texas-hhsc-offices.json for all 254 counties."""
    official = load_counties_from_ts("src/lib/texas/counties.ts")
    existing: dict[str, dict] = {}
    if TX_OUTPUT.is_file():
        try:
            for row in json.loads(TX_OUTPUT.read_text(encoding="utf-8")):
                existing[row["county"]] = row
        except (json.JSONDecodeError, KeyError):
            pass

    result: list[dict] = []
    for county in official:
        parsed = existing.get(county, {})
        prior = parsed if parsed else {
            "county": county,
            "city": county,
            "address": "",
            "phone": "877-541-7905",
            "website": "https://yourtexasbenefits.com",
            "source": "https://www.hhs.texas.gov/services/snap/apply-for-snap",
        }
        prior["county"] = county
        if not prior.get("source"):
            prior["source"] = "https://www.hhs.texas.gov/services/snap/apply-for-snap"
        if not prior.get("website"):
            prior["website"] = "https://yourtexasbenefits.com"
        result.append(prior)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    TX_OUTPUT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with_address = sum(1 for office in result if office.get("address"))
    print(
        f"Wrote {TX_OUTPUT.name}: {len(result)} counties "
        f"({with_address} with address from HHSC directory)"
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync county benefits office JSON data")
    parser.add_argument(
        "--state",
        choices=("ohio", "tennessee", "kentucky", "indiana", "michigan", "illinois", "west-virginia", "georgia", "north-carolina", "virginia", "south-carolina", "alabama", "wisconsin", "florida", "mississippi", "texas", "all"),
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
    if args.state in ("illinois", "all"):
        sync_illinois()
    if args.state in ("west-virginia", "all"):
        sync_west_virginia()
    if args.state in ("georgia", "all"):
        sync_georgia()
    if args.state in ("north-carolina", "all"):
        sync_north_carolina()
    if args.state in ("virginia", "all"):
        sync_virginia()
    if args.state in ("alabama", "all"):
        sync_alabama()
    if args.state in ("south-carolina", "all"):
        sync_south_carolina()
    if args.state in ("wisconsin", "all"):
        sync_wisconsin()
    if args.state in ("florida", "all"):
        sync_florida()
    if args.state in ("mississippi", "all"):
        sync_mississippi()
    if args.state in ("texas", "all"):
        sync_texas()


if __name__ == "__main__":
    main()
