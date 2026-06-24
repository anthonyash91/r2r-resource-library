"""Parse Ohio CDJFS offices from the official ODJFS county directory PDF."""

from __future__ import annotations

import io
import re
import urllib.request

from county_list_utils import normalize_county_name

PDF_URL = "https://dam.assets.ohio.gov/image/upload/jfs.ohio.gov/County/County_Directory.pdf"

AGENCY_BLOCK = re.compile(
    r"((?:County Department of Job and Family Services|"
    r"[A-Za-z .'-]+ County Job and Family Services|"
    r"South Central Ohio Job and Family Services(?:\s*-\s*Income Maintenance)?)"
    r"\s*.*?)\s*CDJFS\s*-",
    re.S | re.I,
)
COUNTY_HEADER = re.compile(r"(?:^|\n)\s*([A-Za-z][A-Za-z .'-]*?) County - \d+", re.M)
ADDRESS = re.compile(
    r"((?:\d[^,]*|P\.?O\.?\s*Box[^,]*)(?:,\s*[^,]+)*,\s*[^,]+,\s*OH\s*\d{5}(?:-\d{4})?)",
    re.I,
)
PHONE = re.compile(r"\(\d{3}\)\s*\d{3}-\d{4}")
WEBSITE = re.compile(r"Website:\s*(\S+)", re.I)


def fetch_pdf_text() -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise SystemExit(
            "pypdf is required for Ohio CDJFS PDF sync: pip3 install pypdf"
        ) from exc

    request = urllib.request.Request(PDF_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        reader = PdfReader(io.BytesIO(response.read()))
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def _choose_agency_block(blocks: list[str]) -> str | None:
    if not blocks:
        return None
    for block in blocks:
        if "income maintenance" in block.lower():
            return block
    for block in blocks:
        if "south central ohio job and family services" in block.lower():
            return block
    return blocks[0]


def _parse_agency_block(block: str, tail: str) -> dict[str, str]:
    normalized = re.sub(r"\s+", " ", block).strip()
    address_match = ADDRESS.search(normalized)
    address = address_match.group(1).strip() if address_match else ""
    city = ""
    if address:
        city_match = re.search(r",\s*([^,]+),\s*OH\s*\d", address)
        if city_match:
            city = city_match.group(1).strip()

    phone = ""
    phone_match = re.search(r"Phone/Ext:\s*(.+?)(?:\s+Website:|$)", normalized, re.I)
    if phone_match:
        phones = PHONE.findall(phone_match.group(1))
        local = [number for number in phones if not number.startswith("(855)") and not number.startswith("(800)")]
        phone = local[0] if local else (phones[0] if phones else "")

    website_match = WEBSITE.search(tail[:500])
    website = website_match.group(1).rstrip(".,") if website_match else ""
    if website and not website.startswith("http"):
        website = f"https://{website}"

    return {
        "city": city,
        "address": address,
        "phone": phone,
        "website": website,
    }


def parse_cdjfs_from_pdf(text: str, official: list[str]) -> dict[str, dict]:
    matches = list(COUNTY_HEADER.finditer(text))
    by_county: dict[str, dict] = {}

    for index, match in enumerate(matches):
        county = normalize_county_name(match.group(1).strip(), official)
        if not county:
            continue
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        section = text[match.end() : end]
        blocks = [block_match.group(1) for block_match in AGENCY_BLOCK.finditer(section)]
        chosen = _choose_agency_block(blocks)
        if not chosen:
            continue
        cdjfs_index = section.find("CDJFS")
        tail = section[cdjfs_index:] if cdjfs_index >= 0 else ""
        parsed = _parse_agency_block(chosen, tail)
        by_county[county] = {
            "county": county,
            "city": parsed["city"],
            "address": parsed["address"],
            "phone": parsed["phone"],
            "website": parsed["website"],
            "source": PDF_URL,
        }
    return by_county
