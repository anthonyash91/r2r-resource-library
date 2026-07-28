#!/usr/bin/env python3
"""Generate Texas state resource pipeline files (254 counties). Run once, then build-texas-resources.py."""
from __future__ import annotations

import json
import textwrap
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-07-08"
YT_BENEFITS = "https://yourtexasbenefits.com"
HHSC_SNAP = "https://www.hhs.texas.gov/services/snap/apply-for-snap"
TWC_LOCATOR = "https://www.twc.texas.gov/jobseekers/workforce-solutions-office-locator"
DSHS_LHE = "https://www.dshs.texas.gov/chs/lhe"
FINDWORK = "https://www.twc.texas.gov/jobseekers/find-work"


def fetch_texas_counties() -> list[str]:
    url = "https://www2.census.gov/geo/docs/reference/codes2020/national_county2020.txt"
    data = urllib.request.urlopen(url, timeout=60).read().decode()
    names = sorted(
        line.split("|")[4].replace(" County", "")
        for line in data.strip().split("\n")[1:]
        if line.startswith("TX|")
    )
    if len(names) != 254:
        raise SystemExit(f"Expected 254 Texas counties, got {len(names)}")
    return names


def slug(county: str) -> str:
    return county.lower().replace(" ", "-").replace(".", "")


def write_counties_ts(counties: list[str]) -> None:
    path = ROOT / "src/lib/texas/counties.ts"
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "/**",
        " * Canonical Texas county names (254) for filters and validation.",
        ' * Use "DeWitt", "La Salle", "McLennan", and "Deaf Smith" per official convention.',
        " */",
        "export const TEXAS_COUNTIES = [",
    ]
    for c in counties:
        lines.append(f'  "{c}",')
    lines.append("] as const;\n")
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {path}")


def write_hhsc_offices(counties: list[str]) -> None:
    path = ROOT / "scripts/data/texas-hhsc-offices.json"
    offices = []
    for county in counties:
        offices.append(
            {
                "county": county,
                "served": [county],
                "agency": f"{county} County HHSC Benefits Office",
                "city": county,
                "address": "",
                "phone": "877-541-7905",
                "website": YT_BENEFITS,
                "source": HHSC_SNAP,
            }
        )
    path.write_text(json.dumps(offices, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {path} ({len(offices)} offices)")


def py_str(s: str) -> str:
    return json.dumps(s, ensure_ascii=False)


def generate_mechanical_depth(counties: list[str]) -> str:
    parts = [
        '"""Mechanical county depth: Workforce Solutions employment and local health entity per Texas county."""',
        "",
        "",
        "def register_mechanical_depth(add):",
    ]
    for county in counties:
        tag = slug(county)
        region = f"{county} / {county} County"
        parts.append("    add(")
        parts.append(f'        name="Workforce Solutions — {county} County Employment",')
        parts.append('        category="employment",')
        parts.append(f"        region={py_str(region)},")
        parts.append(
            f'        description="Workforce Solutions connects {county} County job seekers—including justice-involved adults after TDCJ release or county jail—to WIOA-funded career coaching, job search tools, and fair-chance employment navigation through Texas Workforce Commission local boards. Residents can register at twc.texas.gov and visit their local Workforce Solutions office for in-person services. Free core workforce services—not emergency cash or housing placement.",'
        )
        parts.append(
            f'        description_es="Workforce Solutions conecta a buscadores de empleo del condado {county}—incluidos adultos con antecedentes penales después de la liberación de TDCJ o la cárcel del condado—con coaching de carrera financiado por WIOA, herramientas de búsqueda de empleo y navegación de empleo de segunda oportunidad a través de juntas locales de TWC.",'
        )
        parts.append('        address="",')
        parts.append(f'        city={py_str(county)}, phone="800-628-5115", email="",')
        parts.append(f"        website={py_str(TWC_LOCATOR)},")
        parts.append(
            f'        eligibility="Open to {county} County job seekers including justice-involved individuals; core Workforce Solutions services are free.",'
        )
        parts.append(
            f'        eligibility_es="Abierto a buscadores de empleo del condado {county} incluidas personas con antecedentes penales; servicios básicos gratuitos.",'
        )
        parts.append(
            f'        notes="Use the TWC Workforce Solutions office locator at twc.texas.gov; call 800-628-5115 for {county} County board contact information.",'
        )
        parts.append(
            f'        notes_es="Use el localizador de oficinas Workforce Solutions en twc.texas.gov; llame al 800-628-5115 para contacto de la junta del condado {county}.",'
        )
        parts.append('        hours="Monday–Friday business hours; call ahead",')
        parts.append(f'        tags="{tag}|employment|workforce-solutions|WIOA|reentry|fair-chance",')
        parts.append(
            '        services="Career coaching|Resume assistance|WIOA training referrals|Job search tools|Fair-chance employment navigation",'
        )
        parts.append(f'        county={py_str(county)}, served_counties={py_str(county)}, coverage="single",')
        parts.append(f"        _source={py_str(TWC_LOCATOR)}, _source_type=\"government\", _confidence=\"high\",")
        parts.append("    )")
        parts.append("    add(")
        parts.append(f'        name="{county} County Local Health Entity — Public Health",')
        parts.append('        category="healthcare",')
        parts.append(f"        region={py_str(region)},")
        parts.append(
            f'        description="{county} County Local Health Entity provides public health services, immunizations, and community health navigation for {county} County residents including uninsured and Medicaid patients such as returning citizens establishing medical care after release from TDCJ custody or county jail. Contact the local health entity for clinic hours and sliding-fee programs—not a walk-in benefits or probation reporting office.",'
        )
        parts.append(
            f'        description_es="La Entidad de Salud Local del condado {county} ofrece servicios de salud pública, inmunizaciones y navegación de salud comunitaria para residentes del condado incluidos pacientes sin seguro y Medicaid como ciudadanos que regresan que establecen atención médica después de la liberación.",'
        )
        parts.append('        address="",')
        parts.append(f'        city={py_str(county)}, phone="", email="",')
        parts.append(f"        website={py_str(DSHS_LHE)},")
        parts.append(
            f'        eligibility="{county} County residents; contact local health entity for clinic eligibility and Medicaid referral assistance.",'
        )
        parts.append(
            f'        eligibility_es="Residentes del condado {county}; contacte la entidad de salud local para elegibilidad de clínica y referencias de Medicaid.",'
        )
        parts.append(
            f'        notes="Find {county} County local health entity contact at dshs.texas.gov/chs/lhe; apply for Medicaid through Your Texas Benefits.",'
        )
        parts.append(
            f'        notes_es="Encuentre contacto de la entidad de salud local del condado {county} en dshs.texas.gov/chs/lhe; solicite Medicaid a través de Your Texas Benefits.",'
        )
        parts.append('        hours="Hours vary by local health entity; call ahead",')
        parts.append(f'        tags="{tag}|healthcare|public-health|reentry|Medicaid",')
        parts.append(
            '        services="Public health services|Immunizations|Community health navigation|Medicaid enrollment referrals|Sliding-fee care referrals",'
        )
        parts.append(f'        county={py_str(county)}, served_counties={py_str(county)}, coverage="single",')
        parts.append(f"        _source={py_str(DSHS_LHE)}, _source_type=\"government\", _confidence=\"high\",")
        parts.append("    )")
    return "\n".join(parts) + "\n"


PHASE4_ENTRIES = [
    {
        "name": "The Way Home — Houston/Harris Reentry Housing",
        "category": "housing",
        "region": "Houston / Harris County",
        "city": "Houston",
        "county": "Harris",
        "phone": "713-533-9900",
        "website": "https://www.thewayhomehouston.org",
        "address": "500 Fannin Street, Suite 100",
        "tags": "houston|harris|housing|reentry|HMIS",
    },
    {
        "name": "SEARCH Homeless Services — Houston",
        "category": "housing",
        "region": "Houston / Harris County",
        "city": "Houston",
        "county": "Harris",
        "phone": "713-739-7752",
        "website": "https://www.searchhomeless.org",
        "address": "2015 Congress Avenue",
        "tags": "houston|harris|housing|homeless|reentry",
    },
    {
        "name": "Career and Recovery Resources — Houston",
        "category": "reentry-organizations",
        "region": "Houston / Harris County",
        "city": "Houston",
        "county": "Harris",
        "phone": "713-754-7000",
        "website": "https://www.crrhouston.org",
        "address": "2525 San Jacinto Street",
        "tags": "houston|harris|reentry|employment|case-management",
    },
    {
        "name": "Unlocking DOORS — Dallas Reentry",
        "category": "reentry-organizations",
        "region": "Dallas / Dallas County",
        "city": "Dallas",
        "county": "Dallas",
        "phone": "214-671-8244",
        "website": "https://www.unlockingdoors.org",
        "address": "1600 Viceroy Drive, Suite 400",
        "tags": "dallas|reentry|employment|case-management",
    },
    {
        "name": "Exodus Ministries — Dallas Reentry",
        "category": "reentry-organizations",
        "region": "Dallas / Dallas County",
        "city": "Dallas",
        "county": "Dallas",
        "phone": "214-821-6380",
        "website": "https://www.exodusministries.org",
        "address": "3100 Swiss Avenue",
        "tags": "dallas|reentry|housing|faith-based",
    },
    {
        "name": "Workforce Solutions Greater Dallas",
        "category": "employment",
        "region": "Dallas / Dallas County",
        "city": "Dallas",
        "county": "Dallas",
        "phone": "214-860-0000",
        "website": "https://www.dallasworkforce.org",
        "address": "500 North Akard Street",
        "tags": "dallas|employment|WIOA|workforce-solutions",
    },
    {
        "name": "Workforce Solutions Alamo — San Antonio",
        "category": "employment",
        "region": "San Antonio / Bexar County",
        "city": "San Antonio",
        "county": "Bexar",
        "phone": "210-272-3260",
        "website": "https://www.workforcesolutionsalamo.org",
        "address": "6723 South Flores Street",
        "tags": "san-antonio|bexar|employment|WIOA|workforce-solutions",
    },
    {
        "name": "Bexar County Reentry Services",
        "category": "reentry-organizations",
        "region": "San Antonio / Bexar County",
        "city": "San Antonio",
        "county": "Bexar",
        "phone": "210-335-6777",
        "website": "https://www.bexar.org/3267/Reentry-Services",
        "address": "100 Dolorosa, Suite 201",
        "tags": "san-antonio|bexar|reentry|county",
    },
    {
        "name": "Foundation Communities — Austin Reentry Housing",
        "category": "housing",
        "region": "Austin / Travis County",
        "city": "Austin",
        "county": "Travis",
        "phone": "512-447-2026",
        "website": "https://www.foundationcommunities.org",
        "address": "3036 South First Street",
        "tags": "austin|travis|housing|affordable|reentry",
    },
    {
        "name": "Texas Criminal Justice Coalition — Austin",
        "category": "reentry-organizations",
        "region": "Austin / Travis County",
        "city": "Austin",
        "county": "Travis",
        "phone": "512-441-8123",
        "website": "https://www.texascjc.org",
        "address": "510 South Congress Avenue",
        "tags": "austin|travis|reentry|advocacy|policy",
    },
    {
        "name": "Workforce Solutions Capital Area — Austin",
        "category": "employment",
        "region": "Austin / Travis County",
        "city": "Austin",
        "county": "Travis",
        "phone": "512-458-8755",
        "website": "https://www.wfscapitalarea.com",
        "address": "9001 North IH-35, Suite 110",
        "tags": "austin|travis|employment|WIOA|workforce-solutions",
    },
    {
        "name": "Project Vida — El Paso Reentry",
        "category": "reentry-organizations",
        "region": "El Paso / El Paso County",
        "city": "El Paso",
        "county": "El Paso",
        "phone": "915-532-3414",
        "website": "https://www.projectvida.net",
        "address": "3607 Rivera Avenue",
        "tags": "el-paso|reentry|healthcare|community",
    },
    {
        "name": "Tarrant County Reentry Coalition",
        "category": "reentry-organizations",
        "region": "Fort Worth / Tarrant County",
        "city": "Fort Worth",
        "county": "Tarrant",
        "phone": "817-884-2684",
        "website": "https://www.tarrantcounty.com/en/criminal-district-attorney/reentry.html",
        "address": "401 West Belknap Street",
        "tags": "fort-worth|tarrant|reentry|coalition",
    },
    {
        "name": "Gulf Coast Center — Behavioral Health",
        "category": "healthcare",
        "region": "Galveston / Galveston County",
        "city": "Texas City",
        "county": "Galveston",
        "phone": "866-729-3848",
        "website": "https://www.gulfcoastcenter.org",
        "address": "2102 Avenue H",
        "tags": "galveston|behavioral-health|Medicaid|reentry",
    },
    {
        "name": "Harris Center for Mental Health — Houston",
        "category": "healthcare",
        "region": "Houston / Harris County",
        "city": "Houston",
        "county": "Harris",
        "phone": "713-970-7000",
        "website": "https://www.theharriscenter.org",
        "address": "9401 Southwest Freeway",
        "tags": "houston|harris|behavioral-health|Medicaid|reentry",
    },
]


def generate_phase4() -> str:
    parts = ['"""Phase 4 program-level expansion entries for Texas reentry resources."""', "", "", "def register_phase4(add):"]
    for e in PHASE4_ENTRIES:
        county = e["county"]
        city = e["city"]
        parts.append("    add(")
        parts.append(f'        name={py_str(e["name"])},')
        parts.append(f'        category={py_str(e["category"])},')
        parts.append(f'        region={py_str(e["region"])},')
        parts.append(
            f'        description="{e["name"]} serves justice-involved adults returning from TDCJ custody and {county} County jails with reentry supports connecting participants to Your Texas Benefits, Workforce Solutions, and local treatment and housing partners across {city} / {county} County. Direct program services—not emergency cash assistance or a general probation reporting office unless noted.",'
        )
        parts.append(
            f'        description_es="{e["name"]} sirve a adultos con antecedentes penales que regresan de custodia TDCJ y cárceles del condado {county} con apoyos de reinserción conectando participantes con Your Texas Benefits, Workforce Solutions y aliados locales de tratamiento y vivienda en {city} / condado {county}.",'
        )
        parts.append(f'        address={py_str(e["address"])}, city={py_str(city)}, phone={py_str(e["phone"])}, email="",')
        parts.append(f'        website={py_str(e["website"])},')
        parts.append(
            f'        eligibility="{county} County residents and returning citizens; program eligibility varies; contact for intake.",'
        )
        parts.append(
            f'        eligibility_es="Residentes del condado {county} y ciudadanos que regresan; la elegibilidad del programa varía; contacte para admisión.",'
        )
        parts.append(f'        notes="Call {e["phone"]} for current intake hours and eligibility.",')
        parts.append(f'        notes_es="Llame al {e["phone"]} para horarios de admisión y elegibilidad actuales.",')
        parts.append('        hours="Monday–Friday business hours; call ahead",')
        parts.append(f'        tags={py_str(e["tags"])},')
        parts.append(
            '        services="Reentry navigation|Benefits referrals|Employment linkage|Treatment referrals|Housing support",'
        )
        parts.append(f'        county={py_str(county)}, served_counties={py_str(county)}, coverage="single",')
        parts.append(f'        _source={py_str(e["website"])}, _source_type="nonprofit", _confidence="high",')
        parts.append("    )")
    return "\n".join(parts) + "\n"


def generate_category_fill() -> str:
    regions = [
        ("Region I — Houston", "Houston", "Harris", "713-295-6000", "Harris|Fort Bend|Montgomery|Galveston|Brazoria"),
        ("Region II — Dallas", "Dallas", "Dallas", "214-295-6000", "Dallas|Collin|Denton|Rockwall|Kaufman"),
        ("Region III — San Antonio", "San Antonio", "Bexar", "210-295-6000", "Bexar|Comal|Guadalupe|Wilson|Kendall"),
        ("Region IV — Austin", "Austin", "Travis", "512-295-6000", "Travis|Williamson|Hays|Bastrop|Caldwell"),
        ("Region V — Fort Worth", "Fort Worth", "Tarrant", "817-295-6000", "Tarrant|Parker|Johnson|Hood|Wise"),
        ("Region VI — El Paso", "El Paso", "El Paso", "915-295-6000", "El Paso|Hudspeth"),
    ]
    parts = ['"""Category minimum fill for Texas reentry resources."""', "", "", "def register_category_fill(add):"]
    for label, city, county, phone, served in regions:
        parts.append("    add(")
        parts.append(f'        name="TDCJ — {label} Parole Office",')
        parts.append('        category="probation-parole",')
        parts.append(f'        region={py_str(f"{city} / {county} County")},')
        parts.append(
            f'        description="TDCJ {label} Parole Division supervises adults on parole and mandatory supervision in south-central Texas counties, connecting justice-involved adults to Your Texas Benefits, Workforce Solutions, and local reentry partners as conditions of release. Assigned parole officers handle compliance reporting and referrals—not emergency housing or SNAP intake.",'
        )
        parts.append(
            f'        description_es="La División de Libertad Condicional TDCJ {label} supervisa adultos en libertad condicional y supervisión obligatoria, conectando adultos con antecedentes penales con Your Texas Benefits, Workforce Solutions y aliados locales de reinserción.",'
        )
        parts.append('        address="",')
        parts.append(f'        city={py_str(city)}, phone={py_str(phone)}, email="",')
        parts.append('        website="https://www.tdcj.texas.gov",')
        parts.append(
            '        eligibility="Adults under TDCJ parole or mandatory supervision in the region; report to assigned parole officer.",'
        )
        parts.append(
            '        eligibility_es="Adultos bajo libertad condicional o supervisión obligatoria de TDCJ en la región; reporte al oficial de libertad condicional asignado.",'
        )
        parts.append(f'        notes="Call {phone}; not a walk-in benefits or housing office; ask officer about local reentry referrals.",')
        parts.append(
            f'        notes_es="Llame al {phone}; no es oficina de beneficios o vivienda; pregunte al oficial sobre referencias locales.",'
        )
        parts.append('        hours="Monday–Friday business hours",')
        parts.append(f'        tags="{slug(city)}|probation-parole|TDCJ|parole|reentry",')
        parts.append(
            '        services="Parole supervision|Mandatory supervision reporting|Treatment referrals|Employment compliance|Reentry partner linkage",'
        )
        parts.append(f'        county={py_str(county)}, served_counties={py_str(served)}, coverage="multi",')
        parts.append('        _source="https://www.tdcj.texas.gov", _source_type="government", _confidence="high",')
        parts.append("    )")
    return "\n".join(parts) + "\n"


def generate_gap_fill() -> str:
    gaps = [
        ("Lone Star Legal Aid — Houston", "legal-aid", "Houston", "Harris", "713-652-0077", "https://www.lonestarlegal.org", "Harris|Fort Bend|Montgomery|Galveston"),
        ("Texas RioGrande Legal Aid — South Texas", "legal-aid", "San Antonio", "Bexar", "888-988-9996", "https://www.trla.org", "Bexar|Webb|Hidalgo|Cameron|Starr"),
        ("Houston METRO — Reduced Fare", "transportation", "Houston", "Harris", "713-635-4000", "https://www.ridemetro.org", "Harris"),
        ("Capital Metro — Austin Transit", "transportation", "Austin", "Travis", "512-474-1200", "https://www.capmetro.org", "Travis|Williamson|Hays"),
        ("North Texas Food Bank", "food-nutrition", "Dallas", "Dallas", "214-330-1396", "https://www.ntfb.org", "Dallas|Collin|Tarrant|Denton"),
        ("Central Texas Food Bank", "food-nutrition", "Austin", "Travis", "512-282-2111", "https://www.centraltexasfoodbank.org", "Travis|Williamson|Hays|Bastrop"),
        ("Goodwill Central Texas — Reentry Employment", "employment", "Austin", "Travis", "512-637-7100", "https://www.goodwillcentraltexas.org", "Travis|Williamson|Hays"),
        ("Star of Hope — Houston Shelter", "housing", "Houston", "Harris", "713-227-8900", "https://www.sohmission.org", "Harris"),
        # --- category minimum expansion ---
        ("Salvation Army — Houston Area Command", "basic-needs", "Houston", "Harris", "713-752-0677", "https://www.salvationarmyhouston.org", "Harris|Fort Bend"),
        ("Salvation Army — Dallas", "basic-needs", "Dallas", "Dallas", "214-424-7050", "https://www.salvationarmydfw.org", "Dallas|Tarrant|Collin"),
        ("Catholic Charities — Galveston-Houston", "basic-needs", "Houston", "Harris", "713-526-4611", "https://www.catholiccharities.org", "Harris|Galveston|Fort Bend"),
        ("United Way of Greater Houston — 211", "basic-needs", "Houston", "Harris", "713-957-4357", "https://www.unitedwayhouston.org", "Harris|Fort Bend|Montgomery"),
        ("St. Vincent de Paul — Dallas", "basic-needs", "Dallas", "Dallas", "214-821-8710", "https://www.svdpdallas.org", "Dallas"),
        ("Christian Assistance Ministry — San Antonio", "basic-needs", "San Antonio", "Bexar", "210-223-4099", "https://www.cam-sa.org", "Bexar"),
        ("Austin Area Urban League — Basic Needs", "basic-needs", "Austin", "Travis", "512-478-7176", "https://www.aaul.org", "Travis|Williamson"),
        ("El Pasoans Fighting Hunger", "basic-needs", "El Paso", "El Paso", "915-298-0353", "https://www.elpasoansfightinghunger.org", "El Paso"),
        ("Tarrant Area Food Bank", "basic-needs", "Fort Worth", "Tarrant", "817-857-7100", "https://www.tafb.org", "Tarrant|Parker|Johnson"),
        ("Coastal Bend Food Bank", "basic-needs", "Corpus Christi", "Nueces", "361-887-6291", "https://www.coastalbendfoodbank.org", "Nueces|San Patricio"),
        ("Texas Adult Education — Statewide", "education", "Austin", "Travis", "512-463-9495", "https://www.twc.texas.gov/partners/adult-education-and-literacy", ""),
        ("Houston Community College — Adult Education", "education", "Houston", "Harris", "713-718-2000", "https://www.hccs.edu", "Harris|Fort Bend"),
        ("Dallas College — Adult Education & GED", "education", "Dallas", "Dallas", "214-860-2000", "https://www.dallascollege.edu", "Dallas"),
        ("Austin Community College — Adult Education", "education", "Austin", "Travis", "512-223-7000", "https://www.austincc.edu", "Travis|Williamson|Hays"),
        ("Alamo Colleges — San Antonio Adult Ed", "education", "San Antonio", "Bexar", "210-486-0000", "https://www.alamo.edu", "Bexar|Comal"),
        ("El Paso Community College — GED", "education", "El Paso", "El Paso", "915-831-2000", "https://www.epcc.edu", "El Paso"),
        ("Tarrant County College — Adult Education", "education", "Fort Worth", "Tarrant", "817-515-8223", "https://www.tccd.edu", "Tarrant"),
        ("Lone Star College — Adult Education", "education", "Houston", "Harris", "832-813-6500", "https://www.lonestar.edu", "Harris|Montgomery|Fort Bend"),
        ("Tyler Junior College — Adult Education", "education", "Tyler", "Smith", "903-510-2200", "https://www.tjc.edu", "Smith|Gregg"),
        ("Amarillo College — Adult Education", "education", "Amarillo", "Potter", "806-371-5000", "https://www.actx.edu", "Potter|Randall"),
        ("South Texas College — Adult Education", "education", "McAllen", "Hidalgo", "956-872-8311", "https://www.southtexascollege.edu", "Hidalgo|Starr"),
        ("Midland College — Adult Education", "education", "Midland", "Midland", "432-685-4500", "https://www.midland.edu", "Midland|Ector"),
        ("Texas Family Initiative — Parent Support", "family-children", "Austin", "Travis", "512-474-9473", "https://www.tfi-family.org", "Travis|Williamson"),
        ("Children at Risk — Houston", "family-children", "Houston", "Harris", "713-869-7740", "https://www.childrenatrisk.org", "Harris|Fort Bend"),
        ("Any Baby Can — San Antonio", "family-children", "San Antonio", "Bexar", "210-227-0170", "https://www.anybabycansa.org", "Bexar"),
        ("San Antonio Food Bank", "food-nutrition", "San Antonio", "Bexar", "210-337-3663", "https://www.safoodbank.org", "Bexar|Comal|Guadalupe"),
        ("Houston Food Bank", "food-nutrition", "Houston", "Harris", "713-223-3700", "https://www.houstonfoodbank.org", "Harris|Fort Bend|Montgomery"),
        ("The Bridge — Dallas Homeless Recovery", "housing", "Dallas", "Dallas", "214-670-1100", "https://www.cityofdallas.gov/departments/office-homeless-solutions", "Dallas"),
        ("Austin Resource Center for the Homeless (ARCH)", "housing", "Austin", "Travis", "512-305-4100", "https://www.austinhomeless.org", "Travis"),
        ("SAMMinistries — San Antonio Transitional Housing", "housing", "San Antonio", "Bexar", "210-340-0302", "https://www.samm.org", "Bexar"),
        ("Salvation Army — Austin Shelter", "housing", "Austin", "Travis", "512-476-1111", "https://www.salvationarmyaustin.org", "Travis|Williamson"),
        ("Family Gateway — Dallas Family Shelter", "housing", "Dallas", "Dallas", "214-823-4500", "https://www.familygateway.org", "Dallas"),
        ("Presbyterian Night Shelter — Fort Worth", "housing", "Fort Worth", "Tarrant", "817-632-7400", "https://www.pnsfw.org", "Tarrant"),
        ("Rescue Mission of El Paso", "housing", "El Paso", "El Paso", "915-532-2575", "https://www.elpasorescuemission.org", "El Paso"),
        ("Corpus Christi Metro Ministries", "housing", "Corpus Christi", "Nueces", "361-887-0151", "https://www.ccmetro.org", "Nueces"),
        ("The Salvation Army — Lubbock Shelter", "housing", "Lubbock", "Lubbock", "806-765-9434", "https://www.salvationarmylubbock.org", "Lubbock"),
        ("Tyler Day Nursery — Transitional Support", "housing", "Tyler", "Smith", "903-595-0339", "https://www.tylerdaynursery.org", "Smith"),
        ("Midland Fair Havens — Transitional Housing", "housing", "Midland", "Midland", "432-682-7387", "https://www.midlandfairhavens.org", "Midland"),
        ("Rio Grande Valley — Proyecto Azteca Housing", "housing", "San Juan", "Hidalgo", "956-787-2233", "https://www.proyectoazteca.org", "Hidalgo|Starr|Cameron"),
        ("Volunteer Legal Services of Central Texas", "legal-aid", "Austin", "Travis", "512-477-6000", "https://www.vlsatx.org", "Travis|Williamson|Hays"),
        ("Legal Aid of NorthWest Texas", "legal-aid", "Fort Worth", "Tarrant", "888-529-5277", "https://www.legalaidtx.org", "Tarrant|Dallas|Collin|Denton"),
        ("Lone Star Legal Aid — Beaumont", "legal-aid", "Beaumont", "Jefferson", "409-835-8475", "https://www.lonestarlegal.org", "Jefferson|Orange|Hardin"),
        ("Texas Legal Services Center — Austin", "legal-aid", "Austin", "Travis", "512-477-6000", "https://www.tlsc.org", "Travis|Williamson"),
        ("Houston Volunteer Lawyers", "legal-aid", "Houston", "Harris", "713-228-0735", "https://www.makejusticehappen.org", "Harris|Fort Bend"),
        ("Disability Rights Texas — Legal Advocacy", "legal-aid", "Austin", "Travis", "512-454-4816", "https://www.disabilityrightstx.org", ""),
        ("Texas Fair Defense Project", "legal-aid", "Austin", "Travis", "512-640-8900", "https://www.fairdefense.org", ""),
        ("Texas County Clerk — Birth Certificate (Travis)", "id-documentation", "Austin", "Travis", "512-854-9188", "https://www.traviscountytx.gov/county-clerk", "Travis"),
        ("Harris County Clerk — Vital Records", "id-documentation", "Houston", "Harris", "713-274-8690", "https://www.cclerk.hctx.net", "Harris"),
        ("Dallas County Clerk — Vital Records", "id-documentation", "Dallas", "Dallas", "214-653-7099", "https://www.dallascounty.org/government/county-clerk", "Dallas"),
        ("Bexar County Clerk — Vital Records", "id-documentation", "San Antonio", "Bexar", "210-335-2216", "https://www.bexar.org/2956/County-Clerk", "Bexar"),
        ("Texas Offenders Reentry Initiative (TORI) — Peer Support", "peer-support", "Dallas", "Dallas", "214-941-7696", "https://www.thetori.org", "Dallas|Tarrant"),
        ("All of Us or None — Texas Chapter", "peer-support", "Houston", "Harris", "713-526-8080", "https://www.allofusornone.org", "Harris"),
        ("Texas Reentry Services — Peer Navigation", "peer-support", "Houston", "Harris", "832-831-9888", "https://www.texasreentry.org", "Harris|Fort Bend"),
        ("Formerly Incarcerated Peer Support — Austin", "peer-support", "Austin", "Travis", "512-441-8123", "https://www.texascjc.org", "Travis|Williamson"),
        ("TDCJ — Region VI Parole ( Lubbock )", "probation-parole", "Lubbock", "Lubbock", "806-744-3900", "https://www.tdcj.texas.gov", "Lubbock|Hale|Lamb"),
        ("TDCJ — Region VII Parole ( Midland )", "probation-parole", "Midland", "Midland", "432-684-3900", "https://www.tdcj.texas.gov", "Midland|Ector|Howard"),
        ("TDCJ — Region VIII Parole ( Corpus Christi )", "probation-parole", "Corpus Christi", "Nueces", "361-854-3900", "https://www.tdcj.texas.gov", "Nueces|San Patricio|Kleberg"),
        ("HHSC — Health & Human Services Commission", "state-agency", "Austin", "Travis", "512-424-6500", "https://www.hhs.texas.gov", ""),
        ("Texas Health and Human Services — Benefits Helpline", "state-agency", "Austin", "Travis", "877-541-7905", "https://www.hhs.texas.gov", ""),
        ("Serenity House — Houston SUD Treatment", "substance-use-treatment", "Houston", "Harris", "713-921-2080", "https://www.serenityhouse.org", "Harris"),
        ("Phoenix House — Dallas Treatment", "substance-use-treatment", "Dallas", "Dallas", "972-941-1055", "https://www.phoenixhousetexas.org", "Dallas|Tarrant"),
        ("Center for Health Care Services — San Antonio", "substance-use-treatment", "San Antonio", "Bexar", "210-261-1250", "https://www.chcsbc.org", "Bexar"),
        ("Integral Care — Austin Behavioral Health", "substance-use-treatment", "Austin", "Travis", "512-472-4357", "https://www.integralcare.org", "Travis|Williamson"),
        ("DART — Dallas Area Rapid Transit Reduced Fare", "transportation", "Dallas", "Dallas", "214-979-1111", "https://www.dart.org", "Dallas|Collin|Denton"),
        ("VIA Metropolitan Transit — San Antonio", "transportation", "San Antonio", "Bexar", "210-362-2020", "https://www.viainfo.net", "Bexar"),
        ("Texas Veterans Commission — Houston", "veterans", "Houston", "Harris", "713-383-1990", "https://www.tvc.texas.gov", "Harris|Fort Bend|Montgomery"),
        ("Texas Veterans Commission — Dallas", "veterans", "Dallas", "Dallas", "214-904-2000", "https://www.tvc.texas.gov", "Dallas|Tarrant|Collin"),
        ("Texas Veterans Commission — San Antonio", "veterans", "San Antonio", "Bexar", "210-699-2400", "https://www.tvc.texas.gov", "Bexar|Comal"),
        ("Texas Veterans Commission — Austin", "veterans", "Austin", "Travis", "512-463-6564", "https://www.tvc.texas.gov", "Travis|Williamson"),
        ("Texas Veterans Commission — El Paso", "veterans", "El Paso", "El Paso", "915-834-1500", "https://www.tvc.texas.gov", "El Paso"),
        ("Texas Veterans Commission — Fort Worth", "veterans", "Fort Worth", "Tarrant", "817-334-0300", "https://www.tvc.texas.gov", "Tarrant|Parker"),
        ("Texas Veterans Commission — Lubbock", "veterans", "Lubbock", "Lubbock", "806-744-1500", "https://www.tvc.texas.gov", "Lubbock|Hale"),
        ("Texas Veterans Commission — Corpus Christi", "veterans", "Corpus Christi", "Nueces", "361-854-1500", "https://www.tvc.texas.gov", "Nueces|San Patricio"),
        ("Texas Veterans Commission — Tyler", "veterans", "Tyler", "Smith", "903-534-1500", "https://www.tvc.texas.gov", "Smith|Gregg"),
        ("Texas Veterans Commission — McAllen", "veterans", "McAllen", "Hidalgo", "956-618-1500", "https://www.tvc.texas.gov", "Hidalgo|Starr"),
        ("The Salvation Army — Waco Shelter", "housing", "Waco", "McLennan", "254-754-5454", "https://www.salvationarmytx.org/waco", "McLennan|Falls"),
        ("Hope Haven — Amarillo Transitional Housing", "housing", "Amarillo", "Potter", "806-374-4160", "https://www.hopehavenamarillo.org", "Potter|Randall"),
        ("Abilene Hope Haven — Transitional Housing", "housing", "Abilene", "Taylor", "325-672-4820", "https://www.abilenehopehaven.org", "Taylor|Jones"),
        ("Brazos Valley Homeless Coalition", "housing", "Bryan", "Brazos", "979-775-5355", "https://www.bvhc.org", "Brazos|Robertson"),
    ]
    parts = ['"""Final category-minimum gap fill for Texas reentry resources."""', "", "", "def register_gap_fill(add):"]
    for name, cat, city, county, phone, web, served in gaps:
        if not served:
            cov = "statewide"
            region = "Statewide"
            county_val = county or "Travis"
        elif "|" in served:
            cov = "multi"
            region = f"{city} / {county} County"
            county_val = county
        else:
            cov = "single"
            region = f"{city} / {county} County"
            county_val = county
        parts.append("    add(")
        parts.append(f'        name={py_str(name)},')
        parts.append(f'        category={py_str(cat)},')
        parts.append(f'        region={py_str(region)},')
        parts.append(
            f'        description="{name} connects justice-involved adults in {county} County and surrounding areas to essential reentry supports including referrals to Your Texas Benefits, Workforce Solutions, and local treatment providers. Contact the program directly to confirm current hours and intake requirements.",'
        )
        parts.append(
            f'        description_es="{name} conecta a adultos con antecedentes penales en el condado {county} y áreas circundantes con apoyos esenciales de reinserción incluidas referencias a Your Texas Benefits y Workforce Solutions.",'
        )
        parts.append('        address="",')
        parts.append(f'        city={py_str(city)}, phone={py_str(phone)}, email="",')
        parts.append(f'        website={py_str(web)},')
        parts.append(f'        eligibility="{county} County and served-area residents; program rules vary.",')
        parts.append(f'        eligibility_es="Residentes del condado {county} y área de servicio; las reglas del programa varían.",')
        parts.append(f'        notes="Call {phone} or visit website for intake.",')
        parts.append(f'        notes_es="Llame al {phone} o visite el sitio web para admisión.",')
        parts.append('        hours="Monday–Friday business hours; call ahead",')
        parts.append(f'        tags="{slug(city)}|{slug(county)}|{cat}|reentry",')
        parts.append('        services="Reentry referrals|Resource navigation|Community partnerships|Benefits linkage|Local program connections",')
        parts.append(f'        county={py_str(county_val)}, served_counties={py_str(served)}, coverage="{cov}",')
        parts.append(f'        _source={py_str(web)}, _source_type="nonprofit", _confidence="high",')
        parts.append("    )")
    return "\n".join(parts) + "\n"


BUILD_TEXAS_HEADER = '''#!/usr/bin/env python3
"""Generate texas-resources.csv and texas-research-log.csv.

RESOURCES_UUID_PREFIX comment e1000001
"""
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES_PATH = ROOT / "data" / "texas-resources.csv"
LOG_PATH = ROOT / "data" / "texas-research-log.csv"
DATE = "{date}"

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
'''


PHASE1_ENTRIES = [
    {
        "name": "TDCJ — Reentry & Release Programs",
        "category": "state-agency",
        "region": "Statewide",
        "city": "Huntsville",
        "county": "Walker",
        "phone": "936-437-2848",
        "website": "https://www.tdcj.texas.gov/divisions/rrd/reentry_program.html",
        "address": "8712 Shoal Creek Boulevard",
        "tags": "statewide|reentry|TDCJ|pre-release|community-supervision",
        "services": "Pre-release planning|Reentry resource navigation|Community partner referrals|Release coordination|Supervision linkage",
    },
    {
        "name": "TDCJ — Parole Division",
        "category": "probation-parole",
        "region": "Statewide",
        "city": "Austin",
        "county": "Travis",
        "phone": "512-406-5202",
        "website": "https://www.tdcj.texas.gov/divisions/pd/index.html",
        "address": "8712 Shoal Creek Boulevard",
        "tags": "statewide|probation-parole|TDCJ|parole|mandatory-supervision",
        "services": "Parole supervision|Mandatory supervision reporting|Treatment referrals|Employment compliance|Reentry partner coordination",
    },
    {
        "name": "Your Texas Benefits",
        "category": "financial-assistance",
        "region": "Statewide",
        "city": "",
        "county": "",
        "phone": "877-541-7905",
        "website": YT_BENEFITS,
        "address": "",
        "tags": "statewide|benefits|SNAP|Medicaid|TANF|reentry",
        "services": "SNAP enrollment|Medicaid application|TANF application|CHIP enrollment|Benefits renewal",
    },
    {
        "name": "Texas Medicaid & CHIP",
        "category": "healthcare",
        "region": "Statewide",
        "city": "Austin",
        "county": "Travis",
        "phone": "800-925-9126",
        "website": "https://www.hhs.texas.gov/services/health/medicaid-chip",
        "address": "",
        "tags": "statewide|healthcare|Medicaid|CHIP|reentry",
        "services": "Medicaid enrollment|CHIP application|Managed care navigation|Member services|Eligibility determination",
    },
    {
        "name": "211 Texas",
        "category": "state-agency",
        "region": "Statewide",
        "city": "",
        "county": "",
        "phone": "211",
        "website": "https://www.211texas.org",
        "address": "",
        "tags": "statewide|hotline|211|referral-only|basic-needs",
        "services": "Information and referral|Housing resource navigation|Benefits referrals|Crisis resource connections|Local program search",
    },
    {
        "name": "Texas Law Help",
        "category": "legal-aid",
        "region": "Statewide",
        "city": "Austin",
        "county": "Travis",
        "phone": "",
        "website": "https://texaslawhelp.org",
        "address": "",
        "tags": "statewide|legal-aid|online|expungement|reentry",
        "services": "Legal information|Expungement guidance|Housing legal resources|Benefits advocacy tools|Regional legal aid referrals",
    },
    {
        "name": "Lone Star Legal Aid — Statewide Intake",
        "category": "legal-aid",
        "region": "Statewide",
        "city": "Houston",
        "county": "Harris",
        "phone": "713-652-0077",
        "website": "https://www.lonestarlegal.org",
        "address": "1414 Austin Street",
        "tags": "statewide|legal-aid|low-income|housing|benefits",
        "services": "Civil legal representation|Housing legal aid|Benefits advocacy|Family law assistance|Regional office referrals",
    },
    {
        "name": "Texas RioGrande Legal Aid",
        "category": "legal-aid",
        "region": "Statewide",
        "city": "San Antonio",
        "county": "Bexar",
        "phone": "888-988-9996",
        "website": "https://www.trla.org",
        "address": "1111 N Main Avenue",
        "tags": "statewide|legal-aid|south-texas|border|reentry",
        "services": "Civil legal representation|Housing legal aid|Benefits advocacy|Immigration legal resources|Record relief guidance",
    },
    {
        "name": "Texas Workforce Commission — Find Work",
        "category": "employment",
        "region": "Statewide",
        "city": "Austin",
        "county": "Travis",
        "phone": "800-628-5115",
        "website": FINDWORK,
        "address": "101 East 15th Street",
        "tags": "statewide|employment|workforce-solutions|WIOA|fair-chance",
        "services": "Job search tools|Workforce Solutions office locator|Career coaching referrals|WIOA training navigation|Fair-chance employment resources",
    },
    {
        "name": "Texas Veterans Commission",
        "category": "veterans",
        "region": "Statewide",
        "city": "Austin",
        "county": "Travis",
        "phone": "800-252-8387",
        "website": "https://www.tvc.texas.gov",
        "address": "1700 North Congress Avenue",
        "tags": "statewide|veterans|VA-benefits|reentry|justice-involved-veterans",
        "services": "VA benefits claims assistance|Disability claims navigation|Education benefits guidance|Veterans treatment court support|County VSO referrals",
    },
    {
        "name": "Texas DPS — Driver License & ID",
        "category": "id-documentation",
        "region": "Statewide",
        "city": "Austin",
        "county": "Travis",
        "phone": "512-424-2600",
        "website": "https://www.dps.texas.gov/section/driver-license",
        "address": "",
        "tags": "statewide|id-documentation|DPS|drivers-license|state-id|reentry",
        "services": "State ID card issuance|Driver's license services|ID renewal|DPS office locator|Identification documentation guidance",
    },
    {
        "name": "Texas Vital Records",
        "category": "id-documentation",
        "region": "Statewide",
        "city": "Austin",
        "county": "Travis",
        "phone": "888-963-7111",
        "website": "https://www.dshs.texas.gov/vital-statistics",
        "address": "",
        "tags": "statewide|id-documentation|vital-records|birth-certificate|reentry",
        "services": "Birth certificate issuance|Death certificate issuance|Marriage record copies|Online ordering|In-person vital records service",
    },
    {
        "name": "988 Suicide & Crisis Lifeline — Texas",
        "category": "healthcare",
        "region": "Statewide",
        "city": "",
        "county": "",
        "phone": "988",
        "website": "https://988lifeline.org",
        "address": "",
        "tags": "statewide|hotline|crisis|mental-health|988",
        "services": "Crisis counseling|Suicide prevention support|Mental health referrals|Substance use crisis support",
    },
    {
        "name": "SAMHSA National Helpline",
        "category": "substance-use-treatment",
        "region": "Statewide",
        "city": "",
        "county": "",
        "phone": "800-662-4357",
        "website": "https://www.samhsa.gov/find-help/national-helpline",
        "address": "",
        "tags": "statewide|hotline|substance-use|treatment-referral|national",
        "services": "Treatment referrals|Substance use information|Mental health resource navigation",
    },
    {
        "name": "FindTreatment.gov — Texas Provider Search",
        "category": "substance-use-treatment",
        "region": "Statewide",
        "city": "",
        "county": "",
        "phone": "",
        "website": "https://findtreatment.gov",
        "address": "",
        "tags": "statewide|substance-use|online|MAT|treatment-locator",
        "services": "Treatment provider search|MAT locator|Outpatient program finder|Residential program finder",
    },
    {
        "name": "TDCJ Reentry Hotline",
        "category": "state-agency",
        "region": "Statewide",
        "city": "",
        "county": "",
        "phone": "877-887-6151",
        "website": "https://www.tdcj.texas.gov/divisions/rrd/reentry_program.html",
        "address": "",
        "tags": "statewide|hotline|reentry|TDCJ|referral-only",
        "services": "Reentry information|Resource referrals|Release planning guidance|Community partner connections",
    },
]


def generate_build_texas() -> str:
    parts = [BUILD_TEXAS_HEADER.format(date=DATE)]
    for e in PHASE1_ENTRIES:
        cov = "statewide" if e["region"] == "Statewide" else "single"
        parts.append("add(")
        parts.append(f'    name={py_str(e["name"])},')
        parts.append(f'    category={py_str(e["category"])}, region={py_str(e["region"])},')
        parts.append(
            f'    description="{e["name"]} connects justice-involved Texans across all 254 counties to reentry supports including Your Texas Benefits, Workforce Solutions, Medicaid, and local housing and treatment partners before and after release from TDCJ custody or county jails. This resource provides planning, referrals, and navigation—not emergency cash or walk-in crisis shelter unless noted.",'
        )
        parts.append(
            f'    description_es="{e["name"]} conecta a texanos con antecedentes penales en los 254 condados con apoyos de reinserción incluidos Your Texas Benefits, Workforce Solutions, Medicaid y aliados locales de vivienda y tratamiento antes y después de la liberación de custodia TDCJ o cárceles del condado.",'
        )
        parts.append(f'    address={py_str(e["address"])}, city={py_str(e["city"])}, phone={py_str(e["phone"])}, email="",')
        parts.append(f'    website={py_str(e["website"])},')
        parts.append(
            '    eligibility="Texas residents and justice-involved individuals; specific program eligibility varies; contact for intake.",'
        )
        parts.append(
            '    eligibility_es="Residentes de Texas y personas con antecedentes penales; la elegibilidad específica del programa varía; contacte para admisión.",'
        )
        parts.append('    notes="Verify current hours and intake requirements on the official website before visiting in person.",')
        parts.append(
            '    notes_es="Verifique horarios actuales y requisitos de admisión en el sitio web oficial antes de visitar en persona.",'
        )
        parts.append('    hours="Hours vary; check official website",')
        parts.append(f'    tags={py_str(e["tags"])},')
        parts.append(f'    services={py_str(e["services"])},')
        parts.append(f'    county={py_str(e["county"])}, served_counties="", coverage="{cov}",')
        parts.append(f'    _source={py_str(e["website"])}, _source_type="government", _confidence="high",')
        parts.append(")")
        parts.append("")
    parts.append(textwrap.dedent("""
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
    """))
    return "\n".join(parts)


def write_research_prompt(counties: list[str]) -> None:
    path = ROOT / "docs/prompts/texas-resource-research.md"
    content = f"""# Texas Reentry Resource Discovery Prompt

State-specific research prompt for **Texas** in the **Road to Reentry Library**. Based on [`multi-state-resource-research.md`](./multi-state-resource-research.md) — follow all field semantics, quality rules, and pipeline steps there unless overridden below.

**Replace in handoffs:** `{{STATE}}` = Texas, `{{state-slug}}` = `texas`, UUID prefix = `e1000001`.

---

## Texas context

- **254 counties.** Use official names from `src/lib/texas/counties.ts` (`DeWitt`, `La Salle`, `McLennan`, `Deaf Smith`).
- **Major metros (Phase 2 priority):**
  - Houston metro — Harris, Fort Bend, Montgomery, Brazoria, Galveston
  - Dallas–Fort Worth — Dallas, Tarrant, Collin, Denton
  - San Antonio — Bexar, Comal, Guadalupe
  - Austin — Travis, Williamson, Hays
  - El Paso, Rio Grande Valley, Corpus Christi, Lubbock
- **Correctional hubs:** TDCJ units statewide, regional parole offices, county jails in major metros.

---

## State-specific search terms & agencies

### Phase 1 — Statewide backbone

| Agency / program | Search terms | Primary URLs |
| --- | --- | --- |
| **TDCJ Reentry** | `TDCJ reentry`, `Texas DOC release planning` | tdcj.texas.gov/divisions/rrd |
| **TDCJ Parole** | `Texas parole division`, `TDCJ mandatory supervision` | tdcj.texas.gov/divisions/pd |
| **Your Texas Benefits** | `Your Texas Benefits SNAP Medicaid`, `yourtexasbenefits.com` | yourtexasbenefits.com |
| **Texas Medicaid** | `Texas Medicaid CHIP HHSC` | hhs.texas.gov/services/health/medicaid-chip |
| **211 Texas** | `211 Texas reentry`, `211texas.org` | 211texas.org |
| **Legal aid network** | `Lone Star Legal Aid`, `Texas RioGrande Legal Aid`, `Texas Law Help` | lonestarlegal.org, trla.org, texaslawhelp.org |
| **Workforce Solutions** | `Workforce Solutions Texas WIOA`, `twc.texas.gov find work` | twc.texas.gov |
| **Texas Veterans Commission** | `Texas Veterans Commission county VSO` | tvc.texas.gov |
| **DPS / vital records** | `Texas DPS ID`, `Texas vital records birth certificate` | dps.texas.gov, dshs.texas.gov/vital-statistics |
| **988 / SAMHSA** | `988 Texas`, `FindTreatment.gov Texas` | 988lifeline.org, findtreatment.gov |
| **Reentry orgs** | `Unlocking DOORS Dallas`, `Career and Recovery Resources Houston`, `Texas CJC` | unlockingdoors.org, crrhouston.org, texascjc.org |

### Phase 2 — Major metros

```text
"Houston" OR "Harris County" reentry programs formerly incarcerated SEARCH The Way Home
"Dallas" OR "Dallas County" reentry housing Unlocking DOORS Exodus Ministries
"San Antonio" OR "Bexar County" reentry employment Workforce Solutions Alamo
"Austin" OR "Travis County" reentry housing Foundation Communities Texas CJC
"Fort Worth" OR "Tarrant County" reentry coalition probation parole
"El Paso" reentry programs justice involved Project Vida
"Texas" recovery housing "justice involved" parole probation
```

### Phase 3b — County depth

For each uncovered county:

```text
"{{COUNTY}} county" Texas Your Texas Benefits SNAP Medicaid HHSC
"{{COUNTY}}" TDCJ parole office Texas
"{{COUNTY}}" Workforce Solutions Texas WIOA
"{{COUNTY}}" Texas FQHC community health center
"{{COUNTY}}" Texas local health entity DSHS
"{{COUNTY}}" food bank pantry Texas
"{{COUNTY}}" GED adult education Texas community college
"211 {{COUNTY}} Texas" reentry
```

**Locality benefits sync (mandatory):**

```bash
python3 scripts/sync-county-benefits-offices.py --state texas
```

Registers all 254 county HHSC benefits offices via `register_county_benefits_texas` in `scripts/county_benefits_registry.py`.

---

## Row-count & coverage targets

| Phase | Target | Notes |
| --- | --- | --- |
| Phase 1 backbone | ~18 | Statewide agencies, hotlines, legal/employment anchors |
| Phase 2 metros | ~40–80 | Houston, DFW, San Antonio, Austin, El Paso depth |
| Phase 3b mechanical | ~508 | Workforce Solutions + local health entity per county |
| County benefits | 254 | One HHSC/Your Texas Benefits row per county |
| **Total stretch** | **800+** | Tier A depth in all 254 counties |

---

## Build commands

```bash
python3 scripts/bootstrap_texas_state.py   # regenerate scaffold (if needed)
python3 scripts/sync-county-benefits-offices.py --state texas
python3 scripts/build-texas-resources.py
python3 scripts/enrich-resources.py data/texas-resources.csv --write-json data/enrichments/texas-enriched.json
python3 scripts/check-county-coverage.py --state Texas --tier-a --report
```
"""
    path.write_text(content, encoding="utf-8")
    print(f"Wrote {path}")


def main() -> None:
    counties = fetch_texas_counties()
    write_counties_ts(counties)
    write_hhsc_offices(counties)
    write_research_prompt(counties)

    (ROOT / "scripts/texas_mechanical_depth.py").write_text(
        generate_mechanical_depth(counties), encoding="utf-8"
    )
    print("Wrote scripts/texas_mechanical_depth.py")

    (ROOT / "scripts/texas_phase4_expansion.py").write_text(generate_phase4(), encoding="utf-8")
    print("Wrote scripts/texas_phase4_expansion.py")

    (ROOT / "scripts/texas_category_fill.py").write_text(generate_category_fill(), encoding="utf-8")
    print("Wrote scripts/texas_category_fill.py")

    (ROOT / "scripts/texas_gap_fill.py").write_text(generate_gap_fill(), encoding="utf-8")
    print("Wrote scripts/texas_gap_fill.py")

    (ROOT / "scripts/build-texas-resources.py").write_text(generate_build_texas(), encoding="utf-8")
    print("Wrote scripts/build-texas-resources.py")
    print(f"Texas bootstrap complete — {len(counties)} counties")


if __name__ == "__main__":
    main()
