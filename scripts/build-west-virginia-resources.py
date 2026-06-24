#!/usr/bin/env python3
"""Generate west-virginia-resources.csv and west-virginia-research-log.csv.

RESOURCES_UUID_PREFIX comment d7000001
"""
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES_PATH = ROOT / "data" / "west-virginia-resources.csv"
LOG_PATH = ROOT / "data" / "west-virginia-research-log.csv"
DATE = "2026-06-24"

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
    name="WVDCR — Offender Services & Reentry Planning",
    category="state-agency", region="Statewide",
    description="The West Virginia Division of Corrections and Rehabilitation Offender Services division coordinates statewide reentry planning, the Reentry Planner tool, parole services, and community corrections partnerships for people in WVDCR custody or under community supervision. Staff connect returning citizens to housing, employment, treatment, and DoHS benefits through parole agents and published program directories—not a walk-in crisis line or emergency cash provider.",
    description_es="La división de Servicios para Personas Privadas de Libertad del WVDCR coordina planificación estatal de reinserción, la herramienta Reentry Planner, servicios de libertad condicional y alianzas de correcciones comunitarias para personas bajo custodia o supervisión del WVDCR. El personal conecta a ciudadanos que regresan con vivienda, empleo, tratamiento y beneficios DoHS a través de agentes de libertad condicional—no es una línea de crisis ni proveedor de efectivo de emergencia.",
    address="1409 Greenbrier Street", city="Charleston", phone="304-558-2036", email="",
    website="https://dcr.wv.gov/aboutus/offender-services/Pages/default.aspx",
    eligibility="West Virginia residents under WVDCR custody, parole, or community supervision seeking reentry coordination; community partners seeking WVDCR engagement.",
    eligibility_es="Residentes de Virginia Occidental bajo custodia, libertad condicional o supervisión comunitaria del WVDCR que buscan coordinación de reinserción; aliados comunitarios.",
    notes="Use the Reentry Planner at dcr.wv.gov; contact your parole agent for services; call 211 for community resource navigation.",
    notes_es="Use el Reentry Planner en dcr.wv.gov; contacte a su agente de libertad condicional; llame al 211 para navegación de recursos comunitarios.",
    hours="State office Monday–Friday business hours",
    tags="statewide|reentry|WVDCR|DOC|parole|reentry-planner",
    services="Reentry planning|Reentry Planner tool|Parole services coordination|Community corrections partnerships|Pre-release resource navigation",
    county="Kanawha", served_counties="", coverage="statewide",
    _source="https://dcr.wv.gov/aboutus/offender-services/Pages/default.aspx", _source_type="government", _confidence="high",
)
add(
    name="WV PATH — Public Benefits Portal",
    category="financial-assistance", region="Statewide",
    description="WV PATH is West Virginia's official statewide portal for applying for and managing Medicaid, SNAP food assistance, TANF cash benefits, LIEAP energy assistance, and child care subsidies through the Department of Human Services. Justice-involved individuals can apply for health coverage and food support after release; county DoHS field offices assist with verification and redetermination.",
    description_es="WV PATH es el portal oficial estatal de Virginia Occidental para solicitar y administrar Medicaid, SNAP, asistencia en efectivo TANF, LIEAP y subsidios de cuidado infantil a través del Departamento de Servicios Humanos. Personas en reinserción pueden solicitar cobertura de salud y apoyo alimentario después de la liberación; las oficinas DoHS del condado ayudan con verificación.",
    address="", city="", phone="1-877-716-1212", email="", website="https://wvpath.wv.gov",
    eligibility="West Virginia residents meeting income and program requirements for Medicaid, SNAP, or cash assistance; criminal record generally not a barrier.",
    eligibility_es="Residentes de Virginia Occidental que cumplan requisitos de ingresos para Medicaid, SNAP o asistencia en efectivo; los antecedentes penales generalmente no son barrera.",
    notes="Apply online at wvpath.wv.gov; call 1-877-716-1212 for DoHS Customer Service; county field offices listed at dhhr.wv.gov/Pages/Field-Offices.aspx.",
    notes_es="Solicite en wvpath.wv.gov; llame al 1-877-716-1212 para Servicio al Cliente DoHS; oficinas del condado en dhhr.wv.gov.",
    hours="Online 24/7; DoHS office hours vary by county",
    tags="statewide|benefits|SNAP|Medicaid|WV-PATH|online",
    services="Medicaid application|SNAP enrollment|Cash assistance application|LIEAP energy assistance|Benefits account management",
    county="", served_counties="", coverage="statewide",
    _source="https://wvpath.wv.gov", _source_type="government", _confidence="high",
)
add(
    name="211 West Virginia",
    category="state-agency", region="Statewide",
    description="211 West Virginia is a free statewide information and referral service connecting residents to health and human services including housing, food, utilities, employment, and crisis support. United Way-supported navigators help callers find local programs by need and ZIP code across all 55 counties. 211 West Virginia is a referral line—not a direct-service provider.",
    description_es="211 West Virginia es un servicio gratuito de información y referencia estatal que conecta a residentes con servicios de salud y humanos incluyendo vivienda, alimentos, servicios públicos, empleo y apoyo en crisis. Navegadores apoyados por United Way ayudan a encontrar programas locales por necesidad y código postal en los 55 condados. Es una línea de referencia, no un proveedor directo.",
    address="", city="", phone="211", email="", website="https://www.wv211.org",
    eligibility="Open to all West Virginia residents; no criminal-record restrictions stated.",
    eligibility_es="Abierto a todos los residentes de Virginia Occidental; sin restricciones de antecedentes indicadas.",
    notes="Dial 211 from any West Virginia phone; search resources online at wv211.org; available 24/7 for information and referral.",
    notes_es="Marque 211 desde cualquier teléfono de WV; busque recursos en wv211.org; disponible 24/7.",
    hours="Available 24/7",
    tags="statewide|hotline|211|referral-only|basic-needs",
    services="Information and referral|Housing resource navigation|Benefits referrals|Crisis resource connections",
    county="", served_counties="", coverage="statewide",
    _source="https://www.wv211.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="DoHS — Family Assistance & Benefits Overview",
    category="financial-assistance", region="Statewide",
    description="The West Virginia Department of Human Services administers SNAP, Medicaid, WV WORKS cash assistance, LIEAP, and child care subsidies through county DoHS field offices in every county and the WV PATH online portal. DoHS helps returning citizens establish food and health benefits after release from WVDCR custody or county jails.",
    description_es="El Departamento de Servicios Humanos de Virginia Occidental administra SNAP, Medicaid, asistencia en efectivo WV WORKS, LIEAP y subsidios de cuidado infantil a través de oficinas DoHS en cada condado y el portal WV PATH. DoHS ayuda a ciudadanos que regresan a establecer beneficios alimentarios y de salud después de la liberación.",
    address="350 Capitol Street", city="Charleston", phone="1-877-716-1212", email="",
    website="https://dhhr.wv.gov/bcf/Pages/default.aspx",
    eligibility="West Virginia residents meeting income and household-size requirements; criminal record generally not a barrier to SNAP and Medicaid.",
    eligibility_es="Residentes de Virginia Occidental que cumplan requisitos de ingresos y tamaño del hogar; los antecedentes penales generalmente no son barrera para SNAP y Medicaid.",
    notes="Apply at wvpath.wv.gov or visit your county DoHS field office; call 1-877-716-1212 for help; bring ID and release documents.",
    notes_es="Solicite en wvpath.wv.gov o visite su oficina DoHS del condado; llame al 1-877-716-1212; traiga identificación y documentos de liberación.",
    hours="County offices typically Monday–Friday, 8:30 a.m.–5:00 p.m.",
    tags="statewide|benefits|SNAP|Medicaid|DoHS|reentry",
    services="SNAP enrollment|Medicaid application|Cash assistance|LIEAP energy help|County field office referrals",
    county="Kanawha", served_counties="", coverage="statewide",
    _source="https://dhhr.wv.gov/bcf/Pages/default.aspx", _source_type="government", _confidence="high",
)
add(
    name="Legal Aid of West Virginia — Statewide Intake",
    category="legal-aid", region="Statewide",
    description="Legal Aid of West Virginia is the state's primary nonprofit civil legal aid provider serving low-income residents with housing, public benefits, family law, consumer issues, and criminal record expungement assistance under West Virginia Clean Slate and expungement statutes. Centralized intake at 866-255-4373 routes callers to regional offices—not criminal defense.",
    description_es="Legal Aid of West Virginia es el principal proveedor sin fines de lucro de asistencia legal civil del estado sirviendo a residentes de bajos ingresos con vivienda, beneficios públicos, derecho familiar y eliminación de antecedentes penales bajo estatutos estatales. La admisión centralizada al 866-255-4373 enruta a oficinas regionales—no defensa penal.",
    address="901 Quarrier Street", city="Charleston", phone="866-255-4373", email="",
    website="https://www.lawv.net",
    eligibility="Low-income West Virginia residents with non-criminal legal problems; LSC income limits apply; expungement eligibility depends on offense type and waiting periods.",
    eligibility_es="Residentes de Virginia Occidental de bajos ingresos con problemas legales no penales; aplican límites de ingresos LSC; la elegibilidad para eliminación de antecedentes depende del tipo de delito.",
    notes="Apply online at lawv.net or call 866-255-4373; routes to Charleston, Huntington, Clarksburg, Wheeling, and Martinsburg offices by county.",
    notes_es="Solicite en lawv.net o llame al 866-255-4373; enruta a oficinas de Charleston, Huntington, Clarksburg, Wheeling y Martinsburg por condado.",
    hours="Intake Monday–Friday business hours; online application 24/7",
    tags="statewide|legal-aid|low-income|expungement|hotline",
    services="Civil legal representation|Expungement assistance|Housing legal aid|Benefits advocacy|Regional office referrals",
    county="Kanawha", served_counties="", coverage="statewide",
    _source="https://www.lawv.net", _source_type="nonprofit", _confidence="high",
)
add(
    name="WorkForce West Virginia — Statewide Portal",
    category="employment", region="Statewide",
    description="WorkForce West Virginia is the state workforce agency connecting job seekers—including justice-involved West Virginians—to American Job Centers, career coaching, unemployment services, and WIOA training referrals in seven regional workforce development areas covering all 55 counties. Jobs & Hope recovery workforce navigation is coordinated through WorkForce WV partners.",
    description_es="WorkForce West Virginia es la agencia estatal de fuerza laboral que conecta a buscadores de empleo—incluidos virginianos occidentales con antecedentes penales—a Centros de Empleo Americanos, coaching de carrera, servicios de desempleo y referencias de capacitación WIOA en siete regiones que cubren los 55 condados. Jobs & Hope se coordina a través de aliados de WorkForce WV.",
    address="1900 Kanawha Boulevard East", city="Charleston", phone="304-558-1541", email="",
    website="https://workforcewv.org",
    eligibility="Open to West Virginia job seekers including justice-involved individuals; core AJC services are free.",
    eligibility_es="Abierto a buscadores de empleo de Virginia Occidental incluidas personas con antecedentes penales; servicios básicos del CEA son gratuitos.",
    notes="Find your local workforce board at workforcedb.wv.gov; call 304-558-1541 for statewide information; Jobs & Hope at jobsandhope.wv.gov.",
    notes_es="Encuentre su junta local en workforcedb.wv.gov; llame al 304-558-1541; Jobs & Hope en jobsandhope.wv.gov.",
    hours="State and AJC offices Monday–Friday business hours",
    tags="statewide|employment|WorkForce-WV|AJC|WIOA|Jobs-and-Hope",
    services="Job search assistance|Career coaching|WIOA training referrals|Unemployment services|Fair-chance employment navigation",
    county="Kanawha", served_counties="", coverage="statewide",
    _source="https://workforcewv.org", _source_type="government", _confidence="high",
)
add(
    name="Jobs & Hope West Virginia",
    category="employment", region="Statewide",
    description="Jobs & Hope West Virginia is a statewide initiative connecting West Virginians in recovery from substance use disorder to employment, training, peer support, and wraparound services through WorkForce West Virginia and community partners. The program helps justice-involved participants in recovery rebuild workforce credentials—a navigation program, not emergency cash or housing.",
    description_es="Jobs & Hope West Virginia es una iniciativa estatal que conecta a virginianos occidentales en recuperación de trastornos por uso de sustancias con empleo, capacitación, apoyo entre pares y servicios integrales a través de WorkForce WV y aliados comunitarios. Ayuda a participantes con antecedentes penales en recuperación—un programa de navegación, no efectivo o vivienda de emergencia.",
    address="", city="Charleston", phone="304-558-1541", email="", website="https://jobsandhope.wv.gov",
    eligibility="West Virginia residents in recovery from substance use disorder seeking employment and training supports; program-specific requirements apply.",
    eligibility_es="Residentes de Virginia Occidental en recuperación de trastornos por uso de sustancias que buscan apoyos de empleo y capacitación; aplican requisitos específicos del programa.",
    notes="Visit jobsandhope.wv.gov or contact your local WorkForce West Virginia American Job Center; partners include treatment and peer recovery providers.",
    notes_es="Visite jobsandhope.wv.gov o contacte su Centro de Empleo Americano local de WorkForce WV; aliados incluyen proveedores de tratamiento y recuperación entre pares.",
    hours="Contact local AJC for hours",
    tags="statewide|employment|recovery|Jobs-and-Hope|substance-use|reentry",
    services="Recovery workforce navigation|Employment training referrals|Peer support linkage|WorkForce WV coordination|Credential building",
    county="Kanawha", served_counties="", coverage="statewide",
    _source="https://jobsandhope.wv.gov", _source_type="government", _confidence="high",
)
add(
    name="988 Suicide & Crisis Lifeline — West Virginia",
    category="healthcare", region="Statewide",
    description="Free confidential 24/7 crisis support for people experiencing mental health emergencies, suicidal thoughts, or substance use crises. Trained specialists provide immediate support and can connect callers to local mobile crisis teams in West Virginia. Available to anyone—not reentry-specific but essential for justice-involved individuals in crisis.",
    description_es="Apoyo gratuito y confidencial 24/7 para emergencias de salud mental, pensamientos suicidas o crisis por uso de sustancias. Especialistas capacitados ofrecen apoyo inmediato y conexión a equipos de crisis móviles en Virginia Occidental. Disponible para cualquier persona, esencial para personas con antecedentes penales en crisis.",
    address="", city="", phone="988", email="", website="https://988lifeline.org",
    eligibility="Open to anyone in West Virginia experiencing a mental health or suicide crisis; no eligibility restrictions.",
    eligibility_es="Abierto a cualquier persona en Virginia Occidental en crisis de salud mental o suicidio; sin restricciones.",
    notes="Call or text 988; Spanish-language support available. For immediate physical danger call 911.",
    notes_es="Llame o envíe texto al 988; soporte en español disponible. Para peligro físico inmediato llame al 911.",
    hours="Available 24/7",
    tags="statewide|hotline|crisis|mental-health|988",
    services="Crisis counseling|Suicide prevention support|Mental health referrals|Substance use crisis support",
    county="", served_counties="", coverage="statewide",
    _source="https://988lifeline.org", _source_type="government", _confidence="high",
)
add(
    name="SAMHSA National Helpline",
    category="substance-use-treatment", region="Statewide",
    description="Free confidential 24/7 treatment referral and information service for individuals and families facing mental health or substance use disorders. Provides referrals to local treatment facilities and community organizations in West Virginia and nationwide. Spanish-language support available through trained specialists.",
    description_es="Servicio gratuito y confidencial 24/7 de referencia e información para personas y familias con trastornos de salud mental o uso de sustancias. Proporciona referencias a centros de tratamiento locales en Virginia Occidental y a nivel nacional. Soporte en español disponible.",
    address="", city="", phone="800-662-4357", email="", website="https://www.samhsa.gov/find-help/national-helpline",
    eligibility="Open to anyone in the United States seeking substance use or mental health treatment information and referrals.",
    eligibility_es="Abierto a cualquier persona en Estados Unidos que busque información y referencias de tratamiento.",
    notes="TTY 800-487-4889; also use FindTreatment.gov to search West Virginia providers online.",
    notes_es="TTY 800-487-4889; también use FindTreatment.gov para buscar proveedores en Virginia Occidental.",
    hours="Available 24/7",
    tags="statewide|hotline|substance-use|treatment-referral|national",
    services="Treatment referrals|Substance use information|Mental health resource navigation",
    county="", served_counties="", coverage="statewide",
    _source="https://www.samhsa.gov/find-help/national-helpline", _source_type="government", _confidence="high",
)
add(
    name="FindTreatment.gov — West Virginia Provider Search",
    category="substance-use-treatment", region="Statewide",
    description="SAMHSA's online treatment locator helping West Virginia residents find substance use and mental health treatment providers by location, service type, and payment options including Medicaid. Justice-involved individuals can search outpatient, residential, and MAT providers before or after release from WVDCR custody or county jails.",
    description_es="Localizador en línea de SAMHSA que ayuda a residentes de Virginia Occidental a encontrar proveedores de tratamiento de uso de sustancias y salud mental por ubicación, tipo de servicio y opciones de pago incluido Medicaid. Personas con antecedentes penales pueden buscar proveedores ambulatorios, residenciales y TMO antes o después de la liberación.",
    address="", city="", phone="", email="", website="https://findtreatment.gov",
    eligibility="Open to anyone searching for treatment; provider admission rules vary.",
    eligibility_es="Abierto a cualquier persona que busque tratamiento; las reglas de admisión varían según el proveedor.",
    notes="Search findtreatment.gov by West Virginia county or city; filter for MAT, outpatient, or residential services.",
    notes_es="Busque en findtreatment.gov por condado o ciudad de Virginia Occidental; filtre por TMO, ambulatorio o residencial.",
    hours="Website 24/7",
    tags="statewide|substance-use|online|MAT|treatment-locator",
    services="Treatment provider search|MAT locator|Outpatient program finder|Residential program finder",
    county="", served_counties="", coverage="statewide",
    _source="https://findtreatment.gov", _source_type="government", _confidence="high",
)
add(
    name="DoHS — Behavioral Health & Substance Use Portal",
    category="healthcare", region="Statewide",
    description="West Virginia Department of Human Services coordinates publicly funded behavioral health and substance use disorder services through regional provider networks and Medicaid managed care plans helping justice-involved West Virginians connect to treatment after release. For crisis call 988. Returning citizens should call ahead to confirm walk-in hours and referral requirements.",
    description_es="El Departamento de Servicios Humanos de Virginia Occidental coordina servicios públicos de salud conductual y trastornos por uso de sustancias a través de redes regionales y planes Medicaid ayudando a virginianos occidentales con antecedentes penales a conectarse al tratamiento después de la liberación. Para crisis llame al 988.",
    address="350 Capitol Street", city="Charleston", phone="304-558-0627", email="",
    website="https://dhhr.wv.gov/Office-of-Drug-Control-Policy/Pages/default.aspx",
    eligibility="West Virginia Medicaid beneficiaries and residents accessing publicly funded behavioral health services; eligibility varies by provider.",
    eligibility_es="Beneficiarios de Medicaid de Virginia Occidental y residentes que acceden a servicios públicos de salud conductual; la elegibilidad varía según el proveedor.",
    notes="For immediate crisis call 988; locate regional providers through DoHS Office of Drug Control Policy; Prestera and Seneca serve multiple regions.",
    notes_es="Para crisis inmediata llame al 988; localice proveedores regionales a través de la Oficina de Control de Drogas de DoHS.",
    hours="State office Mon–Fri business hours; 988 available 24/7",
    tags="statewide|mental-health|substance-use|Medicaid|referral-only",
    services="Treatment referrals|Medicaid behavioral health navigation|Regional provider locator|Substance use resource information",
    county="Kanawha", served_counties="", coverage="statewide",
    _source="https://dhhr.wv.gov/Office-of-Drug-Control-Policy/Pages/default.aspx", _source_type="government", _confidence="high",
)
add(
    name="West Virginia Department of Veterans Assistance",
    category="veterans", region="Statewide",
    description="West Virginia Department of Veterans Assistance connects veterans and families to federal VA benefits, state veteran programs, and county Veterans Service Officers statewide including justice-involved veterans navigating healthcare enrollment and benefits restoration after incarceration.",
    description_es="El Departamento de Asistencia para Veteranos de Virginia Occidental conecta a veteranos y familias con beneficios federales del VA, programas estatales para veteranos y Oficiales de Servicios para Veteranos del condado incluidos veteranos con antecedentes penales que restauran beneficios después de la encarcelación.",
    address="1900 Kanawha Boulevard East", city="Charleston", phone="304-558-3661", email="",
    website="https://veterans.wv.gov",
    eligibility="West Virginia veterans, service members, and eligible family members; VA eligibility depends on discharge status and service history.",
    eligibility_es="Veteranos, miembros del servicio y familiares elegibles de Virginia Occidental; la elegibilidad del VA depende del tipo de baja e historial de servicio.",
    notes="Call 304-558-3661 or visit veterans.wv.gov; locate county Veterans Service Officers for local claims assistance.",
    notes_es="Llame al 304-558-3661 o visite veterans.wv.gov; localice Oficiales de Servicios para Veteranos del condado para ayuda con reclamaciones.",
    hours="State office Monday–Friday business hours",
    tags="statewide|veterans|VA|VSO|reentry",
    services="VA benefits navigation|State veterans programs|County VSO referrals|Healthcare enrollment assistance",
    county="Kanawha", served_counties="", coverage="statewide",
    _source="https://veterans.wv.gov", _source_type="government", _confidence="high",
)
add(
    name="West Virginia Division of Motor Vehicles — ID Services",
    category="id-documentation", region="Statewide",
    description="West Virginia DMV issues REAL ID-compliant driver's licenses and state identification cards at regional offices statewide. Reentry partners help returning citizens gather proof of identity and residency documents required for employment and WV PATH benefits enrollment after incarceration.",
    description_es="El DMV de Virginia Occidental emite licencias de conducir compatibles con REAL ID y tarjetas de identificación estatal en oficinas regionales en todo el estado. Los aliados de reinserción ayudan a ciudadanos que regresan a reunir prueba de identidad y residencia requerida para empleo e inscripción en WV PATH.",
    address="1800 Washington Street East", city="Charleston", phone="304-926-3802", email="",
    website="https://transportation.wv.gov/DMV",
    eligibility="West Virginia residents; fees apply; bring certified birth certificate, Social Security card, and two proofs of WV residency.",
    eligibility_es="Residentes de Virginia Occidental; aplican tarifas; traiga certificado de nacimiento, tarjeta de Seguro Social y dos pruebas de residencia en WV.",
    notes="Schedule appointments at transportation.wv.gov/DMV; regional offices listed by county; legal aid partners assist with document gathering.",
    notes_es="Programe citas en transportation.wv.gov/DMV; oficinas regionales listadas por condado; aliados legales ayudan a reunir documentos.",
    hours="Regional office hours vary; check DMV website",
    tags="statewide|ID|DMV|REAL-ID|documentation",
    services="Driver's license issuance|State ID cards|REAL ID compliance|Credential reinstatement guidance",
    county="Kanawha", served_counties="", coverage="statewide",
    _source="https://transportation.wv.gov/DMV", _source_type="government", _confidence="high",
)
add(
    name="WVDCR — Reentry Planner (Online Tool)",
    category="reentry-organizations", region="Statewide",
    description="The WVDCR Reentry Planner is an online resource directory published by the Division of Corrections and Rehabilitation helping returning citizens, families, and community partners locate reentry services by category and county across West Virginia. The tool connects users to verified partners—it is a navigation directory, not a direct-service provider or crisis line.",
    description_es="El Reentry Planner del WVDCR es un directorio de recursos en línea publicado por la División de Correcciones y Rehabilitación que ayuda a ciudadanos que regresan, familias y aliados comunitarios a localizar servicios de reinserción por categoría y condado en Virginia Occidental. Conecta usuarios con aliados verificados—es un directorio de navegación, no un proveedor directo ni línea de crisis.",
    address="", city="Charleston", phone="304-558-2036", email="",
    website="https://dcr.wv.gov/aboutus/offender-services/Pages/reentry-planner.aspx",
    eligibility="Open to West Virginia justice-involved residents, families, and service providers seeking reentry resource navigation.",
    eligibility_es="Abierto a residentes con antecedentes penales de Virginia Occidental, familias y proveedores de servicios que buscan navegación de recursos de reinserción.",
    notes="Search by county and service type at dcr.wv.gov Reentry Planner; also see wvreentry.org for REACH Initiative councils.",
    notes_es="Busque por condado y tipo de servicio en el Reentry Planner de dcr.wv.gov; también vea wvreentry.org para consejos REACH.",
    hours="Website 24/7",
    tags="statewide|reentry|WVDCR|online|referral-only|reentry-planner",
    services="Reentry resource directory|County service search|Partner agency navigation|Category-based referrals",
    county="Kanawha", served_counties="", coverage="statewide",
    _source="https://dcr.wv.gov/aboutus/offender-services/Pages/reentry-planner.aspx", _source_type="government", _confidence="high",
)
add(
    name="West Virginia Coalition Against Domestic Violence",
    category="family-children", region="Statewide",
    description="West Virginia Coalition Against Domestic Violence connects survivors to local domestic violence programs, shelter, and legal advocacy statewide including family members affected by partner violence during reentry. The statewide hotline helps locate county programs—call for 24/7 support.",
    description_es="La Coalición de Virginia Occidental Contra la Violencia Doméstica conecta a sobrevivientes con programas locales de violencia doméstica, refugio y defensa legal en todo el estado incluidos familiares afectados por violencia de pareja durante la reinserción. La línea directa estatal ayuda a localizar programas del condado—llame para apoyo 24/7.",
    address="", city="Charleston", phone="800-799-7233", email="", website="https://www.wvcadv.org",
    eligibility="Survivors of domestic violence and their families in West Virginia; services vary by local program.",
    eligibility_es="Sobrevivientes de violencia doméstica y sus familias en Virginia Occidental; los servicios varían según el programa local.",
    notes="Call 800-799-7233 for the National Domestic Violence Hotline routing to local WV programs; wvcadv.org lists member agencies.",
    notes_es="Llame al 800-799-7233 para enrutamiento a programas locales de WV; wvcadv.org lista agencias miembro.",
    hours="Hotline 24/7; local program hours vary",
    tags="statewide|domestic-violence|family|hotline|shelter",
    services="Domestic violence hotline|Shelter referrals|Legal advocacy referrals|Local program locator",
    county="Kanawha", served_counties="", coverage="statewide",
    _source="https://www.wvcadv.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="West Virginia Adult Education — State Program Locator",
    category="education", region="Statewide",
    description="West Virginia Department of Education adult education directory connects returning citizens to local GED, high school equivalency, and English language programs at community colleges and community sites in every county. Programs are typically free or low-cost for West Virginia adults seeking workforce credentials after incarceration.",
    description_es="El directorio de educación para adultos del Departamento de Educación de Virginia Occidental conecta a ciudadanos que regresan con programas locales de GED, equivalencia de secundaria e inglés en colegios comunitarios y sitios comunitarios en cada condado. Los programas suelen ser gratuitos o de bajo costo.",
    address="", city="Charleston", phone="304-558-2440", email="",
    website="https://wvde.us/adult-education",
    eligibility="West Virginia adults age 16 and older not enrolled in high school; criminal record not a stated barrier.",
    eligibility_es="Adultos de Virginia Occidental de 16 años o más no inscritos en secundaria; los antecedentes penales no son barrera indicada.",
    notes="Search wvde.us/adult-education by county; contact local adult education provider for orientation and enrollment.",
    notes_es="Busque en wvde.us/adult-education por condado; contacte al proveedor local para orientación e inscripción.",
    hours="Program hours vary by county site",
    tags="statewide|education|GED|adult-ed|workforce-credentials",
    services="GED preparation|High school equivalency|English language instruction|Workforce credential pathways",
    county="Kanawha", served_counties="", coverage="statewide",
    _source="https://wvde.us/adult-education", _source_type="government", _confidence="high",
)
add(
    name="Mountaineer Food Bank — Statewide Partner Network",
    category="food-nutrition", region="Statewide",
    description="Mountaineer Food Bank is one of West Virginia's regional food bank networks distributing to partner pantries across north-central and eastern counties, helping returning citizens locate emergency food by ZIP code through the online food finder at mountaineerfoodbank.org.",
    description_es="Mountaineer Food Bank es una de las redes regionales de bancos de alimentos de Virginia Occidental que distribuye a despensas aliadas en condados del centro-norte y este, ayudando a ciudadanos que regresan a localizar alimentos de emergencia por código postal.",
    address="484 Enterprise Drive", city="Gassaway", phone="304-364-5518", email="",
    website="https://www.mountaineerfoodbank.org",
    eligibility="Open to West Virginia residents needing food assistance; partner pantry rules vary by location.",
    eligibility_es="Abierto a residentes de Virginia Occidental que necesitan asistencia alimentaria; las reglas de despensas aliadas varían.",
    notes="Use mountaineerfoodbank.org/find-food for nearest pantry; also see facinghunger.org for Metro Valley coverage.",
    notes_es="Use mountaineerfoodbank.org/find-food para la despensa más cercana; también vea facinghunger.org para el valle metropolitano.",
    hours="Food bank Mon–Fri business hours; pantry hours vary",
    tags="statewide|food-bank|pantry|SNAP-partner|reentry",
    services="Partner pantry referrals|Mobile food distribution|SNAP outreach|Online food finder",
    county="Braxton", served_counties="", coverage="statewide",
    _source="https://www.mountaineerfoodbank.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="West Virginia Community Action Partnership",
    category="basic-needs", region="Statewide",
    description="West Virginia Community Action Partnership connects low-income residents to local Community Action Agencies in every county offering utility assistance, weatherization, emergency aid, and case management. Returning citizens can locate county CAA offices for basic needs support after release through the statewide agency locator.",
    description_es="West Virginia Community Action Partnership conecta a residentes de bajos ingresos con Agencias de Acción Comunitaria locales en cada condado que ofrecen asistencia de servicios públicos, climatización, ayuda de emergencia y manejo de casos. Ciudadanos que regresan pueden localizar oficinas CAA del condado para apoyo de necesidades básicas.",
    address="814 Quarrier Street", city="Charleston", phone="304-414-4444", email="",
    website="https://www.wvcap.org",
    eligibility="Low-income West Virginia residents; income verification required for emergency assistance programs.",
    eligibility_es="Residentes de Virginia Occidental de bajos ingresos; se requiere verificación de ingresos para programas de asistencia de emergencia.",
    notes="Find your local Community Action Agency at wvcap.org; services vary by county including North Central, Southern, and Eastern agencies.",
    notes_es="Encuentre su Agencia de Acción Comunitaria local en wvcap.org; los servicios varían por condado.",
    hours="County agency hours vary",
    tags="statewide|community-action|utility-help|emergency-aid|reentry",
    services="Utility assistance|Weatherization|Emergency aid|Case management|County agency locator",
    county="Kanawha", served_counties="", coverage="statewide",
    _source="https://www.wvcap.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="HELP4WV — Mental Health & SUD Helpline",
    category="substance-use-treatment", region="Statewide",
    description="HELP4WV is West Virginia's 24/7 helpline connecting residents to behavioral health crisis support, substance use treatment referrals, and peer recovery navigation through the Department of Human Services. Specialists help callers find local treatment and recovery resources including justice-involved individuals—not a replacement for 988 emergency crisis response.",
    description_es="HELP4WV es la línea de ayuda 24/7 de Virginia Occidental que conecta a residentes con apoyo de crisis de salud conductual, referencias de tratamiento de sustancias y navegación de recuperación entre pares a través de DoHS. Especialistas ayudan a encontrar recursos locales incluidas personas con antecedentes penales—no reemplaza la respuesta de crisis 988.",
    address="", city="", phone="844-435-7498", email="", website="https://www.help4wv.com",
    eligibility="Open to West Virginia residents seeking behavioral health or substance use treatment information and referrals.",
    eligibility_es="Abierto a residentes de Virginia Occidental que buscan información y referencias de salud conductual o uso de sustancias.",
    notes="Call or text 844-435-7498; for suicide or immediate crisis also call 988; chat available at help4wv.com.",
    notes_es="Llame o envíe texto al 844-435-7498; para suicidio o crisis inmediata también llame al 988; chat en help4wv.com.",
    hours="Available 24/7",
    tags="statewide|hotline|substance-use|mental-health|peer-support",
    services="Treatment referrals|Crisis support navigation|Peer recovery linkage|Provider search assistance",
    county="", served_counties="", coverage="statewide",
    _source="https://www.help4wv.com", _source_type="government", _confidence="high",
)
add(
    name="West Virginia Housing Development Fund",
    category="housing", region="Statewide",
    description="West Virginia Housing Development Fund provides affordable housing resources, rental assistance programs, and housing locator tools for low-income residents including returning citizens seeking income-restricted rental units and emergency rental assistance when programs are open statewide.",
    description_es="West Virginia Housing Development Fund proporciona recursos de vivienda asequible, programas de asistencia de alquiler y herramientas de localización de vivienda para residentes de bajos ingresos incluidos ciudadanos que regresan que buscan unidades de alquiler restringidas por ingresos.",
    address="814 Quarrier Street", city="Charleston", phone="304-345-6475", email="",
    website="https://www.wvhdf.com",
    eligibility="Low-income West Virginia residents; program-specific income limits and availability apply.",
    eligibility_es="Residentes de Virginia Occidental de bajos ingresos; aplican límites de ingresos y disponibilidad específicos del programa.",
    notes="Search affordable rentals at wvhdf.com; emergency rental assistance availability varies; not an emergency shelter provider.",
    notes_es="Busque alquileres asequibles en wvhdf.com; la disponibilidad de asistencia de alquiler de emergencia varía; no es proveedor de refugio de emergencia.",
    hours="State office Monday–Friday business hours",
    tags="statewide|housing|affordable-housing|rental-assistance",
    services="Affordable housing locator|Rental assistance programs|Homeownership resources|Housing counseling referrals",
    county="Kanawha", served_counties="", coverage="statewide",
    _source="https://www.wvhdf.com", _source_type="government", _confidence="high",
)

from west_virginia_phase4_expansion import register_phase4
register_phase4(add)

from phase3b_gapfill import register_phase3b_west_virginia
register_phase3b_west_virginia(add, ENTRIES)

from west_virginia_pass2_expansion import register_pass2
register_pass2(add)

from west_virginia_phase5_depth_expansion import register_phase5
register_phase5(add)

from west_virginia_category_fill import register_category_fill
register_category_fill(add)

# Fix single-county served_counties
for entry in ENTRIES:
    if entry.get("coverage") == "single" and not entry.get("served_counties") and entry.get("county"):
        entry["served_counties"] = entry["county"]

from west_virginia_resources_data import ensure_entry_descriptions

for entry in ENTRIES:
    ensure_entry_descriptions(entry)

# Assign sequential IDs and write CSVs
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
