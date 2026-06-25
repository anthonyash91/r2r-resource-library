"""Register county benefits intake rows from synced JSON (all counties, skip existing FA pins)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

DATA_DIR = Path(__file__).resolve().parent / "data"

TN_LOCATOR = (
    "https://www.tn.gov/humanservices/for-families/"
    "supplemental-nutrition-assistance-program-snap/office-locator-family-assistance.html"
)
PCSAO_DIRECTORY = "https://pcsao.org/membership/agency-directory/"
IN_DFR_LOCATOR = "https://www.in.gov/fssa/dfr/ebt-hoosier-works-card/find-my-local-dfr-office/"
KY_KYNECT = "https://kynect.ky.gov/benefits/s/"
MI_DIRECTORY = (
    "https://mdhhs.michigan.gov/CompositeDirPub/CountyCompositeDirectory.aspx"
)
IL_FCRC_LOCATOR = "https://www.dhs.state.il.us/page.aspx?OfficeType=5&module=12"
IL_ABE = "https://abe.illinois.gov"
WV_DOHS_LOCATOR = "https://dhhr.wv.gov/Pages/Field-Offices.aspx"
WV_PATH = "https://wvpath.wv.gov"
GA_DFCS_LOCATOR = "https://dfcs.georgia.gov/locations"
GA_COMPASS = "https://compass.ga.gov"


def normalize_category(value: str) -> str:
    raw = (value or "").strip()
    display = {
        "Financial Assistance": "financial-assistance",
        "Housing": "housing",
    }
    if raw in display:
        return display[raw]
    return raw.lower().replace(" ", "-")


def collect_financial_assistance_counties(entries: list[dict]) -> set[str]:
    """Counties already pinned by a financial-assistance row (single/multi, not statewide)."""
    pinned: set[str] = set()
    for row in entries:
        if normalize_category(row.get("category", "")) != "financial-assistance":
            continue
        if (row.get("coverage") or "").strip() == "statewide":
            continue
        county = (row.get("county") or "").strip()
        if county:
            pinned.add(county)
        for part in (row.get("served_counties") or "").split("|"):
            part = part.strip()
            if part:
                pinned.add(part)
    return pinned


def _load_offices(filename: str) -> list[dict]:
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path.name}; run: python3 scripts/sync-county-benefits-offices.py"
        )
    return json.loads(path.read_text(encoding="utf-8"))


def register_county_benefits_ohio(add: Callable[..., None], existing_fa: set[str]) -> int:
    from phase3b_gapfill import _jfs_oh, _jfs_desc_en, _jfs_desc_es

    added = 0
    for office in _load_offices("ohio-cdjfs-offices.json"):
        county = office["county"]
        if county in existing_fa:
            continue
        city = office.get("city") or county
        region = f"{city} / {county} County" if city else f"{county} County"
        website = office.get("website") or PCSAO_DIRECTORY
        source = office.get("source") or website
        add(
            **_jfs_oh(
                county,
                city,
                office.get("address", ""),
                office.get("phone", ""),
                website,
                region,
                _jfs_desc_en(county, city),
                _jfs_desc_es(county, city),
            )
            | {
                "_source": source,
                "_confidence": "high" if office.get("address") else "medium",
            }
        )
        existing_fa.add(county)
        added += 1
    return added


def register_county_benefits_tennessee(add: Callable[..., None], existing_fa: set[str]) -> int:
    from phase3b_gapfill import _dhs_desc_en, _dhs_desc_es, _dhs_tn

    added = 0
    for office in _load_offices("tn-tdhs-offices.json"):
        county = office["county"]
        if county in existing_fa:
            continue
        city = office.get("city") or county
        region = f"{city} / {county} County"
        add(
            **_dhs_tn(
                county,
                city,
                office.get("address", ""),
                office.get("phone", ""),
                region,
                _dhs_desc_en(county, city),
                _dhs_desc_es(county, city),
            )
            | {
                "_source": office.get("source", TN_LOCATOR),
                "_confidence": "high" if office.get("address") else "medium",
            }
        )
        existing_fa.add(county)
        added += 1
    return added


def register_county_benefits_indiana(add: Callable[..., None], existing_fa: set[str]) -> int:
    """Mechanical DFR row per county from synced FSSA PDF data."""
    from phase3b_gapfill import _dfr_in

    added = 0
    for office in _load_offices("indiana-dfr-offices.json"):
        county = office["county"]
        if county in existing_fa:
            continue
        city = office.get("city") or county
        website = office.get("website") or IN_DFR_LOCATOR
        add(
            **_dfr_in(
                county=county,
                city=city,
                address=office.get("address", ""),
                phone=office.get("phone", "800-403-0864"),
                website=website,
                region=f"{city} / {county} County",
                desc_en=(
                    f"{county} County Division of Family Resources is the local FSSA benefits intake office "
                    f"serving {county} County, helping Hoosiers apply for SNAP, TANF, Medicaid, Hoosier "
                    f"Healthwise, and Healthy Indiana Plan coverage. Returning citizens and families rebuilding "
                    f"after incarceration can establish health coverage and food benefits through in-person "
                    f"intake, the state Benefits Portal, or phone enrollment with county staff assisting "
                    f"document verification."
                ),
                desc_es=(
                    f"La División de Recursos Familiares del condado {county} es la oficina local de beneficios "
                    f"FSSA que ayuda a solicitar SNAP, TANF, Medicaid, Hoosier Healthwise y el Plan Saludable "
                    f"de Indiana. Ciudadanos que regresan pueden establecer cobertura de salud y beneficios "
                    f"alimentarios mediante admisión en persona, el Portal de Beneficios o inscripción "
                    f"telefónica con ayuda del personal del condado."
                ),
                services="SNAP enrollment|Medicaid and HIP|Hoosier Healthwise|TANF cash assistance|Benefits verification",
                tags=f"{county.lower()}|indiana|benefits|SNAP|Medicaid|reentry",
            )
            | {
                "_source": office.get("source", IN_DFR_LOCATOR),
                "_confidence": "high" if office.get("address") else "medium",
            }
        )
        existing_fa.add(county)
        added += 1
    return added


def register_county_benefits_kentucky(add: Callable[..., None], existing_fa: set[str]) -> int:
    from phase3b_gapfill import _dcbs_desc_en, _dcbs_desc_es, _dcbs_ky

    added = 0
    for office in _load_offices("kentucky-dcbs-offices.json"):
        county = office["county"]
        if county in existing_fa:
            continue
        city = office.get("city") or county
        region = f"{city} / {county} County"
        source = office.get("source") or KY_KYNECT
        add(
            **_dcbs_ky(
                county,
                city,
                office.get("address", ""),
                office.get("phone", ""),
                region,
                _dcbs_desc_en(county, city),
                _dcbs_desc_es(county, city),
            )
            | {
                "_source": source,
                "_confidence": "high" if office.get("address") else "medium",
            }
        )
        existing_fa.add(county)
        added += 1
    return added


def register_county_benefits_michigan(add: Callable[..., None], existing_fa: set[str]) -> int:
    from phase3b_gapfill import _mdhhs_desc_en, _mdhhs_desc_es, _mdhhs_mi

    added = 0
    for office in _load_offices("michigan-mdhhs-offices.json"):
        county = office["county"]
        if county in existing_fa:
            continue
        city = office.get("city") or county
        region = f"{city} / {county} County"
        add(
            **_mdhhs_mi(
                county,
                city,
                office.get("address", ""),
                office.get("phone", "1-844-464-3447"),
                region,
                _mdhhs_desc_en(county, city),
                _mdhhs_desc_es(county, city),
            )
            | {
                "_source": office.get("source", MI_DIRECTORY),
                "_confidence": "high" if office.get("address") else "medium",
            }
        )
        existing_fa.add(county)
        added += 1
    return added


def register_county_benefits_illinois(add: Callable[..., None], existing_fa: set[str]) -> int:
    from phase3b_gapfill import _fcrc_desc_en, _fcrc_desc_es, _fcrc_il

    added = 0
    for office in _load_offices("illinois-idhs-offices.json"):
        county = office["county"]
        if county in existing_fa:
            continue
        city = office.get("city") or county
        region = f"{city} / {county} County"
        add(
            **_fcrc_il(
                county,
                city,
                office.get("address", ""),
                office.get("phone", "1-800-843-6154"),
                region,
                _fcrc_desc_en(county, city),
                _fcrc_desc_es(county, city),
            )
            | {
                "_source": office.get("source", IL_FCRC_LOCATOR),
                "_confidence": "high" if office.get("address") else "medium",
            }
        )
        existing_fa.add(county)
        added += 1
    return added


def register_county_benefits_west_virginia(add: Callable[..., None], existing_fa: set[str]) -> int:
    from phase3b_gapfill import _dohs_desc_en, _dohs_desc_es, _dohs_wv

    added = 0
    for office in _load_offices("west-virginia-dohs-offices.json"):
        county = office["county"]
        if county in existing_fa:
            continue
        city = office.get("city") or county
        region = f"{city} / {county} County"
        add(
            **_dohs_wv(
                county,
                city,
                office.get("address", ""),
                office.get("phone", "1-877-716-1212"),
                region,
                _dohs_desc_en(county, city),
                _dohs_desc_es(county, city),
            )
            | {
                "_source": office.get("source", WV_DOHS_LOCATOR),
                "_confidence": "high" if office.get("address") else "medium",
            }
        )
        existing_fa.add(county)
        added += 1
    return added


def register_county_benefits_georgia(add: Callable[..., None], existing_fa: set[str]) -> int:
    from phase3b_gapfill import _dfcs_desc_en, _dfcs_desc_es, _dfcs_ga

    added = 0
    for office in _load_offices("georgia-dfcs-offices.json"):
        county = office["county"]
        if county in existing_fa:
            continue
        city = office.get("city") or county
        region = f"{city} / {county} County"
        source = office.get("source", GA_DFCS_LOCATOR)
        add(
            **_dfcs_ga(
                county,
                city,
                office.get("address", ""),
                office.get("phone", "1-877-423-4746"),
                region,
                _dfcs_desc_en(county, city),
                _dfcs_desc_es(county, city),
                source,
            )
            | {
                "_confidence": "high" if office.get("address") else "medium",
            }
        )
        existing_fa.add(county)
        added += 1
    return added
