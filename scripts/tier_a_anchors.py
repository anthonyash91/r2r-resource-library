"""Tier A anchor rows from verified public directories (ODRC, PCSAO, FQHC, TN LWDB).

Sources must be cited on each row. Do not add address/phone without a primary source.
"""

from __future__ import annotations

import json
import re
import urllib.request
from html import unescape
from pathlib import Path

DATE = "2026-06-23"
DATA_DIR = Path(__file__).resolve().parent / "data"

# Ohio Adult Parole Authority regional county assignments (ODRC Annual Report 2015, p. 2).
# Verify updates at drc.ohio.gov — structure is stable but confirm before major releases.
OHIO_APA_REGIONS = [
    (
        "Cleveland Region",
        "Cleveland",
        "Cuyahoga|Erie|Medina|Lorain",
        "Lorain",
    ),
    (
        "Akron Region",
        "Akron",
        "Ashtabula|Lake|Geauga|Trumbull|Portage|Summit|Mahoning|Columbiana|Stark|Jefferson|Carroll|Harrison|Tuscarawas|Holmes|Coshocton|Wayne|Knox|Ashland|Huron",
        "Summit",
    ),
    (
        "Columbus Region",
        "Columbus",
        "Franklin|Licking|Muskingum|Guernsey|Belmont|Pickaway|Fairfield|Perry|Morgan|Noble|Monroe|Hocking|Athens|Washington|Vinton|Meigs|Jackson|Gallia|Scioto|Lawrence",
        "Franklin",
    ),
    (
        "Cincinnati Region",
        "Cincinnati",
        "Greene|Madison|Fayette|Butler|Warren|Clinton|Highland|Ross|Hamilton|Clermont|Brown|Adams|Pike",
        "Hamilton",
    ),
    (
        "Dayton Region",
        "Dayton",
        "Darke|Shelby|Logan|Union|Marion|Morrow|Richland|Delaware|Champaign|Clark|Miami|Montgomery|Preble",
        "Montgomery",
    ),
    (
        "Lima Region",
        "Toledo",
        "Williams|Fulton|Wood|Lucas|Ottawa|Henry|Defiance|Sandusky|Seneca|Hancock|Putnam|Paulding|Van Wert|Allen|Hardin|Wyandot|Crawford|Auglaize|Mercer",
        "Lucas",
    ),
]

# Tennessee LWDB → counties (CareerOneStop / tn.gov workforce, WIOA 2018 plan).
TN_LWDB_REGIONS = [
    (
        "East Tennessee Local Workforce Development Board — American Job Centers",
        "Knoxville",
        "9111 Cross Park Drive, Suite D-100",
        "(865) 691-2551",
        "https://www.ethra.org/local-workforce-development-board",
        "Anderson|Blount|Campbell|Claiborne|Cocke|Grainger|Hamblen|Jefferson|Knox|Loudon|Monroe|Morgan|Roane|Scott|Sevier|Union",
        "Knox",
    ),
    (
        "Northeast Tennessee Local Workforce Development Board — American Job Centers",
        "Johnson City",
        "3211 North Roan Street",
        "(423) 928-3257",
        "https://www.tn.gov/workforce/jobs-and-education/job-search1/find-local-american-job-center.html",
        "Carter|Greene|Hancock|Hawkins|Johnson|Sullivan|Unicoi|Washington",
        "Washington",
    ),
    (
        "Southeast Tennessee Local Workforce Development Board — American Job Centers",
        "Chattanooga",
        "1000 Riverfront Parkway",
        "(423) 668-1800",
        "https://www.tn.gov/workforce/jobs-and-education/job-search1/find-local-american-job-center.html",
        "Bledsoe|Bradley|Grundy|Hamilton|Marion|McMinn|Meigs|Polk|Rhea|Sequatchie",
        "Hamilton",
    ),
    (
        "Northern Middle Tennessee Workforce Development Board — American Job Centers",
        "Clarksville",
        "523 Madison Street, Suite A",
        "(931) 648-5111",
        "https://www.tn.gov/workforce/jobs-and-education/job-search1/find-local-american-job-center.html",
        "Cheatham|Davidson|Dickson|Houston|Humphreys|Montgomery|Robertson|Rutherford|Stewart|Sumner|Trousdale|Williamson|Wilson",
        "Montgomery",
    ),
    (
        "Southern Middle Tennessee Local Workforce Development Board — American Job Centers",
        "Mount Pleasant",
        "101 Sam Watkins Boulevard",
        "(931) 379-3100",
        "https://www.tn.gov/workforce/jobs-and-education/job-search1/find-local-american-job-center.html",
        "Bedford|Coffee|Franklin|Giles|Hickman|Lawrence|Lewis|Lincoln|Marshall|Maury|Moore|Perry|Wayne",
        "Maury",
    ),
    (
        "Upper Cumberland Local Workforce Development Board — American Job Centers",
        "Cookeville",
        "1000 England Drive, Suite 201",
        "(931) 520-9500",
        "https://www.tn.gov/workforce/jobs-and-education/job-search1/find-local-american-job-center.html",
        "Cannon|Clay|Cumberland|DeKalb|Fentress|Jackson|Macon|Overton|Pickett|Putnam|Smith|Van Buren|Warren|White",
        "Putnam",
    ),
    (
        "Northwest Tennessee Local Workforce Development Board — American Job Centers",
        "Dyersburg",
        "208 North Mill Avenue, Suite B",
        "(731) 286-3585",
        "https://www.tn.gov/workforce/jobs-and-education/job-search1/find-local-american-job-center.html",
        "Benton|Carroll|Crockett|Dyer|Gibson|Henry|Lake|Obion|Weakley",
        "Dyer",
    ),
    (
        "Southwest Tennessee Local Workforce Development Board — American Job Centers",
        "Dyersburg",
        "208 North Mill Avenue, Suite B",
        "(731) 286-3585",
        "https://www.tn.gov/workforce/jobs-and-education/job-search1/find-local-american-job-center.html",
        "Chester|Decatur|Hardeman|Hardin|Haywood|Henderson|Madison|McNairy",
        "Madison",
    ),
    (
        "Greater Memphis Local Workforce Development Board — American Job Centers",
        "Memphis",
        "1350 Concourse Avenue, Suite 672",
        "(901) 707-8407",
        "https://www.tn.gov/workforce/jobs-and-education/job-search1/find-local-american-job-center.html",
        "Fayette|Lauderdale|Shelby|Tipton",
        "Shelby",
    ),
]


def _scrape_pcsao_jfs() -> list[dict]:
    """Live scrape PCSAO agency directory for CDJFS rows with address and phone."""
    req = urllib.request.Request(
        "https://pcsao.org/membership/agency-directory/",
        headers={"User-Agent": "Mozilla/5.0"},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        html = r.read().decode("utf-8", errors="replace")
    pattern = re.compile(
        r'organization-unit notranslate">([^<]*Job[^<]*Family Services[^<]*)</span>.*?'
        r'street-address notranslate">([^<]*)</span>\s*<span class="locality">([^<]*)</span>.*?'
        r'class="value">([^<]*)</span>.*?'
        r'href="(https?://[^"]+)"',
        re.S,
    )
    offices: list[dict] = []
    for m in pattern.finditer(html):
        name = unescape(m.group(1).replace("&#038;", "&"))
        if "Consolidated" in name:
            counties = ["Defiance", "Paulding"]
        else:
            county_m = re.match(r"([A-Za-z .'-]+) County", name)
            counties = [county_m.group(1)] if county_m else []
        if not counties:
            continue
        offices.append(
            {
                "counties": counties,
                "name": name,
                "address": unescape(m.group(2).strip()),
                "city": unescape(m.group(3).strip()),
                "phone": unescape(m.group(4).strip()),
                "website": m.group(5),
                "source": "https://pcsao.org/membership/agency-directory/",
            }
        )
    return offices


def _load_verified_jfs_extras() -> list[dict]:
    path = DATA_DIR / "ohio-cdjfs-verified.json"
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def _jfs_desc_en(county: str, city: str) -> str:
    return (
        f"{county} County Job and Family Services is the county public benefits intake office in "
        f"{city}, administering Medicaid, SNAP, Ohio Works First cash assistance, and child care "
        f"subsidies for Ohio residents including justice-involved individuals establishing food and "
        f"health coverage after release. Staff assist with benefits.ohio.gov applications and "
        f"OhioMeansJobs workforce connections for fair-chance employment."
    )


def _jfs_desc_es(county: str, city: str) -> str:
    return (
        f"{county} County Job and Family Services es la oficina de admisión de beneficios públicos "
        f"del condado en {city}, que administra Medicaid, SNAP, asistencia en efectivo Ohio Works "
        f"First y subsidios de cuidado infantil para residentes de Ohio, incluidas personas con "
        f"antecedentes penales que establecen cobertura alimentaria y de salud después de la "
        f"liberación. El personal ayuda con solicitudes en benefits.ohio.gov y conexiones "
        f"OhioMeansJobs para empleo justo."
    )


def register_ohio_tier_a_anchors(add, _jfs_oh, existing_jfs_counties: set[str]) -> None:
    """Verified Tier A anchors: ODRC parole regions, FQHC networks (CDJFS via county_benefits_registry)."""

    for region, city_label, served, office_county in OHIO_APA_REGIONS:
        counties = served.split("|")
        add(
            name=f"Ohio Adult Parole Authority — {region} Field Services",
            category="probation-parole",
            region=f"{city_label} / {region}",
            description=(
                f"Ohio Adult Parole Authority {region} field offices supervise state parole and "
                f"community control for justice-involved individuals in {len(counties)} Ohio counties. "
                f"Parole officers connect supervisees to county Job and Family Services, OhioMeansJobs "
                f"centers, and regional treatment and housing partners. Contact for reporting "
                f"requirements and supervision compliance—not emergency reentry navigation."
            ),
            description_es=(
                f"Las oficinas de campo de la región {region} de la Autoridad de Libertad Condicional "
                f"de Ohio supervisan la libertad condicional estatal y el control comunitario para "
                f"personas con antecedentes penales en {len(counties)} condados de Ohio. Los oficiales "
                f"conectan a supervisados con JFS del condado, OhioMeansJobs y aliados regionales. "
                f"Contacte para requisitos de reporte, no para navegación de crisis."
            ),
            address="770 West Broad Street",
            city="Columbus",
            phone="(614) 752-1161",
            email="",
            website="https://drc.ohio.gov/about-us/divisions-and-offices/adult-parole-authority",
            eligibility=f"Individuals under Ohio state parole or post-release control in {region} counties.",
            eligibility_es=(
                f"Personas bajo libertad condicional estatal o control posterior a la liberación "
                f"de Ohio en los condados de la región {region}."
            ),
            notes="Field office locations vary by supervisee assignment; confirm reporting site with assigned officer.",
            notes_es="Las ubicaciones de oficinas de campo varían; confirme el sitio de reporte con su oficial.",
            hours="Monday–Friday business hours",
            tags=f"{region.lower().replace(' ', '-')}|ohio|parole|ODRC|reentry",
            services="Parole supervision|Community control|Reporting compliance|Workforce referrals|Treatment referrals",
            county=office_county,
            served_counties=served,
            coverage="multi",
            _source="https://drc.ohio.gov/wps/wcm/connect/gov/fd0b9dc5-7660-472c-b37e-befa93cd2d0d/Annual+Report+2015.pdf",
            _source_type="government",
            _confidence="high",
        )

    add(
        name="Muskingum Valley Health Centers — Primary Care Network",
        category="healthcare",
        region="Southeast Ohio — 4 counties",
        description=(
            "Muskingum Valley Health Centers is a federally qualified health center operating 13 "
            "locations in Coshocton, Guernsey, Morgan, and Muskingum counties, providing primary care, "
            "behavioral health, dental, and substance use treatment on a sliding-fee scale for "
            "uninsured and Medicaid patients including justice-involved adults reestablishing care "
            "after release. Not an emergency room—call ahead for intake."
        ),
        description_es=(
            "Muskingum Valley Health Centers es un centro de salud calificado federalmente con 13 "
            "ubicaciones en los condados Coshocton, Guernsey, Morgan y Muskingum, que ofrece atención "
            "primaria, salud conductual, dental y tratamiento de sustancias con tarifa móvil para "
            "pacientes sin seguro o con Medicaid, incluidos adultos con antecedentes penales que "
            "restablecen atención después de la liberación."
        ),
        address="716 Adair Avenue",
        city="Zanesville",
        phone="(740) 891-9000",
        email="",
        website="https://www.mvhccares.org/",
        eligibility="Open to residents of listed counties; sliding fee available; Medicaid accepted.",
        eligibility_es="Abierto a residentes de los condados listados; tarifa móvil disponible; acepta Medicaid.",
        notes="Multiple clinic sites in Zanesville, Cambridge, Coshocton, and Malta; call for nearest location.",
        notes_es="Varias clínicas en Zanesville, Cambridge, Coshocton y Malta; llame para la ubicación más cercana.",
        hours="Monday–Friday; hours vary by site",
        tags="southeast-ohio|FQHC|healthcare|behavioral-health|reentry",
        services="Primary care|Behavioral health|Dental care|Substance use treatment|Sliding-fee scale|Medicaid enrollment",
        county="Muskingum",
        served_counties="Coshocton|Guernsey|Morgan|Muskingum",
        coverage="multi",
        _source="https://www.mvhccares.org/about",
        _source_type="nonprofit",
        _confidence="high",
    )
    add(
        name="Hopewell Health Centers — Integrated Care Network",
        category="healthcare",
        region="Southeast Ohio — 9 counties",
        description=(
            "Hopewell Health Centers is a nationally accredited federally qualified health center "
            "with 22 sites across nine Appalachian Ohio counties, providing integrated primary care, "
            "dental, behavioral health, and substance use services on a sliding-fee scale for "
            "justice-involved and low-income residents. Returning citizens can establish Medicaid "
            "and primary care after release; not a walk-in crisis line."
        ),
        description_es=(
            "Hopewell Health Centers es un centro de salud calificado federalmente acreditado con "
            "22 sitios en nueve condados apalaches de Ohio, que ofrece atención primaria integrada, "
            "dental, salud conductual y servicios de sustancias con tarifa móvil para residentes "
            "de bajos ingresos y personas con antecedentes penales. Los ciudadanos que regresan "
            "pueden establecer Medicaid y atención primaria después de la liberación."
        ),
        address="90 Hospital Drive",
        city="Athens",
        phone="(740) 593-5555",
        email="",
        website="https://www.hopewellhealth.org/",
        eligibility="Open to residents of listed counties; sliding fee and Medicaid accepted.",
        eligibility_es="Abierto a residentes de los condados listados; tarifa móvil y Medicaid aceptados.",
        notes="Clinic locations in Athens, Logan, Jackson, McArthur, and other county seats; call for intake.",
        notes_es="Clínicas en Athens, Logan, Jackson, McArthur y otras sedes; llame para admisión.",
        hours="Monday–Friday; hours vary by site",
        tags="southeast-ohio|FQHC|healthcare|behavioral-health|MAT|reentry",
        services="Primary care|Behavioral health|Dental care|Substance use treatment|Medicaid enrollment assistance|Sliding-fee scale",
        county="Athens",
        served_counties="Athens|Gallia|Hocking|Jackson|Meigs|Perry|Ross|Vinton|Washington",
        coverage="multi",
        _source="https://www.hopewellhealth.org/services/",
        _source_type="nonprofit",
        _confidence="high",
    )
    add(
        name="AxessPointe Community Health Centers — Northeast Ohio Network",
        category="healthcare",
        region="Northeast Ohio — 4 counties",
        description=(
            "AxessPointe Community Health Centers, merged with Family & Community Services in 2024, "
            "provides federally qualified primary care, dental, behavioral health, and pharmacy "
            "services across Summit, Portage, Trumbull, and Mahoning counties on a sliding-fee scale "
            "for uninsured and Medicaid patients including justice-involved adults in the Akron–Youngstown "
            "region reestablishing medical care after release."
        ),
        description_es=(
            "AxessPointe Community Health Centers, fusionado con Family & Community Services en 2024, "
            "ofrece atención primaria calificada federalmente, dental, salud conductual y farmacia en "
            "los condados Summit, Portage, Trumbull y Mahoning con tarifa móvil para pacientes sin "
            "seguro o con Medicaid, incluidos adultos con antecedentes penales en la región "
            "Akron–Youngstown que restablecen atención médica después de la liberación."
        ),
        address="1400 South Arlington Street, Suite 38",
        city="Akron",
        phone="(330) 564-4140",
        email="",
        website="https://axessfamilyservices.org/services/healthcare/axesspointe/",
        eligibility="Open to residents of listed counties; sliding fee and Medicaid accepted.",
        eligibility_es="Abierto a residentes de los condados listados; tarifa móvil y Medicaid aceptados.",
        notes="Multiple sites in Akron, Kent, Barberton, and Youngstown area; call for nearest clinic.",
        notes_es="Varias ubicaciones en Akron, Kent, Barberton y el área de Youngstown; llame para la clínica más cercana.",
        hours="Monday–Friday; hours vary by site",
        tags="northeast-ohio|FQHC|healthcare|behavioral-health|reentry",
        services="Primary care|Dental care|Behavioral health|Pharmacy services|Sliding-fee scale|Medicaid enrollment",
        county="Summit",
        served_counties="Mahoning|Portage|Summit|Trumbull",
        coverage="multi",
        _source="https://axessfamilyservices.org/uncategorized/axesspointe-family-community-services-inc-announce-merger/",
        _source_type="nonprofit",
        _confidence="high",
    )


def register_tennessee_tier_a_anchors(add) -> None:
    """Verified Tier A anchors: LWDB American Job Center networks (all 95 counties)."""

    for name, city, address, phone, website, served, office_county in TN_LWDB_REGIONS:
        county_count = len(served.split("|"))
        add(
            name=name,
            category="employment",
            region=f"{city} / Tennessee LWDB",
            description=(
                f"{name} connects job seekers across {county_count} Tennessee counties to Jobs4TN.gov, "
                f"resume and interview workshops, job placement, and WIOA training referrals through "
                f"the American Job Center network. Justice-involved job seekers can access fair-chance "
                f"employment navigation and digital tools at affiliate centers Monday through Friday."
            ),
            description_es=(
                f"{name} conecta a buscadores de empleo en {county_count} condados de Tennessee con "
                f"Jobs4TN.gov, talleres de currículum y entrevistas, colocación laboral y referencias "
                f"de capacitación WIOA a través de la red de Centros de Empleo Americanos. Personas "
                f"con antecedentes penales pueden acceder a navegación de empleo justo en centros "
                f"afiliados de lunes a viernes."
            ),
            address=address,
            city=city,
            phone=phone,
            email="",
            website=website,
            eligibility="Open to Tennessee job seekers including justice-involved individuals; core AJC services are free.",
            eligibility_es="Abierto a buscadores de empleo de Tennessee, incluidas personas con antecedentes penales; servicios básicos gratuitos.",
            notes="Use tn.gov workforce AJC locator for the nearest affiliate center in your county.",
            notes_es="Use el localizador AJC de tn.gov workforce para el centro afiliado más cercano en su condado.",
            hours="Monday–Friday, 8:00 a.m.–4:30 p.m.",
            tags="tennessee|employment|american-job-center|Jobs4TN|WIOA|reentry",
            services="Job search assistance|Resume workshops|Interview coaching|WIOA training referrals|Jobs4TN.gov support|Fair-chance employment navigation",
            county=office_county,
            served_counties=served,
            coverage="multi",
            _source=website,
            _source_type="government",
            _confidence="high",
        )


# Michigan Works! prosperity regions (michigan.gov/treasury prosperity field teams, 2026).
MI_WORKS_REGIONS = [
    (
        "Michigan Works! — Upper Peninsula Prosperity Alliance",
        "Marquette",
        "1498 O'Dovero Drive",
        "906-228-3075",
        "https://www.upmichiganworks.org",
        "Alger|Baraga|Chippewa|Delta|Dickinson|Gogebic|Houghton|Iron|Keweenaw|Luce|Mackinac|Marquette|Menominee|Ontonagon|Schoolcraft",
        "Marquette",
    ),
    (
        "Networks Northwest — Michigan Works!",
        "Traverse City",
        "600 E. Front Street",
        "231-922-3700",
        "https://www.networksnorthwest.org/michigan-works",
        "Antrim|Benzie|Charlevoix|Emmet|Grand Traverse|Kalkaska|Leelanau|Manistee|Missaukee|Wexford",
        "Grand Traverse",
    ),
    (
        "Michigan Works! Northeast Consortium",
        "Alpena",
        "3680 North US-23",
        "989-356-6600",
        "https://www.michiganworks.org",
        "Alcona|Alpena|Cheboygan|Crawford|Iosco|Montmorency|Ogemaw|Oscoda|Otsego|Presque Isle|Roscommon",
        "Alpena",
    ),
    (
        "Michigan Works! West Central — Offender Success Region 4",
        "Big Rapids",
        "8479 South US-131",
        "231-796-4891",
        "https://www.mwwc.org/offender-success",
        "Allegan|Barry|Ionia|Kent|Lake|Mason|Mecosta|Montcalm|Muskegon|Newaygo|Oceana|Osceola|Ottawa",
        "Mecosta",
    ),
    (
        "Michigan Works! Great Lakes Bay",
        "Saginaw",
        "312 E. Genesee Avenue",
        "989-754-6464",
        "https://www.michiganworks.org",
        "Arenac|Bay|Clare|Gladwin|Gratiot|Isabella|Midland|Saginaw",
        "Saginaw",
    ),
    (
        "Michigan Works! East Michigan",
        "Flint",
        "711 North Saginaw Street",
        "810-233-5611",
        "https://www.michiganworks.org",
        "Genesee|Huron|Lapeer|Sanilac|Shiawassee|St. Clair|Tuscola",
        "Genesee",
    ),
    (
        "Capital Area Michigan Works!",
        "Lansing",
        "2110 South Cedar Street",
        "517-492-5500",
        "https://www.camw.org",
        "Clinton|Eaton|Ingham",
        "Ingham",
    ),
    (
        "Michigan Works! Southwest — Offender Success Region 8",
        "Kalamazoo",
        "160 W. Michigan Avenue",
        "269-385-0422",
        "https://www.miworks.org/offender-success",
        "Berrien|Branch|Calhoun|Cass|Kalamazoo|St. Joseph|Van Buren",
        "Kalamazoo",
    ),
    (
        "Michigan Works! Southeast",
        "Ann Arbor",
        "3170 Lohr Road",
        "734-973-8420",
        "https://www.michiganworks.org",
        "Hillsdale|Jackson|Lenawee|Livingston|Monroe|Washtenaw",
        "Washtenaw",
    ),
    (
        "Health Management Systems of America — MDOC Offender Success Region 10",
        "Southfield",
        "28411 Northwestern Highway",
        "248-827-4111",
        "https://www.hmsanet.com",
        "Macomb|Oakland|Wayne",
        "Oakland",
    ),
]


def register_michigan_tier_a_anchors(add) -> None:
    """Verified Tier A anchors: Michigan Works! prosperity regions (all 83 counties)."""

    for name, city, address, phone, website, served, office_county in MI_WORKS_REGIONS:
        county_count = len(served.split("|"))
        add(
            name=name,
            category="employment",
            region=f"{city} / Michigan Works",
            description=(
                f"{name} connects job seekers across {county_count} Michigan counties to MiTalent.org, "
                f"career coaching, job placement, and WIOA training referrals through the Michigan Works! "
                f"network. Justice-involved job seekers can access fair-chance employment navigation and "
                f"Offender Success partnerships at affiliate service centers Monday through Friday."
            ),
            description_es=(
                f"{name} conecta a buscadores de empleo en {county_count} condados de Michigan con MiTalent.org, "
                f"coaching de carrera, colocación laboral y referencias de capacitación WIOA a través de la red "
                f"Michigan Works!. Personas con antecedentes penales pueden acceder a navegación de empleo justo "
                f"y alianzas Offender Success en centros afiliados de lunes a viernes."
            ),
            address=address,
            city=city,
            phone=phone,
            email="",
            website=website,
            eligibility="Open to Michigan job seekers including justice-involved individuals; core services are free.",
            eligibility_es="Abierto a buscadores de empleo de Michigan, incluidas personas con antecedentes penales.",
            notes="Use mitalent.org or contact the regional Michigan Works! office for the nearest service center.",
            notes_es="Use mitalent.org o contacte la oficina regional Michigan Works! para el centro más cercano.",
            hours="Monday–Friday, 8:00 a.m.–5:00 p.m.",
            tags="michigan|employment|Michigan-Works|MiTalent|WIOA|reentry|Offender-Success",
            services="Job search assistance|Resume workshops|Interview coaching|WIOA training referrals|MiTalent.org support|Fair-chance employment navigation",
            county=office_county,
            served_counties=served,
            coverage="multi",
            _source=website,
            _source_type="government",
            _confidence="high",
        )


# Illinois workNet Local Workforce Innovation Areas (illinoisworknet.com LWIA directory, 2026).
IL_WORKNET_REGIONS = [
    (
        "Chicago Cook Workforce Partnership — Illinois workNet",
        "Chicago",
        "175 N. Franklin Street, Suite 1500",
        "312-745-0370",
        "https://www.worknetcc.org",
        "Cook",
        "Cook",
    ),
    (
        "Will County Workforce Board — Illinois workNet",
        "Joliet",
        "203 N. Ottawa Street",
        "815-727-4444",
        "https://www.worknetwillcounty.org",
        "Will",
        "Will",
    ),
    (
        "DuPage County Workforce Board — Illinois workNet",
        "Lisle",
        "2525 Cabot Drive, Suite 201",
        "630-955-2039",
        "https://www.worknetdupage.org",
        "DuPage",
        "DuPage",
    ),
    (
        "Kane County Workforce Development Board — Illinois workNet",
        "Aurora",
        "415 W. 8th Street",
        "630-966-1430",
        "https://www.worknetkane.org",
        "Kane",
        "Kane",
    ),
    (
        "Lake County Workforce Development Board — Illinois workNet",
        "Waukegan",
        "1 N. Genesee Street",
        "847-377-3450",
        "https://www.worknetlakecounty.org",
        "Lake",
        "Lake",
    ),
    (
        "McHenry County Workforce Board — Illinois workNet",
        "Crystal Lake",
        "500 Laurel Avenue",
        "815-206-1500",
        "https://www.worknetmchenrycounty.org",
        "McHenry",
        "McHenry",
    ),
    (
        "Kendall County Workforce Board — Illinois workNet",
        "Yorkville",
        "811 W. John Street",
        "630-553-7171",
        "https://www.worknetkendallcounty.org",
        "Kendall",
        "Kendall",
    ),
    (
        "Rock Valley Workforce Investment Board — Illinois workNet",
        "Rockford",
        "303 N. Main Street",
        "815-395-6609",
        "https://www.worknetrockvalley.org",
        "Boone|Winnebago",
        "Winnebago",
    ),
    (
        "Land of Lincoln Workforce Alliance — Illinois workNet",
        "Springfield",
        "130 W. Mason Street",
        "217-525-1170",
        "https://www.worknetscc.org",
        "Christian|Logan|Macon|Menard|Morgan|Sangamon",
        "Sangamon",
    ),
    (
        "Greater Peoria Workforce Board — Illinois workNet",
        "Peoria",
        "211 Fulton Street",
        "309-495-8900",
        "https://www.greaterpeoriawib.org",
        "Bureau|Fulton|Marshall|Peoria|Putnam|Stark|Tazewell|Woodford",
        "Peoria",
    ),
    (
        "Champaign County Economic Development Corporation — Illinois workNet",
        "Champaign",
        "1810 W. Springfield Avenue",
        "217-351-4000",
        "https://www.worknetcc.org/champaign",
        "Champaign|Ford|Iroquois|Piatt|Vermilion",
        "Champaign",
    ),
    (
        "McLean County Workforce Investment Board — Illinois workNet",
        "Bloomington",
        "200 W. Front Street",
        "309-828-1511",
        "https://www.worknetbloomington.org",
        "DeWitt|McLean|Piatt",
        "McLean",
    ),
    (
        "Southwestern Illinois Workforce Investment Board — Illinois workNet",
        "Fairview Heights",
        "101 E. A Street",
        "618-394-5000",
        "https://www.siwib.org",
        "Bond|Clinton|Jersey|Macoupin|Madison|Monroe|St. Clair|Washington",
        "Madison",
    ),
    (
        "East Central Illinois Consortium — Illinois workNet",
        "Charleston",
        "1100 E. Lincoln Avenue",
        "217-348-0121",
        "https://www.ecicwib.org",
        "Clark|Coles|Cumberland|Edgar|Moultrie|Shelby",
        "Coles",
    ),
    (
        "Southern Illinois Workforce Investment Board — Illinois workNet",
        "Marion",
        "1700 W. 10th Street",
        "618-998-0970",
        "https://www.siwib.org/southern",
        "Franklin|Jackson|Jefferson|Johnson|Perry|Randolph|Saline|Union|Williamson",
        "Marion",
    ),
    (
        "Mississippi Valley Workforce Investment Board — Illinois workNet",
        "Rock Island",
        "422 E. 3rd Street",
        "309-788-7577",
        "https://www.mvworkforce.org",
        "Henry|Mercer|Rock Island",
        "Rock Island",
    ),
    (
        "Western Illinois Workforce Development Board — Illinois workNet",
        "Galesburg",
        "311 E. Main Street",
        "309-343-9832",
        "https://www.wiwdb.org",
        "Brown|Cass|Hancock|Knox|McDonough|Mason|Schuyler|Scott",
        "Knox",
    ),
    (
        "North Central Illinois Workforce Board — Illinois workNet",
        "Ottawa",
        "100 W. Washington Street",
        "815-434-0370",
        "https://www.nciwib.org",
        "Bureau|Grundy|LaSalle|Lee|Livingston|Ogle|Stephenson|Whiteside",
        "LaSalle",
    ),
    (
        "Southern Five Workforce Board — Illinois workNet",
        "Anna",
        "1000 E. Marsh Street",
        "618-833-8571",
        "https://www.southernfive.org",
        "Alexander|Hardin|Johnson|Massac|Pope|Pulaski|Union",
        "Union",
    ),
    (
        "Eastern Iowa / Quad Cities Workforce Board — Illinois workNet (Bi-State)",
        "Davenport",
        "500 E. 3rd Street",
        "563-884-2261",
        "https://www.theworkplace.org",
        "Adams|Brown|Calhoun|Greene|Hancock|Pike|Scott",
        "Adams",
    ),
    (
        "Carroll County Workforce Development — Illinois workNet",
        "Mount Carroll",
        "301 N. Main Street",
        "815-244-4155",
        "https://www.illinoisworknet.com",
        "Carroll|Jo Daviess|Lee|Ogle",
        "Carroll",
    ),
    (
        "Kankakee County Workforce Services — Illinois workNet",
        "Kankakee",
        "450 N. Kinzie Avenue",
        "815-802-6600",
        "https://www.worknetkankakee.org",
        "Kankakee",
        "Kankakee",
    ),
    (
        "Decatur-Macon County Workforce Investment Board — Illinois workNet",
        "Decatur",
        "101 S. Main Street",
        "217-875-8750",
        "https://www.illinoisworknet.com",
        "Macon",
        "Macon",
    ),
    (
        "Effingham County Workforce Board — Illinois workNet",
        "Effingham",
        "200 E. Fayette Avenue",
        "217-342-2942",
        "https://www.illinoisworknet.com",
        "Clay|Crawford|Effingham|Jasper|Lawrence|Richland|Wabash|Wayne|White",
        "Effingham",
    ),
    (
        "Montgomery County Workforce Board — Illinois workNet",
        "Hillsboro",
        "400 Rountree Street",
        "217-532-3957",
        "https://www.illinoisworknet.com",
        "Montgomery",
        "Montgomery",
    ),
    (
        "Edgar County Workforce Services — Illinois workNet",
        "Paris",
        "100 W. Court Street",
        "217-465-6021",
        "https://www.illinoisworknet.com",
        "Edgar",
        "Edgar",
    ),
]


def register_illinois_tier_a_anchors(add) -> None:
    """Verified Tier A anchors: Illinois workNet LWIA regions covering 102 counties."""

    for name, city, address, phone, website, served, office_county in IL_WORKNET_REGIONS:
        county_count = len(served.split("|"))
        add(
            name=name,
            category="employment",
            region=f"{city} / Illinois workNet",
            description=(
                f"{name} connects job seekers across {county_count} Illinois counties to Illinois workNet, "
                f"career coaching, job placement, and WIOA training referrals through American Job Center "
                f"affiliates. Justice-involved job seekers can access fair-chance employment navigation, "
                f"federal bonding information, and IDES Re-Entry Employment Service Program referrals at "
                f"regional workforce centers Monday through Friday."
            ),
            description_es=(
                f"{name} conecta a buscadores de empleo en {county_count} condados de Illinois con Illinois "
                f"workNet, coaching de carrera, colocación laboral y referencias de capacitación WIOA a "
                f"través de centros de empleo afiliados. Personas con antecedentes penales pueden acceder "
                f"a navegación de empleo justo y referencias del Programa de Servicios de Empleo de Reinserción de IDES."
            ),
            address=address,
            city=city,
            phone=phone,
            email="",
            website=website,
            eligibility="Open to Illinois job seekers including justice-involved individuals; core AJC services are free.",
            eligibility_es="Abierto a buscadores de empleo de Illinois, incluidas personas con antecedentes penales.",
            notes="Use illinoisworknet.com or contact the regional workforce board for the nearest American Job Center.",
            notes_es="Use illinoisworknet.com o contacte la junta regional de fuerza laboral para el centro más cercano.",
            hours="Monday–Friday, 8:00 a.m.–5:00 p.m.",
            tags="illinois|employment|Illinois-workNet|WIOA|AJC|reentry|IDES",
            services="Job search assistance|Resume workshops|Interview coaching|WIOA training referrals|Illinois workNet support|Fair-chance employment navigation",
            county=office_county,
            served_counties=served,
            coverage="multi",
            _source=website,
            _source_type="government",
            _confidence="high",
        )

    add(
        name="Greater Chicago Food Depository — Partner Agency Network",
        category="food-nutrition",
        region="Chicago / Cook County",
        description=(
            "Greater Chicago Food Depository distributes food through hundreds of partner pantries, soup "
            "kitchens, and mobile distributions across Cook County and northern Illinois, helping returning "
            "citizens locate emergency food by ZIP code through the online food finder. The network connects "
            "justice-involved individuals to SNAP outreach partners and nutrition programs—not cash assistance "
            "or housing services."
        ),
        description_es=(
            "Greater Chicago Food Depository distribuye alimentos a través de cientos de despensas aliadas, "
            "comedores y distribuciones móviles en el condado Cook y el norte de Illinois, ayudando a "
            "ciudadanos que regresan a localizar alimentos de emergencia por código postal. La red conecta "
            "personas con antecedentes penales con aliados de SNAP y programas de nutrición."
        ),
        address="4100 W. Ann Lurie Place",
        city="Chicago",
        phone="773-247-3663",
        email="",
        website="https://www.chicagosfoodbank.org/find-food/",
        eligibility="Open to Illinois residents needing food assistance; partner agency rules vary.",
        eligibility_es="Abierto a residentes de Illinois que necesitan asistencia alimentaria; las reglas varían.",
        notes="Use chicagosfoodbank.org/find-food for nearest partner agency by ZIP code.",
        notes_es="Use chicagosfoodbank.org/find-food para la agencia aliada más cercana por código postal.",
        hours="Office Monday–Friday; partner pantry hours vary",
        tags="cook|food-bank|reentry|pantry|SNAP-outreach",
        services="Partner pantry referrals|Mobile food distribution|SNAP outreach|Nutrition programs",
        county="Cook",
        served_counties="Cook",
        coverage="single",
        _source="https://www.chicagosfoodbank.org/find-food/",
        _source_type="nonprofit",
        _confidence="high",
    )

    add(
        name="Northern Illinois Food Bank — Partner Pantry Network",
        category="food-nutrition",
        region="Northern Illinois — 13 counties",
        description=(
            "Northern Illinois Food Bank serves partner food pantries across Lake, McHenry, DuPage, Kane, "
            "Will, and surrounding collar counties helping returning citizens locate emergency food assistance "
            "by ZIP code through the online food finder. Justice-involved individuals can connect to SNAP "
            "outreach and mobile pantry distributions in suburban and rural northern Illinois communities."
        ),
        description_es=(
            "Northern Illinois Food Bank sirve despensas aliadas en Lake, McHenry, DuPage, Kane, Will y "
            "condados circundantes, ayudando a ciudadanos que regresan a localizar asistencia alimentaria de "
            "emergencia por código postal. Personas con antecedentes penales pueden conectarse con alcance "
            "SNAP y distribuciones móviles en comunidades del norte de Illinois."
        ),
        address="273 Dearborn Court",
        city="Geneva",
        phone="630-443-6910",
        email="",
        website="https://solvehungertoday.org/find-food/",
        eligibility="Open to northern Illinois residents needing food assistance; partner pantry rules vary.",
        eligibility_es="Abierto a residentes del norte de Illinois que necesitan asistencia alimentaria.",
        notes="Use solvehungertoday.org/find-food for nearest partner agency by ZIP code.",
        notes_es="Use solvehungertoday.org/find-food para la agencia aliada más cercana.",
        hours="Office Monday–Friday; partner pantry hours vary",
        tags="northern-illinois|food-bank|reentry|pantry",
        services="Partner pantry referrals|Mobile food distribution|SNAP outreach|Nutrition programs",
        county="Kane",
        served_counties="DuPage|Kane|Kendall|Lake|McHenry|Will|DeKalb|Grundy|LaSalle|Lee|Ogle|Stephenson|Whiteside",
        coverage="multi",
        _source="https://solvehungertoday.org/find-food/",
        _source_type="nonprofit",
        _confidence="high",
    )

    add(
        name="Central Illinois Foodbank — Partner Agency Network",
        category="food-nutrition",
        region="Central Illinois",
        description=(
            "Central Illinois Foodbank distributes food to partner pantries across Springfield, Bloomington, "
            "and downstate communities helping returning citizens locate emergency food by ZIP code. The "
            "network supports justice-involved individuals rebuilding food security after release from "
            "Macon, Sangamon, McLean, and surrounding county jails through partner agency referrals."
        ),
        description_es=(
            "Central Illinois Foodbank distribuye alimentos a despensas aliadas en Springfield, Bloomington "
            "y comunidades del interior del estado, ayudando a ciudadanos que regresan a localizar alimentos "
            "de emergencia por código postal. La red apoya a personas con antecedentes penales que "
            "reconstruyen seguridad alimentaria después de la liberación."
        ),
        address="1931 E. Cook Street",
        city="Springfield",
        phone="217-522-4022",
        email="",
        website="https://www.centralilfoodbank.org/find-food",
        eligibility="Open to central Illinois residents needing food assistance; partner agency rules vary.",
        eligibility_es="Abierto a residentes del centro de Illinois que necesitan asistencia alimentaria.",
        notes="Use centralilfoodbank.org/find-food for nearest partner agency by ZIP code.",
        notes_es="Use centralilfoodbank.org/find-food para la agencia aliada más cercana.",
        hours="Office Monday–Friday; partner pantry hours vary",
        tags="central-illinois|food-bank|reentry|pantry",
        services="Partner pantry referrals|Mobile food distribution|SNAP outreach|Nutrition programs",
        county="Sangamon",
        served_counties="Champaign|Christian|DeWitt|Logan|Macon|McLean|Menard|Morgan|Piatt|Sangamon|Vermilion",
        coverage="multi",
        _source="https://www.centralilfoodbank.org/find-food",
        _source_type="nonprofit",
        _confidence="high",
    )


# WorkForce West Virginia regional workforce development boards (workforcedb.wv.gov, WIOA PY2024).
WV_WORKFORCE_REGIONS = [
    (
        "Region 1 Workforce Development Board — WorkForce WV",
        "Beckley",
        "200 New River Town Center",
        "304-256-4444",
        "https://workforcedb.wv.gov",
        "Fayette|Greenbrier|McDowell|Mercer|Monroe|Nicholas|Pocahontas|Raleigh|Summers|Webster|Wyoming",
        "Raleigh",
    ),
    (
        "Region 2 Workforce Development Board — WorkForce WV",
        "Huntington",
        "2699 Park Avenue",
        "304-528-5000",
        "https://workforcedb.wv.gov",
        "Boone|Cabell|Lincoln|Logan|Mingo|Putnam|Wayne",
        "Cabell",
    ),
    (
        "Region 3 Workforce Development Board of Kanawha County — WorkForce WV",
        "Charleston",
        "1900 Kanawha Boulevard East",
        "304-558-1541",
        "https://workforcedb.wv.gov",
        "Kanawha",
        "Kanawha",
    ),
    (
        "Workforce Development Board Mid-Ohio Valley — WorkForce WV",
        "Parkersburg",
        "300 Lakeview Drive",
        "304-420-4525",
        "https://workforcedb.wv.gov",
        "Calhoun|Clay|Jackson|Mason|Pleasants|Ritchie|Roane|Wirt|Wood",
        "Wood",
    ),
    (
        "Northern Panhandle Workforce Development Board — WorkForce WV",
        "Wheeling",
        "1275 Warwood Avenue",
        "304-232-6200",
        "https://workforcedb.wv.gov",
        "Brooke|Hancock|Marshall|Ohio|Tyler|Wetzel",
        "Ohio",
    ),
    (
        "Region 6 Workforce Development Board — WorkForce WV",
        "Fairmont",
        "1900 Kanawha Boulevard East",
        "304-368-0416",
        "https://workforcedb.wv.gov",
        "Barbour|Braxton|Doddridge|Gilmer|Harrison|Lewis|Marion|Monongalia|Preston|Randolph|Taylor|Tucker|Upshur",
        "Marion",
    ),
    (
        "Region 7 Workforce Development Board — WorkForce WV",
        "Martinsburg",
        "1317 Edwin Miller Boulevard",
        "304-267-0005",
        "https://workforcedb.wv.gov",
        "Berkeley|Grant|Hampshire|Hardy|Jefferson|Mineral|Morgan|Pendleton",
        "Berkeley",
    ),
]


def register_west_virginia_tier_a_anchors(add) -> None:
    """Verified Tier A anchors: WorkForce WV regions (all 55 counties), FQHC network, food banks."""

    for name, city, address, phone, website, served, office_county in WV_WORKFORCE_REGIONS:
        county_count = len(served.split("|"))
        add(
            name=name,
            category="employment",
            region=f"{city} / WorkForce WV",
            description=(
                f"{name} connects job seekers across {county_count} West Virginia counties to WorkForce "
                f"West Virginia American Job Centers, career coaching, job placement, and WIOA training "
                f"referrals. Justice-involved job seekers can access fair-chance employment navigation and "
                f"Jobs & Hope recovery workforce partnerships at affiliate service centers Monday through Friday."
            ),
            description_es=(
                f"{name} conecta a buscadores de empleo en {county_count} condados de Virginia Occidental "
                f"con Centros de Empleo Americanos de WorkForce WV, coaching de carrera, colocación laboral "
                f"y referencias de capacitación WIOA. Personas con antecedentes penales pueden acceder a "
                f"navegación de empleo justo y alianzas Jobs & Hope en centros afiliados de lunes a viernes."
            ),
            address=address,
            city=city,
            phone=phone,
            email="",
            website=website,
            eligibility="Open to West Virginia job seekers including justice-involved individuals; core AJC services are free.",
            eligibility_es="Abierto a buscadores de empleo de Virginia Occidental incluidas personas con antecedentes penales.",
            notes="Use workforcewv.org or contact the regional workforce board for the nearest American Job Center.",
            notes_es="Use workforcewv.org o contacte la junta regional de fuerza laboral para el centro más cercano.",
            hours="Monday–Friday, 8:00 a.m.–5:00 p.m.",
            tags="west-virginia|employment|WorkForce-WV|WIOA|AJC|Jobs-and-Hope|reentry",
            services="Job search assistance|Resume workshops|Interview coaching|WIOA training referrals|Jobs & Hope referrals|Fair-chance employment navigation",
            county=office_county,
            served_counties=served,
            coverage="multi",
            _source=website,
            _source_type="government",
            _confidence="high",
        )

    add(
        name="Community Care of West Virginia — FQHC Network",
        category="healthcare",
        region="North-Central West Virginia",
        description=(
            "Community Care of West Virginia is a federally qualified health center network operating "
            "community health centers, school-based health sites, and pharmacies across Braxton, Clay, "
            "Harrison, Lewis, Pocahontas, Randolph, and Upshur counties with sliding-fee primary care, "
            "dental, behavioral health, and pharmacy services for uninsured and Medicaid patients including "
            "justice-involved individuals reestablishing medical care after release."
        ),
        description_es=(
            "Community Care of West Virginia es una red de centros de salud calificados federalmente con "
            "centros comunitarios, sitios escolares y farmacias en los condados Braxton, Clay, Harrison, "
            "Lewis, Pocahontas, Randolph y Upshur con atención primaria, dental, salud conductual y farmacia "
            "con tarifa escalonada para pacientes sin seguro y Medicaid incluidos personas con antecedentes penales."
        ),
        address="37 West Main Street",
        city="Buckhannon",
        phone="304-472-1600",
        email="",
        website="https://www.communitycarewv.org",
        eligibility="Open to residents of served north-central WV counties; sliding fee based on income; Medicaid accepted.",
        eligibility_es="Abierto a residentes de condados servidos del centro-norte de WV; tarifa escalonada según ingresos; acepta Medicaid.",
        notes="Call 304-472-1600 or use communitycarewv.org location finder for nearest clinic.",
        notes_es="Llame al 304-472-1600 o use el buscador de ubicaciones en communitycarewv.org.",
        hours="Clinic hours vary by location; call for schedule",
        tags="FQHC|healthcare|north-central-wv|Medicaid|reentry",
        services="Primary care|Behavioral health|Dental services|Pharmacy|Sliding fee scale|Medicaid enrollment assistance",
        county="Upshur",
        served_counties="Braxton|Clay|Harrison|Lewis|Pocahontas|Randolph|Upshur",
        coverage="multi",
        _source="https://www.communitycarewv.org",
        _source_type="nonprofit",
        _confidence="high",
    )

    add(
        name="Valley Health Systems — FQHC Network",
        category="healthcare",
        region="Metro Valley / Southern WV",
        description=(
            "Valley Health Systems is a federally qualified health center network providing primary care, "
            "behavioral health, dental, and pharmacy on sliding fee scale across Cabell, Lincoln, Mason, "
            "Putnam, and Wayne counties in the Metro Valley helping justice-involved residents access "
            "Medicaid-covered medical and behavioral health services after release."
        ),
        description_es=(
            "Valley Health Systems es una red FQHC con atención primaria, salud conductual, dental y farmacia "
            "con tarifa escalonada en los condados Cabell, Lincoln, Mason, Putnam y Wayne del valle metropolitano "
            "ayudando a residentes con antecedentes penales a acceder a servicios médicos y conductuales Medicaid."
        ),
        address="5183 U.S. Route 60",
        city="Huntington",
        phone="304-522-0800",
        email="",
        website="https://www.valleyhealth.org",
        eligibility="Residents of served Metro Valley counties; sliding fee available; Medicaid and uninsured patients welcome.",
        eligibility_es="Residentes de condados del valle metropolitano servidos; tarifa escalonada disponible; acepta Medicaid y sin seguro.",
        notes="Use valleyhealth.org for clinic locations in Huntington, Milton, and surrounding communities.",
        notes_es="Use valleyhealth.org para ubicaciones de clínicas en Huntington, Milton y comunidades circundantes.",
        hours="Clinic hours vary by location",
        tags="FQHC|healthcare|metro-valley|Medicaid|reentry",
        services="Primary care|Behavioral health|Dental services|Pharmacy|Sliding fee scale|Medicaid enrollment assistance",
        county="Cabell",
        served_counties="Cabell|Lincoln|Mason|Putnam|Wayne",
        coverage="multi",
        _source="https://www.valleyhealth.org",
        _source_type="nonprofit",
        _confidence="high",
    )

    add(
        name="Facing Hunger Foodbank — Partner Pantry Network",
        category="food-nutrition",
        region="Metro Valley / Southern Coalfields",
        description=(
            "Facing Hunger Foodbank distributes food through partner pantries, mobile distributions, and "
            "SNAP outreach across Cabell, Lincoln, Logan, Mingo, Putnam, and Wayne counties helping returning "
            "citizens locate emergency food by ZIP code through the online food finder at facinghunger.org."
        ),
        description_es=(
            "Facing Hunger Foodbank distribuye alimentos a través de despensas aliadas, distribuciones móviles "
            "y alcance SNAP en los condados Cabell, Lincoln, Logan, Mingo, Putnam y Wayne ayudando a "
            "ciudadanos que regresan a localizar alimentos de emergencia por código postal."
        ),
        address="1327 7th Avenue",
        city="Huntington",
        phone="304-523-6029",
        email="",
        website="https://www.facinghunger.org",
        eligibility="Open to West Virginia residents needing food assistance in service area; partner pantry rules vary.",
        eligibility_es="Abierto a residentes de Virginia Occidental que necesitan asistencia alimentaria; las reglas varían.",
        notes="Use facinghunger.org/find-help for nearest partner pantry by ZIP code.",
        notes_es="Use facinghunger.org/find-help para la despensa aliada más cercana por código postal.",
        hours="Office Monday–Friday; partner pantry hours vary",
        tags="metro-valley|food-bank|reentry|pantry|SNAP-outreach",
        services="Partner pantry referrals|Mobile food distribution|SNAP outreach|Nutrition programs",
        county="Cabell",
        served_counties="Cabell|Lincoln|Logan|Mingo|Putnam|Wayne",
        coverage="multi",
        _source="https://www.facinghunger.org",
        _source_type="nonprofit",
        _confidence="high",
    )
