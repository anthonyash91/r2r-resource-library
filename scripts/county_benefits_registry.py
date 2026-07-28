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
NC_DSS_LOCATOR = "https://www.ncdhhs.gov/divisions/social-services/local-dss-directory"
NC_EPASS = "https://epass.nc.gov"
VA_LDSS_LOCATOR = "https://www.dss.virginia.gov/localagency/index.php"
VA_COMMONHELP = "https://commonhelp.virginia.gov"
AL_DHR_LOCATOR = "https://dhr.alabama.gov/county-office-contact/"
AL_MYDHR = "https://mydhr.alabama.gov"
AZ_DES_LOCATOR = "https://des.az.gov/find-your-local-office"
AZ_HEALTHE_ARIZONA = "https://www.healthearizonaplus.gov"
MS_MDHS_LOCATOR = "https://www.mdhs.ms.gov/contact/"
MS_ACCESS_MS = "https://www.access.ms.gov"
FL_DCF_LOCATOR = "https://www.myflfamilies.com/service-programs/access/apply-now"
FL_MYACCESS = "https://myaccess.myflfamilies.com"
WI_EM_LOCATOR = "https://www.dhs.wisconsin.gov/em/index.htm"
TX_YTB = "https://yourtexasbenefits.com"
TX_HHSC_SNAP = "https://www.hhs.texas.gov/services/snap/apply-for-snap"
WI_ACCESS = "https://access.wi.gov"


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


# Virginia's 38 independent cities (canonical locality names from
# src/lib/virginia/counties.ts); everything else in the list is a county.
VA_INDEPENDENT_CITIES = {
    "Alexandria", "Bristol", "Buena Vista", "Charlottesville", "Chesapeake",
    "Colonial Heights", "Covington", "Danville", "Emporia", "Fairfax City",
    "Falls Church", "Franklin City", "Fredericksburg", "Galax", "Hampton",
    "Harrisonburg", "Hopewell", "Lexington", "Lynchburg", "Manassas",
    "Manassas Park", "Martinsville", "Newport News", "Norfolk", "Norton",
    "Petersburg", "Poquoson", "Portsmouth", "Radford", "Richmond City",
    "Roanoke City", "Salem", "Staunton", "Suffolk", "Virginia Beach",
    "Waynesboro", "Williamsburg", "Winchester",
}


def _va_locality_label(locality: str) -> str:
    if locality in VA_INDEPENDENT_CITIES:
        base = locality[:-5] if locality.endswith(" City") else locality
        return f"City of {base}"
    return f"{locality} County"


def _va_locality_en(locality: str) -> str:
    label = _va_locality_label(locality)
    return f"the {label}" if label.startswith("City of") else label


def _va_locality_es(locality: str) -> str:
    if locality in VA_INDEPENDENT_CITIES:
        base = locality[:-5] if locality.endswith(" City") else locality
        return f"la ciudad de {base}"
    return f"el condado de {locality}"


def _va_join_en(parts: list[str]) -> str:
    if len(parts) <= 1:
        return parts[0] if parts else ""
    if len(parts) == 2:
        return f"{parts[0]} and {parts[1]}"
    return ", ".join(parts[:-1]) + f", and {parts[-1]}"


def _va_join_es(parts: list[str]) -> str:
    if len(parts) <= 1:
        return parts[0] if parts else ""
    return ", ".join(parts[:-1]) + f" y {parts[-1]}"


def _va_area_es_with_de(served: list[str]) -> str:
    """Spanish area phrase already fused with the preposition "de" ("del condado…")."""
    joined = _va_join_es([_va_locality_es(loc) for loc in served])
    if joined.startswith("el "):
        return "del " + joined[3:]
    return "de " + joined


def register_county_benefits_virginia(add: Callable[..., None], existing_fa: set[str] | None = None) -> int:
    """One financial-assistance row per VDSS local department (121 offices, 133 localities)."""
    existing_fa = existing_fa if existing_fa is not None else set()
    added = 0
    for office in _load_offices("virginia-dss-offices.json"):
        served: list[str] = office.get("served") or [office["county"]]
        if office["county"] != served[0]:
            continue  # combined district; row is emitted for its primary locality
        if served[0] in existing_fa:
            continue
        agency = office.get("agency") or f"{_va_locality_en(served[0])} Department of Social Services"
        city = office.get("city") or served[0]
        area_en = _va_join_en([_va_locality_en(loc) for loc in served])
        area_es = _va_area_es_with_de(served)
        desc_en = (
            f"{agency} in {city} processes SNAP, Medicaid, TANF, and energy assistance applications "
            f"for residents of {area_en}, including returning citizens reestablishing food and health "
            f"benefits after release from jail or Virginia Department of Corrections custody."
        )
        desc_es = (
            f"{agency} en {city} procesa solicitudes de SNAP, Medicaid, TANF y asistencia de energía "
            f"para residentes {area_es}, incluidos ciudadanos que regresan que restablecen beneficios "
            f"alimentarios y de salud después de salir de la cárcel o de la custodia del Departamento "
            f"Correccional de Virginia."
        )
        add(
            name=f"{agency} — Benefits & Family Support",
            category="financial-assistance",
            region=f"{city} / {_va_locality_label(served[0])}",
            description=desc_en,
            description_es=desc_es,
            address=office.get("address", ""),
            city=city,
            phone=office.get("phone") or "833-522-5582",
            email="",
            website=office.get("website") or VA_LDSS_LOCATOR,
            eligibility=(
                f"Residents of {area_en} meeting income and household-size requirements for SNAP, "
                f"Medicaid, and TANF; criminal record generally not a barrier."
            ),
            eligibility_es=(
                f"Residentes {area_es} que cumplan requisitos de ingresos y tamaño de hogar para "
                f"SNAP, Medicaid y TANF; los antecedentes penales generalmente no son barrera."
            ),
            notes="Apply online at commonhelp.virginia.gov, call 833-522-5582, or visit the local department of social services.",
            notes_es="Solicite en línea en commonhelp.virginia.gov, llame al 833-522-5582 o visite el departamento local de servicios sociales.",
            hours="Typically Monday–Friday business hours; call ahead",
            tags=f"{served[0].lower()}|virginia|benefits|SNAP|Medicaid|DSS|reentry",
            services="SNAP enrollment|Medicaid application help|TANF cash assistance|Energy assistance|CommonHelp application help",
            county=served[0],
            served_counties="|".join(served),
            coverage="single" if len(served) == 1 else "multi",
            _source=office.get("source", VA_LDSS_LOCATOR),
            _source_type="government",
            _confidence="high" if office.get("address") else "medium",
        )
        existing_fa.update(served)
        added += 1
    return added


SC_DSS_LOCATOR = "https://dss.sc.gov/contact-dss/"


def _sc_desc_en(county: str, city: str) -> str:
    return (
        f"The {county} County Department of Social Services office in {city} processes SNAP, "
        f"Medicaid, TANF, and child care assistance applications for South Carolina residents, "
        f"including returning citizens reestablishing food and health benefits after release from "
        f"jail or South Carolina Department of Corrections custody. County DSS staff help verify "
        f"identity and income and accept applications submitted through the statewide benefits portal."
    )


def _sc_desc_es(county: str, city: str) -> str:
    return (
        f"La oficina del Departamento de Servicios Sociales del condado {county} en {city} procesa "
        f"solicitudes de SNAP, Medicaid, TANF y asistencia de cuidado infantil para residentes de "
        f"Carolina del Sur, incluidos ciudadanos que regresan que restablecen beneficios alimentarios "
        f"y de salud después de salir de la cárcel o de la custodia del Departamento de Correcciones. "
        f"El personal del condado ayuda a verificar identidad e ingresos y acepta solicitudes del portal estatal."
    )


def register_county_benefits_south_carolina(add: Callable[..., None], existing_fa: set[str]) -> int:
    """One financial-assistance row per SCDSS county office (46 counties)."""
    added = 0
    for office in _load_offices("south-carolina-dss-offices.json"):
        county = office["county"]
        if county in existing_fa:
            continue
        city = office.get("city") or county
        region = f"{city} / {county} County"
        source = office.get("source", SC_DSS_LOCATOR)
        add(
            name=f"{county} County DSS — Benefits & Family Support",
            category="financial-assistance",
            region=region,
            description=_sc_desc_en(county, city),
            description_es=_sc_desc_es(county, city),
            address=office.get("address", ""),
            city=city,
            phone=office.get("phone") or "1-800-616-1309",
            email="",
            website=source,
            eligibility=(
                f"{county} County residents meeting income and household-size requirements for SNAP, "
                f"Medicaid, and TANF; criminal record generally not a barrier."
            ),
            eligibility_es=(
                f"Residentes del condado {county} que cumplan requisitos de ingresos y tamaño de hogar "
                f"para SNAP, Medicaid y TANF; los antecedentes penales generalmente no son barrera."
            ),
            notes=(
                "Apply online at benefitsportal.dss.sc.gov or portal.dss.sc.gov; call 1-800-616-1309 "
                "for statewide DSS help; visit the county office for in-person verification."
            ),
            notes_es=(
                "Solicite en benefitsportal.dss.sc.gov o portal.dss.sc.gov; llame al 1-800-616-1309 "
                "para ayuda estatal; visite la oficina del condado para verificación presencial."
            ),
            hours="Typically Monday–Friday business hours; call ahead",
            tags=f"{county.lower()}|south-carolina|benefits|SNAP|Medicaid|DSS|reentry",
            services="SNAP enrollment|Medicaid application help|TANF cash assistance|Child care subsidies|Benefits verification",
            county=county,
            served_counties=county,
            coverage="single",
            _source=source,
            _source_type="government",
            _confidence="high" if office.get("address") else "medium",
        )
        existing_fa.add(county)
        added += 1
    return added


def register_county_benefits_alabama(add: Callable[..., None], existing_fa: set[str]) -> int:
    from phase3b_gapfill import _dhr_desc_en, _dhr_desc_es, _dhr_al

    added = 0
    for office in _load_offices("alabama-dhr-offices.json"):
        county = office["county"]
        if county in existing_fa:
            continue
        city = office.get("city") or county
        region = f"{city} / {county} County"
        source = office.get("source", AL_DHR_LOCATOR)
        add(
            **_dhr_al(
                county,
                city,
                office.get("address", ""),
                office.get("phone", "1-800-410-5827"),
                region,
                _dhr_desc_en(county, city),
                _dhr_desc_es(county, city),
                source,
            )
            | {
                "_confidence": "high" if office.get("address") else "medium",
            }
        )
        existing_fa.add(county)
        added += 1
    return added


def register_county_benefits_north_carolina(add: Callable[..., None], existing_fa: set[str]) -> int:
    from phase3b_gapfill import _dss_desc_en, _dss_desc_es, _dss_nc

    added = 0
    for office in _load_offices("north-carolina-dss-offices.json"):
        county = office["county"]
        if county in existing_fa:
            continue
        city = office.get("city") or county
        region = f"{city} / {county} County"
        source = office.get("source", NC_DSS_LOCATOR)
        add(
            **_dss_nc(
                county,
                city,
                office.get("address", ""),
                office.get("phone", "1-866-719-0141"),
                region,
                _dss_desc_en(county, city),
                _dss_desc_es(county, city),
                source,
            )
            | {
                "_confidence": "high" if office.get("address") else "medium",
            }
        )
        existing_fa.add(county)
        added += 1
    return added


def _des_desc_en(county: str, city: str) -> str:
    return (
        f"The {county} County DES Family Assistance Administration office in {city} processes Nutrition "
        f"Assistance (SNAP), Cash Assistance (TANF), and AHCCCS Medicaid eligibility applications for "
        f"Arizona residents including returning citizens reestablishing food and health benefits after "
        f"release from {county} County Jail or ADCRR custody. County DES staff help verify identity and "
        f"income and accept applications submitted through Health-e-Arizona Plus."
    )


def _des_desc_es(county: str, city: str) -> str:
    return (
        f"La oficina de Administración de Asistencia Familiar de DES del condado {county} en {city} "
        f"procesa solicitudes de Asistencia Nutricional (SNAP), Asistencia en Efectivo (TANF) y "
        f"elegibilidad de Medicaid AHCCCS para residentes de Arizona, incluidos ciudadanos que regresan "
        f"que restablecen beneficios alimentarios y de salud después de salir de la cárcel del condado "
        f"{county} o de la custodia de ADCRR. El personal del condado ayuda a verificar identidad e "
        f"ingresos y acepta solicitudes presentadas a través de Health-e-Arizona Plus."
    )


def register_county_benefits_arizona(add: Callable[..., None], existing_fa: set[str]) -> int:
    """One financial-assistance row per DES county office (15 counties)."""
    added = 0
    for office in _load_offices("arizona-des-offices.json"):
        county = office["county"]
        if county in existing_fa:
            continue
        city = office.get("city") or county
        region = f"{city} / {county} County"
        source = office.get("source", AZ_DES_LOCATOR)
        add(
            name=f"{county} County DES — Benefits & Family Support",
            category="financial-assistance",
            region=region,
            description=_des_desc_en(county, city),
            description_es=_des_desc_es(county, city),
            address=office.get("address", ""),
            city=city,
            phone=office.get("phone") or "1-855-432-7587",
            email="",
            website=source,
            eligibility=(
                f"{county} County residents meeting income and household-size requirements for SNAP, "
                f"TANF, and AHCCCS Medicaid; criminal record generally not a barrier."
            ),
            eligibility_es=(
                f"Residentes del condado {county} que cumplan requisitos de ingresos y tamaño de hogar "
                f"para SNAP, TANF y Medicaid AHCCCS; los antecedentes penales generalmente no son barrera."
            ),
            notes=(
                "Apply online at healthearizonaplus.gov; call 1-855-432-7587 for DES help; "
                "statewide interview line 1-855-777-8590; visit the county office for in-person verification."
            ),
            notes_es=(
                "Solicite en healthearizonaplus.gov; llame al 1-855-432-7587; línea de entrevista estatal "
                "1-855-777-8590; visite la oficina del condado para verificación presencial."
            ),
            hours="Typically Monday–Friday business hours; call ahead",
            tags=f"{county.lower()}|arizona|benefits|SNAP|Medicaid|DES|reentry",
            services="SNAP enrollment|AHCCCS Medicaid application|TANF cash assistance|Document verification|Health-e-Arizona Plus help",
            county=county,
            served_counties=county,
            coverage="single",
            _source=source,
            _source_type="government",
            _confidence="high" if office.get("address") else "medium",
        )
        existing_fa.add(county)
        added += 1
    return added


def _mdhs_desc_en(county: str, city: str) -> str:
    return (
        f"The {county} County MDHS Economic Assistance office in {city} processes SNAP nutrition assistance, "
        f"Temporary Assistance for Needy Families (TANF), and Medicaid application referrals for Mississippi "
        f"residents including returning citizens reestablishing food and health benefits after release from "
        f"{county} County Jail or MDOC custody. County MDHS staff help verify identity and income and accept "
        f"applications submitted through access.ms.gov."
    )


def _mdhs_desc_es(county: str, city: str) -> str:
    return (
        f"La oficina de Asistencia Económica MDHS del condado {county} en {city} procesa asistencia "
        f"nutricional SNAP, Asistencia Temporal para Familias Necesitadas (TANF) y referencias de solicitud "
        f"de Medicaid para residentes de Mississippi, incluidos ciudadanos que regresan que restablecen "
        f"beneficios alimentarios y de salud después de salir de la cárcel del condado {county} o de la "
        f"custodia de MDOC. El personal del condado ayuda a verificar identidad e ingresos y acepta "
        f"solicitudes presentadas a través de access.ms.gov."
    )


def register_county_benefits_mississippi(add: Callable[..., None], existing_fa: set[str]) -> int:
    """One financial-assistance row per MDHS county office (82 counties)."""
    added = 0
    for office in _load_offices("mississippi-mdhs-offices.json"):
        county = office["county"]
        if county in existing_fa:
            continue
        city = office.get("city") or county
        region = f"{city} / {county} County"
        source = office.get("source", MS_MDHS_LOCATOR)
        add(
            name=f"{county} County MDHS — Benefits & Family Support",
            category="financial-assistance",
            region=region,
            description=_mdhs_desc_en(county, city),
            description_es=_mdhs_desc_es(county, city),
            address=office.get("address", ""),
            city=city,
            phone=office.get("phone") or "800-948-3050",
            email="",
            website=source,
            eligibility=(
                f"{county} County residents meeting income and household-size requirements for SNAP, "
                f"TANF, and Medicaid; criminal record generally not a barrier to SNAP."
            ),
            eligibility_es=(
                f"Residentes del condado {county} que cumplan requisitos de ingresos y tamaño de hogar "
                f"para SNAP, TANF y Medicaid; los antecedentes penales generalmente no son barrera para SNAP."
            ),
            notes=(
                "Apply online at access.ms.gov; call 800-948-3050 for SNAP/TANF customer service; "
                "visit the county MDHS office for in-person verification; Medicaid enrollment through DOM."
            ),
            notes_es=(
                "Solicite en access.ms.gov; llame al 800-948-3050; visite la oficina MDHS del condado "
                f"para verificación presencial; inscripción de Medicaid a través de DOM."
            ),
            hours="Typically Monday–Friday business hours; call ahead",
            tags=f"{county.lower().replace(' ', '-')}|mississippi|benefits|SNAP|MDHS|reentry",
            services="SNAP enrollment|TANF application help|Medicaid referral|Document verification|access.ms.gov assistance",
            county=county,
            served_counties=county,
            coverage="single",
            _source=source,
            _source_type="government",
            _confidence="high" if office.get("address") else "medium",
        )
        existing_fa.add(county)
        added += 1
    return added


def _dcf_desc_en(county: str, city: str) -> str:
    return (
        f"The {county} County DCF Family Resource Center / ACCESS intake office in {city} processes "
        f"SNAP food assistance, Temporary Cash Assistance (TCA), and Florida Medicaid eligibility "
        f"applications for residents including returning citizens reestablishing food and health benefits "
        f"after release from {county} County Jail or FDC custody. County DCF staff help verify identity "
        f"and income and accept applications submitted through the MyACCESS Florida portal."
    )


def _dcf_desc_es(county: str, city: str) -> str:
    return (
        f"La oficina de admisión DCF / ACCESS del condado {county} en {city} procesa solicitudes de "
        f"asistencia alimentaria SNAP, Asistencia Temporal en Efectivo (TCA) y elegibilidad de Medicaid "
        f"de Florida para residentes, incluidos ciudadanos que regresan que restablecen beneficios "
        f"alimentarios y de salud después de salir de la cárcel del condado {county} o de custodia FDC. "
        f"El personal del condado ayuda a verificar identidad e ingresos y acepta solicitudes presentadas "
        f"a través del portal MyACCESS Florida."
    )


def register_county_benefits_florida(add: Callable[..., None], existing_fa: set[str]) -> int:
    """One financial-assistance row per DCF county office (67 counties)."""
    added = 0
    for office in _load_offices("florida-dcf-offices.json"):
        county = office["county"]
        if county in existing_fa:
            continue
        city = office.get("city") or county
        region = f"{city} / {county} County"
        source = office.get("source", FL_DCF_LOCATOR)
        add(
            name=f"{county} County DCF — ACCESS Benefits & Family Support",
            category="financial-assistance",
            region=region,
            description=_dcf_desc_en(county, city),
            description_es=_dcf_desc_es(county, city),
            address=office.get("address", ""),
            city=city,
            phone=office.get("phone") or "850-300-4323",
            email="",
            website=source,
            eligibility=(
                f"{county} County residents meeting income and household-size requirements for SNAP, "
                f"TCA, and Florida Medicaid; criminal record generally not a barrier."
            ),
            eligibility_es=(
                f"Residentes del condado {county} que cumplan requisitos de ingresos y tamaño de hogar "
                f"para SNAP, TCA y Medicaid de Florida; los antecedentes penales generalmente no son barrera."
            ),
            notes=(
                "Apply online at myaccess.myflfamilies.com; call 850-300-4323 for DCF Customer Call Center; "
                "visit the county Family Resource Center for in-person verification and document drop-off."
            ),
            notes_es=(
                "Solicite en myaccess.myflfamilies.com; llame al 850-300-4323; visite el Centro de Recursos "
                "Familiares del condado para verificación presencial y entrega de documentos."
            ),
            hours="Typically Monday–Friday business hours; call ahead",
            tags=f"{county.lower().replace('.', '').replace(' ', '-')}|florida|benefits|SNAP|Medicaid|DCF|ACCESS|reentry",
            services="SNAP enrollment|Florida Medicaid application|TCA cash assistance|Document verification|MyACCESS portal help",
            county=county,
            served_counties=county,
            coverage="single",
            _source=source,
            _source_type="government",
            _confidence="high" if office.get("address") else "medium",
        )
        existing_fa.add(county)
        added += 1
    return added


def _wi_em_desc_en(county: str, city: str) -> str:
    return (
        f"The {county} County DHS Eligibility Management office in {city} processes FoodShare (SNAP) "
        f"nutrition assistance, Wisconsin Works (W-2) cash benefits, and BadgerCare Plus Medicaid "
        f"applications for Wisconsin residents including returning citizens reestablishing food and health "
        f"benefits after release from {county} County Jail or WDOC custody. County DHS EM staff help verify "
        f"identity and income and accept applications submitted through ACCESS Wisconsin at access.wi.gov."
    )


def _wi_em_desc_es(county: str, city: str) -> str:
    return (
        f"La oficina de Gestión de Elegibilidad DHS del condado {county} en {city} procesa asistencia "
        f"nutricional FoodShare (SNAP), beneficios en efectivo Wisconsin Works (W-2) y solicitudes de "
        f"Medicaid BadgerCare Plus para residentes de Wisconsin, incluidos ciudadanos que regresan que "
        f"restablecen beneficios alimentarios y de salud después de salir de la cárcel del condado {county} "
        f"o de la custodia de WDOC. El personal DHS EM del condado ayuda a verificar identidad e ingresos "
        f"y acepta solicitudes presentadas a través de ACCESS Wisconsin en access.wi.gov."
    )


def register_county_benefits_wisconsin(add: Callable[..., None], existing_fa: set[str]) -> int:
    """One financial-assistance row per DHS EM county office (72 counties)."""
    added = 0
    for office in _load_offices("wisconsin-dhs-offices.json"):
        county = office["county"]
        if county in existing_fa:
            continue
        city = office.get("city") or county
        region = f"{city} / {county} County"
        source = office.get("source", WI_EM_LOCATOR)
        add(
            name=f"{county} County DHS — ACCESS Wisconsin Benefits",
            category="financial-assistance",
            region=region,
            description=_wi_em_desc_en(county, city),
            description_es=_wi_em_desc_es(county, city),
            address=office.get("address", ""),
            city=city,
            phone=office.get("phone") or "1-800-362-3002",
            email="",
            website=office.get("website") or WI_ACCESS,
            eligibility=(
                f"{county} County residents meeting income and household-size requirements for FoodShare, "
                f"W-2, and BadgerCare Plus; criminal record generally not a barrier to FoodShare."
            ),
            eligibility_es=(
                f"Residentes del condado {county} que cumplan requisitos de ingresos y tamaño de hogar "
                f"para FoodShare, W-2 y BadgerCare Plus; los antecedentes penales generalmente no son "
                f"barrera para FoodShare."
            ),
            notes=(
                "Apply online at access.wi.gov; call 1-800-362-3002 for ACCESS customer service; "
                "visit the county DHS EM office for in-person verification."
            ),
            notes_es=(
                "Solicite en access.wi.gov; llame al 1-800-362-3002; visite la oficina DHS EM del condado "
                f"para verificación presencial."
            ),
            hours="Typically Monday–Friday business hours; call ahead",
            tags=f"{county.lower().replace(' ', '-')}|wisconsin|benefits|FoodShare|ACCESS|reentry",
            services="FoodShare enrollment|W-2 application help|BadgerCare Plus referral|Document verification|ACCESS Wisconsin assistance",
            county=county,
            served_counties=county,
            coverage="single",
            _source=source,
            _source_type="government",
            _confidence="high",
        )
        existing_fa.add(county)
        added += 1
    return added


def _tx_hhsc_desc_en(county: str, city: str) -> str:
    return (
        f"The {county} County HHSC benefits office helps residents apply for and manage SNAP food assistance, "
        f"TANF cash benefits, and Medicaid through Your Texas Benefits. Justice-involved Texans can restore "
        f"food and health coverage after release from TDCJ custody or {county} County Jail using the same "
        f"Your Texas Benefits account used statewide. Staff at the {city} service area assist with identity "
        f"verification, document upload, and renewal—not emergency cash on demand."
    )


def _tx_hhsc_desc_es(county: str, city: str) -> str:
    return (
        f"La oficina de beneficios HHSC del condado {county} ayuda a residentes a solicitar y administrar "
        f"asistencia alimentaria SNAP, beneficios en efectivo TANF y Medicaid a través de Your Texas Benefits. "
        f"Los texanos en reinserción pueden restablecer cobertura alimentaria y de salud después de salir de "
        f"la custodia de TDCJ o la cárcel del condado {county}. El personal del área de servicio de {city} "
        f"ayuda con verificación de identidad y documentos."
    )


def register_county_benefits_texas(add: Callable[..., None], existing_fa: set[str]) -> int:
    """One financial-assistance row per HHSC county office (254 counties)."""
    added = 0
    for office in _load_offices("texas-hhsc-offices.json"):
        county = office["county"]
        if county in existing_fa:
            continue
        city = office.get("city") or county
        region = f"{city} / {county} County"
        source = office.get("source", TX_HHSC_SNAP)
        add(
            name=f"{county} County HHSC — Your Texas Benefits",
            category="financial-assistance",
            region=region,
            description=_tx_hhsc_desc_en(county, city),
            description_es=_tx_hhsc_desc_es(county, city),
            address=office.get("address", ""),
            city=city,
            phone=office.get("phone") or "877-541-7905",
            email="",
            website=office.get("website") or TX_YTB,
            eligibility=(
                f"{county} County residents meeting income and household-size requirements for SNAP, "
                f"TANF, and Medicaid; criminal record generally not a barrier to SNAP."
            ),
            eligibility_es=(
                f"Residentes del condado {county} que cumplan requisitos de ingresos y tamaño de hogar "
                f"para SNAP, TANF y Medicaid; los antecedentes penales generalmente no son barrera para SNAP."
            ),
            notes=(
                "Apply online at yourtexasbenefits.com; call 877-541-7905 for Your Texas Benefits customer "
                "service; visit the county HHSC office for in-person verification when required."
            ),
            notes_es=(
                "Solicite en yourtexasbenefits.com; llame al 877-541-7905; visite la oficina HHSC del "
                f"condado para verificación presencial cuando sea necesario."
            ),
            hours="Typically Monday–Friday business hours; call ahead",
            tags=f"{county.lower().replace(' ', '-')}|texas|benefits|SNAP|Medicaid|Your-Texas-Benefits|reentry",
            services="SNAP enrollment|TANF application help|Medicaid referral|Document verification|Your Texas Benefits assistance",
            county=county,
            served_counties=county,
            coverage="single",
            _source=source,
            _source_type="government",
            _confidence="high",
        )
        existing_fa.add(county)
        added += 1
    return added

