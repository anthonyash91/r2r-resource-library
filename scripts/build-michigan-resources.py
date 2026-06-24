#!/usr/bin/env python3
"""Generate michigan-resources.csv and michigan-research-log.csv.

RESOURCES_UUID_PREFIX comment d5000001
"""
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES_PATH = ROOT / "data" / "michigan-resources.csv"
LOG_PATH = ROOT / "data" / "michigan-research-log.csv"
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


# --- Phase 1: Statewide backbone (~20 rows) ---
add(
    name="MDOC — Offender Success Administration (OSA)",
    category="state-agency", region="Statewide",
    description="The Michigan Department of Corrections Offender Success Administration coordinates statewide reentry programming, education, In-Reach transition planning, and contracted community supports for prisoners, parolees, and probationers. OSA oversees Vocational Village skilled trades training, evidence-based programming in facilities, and 11 regional Offender Success Administrative Agencies. Contact your parole agent for services—not a walk-in crisis line.",
    description_es="La Administración Offender Success del Departamento de Corrección de Michigan coordina programación estatal de reinserción, educación, planificación de transición In-Reach y apoyos comunitarios contratados para prisioneros, personas en libertad condicional y probatoria. OSA supervisa Vocational Village, programación basada en evidencia y 11 agencias administrativas regionales. Contacte a su agente de libertad condicional, no es una línea de crisis.",
    address="400 South Walnut Street", city="Lansing", phone="517-241-0456",
    email="", website="https://www.michigan.gov/corrections/our-operations/osa",
    eligibility="Michigan residents under MDOC custody, parole, or probation seeking reentry coordination; community partners seeking OSA engagement.",
    eligibility_es="Residentes de Michigan bajo custodia, libertad condicional o probatoria del MDOC que buscan coordinación de reinserción; aliados comunitarios.",
    notes="See michigan.gov/corrections/our-operations/osa for Vocational Village, In-Reach, and regional admin agency contacts; call 211 for community resources.",
    notes_es="Consulte michigan.gov/corrections/our-operations/osa para Vocational Village, In-Reach y contactos de agencias regionales; llame al 211 para recursos comunitarios.",
    hours="State office Monday–Friday business hours",
    tags="statewide|reentry|DOC|OSA|Offender-Success",
    services="Reentry programming coordination|Vocational Village oversight|In-Reach transition planning|Regional admin agency contracts|Education and evidence-based programs",
    county="Ingham", served_counties="", coverage="statewide",
    _source="https://www.michigan.gov/corrections/our-operations/osa", _source_type="government", _confidence="high",
)
add(
    name="MDOC — Reentry Services (OSRS)",
    category="state-agency", region="Statewide",
    description="Offender Success Reentry Services section ensuring eligible parolees, SAI probationers, and HYTA trainees receive residential stability, job placement, health and behavioral health, and social supports through contracted regional agencies. Individuals should speak with their parole agent to determine available county services. Also directs returning citizens to 211 and the Calvin University/MDOC resource map.",
    description_es="Sección de Servicios de Reinserción Offender Success que garantiza que personas elegibles en libertad condicional reciban estabilidad residencial, colocación laboral, salud conductual y apoyos sociales a través de agencias regionales contratadas. Hable con su agente de libertad condicional para determinar servicios disponibles. También dirige a 211 y al mapa de recursos Calvin/MDOC.",
    address="400 South Walnut Street", city="Lansing", phone="517-241-0456",
    email="", website="https://www.michigan.gov/corrections/our-operations/osa/reentry-services",
    eligibility="Eligible MDOC parolees, SAI probationers, and HYTA trainees; services vary by county and parole agent authorization.",
    eligibility_es="Personas elegibles en libertad condicional del MDOC, libertad probatoria SAI y aprendices HYTA; los servicios varían según condado y autorización del agente.",
    notes="Community-based resources at 211 or Calvin University Returning Citizen Services map; contact regional Community Coordinator via OSA page.",
    notes_es="Recursos comunitarios en 211 o mapa de Servicios para Ciudadanos que Regresan de Calvin University; contacte al Coordinador Comunitario regional.",
    hours="Monday–Friday business hours",
    tags="statewide|reentry|DOC|housing|employment|referral-only",
    services="Residential stability referrals|Job placement assistance|Behavioral health coordination|Social supports|Community resource navigation",
    county="Ingham", served_counties="", coverage="statewide",
    _source="https://www.michigan.gov/corrections/our-operations/osa/reentry-services", _source_type="government", _confidence="high",
)
add(
    name="MI Bridges — Public Benefits Portal",
    category="financial-assistance", region="Statewide",
    description="Official statewide portal for applying for and managing Michigan public benefits including Medicaid, Healthy Michigan Plan, SNAP food assistance, cash assistance, and child care subsidies through MDHHS. Justice-involved individuals can apply for health coverage and food support after release. County MDHHS offices assist with verification and redetermination.",
    description_es="Portal oficial estatal para solicitar y administrar beneficios públicos de Michigan incluyendo Medicaid, Healthy Michigan Plan, SNAP, asistencia en efectivo y subsidios de cuidado infantil a través de MDHHS. Personas en reinserción pueden solicitar cobertura de salud y apoyo alimentario después de la liberación.",
    address="", city="", phone="844-464-3447", email="",
    website="https://newmibridges.michigan.gov",
    eligibility="Michigan residents meeting income and program requirements for Medicaid, SNAP, or cash assistance; criminal record generally not a barrier.",
    eligibility_es="Residentes de Michigan que cumplan requisitos de ingresos para Medicaid, SNAP o asistencia en efectivo; antecedentes penales generalmente no son barrera.",
    notes="Apply online at newmibridges.michigan.gov; call 844-464-3447 for MI Bridges help desk; county MDHHS offices listed at mdhhs.michigan.gov.",
    notes_es="Solicite en línea en newmibridges.michigan.gov; llame al 844-464-3447 para la mesa de ayuda; oficinas MDHHS del condado en mdhhs.michigan.gov.",
    hours="Online 24/7; MDHHS office hours vary",
    tags="statewide|benefits|SNAP|Medicaid|MI-Bridges|online",
    services="Medicaid application|SNAP enrollment|Cash assistance application|Benefits account management|County MDHHS referrals",
    county="", served_counties="", coverage="statewide",
    _source="https://newmibridges.michigan.gov", _source_type="government", _confidence="high",
)
add(
    name="Michigan 211",
    category="state-agency", region="Statewide",
    description="Free statewide information and referral service connecting Michiganders to health and human services including housing, food, utilities, employment, and crisis support. United Way–supported navigators help callers find local programs by need and ZIP code. Michigan 211 is a referral line—not a direct-service provider.",
    description_es="Servicio gratuito de información y referencia en todo el estado que conecta a los habitantes de Michigan con servicios de salud y humanos incluyendo vivienda, alimentos, empleo y apoyo en crisis. Navegadores apoyados por United Way ayudan a encontrar programas locales. Michigan 211 es una línea de referencia, no un proveedor directo.",
    address="", city="", phone="211", email="", website="https://www.mi211.org",
    eligibility="Open to all Michigan residents; no criminal-record restrictions stated.",
    eligibility_es="Abierto a todos los residentes de Michigan; sin restricciones de antecedentes indicadas.",
    notes="Dial 211 from any Michigan phone; search resources online at mi211.org; available 24/7 for information and referral.",
    notes_es="Marque 211 desde cualquier teléfono de Michigan; busque recursos en línea en mi211.org; disponible 24/7.",
    hours="Available 24/7",
    tags="statewide|hotline|211|referral-only|basic-needs",
    services="Information and referral|Housing resource navigation|Benefits referrals|Crisis resource connections",
    county="", served_counties="", coverage="statewide",
    _source="https://www.mi211.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="988 Suicide & Crisis Lifeline — Michigan",
    category="healthcare", region="Statewide",
    description="Free confidential 24/7 crisis support for people experiencing mental health emergencies, suicidal thoughts, or substance use crises. Trained specialists provide immediate support and can connect callers to local mobile crisis teams in Michigan. Available to anyone—not reentry-specific but essential for justice-involved individuals in crisis.",
    description_es="Apoyo gratuito y confidencial 24/7 para emergencias de salud mental, pensamientos suicidas o crisis por uso de sustancias. Especialistas capacitados ofrecen apoyo inmediato y conexión a equipos de crisis móviles en Michigan. Disponible para cualquier persona, esencial para personas con antecedentes penales en crisis.",
    address="", city="", phone="988", email="",
    website="https://988lifeline.org",
    eligibility="Open to anyone in Michigan experiencing a mental health or suicide crisis; no eligibility restrictions.",
    eligibility_es="Abierto a cualquier persona en Michigan en crisis de salud mental o suicidio; sin restricciones.",
    notes="Call or text 988; Spanish-language support available. For immediate physical danger call 911.",
    notes_es="Llame o envíe texto al 988; soporte en español disponible. Para peligro físico inmediato llame al 911.",
    hours="Available 24/7",
    tags="statewide|hotline|crisis|mental-health|988",
    services="Crisis counseling|Suicide prevention support|Mental health referrals|Substance use crisis support",
    county="", served_counties="", coverage="statewide",
    _source="https://988lifeline.org", _source_type="government", _confidence="high",
)
add(
    name="Legal Aid of Michigan — Statewide Intake",
    category="legal-aid", region="Statewide",
    description="Michigan's largest nonprofit civil legal aid provider serving low-income residents across the state with housing, public benefits, family law, consumer issues, and civil record-related matters through regional offices. Centralized intake connects callers to the appropriate local office. Does not handle criminal defense cases.",
    description_es="El mayor proveedor sin fines de lucro de asistencia legal civil de Michigan que sirve a residentes de bajos ingresos en todo el estado con vivienda, beneficios, derecho familiar y asuntos civiles relacionados con antecedentes. La admisión centralizada conecta con la oficina local. No maneja defensa penal.",
    address="3030 South State Street", city="Ann Arbor", phone="888-783-8190",
    email="", website="https://www.legalaidmichigan.org",
    eligibility="Low-income Michigan residents with non-criminal legal problems; income and household-size limits apply by federal LSC guidelines.",
    eligibility_es="Residentes de Michigan de bajos ingresos con problemas legales no penales; aplican límites de ingresos federales.",
    notes="Apply online at legalaidmichigan.org or call 888-783-8190; routes to Lakeshore, LSSCM, UPLS, and regional offices by county.",
    notes_es="Solicite en línea en legalaidmichigan.org o llame al 888-783-8190; enruta a Lakeshore, LSSCM, UPLS y oficinas regionales por condado.",
    hours="Intake Monday–Friday business hours; online application 24/7",
    tags="statewide|legal-aid|low-income|housing|hotline",
    services="Civil legal representation|Housing legal aid|Benefits advocacy|Regional office referrals|Expungement assistance",
    county="Washtenaw", served_counties="", coverage="statewide",
    _source="https://www.legalaidmichigan.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Michigan Legal Help",
    category="legal-aid", region="Statewide",
    description="Statewide legal information portal operated by the Michigan Advocacy Program providing plain-language guides, court forms, and self-help tools for housing, benefits, family law, and expungement. Helps residents understand civil legal options and connect to free or low-cost attorneys. Online resource hub—not a law firm providing direct representation.",
    description_es="Portal estatal de información legal operado por Michigan Advocacy Program con guías en lenguaje sencillo, formularios judiciales y herramientas de autoayuda para vivienda, beneficios y eliminación de antecedentes. Ayuda a conectar con asistencia legal gratuita o de bajo costo. Es un centro de recursos en línea, no un bufete.",
    address="", city="Ann Arbor", phone="", email="",
    website="https://michiganlegalhelp.org",
    eligibility="Open to all Michigan residents seeking civil legal information; direct representation eligibility varies by local legal aid provider.",
    eligibility_es="Abierto a todos los residentes de Michigan que buscan información legal civil; la representación directa varía según el proveedor local.",
    notes="Search michiganlegalhelp.org by topic and county; connects to Legal Aid of Michigan regional providers.",
    notes_es="Busque en michiganlegalhelp.org por tema y condado; conecta con proveedores regionales de Legal Aid of Michigan.",
    hours="Website 24/7",
    tags="statewide|legal-aid|online|housing|self-help",
    services="Legal information guides|Court form assistance|Local legal aid finder|Expungement resources|Benefits legal information",
    county="", served_counties="", coverage="statewide",
    _source="https://michiganlegalhelp.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="MDHHS — Behavioral Health & Substance Use Portal",
    category="healthcare", region="Statewide",
    description="Michigan Department of Health and Human Services portal coordinating publicly funded behavioral health services, substance use disorder treatment access, and Prepaid Inpatient Health Plan (PIHP) regional networks. Justice-involved individuals connect to county PIHPs and Medicaid behavioral health providers after release. For crisis call 988.",
    description_es="Portal del Departamento de Salud y Servicios Humanos de Michigan que coordina servicios públicos de salud conductual, acceso a tratamiento de trastornos por uso de sustancias y redes regionales PIHP. Personas con antecedentes penales se conectan a PIHPs del condado y proveedores Medicaid después de la liberación. Para crisis llame al 988.",
    address="333 South Grand Avenue", city="Lansing", phone="517-241-3740",
    email="", website="https://www.michigan.gov/mdhhs/assistance-programs/behavioral-health",
    eligibility="Michigan Medicaid beneficiaries and residents accessing publicly funded behavioral health services; eligibility varies by PIHP region.",
    eligibility_es="Beneficiarios de Medicaid de Michigan y residentes que acceden a servicios públicos de salud conductual; la elegibilidad varía según región PIHP.",
    notes="For immediate crisis call 988; locate county PIHP at mdhhs.michigan.gov behavioral health page; DWIHN serves Wayne County.",
    notes_es="Para crisis inmediata llame al 988; localice PIHP del condado en mdhhs.michigan.gov; DWIHN sirve al condado Wayne.",
    hours="State office Mon–Fri business hours; 988 available 24/7",
    tags="statewide|mental-health|substance-use|Medicaid|referral-only",
    services="PIHP regional locator|Treatment referrals|Medicaid behavioral health navigation|Substance use resource information",
    county="Ingham", served_counties="", coverage="statewide",
    _source="https://www.michigan.gov/mdhhs/assistance-programs/behavioral-health", _source_type="government", _confidence="high",
)
add(
    name="Michigan Rehabilitation Services (MRS)",
    category="employment", region="Statewide",
    description="State vocational rehabilitation agency helping Michiganders with disabilities including justice-involved individuals with documented disabilities obtain employment, training, and independent living supports. MRS counselors coordinate with MDOC reentry partners for clients with physical, mental, or cognitive disabilities affecting employment.",
    description_es="Agencia estatal de rehabilitación vocacional que ayuda a habitantes de Michigan con discapacidades, incluidas personas con antecedentes penales con discapacidades documentadas, a obtener empleo, capacitación y apoyos de vida independiente. Los consejeros MRS coordinan con aliados de reinserción del MDOC.",
    address="201 North Washington Square, 6th Floor", city="Lansing", phone="800-605-6722",
    email="", website="https://www.michigan.gov/leo/bureau-services/michigan-rehabilitation-services",
    eligibility="Michigan residents with disabilities that create a barrier to employment; eligibility determined through MRS assessment.",
    eligibility_es="Residentes de Michigan con discapacidades que crean una barrera al empleo; elegibilidad determinada mediante evaluación MRS.",
    notes="Call 800-605-6722 or apply at michigan.gov/leo MRS page; office locator by county; partners with Michigan Works! for job placement.",
    notes_es="Llame al 800-605-6722 o solicite en michigan.gov/leo; localizador de oficinas por condado; aliado con Michigan Works!.",
    hours="State and local offices Monday–Friday business hours",
    tags="statewide|employment|disability|MRS|vocational-rehab",
    services="Vocational rehabilitation counseling|Job training referrals|Assistive technology|Independent living supports|Employer placement assistance",
    county="Ingham", served_counties="", coverage="statewide",
    _source="https://www.michigan.gov/leo/bureau-services/michigan-rehabilitation-services", _source_type="government", _confidence="high",
)
add(
    name="SAMHSA National Helpline",
    category="substance-use-treatment", region="Statewide",
    description="Free confidential 24/7 treatment referral and information service for individuals and families facing mental health or substance use disorders. Provides referrals to local treatment facilities and community organizations in Michigan and nationwide. Spanish-language support available through trained specialists.",
    description_es="Servicio gratuito y confidencial 24/7 de referencia e información para personas y familias con trastornos de salud mental o uso de sustancias. Proporciona referencias a centros de tratamiento locales en Michigan y a nivel nacional. Soporte en español disponible.",
    address="", city="", phone="800-662-4357", email="", website="https://www.samhsa.gov/find-help/national-helpline",
    eligibility="Open to anyone in the United States seeking substance use or mental health treatment information and referrals.",
    eligibility_es="Abierto a cualquier persona en Estados Unidos que busque información y referencias de tratamiento.",
    notes="TTY 800-487-4889; also use FindTreatment.gov to search Michigan providers online.",
    notes_es="TTY 800-487-4889; también use FindTreatment.gov para buscar proveedores en Michigan.",
    hours="Available 24/7",
    tags="statewide|hotline|substance-use|treatment-referral|national",
    services="Treatment referrals|Substance use information|Mental health resource navigation",
    county="", served_counties="", coverage="statewide",
    _source="https://www.samhsa.gov/find-help/national-helpline", _source_type="government", _confidence="high",
)
add(
    name="FindTreatment.gov — Michigan Provider Search",
    category="substance-use-treatment", region="Statewide",
    description="Official SAMHSA online locator for substance use and mental health treatment facilities serving Michigan. Users search by location, treatment type, and payment options to find licensed providers with current openings. Facility admission requirements vary; justice-involved individuals should confirm criminal-record policies with each provider.",
    description_es="Localizador oficial en línea de SAMHSA para centros de tratamiento de sustancias y salud mental que sirven a Michigan. Los usuarios buscan por ubicación, tipo de tratamiento y opciones de pago. Los requisitos de admisión varían; las personas con antecedentes penales deben confirmar políticas con cada proveedor.",
    address="", city="", phone="833-888-1553", email="FindTreatment@samhsa.hhs.gov",
    website="https://findtreatment.gov",
    eligibility="Open to anyone seeking treatment; facility admission requirements vary by provider.",
    eligibility_es="Abierto a cualquier persona que busque tratamiento; los requisitos de admisión varían según el proveedor.",
    notes="SAMHSA helpline 800-662-4357 also routes to treatment help; facility data updated weekly.",
    notes_es="La línea SAMHSA 800-662-4357 también conecta con ayuda de tratamiento.",
    hours="Online 24/7; BHSIS support Mon–Fri 8 a.m.–6 p.m. ET",
    tags="statewide|substance-use|online|treatment-referral",
    services="Treatment facility search|Provider availability information|Mental health provider locator",
    county="", served_counties="", coverage="statewide",
    _source="https://findtreatment.gov", _source_type="government", _confidence="high",
)
add(
    name="MDOC — Parole Board",
    category="probation-parole", region="Statewide",
    description="Michigan Parole Board serving as the sole paroling authority for persons committed to MDOC jurisdiction. The board reviews parole eligibility, sets release conditions, and coordinates with In-Reach staff for transition planning. Contact for parole status inquiries through institutional or field parole agents—not a general reentry resource hotline.",
    description_es="Junta de Libertad Condicional de Michigan como única autoridad de libertad condicional para personas bajo jurisdicción del MDOC. La junta revisa elegibilidad, establece condiciones de liberación y coordina con personal In-Reach para planificación de transición. Contacte a agentes institucionales o de campo, no es una línea general de recursos de reinserción.",
    address="400 South Walnut Street", city="Lansing", phone="517-373-0270",
    email="", website="https://www.michigan.gov/corrections/parole-probation/parole-board",
    eligibility="Persons under MDOC jurisdiction and their authorized representatives seeking parole status information.",
    eligibility_es="Personas bajo jurisdicción del MDOC y sus representantes autorizados que buscan información de estado de libertad condicional.",
    notes="Parole decisions communicated through institutional parole agents; see michigan.gov/corrections parole board page for public meeting information.",
    notes_es="Decisiones de libertad condicional comunicadas a través de agentes institucionales; consulte la página de la junta en michigan.gov/corrections.",
    hours="Monday–Friday business hours",
    tags="statewide|parole|DOC|Parole-Board",
    services="Parole eligibility review|Release condition setting|In-Reach coordination|Parole status information",
    county="Ingham", served_counties="", coverage="statewide",
    _source="https://www.michigan.gov/corrections/parole-probation/parole-board", _source_type="government", _confidence="high",
)
add(
    name="MDOC — Field Operations Administration",
    category="probation-parole", region="Statewide",
    description="State agency responsible for parole and probation supervision across 10 regions in Michigan's Metropolitan and Outstate territories. Parole and probation agents connect supervisees to Offender Success services, treatment providers, and community partners. Contact for reporting requirements and regional office locations—not a general resource navigation hotline.",
    description_es="Agencia estatal responsable de la supervisión de libertad condicional y probatoria en 10 regiones de los territorios Metropolitano y del Interior del estado. Los agentes conectan a supervisados con servicios Offender Success y aliados comunitarios. Contacte para requisitos de reporte y ubicaciones de oficinas regionales.",
    address="400 South Walnut Street", city="Lansing", phone="517-373-0270",
    email="", website="https://www.michigan.gov/corrections/parole-probation",
    eligibility="Individuals under Michigan parole or probation supervision; family members may contact for general district information.",
    eligibility_es="Personas bajo supervisión de libertad condicional o probatoria de Michigan; familiares pueden contactar para información del distrito.",
    notes="See michigan.gov/corrections parole-probation office directory for Regions 1–10 phones and addresses.",
    notes_es="Consulte el directorio de oficinas en michigan.gov/corrections para teléfonos y direcciones de las Regiones 1–10.",
    hours="Regional offices Monday–Friday business hours",
    tags="statewide|parole|probation|DOC|supervision",
    services="Parole and probation supervision|Regional office coordination|Offender Success referrals|Supervision compliance support",
    county="Ingham", served_counties="", coverage="statewide",
    _source="https://www.michigan.gov/corrections/parole-probation", _source_type="government", _confidence="high",
)
add(
    name="Michigan Secretary of State — Driver & State ID Services",
    category="id-documentation", region="Statewide",
    description="State agency providing REAL ID–compliant driver's licenses, state identification cards, and reinstatement services at branch offices across Michigan. Reentry partners and MDOC assist returning citizens with documentation needed for employment and MI Bridges benefits. Online services available at michigan.gov/sos.",
    description_es="Agencia estatal que proporciona licencias de conducir compatibles con REAL ID, tarjetas de identificación estatal y servicios de restablecimiento en oficinas en todo Michigan. Los aliados de reinserción y el MDOC ayudan a ciudadanos que regresan con documentación necesaria para empleo y beneficios MI Bridges.",
    address="", city="Lansing", phone="888-SOS-MICH",
    email="", website="https://www.michigan.gov/sos",
    eligibility="Michigan residents seeking credentials or reinstatement; specific document requirements apply for ID issuance after incarceration.",
    eligibility_es="Residentes de Michigan que buscan credenciales o restablecimiento; aplican requisitos específicos de documentos para emisión de identificación.",
    notes="Call 888-SOS-MICH (888-767-6424) or schedule at michigan.gov/sos branch locator; MDOC Reentry Services assists with vital records.",
    notes_es="Llame al 888-SOS-MICH o programe cita en el localizador de michigan.gov/sos; Servicios de Reinserción del MDOC ayudan con registros vitales.",
    hours="Branch hours vary by location",
    tags="statewide|id-documentation|drivers-license|REAL-ID|online",
    services="State ID issuance|Driver's license services|Reinstatement fee payment|Branch office locator|Online appointment scheduling",
    county="Ingham", served_counties="", coverage="statewide",
    _source="https://www.michigan.gov/sos", _source_type="government", _confidence="high",
)
add(
    name="MiTalent.org — Michigan Works! Statewide",
    category="employment", region="Statewide",
    description="Statewide workforce portal connecting job seekers—including justice-involved Michiganders—to Michigan Works! career coaching, job postings, training referrals, and American Job Center locations in every prosperity region. Offender Success employment partners coordinate through regional Michigan Works! agencies. Core services free for job seekers.",
    description_es="Portal estatal de fuerza laboral que conecta a buscadores de empleo—incluidas personas con antecedentes penales en Michigan—a coaching de carrera Michigan Works!, ofertas de empleo, referencias de capacitación y ubicaciones de centros en cada región de prosperidad. Aliados de empleo Offender Success coordinan a través de agencias regionales.",
    address="", city="Lansing", phone="517-335-5858",
    email="", website="https://www.mitalent.org",
    eligibility="Michigan residents seeking employment or training; no criminal-record restrictions stated for core Michigan Works! services.",
    eligibility_es="Residentes de Michigan que buscan empleo o capacitación; sin restricciones de antecedentes indicadas para servicios básicos de Michigan Works!.",
    notes="Register at mitalent.org; locate nearest Michigan Works! service center by county; Offender Success regions listed at michigan.gov/corrections OSA page.",
    notes_es="Regístrese en mitalent.org; localice el centro Michigan Works! más cercano por condado; regiones Offender Success en michigan.gov/corrections OSA.",
    hours="Online 24/7; service center hours vary",
    tags="statewide|employment|Michigan-Works|MiTalent|AJC|Offender-Success",
    services="Job search assistance|Skills training referrals|Resume workshops|Michigan Works! center locator|Fair-chance employment navigation",
    county="", served_counties="", coverage="statewide",
    _source="https://www.mitalent.org", _source_type="government", _confidence="high",
)
add(
    name="Calvin University — MDOC Returning Citizen Resource Map",
    category="reentry-organizations", region="Statewide",
    description="Interactive statewide map developed by Calvin University in partnership with MDOC aggregating reentry services including housing, employment, food, legal aid, counseling, transportation, and peer support by county. Used by parole officers, families, and returning citizens to locate verified community providers across Michigan.",
    description_es="Mapa interactivo estatal desarrollado por Calvin University en asociación con el MDOC que agrega servicios de reinserción incluyendo vivienda, empleo, alimentos, asistencia legal, consejería, transporte y apoyo entre pares por condado. Usado por oficiales de libertad condicional, familias y ciudadanos que regresan.",
    address="", city="Grand Rapids", phone="",
    email="", website="https://calvin.maps.arcgis.com/apps/webappviewer/index.html?id=70f61d915bdf47dea727b8123b483bbd",
    eligibility="Open to anyone seeking Michigan reentry resource information; provider listings vary by county coverage.",
    eligibility_es="Abierto a cualquier persona que busque información de recursos de reinserción en Michigan; los listados varían según cobertura del condado.",
    notes="Also accessible at gis.calvin.edu/rc; categories include housing, employment, legal, counseling, and transportation; expanded county coverage ongoing.",
    notes_es="También accesible en gis.calvin.edu/rc; categorías incluyen vivienda, empleo, legal, consejería y transporte; cobertura de condados en expansión.",
    hours="Online 24/7",
    tags="statewide|reentry|online|resource-map|referral-only",
    services="Interactive reentry service map|County provider listings|Housing and employment locator|Legal aid finder|Transportation resources",
    county="Kent", served_counties="", coverage="statewide",
    _source="https://calvin.edu/prison-initiative/resources/", _source_type="nonprofit", _confidence="high",
)
add(
    name="Michigan Veterans Affairs Agency — Statewide Hotline",
    category="veterans", region="Statewide",
    description="State agency connecting Michigan veterans and their families to federal VA benefits, state veteran benefits, employment resources, and county veteran service officers. MVAA navigators assist justice-involved veterans with discharge upgrades, VA healthcare enrollment, and housing referrals. Call 800-MICH-VET for benefits navigation.",
    description_es="Agencia estatal que conecta a veteranos de Michigan y sus familias con beneficios federales de la VA, beneficios estatales, recursos de empleo y oficiales de servicios para veteranos del condado. Los navegadores MVAA ayudan a veteranos con antecedentes penales. Llame al 800-MICH-VET.",
    address="611 West Ottawa Street", city="Lansing", phone="800-MICH-VET",
    email="MichiganVeterans@michigan.gov", website="https://www.michigan.gov/veterans",
    eligibility="Michigan veterans, active-duty service members, and eligible family members; no criminal-record restrictions for benefits navigation.",
    eligibility_es="Veteranos de Michigan, miembros en servicio activo y familiares elegibles; sin restricciones de antecedentes penales para navegación de beneficios.",
    notes="Call 800-MICH-VET (800-642-4838); county veteran service offices listed at michigan.gov/veterans.",
    notes_es="Llame al 800-MICH-VET (800-642-4838); oficinas de servicios para veteranos del condado en michigan.gov/veterans.",
    hours="Hotline Mon–Fri business hours",
    tags="statewide|veterans|hotline|VA-benefits|reentry",
    services="VA benefits navigation|State veteran benefits|County VSO referrals|Employment resources|Healthcare enrollment assistance",
    county="Ingham", served_counties="", coverage="statewide",
    _source="https://www.michigan.gov/veterans", _source_type="government", _confidence="high",
)
add(
    name="Michigan Reentry Community Resource Map",
    category="reentry-organizations", region="Statewide",
    description="MDOC-referenced online reentry resource directory and map connecting returning citizens to community-based housing, employment, treatment, and legal services across Michigan counties. Complements Calvin University GIS mapping and 211 referrals for parole agents and supervisees seeking local providers.",
    description_es="Directorio y mapa en línea de recursos de reinserción referenciado por el MDOC que conecta a ciudadanos que regresan con servicios comunitarios de vivienda, empleo, tratamiento y legales en condados de Michigan. Complementa el mapeo GIS de Calvin University y referencias del 211.",
    address="", city="Lansing", phone="211", email="",
    website="http://gis.calvin.edu/rc",
    eligibility="Justice-involved Michigan residents and community partners seeking local reentry provider listings.",
    eligibility_es="Residentes de Michigan con antecedentes penales y aliados comunitarios que buscan listados de proveedores locales de reinserción.",
    notes="Listed on michigan.gov/corrections OSA reentry services page; also dial 211 for live navigator assistance; ArcGIS version at calvin.maps.arcgis.com.",
    notes_es="Listado en la página de servicios de reinserción OSA de michigan.gov/corrections; también marque 211 para asistencia de navegador; versión ArcGIS en calvin.maps.arcgis.com.",
    hours="Online 24/7; 211 navigators available 24/7",
    tags="statewide|reentry|online|resource-map|211|referral-only",
    services="Reentry provider directory|County service map|Housing and employment locator|Treatment provider finder|Legal aid routing",
    county="", served_counties="", coverage="statewide",
    _source="https://www.michigan.gov/corrections/our-operations/osa/reentry-services", _source_type="government", _confidence="high",
)
add(
    name="MDOC — In-Reach Transition Planning",
    category="state-agency", region="Statewide",
    description="MDOC In-Reach program linking incarcerated individuals designated by the Parole Board to intensive pre-release transition planning including housing arrangements, case plan finalization, and virtual transition team meetings with community parole agents and Offender Success partners. In-Reach facilities serve as statewide reentry preparation sites.",
    description_es="Programa In-Reach del MDOC que vincula a personas encarceladas designadas por la Junta de Libertad Condicional a planificación intensiva de transición previa a la liberación incluyendo arreglos de vivienda, finalización del plan de casos y reuniones virtuales del equipo de transición con agentes comunitarios y aliados Offender Success.",
    address="400 South Walnut Street", city="Lansing", phone="517-241-0456",
    email="", website="https://www.michigan.gov/corrections/our-operations/osa/in-reach",
    eligibility="MDOC prisoners designated by Parole Board for In-Reach services based on risks, needs, and housing requirements.",
    eligibility_es="Prisioneros del MDOC designados por la Junta de Libertad Condicional para servicios In-Reach según riesgos, necesidades y requisitos de vivienda.",
    notes="In-Reach sites include Parnall, Handlon, and other designated facilities; transition team meetings connect returning citizens to community agents before release.",
    notes_es="Los sitios In-Reach incluyen Parnall, Handlon y otras instalaciones designadas; las reuniones del equipo de transición conectan antes de la liberación.",
    hours="Facility programming during incarceration; community coordination pre-release",
    tags="statewide|reentry|DOC|In-Reach|pre-release",
    services="Pre-release transition planning|Housing placement coordination|Transition team meetings|Case plan finalization|Community agent linkage",
    county="Ingham", served_counties="", coverage="statewide",
    _source="https://www.michigan.gov/corrections/our-operations/osa/in-reach", _source_type="government", _confidence="high",
)
add(
    name="MDOC — Employment & Opportunities Unit",
    category="employment", region="Statewide",
    description="MDOC unit connecting job-ready parolees and probationers under MDOC jurisdiction to employer partnerships, training schools, and regional job fairs statewide. Coordinates with Offender Success Administrative Agencies and Michigan Works! to reduce employment barriers. Individuals not under MDOC jurisdiction should use local Michigan Works! instead.",
    description_es="Unidad del MDOC que conecta a personas en libertad condicional y probatoria bajo jurisdicción del MDOC listas para empleo con aliados empleadores, escuelas de capacitación y ferias de empleo estatales. Coordina con agencias administrativas Offender Success y Michigan Works!. Personas fuera de jurisdicción del MDOC deben usar Michigan Works! local.",
    address="400 South Walnut Street", city="Lansing", phone="517-241-0456",
    email="", website="https://www.michigan.gov/corrections/our-operations/osa/employment-and-opportunities-unit",
    eligibility="Parolees and probationers currently under MDOC jurisdiction; employer partners seeking justice-involved candidates.",
    eligibility_es="Personas en libertad condicional y probatoria bajo jurisdicción actual del MDOC; aliados empleadores que buscan candidatos con antecedentes penales.",
    notes="Employers may access Fidelity Bonding and Work Opportunity Tax Credit via michigan.gov/leo; job fairs held throughout the year by region.",
    notes_es="Los empleadores pueden acceder a Fidelity Bonding y Work Opportunity Tax Credit vía michigan.gov/leo; ferias de empleo durante el año por región.",
    hours="Monday–Friday business hours; job fair dates vary",
    tags="statewide|employment|DOC|fair-chance|job-fairs",
    services="Employer partnership coordination|Regional job fairs|Training school referrals|Fidelity bonding information|WOTC tax credit navigation",
    county="Ingham", served_counties="", coverage="statewide",
    _source="https://www.michigan.gov/corrections/our-operations/osa/employment-and-opportunities-unit", _source_type="government", _confidence="high",
)

# --- Phase 2: OSA admin agencies, facilities, field offices (~25 rows) ---
OSA_AGENCIES = [
    dict(name="Health Management Systems of America — MDOC Offender Success Region 10",
         region="Metro Detroit / Wayne, Oakland & Macomb", phone="248-827-4111",
         address="28411 Northwestern Highway", city="Southfield", county="Oakland",
         served="Macomb|Oakland|Wayne", website="https://www.hmsanet.com",
         notes="MDOC-contracted Offender Success Administrative Agency for Region 10 providing residential stability, employment readiness, and behavioral health subcontractor coordination in metro Detroit."),
    dict(name="Michigan Works! West Central — Offender Success Region 4",
         region="West Michigan — 13 counties", phone="231-796-4891",
         address="8479 South US-131", city="Big Rapids", county="Mecosta",
         served="Allegan|Barry|Ionia|Kent|Lake|Mason|Mecosta|Montcalm|Muskegon|Newaygo|Oceana|Osceola|Ottawa",
         website="https://www.mwwc.org/offender-success",
         notes="MDOC Offender Success Administrative Agency for Region 4; see mwwc.org/offender-success for community coordinator contacts."),
    dict(name="Kinexus — Michigan Works! Southwest Offender Success Region 8",
         region="Southwest Michigan — 7 counties", phone="269-385-0422",
         address="160 West Michigan Avenue", city="Kalamazoo", county="Kalamazoo",
         served="Berrien|Branch|Calhoun|Cass|Kalamazoo|St. Joseph|Van Buren",
         website="https://www.miworks.org/offender-success",
         notes="Kinexus operates Region 8 Offender Success covering seven southwest Michigan counties; contact DeamudJ@kinexus.org for employer partnerships."),
    dict(name="Michigan Works! — Upper Peninsula Prosperity Alliance (OSAA Region 1)",
         region="Upper Peninsula", phone="906-228-3075",
         address="1498 O'Dovero Drive", city="Marquette", county="Marquette",
         served="Alger|Baraga|Chippewa|Delta|Dickinson|Gogebic|Houghton|Iron|Keweenaw|Luce|Mackinac|Marquette|Menominee|Ontonagon|Schoolcraft",
         website="https://www.upmichiganworks.org",
         notes="Offender Success Administrative Agency serving all 15 UP counties; coordinates reentry employment and community supports with MDOC Region 1."),
    dict(name="Networks Northwest — Michigan Works! (OSAA Region 2)",
         region="Northwest Lower Michigan", phone="231-922-3700",
         address="600 East Front Street", city="Traverse City", county="Grand Traverse",
         served="Antrim|Benzie|Charlevoix|Emmet|Grand Traverse|Kalkaska|Leelanau|Manistee|Missaukee|Wexford",
         website="https://www.networksnorthwest.org/michigan-works",
         notes="Offender Success Administrative Agency for northwest Lower Michigan MDOC Region 2 counties."),
    dict(name="Michigan Works! Northeast Consortium (OSAA Region 3)",
         region="Northeast Lower Michigan", phone="989-356-6600",
         address="3680 North US-23", city="Alpena", county="Alpena",
         served="Alcona|Alpena|Cheboygan|Crawford|Iosco|Montmorency|Ogemaw|Oscoda|Otsego|Presque Isle|Roscommon",
         website="https://www.michiganworks.org",
         notes="Offender Success Administrative Agency for northeast Michigan MDOC Region 3."),
    dict(name="Michigan Works! Great Lakes Bay (OSAA Region 5)",
         region="Great Lakes Bay", phone="989-754-6464",
         address="312 East Genesee Avenue", city="Saginaw", county="Saginaw",
         served="Arenac|Bay|Clare|Gladwin|Gratiot|Isabella|Midland|Saginaw",
         website="https://www.michiganworks.org",
         notes="Offender Success Administrative Agency for Great Lakes Bay MDOC Region 5."),
    dict(name="Michigan Works! East Michigan (OSAA Region 6)",
         region="East Central Michigan", phone="810-233-5611",
         address="711 North Saginaw Street", city="Flint", county="Genesee",
         served="Genesee|Huron|Lapeer|Sanilac|Shiawassee|St. Clair|Tuscola",
         website="https://www.michiganworks.org",
         notes="Offender Success Administrative Agency for east central Michigan including Genesee and St. Clair counties."),
    dict(name="Capital Area Michigan Works! (OSAA Region 7)",
         region="Lansing / Clinton, Eaton & Ingham", phone="517-492-5500",
         address="2110 South Cedar Street", city="Lansing", county="Ingham",
         served="Clinton|Eaton|Ingham",
         website="https://www.camw.org",
         notes="Offender Success Administrative Agency for Lansing-area MDOC Region 7."),
    dict(name="Michigan Works! Southeast (OSAA Region 9)",
         region="Southeast Michigan", phone="734-973-8420",
         address="3170 Lohr Road", city="Ann Arbor", county="Washtenaw",
         served="Hillsdale|Jackson|Lenawee|Livingston|Monroe|Washtenaw",
         website="https://www.michiganworks.org",
         notes="Offender Success Administrative Agency for southeast Michigan excluding Wayne/Oakland/Macomb (Region 10)."),
    dict(name="Detroit Employment Solutions Corporation — Offender Success Partner",
         region="Detroit / Wayne County", phone="313-962-9675",
         address="9301 Michigan Avenue", city="Detroit", county="Wayne",
         served="Wayne", website="https://descmiworks.org",
         notes="City of Detroit Michigan Works! agency partnering with HMSA Offender Success for Detroit at Work career centers and fair-chance employment in Wayne County."),
]

for o in OSA_AGENCIES:
    cov = "single" if "|" not in o["served"] else "multi"
    county_count = len(o["served"].split("|"))
    desc_en = (
        f"MDOC-contracted Offender Success Administrative Agency serving {county_count} Michigan counties with "
        "residential stability, employment readiness, job development, behavioral health coordination, and social "
        "supports for eligible parolees and probationers. Parole agents refer supervisees; community coordinators "
        "connect participants to subcontracted housing, treatment, and employment partners. Not a walk-in crisis provider."
    )
    desc_es = (
        f"Agencia Administrativa Offender Success contratada por el MDOC que sirve {county_count} condados de Michigan con "
        "estabilidad residencial, preparación laboral, desarrollo de empleo, coordinación de salud conductual y apoyos "
        "sociales para personas elegibles en libertad condicional y probatoria. Los agentes refieren supervisados; "
        "los coordinadores comunitarios conectan con aliados de vivienda, tratamiento y empleo. No es un proveedor de crisis."
    )
    add(
        name=o["name"], category="reentry-organizations", region=o["region"],
        description=desc_en, description_es=desc_es,
        address=o["address"], city=o["city"], phone=o["phone"], email="",
        website=o["website"],
        eligibility="Eligible MDOC parolees and SAI probationers referred by parole agents; services vary by county and authorization.",
        eligibility_es="Personas elegibles en libertad condicional del MDOC y libertad probatoria SAI referidas por agentes; los servicios varían según condado.",
        notes=o["notes"],
        notes_es=o["notes"],
        hours="Monday–Friday business hours",
        tags="Offender-Success|OSAA|reentry|MDOC|referral-only",
        services="Residential stability coordination|Employment readiness|Job development|Behavioral health referrals|Social supports",
        county=o["county"], served_counties=o["served"], coverage=cov,
        _source=o["website"], _source_type="government", _confidence="high",
    )

FACILITIES = [
    dict(name="Parnall Correctional Facility — Vocational Village & In-Reach",
         region="Jackson / Jackson County", phone="517-780-6004",
         address="1780 East Parnall Road", city="Jackson", county="Jackson",
         desc="Minimum-security MDOC facility serving as statewide In-Reach site with Vocational Village skilled trades training in auto mechanics, carpentry, CDL, CNC/robotics, masonry, and diesel mechanics for prisoners within 24 months of release."),
    dict(name="Richard A. Handlon Correctional Facility — Vocational Village",
         region="Ionia / Ionia County", phone="616-527-2800",
         address="1728 Bluewater Highway", city="Ionia", county="Ionia",
         desc="Medium-security MDOC facility hosting Michigan's first Vocational Village with immersive skilled trades training, employment readiness, and pre-release certification programs for prisoners preparing for community reintegration."),
    dict(name="Cooper Street Correctional Facility",
         region="Jackson / Jackson County", phone="517-780-5600",
         address="3100 Cooper Street", city="Jackson", county="Jackson",
         desc="MDOC minimum-security facility in Jackson providing education, GED programming, and reentry preparation for adult male prisoners paroling to Michigan communities including In-Reach transition coordination."),
    dict(name="Lakeland Correctional Facility",
         region="Coldwater / Branch County", phone="517-279-5000",
         address="141 First Street", city="Coldwater", county="Branch",
         desc="MDOC facility in Coldwater providing education, programming, and pre-release preparation for prisoners including reentry planning coordination with southwest Michigan Offender Success Region 8 partners."),
    dict(name="Macomb Correctional Facility",
         region="Lenox Township / Macomb County", phone="586-749-4900",
         address="34625 26 Mile Road", city="Lenox Township", county="Macomb",
         desc="MDOC facility in Macomb County providing education, vocational programming, and institutional parole agent coordination for prisoners releasing to metro Detroit Offender Success Region 10 through HMSA."),
    dict(name="G. Robert Cotton Correctional Facility",
         region="Jackson / Jackson County", phone="517-780-5600",
         address="3500 N. Elm Road", city="Jackson", county="Jackson",
         desc="MDOC facility offering education, cognitive programming, and reentry preparation with institutional parole agents coordinating transition to Jackson-area and statewide community supervision offices."),
]

for f in FACILITIES:
    desc_es = (
        f"Instalación del MDOC que ofrece educación, programación vocacional y preparación para reinserción "
        f"con agentes de libertad condicional institucional coordinando la transición a supervisión comunitaria. "
        f"{f['desc'].split('.')[0]}."
    )
    add(
        name=f["name"], category="state-agency", region=f["region"],
        description=f["desc"] + " Institutional parole agents coordinate release planning with community Field Operations and Offender Success partners—not a community walk-in reentry center.",
        description_es=desc_es + " Los agentes institucionales coordinan la planificación de liberación con Operaciones de Campo y aliados Offender Success, no es un centro comunitario de reinserción.",
        address=f["address"], city=f["city"], phone=f["phone"], email="",
        website="https://www.michigan.gov/corrections/prisons",
        eligibility="Persons committed to MDOC custody at this facility; community reentry services accessed through parole agents after release.",
        eligibility_es="Personas bajo custodia del MDOC en esta instalación; servicios comunitarios de reinserción accedidos a través de agentes después de la liberación.",
        notes="See michigan.gov/corrections/prisons for visiting and programming information; Vocational Village eligibility requires application and misconduct-free status.",
        notes_es="Consulte michigan.gov/corrections/prisons para información de visitas y programación; elegibilidad Vocational Village requiere solicitud y estado sin faltas.",
        hours="Facility operations daily; programming during incarceration",
        tags=f"{f['county'].lower()}|MDOC|facility|reentry|vocational",
        services="In-facility education|Vocational training|In-Reach transition planning|Institutional parole coordination|Pre-release programming",
        county=f["county"], served_counties=f["county"], coverage="single",
        _source="https://www.michigan.gov/corrections/prisons", _source_type="government", _confidence="high",
    )

FIELD_OFFICES = [
    dict(name="MDOC Field Operations — Region 10 Detroit Metro Parole",
         region="Detroit / Wayne County", phone="313-456-1000",
         address="3048 West Grand Boulevard, Suite 4-400", city="Detroit", county="Wayne", served="Wayne",
         notes="Region 10 West District supervising Wayne County parolees; co-located with Metropolitan Territory administration."),
    dict(name="MDOC Field Operations — Region 10 Pontiac Parole",
         region="Pontiac / Oakland County", phone="248-253-2440",
         address="235 North Saginaw Street, Suite 100", city="Pontiac", county="Oakland",
         served="Oakland|Macomb",
         notes="Region 10 Northwest District; Northwest Operations Office at 1200 N. Telegraph Road Building 26."),
    dict(name="MDOC Field Operations — Region 9 Jackson Parole",
         region="Jackson / Jackson County", phone="517-780-6270",
         address="106 West Michigan Avenue", city="Jackson", county="Jackson",
         served="Jackson|Hillsdale|Lenawee|Livingston|Monroe|Washtenaw",
         notes="Metropolitan Territory Region 9 serving south-central Michigan counties outside Wayne/Oakland/Macomb core."),
    dict(name="MDOC Field Operations — Region 4 Grand Rapids",
         region="Grand Rapids / Kent County", phone="616-356-0700",
         address="678 Front Avenue NW", city="Grand Rapids", county="Kent", served="Kent",
         notes="Outstate Region 4 hub for West Michigan parole and probation supervision."),
    dict(name="MDOC Field Operations — Region 7 Lansing",
         region="Lansing / Ingham County", phone="517-373-5060",
         address="5303 South Cedar Street", city="Lansing", county="Ingham",
         served="Clinton|Eaton|Ingham",
         notes="Region 7 office serving Lansing-area supervisees; coordinates with Capital Area Michigan Works! Offender Success."),
    dict(name="MDOC Field Operations — Region 6 Flint",
         region="Flint / Genesee County", phone="810-760-7200",
         address="711 North Saginaw Street", city="Flint", county="Genesee", served="Genesee",
         notes="Region 6 office co-located with Michigan Works! East Michigan; serves Genesee and surrounding east-central counties."),
    dict(name="MDOC Field Operations — Region 8 Kalamazoo",
         region="Kalamazoo / Kalamazoo County", phone="269-337-4400",
         address="1500 Alcott Street", city="Kalamazoo", county="Kalamazoo", served="Kalamazoo",
         notes="Region 8 office coordinating with Kinexus Offender Success for southwest Michigan supervisees."),
]

for fo in FIELD_OFFICES:
    sc = fo["served"]
    cov = "single" if "|" not in sc else "multi"
    counties_label = sc.replace("|", ", ")
    desc_en = (
        f"MDOC Field Operations parole and probation office supervising community corrections in {counties_label}. "
        "Agents connect supervisees to Offender Success Administrative Agencies, treatment providers, and Michigan Works! "
        "partners. Contact for reporting requirements—not emergency services."
    )
    desc_es = (
        f"Oficina de Operaciones de Campo del MDOC que supervisa correcciones comunitarias en {counties_label}. "
        "Los agentes conectan supervisados con agencias Offender Success, proveedores de tratamiento y aliados Michigan Works!. "
        "Contacte para requisitos de reporte, no servicios de emergencia."
    )
    add(
        name=fo["name"], category="probation-parole", region=fo["region"],
        description=desc_en, description_es=desc_es,
        address=fo["address"], city=fo["city"], phone=fo["phone"], email="",
        website="https://www.michigan.gov/corrections/parole-probation/office-directory",
        eligibility="Individuals under Michigan parole or probation supervision in served counties.",
        eligibility_es="Personas bajo supervisión de libertad condicional o probatoria de Michigan en los condados servidos.",
        notes=fo["notes"],
        notes_es=fo["notes"],
        hours="Monday–Friday business hours",
        tags=f"parole|probation|{fo['county'].lower()}|MDOC|supervision",
        services="Parole and probation supervision|Offender Success referrals|Reporting compliance|Treatment coordination|Workforce partner connections",
        county=fo["county"], served_counties=sc, coverage=cov,
        _source="https://www.michigan.gov/corrections/parole-probation/office-directory", _source_type="government", _confidence="high",
    )

# --- Phase 3: Category minimum direct-service programs (~15 rows) ---
PHASE3 = [
    dict(name="Forgotten Harvest", category="food-nutrition", region="Southeast Michigan",
         phone="248-967-1500", website="https://www.forgottenharvest.org",
         address="21800 Greenfield Road", city="Oak Park", county="Oakland",
         cov="multi", served="Wayne|Oakland|Macomb",
         desc="Southeast Michigan food rescue organization distributing surplus food to partner pantries and mobile distributions across Wayne, Oakland, and Macomb counties for low-income residents including returning citizens."),
    dict(name="GTC Michigan — Federally Qualified Health Center Network", category="healthcare", region="Southeast Michigan",
         phone="313-871-2000", website="https://www.gtcmichigan.org",
         address="4201 Saint Antoine Street", city="Detroit", county="Wayne",
         cov="multi", served="Wayne|Macomb",
         desc="Federally qualified health center network providing primary care, behavioral health, dental, and pharmacy services on sliding fee scale for underserved southeast Michigan residents including justice-involved patients reestablishing medical care."),
    dict(name="Michigan Problem Gambling Helpline", category="healthcare", region="Statewide",
         phone="800-270-7117", website="https://www.michigan.gov/mdhhs/assistance-programs/gambling",
         address="", city="Lansing", county="Ingham", cov="statewide", served="",
         desc="State-supported confidential helpline providing problem gambling referrals, counseling navigation, and self-exclusion information for Michigan residents including returning citizens facing gambling-related reentry barriers."),
    dict(name="MDHHS — Recovery Help Line", category="substance-use-treatment", region="Statewide",
         phone="800-662-4357", website="https://www.michigan.gov/mdhhs/assistance-programs/behavioral-health/substance-use-disorder",
         address="", city="Lansing", county="Ingham", cov="statewide", served="",
         desc="MDHHS-coordinated substance use disorder treatment navigation connecting Michigan residents to Medicaid-covered treatment, recovery supports, and regional PIHP providers including justice-involved individuals after release."),
    dict(name="Food Bank Council of Michigan", category="food-nutrition", region="Statewide",
         phone="517-485-1202", website="https://www.fbcmich.org",
         address="330 Marshall Street", city="Lansing", county="Ingham", cov="statewide", served="",
         desc="Statewide association connecting Michigan residents to seven regional food bank networks and partner pantries by county including resources for returning citizens seeking emergency food assistance."),
    dict(name="Focus: HOPE — Workforce & Basic Needs", category="employment", region="Detroit / Wayne County",
         phone="313-494-5500", website="https://www.focushope.edu",
         address="1355 Oakman Boulevard", city="Detroit", county="Wayne", cov="single", served="Wayne",
         desc="Detroit nonprofit providing workforce training, food distribution, and senior services for low-income Wayne County residents including returning citizens in metro Detroit employment programs."),
    dict(name="Community Action Agency — Michigan State Association", category="basic-needs", region="Statewide",
         phone="517-393-4644", website="https://www.mica-michigan.org",
         address="721 North Capitol Avenue", city="Lansing", county="Ingham", cov="statewide", served="",
         desc="Statewide network locator connecting low-income Michigan residents to local Community Action Agencies offering utility assistance, weatherization, emergency aid, and case management in all 83 counties."),
    dict(name="Michigan Coalition Against Homelessness", category="housing", region="Statewide",
         phone="517-482-5555", website="https://www.mihomeless.org",
         address="3030 South State Street", city="Ann Arbor", county="Washtenaw", cov="statewide", served="",
         desc="Statewide advocacy and resource hub connecting Michiganders experiencing homelessness to Coordinated Entry systems, shelter directories, and housing navigation by county including justice-involved individuals."),
    dict(name="Michigan Warmline", category="healthcare", region="Statewide",
         phone="888-733-7753", website="https://www.michigan.gov/mdhhs/assistance-programs/behavioral-health",
         address="", city="", county="", cov="statewide", served="",
         desc="Peer-operated warmline providing non-crisis emotional support and mental health resource navigation for Michigan residents including returning citizens seeking connection before crisis escalation. For crisis call 988."),
    dict(name="Habitat for Humanity Michigan", category="housing", region="Statewide",
         phone="517-485-5866", website="https://www.habitatmichigan.org",
         address="12163 South I-69 Highway", city="Potterville", county="Eaton", cov="statewide", served="",
         desc="Statewide Habitat affiliate locator connecting low-income Michigan families including returning citizens to affordable homeownership and repair programs through local Habitat chapters in communities statewide."),
    dict(name="InterCare Community Health Network", category="healthcare", region="Southwest Michigan",
         phone="269-429-7100", website="https://www.intercare.org",
         address="620 Pipestone Street", city="Benton Harbor", county="Berrien", cov="multi",
         served="Berrien|Cass|Van Buren",
         desc="Federally qualified health center serving southwest Michigan with primary care, behavioral health, and dental services on sliding fee scale for uninsured and Medicaid patients including reentry populations."),
    dict(name="Detroit at Work — American Job Center", category="employment", region="Detroit / Wayne County",
         phone="313-962-9675", website="https://detroitatwork.com",
         address="9301 Michigan Avenue", city="Detroit", county="Wayne", cov="single", served="Wayne",
         desc="Detroit American Job Center operated by Detroit Employment Solutions connecting Wayne County job seekers including justice-involved residents to training, career coaching, and employer partnerships through Michigan Works!."),
    dict(name="Michigan Department of Education — Adult Education Locator", category="education", region="Statewide",
         phone="517-335-5858", website="https://www.michigan.gov/leo/bureau-services/michigan-adult-education",
         address="", city="Lansing", county="Ingham", cov="statewide", served="",
         desc="State directory connecting Michigan adults including returning citizens to local GED, high school equivalency, and adult basic education programs at community sites in every county."),
    dict(name="Michigan Housing Locator", category="housing", region="Statewide",
         phone="877-428-8844", website="https://www.michiganhousinglocator.org",
         address="", city="", county="", cov="statewide", served="",
         desc="Statewide affordable rental housing search tool listing income-restricted units and accessible housing options for Michigan residents including returning citizens rebuilding stable housing after incarceration."),
    dict(name="Michigan Reconnect — Free Community College", category="education", region="Statewide",
         phone="517-335-5858", website="https://www.michigan.gov/reconnect",
         address="", city="Lansing", county="Ingham", cov="statewide", served="",
         desc="State scholarship program providing tuition-free associate degree and certificate pathways at Michigan community colleges for eligible adults age 25 and older including returning citizens seeking workforce credentials."),
]

for p in PHASE3:
    desc_en = p.get("description") or (
        p["desc"]
        + " Returning citizens and families rebuilding after incarceration can call ahead to confirm "
        "walk-in hours, referral requirements, and documents needed before visiting."
    )
    desc_es = p.get("description_es") or (
        p["desc"]
        + " Los ciudadanos que regresan y las familias pueden llamar con anticipación para confirmar "
        "horarios sin cita, requisitos de referencia y documentos necesarios antes de visitar."
    )
    add(
        name=p["name"], category=p["category"], region=p.get("region", p.get("city", "")),
        description=desc_en,
        description_es=desc_es,
        address=p.get("address", ""), city=p.get("city", ""), phone=p["phone"], email="",
        website=p["website"],
        eligibility=p.get(
            "eligibility",
            "Open to Michigan residents in the program service area; justice-involved individuals generally welcome; income or referral rules vary by service.",
        ),
        eligibility_es=p.get(
            "eligibility_es",
            "Abierto a residentes de Michigan en el área de servicio; personas con antecedentes penales generalmente son bienvenidas; las reglas varían según el servicio.",
        ),
        notes=p.get("notes", f"Call {p['phone']} to confirm current intake hours and whether walk-ins or referrals are accepted."),
        notes_es=p.get("notes_es", f"Llame al {p['phone']} para confirmar horarios de admisión y si se aceptan visitas sin cita o referencias."),
        hours=p.get("hours", "Call for current hours"),
        tags=p.get("tags", f"reentry|{p.get('county', 'statewide').lower() or 'statewide'}"),
        services=p.get("services", ""),
        county=p.get("county", ""),
        served_counties=p.get("served", ""), coverage=p["cov"],
        _source=p["website"], _source_type="nonprofit", _confidence="high",
    )

# --- Phase 4: Program-level expansion ---
from michigan_phase4_expansion import register_phase4
register_phase4(add)

from phase3b_gapfill import register_phase3b_michigan
register_phase3b_michigan(add, ENTRIES)

from michigan_pass2_expansion import register_pass2
register_pass2(add)

from michigan_phase5_depth_expansion import register_phase5
register_phase5(add)

# Fix single-county served_counties
for entry in ENTRIES:
    if entry.get("coverage") == "single" and not entry.get("served_counties") and entry.get("county"):
        entry["served_counties"] = entry["county"]

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
for r in low:
    print(f"  id {r['id_reference']}: {r['notes']}")
