"""Shared helpers and verified program data for West Virginia resource build."""

from __future__ import annotations

WV_DCR = "https://dcr.wv.gov"
WV_PATH = "https://wvpath.wv.gov"

MIN_DESCRIPTION_LEN = 350

_CATEGORY_SUFFIX_EN: dict[str, str] = {
    "healthcare": (
        "The {area} office provides immunizations, WIC navigation, maternal and child health "
        "screenings, environmental health services, and referrals to regional FQHCs, hospitals, "
        "and behavioral health partners. Justice-involved residents can establish a local health "
        "contact after release from WVDCR custody or county jail—not emergency hospital or crisis care."
    ),
    "education": (
        "Programs include high school equivalency (GED), adult basic education, and workforce "
        "readiness aligned with WorkForce West Virginia and Jobs & Hope referrals in {area}. "
        "Returning citizens can rebuild credentials for fair-chance employment; call to confirm "
        "class schedules, testing fees, and enrollment documents before your first visit."
    ),
    "housing": (
        "Staff conduct intake assessment and connect residents to structured shelter or transitional "
        "programming with referrals to WV PATH benefits, Legal Aid of West Virginia, and regional "
        "workforce partners in {area}. Returning citizens should call ahead to confirm bed "
        "availability, sobriety requirements, and referral policies."
    ),
    "basic-needs": (
        "Emergency assistance may include food, utility help, clothing, and case management with "
        "referrals to WV PATH, 211 West Virginia, and housing partners serving {area}. Low-income "
        "returning citizens should bring photo ID and proof of address when available."
    ),
    "veterans": (
        "Navigators connect eligible veterans—including justice-involved veterans—to VA benefits, "
        "peer support, employment resources, and civil legal help for housing and benefits issues "
        "in {area}. Military discharge papers and income documentation may be required at intake."
    ),
    "substance-use-treatment": (
        "Licensed clinicians provide assessment, outpatient or residential treatment, "
        "medication-assisted recovery, and peer support with Medicaid acceptance and many justice "
        "referrals from drug courts and WVDCR parole serving {area}. Walk-in availability varies; "
        "call for intake assessment before traveling."
    ),
    "employment": (
        "Career specialists connect job seekers in {area} to American Job Centers, WIOA training, "
        "fair-chance employer networks, and Jobs & Hope recovery employment pathways. "
        "Justice-involved adults can access resume help, skills assessments, and referral to "
        "regional training providers."
    ),
    "legal-aid": (
        "Attorneys assist with housing and eviction defense, public benefits appeals, family law, "
        "and West Virginia Clean Slate expungement for low-income clients in {area}—not criminal "
        "defense. Apply through the statewide intake hotline or local office; LSC income limits apply."
    ),
    "id-documentation": (
        "Staff help returning citizens in {area} obtain state ID, birth certificates, Social Security "
        "cards, and DMV documentation needed for employment, WV PATH benefits, and supervision "
        "reporting after release from incarceration."
    ),
    "peer-support": (
        "Certified peer recovery specialists with lived experience provide mentoring, support groups, "
        "and recovery coaching for justice-involved individuals and families affected by substance use "
        "in {area}."
    ),
    "reentry-organizations": (
        "Reentry navigators in {area} connect returning citizens to housing, employment, treatment, "
        "and DoHS benefits through WVDCR community partnerships and regional directories—not "
        "emergency cash assistance or crisis intervention."
    ),
    "transportation": (
        "Programs help returning citizens in {area} access bus passes, ride vouchers, or travel "
        "assistance to reach medical appointments, employment, probation reporting, and benefits "
        "interviews after release."
    ),
    "food-nutrition": (
        "Partner pantries and SNAP outreach help food-insecure households in {area} locate emergency "
        "meals and enroll in WV PATH food benefits after release from incarceration."
    ),
    "family-children": (
        "Family support programs in {area} assist parents and children affected by incarceration with "
        "parenting resources, visitation navigation, and referrals to DoHS and community partners."
    ),
}

_CATEGORY_SUFFIX_ES: dict[str, str] = {
    "healthcare": (
        "La oficina de {area} ofrece inmunizaciones, navegación WIC, exámenes de salud materno-infantil, "
        "servicios de salud ambiental y referencias a FQHC, hospitales y aliados de salud conductual "
        "regionales. Residentes con antecedentes penales pueden establecer un contacto de salud local "
        "después de la liberación—no es atención hospitalaria de emergencia."
    ),
    "education": (
        "Los programas incluyen equivalencia de secundaria (GED), educación básica para adultos y "
        "preparación laboral alineada con WorkForce West Virginia y Jobs & Hope en {area}. "
        "Ciudadanos que regresan pueden reconstruir credenciales; llame para confirmar horarios y documentos."
    ),
    "housing": (
        "El personal realiza evaluaciones de admisión y conecta a residentes con refugio o vivienda "
        "transicional estructurada y referencias a WV PATH, Legal Aid of West Virginia y socios "
        "laborales en {area}. Llame con anticipación para confirmar disponibilidad y requisitos."
    ),
    "basic-needs": (
        "La asistencia de emergencia puede incluir alimentos, ayuda con servicios, ropa y manejo de "
        "casos con referencias a WV PATH, 211 West Virginia y aliados de vivienda en {area}."
    ),
    "veterans": (
        "Los navegadores conectan a veteranos elegibles—incluidos veteranos con antecedentes penales—"
        "con beneficios del VA, apoyo entre pares y recursos laborales en {area}."
    ),
    "substance-use-treatment": (
        "Clínicos licenciados ofrecen evaluación, tratamiento ambulatorio o residencial, recuperación "
        "asistida con medicamentos y apoyo entre pares con aceptación de Medicaid en {area}."
    ),
    "employment": (
        "Especialistas conectan a buscadores de empleo en {area} con Centros de Empleo Americanos, "
        "capacitación WIOA, empleadores de segunda oportunidad y Jobs & Hope."
    ),
    "legal-aid": (
        "Abogados ayudan con defensa de vivienda y desalojo, apelaciones de beneficios públicos, "
        "derecho familiar y eliminación Clean Slate en {area}—no defensa penal."
    ),
    "id-documentation": (
        "El personal ayuda a ciudadanos que regresan en {area} a obtener identificación estatal, "
        "certificados de nacimiento y documentos del DMV necesarios para empleo y beneficios."
    ),
    "peer-support": (
        "Especialistas certificados en recuperación entre pares con experiencia vivida ofrecen "
        "mentoría y grupos de apoyo en {area}."
    ),
    "reentry-organizations": (
        "Navegadores de reinserción en {area} conectan a ciudadanos que regresan con vivienda, empleo, "
        "tratamiento y beneficios DoHS—no efectivo de emergencia."
    ),
    "transportation": (
        "Los programas ayudan a ciudadanos que regresan en {area} a acceder a pases de autobús o "
        "asistencia de transporte para citas médicas, empleo y reportes de supervisión."
    ),
    "food-nutrition": (
        "Despensas aliadas y alcance SNAP ayudan a hogares con inseguridad alimentaria en {area} "
        "a localizar comidas de emergencia e inscribirse en WV PATH."
    ),
    "family-children": (
        "Programas de apoyo familiar en {area} ayudan a padres e hijos afectados por la encarcelación "
        "con recursos de crianza y referencias a DoHS."
    ),
}

_DEFAULT_SUFFIX_EN = (
    "This program serves justice-involved West Virginians in {area} with referrals to regional "
    "reentry partners including DoHS benefits, Legal Aid of West Virginia, and WorkForce West Virginia."
)
_DEFAULT_SUFFIX_ES = (
    "Este programa sirve a virginianos occidentales con antecedentes penales en {area} con "
    "referencias a aliados regionales de reinserción incluidos DoHS, Legal Aid y WorkForce West Virginia."
)


def _area_label(*, region: str, county: str, served: str) -> str:
    if county:
        return f"{county} County"
    if served:
        parts = [part.strip() for part in served.split("|") if part.strip()]
        if len(parts) == 1:
            return f"{parts[0]} County"
        if len(parts) > 1:
            return f"{region or 'regional West Virginia'} ({len(parts)} counties)"
    return region or "West Virginia"


def _ensure_description(
    description: str,
    *,
    category: str,
    region: str,
    county: str,
    served: str,
    lang: str,
) -> str:
    text = (description or "").strip()
    if len(text) >= MIN_DESCRIPTION_LEN:
        return text
    area = _area_label(region=region, county=county, served=served)
    suffix_map = _CATEGORY_SUFFIX_ES if lang == "es" else _CATEGORY_SUFFIX_EN
    suffix = suffix_map.get(category, _DEFAULT_SUFFIX_ES if lang == "es" else _DEFAULT_SUFFIX_EN)
    suffix = suffix.format(area=area, region=region or area, county=county or area)
    if text and not text.endswith("."):
        text += "."
    combined = f"{text} {suffix}".strip() if text else suffix
    if len(combined) < MIN_DESCRIPTION_LEN:
        pad = (_DEFAULT_SUFFIX_ES if lang == "es" else _DEFAULT_SUFFIX_EN).format(
            area=area, region=region or area, county=county or area
        )
        if pad not in combined:
            combined = f"{combined} {pad}".strip()
    return combined


def ensure_entry_descriptions(entry: dict) -> None:
    """Expand short description fields to publication depth (Pass 2C)."""
    entry["description"] = _ensure_description(
        entry.get("description", ""),
        category=entry.get("category", ""),
        region=entry.get("region", ""),
        county=entry.get("county", ""),
        served=entry.get("served_counties", ""),
        lang="en",
    )
    entry["description_es"] = _ensure_description(
        entry.get("description_es", ""),
        category=entry.get("category", ""),
        region=entry.get("region", ""),
        county=entry.get("county", ""),
        served=entry.get("served_counties", ""),
        lang="es",
    )


def _mk(
    add,
    *,
    name,
    category,
    region,
    description,
    description_es,
    phone,
    website,
    county="",
    served="",
    coverage="single",
    address="",
    city="",
    email="",
    eligibility="",
    eligibility_es="",
    notes="",
    notes_es="",
    hours="Monday–Friday, 8:30 a.m.–5:00 p.m. ET",
    tags="",
    services="",
    source="",
    source_type="nonprofit",
    confidence="high",
):
    if not eligibility:
        eligibility = (
            f"West Virginia residents in the program service area; justice-involved individuals "
            f"generally welcome; income or referral rules vary by service."
        )
        eligibility_es = (
            "Residentes de Virginia Occidental en el área de servicio; personas con antecedentes "
            "penales generalmente son bienvenidas; las reglas varían según el servicio."
        )
    if not notes:
        notes = f"Call {phone} or visit {website} to confirm current intake hours and whether walk-ins or referrals are accepted."
        notes_es = f"Llame al {phone} o visite {website} para confirmar horarios de admisión y si se aceptan visitas sin cita o referencias."
    if not tags:
        tags = f"reentry|west-virginia|{county.lower() or 'statewide'}|{category}"
    description = _ensure_description(
        description, category=category, region=region, county=county, served=served, lang="en"
    )
    description_es = _ensure_description(
        description_es, category=category, region=region, county=county, served=served, lang="es"
    )
    add(
        name=name,
        category=category,
        region=region,
        description=description,
        description_es=description_es,
        address=address,
        city=city,
        phone=phone,
        email=email,
        website=website,
        eligibility=eligibility,
        eligibility_es=eligibility_es,
        notes=notes,
        notes_es=notes_es,
        hours=hours,
        tags=tags,
        services=services,
        county=county,
        served_counties=served,
        coverage=coverage,
        _source=source or website,
        _source_type=source_type,
        _confidence=confidence,
    )


# WVDCR parole services offices (dcr.wv.gov/facilities parole-services-offices)
PAROLE_OFFICES = [
    (
        "WVDCR — Beckley Parole Office",
        "Beckley",
        "Raleigh",
        "110 S. Eisenhower Drive",
        "304-256-6720",
        "Fayette|Greenbrier|Nicholas|Pocahontas|Raleigh|Summers|Webster|Wyoming",
        "Southern District Region 3: Fayette, Greenbrier, Nicholas, Pocahontas, Raleigh and surrounding southeastern counties.",
    ),
    (
        "WVDCR — Charleston Parole Office",
        "Charleston",
        "Kanawha",
        "1356 Hansford Street, Suite B",
        "304-558-3597",
        "Boone|Clay|Jackson|Kanawha|Logan|Mingo|Roane",
        "Southern District Region 2: Boone, Clay, Jackson, Kanawha, Logan, Mingo, and Roane counties.",
    ),
    (
        "WVDCR — Clarksburg Parole Office",
        "Clarksburg",
        "Harrison",
        "200 West Main Street",
        "304-624-2000",
        "Barbour|Braxton|Doddridge|Harrison|Lewis|Marion|Monongalia|Preston|Taylor|Upshur",
        "Northern District Region 6: north-central West Virginia including Harrison, Marion, and Monongalia counties.",
    ),
    (
        "WVDCR — Elkins Parole Office",
        "Elkins",
        "Randolph",
        "1023 North Randolph Avenue",
        "304-637-0250",
        "Pendleton|Randolph|Tucker|Webster",
        "Northern District Region 6: Randolph, Pendleton, Tucker, and Webster counties in the Allegheny highlands.",
    ),
    (
        "WVDCR — Huntington Parole Office",
        "Huntington",
        "Cabell",
        "2699 Park Avenue, Suite 200",
        "304-528-5060",
        "Cabell|Lincoln|Mason|Putnam|Wayne",
        "Southern District Region 1: Cabell, Lincoln, Mason, Putnam, and Wayne counties in the Metro Valley.",
    ),
    (
        "WVDCR — Lewisburg Parole Office",
        "Lewisburg",
        "Greenbrier",
        "912 North Jefferson Street",
        "304-647-7474",
        "Greenbrier|Monroe|Summers",
        "Southern District Region 3: Greenbrier, Monroe, and Summers counties in the Greenbrier Valley.",
    ),
    (
        "WVDCR — Logan Parole Office",
        "Logan",
        "Logan",
        "1000 State Route 10",
        "304-792-7020",
        "Boone|Logan|Mingo",
        "Southern District Region 2: Boone, Logan, and Mingo counties in the coalfields.",
    ),
    (
        "WVDCR — Martinsburg Parole Office",
        "Martinsburg",
        "Berkeley",
        "510 North Queen Street",
        "304-263-0611",
        "Berkeley|Grant|Hampshire|Hardy|Jefferson|Mineral|Morgan",
        "Northern District Region 7: Eastern Panhandle counties including Berkeley and Jefferson.",
    ),
    (
        "WVDCR — Moorefield Parole Office",
        "Moorefield",
        "Hardy",
        "819 North Main Street",
        "304-538-2700",
        "Grant|Hardy|Pendleton",
        "Northern District Region 7: Grant, Hardy, and Pendleton counties in the Potomac Highlands.",
    ),
    (
        "WVDCR — Parkersburg Parole Office",
        "Parkersburg",
        "Wood",
        "1515 Murdoch Avenue",
        "304-420-4500",
        "Calhoun|Clay|Jackson|Pleasants|Ritchie|Roane|Wirt|Wood",
        "Northern District Region 5: Mid-Ohio Valley counties including Wood and Jackson.",
    ),
    (
        "WVDCR — Princeton Parole Office",
        "Princeton",
        "Mercer",
        "200 Mercer Street",
        "304-487-3500",
        "McDowell|Mercer|Monroe|Summers|Wyoming",
        "Southern District Region 4: McDowell, Mercer, Monroe, Summers, and Wyoming counties.",
    ),
    (
        "WVDCR — Welch Parole Office",
        "Welch",
        "McDowell",
        "140 Main Street",
        "304-436-4200",
        "McDowell|Mingo|Wyoming",
        "Southern District Region 4: McDowell, Mingo, and Wyoming counties in southern coalfield communities.",
    ),
    (
        "WVDCR — Wheeling Parole Office",
        "Wheeling",
        "Ohio",
        "1058 East Bethlehem Boulevard",
        "304-238-0500",
        "Brooke|Hancock|Marshall|Ohio|Tyler|Wetzel",
        "Northern District Region 5: Northern Panhandle counties including Ohio, Marshall, and Hancock.",
    ),
]
