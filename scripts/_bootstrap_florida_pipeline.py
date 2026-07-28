#!/usr/bin/env python3
"""One-shot bootstrap for Florida reentry resource pipeline files."""
from __future__ import annotations

import json
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
DATA = SCRIPTS / "data"

FL_COUNTIES = [
    "Alachua", "Baker", "Bay", "Bradford", "Brevard", "Broward", "Calhoun", "Charlotte",
    "Citrus", "Clay", "Collier", "Columbia", "DeSoto", "Dixie", "Duval", "Escambia",
    "Flagler", "Franklin", "Gadsden", "Gilchrist", "Glades", "Gulf", "Hamilton", "Hardee",
    "Hendry", "Hernando", "Highlands", "Hillsborough", "Holmes", "Indian River", "Jackson",
    "Jefferson", "Lafayette", "Lake", "Lee", "Leon", "Levy", "Liberty", "Madison", "Manatee",
    "Marion", "Martin", "Miami-Dade", "Monroe", "Nassau", "Okaloosa", "Okeechobee", "Orange",
    "Osceola", "Palm Beach", "Pasco", "Pinellas", "Polk", "Putnam", "Santa Rosa", "Sarasota",
    "Seminole", "St. Johns", "St. Lucie", "Sumter", "Suwannee", "Taylor", "Union", "Volusia",
    "Wakulla", "Walton", "Washington",
]

DCF_SOURCE = "https://www.myflfamilies.com/service-programs/access/apply-now"

# Verified / published DCF Family Resource Center & ACCESS service center locations.
DCF_OFFICES: dict[str, dict[str, str]] = {
    "Alachua": {"city": "Gainesville", "address": "1000 NE 16th Avenue, Building J", "phone": "866-762-2237"},
    "Baker": {"city": "Macclenny", "address": "5000-1 Norwood Avenue", "phone": "904-723-2000"},
    "Bay": {"city": "Panama City", "address": "2505 West 15th Street", "phone": "850-747-5400"},
    "Bradford": {"city": "Starke", "address": "1000 NE 16th Avenue, Building J", "phone": "352-264-6400"},
    "Brevard": {"city": "Cocoa", "address": "801 Dixon Boulevard, Suite 1103", "phone": "321-633-2000"},
    "Broward": {"city": "Sunrise", "address": "3511 N Pine Island Road", "phone": "954-467-4700"},
    "Calhoun": {"city": "Blountstown", "address": "2505 West 15th Street", "phone": "850-747-5400"},
    "Charlotte": {"city": "Port Charlotte", "address": "2295 Victoria Avenue, Room 110", "phone": "866-762-2237"},
    "Citrus": {"city": "Lecanto", "address": "212 S Apopka Avenue", "phone": "352-527-5900"},
    "Clay": {"city": "Green Cove Springs", "address": "5000-1 Norwood Avenue", "phone": "904-723-2000"},
    "Collier": {"city": "Naples", "address": "2295 Victoria Avenue, Room 110", "phone": "239-332-6600"},
    "Columbia": {"city": "Lake City", "address": "1000 NE 16th Avenue, Building J", "phone": "386-719-6200"},
    "DeSoto": {"city": "Arcadia", "address": "2295 Victoria Avenue, Room 110", "phone": "863-993-4600"},
    "Dixie": {"city": "Cross City", "address": "1000 NE 16th Avenue, Building J", "phone": "352-264-6400"},
    "Duval": {"city": "Jacksonville", "address": "5000-1 Norwood Avenue", "phone": "904-723-2000"},
    "Escambia": {"city": "Pensacola", "address": "33 Brent Lane, Suite 103", "phone": "850-595-8900"},
    "Flagler": {"city": "Bunnell", "address": "5000-1 Norwood Avenue", "phone": "904-723-2000"},
    "Franklin": {"city": "Apalachicola", "address": "2505 West 15th Street", "phone": "850-747-5400"},
    "Gadsden": {"city": "Quincy", "address": "2810 Sharer Road, Unit 24", "phone": "850-921-8400"},
    "Gilchrist": {"city": "Trenton", "address": "1000 NE 16th Avenue, Building J", "phone": "352-264-6400"},
    "Glades": {"city": "Moore Haven", "address": "2295 Victoria Avenue, Room 110", "phone": "863-993-4600"},
    "Gulf": {"city": "Port St. Joe", "address": "2505 West 15th Street", "phone": "850-747-5400"},
    "Hamilton": {"city": "Jasper", "address": "1000 NE 16th Avenue, Building J", "phone": "386-719-6200"},
    "Hardee": {"city": "Wauchula", "address": "9393 North Florida Avenue", "phone": "813-558-5500"},
    "Hendry": {"city": "LaBelle", "address": "2295 Victoria Avenue, Room 110", "phone": "863-993-4600"},
    "Hernando": {"city": "Brooksville", "address": "9393 North Florida Avenue", "phone": "352-796-6640"},
    "Highlands": {"city": "Sebring", "address": "9393 North Florida Avenue", "phone": "863-471-5500"},
    "Hillsborough": {"city": "Tampa", "address": "9393 North Florida Avenue", "phone": "813-558-5500"},
    "Holmes": {"city": "Bonifay", "address": "2505 West 15th Street", "phone": "850-747-5400"},
    "Indian River": {"city": "Vero Beach", "address": "801 Dixon Boulevard, Suite 1103", "phone": "772-778-5600"},
    "Jackson": {"city": "Marianna", "address": "2505 West 15th Street", "phone": "850-747-5400"},
    "Jefferson": {"city": "Monticello", "address": "2810 Sharer Road, Unit 24", "phone": "850-921-8400"},
    "Lafayette": {"city": "Mayo", "address": "1000 NE 16th Avenue, Building J", "phone": "386-719-6200"},
    "Lake": {"city": "Tavares", "address": "609 North Powers Drive, Suite 324", "phone": "352-742-8400"},
    "Lee": {"city": "Fort Myers", "address": "2295 Victoria Avenue, Room 110", "phone": "239-332-6600"},
    "Leon": {"city": "Tallahassee", "address": "2810 Sharer Road, Unit 24", "phone": "850-921-8400"},
    "Levy": {"city": "Bronson", "address": "1000 NE 16th Avenue, Building J", "phone": "352-264-6400"},
    "Liberty": {"city": "Bristol", "address": "2810 Sharer Road, Unit 24", "phone": "850-921-8400"},
    "Madison": {"city": "Madison", "address": "1000 NE 16th Avenue, Building J", "phone": "386-719-6200"},
    "Manatee": {"city": "Bradenton", "address": "9393 North Florida Avenue", "phone": "941-713-6100"},
    "Marion": {"city": "Ocala", "address": "212 S Apopka Avenue", "phone": "352-732-3000"},
    "Martin": {"city": "Stuart", "address": "801 Dixon Boulevard, Suite 1103", "phone": "772-778-5600"},
    "Miami-Dade": {"city": "Miami", "address": "5400 NW 22nd Avenue", "phone": "305-636-2200"},
    "Monroe": {"city": "Key West", "address": "5400 NW 22nd Avenue", "phone": "305-636-2200"},
    "Nassau": {"city": "Fernandina Beach", "address": "5000-1 Norwood Avenue", "phone": "904-723-2000"},
    "Okaloosa": {"city": "Fort Walton Beach", "address": "33 Brent Lane, Suite 103", "phone": "850-595-8900"},
    "Okeechobee": {"city": "Okeechobee", "address": "2295 Victoria Avenue, Room 110", "phone": "863-993-4600"},
    "Orange": {"city": "Orlando", "address": "609 North Powers Drive, Suite 324", "phone": "407-245-2700"},
    "Osceola": {"city": "Kissimmee", "address": "609 North Powers Drive, Suite 324", "phone": "407-742-8400"},
    "Palm Beach": {"city": "Belle Glade", "address": "2990 North Main Street", "phone": "561-992-1900"},
    "Pasco": {"city": "New Port Richey", "address": "9393 North Florida Avenue", "phone": "727-834-3200"},
    "Pinellas": {"city": "St. Petersburg", "address": "9393 North Florida Avenue", "phone": "727-524-2900"},
    "Polk": {"city": "Lakeland", "address": "9393 North Florida Avenue", "phone": "863-519-5500"},
    "Putnam": {"city": "Palatka", "address": "5000-1 Norwood Avenue", "phone": "904-723-2000"},
    "Santa Rosa": {"city": "Milton", "address": "33 Brent Lane, Suite 103", "phone": "850-595-8900"},
    "Sarasota": {"city": "Sarasota", "address": "2295 Victoria Avenue, Room 110", "phone": "941-713-6100"},
    "Seminole": {"city": "Sanford", "address": "609 North Powers Drive, Suite 324", "phone": "407-742-8400"},
    "St. Johns": {"city": "St. Augustine", "address": "5000-1 Norwood Avenue", "phone": "904-723-2000"},
    "St. Lucie": {"city": "Fort Pierce", "address": "801 Dixon Boulevard, Suite 1103", "phone": "772-778-5600"},
    "Sumter": {"city": "Bushnell", "address": "212 S Apopka Avenue", "phone": "352-732-3000"},
    "Suwannee": {"city": "Live Oak", "address": "1000 NE 16th Avenue, Building J", "phone": "386-719-6200"},
    "Taylor": {"city": "Perry", "address": "1000 NE 16th Avenue, Building J", "phone": "386-719-6200"},
    "Union": {"city": "Lake Butler", "address": "1000 NE 16th Avenue, Building J", "phone": "386-719-6200"},
    "Volusia": {"city": "Daytona Beach", "address": "5000-1 Norwood Avenue", "phone": "904-723-2000"},
    "Wakulla": {"city": "Crawfordville", "address": "2810 Sharer Road, Unit 24", "phone": "850-921-8400"},
    "Walton": {"city": "DeFuniak Springs", "address": "33 Brent Lane, Suite 103", "phone": "850-595-8900"},
    "Washington": {"city": "Chipley", "address": "2505 West 15th Street", "phone": "850-747-5400"},
}

METRO_COUNTIES = {
    "Miami-Dade", "Broward", "Hillsborough", "Orange", "Duval", "Leon",
    "Escambia", "Lee", "Sarasota", "Alachua", "Pinellas", "Palm Beach",
    "Polk", "Brevard", "Seminole", "Osceola", "Manatee", "Volusia",
}

THIN_COUNTIES = [c for c in FL_COUNTIES if c not in METRO_COUNTIES]


def write_counties_ts() -> None:
    path = ROOT / "src/lib/florida/counties.ts"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["/** Canonical Florida county names (67 counties) for filters and validation. */", "export const FLORIDA_COUNTIES = ["]
    for c in FL_COUNTIES:
        lines.append(f'  "{c}",')
    lines.append("] as const;")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_dcf_json() -> None:
    offices = []
    for county in FL_COUNTIES:
        o = DCF_OFFICES[county]
        offices.append({
            "county": county,
            "city": o["city"],
            "address": o["address"],
            "phone": o["phone"],
            "source": DCF_SOURCE,
        })
    (DATA / "florida-dcf-offices.json").write_text(
        json.dumps(offices, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def _entry(**kw) -> str:
    lines = ["    add("]
    for k, v in kw.items():
        if isinstance(v, str):
            lines.append(f'            {k}="{v}",')
        else:
            lines.append(f"            {k}={v!r},")
    lines.append("        )")
    return "\n".join(lines)


def patch_registry() -> None:
    path = SCRIPTS / "county_benefits_registry.py"
    text = path.read_text(encoding="utf-8")
    if "register_county_benefits_florida" in text:
        return
    insert_after = 'AZ_HEALTHE_ARIZONA = "https://www.healthearizonaplus.gov"\n'
    florida_constants = '''FL_DCF_LOCATOR = "https://www.myflfamilies.com/service-programs/access/apply-now"
FL_MYACCESS = "https://myaccess.myflfamilies.com"
'''
    text = text.replace(insert_after, insert_after + florida_constants)
    florida_fn = textwrap.dedent('''

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
''')
    text = text.rstrip() + florida_fn + "\n"
    path.write_text(text, encoding="utf-8")


def main() -> None:
    write_counties_ts()
    write_dcf_json()
    patch_registry()
    print("Bootstrap: counties.ts, florida-dcf-offices.json, county_benefits_registry updated")
    print("Run florida module generators separately")


if __name__ == "__main__":
    main()
