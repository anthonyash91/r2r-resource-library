#!/usr/bin/env python3
"""Generate texas-resources.csv and texas-research-log.csv.

RESOURCES_UUID_PREFIX comment e1000001
"""
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES_PATH = ROOT / "data" / "texas-resources.csv"
LOG_PATH = ROOT / "data" / "texas-research-log.csv"
DATE = "2026-07-08"

COLUMNS = [
    "id", "name", "category", "region", "description", "description_es",
    "address", "city", "phone", "email", "website", "eligibility", "eligibility_es",
    "notes", "notes_es", "hours", "tags", "services", "county", "served_counties", "coverage",
]
LOG_COLUMNS = ["source_url", "source_type", "date_accessed", "confidence", "notes", "id_reference"]

ENTRIES = []


def add(**kw):
    ENTRIES.append(kw)


# --- Phase 1: Statewide backbone ---

add(
    name="TDCJ — Reentry & Release Programs",
    category="state-agency", region="Statewide",
    description="TDCJ — Reentry & Release Programs connects justice-involved Texans across all 254 counties to reentry supports including Your Texas Benefits, Workforce Solutions, Medicaid, and local housing and treatment partners before and after release from TDCJ custody or county jails. This resource provides planning, referrals, and navigation—not emergency cash or walk-in crisis shelter unless noted.",
    description_es="TDCJ — Reentry & Release Programs conecta a texanos con antecedentes penales en los 254 condados con apoyos de reinserción incluidos Your Texas Benefits, Workforce Solutions, Medicaid y aliados locales de vivienda y tratamiento antes y después de la liberación de custodia TDCJ o cárceles del condado.",
    address="8712 Shoal Creek Boulevard", city="Huntsville", phone="936-437-2848", email="",
    website="https://www.tdcj.texas.gov/divisions/rrd/reentry_program.html",
    eligibility="Texas residents and justice-involved individuals; specific program eligibility varies; contact for intake.",
    eligibility_es="Residentes de Texas y personas con antecedentes penales; la elegibilidad específica del programa varía; contacte para admisión.",
    notes="Verify current hours and intake requirements on the official website before visiting in person.",
    notes_es="Verifique horarios actuales y requisitos de admisión en el sitio web oficial antes de visitar en persona.",
    hours="Hours vary; check official website",
    tags="statewide|reentry|TDCJ|pre-release|community-supervision",
    services="Pre-release planning|Reentry resource navigation|Community partner referrals|Release coordination|Supervision linkage",
    county="Walker", served_counties="", coverage="statewide",
    _source="https://www.tdcj.texas.gov/divisions/rrd/reentry_program.html", _source_type="government", _confidence="high",
)

add(
    name="TDCJ — Parole Division",
    category="probation-parole", region="Statewide",
    description="TDCJ — Parole Division connects justice-involved Texans across all 254 counties to reentry supports including Your Texas Benefits, Workforce Solutions, Medicaid, and local housing and treatment partners before and after release from TDCJ custody or county jails. This resource provides planning, referrals, and navigation—not emergency cash or walk-in crisis shelter unless noted.",
    description_es="TDCJ — Parole Division conecta a texanos con antecedentes penales en los 254 condados con apoyos de reinserción incluidos Your Texas Benefits, Workforce Solutions, Medicaid y aliados locales de vivienda y tratamiento antes y después de la liberación de custodia TDCJ o cárceles del condado.",
    address="8712 Shoal Creek Boulevard", city="Austin", phone="512-406-5202", email="",
    website="https://www.tdcj.texas.gov/divisions/pd/index.html",
    eligibility="Texas residents and justice-involved individuals; specific program eligibility varies; contact for intake.",
    eligibility_es="Residentes de Texas y personas con antecedentes penales; la elegibilidad específica del programa varía; contacte para admisión.",
    notes="Verify current hours and intake requirements on the official website before visiting in person.",
    notes_es="Verifique horarios actuales y requisitos de admisión en el sitio web oficial antes de visitar en persona.",
    hours="Hours vary; check official website",
    tags="statewide|probation-parole|TDCJ|parole|mandatory-supervision",
    services="Parole supervision|Mandatory supervision reporting|Treatment referrals|Employment compliance|Reentry partner coordination",
    county="Travis", served_counties="", coverage="statewide",
    _source="https://www.tdcj.texas.gov/divisions/pd/index.html", _source_type="government", _confidence="high",
)

add(
    name="Your Texas Benefits",
    category="financial-assistance", region="Statewide",
    description="Your Texas Benefits connects justice-involved Texans across all 254 counties to reentry supports including Your Texas Benefits, Workforce Solutions, Medicaid, and local housing and treatment partners before and after release from TDCJ custody or county jails. This resource provides planning, referrals, and navigation—not emergency cash or walk-in crisis shelter unless noted.",
    description_es="Your Texas Benefits conecta a texanos con antecedentes penales en los 254 condados con apoyos de reinserción incluidos Your Texas Benefits, Workforce Solutions, Medicaid y aliados locales de vivienda y tratamiento antes y después de la liberación de custodia TDCJ o cárceles del condado.",
    address="", city="", phone="877-541-7905", email="",
    website="https://yourtexasbenefits.com",
    eligibility="Texas residents and justice-involved individuals; specific program eligibility varies; contact for intake.",
    eligibility_es="Residentes de Texas y personas con antecedentes penales; la elegibilidad específica del programa varía; contacte para admisión.",
    notes="Verify current hours and intake requirements on the official website before visiting in person.",
    notes_es="Verifique horarios actuales y requisitos de admisión en el sitio web oficial antes de visitar en persona.",
    hours="Hours vary; check official website",
    tags="statewide|benefits|SNAP|Medicaid|TANF|reentry",
    services="SNAP enrollment|Medicaid application|TANF application|CHIP enrollment|Benefits renewal",
    county="", served_counties="", coverage="statewide",
    _source="https://yourtexasbenefits.com", _source_type="government", _confidence="high",
)

add(
    name="Texas Medicaid & CHIP",
    category="healthcare", region="Statewide",
    description="Texas Medicaid & CHIP connects justice-involved Texans across all 254 counties to reentry supports including Your Texas Benefits, Workforce Solutions, Medicaid, and local housing and treatment partners before and after release from TDCJ custody or county jails. This resource provides planning, referrals, and navigation—not emergency cash or walk-in crisis shelter unless noted.",
    description_es="Texas Medicaid & CHIP conecta a texanos con antecedentes penales en los 254 condados con apoyos de reinserción incluidos Your Texas Benefits, Workforce Solutions, Medicaid y aliados locales de vivienda y tratamiento antes y después de la liberación de custodia TDCJ o cárceles del condado.",
    address="", city="Austin", phone="800-925-9126", email="",
    website="https://www.hhs.texas.gov/services/health/medicaid-chip",
    eligibility="Texas residents and justice-involved individuals; specific program eligibility varies; contact for intake.",
    eligibility_es="Residentes de Texas y personas con antecedentes penales; la elegibilidad específica del programa varía; contacte para admisión.",
    notes="Verify current hours and intake requirements on the official website before visiting in person.",
    notes_es="Verifique horarios actuales y requisitos de admisión en el sitio web oficial antes de visitar en persona.",
    hours="Hours vary; check official website",
    tags="statewide|healthcare|Medicaid|CHIP|reentry",
    services="Medicaid enrollment|CHIP application|Managed care navigation|Member services|Eligibility determination",
    county="Travis", served_counties="", coverage="statewide",
    _source="https://www.hhs.texas.gov/services/health/medicaid-chip", _source_type="government", _confidence="high",
)

add(
    name="211 Texas",
    category="state-agency", region="Statewide",
    description="211 Texas connects justice-involved Texans across all 254 counties to reentry supports including Your Texas Benefits, Workforce Solutions, Medicaid, and local housing and treatment partners before and after release from TDCJ custody or county jails. This resource provides planning, referrals, and navigation—not emergency cash or walk-in crisis shelter unless noted.",
    description_es="211 Texas conecta a texanos con antecedentes penales en los 254 condados con apoyos de reinserción incluidos Your Texas Benefits, Workforce Solutions, Medicaid y aliados locales de vivienda y tratamiento antes y después de la liberación de custodia TDCJ o cárceles del condado.",
    address="", city="", phone="211", email="",
    website="https://www.211texas.org",
    eligibility="Texas residents and justice-involved individuals; specific program eligibility varies; contact for intake.",
    eligibility_es="Residentes de Texas y personas con antecedentes penales; la elegibilidad específica del programa varía; contacte para admisión.",
    notes="Verify current hours and intake requirements on the official website before visiting in person.",
    notes_es="Verifique horarios actuales y requisitos de admisión en el sitio web oficial antes de visitar en persona.",
    hours="Hours vary; check official website",
    tags="statewide|hotline|211|referral-only|basic-needs",
    services="Information and referral|Housing resource navigation|Benefits referrals|Crisis resource connections|Local program search",
    county="", served_counties="", coverage="statewide",
    _source="https://www.211texas.org", _source_type="government", _confidence="high",
)

add(
    name="Texas Law Help",
    category="legal-aid", region="Statewide",
    description="Texas Law Help connects justice-involved Texans across all 254 counties to reentry supports including Your Texas Benefits, Workforce Solutions, Medicaid, and local housing and treatment partners before and after release from TDCJ custody or county jails. This resource provides planning, referrals, and navigation—not emergency cash or walk-in crisis shelter unless noted.",
    description_es="Texas Law Help conecta a texanos con antecedentes penales en los 254 condados con apoyos de reinserción incluidos Your Texas Benefits, Workforce Solutions, Medicaid y aliados locales de vivienda y tratamiento antes y después de la liberación de custodia TDCJ o cárceles del condado.",
    address="", city="Austin", phone="", email="",
    website="https://texaslawhelp.org",
    eligibility="Texas residents and justice-involved individuals; specific program eligibility varies; contact for intake.",
    eligibility_es="Residentes de Texas y personas con antecedentes penales; la elegibilidad específica del programa varía; contacte para admisión.",
    notes="Verify current hours and intake requirements on the official website before visiting in person.",
    notes_es="Verifique horarios actuales y requisitos de admisión en el sitio web oficial antes de visitar en persona.",
    hours="Hours vary; check official website",
    tags="statewide|legal-aid|online|expungement|reentry",
    services="Legal information|Expungement guidance|Housing legal resources|Benefits advocacy tools|Regional legal aid referrals",
    county="Travis", served_counties="", coverage="statewide",
    _source="https://texaslawhelp.org", _source_type="government", _confidence="high",
)

add(
    name="Lone Star Legal Aid — Statewide Intake",
    category="legal-aid", region="Statewide",
    description="Lone Star Legal Aid — Statewide Intake connects justice-involved Texans across all 254 counties to reentry supports including Your Texas Benefits, Workforce Solutions, Medicaid, and local housing and treatment partners before and after release from TDCJ custody or county jails. This resource provides planning, referrals, and navigation—not emergency cash or walk-in crisis shelter unless noted.",
    description_es="Lone Star Legal Aid — Statewide Intake conecta a texanos con antecedentes penales en los 254 condados con apoyos de reinserción incluidos Your Texas Benefits, Workforce Solutions, Medicaid y aliados locales de vivienda y tratamiento antes y después de la liberación de custodia TDCJ o cárceles del condado.",
    address="1414 Austin Street", city="Houston", phone="713-652-0077", email="",
    website="https://www.lonestarlegal.org",
    eligibility="Texas residents and justice-involved individuals; specific program eligibility varies; contact for intake.",
    eligibility_es="Residentes de Texas y personas con antecedentes penales; la elegibilidad específica del programa varía; contacte para admisión.",
    notes="Verify current hours and intake requirements on the official website before visiting in person.",
    notes_es="Verifique horarios actuales y requisitos de admisión en el sitio web oficial antes de visitar en persona.",
    hours="Hours vary; check official website",
    tags="statewide|legal-aid|low-income|housing|benefits",
    services="Civil legal representation|Housing legal aid|Benefits advocacy|Family law assistance|Regional office referrals",
    county="Harris", served_counties="", coverage="statewide",
    _source="https://www.lonestarlegal.org", _source_type="government", _confidence="high",
)

add(
    name="Texas RioGrande Legal Aid",
    category="legal-aid", region="Statewide",
    description="Texas RioGrande Legal Aid connects justice-involved Texans across all 254 counties to reentry supports including Your Texas Benefits, Workforce Solutions, Medicaid, and local housing and treatment partners before and after release from TDCJ custody or county jails. This resource provides planning, referrals, and navigation—not emergency cash or walk-in crisis shelter unless noted.",
    description_es="Texas RioGrande Legal Aid conecta a texanos con antecedentes penales en los 254 condados con apoyos de reinserción incluidos Your Texas Benefits, Workforce Solutions, Medicaid y aliados locales de vivienda y tratamiento antes y después de la liberación de custodia TDCJ o cárceles del condado.",
    address="1111 N Main Avenue", city="San Antonio", phone="888-988-9996", email="",
    website="https://www.trla.org",
    eligibility="Texas residents and justice-involved individuals; specific program eligibility varies; contact for intake.",
    eligibility_es="Residentes de Texas y personas con antecedentes penales; la elegibilidad específica del programa varía; contacte para admisión.",
    notes="Verify current hours and intake requirements on the official website before visiting in person.",
    notes_es="Verifique horarios actuales y requisitos de admisión en el sitio web oficial antes de visitar en persona.",
    hours="Hours vary; check official website",
    tags="statewide|legal-aid|south-texas|border|reentry",
    services="Civil legal representation|Housing legal aid|Benefits advocacy|Immigration legal resources|Record relief guidance",
    county="Bexar", served_counties="", coverage="statewide",
    _source="https://www.trla.org", _source_type="government", _confidence="high",
)

add(
    name="Texas Workforce Commission — Find Work",
    category="employment", region="Statewide",
    description="Texas Workforce Commission — Find Work connects justice-involved Texans across all 254 counties to reentry supports including Your Texas Benefits, Workforce Solutions, Medicaid, and local housing and treatment partners before and after release from TDCJ custody or county jails. This resource provides planning, referrals, and navigation—not emergency cash or walk-in crisis shelter unless noted.",
    description_es="Texas Workforce Commission — Find Work conecta a texanos con antecedentes penales en los 254 condados con apoyos de reinserción incluidos Your Texas Benefits, Workforce Solutions, Medicaid y aliados locales de vivienda y tratamiento antes y después de la liberación de custodia TDCJ o cárceles del condado.",
    address="101 East 15th Street", city="Austin", phone="800-628-5115", email="",
    website="https://www.twc.texas.gov/jobseekers/find-work",
    eligibility="Texas residents and justice-involved individuals; specific program eligibility varies; contact for intake.",
    eligibility_es="Residentes de Texas y personas con antecedentes penales; la elegibilidad específica del programa varía; contacte para admisión.",
    notes="Verify current hours and intake requirements on the official website before visiting in person.",
    notes_es="Verifique horarios actuales y requisitos de admisión en el sitio web oficial antes de visitar en persona.",
    hours="Hours vary; check official website",
    tags="statewide|employment|workforce-solutions|WIOA|fair-chance",
    services="Job search tools|Workforce Solutions office locator|Career coaching referrals|WIOA training navigation|Fair-chance employment resources",
    county="Travis", served_counties="", coverage="statewide",
    _source="https://www.twc.texas.gov/jobseekers/find-work", _source_type="government", _confidence="high",
)

add(
    name="Texas Veterans Commission",
    category="veterans", region="Statewide",
    description="Texas Veterans Commission connects justice-involved Texans across all 254 counties to reentry supports including Your Texas Benefits, Workforce Solutions, Medicaid, and local housing and treatment partners before and after release from TDCJ custody or county jails. This resource provides planning, referrals, and navigation—not emergency cash or walk-in crisis shelter unless noted.",
    description_es="Texas Veterans Commission conecta a texanos con antecedentes penales en los 254 condados con apoyos de reinserción incluidos Your Texas Benefits, Workforce Solutions, Medicaid y aliados locales de vivienda y tratamiento antes y después de la liberación de custodia TDCJ o cárceles del condado.",
    address="1700 North Congress Avenue", city="Austin", phone="800-252-8387", email="",
    website="https://www.tvc.texas.gov",
    eligibility="Texas residents and justice-involved individuals; specific program eligibility varies; contact for intake.",
    eligibility_es="Residentes de Texas y personas con antecedentes penales; la elegibilidad específica del programa varía; contacte para admisión.",
    notes="Verify current hours and intake requirements on the official website before visiting in person.",
    notes_es="Verifique horarios actuales y requisitos de admisión en el sitio web oficial antes de visitar en persona.",
    hours="Hours vary; check official website",
    tags="statewide|veterans|VA-benefits|reentry|justice-involved-veterans",
    services="VA benefits claims assistance|Disability claims navigation|Education benefits guidance|Veterans treatment court support|County VSO referrals",
    county="Travis", served_counties="", coverage="statewide",
    _source="https://www.tvc.texas.gov", _source_type="government", _confidence="high",
)

add(
    name="Texas DPS — Driver License & ID",
    category="id-documentation", region="Statewide",
    description="Texas DPS — Driver License & ID connects justice-involved Texans across all 254 counties to reentry supports including Your Texas Benefits, Workforce Solutions, Medicaid, and local housing and treatment partners before and after release from TDCJ custody or county jails. This resource provides planning, referrals, and navigation—not emergency cash or walk-in crisis shelter unless noted.",
    description_es="Texas DPS — Driver License & ID conecta a texanos con antecedentes penales en los 254 condados con apoyos de reinserción incluidos Your Texas Benefits, Workforce Solutions, Medicaid y aliados locales de vivienda y tratamiento antes y después de la liberación de custodia TDCJ o cárceles del condado.",
    address="", city="Austin", phone="512-424-2600", email="",
    website="https://www.dps.texas.gov/section/driver-license",
    eligibility="Texas residents and justice-involved individuals; specific program eligibility varies; contact for intake.",
    eligibility_es="Residentes de Texas y personas con antecedentes penales; la elegibilidad específica del programa varía; contacte para admisión.",
    notes="Verify current hours and intake requirements on the official website before visiting in person.",
    notes_es="Verifique horarios actuales y requisitos de admisión en el sitio web oficial antes de visitar en persona.",
    hours="Hours vary; check official website",
    tags="statewide|id-documentation|DPS|drivers-license|state-id|reentry",
    services="State ID card issuance|Driver's license services|ID renewal|DPS office locator|Identification documentation guidance",
    county="Travis", served_counties="", coverage="statewide",
    _source="https://www.dps.texas.gov/section/driver-license", _source_type="government", _confidence="high",
)

add(
    name="Texas Vital Records",
    category="id-documentation", region="Statewide",
    description="Texas Vital Records connects justice-involved Texans across all 254 counties to reentry supports including Your Texas Benefits, Workforce Solutions, Medicaid, and local housing and treatment partners before and after release from TDCJ custody or county jails. This resource provides planning, referrals, and navigation—not emergency cash or walk-in crisis shelter unless noted.",
    description_es="Texas Vital Records conecta a texanos con antecedentes penales en los 254 condados con apoyos de reinserción incluidos Your Texas Benefits, Workforce Solutions, Medicaid y aliados locales de vivienda y tratamiento antes y después de la liberación de custodia TDCJ o cárceles del condado.",
    address="", city="Austin", phone="888-963-7111", email="",
    website="https://www.dshs.texas.gov/vital-statistics",
    eligibility="Texas residents and justice-involved individuals; specific program eligibility varies; contact for intake.",
    eligibility_es="Residentes de Texas y personas con antecedentes penales; la elegibilidad específica del programa varía; contacte para admisión.",
    notes="Verify current hours and intake requirements on the official website before visiting in person.",
    notes_es="Verifique horarios actuales y requisitos de admisión en el sitio web oficial antes de visitar en persona.",
    hours="Hours vary; check official website",
    tags="statewide|id-documentation|vital-records|birth-certificate|reentry",
    services="Birth certificate issuance|Death certificate issuance|Marriage record copies|Online ordering|In-person vital records service",
    county="Travis", served_counties="", coverage="statewide",
    _source="https://www.dshs.texas.gov/vital-statistics", _source_type="government", _confidence="high",
)

add(
    name="988 Suicide & Crisis Lifeline — Texas",
    category="healthcare", region="Statewide",
    description="988 Suicide & Crisis Lifeline — Texas connects justice-involved Texans across all 254 counties to reentry supports including Your Texas Benefits, Workforce Solutions, Medicaid, and local housing and treatment partners before and after release from TDCJ custody or county jails. This resource provides planning, referrals, and navigation—not emergency cash or walk-in crisis shelter unless noted.",
    description_es="988 Suicide & Crisis Lifeline — Texas conecta a texanos con antecedentes penales en los 254 condados con apoyos de reinserción incluidos Your Texas Benefits, Workforce Solutions, Medicaid y aliados locales de vivienda y tratamiento antes y después de la liberación de custodia TDCJ o cárceles del condado.",
    address="", city="", phone="988", email="",
    website="https://988lifeline.org",
    eligibility="Texas residents and justice-involved individuals; specific program eligibility varies; contact for intake.",
    eligibility_es="Residentes de Texas y personas con antecedentes penales; la elegibilidad específica del programa varía; contacte para admisión.",
    notes="Verify current hours and intake requirements on the official website before visiting in person.",
    notes_es="Verifique horarios actuales y requisitos de admisión en el sitio web oficial antes de visitar en persona.",
    hours="Hours vary; check official website",
    tags="statewide|hotline|crisis|mental-health|988",
    services="Crisis counseling|Suicide prevention support|Mental health referrals|Substance use crisis support",
    county="", served_counties="", coverage="statewide",
    _source="https://988lifeline.org", _source_type="government", _confidence="high",
)

add(
    name="SAMHSA National Helpline",
    category="substance-use-treatment", region="Statewide",
    description="SAMHSA National Helpline connects justice-involved Texans across all 254 counties to reentry supports including Your Texas Benefits, Workforce Solutions, Medicaid, and local housing and treatment partners before and after release from TDCJ custody or county jails. This resource provides planning, referrals, and navigation—not emergency cash or walk-in crisis shelter unless noted.",
    description_es="SAMHSA National Helpline conecta a texanos con antecedentes penales en los 254 condados con apoyos de reinserción incluidos Your Texas Benefits, Workforce Solutions, Medicaid y aliados locales de vivienda y tratamiento antes y después de la liberación de custodia TDCJ o cárceles del condado.",
    address="", city="", phone="800-662-4357", email="",
    website="https://www.samhsa.gov/find-help/national-helpline",
    eligibility="Texas residents and justice-involved individuals; specific program eligibility varies; contact for intake.",
    eligibility_es="Residentes de Texas y personas con antecedentes penales; la elegibilidad específica del programa varía; contacte para admisión.",
    notes="Verify current hours and intake requirements on the official website before visiting in person.",
    notes_es="Verifique horarios actuales y requisitos de admisión en el sitio web oficial antes de visitar en persona.",
    hours="Hours vary; check official website",
    tags="statewide|hotline|substance-use|treatment-referral|national",
    services="Treatment referrals|Substance use information|Mental health resource navigation",
    county="", served_counties="", coverage="statewide",
    _source="https://www.samhsa.gov/find-help/national-helpline", _source_type="government", _confidence="high",
)

add(
    name="FindTreatment.gov — Texas Provider Search",
    category="substance-use-treatment", region="Statewide",
    description="FindTreatment.gov — Texas Provider Search connects justice-involved Texans across all 254 counties to reentry supports including Your Texas Benefits, Workforce Solutions, Medicaid, and local housing and treatment partners before and after release from TDCJ custody or county jails. This resource provides planning, referrals, and navigation—not emergency cash or walk-in crisis shelter unless noted.",
    description_es="FindTreatment.gov — Texas Provider Search conecta a texanos con antecedentes penales en los 254 condados con apoyos de reinserción incluidos Your Texas Benefits, Workforce Solutions, Medicaid y aliados locales de vivienda y tratamiento antes y después de la liberación de custodia TDCJ o cárceles del condado.",
    address="", city="", phone="", email="",
    website="https://findtreatment.gov",
    eligibility="Texas residents and justice-involved individuals; specific program eligibility varies; contact for intake.",
    eligibility_es="Residentes de Texas y personas con antecedentes penales; la elegibilidad específica del programa varía; contacte para admisión.",
    notes="Verify current hours and intake requirements on the official website before visiting in person.",
    notes_es="Verifique horarios actuales y requisitos de admisión en el sitio web oficial antes de visitar en persona.",
    hours="Hours vary; check official website",
    tags="statewide|substance-use|online|MAT|treatment-locator",
    services="Treatment provider search|MAT locator|Outpatient program finder|Residential program finder",
    county="", served_counties="", coverage="statewide",
    _source="https://findtreatment.gov", _source_type="government", _confidence="high",
)

add(
    name="TDCJ Reentry Hotline",
    category="state-agency", region="Statewide",
    description="TDCJ Reentry Hotline connects justice-involved Texans across all 254 counties to reentry supports including Your Texas Benefits, Workforce Solutions, Medicaid, and local housing and treatment partners before and after release from TDCJ custody or county jails. This resource provides planning, referrals, and navigation—not emergency cash or walk-in crisis shelter unless noted.",
    description_es="TDCJ Reentry Hotline conecta a texanos con antecedentes penales en los 254 condados con apoyos de reinserción incluidos Your Texas Benefits, Workforce Solutions, Medicaid y aliados locales de vivienda y tratamiento antes y después de la liberación de custodia TDCJ o cárceles del condado.",
    address="", city="", phone="877-887-6151", email="",
    website="https://www.tdcj.texas.gov/divisions/rrd/reentry_program.html",
    eligibility="Texas residents and justice-involved individuals; specific program eligibility varies; contact for intake.",
    eligibility_es="Residentes de Texas y personas con antecedentes penales; la elegibilidad específica del programa varía; contacte para admisión.",
    notes="Verify current hours and intake requirements on the official website before visiting in person.",
    notes_es="Verifique horarios actuales y requisitos de admisión en el sitio web oficial antes de visitar en persona.",
    hours="Hours vary; check official website",
    tags="statewide|hotline|reentry|TDCJ|referral-only",
    services="Reentry information|Resource referrals|Release planning guidance|Community partner connections",
    county="", served_counties="", coverage="statewide",
    _source="https://www.tdcj.texas.gov/divisions/rrd/reentry_program.html", _source_type="government", _confidence="high",
)


# --- County benefits + expansion modules ---
from county_benefits_registry import register_county_benefits_texas

_existing_fa = {
    e["county"]
    for e in ENTRIES
    if e["category"] == "financial-assistance" and e.get("county")
}
register_county_benefits_texas(add, _existing_fa)

from texas_phase4_expansion import register_phase4
register_phase4(add)

from texas_category_fill import register_category_fill
register_category_fill(add)

from texas_mechanical_depth import register_mechanical_depth
register_mechanical_depth(add)

from texas_gap_fill import register_gap_fill
register_gap_fill(add)


def _dedupe_entries(entries: list[dict]) -> list[dict]:
    best: dict[tuple[str, str], dict] = {}
    order: list[tuple[str, str]] = []
    for entry in entries:
        key = (entry["name"].strip().lower(), (entry.get("county") or "").strip().lower())
        if key not in best:
            best[key] = entry
            order.append(key)
            continue
        cur = best[key]
        cur_n = len([c for c in (cur.get("served_counties") or "").split("|") if c.strip()])
        new_n = len([c for c in (entry.get("served_counties") or "").split("|") if c.strip()])
        cur_addr = len(cur.get("address") or "")
        new_addr = len(entry.get("address") or "")
        if new_n > cur_n or (new_n == cur_n and new_addr > cur_addr):
            best[key] = entry
    return [best[k] for k in order]


ENTRIES = _dedupe_entries(ENTRIES)

for entry in ENTRIES:
    if entry.get("coverage") == "single" and not entry.get("served_counties") and entry.get("county"):
        entry["served_counties"] = entry["county"]

log_rows = []
for i, e in enumerate(ENTRIES, start=1):
    e["id"] = str(i)
    log_rows.append({
        "source_url": e.pop("_source"),
        "source_type": e.pop("_source_type"),
        "date_accessed": DATE,
        "confidence": e.pop("_confidence"),
        "notes": f"Resource id {i}: {e['name']}",
        "id_reference": str(i),
    })

with RESOURCES_PATH.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=COLUMNS, quoting=csv.QUOTE_MINIMAL)
    w.writeheader()
    for e in ENTRIES:
        row = {c: e.get(c, "") for c in COLUMNS}
        w.writerow(row)

with LOG_PATH.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=LOG_COLUMNS, quoting=csv.QUOTE_MINIMAL)
    w.writeheader()
    w.writerows(log_rows)

cats = Counter(e["category"] for e in ENTRIES)
low = [e for e in log_rows if e["confidence"] == "medium"]
print(f"Total rows: {len(ENTRIES)}")
print("Category counts:")
for k, v in sorted(cats.items()):
    print(f"  {k}: {v}")
print(f"Low confidence: {len(low)}")
