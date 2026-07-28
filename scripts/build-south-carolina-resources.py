#!/usr/bin/env python3
"""Generate south-carolina-resources.csv and south-carolina-research-log.csv.

RESOURCES_UUID_PREFIX comment db000001
"""
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES_PATH = ROOT / "data" / "south-carolina-resources.csv"
LOG_PATH = ROOT / "data" / "south-carolina-research-log.csv"
DATE = "2026-07-06"

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
    name="SCDC — Reentry Programs",
    category="state-agency", region="Statewide",
    description="The South Carolina Department of Corrections coordinates statewide reentry programming, pre-release planning, and community partner connections for individuals preparing to leave SCDC custody or under community supervision through the Department of Probation, Parole and Pardon Services. Staff work with county DSS offices, SC Works career centers, and treatment providers on housing, employment, and benefits navigation before and after release. This office provides planning and referrals—not a walk-in crisis line or emergency cash provider.",
    description_es="El Departamento de Correcciones de Carolina del Sur coordina programación estatal de reinserción, planificación previa a la liberación y conexiones con aliados comunitarios para personas que preparan salir de custodia de SCDC o bajo supervisión comunitaria a través del Departamento de Probatoria, Libertad Condicional e Indulto. El personal trabaja con oficinas DSS del condado, centros SC Works y proveedores de tratamiento. Esta oficina ofrece planificación y referencias, no es una línea de crisis ni proveedor de efectivo de emergencia.",
    address="4444 Broad River Road", city="Columbia", phone="803-896-8555", email="",
    website="https://doc.sc.gov/programs",
    eligibility="Individuals in SCDC custody or recently released seeking state reentry coordination; community partners seeking SCDC engagement.",
    eligibility_es="Personas en custodia de SCDC o recién liberadas que buscan coordinación estatal de reinserción; aliados comunitarios.",
    notes="Visit doc.sc.gov/programs for reentry resources; coordinate through facility reentry staff and assigned probation or parole officer after release.",
    notes_es="Visite doc.sc.gov/programs para recursos de reinserción; coordine a través del personal de reinserción de la instalación y el oficial de probatoria asignado.",
    hours="State office Monday–Friday business hours",
    tags="statewide|reentry|SCDC|DOC|pre-release|parole",
    services="Pre-release planning|Transitional programming coordination|Community partner referrals|Reentry resource navigation|Supervision linkage",
    county="Richland", served_counties="", coverage="statewide",
    _source="https://doc.sc.gov/programs", _source_type="government", _confidence="high",
)
add(
    name="SCDPPPS — Probation, Parole & Pardon Services",
    category="probation-parole", region="Statewide",
    description="The South Carolina Department of Probation, Parole and Pardon Services supervises more than 30,000 adults on probation and parole through field offices in every region of the state. District agents connect justice-involved South Carolinians to local reentry partners for housing, employment, treatment compliance, and community reporting. Contact your assigned agent—not a walk-in benefits or emergency housing intake center.",
    description_es="El Departamento de Probatoria, Libertad Condicional e Indulto de Carolina del Sur supervisa a más de 30.000 adultos en probatoria y libertad condicional a través de oficinas de campo en cada región del estado. Los agentes conectan a carolinenses con antecedentes penales con aliados locales de reinserción para vivienda, empleo y cumplimiento de tratamiento. Contacte a su agente asignado; no es un centro de admisión de beneficios o vivienda de emergencia.",
    address="1100 North Main Street", city="Columbia", phone="803-734-3900", email="",
    website="https://www.ppp.sc.gov",
    eligibility="Adults under SCDPPPS probation, parole, or community supervision in South Carolina; report to assigned agent.",
    eligibility_es="Adultos bajo supervisión probatoria, libertad condicional o comunitaria de SCDPPPS en Carolina del Sur; reporte al agente asignado.",
    notes="Find regional field offices at ppp.sc.gov; statewide information 803-734-3900; ask your agent about local reentry referrals.",
    notes_es="Encuentre oficinas regionales en ppp.sc.gov; información estatal 803-734-3900; pregunte a su agente sobre referencias locales de reinserción.",
    hours="Field offices typically Monday–Friday business hours",
    tags="statewide|probation-parole|SCDPPPS|community-supervision|reentry",
    services="Probation supervision|Parole supervision|Community reporting|Treatment referrals|Reentry partner coordination",
    county="Richland", served_counties="", coverage="statewide",
    _source="https://www.ppp.sc.gov", _source_type="government", _confidence="high",
)
add(
    name="SC Benefits Portal — Online Applications",
    category="financial-assistance", region="Statewide",
    description="The South Carolina Benefits Portal at benefitsportal.dss.sc.gov is the official online system for applying for and managing SNAP food assistance, Medicaid and Healthy Connections coverage, TANF cash benefits, child care subsidies, and energy assistance through county Department of Social Services offices. Justice-involved South Carolinians can apply for health coverage and food support after release; county DSS staff assist with verification at all 46 county offices.",
    description_es="El Portal de Beneficios de Carolina del Sur en benefitsportal.dss.sc.gov es el sistema en línea oficial para solicitar y administrar asistencia alimentaria SNAP, cobertura Medicaid y Healthy Connections, beneficios en efectivo TANF, subsidios de cuidado infantil y asistencia energética a través de oficinas DSS del condado. Los carolinenses en reinserción pueden solicitar cobertura de salud y apoyo alimentario después de la liberación.",
    address="", city="", phone="1-800-616-1309", email="", website="https://benefitsportal.dss.sc.gov",
    eligibility="South Carolina residents meeting income and program requirements for Medicaid, SNAP, or TANF; criminal record generally not a barrier.",
    eligibility_es="Residentes de Carolina del Sur que cumplan requisitos de ingresos para Medicaid, SNAP o TANF; los antecedentes penales generalmente no son barrera.",
    notes="Apply online at benefitsportal.dss.sc.gov; call 1-800-616-1309 for DSS help; visit your county DSS office for in-person assistance.",
    notes_es="Solicite en benefitsportal.dss.sc.gov; llame al 1-800-616-1309; visite su oficina DSS del condado para asistencia presencial.",
    hours="Online 24/7; county DSS office hours vary",
    tags="statewide|benefits|SNAP|Medicaid|online|reentry",
    services="Medicaid application|SNAP enrollment|TANF cash assistance|Child care subsidies|Benefits account management",
    county="", served_counties="", coverage="statewide",
    _source="https://benefitsportal.dss.sc.gov", _source_type="government", _confidence="high",
)
add(
    name="SC DSS — Benefits & Family Support Portal",
    category="financial-assistance", region="Statewide",
    description="The South Carolina Department of Social Services administers SNAP, TANF, Medicaid intake, energy assistance, and child care subsidies through 46 county offices organized in four regional service areas. Returning citizens can apply online through portal.dss.sc.gov or in person at their county DSS office with help establishing food and health benefits after release from SCDC custody or county jails.",
    description_es="El Departamento de Servicios Sociales de Carolina del Sur administra SNAP, TANF, admisión de Medicaid, asistencia energética y subsidios de cuidado infantil a través de 46 oficinas del condado organizadas en cuatro áreas de servicio regionales. Los ciudadanos que regresan pueden solicitar en línea a través de portal.dss.sc.gov o en persona en su oficina DSS del condado.",
    address="1535 Confederate Avenue", city="Columbia", phone="1-800-616-1309", email="",
    website="https://portal.dss.sc.gov",
    eligibility="South Carolina residents meeting income and household-size requirements; criminal record generally not a barrier to SNAP and Medicaid.",
    eligibility_es="Residentes de Carolina del Sur que cumplan requisitos de ingresos y tamaño del hogar; los antecedentes penales generalmente no son barrera para SNAP y Medicaid.",
    notes="Apply at portal.dss.sc.gov or benefitsportal.dss.sc.gov; call 1-800-616-1309; bring ID and release documents to county office.",
    notes_es="Solicite en portal.dss.sc.gov o benefitsportal.dss.sc.gov; llame al 1-800-616-1309; traiga identificación y documentos de liberación.",
    hours="County DSS offices typically Monday–Friday business hours",
    tags="statewide|benefits|SNAP|Medicaid|DSS|reentry",
    services="SNAP enrollment|Medicaid application|TANF intake|County DSS referrals|Document verification",
    county="Richland", served_counties="", coverage="statewide",
    _source="https://portal.dss.sc.gov", _source_type="government", _confidence="high",
)
add(
    name="SC 211",
    category="state-agency", region="Statewide",
    description="SC 211 is a free statewide information and referral service connecting South Carolina residents to health and human services including housing, food, utilities, employment, and crisis support across all 46 counties. United Way-supported navigators help callers find local programs by need and ZIP code through sc211.org and the 211 phone line. SC 211 is a referral service—not a direct-service provider.",
    description_es="SC 211 es un servicio gratuito de información y referencia estatal que conecta a residentes de Carolina del Sur con servicios de salud y humanos incluyendo vivienda, alimentos, servicios públicos, empleo y apoyo en crisis en los 46 condados. Navegadores apoyados por United Way ayudan a encontrar programas locales por necesidad y código postal. Es un servicio de referencia, no un proveedor directo.",
    address="", city="", phone="211", email="", website="https://sc211.org",
    eligibility="Open to all South Carolina residents; no criminal-record restrictions stated.",
    eligibility_es="Abierto a todos los residentes de Carolina del Sur; sin restricciones de antecedentes indicadas.",
    notes="Dial 211 from any South Carolina phone; search resources online at sc211.org; text your ZIP code to 898-211.",
    notes_es="Marque 211 desde cualquier teléfono de Carolina del Sur; busque recursos en sc211.org; envíe su código postal al 898-211.",
    hours="Available during published service hours; check sc211.org",
    tags="statewide|hotline|211|referral-only|basic-needs",
    services="Information and referral|Housing resource navigation|Benefits referrals|Crisis resource connections",
    county="", served_counties="", coverage="statewide",
    _source="https://sc211.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="South Carolina Legal Services — Statewide Helpline",
    category="legal-aid", region="Statewide",
    description="South Carolina Legal Services is the state's primary nonprofit civil legal aid provider serving low-income South Carolinians with housing, public benefits, family law, and criminal record relief assistance including expungement under South Carolina statutes. Centralized intake at 1-888-346-5592 routes callers to regional offices in Charleston, Columbia, Florence, Greenville, and Spartanburg—not criminal defense representation.",
    description_es="South Carolina Legal Services es el principal proveedor sin fines de lucro de asistencia legal civil del estado que sirve a carolinenses de bajos ingresos con vivienda, beneficios públicos, derecho familiar y alivio de antecedentes penales incluida expungación. La admisión centralizada al 1-888-346-5592 enruta a oficinas regionales, no defensa penal.",
    address="2109 Bull Street", city="Columbia", phone="1-888-346-5592", email="",
    website="https://sclegal.org",
    eligibility="Low-income South Carolina residents with non-criminal legal problems; LSC income limits apply; offense-type restrictions may apply for record relief.",
    eligibility_es="Residentes de Carolina del Sur de bajos ingresos con problemas legales no penales; aplican límites de ingresos LSC; pueden aplicar restricciones por tipo de delito para alivio de antecedentes.",
    notes="Apply online at sclegal.org or call 1-888-346-5592; regional offices serve specific counties listed on the website.",
    notes_es="Solicite en sclegal.org o llame al 1-888-346-5592; las oficinas regionales sirven condados específicos listados en el sitio web.",
    hours="Intake Monday–Friday business hours; online application 24/7",
    tags="statewide|legal-aid|low-income|expungement|hotline",
    services="Civil legal representation|Expungement assistance|Housing legal aid|Benefits advocacy|Regional office referrals",
    county="Richland", served_counties="", coverage="statewide",
    _source="https://sclegal.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="SC Appleseed Legal Justice Center",
    category="reentry-organizations", region="Statewide",
    description="The South Carolina Appleseed Legal Justice Center advocates for fair public policies and connects low-income South Carolinians—including justice-involved residents—to legal resources, benefits navigation, and workforce partners across the state. Staff provide policy education, community outreach, and referral navigation for housing, employment, and record relief—not direct emergency cash or shelter placement.",
    description_es="El Centro de Justicia Legal SC Appleseed aboga por políticas públicas justas y conecta a carolinenses de bajos ingresos—incluidos residentes con antecedentes penales—a recursos legales, navegación de beneficios y aliados laborales en todo el estado. El personal ofrece educación de políticas y referencias, no efectivo de emergencia ni colocación en refugio.",
    address="1201 Main Street, Suite 1820", city="Columbia", phone="803-779-1112", email="",
    website="https://scjustice.org",
    eligibility="Low-income South Carolina residents and advocates seeking policy information, legal referrals, and reentry resource navigation.",
    eligibility_es="Residentes de Carolina del Sur de bajos ingresos y defensores que buscan información de políticas, referencias legales y navegación de recursos de reinserción.",
    notes="Visit scjustice.org for policy resources; connects to SCLS regional offices and local reentry coalitions.",
    notes_es="Visite scjustice.org para recursos de políticas; conecta con oficinas regionales de SCLS y coaliciones locales de reinserción.",
    hours="Monday–Friday business hours",
    tags="statewide|reentry|policy|fair-chance|referral-only",
    services="Policy advocacy|Legal resource referrals|Benefits education|Workforce partner navigation|Community outreach",
    county="Richland", served_counties="", coverage="statewide",
    _source="https://scjustice.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="SC Bar — Lawyer Referral & Pro Bono Program",
    category="legal-aid", region="Statewide",
    description="The South Carolina Bar Lawyer Referral Service and Pro Bono Program connect South Carolinians to attorneys for civil matters including housing, family law, and limited criminal record relief guidance. The PILS pro bono initiative coordinates volunteer attorneys for qualifying low-income clients who do not meet full legal aid eligibility. Referral and limited pro bono—not a public defender office.",
    description_es="El Servicio de Referencia de Abogados y Programa Pro Bono del Colegio de Abogados de Carolina del Sur conecta a carolinenses con abogados para asuntos civiles incluyendo vivienda, derecho familiar y orientación limitada sobre alivio de antecedentes penales. La iniciativa PILS coordina abogados voluntarios para clientes de bajos ingresos. Referencia y pro bono limitado, no defensor público.",
    address="950 Taylor Street", city="Columbia", phone="803-799-6653", email="",
    website="https://www.scbar.org/public/get-legal-help/lawyer-referral-service/",
    eligibility="South Carolina residents seeking attorney referrals; pro bono through PILS for qualifying low-income civil matters.",
    eligibility_es="Residentes de Carolina del Sur que buscan referencias de abogados; pro bono a través de PILS para asuntos civiles de bajos ingresos calificados.",
    notes="Call 803-799-6653 for lawyer referral; visit scbar.org for PILS and pro bono program information.",
    notes_es="Llame al 803-799-6653 para referencia de abogado; visite scbar.org para información del programa PILS y pro bono.",
    hours="Monday–Friday business hours",
    tags="statewide|legal-aid|lawyer-referral|pro-bono|reentry",
    services="Attorney referrals|Pro bono civil assistance|PILS volunteer coordination|Legal information resources",
    county="Richland", served_counties="", coverage="statewide",
    _source="https://www.scbar.org/public/get-legal-help/lawyer-referral-service/", _source_type="nonprofit", _confidence="high",
)
add(
    name="SC Works — Statewide Workforce System",
    category="employment", region="Statewide",
    description="SC Works is South Carolina's statewide workforce system connecting job seekers—including justice-involved South Carolinians—to SC Works centers, career coaching, unemployment services, and WIOA training referrals through regional workforce boards covering all 46 counties. Fair-chance employment partners and SC Second Chance initiatives coordinate through SC Works offices for returning citizens seeking sustainable employment.",
    description_es="SC Works es el sistema estatal de fuerza laboral de Carolina del Sur que conecta a buscadores de empleo—incluidos carolinenses con antecedentes penales—a centros SC Works, coaching de carrera, servicios de desempleo y referencias de capacitación WIOA a través de juntas regionales en los 46 condados. Las iniciativas de empleo de segunda oportunidad se coordinan a través de oficinas SC Works.",
    address="1550 Gadsden Street", city="Columbia", phone="1-866-359-3222", email="",
    website="https://www.scworks.org",
    eligibility="Open to South Carolina job seekers including justice-involved individuals; core career center services are free.",
    eligibility_es="Abierto a buscadores de empleo de Carolina del Sur incluidas personas con antecedentes penales; servicios básicos del centro de carrera son gratuitos.",
    notes="Find your nearest SC Works center at scworks.org; register for job search tools; pairs with DEW unemployment services.",
    notes_es="Encuentre su centro SC Works más cercano en scworks.org; regístrese para herramientas de búsqueda de empleo; se vincula con servicios de desempleo DEW.",
    hours="Career centers Monday–Friday business hours",
    tags="statewide|employment|SC-Works|WIOA|fair-chance|reentry",
    services="Job search assistance|Career coaching|WIOA training referrals|Unemployment services|Fair-chance employment navigation",
    county="Richland", served_counties="", coverage="statewide",
    _source="https://www.scworks.org", _source_type="government", _confidence="high",
)
add(
    name="SC Department of Employment and Workforce (DEW)",
    category="employment", region="Statewide",
    description="The South Carolina Department of Employment and Workforce administers unemployment insurance, labor market information, and workforce development programs that partner with SC Works centers statewide. Justice-involved South Carolinians can file unemployment claims, access job training referrals, and connect to employer services through dew.sc.gov and local SC Works offices after release.",
    description_es="El Departamento de Empleo y Fuerza Laboral de Carolina del Sur administra seguro de desempleo, información del mercado laboral y programas de desarrollo de la fuerza laboral que se asocian con centros SC Works en todo el estado. Los carolinenses con antecedentes penales pueden presentar reclamaciones de desempleo y conectarse con servicios para empleadores a través de dew.sc.gov.",
    address="1550 Gadsden Street", city="Columbia", phone="1-866-831-1724", email="",
    website="https://dew.sc.gov",
    eligibility="South Carolina workers meeting unemployment eligibility requirements; job seekers may access SC Works partner services.",
    eligibility_es="Trabajadores de Carolina del Sur que cumplan requisitos de elegibilidad para desempleo; buscadores de empleo pueden acceder a servicios aliados de SC Works.",
    notes="File unemployment at dew.sc.gov; employer services and labor data at dew.sc.gov; SC Works centers for reemployment help.",
    notes_es="Presente desempleo en dew.sc.gov; servicios para empleadores y datos laborales en dew.sc.gov; centros SC Works para ayuda de reempleo.",
    hours="Online 24/7; phone support Monday–Friday business hours",
    tags="statewide|employment|DEW|unemployment|SC-Works|reentry",
    services="Unemployment insurance|Labor market information|Workforce development|SC Works partnerships|Employer services",
    county="Richland", served_counties="", coverage="statewide",
    _source="https://dew.sc.gov", _source_type="government", _confidence="high",
)
add(
    name="SC Vocational Rehabilitation Department (SCVRD)",
    category="employment", region="Statewide",
    description="The South Carolina Vocational Rehabilitation Department helps South Carolinians with disabilities—including justice-involved individuals with qualifying disabilities—prepare for, obtain, and maintain employment through counseling, training, job placement, and employer partnerships at offices statewide. SCVRD coordinates with SC Works and SCDC reentry programs for disability employment supports after release from custody.",
    description_es="El Departamento de Rehabilitación Vocacional de Carolina del Sur ayuda a carolinenses con discapacidades—incluidas personas con antecedentes penales con discapacidades calificadas—a prepararse, obtener y mantener empleo a través de consejería, capacitación, colocación laboral y alianzas con empleadores. SCVRD coordina con SC Works y programas de reinserción de SCDC.",
    address="1410 Boston Avenue", city="West Columbia", phone="1-800-832-7524", email="",
    website="https://scvrd.net",
    eligibility="South Carolina residents with physical or mental disabilities that create employment barriers; eligibility determined through SCVRD assessment.",
    eligibility_es="Residentes de Carolina del Sur con discapacidades físicas o mentales que crean barreras laborales; elegibilidad determinada por evaluación SCVRD.",
    notes="Apply at scvrd.net or call 1-800-832-7524; area offices listed at scvrd.net/locations.",
    notes_es="Solicite en scvrd.net o llame al 1-800-832-7524; oficinas de área en scvrd.net/locations.",
    hours="State and regional offices Monday–Friday business hours",
    tags="statewide|employment|SCVRD|disability|reentry|WIOA",
    services="Vocational counseling|Job placement|Skills training|Employer partnerships|Disability employment supports",
    county="Lexington", served_counties="", coverage="statewide",
    _source="https://scvrd.net", _source_type="government", _confidence="high",
)
add(
    name="SCDMH — Behavioral Health Services",
    category="healthcare", region="Statewide",
    description="The South Carolina Department of Mental Health operates community mental health centers, crisis services, and substance use treatment programs serving all 46 counties. Justice-involved South Carolinians can access outpatient counseling, psychiatric services, and community-based treatment through local SCDMH centers—not emergency housing or benefits intake at the state office.",
    description_es="El Departamento de Salud Mental de Carolina del Sur opera centros comunitarios de salud mental, servicios de crisis y programas de tratamiento de uso de sustancias en los 46 condados. Los carolinenses con antecedentes penales pueden acceder a consejería ambulatoria, servicios psiquiátricos y tratamiento comunitario a través de centros locales SCDMH.",
    address="2414 Bull Street", city="Columbia", phone="803-898-8581", email="",
    website="https://scdmh.net",
    eligibility="South Carolina residents needing mental health or substance use services; intake through local community mental health centers.",
    eligibility_es="Residentes de Carolina del Sur que necesiten servicios de salud mental o uso de sustancias; admisión a través de centros comunitarios locales.",
    notes="Find your local center at scdmh.net; crisis line 833-364-2274; pairs with 988 for behavioral health emergencies.",
    notes_es="Encuentre su centro local en scdmh.net; línea de crisis 833-364-2274; se vincula con 988 para emergencias de salud conductual.",
    hours="Crisis services 24/7; clinic hours vary by center",
    tags="statewide|healthcare|behavioral-health|SCDMH|crisis|reentry",
    services="Outpatient mental health|Psychiatric services|Substance use treatment|Crisis intervention|Community mental health centers",
    county="Richland", served_counties="", coverage="statewide",
    _source="https://scdmh.net", _source_type="government", _confidence="high",
)
add(
    name="SC CARES — Statewide Reentry Network",
    category="reentry-organizations", region="Statewide",
    description="SC CARES is South Carolina's statewide community-based reentry network providing mentoring, case management, employment navigation, and life-skills support for justice-involved adults returning from SCDC custody and local jails. Regional SC CARES sites in Columbia, Charleston, Greenville, Florence, and Rock Hill coordinate with SCDPPPS agents, SC Works, and local housing partners. Direct reentry services—not a benefits application office.",
    description_es="SC CARES es la red estatal comunitaria de reinserción de Carolina del Sur que ofrece mentoría, manejo de casos, navegación de empleo y apoyo en habilidades de vida para adultos con antecedentes penales que regresan de custodia SCDC y cárceles locales. Los sitios regionales en Columbia, Charleston, Greenville, Florence y Rock Hill coordinan con agentes SCDPPPS y SC Works.",
    address="2711 Middleburg Drive, Suite 111", city="Columbia", phone="803-708-4863", email="",
    website="https://sccares.org",
    eligibility="Justice-involved South Carolina adults within 12 months of release or under community supervision; regional enrollment requirements vary.",
    eligibility_es="Adultos de Carolina del Sur con antecedentes penales dentro de 12 meses de la liberación o bajo supervisión comunitaria; los requisitos de inscripción regional varían.",
    notes="Visit sccares.org for regional site contacts; Columbia hub 803-708-4863; pairs with SCDPPPS and SC Works in each region.",
    notes_es="Visite sccares.org para contactos de sitios regionales; centro de Columbia 803-708-4863; se vincula con SCDPPPS y SC Works en cada región.",
    hours="Regional offices Monday–Friday business hours",
    tags="statewide|reentry|SC-CARES|mentoring|employment|case-management",
    services="Reentry mentoring|Case management|Employment navigation|Life skills training|Regional reentry coordination",
    county="Richland", served_counties="", coverage="statewide",
    _source="https://sccares.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="SCDMV Online — ID & Driver Services",
    category="id-documentation", region="Statewide",
    description="SCDMV Online at scdmvonline.com is South Carolina's portal for scheduling DMV appointments, renewing licenses, and obtaining identification documents needed for employment, housing, and benefits applications after release. Returning citizens can use branch locator tools and online services to replace lost IDs and restore driving privileges per SCDMV policy. ID and licensing services—not a legal aid or benefits office.",
    description_es="SCDMV Online en scdmvonline.com es el portal de Carolina del Sur para programar citas del DMV, renovar licencias y obtener documentos de identificación necesarios para empleo, vivienda y solicitudes de beneficios después de la liberación. Los ciudadanos que regresan pueden usar herramientas de localización de sucursales y servicios en línea para reemplazar identificaciones perdidas.",
    address="", city="", phone="803-896-5000", email="",
    website="https://www.scdmvonline.com",
    eligibility="South Carolina residents seeking driver's licenses, state IDs, or vehicle registration; bring required identity documents per SCDMV checklist.",
    eligibility_es="Residentes de Carolina del Sur que busquen licencias de conducir, identificaciones estatales o registro de vehículos; traiga documentos de identidad requeridos según lista SCDMV.",
    notes="Schedule appointments at scdmvonline.com; call 803-896-5000; SCDC and county jail reentry staff may coordinate DMV visits before release.",
    notes_es="Programe citas en scdmvonline.com; llame al 803-896-5000; el personal de reinserción de SCDC puede coordinar visitas al DMV antes de la liberación.",
    hours="Online 24/7; branch hours vary",
    tags="statewide|id-documentation|DMV|driver-license|reentry",
    services="State ID issuance|Driver license services|Appointment scheduling|Vehicle registration|Online DMV transactions",
    county="", served_counties="", coverage="statewide",
    _source="https://www.scdmvonline.com", _source_type="government", _confidence="high",
)
add(
    name="SC Department of Veterans' Affairs (SCDVA)",
    category="veterans", region="Statewide",
    description="The South Carolina Department of Veterans' Affairs helps honorably discharged and qualifying veterans and their families access VA benefits, disability claims, education benefits, and employment programs through county veterans service officers in all 46 counties. Justice-involved veterans can receive free benefits claims assistance and referrals to veteran treatment courts and SC CARES veteran tracks.",
    description_es="El Departamento de Asuntos de Veteranos de Carolina del Sur ayuda a veteranos con baja honorable o calificados y sus familias a acceder a beneficios VA, reclamaciones de discapacidad, beneficios educativos y programas de empleo a través de oficiales de servicios para veteranos del condado en los 46 condados.",
    address="1205 Pendleton Street", city="Columbia", phone="803-734-0200", email="",
    website="https://scdva.sc.gov",
    eligibility="Honorably discharged or qualifying South Carolina veterans and their dependents; service documentation required.",
    eligibility_es="Veteranos de Carolina del Sur con baja honorable o calificados y sus dependientes; se requiere documentación de servicio.",
    notes="Find your county veterans service office at scdva.sc.gov; free VA claims assistance at all 46 county offices.",
    notes_es="Encuentre su oficina de servicios para veteranos del condado en scdva.sc.gov; asistencia gratuita con reclamaciones VA.",
    hours="County offices Monday–Friday business hours",
    tags="statewide|veterans|VA-benefits|reentry|justice-involved-veterans",
    services="VA benefits claims assistance|Disability claims navigation|Education benefit referrals|Veteran employment programs|County VSO coordination",
    county="Richland", served_counties="", coverage="statewide",
    _source="https://scdva.sc.gov", _source_type="government", _confidence="high",
)
add(
    name="988 Suicide & Crisis Lifeline",
    category="healthcare", region="Statewide",
    description="The 988 Suicide and Crisis Lifeline provides free, confidential 24/7 support for people in mental health, substance use, or suicidal crises across South Carolina. Callers are connected to trained counselors who can de-escalate emergencies, provide crisis counseling, and refer to local SCDMH centers and mobile crisis teams. Crisis support—not reentry housing or benefits intake.",
    description_es="La Línea de Crisis y Prevención del Suicidio 988 ofrece apoyo gratuito y confidencial 24/7 para personas en crisis de salud mental, uso de sustancias o suicidio en toda Carolina del Sur. Los llamantes se conectan con consejeros capacitados que pueden desescalar emergencias y referir a centros SCDMH locales.",
    address="", city="", phone="988", email="", website="https://988lifeline.org",
    eligibility="Anyone in the United States experiencing a mental health or suicidal crisis; Spanish-language support available.",
    eligibility_es="Cualquier persona en Estados Unidos que experimente una crisis de salud mental o suicida; apoyo en español disponible.",
    notes="Dial or text 988; chat at 988lifeline.org; veterans press 1; pairs with SCDMH crisis line 833-364-2274 for local follow-up.",
    notes_es="Marque o envíe mensaje al 988; chat en 988lifeline.org; veteranos presione 1; se vincula con línea de crisis SCDMH 833-364-2274.",
    hours="24/7",
    tags="statewide|crisis|988|behavioral-health|hotline",
    services="Crisis counseling|Suicide prevention|Substance use crisis support|Local referral connections|Veterans crisis line",
    county="", served_counties="", coverage="statewide",
    _source="https://988lifeline.org", _source_type="government", _confidence="high",
)
add(
    name="SAMHSA National Helpline",
    category="substance-use-treatment", region="Statewide",
    description="The SAMHSA National Helpline at 1-800-662-4357 is a free, confidential, 24/7 treatment referral service connecting South Carolinians to local substance use disorder treatment providers, detox programs, and recovery support including justice-involved individuals seeking treatment after release. Referral specialists search by ZIP code and insurance status—not direct treatment at the helpline.",
    description_es="La Línea Nacional de Ayuda de SAMHSA al 1-800-662-4357 es un servicio gratuito y confidencial de referencia a tratamiento 24/7 que conecta a carolinenses con proveedores locales de trastornos por uso de sustancias, programas de desintoxicación y apoyo en recuperación incluidas personas con antecedentes penales.",
    address="", city="", phone="1-800-662-4357", email="", website="https://www.samhsa.gov/find-help/national-helpline",
    eligibility="Anyone in the United States seeking substance use treatment information and referrals; no insurance required to call.",
    eligibility_es="Cualquier persona en Estados Unidos que busque información y referencias de tratamiento de uso de sustancias; no se requiere seguro para llamar.",
    notes="Call 1-800-662-4357; TTY 1-800-487-4889; also use FindTreatment.gov for provider search; Spanish-language support available.",
    notes_es="Llame al 1-800-662-4357; TTY 1-800-487-4889; también use FindTreatment.gov; apoyo en español disponible.",
    hours="24/7",
    tags="statewide|substance-use-treatment|SAMHSA|hotline|referral-only",
    services="Treatment referrals|Detox program navigation|Recovery support connections|Insurance guidance|Provider search assistance",
    county="", served_counties="", coverage="statewide",
    _source="https://www.samhsa.gov/find-help/national-helpline", _source_type="government", _confidence="high",
)
add(
    name="FindTreatment.gov — Treatment Locator",
    category="substance-use-treatment", region="Statewide",
    description="FindTreatment.gov is SAMHSA's official online locator for substance use disorder treatment facilities across South Carolina, searchable by location, treatment type, payment options, and services offered including outpatient, residential, and medication-assisted treatment. Justice-involved South Carolinians and SCDPPPS agents use the tool to identify certified providers accepting Medicaid or offering sliding-fee care near their county.",
    description_es="FindTreatment.gov es el localizador en línea oficial de SAMHSA para instalaciones de tratamiento de trastornos por uso de sustancias en Carolina del Sur, buscable por ubicación, tipo de tratamiento, opciones de pago y servicios ofrecidos. Los carolinenses con antecedentes penales y agentes SCDPPPS usan la herramienta para identificar proveedores certificados.",
    address="", city="", phone="1-800-662-4357", email="", website="https://findtreatment.gov",
    eligibility="Open to anyone seeking substance use treatment information; facility-specific eligibility applies at enrollment.",
    eligibility_es="Abierto a cualquier persona que busque información de tratamiento de uso de sustancias; la elegibilidad específica de la instalación aplica al inscribirse.",
    notes="Search by ZIP code at findtreatment.gov; call SAMHSA helpline 1-800-662-4357 for live referral help; verify Medicaid acceptance with each provider.",
    notes_es="Busque por código postal en findtreatment.gov; llame a la línea SAMHSA 1-800-662-4357; verifique aceptación de Medicaid con cada proveedor.",
    hours="Online 24/7",
    tags="statewide|substance-use-treatment|SAMHSA|locator|MAT|reentry",
    services="Treatment facility search|Outpatient program locator|Residential treatment finder|MAT provider search|Payment option filtering",
    county="", served_counties="", coverage="statewide",
    _source="https://findtreatment.gov", _source_type="government", _confidence="high",
)
add(
    name="SC DHEC — Vital Records",
    category="id-documentation", region="Statewide",
    description="The South Carolina Department of Health and Environmental Control Vital Records office issues certified birth certificates, death certificates, and marriage records needed for benefits applications, employment verification, and ID restoration after incarceration. Returning citizens can order records online, by mail, or in person at the Columbia vital records office or through county health departments.",
    description_es="La oficina de Registros Vitales del Departamento de Salud y Control Ambiental de Carolina del Sur emite certificados de nacimiento, defunción y matrimonio certificados necesarios para solicitudes de beneficios, verificación de empleo y restauración de identificación después de la encarcelación.",
    address="2600 Bull Street", city="Columbia", phone="803-898-3630", email="",
    website="https://scdhec.gov/vital-records",
    eligibility="Individuals requesting their own vital records or authorized family members; government-issued photo ID required for in-person requests.",
    eligibility_es="Personas que soliciten sus propios registros vitales o familiares autorizados; se requiere identificación con foto emitida por el gobierno para solicitudes en persona.",
    notes="Order online at scdhec.gov/vital-records; Columbia office 2600 Bull Street; fees apply; needed for DMV ID and benefits verification.",
    notes_es="Ordene en línea en scdhec.gov/vital-records; oficina de Columbia 2600 Bull Street; aplican tarifas; necesario para identificación DMV y verificación de beneficios.",
    hours="Monday–Friday business hours; online ordering 24/7",
    tags="statewide|id-documentation|vital-records|birth-certificate|reentry",
    services="Birth certificate issuance|Death certificate copies|Marriage record requests|Online vital records ordering|County health department referrals",
    county="Richland", served_counties="", coverage="statewide",
    _source="https://scdhec.gov/vital-records", _source_type="government", _confidence="high",
)

# --- Phase 2: Major metro anchors ---
add(
    name="One80 Place — Charleston Reentry Housing",
    category="housing", region="Charleston / Charleston County",
    description="One80 Place is the Lowcountry's leading homeless services organization providing emergency shelter, rapid rehousing, permanent supportive housing, and veteran-specific programs for unhoused adults in Charleston County including returning citizens recently released from Charleston County Detention Center or SCDC custody. Case managers connect residents to SC Works, DSS benefits, and local employers through coordinated entry partners. Direct housing services—not a statewide hotline.",
    description_es="One80 Place es la principal organización de servicios para personas sin hogar del Lowcountry que ofrece refugio de emergencia, realojamiento rápido, vivienda de apoyo permanente y programas específicos para veteranos en el condado Charleston incluidos ciudadanos que regresan recién liberados. Los administradores de casos conectan a residentes con SC Works, beneficios DSS y empleadores locales.",
    address="35 Walnut Street", city="Charleston", phone="843-723-9477", email="",
    website="https://one80place.org",
    eligibility="Unhoused adults in Charleston County; justice-involved individuals welcome through coordinated entry intake.",
    eligibility_es="Adultos sin hogar en el condado Charleston; personas con antecedentes penales bienvenidas mediante admisión de entrada coordinada.",
    notes="Call 843-723-9477 for housing intake; veteran programs through SSVF; pairs with Turning Leaf and SC CARES Charleston.",
    notes_es="Llame al 843-723-9477 para admisión de vivienda; programas para veteranos a través de SSVF; se vincula con Turning Leaf y SC CARES Charleston.",
    hours="Contact for intake hours",
    tags="charleston|housing|shelter|rapid-rehousing|reentry|veterans",
    services="Emergency shelter|Rapid rehousing|Permanent supportive housing|Veteran housing|Case management",
    county="Charleston", served_counties="Charleston", coverage="single",
    _source="https://one80place.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Turning Leaf Project — Charleston",
    category="reentry-organizations", region="Charleston / Charleston County",
    description="Turning Leaf Project provides cognitive-behavioral programming, transitional employment, and case management for justice-involved men returning to Charleston County after incarceration. Participants complete evidence-based classes while working in Turning Leaf's social enterprise printing shop, building job skills and stable employment histories before transitioning to community employers. Men-only reentry program—not emergency shelter for families.",
    description_es="Turning Leaf Project ofrece programación cognitivo-conductual, empleo transicional y manejo de casos para hombres con antecedentes penales que regresan al condado Charleston después de la encarcelación. Los participantes completan clases basadas en evidencia mientras trabajan en la imprenta de empresa social de Turning Leaf.",
    address="423 Meeting Street", city="Charleston", phone="843-972-7399", email="",
    website="https://turningleafproject.com",
    eligibility="Justice-involved men referred from SCDC, Charleston County Jail, or SCDPPPS; program-specific enrollment requirements.",
    eligibility_es="Hombres con antecedentes penales referidos por SCDC, cárcel del condado Charleston o SCDPPPS; requisitos específicos de inscripción.",
    notes="Call 843-972-7399 for enrollment; referral from probation agent or facility reentry staff preferred; pairs with One80 Place and SC Works Charleston.",
    notes_es="Llame al 843-972-7399 para inscripción; se prefiere referencia del agente de probatoria; se vincula con One80 Place y SC Works Charleston.",
    hours="Monday–Friday business hours; program schedules vary",
    tags="charleston|reentry|employment|cognitive-behavioral|men|reentry-organizations",
    services="Cognitive-behavioral classes|Transitional employment|Social enterprise work|Case management|Employer transition support",
    county="Charleston", served_counties="Charleston|Berkeley|Dorchester", coverage="multi",
    _source="https://turningleafproject.com", _source_type="nonprofit", _confidence="high",
)
add(
    name="Lowcountry Food Bank",
    category="food-nutrition", region="Charleston / Tri-County",
    description="Lowcountry Food Bank distributes millions of pounds of food annually through partner agencies, mobile pantries, and direct programs serving food-insecure households in Berkeley, Charleston, Dorchester, and coastal South Carolina counties. Returning citizens reestablishing food security after release can find partner pantries by ZIP code and access SNAP application assistance through agency partners.",
    description_es="Lowcountry Food Bank distribuye millones de libras de alimentos anualmente a través de agencias aliadas, despensas móviles y programas directos sirviendo hogares con inseguridad alimentaria en Berkeley, Charleston, Dorchester y condados costeros de Carolina del Sur.",
    address="2864 Azalea Drive", city="North Charleston", phone="843-747-8146", email="",
    website="https://lowcountryfoodbank.org",
    eligibility="Food-insecure residents of the Lowcountry service area; partner agency registration may require proof of address.",
    eligibility_es="Residentes con inseguridad alimentaria del área de servicio del Lowcountry; el registro en agencias aliadas puede requerir prueba de dirección.",
    notes="Find partner pantries at lowcountryfoodbank.org/find-food; call 843-747-8146; mobile pantry schedule online.",
    notes_es="Encuentre despensas aliadas en lowcountryfoodbank.org/find-food; llame al 843-747-8146; horario de despensa móvil en línea.",
    hours="Warehouse Monday–Friday; partner pantry hours vary",
    tags="charleston|food-nutrition|food-bank|pantry|tri-county|reentry",
    services="Food distribution|Mobile food pantry|Partner agency network|SNAP outreach|Nutrition programs",
    county="Charleston", served_counties="Berkeley|Charleston|Dorchester|Beaufort|Colleton|Georgetown|Hampton|Jasper", coverage="multi",
    _source="https://lowcountryfoodbank.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Metanoia — North Charleston Community Development",
    category="basic-needs", region="North Charleston / Charleston County",
    description="Metanoia is a community development corporation in North Charleston providing youth programs, affordable housing, workforce development, and basic needs support for low-income residents including justice-involved adults in the Cooper River Bridge area. Staff connect participants to SC Works, DSS benefits, and local employers while operating community gardens and housing rehabilitation projects.",
    description_es="Metanoia es una corporación de desarrollo comunitario en North Charleston que ofrece programas juveniles, vivienda asequible, desarrollo de la fuerza laboral y apoyo de necesidades básicas para residentes de bajos ingresos incluidos adultos con antecedentes penales en el área del Puente Cooper River.",
    address="3100 Rivers Avenue", city="North Charleston", phone="843-529-3010", email="",
    website="https://pushingforward.org",
    eligibility="Low-income North Charleston and Charleston County residents; justice-involved participants welcome in workforce and housing programs.",
    eligibility_es="Residentes de bajos ingresos de North Charleston y el condado Charleston; participantes con antecedentes penales bienvenidos en programas de fuerza laboral y vivienda.",
    notes="Call 843-529-3010; workforce programs pair with SC Works North Charleston; affordable housing waitlist applies.",
    notes_es="Llame al 843-529-3010; programas de fuerza laboral se vinculan con SC Works North Charleston; aplica lista de espera de vivienda asequible.",
    hours="Monday–Friday business hours",
    tags="charleston|north-charleston|basic-needs|workforce|affordable-housing|reentry",
    services="Workforce development|Affordable housing|Youth programs|Community gardens|Basic needs navigation",
    county="Charleston", served_counties="Charleston", coverage="single",
    _source="https://pushingforward.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Oliver Gospel Mission — Columbia",
    category="housing", region="Columbia / Richland County",
    description="Oliver Gospel Mission in Columbia provides emergency shelter, addiction recovery, transitional housing, and workforce development for homeless men in Richland County including returning citizens recently released from Alvin S. Glenn Detention Center or SCDC custody. The long-term recovery program offers meals, counseling, GED preparation, and job placement on the Taylor Street campus. Men's shelter and recovery—not a women's or family intake center.",
    description_es="Oliver Gospel Mission en Columbia ofrece refugio de emergencia, recuperación de adicciones, vivienda transicional y desarrollo de la fuerza laboral para hombres sin hogar en el condado Richland incluidos ciudadanos que regresan recién liberados. El programa de recuperación a largo plazo ofrece comidas, consejería, preparación GED y colocación laboral.",
    address="1100 Taylor Street", city="Columbia", phone="803-256-7392", email="",
    website="https://olivergospelmission.org",
    eligibility="Homeless men in Richland County seeking shelter or recovery; justice-involved men welcome per program policy.",
    eligibility_es="Hombres sin hogar en el condado Richland que busquen refugio o recuperación; hombres con antecedentes penales bienvenidos según política.",
    notes="Call 803-256-7392 for intake; recovery program requires commitment; pairs with SC CARES Columbia and SC Works Midlands.",
    notes_es="Llame al 803-256-7392 para admisión; el programa de recuperación requiere compromiso; se vincula con SC CARES Columbia y SC Works Midlands.",
    hours="Shelter intake daily; office Monday–Friday business hours",
    tags="columbia|richland|housing|shelter|recovery|men|reentry",
    services="Emergency shelter|Addiction recovery|Transitional housing|GED preparation|Job placement",
    county="Richland", served_counties="Richland|Lexington", coverage="multi",
    _source="https://olivergospelmission.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="New Directions of the Midlands — Columbia",
    category="reentry-organizations", region="Columbia / Richland County",
    description="New Directions of the Midlands provides reentry case management, transitional housing referrals, employment coaching, and life-skills classes for justice-involved adults returning to Richland and Lexington counties. Staff coordinate with SCDPPPS agents, SC CARES, and Midlands employers to help returning citizens obtain IDs, benefits, and stable housing within 90 days of release.",
    description_es="New Directions of the Midlands ofrece manejo de casos de reinserción, referencias de vivienda transicional, coaching de empleo y clases de habilidades de vida para adultos con antecedentes penales que regresan a los condados Richland y Lexington.",
    address="2711 Middleburg Drive, Suite 304", city="Columbia", phone="803-731-3000", email="",
    website="https://newdirectionsmidlands.org",
    eligibility="Justice-involved adults in Richland or Lexington counties within 12 months of release; referral from SCDPPPS or self-referral.",
    eligibility_es="Adultos con antecedentes penales en los condados Richland o Lexington dentro de 12 meses de la liberación; referencia de SCDPPPS o autorreferencia.",
    notes="Call 803-731-3000 for intake; co-located with SC CARES regional hub; pairs with Oliver Gospel Mission and Transitions SC.",
    notes_es="Llame al 803-731-3000 para admisión; ubicado con el centro regional SC CARES; se vincula con Oliver Gospel Mission y Transitions SC.",
    hours="Monday–Friday business hours",
    tags="columbia|richland|lexington|reentry|case-management|employment|reentry-organizations",
    services="Reentry case management|Housing referrals|Employment coaching|Life skills classes|Benefits navigation",
    county="Richland", served_counties="Richland|Lexington", coverage="multi",
    _source="https://newdirectionsmidlands.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Transitions — Columbia Homeless Services",
    category="housing", region="Columbia / Richland County",
    description="Transitions is Columbia's primary homeless services provider offering emergency shelter, rapid rehousing, permanent supportive housing, and veteran programs for unhoused adults and families in Richland County including justice-involved individuals exiting jail or prison. The Main Street campus provides case management, employment navigation, and connections to Midlands SC Works and DSS offices.",
    description_es="Transitions es el principal proveedor de servicios para personas sin hogar de Columbia que ofrece refugio de emergencia, realojamiento rápido, vivienda de apoyo permanente y programas para veteranos para adultos y familias sin hogar en el condado Richland incluidas personas con antecedentes penales.",
    address="2025 Main Street", city="Columbia", phone="803-708-4862", email="",
    website="https://transitionssc.org",
    eligibility="Unhoused adults and families in Richland County; coordinated entry screening required for housing programs.",
    eligibility_es="Adultos y familias sin hogar en el condado Richland; se requiere evaluación de entrada coordinada para programas de vivienda.",
    notes="Call 803-708-4862 for coordinated entry; veteran SSVF program available; pairs with New Directions and SC CARES.",
    notes_es="Llame al 803-708-4862 para entrada coordinada; programa SSVF para veteranos disponible; se vincula con New Directions y SC CARES.",
    hours="Contact for shelter intake hours",
    tags="columbia|richland|housing|shelter|rapid-rehousing|veterans|reentry",
    services="Emergency shelter|Rapid rehousing|Permanent supportive housing|Veteran housing|Employment navigation",
    county="Richland", served_counties="Richland", coverage="single",
    _source="https://transitionssc.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="United Housing Connections — Greenville",
    category="housing", region="Greenville / Greenville County",
    description="United Housing Connections is the Upstate's lead homeless services organization providing coordinated entry, emergency shelter referrals, rapid rehousing, and permanent supportive housing for unhoused adults in Greenville County including returning citizens recently released from Greenville County Detention Center. Housing navigators connect participants to SC Works Greenville, Prisma Health, and local employers.",
    description_es="United Housing Connections es la principal organización de servicios para personas sin hogar del Upstate que ofrece entrada coordinada, referencias de refugio de emergencia, realojamiento rápido y vivienda de apoyo permanente para adultos sin hogar en el condado Greenville incluidos ciudadanos que regresan recién liberados.",
    address="135 Edinburgh Court", city="Greenville", phone="864-241-0462", email="",
    website="https://unitedhousingconnections.org",
    eligibility="Unhoused adults in Greenville County; coordinated entry assessment required; justice-involved individuals welcome.",
    eligibility_es="Adultos sin hogar en el condado Greenville; se requiere evaluación de entrada coordinada; personas con antecedentes penales bienvenidas.",
    notes="Call 864-241-0462 for housing assessment; Homeless Crisis Line 864-234-7505; pairs with Miracle Hill and SC CARES Greenville.",
    notes_es="Llame al 864-241-0462 para evaluación de vivienda; Línea de Crisis 864-234-7505; se vincula con Miracle Hill y SC CARES Greenville.",
    hours="Monday–Friday business hours; crisis line extended hours",
    tags="greenville|housing|coordinated-entry|rapid-rehousing|reentry",
    services="Coordinated entry|Emergency shelter referrals|Rapid rehousing|Permanent supportive housing|Housing navigation",
    county="Greenville", served_counties="Greenville", coverage="single",
    _source="https://unitedhousingconnections.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Miracle Hill Ministries — Greenville Recovery & Shelter",
    category="housing", region="Greenville / Greenville County",
    description="Miracle Hill Ministries operates emergency shelters, addiction recovery programs, and transitional housing for men, women, and children in Greenville County including justice-involved adults seeking faith-based recovery and stable housing after incarceration. The Overcomers addiction recovery program provides residential treatment, counseling, and workforce preparation on multiple Upstate campuses.",
    description_es="Miracle Hill Ministries opera refugios de emergencia, programas de recuperación de adicciones y vivienda transicional para hombres, mujeres y niños en el condado Greenville incluidos adultos con antecedentes penales que buscan recuperación basada en la fe y vivienda estable después de la encarcelación.",
    address="1890 Old Buncombe Road", city="Greenville", phone="864-268-4357", email="",
    website="https://miraclehill.org",
    eligibility="Homeless adults and families in Greenville County; Overcomers recovery program for adults with substance use disorders.",
    eligibility_es="Adultos y familias sin hogar en el condado Greenville; programa de recuperación Overcomers para adultos con trastornos por uso de sustancias.",
    notes="Call 864-268-4357 for shelter intake; Overcomers program separate intake; Spartanburg campus also serves Upstate.",
    notes_es="Llame al 864-268-4357 para admisión al refugio; admisión separada para programa Overcomers; campus de Spartanburg también sirve al Upstate.",
    hours="Shelter 24/7; office Monday–Friday business hours",
    tags="greenville|housing|shelter|recovery|SUD|faith-based|reentry",
    services="Emergency shelter|Addiction recovery|Transitional housing|Workforce preparation|Family shelter",
    county="Greenville", served_counties="Greenville|Spartanburg|Pickens|Anderson", coverage="multi",
    _source="https://miraclehill.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="ROAR — Reentry Organization of Anderson & Region",
    category="reentry-organizations", region="Anderson / Upstate",
    description="ROAR (Reentry Organization of Anderson and Region) provides reentry coaching, employment navigation, mentoring, and resource connections for justice-involved adults returning to Anderson, Greenville, Pickens, and Oconee counties. Staff work with SCDPPPS agents and Upstate employers to reduce recidivism through stable employment, housing referrals, and benefits enrollment support.",
    description_es="ROAR (Organización de Reinserción de Anderson y la Región) ofrece coaching de reinserción, navegación de empleo, mentoría y conexiones de recursos para adultos con antecedentes penales que regresan a los condados Anderson, Greenville, Pickens y Oconee.",
    address="604 N. Main Street", city="Anderson", phone="864-332-7856", email="",
    website="https://roarreentry.org",
    eligibility="Justice-involved adults in the Upstate service area; referral from SCDPPPS, facilities, or self-referral within 12 months of release.",
    eligibility_es="Adultos con antecedentes penales en el área de servicio del Upstate; referencia de SCDPPPS, instalaciones o autorreferencia dentro de 12 meses de la liberación.",
    notes="Call 864-332-7856 for enrollment; pairs with SC Works Anderson and United Housing Connections.",
    notes_es="Llame al 864-332-7856 para inscripción; se vincula con SC Works Anderson y United Housing Connections.",
    hours="Monday–Friday business hours",
    tags="anderson|upstate|reentry|employment|mentoring|reentry-organizations",
    services="Reentry coaching|Employment navigation|Mentoring|Housing referrals|Benefits enrollment support",
    county="Anderson", served_counties="Anderson|Greenville|Pickens|Oconee", coverage="multi",
    _source="https://roarreentry.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Miracle Hill Ministries — Spartanburg Campus",
    category="housing", region="Spartanburg / Spartanburg County",
    description="Miracle Hill's Spartanburg campus provides emergency shelter, the Overcomers addiction recovery program, and transitional housing for unhoused men and women in Spartanburg County including justice-involved adults returning from Spartanburg County Detention Center. Residents receive meals, counseling, life-skills classes, and connections to SC Works Spartanburg and local treatment providers.",
    description_es="El campus de Miracle Hill en Spartanburg ofrece refugio de emergencia, el programa de recuperación Overcomers y vivienda transicional para hombres y mujeres sin hogar en el condado Spartanburg incluidos adultos con antecedentes penales que regresan de la cárcel del condado.",
    address="499 Howard Street", city="Spartanburg", phone="864-582-0329", email="",
    website="https://miraclehill.org",
    eligibility="Homeless adults in Spartanburg County; Overcomers program for adults with substance use disorders willing to commit to residential recovery.",
    eligibility_es="Adultos sin hogar en el condado Spartanburg; programa Overcomers para adultos con trastornos por uso de sustancias dispuestos a comprometerse con recuperación residencial.",
    notes="Call 864-582-0329 for Spartanburg shelter intake; Overcomers admissions through miraclehill.org; pairs with Piedmont Community Actions.",
    notes_es="Llame al 864-582-0329 para admisión al refugio de Spartanburg; admisiones Overcomers a través de miraclehill.org; se vincula con Piedmont Community Actions.",
    hours="Shelter 24/7; office Monday–Friday business hours",
    tags="spartanburg|housing|shelter|recovery|SUD|reentry",
    services="Emergency shelter|Overcomers recovery|Transitional housing|Life skills classes|Employment referrals",
    county="Spartanburg", served_counties="Spartanburg|Cherokee|Union", coverage="multi",
    _source="https://miraclehill.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Piedmont Community Actions — Spartanburg",
    category="basic-needs", region="Spartanburg / Upstate",
    description="Piedmont Community Actions is the community action agency serving Spartanburg, Cherokee, and Union counties with emergency rent and utility assistance, weatherization, Head Start, and self-sufficiency coaching for low-income families including justice-involved households rebuilding after incarceration. Staff connect clients to SC Works, DSS benefits, and local housing partners.",
    description_es="Piedmont Community Actions es la agencia de acción comunitaria que sirve a los condados Spartanburg, Cherokee y Union con asistencia de emergencia para renta y servicios públicos, climatización, Head Start y coaching de autosuficiencia para familias de bajos ingresos incluidos hogares con antecedentes penales.",
    address="300 Piedmont Avenue", city="Spartanburg", phone="864-585-8181", email="",
    website="https://piedmontcaa.org",
    eligibility="Low-income residents of Spartanburg, Cherokee, and Union counties; income documentation required for emergency assistance.",
    eligibility_es="Residentes de bajos ingresos de los condados Spartanburg, Cherokee y Union; se requiere documentación de ingresos para asistencia de emergencia.",
    notes="Call 864-585-8181 for emergency assistance intake; weatherization and Head Start programs also available.",
    notes_es="Llame al 864-585-8181 para admisión de asistencia de emergencia; también programas de climatización y Head Start.",
    hours="Monday–Friday business hours",
    tags="spartanburg|basic-needs|emergency-assistance|community-action|reentry",
    services="Emergency rent assistance|Utility assistance|Weatherization|Head Start|Self-sufficiency coaching",
    county="Spartanburg", served_counties="Spartanburg|Cherokee|Union", coverage="multi",
    _source="https://piedmontcaa.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Hope Haven of the Lowcountry — Florence",
    category="housing", region="Florence / Pee Dee",
    description="Hope Haven of the Lowcountry provides emergency shelter, transitional housing, and case management for unhoused women and families in Florence and the Pee Dee region including justice-involved mothers reuniting with children after release from SCDC custody or Florence County Detention Center. Staff connect residents to SC Works Pee Dee, New Directions, and local treatment providers.",
    description_es="Hope Haven of the Lowcountry ofrece refugio de emergencia, vivienda transicional y manejo de casos para mujeres y familias sin hogar en Florence y la región Pee Dee incluidas madres con antecedentes penales que se reúnen con sus hijos después de la liberación.",
    address="1267 Celebration Boulevard", city="Florence", phone="843-669-0571", email="",
    website="https://hopehavenlowcountry.org",
    eligibility="Unhoused women and families in the Pee Dee region; justice-involved women with children welcome per intake policy.",
    eligibility_es="Mujeres y familias sin hogar en la región Pee Dee; mujeres con antecedentes penales con hijos bienvenidas según política de admisión.",
    notes="Call 843-669-0571 for intake; pairs with Keystone Substance Abuse Services and SC CARES Florence.",
    notes_es="Llame al 843-669-0571 para admisión; se vincula con Keystone Substance Abuse Services y SC CARES Florence.",
    hours="Contact for shelter intake hours",
    tags="florence|pee-dee|housing|shelter|women|families|reentry",
    services="Emergency shelter|Transitional housing|Case management|Family reunification support|Employment referrals",
    county="Florence", served_counties="Florence|Darlington|Marion|Dillon|Marlboro|Chesterfield", coverage="multi",
    _source="https://hopehavenlowcountry.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Keystone Substance Abuse Services — Florence",
    category="substance-use-treatment", region="Florence / Pee Dee",
    description="Keystone Substance Abuse Services is the Pee Dee region's primary substance use treatment provider offering outpatient counseling, intensive outpatient programs, medication-assisted treatment, and DUI evaluation services in Florence County. Justice-involved clients referred by SCDPPPS agents, drug courts, and reentry programs can access Medicaid-funded treatment and sliding-fee services.",
    description_es="Keystone Substance Abuse Services es el principal proveedor de tratamiento de uso de sustancias de la región Pee Dee que ofrece consejería ambulatoria, programas intensivos ambulatorios, tratamiento asistido con medicamentos y servicios de evaluación DUI en el condado Florence.",
    address="1305 West Evans Street", city="Florence", phone="843-669-7060", email="",
    website="https://keystonesc.org",
    eligibility="Adults and adolescents with substance use disorders in the Pee Dee region; Medicaid and sliding-fee accepted; justice referrals welcome.",
    eligibility_es="Adultos y adolescentes con trastornos por uso de sustancias en la región Pee Dee; se aceptan Medicaid y tarifa móvil; referencias de justicia bienvenidas.",
    notes="Call 843-669-7060 for intake; MAT program available; pairs with Hope Haven and SCDPPPS Pee Dee field offices.",
    notes_es="Llame al 843-669-7060 para admisión; programa MAT disponible; se vincula con Hope Haven y oficinas de campo SCDPPPS Pee Dee.",
    hours="Monday–Friday clinic hours; call for appointment",
    tags="florence|pee-dee|substance-use-treatment|MAT|outpatient|reentry",
    services="Outpatient counseling|Intensive outpatient|Medication-assisted treatment|DUI evaluation|Justice system referrals",
    county="Florence", served_counties="Florence|Darlington|Marion|Dillon|Marlboro|Chesterfield|Williamsburg", coverage="multi",
    _source="https://keystonesc.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="New Directions — Myrtle Beach",
    category="reentry-organizations", region="Myrtle Beach / Horry County",
    description="New Directions provides reentry case management, employment coaching, and housing navigation for justice-involved adults returning to Horry County including the Myrtle Beach and Conway areas after release from J. Reuben Long Detention Center or SCDC custody. Staff coordinate with SC Works Coastal, Helping Hand, and Grand Strand employers for fair-chance hiring.",
    description_es="New Directions ofrece manejo de casos de reinserción, coaching de empleo y navegación de vivienda para adultos con antecedentes penales que regresan al condado Horry incluyendo las áreas de Myrtle Beach y Conway después de la liberación.",
    address="1010 5th Avenue North", city="Myrtle Beach", phone="843-839-0130", email="",
    website="https://newdirectionsmb.org",
    eligibility="Justice-involved adults in Horry County within 12 months of release; referral from SCDPPPS or self-referral.",
    eligibility_es="Adultos con antecedentes penales en el condado Horry dentro de 12 meses de la liberación; referencia de SCDPPPS o autorreferencia.",
    notes="Call 843-839-0130 for intake; pairs with Helping Hand of Myrtle Beach and SC Works Conway.",
    notes_es="Llame al 843-839-0130 para admisión; se vincula con Helping Hand of Myrtle Beach y SC Works Conway.",
    hours="Monday–Friday business hours",
    tags="myrtle-beach|horry|reentry|employment|housing|reentry-organizations",
    services="Reentry case management|Employment coaching|Housing navigation|Benefits enrollment|Employer connections",
    county="Horry", served_counties="Horry", coverage="single",
    _source="https://newdirectionsmb.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Helping Hand of Myrtle Beach",
    category="basic-needs", region="Myrtle Beach / Horry County",
    description="Helping Hand of Myrtle Beach provides emergency food, clothing, utility assistance, and referral navigation for low-income Horry County residents including returning citizens reestablishing basic needs after incarceration. The day-services center offers showers, mail receipt, and connections to Grand Strand housing and employment partners.",
    description_es="Helping Hand of Myrtle Beach ofrece alimentos de emergencia, ropa, asistencia con servicios públicos y navegación de referencias para residentes de bajos ingresos del condado Horry incluidos ciudadanos que regresan que reestablecen necesidades básicas después de la encarcelación.",
    address="1411 Osceola Street", city="Myrtle Beach", phone="843-448-0000", email="",
    website="https://helpinghandofmyrtlebeach.org",
    eligibility="Low-income Horry County residents; proof of residency and income may be required for utility assistance.",
    eligibility_es="Residentes de bajos ingresos del condado Horry; puede requerirse prueba de residencia e ingresos para asistencia con servicios públicos.",
    notes="Call 843-448-0000 for assistance; food pantry hours posted online; pairs with New Directions and SC 211.",
    notes_es="Llame al 843-448-0000 para asistencia; horario de despensa publicado en línea; se vincula con New Directions y SC 211.",
    hours="Monday–Friday business hours; food pantry hours vary",
    tags="myrtle-beach|horry|basic-needs|food|utility-assistance|reentry",
    services="Emergency food|Clothing assistance|Utility assistance|Day services|Referral navigation",
    county="Horry", served_counties="Horry", coverage="single",
    _source="https://helpinghandofmyrtlebeach.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Keystone Substance Abuse Services — Rock Hill",
    category="substance-use-treatment", region="Rock Hill / York County",
    description="Keystone Substance Abuse Services operates a York County outpatient clinic in Rock Hill providing counseling, intensive outpatient treatment, and medication-assisted treatment for justice-involved adults under SCDPPPS supervision in York, Lancaster, and Chester counties. The clinic accepts Medicaid and offers sliding-fee services for uninsured clients reestablishing recovery after release.",
    description_es="Keystone Substance Abuse Services opera una clínica ambulatoria del condado York en Rock Hill que ofrece consejería, tratamiento intensivo ambulatorio y tratamiento asistido con medicamentos para adultos con antecedentes penales bajo supervisión SCDPPPS en los condados York, Lancaster y Chester.",
    address="1308 Ebenezer Road", city="Rock Hill", phone="803-324-1800", email="",
    website="https://keystonesc.org",
    eligibility="Adults with substance use disorders in York County and surrounding areas; Medicaid and sliding-fee accepted; SCDPPPS referrals welcome.",
    eligibility_es="Adultos con trastornos por uso de sustancias en el condado York y áreas circundantes; se aceptan Medicaid y tarifa móvil; referencias SCDPPPS bienvenidas.",
    notes="Call 803-324-1800 for Rock Hill clinic intake; MAT program available; pairs with SC CARES Rock Hill and Catawba Community Action.",
    notes_es="Llame al 803-324-1800 para admisión en clínica de Rock Hill; programa MAT disponible; se vincula con SC CARES Rock Hill y Catawba Community Action.",
    hours="Monday–Friday clinic hours",
    tags="rock-hill|york|substance-use-treatment|MAT|outpatient|reentry",
    services="Outpatient counseling|Intensive outpatient|Medication-assisted treatment|SCDPPPS coordination|Sliding-fee care",
    county="York", served_counties="York|Lancaster|Chester", coverage="multi",
    _source="https://keystonesc.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Catawba Community Action Agency — Rock Hill",
    category="basic-needs", region="Rock Hill / York County",
    description="Catawba Community Action Agency serves York, Lancaster, and Chester counties with emergency assistance for rent, utilities, and food plus weatherization, Head Start, and workforce development programs for low-income families including justice-involved households. Staff connect clients to SC Works Rock Hill, DSS benefits, and local housing partners in the Charlotte metro South Carolina corridor.",
    description_es="Catawba Community Action Agency sirve a los condados York, Lancaster y Chester con asistencia de emergencia para renta, servicios públicos y alimentos además de climatización, Head Start y programas de desarrollo de la fuerza laboral para familias de bajos ingresos incluidos hogares con antecedentes penales.",
    address="1136 Saluda Street", city="Rock Hill", phone="803-327-2101", email="",
    website="https://catawbaccaa.org",
    eligibility="Low-income residents of York, Lancaster, and Chester counties; income documentation required for emergency assistance programs.",
    eligibility_es="Residentes de bajos ingresos de los condados York, Lancaster y Chester; se requiere documentación de ingresos para programas de asistencia de emergencia.",
    notes="Call 803-327-2101 for intake; emergency assistance by appointment; pairs with Keystone and SC CARES Rock Hill.",
    notes_es="Llame al 803-327-2101 para admisión; asistencia de emergencia con cita; se vincula con Keystone y SC CARES Rock Hill.",
    hours="Monday–Friday business hours",
    tags="rock-hill|york|basic-needs|community-action|emergency-assistance|reentry",
    services="Emergency rent assistance|Utility assistance|Food aid|Weatherization|Workforce development",
    county="York", served_counties="York|Lancaster|Chester", coverage="multi",
    _source="https://catawbaccaa.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Harvest Hope Food Bank — Midlands",
    category="food-nutrition", region="Columbia / Midlands",
    description="Harvest Hope Food Bank distributes food through partner agencies and direct programs across 20 Midlands and Pee Dee counties including Richland, Lexington, Sumter, and Orangeburg. Returning citizens reestablishing food security can locate partner pantries online and access mobile pantry schedules serving justice-involved communities near Columbia and Florence.",
    description_es="Harvest Hope Food Bank distribuye alimentos a través de agencias aliadas y programas directos en 20 condados de Midlands y Pee Dee incluyendo Richland, Lexington, Sumter y Orangeburg. Los ciudadanos que regresan pueden localizar despensas aliadas en línea y acceder a horarios de despensas móviles.",
    address="2228 Shop Road", city="Columbia", phone="803-254-4432", email="",
    website="https://harvesthope.org",
    eligibility="Food-insecure residents of Midlands and Pee Dee service counties; partner agency registration requirements vary.",
    eligibility_es="Residentes con inseguridad alimentaria de condados de servicio de Midlands y Pee Dee; los requisitos de registro en agencias aliadas varían.",
    notes="Find food at harvesthope.org/find-food; Columbia warehouse 803-254-4432; Florence branch serves Pee Dee region.",
    notes_es="Encuentre alimentos en harvesthope.org/find-food; almacén de Columbia 803-254-4432; sucursal de Florence sirve región Pee Dee.",
    hours="Warehouse Monday–Friday; partner pantry hours vary",
    tags="columbia|midlands|food-nutrition|food-bank|pee-dee|reentry",
    services="Food distribution|Partner agency network|Mobile food pantry|SNAP outreach|Emergency food boxes",
    county="Richland", served_counties="Richland|Lexington|Sumter|Orangeburg|Calhoun|Fairfield|Kershaw|Lee|Clarendon", coverage="multi",
    _source="https://harvesthope.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="SC Works — Charleston Center",
    category="employment", region="Charleston / Tri-County",
    description="The SC Works Charleston center connects Tri-County job seekers including justice-involved adults from Charleston County Detention Center and SCDC release to resume coaching, WIOA training referrals, and fair-chance employer partnerships. Staff coordinate with Turning Leaf, One80 Place, and Lowcountry employers for returning citizens rebuilding work histories in Berkeley, Charleston, and Dorchester counties.",
    description_es="El centro SC Works de Charleston conecta buscadores de empleo del Tri-County incluidos adultos con antecedentes penales de la cárcel del condado Charleston y liberación de SCDC con coaching de currículum, referencias de capacitación WIOA y alianzas de empleadores de segunda oportunidad.",
    address="1930 Hanahan Road", city="North Charleston", phone="843-574-1800", email="",
    website="https://www.scworks.org",
    eligibility="Open to Tri-County job seekers including justice-involved individuals; core SC Works services are free.",
    eligibility_es="Abierto a buscadores de empleo del Tri-County incluidas personas con antecedentes penales; servicios básicos de SC Works son gratuitos.",
    notes="Register at scworks.org; call 843-574-1800; co-located with Trident Workforce Development Board services.",
    notes_es="Regístrese en scworks.org; llame al 843-574-1800; ubicado con servicios de la Junta de Desarrollo de la Fuerza Laboral Trident.",
    hours="Monday–Friday business hours",
    tags="charleston|employment|SC-Works|WIOA|fair-chance|reentry",
    services="Job search assistance|Resume coaching|WIOA training referrals|Fair-chance employer connections|Career workshops",
    county="Charleston", served_counties="Berkeley|Charleston|Dorchester", coverage="multi",
    _source="https://www.scworks.org", _source_type="government", _confidence="high",
)
add(
    name="SC Works — Greenville Center",
    category="employment", region="Greenville / Upstate",
    description="The SC Works Greenville center on Pelham Road provides free employment services for Upstate job seekers including justice-involved adults under SCDPPPS supervision in Greenville, Spartanburg, and Anderson counties. Career coaches offer resume assistance, skills assessments, WIOA training referrals, and connections to fair-chance employers coordinated with ROAR and United Housing Connections.",
    description_es="El centro SC Works de Greenville en Pelham Road brinda servicios de empleo gratuitos para buscadores de empleo del Upstate incluidos adultos con antecedentes penales bajo supervisión SCDPPPS en los condados Greenville, Spartanburg y Anderson.",
    address="1400 Pelham Road", city="Greenville", phone="864-271-4825", email="",
    website="https://www.scworks.org",
    eligibility="Open to Upstate job seekers including justice-involved individuals; veterans receive priority services.",
    eligibility_es="Abierto a buscadores de empleo del Upstate incluidas personas con antecedentes penales; veteranos reciben servicios prioritarios.",
    notes="Register at scworks.org; call 864-271-4825; Upstate Workforce Board partner location.",
    notes_es="Regístrese en scworks.org; llame al 864-271-4825; ubicación aliada de la Junta de Fuerza Laboral del Upstate.",
    hours="Monday–Friday business hours",
    tags="greenville|employment|SC-Works|WIOA|fair-chance|reentry",
    services="Career coaching|Resume assistance|Skills assessments|WIOA referrals|Veteran employment services",
    county="Greenville", served_counties="Greenville", coverage="single",
    _source="https://www.scworks.org", _source_type="government", _confidence="high",
)
add(
    name="SC Works — Rock Hill Center",
    category="employment", region="Rock Hill / York County",
    description="The SC Works Rock Hill center on Oakland Avenue connects York, Lancaster, and Chester county job seekers including justice-involved adults to career coaching, on-the-job training referrals, and fair-chance employment navigation. Staff coordinate with Keystone, Catawba Community Action, and SC CARES Rock Hill for returning citizens rebuilding employment after release from York County Detention Center.",
    description_es="El centro SC Works de Rock Hill en Oakland Avenue conecta buscadores de empleo de los condados York, Lancaster y Chester incluidos adultos con antecedentes penales con coaching de carrera, referencias de capacitación en el trabajo y navegación de empleo de segunda oportunidad.",
    address="2045 Oakland Avenue", city="Rock Hill", phone="803-324-4030", email="",
    website="https://www.scworks.org",
    eligibility="Open to York County area job seekers including justice-involved individuals; core services free.",
    eligibility_es="Abierto a buscadores de empleo del área del condado York incluidas personas con antecedentes penales; servicios básicos gratuitos.",
    notes="Register at scworks.org; call 803-324-4030; Catawba Workforce Development Board partner.",
    notes_es="Regístrese en scworks.org; llame al 803-324-4030; aliado de la Junta de Desarrollo de la Fuerza Laboral Catawba.",
    hours="Monday–Friday business hours",
    tags="rock-hill|york|employment|SC-Works|WIOA|fair-chance|reentry",
    services="Career coaching|On-the-job training referrals|Job search assistance|Fair-chance employment|Workshop programs",
    county="York", served_counties="York|Lancaster|Chester", coverage="multi",
    _source="https://www.scworks.org", _source_type="government", _confidence="high",
)

# --- County benefits + expansion modules ---
from county_benefits_registry import register_county_benefits_south_carolina

_existing_fa = {
    e["county"]
    for e in ENTRIES
    if e["category"] == "financial-assistance" and e.get("county")
}
register_county_benefits_south_carolina(add, _existing_fa)

from south_carolina_phase4_expansion import register_phase4
register_phase4(add)

from south_carolina_category_fill import register_category_fill
register_category_fill(add)

from south_carolina_thin_counties import register_thin_counties
register_thin_counties(add)


def _dedupe_entries(entries: list[dict]) -> list[dict]:
    """Keep one row per (name, county); prefer wider served_counties and fuller address."""
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
