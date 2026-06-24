#!/usr/bin/env python3
"""Append Tier A weak-county research log entries for Ohio and Tennessee.

Documents systematic search per docs/coverage-policy.md when a county remains
below 3 Tier A core categories after gap-fill. Distinguishes:
  - MECHANICAL ROW: county benefits office exists in every county — use sync-county-benefits-offices.py
    + county_benefits_registry.py; do NOT log as GAP
  - BACKLOG: verifiable provider exists; CSV row deferred pending primary-source contact
  - GAP: no published local/regional direct-service provider found after search

Usage: python3 scripts/append-tier-a-research-gaps.py
"""

from __future__ import annotations

import csv
from pathlib import Path

DATE = "2026-06-23"
ROOT = Path(__file__).resolve().parent.parent

SEARCH_OH = (
    "Searches: Ohio 211 (211.org/get-help/ohio); ODJFS local agencies directory; "
    "ODRC Adult Parole Authority regions; OhioMeansJobs/AJC; regional Feeding America "
    "food banks; HRSA findahealthcenter.hrsa.gov + ohiochc.org; regional legal aid orgs."
)
SEARCH_TN = (
    "Searches: TN 211 (uwtn.org/tn-211); TDHS Family Assistance office locator (tn.gov/humanservices); "
    "TDOC field office directory; tn.gov workforce AJC/LWDB map; regional food banks "
    "(Second Harvest ETN, Mid-South, Chattanooga Area); LAET/LASMT/Help4TN; HRSA FQHC locator."
)

# (state, county, has_core pipe-sep, blocking_category, outcome, source_url, detail)
ENTRIES: list[tuple[str, str, str, str, str, str, str]] = [
    # --- Ohio (12 Tier A weak) ---
    (
        "ohio",
        "Crawford",
        "financial-assistance|probation-parole",
        "legal-aid",
        "GAP",
        "https://www.ohiolegalhelp.org/",
        "Crawford not listed in LAWO or LASCO served_counties. No standalone county legal aid "
        "clinic found in 211 or county bar referral pages. Mid-Ohio Reentry Coalition provides "
        "navigation only. BACKLOG candidate: OhioMeansJobs Crawford (verify at county JFS).",
    ),
    (
        "ohio",
        "Hancock",
        "legal-aid|probation-parole",
        "financial-assistance",
        "BACKLOG",
        "https://pcsao.org/membership/agency-directory/",
        "Hancock County CDJFS (Findlay) exists per county structure; not yet in CSV with verified "
        "street address/phone from primary .gov page. LAWO covers Hancock for legal-aid; Lima APA "
        "region covers probation-parole.",
    ),
    (
        "ohio",
        "Hardin",
        "legal-aid|probation-parole",
        "financial-assistance",
        "BACKLOG",
        "https://pcsao.org/membership/agency-directory/",
        "Hardin County CDJFS (Kenton) not yet in CSV. LAWO and Lima APA region already pin legal-aid "
        "and probation-parole.",
    ),
    (
        "ohio",
        "Jefferson",
        "probation-parole",
        "legal-aid",
        "GAP",
        "https://www.ohiolegalhelp.org/",
        "Jefferson not in LAWO or LASCO served_counties. Route 11 coalition is referral-only. "
        "BACKLOG: Jefferson County CDJFS (Steubenville) for financial-assistance once verified.",
    ),
    (
        "ohio",
        "Lawrence",
        "legal-aid|probation-parole",
        "financial-assistance",
        "BACKLOG",
        "https://drc.ohio.gov/about-us/divisions-and-offices/adult-parole-authority",
        "Lawrence County CDJFS (Ironton) not in CSV. Columbus APA region and southeast legal aid "
        "partners cover other cores; county JFS row pending verified contact from county .gov.",
    ),
    (
        "ohio",
        "Marion",
        "legal-aid|probation-parole",
        "financial-assistance",
        "BACKLOG",
        "https://pcsao.org/membership/agency-directory/",
        "Marion County CDJFS not in CSV. LAWO covers Marion. Dayton APA region includes Marion for "
        "probation-parole.",
    ),
    (
        "ohio",
        "Mercer",
        "legal-aid|probation-parole",
        "financial-assistance",
        "BACKLOG",
        "https://pcsao.org/membership/agency-directory/",
        "Mercer County CDJFS (Celina) not in CSV. LAWO and Lima APA region cover legal-aid and "
        "probation-parole.",
    ),
    (
        "ohio",
        "Preble",
        "employment|probation-parole",
        "financial-assistance",
        "BACKLOG",
        "https://pcsao.org/membership/agency-directory/",
        "Preble County CDJFS (Eaton) not in CSV. Cincinnati APA region covers probation-parole. "
        "Preble not in LAWO list; legal-aid gap may remain after JFS added.",
    ),
    (
        "ohio",
        "Putnam",
        "legal-aid|probation-parole",
        "financial-assistance",
        "BACKLOG",
        "https://defiancepauldingjfs.com/about-jfs/",
        "Putnam served by Defiance/Paulding consolidated JFS; county not explicitly pinned in CSV. "
        "LAWO covers Putnam for legal-aid.",
    ),
    (
        "ohio",
        "Trumbull",
        "healthcare|probation-parole",
        "financial-assistance",
        "BACKLOG",
        "https://pcsao.org/membership/agency-directory/",
        "Trumbull County CDJFS (Warren) not in CSV. AxessPointe network pins healthcare; Akron APA "
        "region pins probation-parole.",
    ),
    (
        "ohio",
        "Union",
        "food-nutrition|probation-parole",
        "financial-assistance",
        "BACKLOG",
        "https://pcsao.org/membership/agency-directory/",
        "Union County CDJFS (Marysville) not in CSV. Mid-Ohio Food Collective may serve via partner "
        "network; Dayton APA region covers probation-parole.",
    ),
    (
        "ohio",
        "Wood",
        "legal-aid|probation-parole",
        "financial-assistance",
        "BACKLOG",
        "https://pcsao.org/membership/agency-directory/",
        "Wood County CDJFS (Bowling Green) not in CSV. LAWO and Lima APA region cover legal-aid and "
        "probation-parole.",
    ),
    # --- Tennessee (17 Tier A weak) ---
    (
        "tennessee",
        "Anderson",
        "employment|food-nutrition",
        "financial-assistance",
        "BACKLOG",
        "https://www.tn.gov/humanservices/for-families/supplemental-nutrition-assistance-program-snap/office-locator-family-assistance.html",
        "Anderson County TDHS Family Assistance (Clinton/Oak Ridge area) not pinned in CSV. ETHRA "
        "LWDB and Second Harvest ETN already pin employment and food-nutrition.",
    ),
    (
        "tennessee",
        "Blount",
        "employment|food-nutrition",
        "financial-assistance",
        "BACKLOG",
        "https://www.tn.gov/humanservices/for-families/supplemental-nutrition-assistance-program-snap/office-locator-family-assistance.html",
        "Blount County TDHS office not in CSV. ETHRA LWDB and Second Harvest ETN cover employment and "
        "food-nutrition.",
    ),
    (
        "tennessee",
        "Bradley",
        "employment|food-nutrition",
        "financial-assistance",
        "BACKLOG",
        "https://www.tn.gov/humanservices/for-families/supplemental-nutrition-assistance-program-snap/office-locator-family-assistance.html",
        "Bradley County TDHS office not in CSV. Southeast LWDB and Chattanooga Area Food Bank network "
        "cover employment and food-nutrition.",
    ),
    (
        "tennessee",
        "Cannon",
        "employment|legal-aid",
        "financial-assistance",
        "BACKLOG",
        "https://www.tn.gov/humanservices/for-families/supplemental-nutrition-assistance-program-snap/office-locator-family-assistance.html",
        "Cannon County TDHS office not in CSV. Upper Cumberland LWDB and LASMT legal aid cover "
        "employment and legal-aid.",
    ),
    (
        "tennessee",
        "Carter",
        "employment|legal-aid",
        "financial-assistance",
        "BACKLOG",
        "https://www.tn.gov/humanservices/for-families/supplemental-nutrition-assistance-program-snap/office-locator-family-assistance.html",
        "Carter County TDHS office not in CSV. Northeast LWDB and LAET cover employment and legal-aid.",
    ),
    (
        "tennessee",
        "Clay",
        "employment|legal-aid",
        "financial-assistance",
        "BACKLOG",
        "https://www.tn.gov/humanservices/for-families/supplemental-nutrition-assistance-program-snap/office-locator-family-assistance.html",
        "Clay County TDHS office not in CSV. Upper Cumberland LWDB and LASMT cover employment and "
        "legal-aid.",
    ),
    (
        "tennessee",
        "Crockett",
        "employment|food-nutrition",
        "financial-assistance",
        "BACKLOG",
        "https://www.tn.gov/humanservices/for-families/supplemental-nutrition-assistance-program-snap/office-locator-family-assistance.html",
        "Crockett County TDHS office not in CSV (West TN). Northwest LWDB and Mid-South Food Bank "
        "cover employment and food-nutrition.",
    ),
    (
        "tennessee",
        "DeKalb",
        "employment|legal-aid",
        "financial-assistance",
        "BACKLOG",
        "https://www.tn.gov/humanservices/for-families/supplemental-nutrition-assistance-program-snap/office-locator-family-assistance.html",
        "DeKalb County TDHS office not in CSV. Upper Cumberland LWDB and LASMT cover employment and "
        "legal-aid.",
    ),
    (
        "tennessee",
        "Greene",
        "employment|legal-aid",
        "financial-assistance",
        "BACKLOG",
        "https://www.tn.gov/humanservices/for-families/supplemental-nutrition-assistance-program-snap/office-locator-family-assistance.html",
        "Greene County TDHS office not in CSV. Northeast LWDB and LAET cover employment and legal-aid.",
    ),
    (
        "tennessee",
        "Hawkins",
        "employment|legal-aid",
        "financial-assistance",
        "BACKLOG",
        "https://www.tn.gov/humanservices/for-families/supplemental-nutrition-assistance-program-snap/office-locator-family-assistance.html",
        "Hawkins County TDHS office not in CSV. Northeast LWDB and LAET cover employment and legal-aid.",
    ),
    (
        "tennessee",
        "Humphreys",
        "employment|financial-assistance",
        "healthcare",
        "GAP",
        "https://findahealthcenter.hrsa.gov/",
        "TDHS Waverly and AJC access already pinned. No FQHC or CMHC with Humphreys explicitly in "
        "served_counties found via HRSA locator or regional health org sites after search.",
    ),
    (
        "tennessee",
        "Johnson",
        "employment|legal-aid",
        "financial-assistance",
        "BACKLOG",
        "https://www.tn.gov/humanservices/for-families/supplemental-nutrition-assistance-program-snap/office-locator-family-assistance.html",
        "Johnson County TDHS office not in CSV. Northeast LWDB and LAET cover employment and legal-aid.",
    ),
    (
        "tennessee",
        "Lewis",
        "employment|legal-aid",
        "financial-assistance",
        "BACKLOG",
        "https://www.tn.gov/humanservices/for-families/supplemental-nutrition-assistance-program-snap/office-locator-family-assistance.html",
        "Lewis County TDHS office not in CSV. Southern Middle LWDB and LASMT cover employment and "
        "legal-aid.",
    ),
    (
        "tennessee",
        "McMinn",
        "employment|food-nutrition",
        "financial-assistance",
        "BACKLOG",
        "https://www.tn.gov/humanservices/for-families/supplemental-nutrition-assistance-program-snap/office-locator-family-assistance.html",
        "McMinn County TDHS office not in CSV. ETHRA/ Southeast networks cover employment and "
        "food-nutrition.",
    ),
    (
        "tennessee",
        "Meigs",
        "employment|food-nutrition",
        "financial-assistance",
        "BACKLOG",
        "https://www.tn.gov/humanservices/for-families/supplemental-nutrition-assistance-program-snap/office-locator-family-assistance.html",
        "Meigs County TDHS office not in CSV. ETHRA LWDB and Second Harvest ETN cover employment and "
        "food-nutrition.",
    ),
    (
        "tennessee",
        "Monroe",
        "employment|food-nutrition",
        "financial-assistance",
        "BACKLOG",
        "https://www.tn.gov/humanservices/for-families/supplemental-nutrition-assistance-program-snap/office-locator-family-assistance.html",
        "Monroe County TDHS office not in CSV. ETHRA LWDB and Second Harvest ETN cover employment and "
        "food-nutrition.",
    ),
    (
        "tennessee",
        "Unicoi",
        "employment|legal-aid",
        "financial-assistance",
        "BACKLOG",
        "https://www.tn.gov/humanservices/for-families/supplemental-nutrition-assistance-program-snap/office-locator-family-assistance.html",
        "Unicoi County TDHS office not in CSV. Northeast LWDB and LAET cover employment and legal-aid.",
    ),
]


def append_gaps() -> None:
    by_state: dict[str, list] = {"ohio": [], "tennessee": []}
    for state, county, has_core, blocking, outcome, source, detail in ENTRIES:
        search = SEARCH_OH if state == "ohio" else SEARCH_TN
        notes = (
            f"Tier A audit ({DATE}): {len(has_core.split('|'))}/8 core pinned [{has_core}]. "
            f"Blocking 3rd category: {blocking}. Outcome: {outcome}. {search} {detail}"
        )
        ref = f"TIERA-{outcome}-{'OH' if state == 'ohio' else 'TN'}-{county.replace(' ', '')}"
        conf = "high" if outcome == "BACKLOG" else "medium"
        by_state[state].append(
            {
                "source_url": source,
                "source_type": "audit",
                "date_accessed": DATE,
                "confidence": conf,
                "notes": notes,
                "id_reference": ref,
            }
        )

    for state, rows in by_state.items():
        path = ROOT / f"data/{state}-research-log.csv"
        existing = path.read_text(encoding="utf-8")
        existing_refs = {line.split(",")[-1].strip() for line in existing.splitlines()[1:] if line}
        new_rows = [r for r in rows if r["id_reference"] not in existing_refs]
        if not new_rows:
            print(f"{state}: no new gap entries")
            continue
        with path.open("a", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["source_url", "source_type", "date_accessed", "confidence", "notes", "id_reference"],
            )
            for row in new_rows:
                writer.writerow(row)
        print(f"{state}: appended {len(new_rows)} Tier A gap/backlog entries")


if __name__ == "__main__":
    append_gaps()
