#!/usr/bin/env python3
"""Generate virginia-resources.csv and virginia-research-log.csv.

RESOURCES_UUID_PREFIX comment da000001
"""
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES_PATH = ROOT / "data" / "virginia-resources.csv"
LOG_PATH = ROOT / "data" / "virginia-research-log.csv"
DATE = "2026-07-04"

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
    name="VADOC — Reentry & Reintegration Services",
    category="state-agency", region="Statewide",
    description="The Virginia Department of Corrections coordinates statewide reentry planning that begins at intake and continues through release and community supervision. Reentry staff connect people leaving state custody to housing options, Medicaid enrollment, DMV Connect ID services, employment programs, and local reentry councils across Virginia. This office provides planning, programming, and referrals—not a walk-in crisis line or emergency cash assistance.",
    description_es="El Departamento de Correcciones de Virginia coordina la planificación estatal de reinserción que comienza al ingreso y continúa durante la liberación y la supervisión comunitaria. El personal de reinserción conecta a las personas que salen de custodia estatal con vivienda, inscripción en Medicaid, servicios de identificación DMV Connect, programas de empleo y consejos locales de reinserción en toda Virginia. Esta oficina ofrece planificación y referencias, no es una línea de crisis ni asistencia de efectivo de emergencia.",
    address="6900 Atmore Drive", city="Richmond", phone="804-674-3000", email="",
    website="https://vadoc.virginia.gov/inmates-and-supervisees/reentry-resources/",
    eligibility="People in VADOC custody, preparing for release, or under VADOC community supervision; families and community partners may use the published reentry resources.",
    eligibility_es="Personas en custodia de VADOC, preparándose para la liberación o bajo supervisión comunitaria de VADOC; las familias y los aliados comunitarios pueden usar los recursos publicados de reinserción.",
    notes="Review the Reentry Resource Packet and Pathway to Benefits brochure on the VADOC website; coordinate through your facility reentry staff or assigned probation officer; dial 211 for local referrals.",
    notes_es="Revise el Paquete de Recursos de Reinserción y el folleto Pathway to Benefits en el sitio web de VADOC; coordine con el personal de reinserción de su instalación o su oficial de probatoria; marque 211 para referencias locales.",
    hours="State office Monday–Friday business hours",
    tags="statewide|reentry|VADOC|DOC|pre-release|parole|probation",
    services="Pre-release reentry planning|Medicaid enrollment coordination|DMV Connect ID scheduling|Local reentry council connections|Community partner referrals",
    county="Richmond City", served_counties="", coverage="statewide",
    _source="https://vadoc.virginia.gov/inmates-and-supervisees/reentry-resources/", _source_type="government", _confidence="high",
)
add(
    name="VADOC — Probation & Parole District Offices",
    category="probation-parole", region="Statewide",
    description="The Virginia Department of Corrections Division of Community Corrections supervises people on probation and parole through 43 probation and parole district offices that together cover every Virginia city and county. District officers complete risk and needs assessments, refer supervisees to substance use treatment, mental health care, employment services, and housing, and coordinate Community Corrections Alternative Programs and reentry probation seminars for people returning from prison.",
    description_es="La División de Correcciones Comunitarias del Departamento de Correcciones de Virginia supervisa a personas en probatoria y libertad condicional a través de 43 oficinas de distrito que en conjunto cubren cada ciudad y condado de Virginia. Los oficiales de distrito realizan evaluaciones de riesgo y necesidades, refieren a tratamiento de uso de sustancias, salud mental, empleo y vivienda, y coordinan los Programas Alternativos de Correcciones Comunitarias.",
    address="6900 Atmore Drive", city="Richmond", phone="804-674-3000", email="",
    website="https://vadoc.virginia.gov/inmates-and-supervisees/community-supervision/",
    eligibility="Virginians under VADOC community supervision (probation, parole, or post-release supervision) assigned to a district office by the court or the department.",
    eligibility_es="Virginianos bajo supervisión comunitaria de VADOC (probatoria, libertad condicional o supervisión posterior a la liberación) asignados a una oficina de distrito por el tribunal o el departamento.",
    notes="Find your assigned district office through the VADOC website locations directory; report as directed by your supervision officer; ask your officer about treatment, employment, and housing referrals.",
    notes_es="Encuentre su oficina de distrito asignada en el directorio del sitio web de VADOC; repórtese según lo indique su oficial de supervisión; pregunte a su oficial sobre referencias de tratamiento, empleo y vivienda.",
    hours="District offices Monday–Friday business hours",
    tags="statewide|probation|parole|supervision|VADOC|reentry",
    services="Community supervision|Risk and needs assessment|Treatment referrals|Employment and housing referrals|Reentry probation seminars",
    county="Richmond City", served_counties="", coverage="statewide",
    _source="https://vadoc.virginia.gov/inmates-and-supervisees/community-supervision/", _source_type="government", _confidence="high",
)
add(
    name="CommonHelp — Virginia Benefits Portal",
    category="financial-assistance", region="Statewide",
    description="CommonHelp is Virginia's official online portal for screening, applying for, and managing SNAP food assistance, Medicaid and other health coverage, TANF cash assistance, child care assistance, and energy assistance administered through local departments of social services. People returning from incarceration can apply for food and health benefits online after release, and account holders can upload documents, report changes, and track renewals in one place.",
    description_es="CommonHelp es el portal oficial en línea de Virginia para evaluar, solicitar y administrar asistencia alimentaria SNAP, Medicaid y otra cobertura de salud, asistencia en efectivo TANF, asistencia de cuidado infantil y asistencia de energía administradas por los departamentos locales de servicios sociales. Las personas que regresan de la encarcelación pueden solicitar beneficios de alimentos y salud en línea después de la liberación, subir documentos, reportar cambios y seguir renovaciones.",
    address="", city="", phone="855-635-4370", email="", website="https://commonhelp.virginia.gov",
    eligibility="Virginia residents who meet income and household requirements for SNAP, Medicaid, TANF, child care, or energy assistance; a criminal record is generally not a barrier to SNAP or Medicaid in Virginia.",
    eligibility_es="Residentes de Virginia que cumplan los requisitos de ingresos y hogar para SNAP, Medicaid, TANF, cuidado infantil o asistencia de energía; los antecedentes penales generalmente no son una barrera para SNAP o Medicaid en Virginia.",
    notes="Apply online at commonhelp.virginia.gov or call the Enterprise Customer Service Center at 855-635-4370 (Mon–Fri 7 a.m.–6 p.m.); for health coverage help call Cover Virginia at 833-522-5582; paper applications are accepted at local DSS offices.",
    notes_es="Solicite en commonhelp.virginia.gov o llame al Centro de Servicio al Cliente al 855-635-4370 (lun–vie 7 a.m.–6 p.m.); para ayuda con cobertura de salud llame a Cover Virginia al 833-522-5582; las oficinas locales de DSS aceptan solicitudes en papel.",
    hours="Online 24/7; phone support Monday–Friday, 7:00 a.m.–6:00 p.m.",
    tags="statewide|benefits|SNAP|Medicaid|TANF|online|reentry",
    services="SNAP application|Medicaid and health coverage application|TANF cash assistance application|Child care assistance|Benefits account management",
    county="", served_counties="", coverage="statewide",
    _source="https://commonhelp.virginia.gov", _source_type="government", _confidence="high",
)
add(
    name="Virginia Department of Social Services — Local DSS Offices",
    category="financial-assistance", region="Statewide",
    description="The Virginia Department of Social Services administers SNAP, TANF, Medicaid intake, energy assistance, and child care assistance through 120 local departments of social services serving all 133 Virginia cities and counties. Returning citizens can apply in person at their local DSS office with help verifying identity and income, and VADOC reentry staff coordinate benefit applications with local departments before release. VDSS is a benefits agency—not a housing or crisis provider.",
    description_es="El Departamento de Servicios Sociales de Virginia administra SNAP, TANF, la admisión de Medicaid, asistencia de energía y asistencia de cuidado infantil a través de 120 departamentos locales que sirven a las 133 ciudades y condados de Virginia. Los ciudadanos que regresan pueden solicitar en persona en su oficina local de DSS con ayuda para verificar identidad e ingresos. VDSS es una agencia de beneficios, no un proveedor de vivienda ni de crisis.",
    address="801 East Main Street", city="Richmond", phone="804-726-7000", email="",
    website="https://www.dss.virginia.gov",
    eligibility="Virginia residents who meet program income and household-size requirements; bring identification and release paperwork if recently released from incarceration.",
    eligibility_es="Residentes de Virginia que cumplan los requisitos de ingresos y tamaño del hogar del programa; traiga identificación y documentos de liberación si fue liberado recientemente.",
    notes="Use the 'Find my local department' tool at dss.virginia.gov to locate your city or county office; apply online through CommonHelp to avoid a first trip; call 804-726-7000 for help finding the right contact.",
    notes_es="Use la herramienta 'Find my local department' en dss.virginia.gov para ubicar su oficina local; solicite en línea mediante CommonHelp para evitar un primer viaje; llame al 804-726-7000 para encontrar el contacto correcto.",
    hours="Local office hours vary; typically Monday–Friday business hours",
    tags="statewide|benefits|SNAP|TANF|Medicaid|DSS|reentry",
    services="SNAP intake|TANF intake|Medicaid application assistance|Energy assistance|Document verification",
    county="Richmond City", served_counties="", coverage="statewide",
    _source="https://www.dss.virginia.gov/general-info/contact-us/", _source_type="government", _confidence="high",
)
add(
    name="211 Virginia",
    category="state-agency", region="Statewide",
    description="211 Virginia is a free, confidential, 24/7 information and referral service operated by the Virginia Department of Social Services that connects residents to housing, food, utility help, employment, health care, and reentry programs across the Commonwealth. Trained specialists search a database of more than 20,000 listings by ZIP code, with live help in English and Spanish and interpretation in over 150 languages. 211 Virginia is a referral service—not a direct-service provider.",
    description_es="211 Virginia es un servicio gratuito y confidencial de información y referencia, disponible 24/7, operado por el Departamento de Servicios Sociales de Virginia, que conecta a los residentes con vivienda, alimentos, ayuda con servicios públicos, empleo, atención médica y programas de reinserción en todo el estado. Especialistas capacitados buscan en una base de datos de más de 20,000 listados por código postal, con ayuda en inglés y español. Es un servicio de referencia, no un proveedor directo.",
    address="", city="", phone="211", email="", website="https://211virginia.org",
    eligibility="Open to anyone in Virginia; no criminal-record restrictions stated.",
    eligibility_es="Abierto a cualquier persona en Virginia; sin restricciones de antecedentes penales indicadas.",
    notes="Dial 211 from any Virginia phone; text CONNECT to 247211; chat or search online at 211virginia.org; from outside Virginia call 1-800-230-6977.",
    notes_es="Marque 211 desde cualquier teléfono en Virginia; envíe CONNECT por texto al 247211; chatee o busque en 211virginia.org; desde fuera de Virginia llame al 1-800-230-6977.",
    hours="Available 24/7, 365 days a year",
    tags="statewide|hotline|211|referral-only|basic-needs|reentry",
    services="Information and referral|Housing resource navigation|Food and utility referrals|Reentry program referrals|Crisis resource connections",
    county="", served_counties="", coverage="statewide",
    _source="https://211virginia.org/about-us/", _source_type="government", _confidence="high",
)
add(
    name="Virginia Legal Aid Network — Statewide Intake (VaLegalAid.org)",
    category="legal-aid", region="Statewide",
    description="Virginia's nine regional legal aid programs provide free civil legal help to low-income Virginians with housing, public benefits, family law, consumer, and criminal record matters including expungement and the record sealing process taking effect July 1, 2026. The statewide helpline at 1-866-LEGLAID routes callers to the legal aid office serving their city or county, and VaLegalAid.org publishes self-help guides. Legal aid programs handle civil matters—not criminal defense.",
    description_es="Los nueve programas regionales de asistencia legal de Virginia ofrecen ayuda legal civil gratuita a virginianos de bajos ingresos con vivienda, beneficios públicos, derecho familiar, asuntos de consumidor y antecedentes penales, incluida la expungación y el proceso de sellado de antecedentes vigente desde el 1 de julio de 2026. La línea estatal 1-866-LEGLAID dirige a la oficina que sirve su ciudad o condado. Los programas atienden asuntos civiles, no defensa penal.",
    address="", city="", phone="1-866-534-5243", email="", website="https://www.valegalaid.org",
    eligibility="Low-income Virginia residents; LSC income limits generally apply; each regional program serves specific cities and counties listed on valegalaid.org.",
    eligibility_es="Residentes de Virginia de bajos ingresos; generalmente aplican límites de ingresos LSC; cada programa regional sirve ciudades y condados específicos listados en valegalaid.org.",
    notes="Call 1-866-LEGLAID (1-866-534-5243) to be connected to your local legal aid office; browse self-help guides at valegalaid.org; automatic sealing of certain records begins July 1, 2026 with petition sealing also available.",
    notes_es="Llame al 1-866-LEGLAID (1-866-534-5243) para conectarse con su oficina local de asistencia legal; consulte guías de autoayuda en valegalaid.org; el sellado automático de ciertos antecedentes comienza el 1 de julio de 2026, y también hay sellado por petición.",
    hours="Helpline available during business hours; online resources 24/7",
    tags="statewide|legal-aid|expungement|record-sealing|hotline|low-income",
    services="Legal aid office routing|Expungement information|Record sealing guidance|Housing legal help referrals|Benefits advocacy referrals",
    county="", served_counties="", coverage="statewide",
    _source="https://www.valegalaid.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Virginia Poverty Law Center",
    category="legal-aid", region="Statewide",
    description="The Virginia Poverty Law Center is a statewide advocacy organization that supports Virginia's legal aid network with policy work, litigation, and free specialized helplines covering SNAP benefits, health coverage enrollment, utilities, predatory loans, and eviction defense tools. VPLC generally does not provide direct legal representation; it connects low-income Virginians—including people with criminal records—to their regional legal aid office and to self-help legal resources.",
    description_es="El Virginia Poverty Law Center es una organización estatal de defensa que apoya la red de asistencia legal de Virginia con trabajo de políticas, litigio y líneas de ayuda gratuitas especializadas en beneficios SNAP, inscripción en cobertura de salud, servicios públicos, préstamos abusivos y herramientas contra desalojos. VPLC generalmente no ofrece representación legal directa; conecta a virginianos de bajos ingresos, incluidas personas con antecedentes penales, con su oficina regional de asistencia legal.",
    address="919 East Main Street, Suite 610", city="Richmond", phone="804-782-9430", email="info@vplc.org",
    website="https://www.vplc.org",
    eligibility="Low-income Virginians seeking help with benefits, health coverage, utilities, predatory loans, or referrals to regional legal aid; direct representation only in limited referred matters.",
    eligibility_es="Virginianos de bajos ingresos que buscan ayuda con beneficios, cobertura de salud, servicios públicos, préstamos abusivos o referencias a asistencia legal regional; representación directa solo en asuntos limitados referidos.",
    notes="Call the VPLC helpline at 1-800-868-8752; SNAP helpline 866-753-7627; Enroll Virginia health coverage helpline 888-392-5132; for representation call 1-866-534-5243 to find your local legal aid office.",
    notes_es="Llame a la línea de VPLC al 1-800-868-8752; línea SNAP 866-753-7627; línea de cobertura de salud Enroll Virginia 888-392-5132; para representación llame al 1-866-534-5243 y encuentre su oficina local de asistencia legal.",
    hours="Monday–Friday business hours; helpline hours vary",
    tags="statewide|legal-aid|benefits|advocacy|helpline|referral-only",
    services="SNAP benefits helpline|Health coverage enrollment help|Utility assistance helpline|Predatory loan helpline|Legal aid referrals",
    county="Richmond City", served_counties="", coverage="statewide",
    _source="https://www.vplc.org/get-legal-help/", _source_type="nonprofit", _confidence="high",
)
add(
    name="Virginia Works — Virginia Career Works Centers",
    category="employment", region="Statewide",
    description="Virginia Works is the Commonwealth's workforce development agency, operating the Virginia Career Works network of American Job Centers through 15 regional workforce boards. Centers offer free job search assistance, career coaching, WIOA-funded training referrals, apprenticeship connections, and hiring events open to justice-involved job seekers, plus employer incentives such as the Work Opportunity Tax Credit that support fair-chance hiring across Virginia.",
    description_es="Virginia Works es la agencia de desarrollo de la fuerza laboral del estado y opera la red Virginia Career Works de Centros de Empleo Americanos a través de 15 juntas regionales. Los centros ofrecen ayuda gratuita para buscar empleo, orientación profesional, referencias a capacitación financiada por WIOA, conexiones con aprendizajes y ferias de contratación abiertas a buscadores de empleo con antecedentes penales, además de incentivos para empleadores que apoyan la contratación de segunda oportunidad.",
    address="", city="", phone="", email="", website="https://virginiacareerworks.com",
    eligibility="Open to Virginia job seekers including people with criminal records; core career center services are free; WIOA training eligibility is determined at your local center.",
    eligibility_es="Abierto a buscadores de empleo de Virginia, incluidas personas con antecedentes penales; los servicios básicos del centro son gratuitos; la elegibilidad para capacitación WIOA se determina en su centro local.",
    notes="Find your nearest center with the locator at virginiacareerworks.com/locations; register for job listings on the Virginia Workforce Connection; ask center staff about fair-chance employers and federal bonding.",
    notes_es="Encuentre su centro más cercano en virginiacareerworks.com/locations; regístrese para ofertas de empleo en Virginia Workforce Connection; pregunte al personal sobre empleadores de segunda oportunidad y fianzas federales.",
    hours="Center hours vary; typically Monday–Friday business hours",
    tags="statewide|employment|workforce|WIOA|fair-chance|reentry",
    services="Job search assistance|Career coaching|WIOA training referrals|Apprenticeship connections|Hiring events",
    county="", served_counties="", coverage="statewide",
    _source="https://virginiacareerworks.com/locations/", _source_type="government", _confidence="high",
)
add(
    name="Virginia DARS — Vocational Rehabilitation",
    category="employment", region="Statewide",
    description="The Virginia Department for Aging and Rehabilitative Services helps Virginians with disabilities—including justice-involved people with qualifying physical or mental health disabilities—prepare for, find, and keep employment. Vocational rehabilitation counselors at field offices statewide arrange evaluation, counseling, skills training, job placement, and supports such as the Wilson Workforce and Rehabilitation Center, working through roughly 85 approved community rehabilitation providers.",
    description_es="El Departamento de Servicios para Personas Mayores y de Rehabilitación de Virginia ayuda a virginianos con discapacidades—incluidas personas con antecedentes penales y discapacidades físicas o de salud mental calificadas—a prepararse para el empleo, encontrarlo y mantenerlo. Los consejeros de rehabilitación vocacional en oficinas de campo en todo el estado organizan evaluación, consejería, capacitación, colocación laboral y apoyos a través de unos 85 proveedores comunitarios aprobados.",
    address="5620 Cox Road", city="Glen Allen", phone="800-552-5019", email="",
    website="https://dars.virginia.gov/about/divisions/rehabilitative-services/",
    eligibility="Virginia residents with a physical or mental disability that creates a barrier to employment; eligibility determined through DARS assessment; self-referrals accepted.",
    eligibility_es="Residentes de Virginia con una discapacidad física o mental que crea una barrera para el empleo; la elegibilidad se determina mediante evaluación de DARS; se aceptan autorreferencias.",
    notes="Call 800-552-5019 or contact your nearest DARS field office to start an application; dial 711 for relay services; DARS coordinates with Virginia Career Works centers on shared cases.",
    notes_es="Llame al 800-552-5019 o contacte su oficina de campo de DARS más cercana para iniciar una solicitud; marque 711 para servicios de retransmisión; DARS coordina con los centros Virginia Career Works.",
    hours="Field offices Monday–Friday business hours",
    tags="statewide|employment|disability|vocational-rehabilitation|DARS|reentry",
    services="Vocational counseling|Skills training|Job placement|Assistive technology|Employer partnerships",
    county="Henrico", served_counties="", coverage="statewide",
    _source="https://www.dars.virginia.gov/ContactUs.htm", _source_type="government", _confidence="high",
)
add(
    name="Virginia Community Services Boards (DBHDS Network)",
    category="healthcare", region="Statewide",
    description="Virginia's 40 community services boards are the single points of entry into publicly funded mental health, developmental disability, and substance use disorder services, together covering all 133 cities and counties. Under the STEP-VA initiative, CSBs offer same-day mental health assessment, outpatient treatment, case management, and crisis services, and many operate jail-based and reentry-focused behavioral health programs. Find your CSB by locality through the DBHDS website.",
    description_es="Las 40 juntas de servicios comunitarios de Virginia son los puntos únicos de entrada a los servicios públicos de salud mental, discapacidades del desarrollo y trastornos por uso de sustancias, y en conjunto cubren las 133 ciudades y condados. Bajo la iniciativa STEP-VA, las CSB ofrecen evaluación de salud mental el mismo día, tratamiento ambulatorio, manejo de casos y servicios de crisis, y muchas operan programas conductuales en cárceles y enfocados en la reinserción.",
    address="", city="", phone="", email="", website="https://dbhds.virginia.gov/find-help/",
    eligibility="Open to residents of each CSB's catchment area; publicly funded services are available regardless of ability to pay, with sliding fees and Medicaid accepted.",
    eligibility_es="Abierto a residentes del área de cobertura de cada CSB; los servicios con fondos públicos están disponibles independientemente de la capacidad de pago, con tarifas móviles y Medicaid aceptado.",
    notes="Use the 'Find your CSB' tool at dbhds.virginia.gov/find-help or the directory at vacsb.org/csb-bha-directory; for behavioral health crises call or text 988 any time.",
    notes_es="Use la herramienta 'Find your CSB' en dbhds.virginia.gov/find-help o el directorio en vacsb.org/csb-bha-directory; para crisis de salud conductual llame o envíe un texto al 988 en cualquier momento.",
    hours="CSB hours vary by locality; crisis services 24/7 via 988",
    tags="statewide|healthcare|mental-health|substance-use|CSB|STEP-VA|reentry",
    services="Same-day mental health assessment|Outpatient behavioral health treatment|Substance use disorder services|Case management|Crisis services",
    county="", served_counties="", coverage="statewide",
    _source="https://dbhds.virginia.gov/find-help/", _source_type="government", _confidence="high",
)
add(
    name="988 Suicide & Crisis Lifeline — Virginia",
    category="healthcare", region="Statewide",
    description="Free, confidential crisis support available 24/7 for anyone in Virginia experiencing a mental health emergency, suicidal thoughts, or a substance use crisis. Trained crisis counselors provide immediate phone and text support and can connect callers to local community services board crisis teams and mobile crisis response. Available to everyone—not reentry-specific, but an essential safety net for justice-involved Virginians and their families in crisis.",
    description_es="Apoyo de crisis gratuito y confidencial disponible 24/7 para cualquier persona en Virginia que experimente una emergencia de salud mental, pensamientos suicidas o una crisis por uso de sustancias. Consejeros de crisis capacitados brindan apoyo inmediato por teléfono y texto y pueden conectar a los usuarios con equipos de crisis de las juntas de servicios comunitarios locales y respuesta móvil de crisis. Disponible para todos; esencial para personas con antecedentes penales y sus familias.",
    address="", city="", phone="988", email="", website="https://988lifeline.org",
    eligibility="Open to anyone in Virginia experiencing a mental health, suicide, or substance use crisis; no eligibility restrictions.",
    eligibility_es="Abierto a cualquier persona en Virginia en crisis de salud mental, suicidio o uso de sustancias; sin restricciones de elegibilidad.",
    notes="Call or text 988; Spanish-language support available; for immediate physical danger call 911.",
    notes_es="Llame o envíe un texto al 988; soporte en español disponible; para peligro físico inmediato llame al 911.",
    hours="Available 24/7",
    tags="statewide|hotline|crisis|mental-health|988",
    services="Crisis counseling|Suicide prevention support|Substance use crisis support|Local crisis team connections",
    county="", served_counties="", coverage="statewide",
    _source="https://988lifeline.org", _source_type="government", _confidence="high",
)
add(
    name="SAMHSA National Helpline — Virginia Treatment Referrals",
    category="substance-use-treatment", region="Statewide",
    description="Free, confidential 24/7 treatment referral and information service for individuals and families facing mental health or substance use disorders. Specialists refer callers to licensed treatment providers, community services boards, and recovery supports across Virginia, with Spanish-language support available. The helpline provides referrals and information only—it is not a counseling line and does not provide direct treatment.",
    description_es="Servicio gratuito y confidencial de referencia e información de tratamiento, disponible 24/7, para personas y familias con trastornos de salud mental o uso de sustancias. Los especialistas refieren a proveedores de tratamiento con licencia, juntas de servicios comunitarios y apoyos de recuperación en toda Virginia, con soporte en español disponible. La línea ofrece solo referencias e información; no brinda consejería ni tratamiento directo.",
    address="", city="", phone="800-662-4357", email="", website="https://www.samhsa.gov/find-help/national-helpline",
    eligibility="Open to anyone in the United States seeking substance use or mental health treatment information and referrals.",
    eligibility_es="Abierto a cualquier persona en Estados Unidos que busque información y referencias de tratamiento de uso de sustancias o salud mental.",
    notes="TTY 800-487-4889; search Virginia providers online at FindTreatment.gov and filter by MAT, outpatient, or residential care.",
    notes_es="TTY 800-487-4889; busque proveedores de Virginia en FindTreatment.gov y filtre por TMO, atención ambulatoria o residencial.",
    hours="Available 24/7",
    tags="statewide|hotline|substance-use|treatment-referral|national",
    services="Treatment referrals|Substance use information|Mental health resource navigation",
    county="", served_counties="", coverage="statewide",
    _source="https://www.samhsa.gov/find-help/national-helpline", _source_type="government", _confidence="high",
)
add(
    name="Virginia CARES, Inc.",
    category="reentry-organizations", region="Statewide",
    description="Virginia CARES (Community Action Reentry System) is a statewide network of community action agencies serving returning citizens since 1981, with pre-release programs in 15 prisons and 11 regional and local jails and post-release services in 43 Virginia localities. Local sites provide case management, job readiness training, peer support groups, emergency aid for food, clothing, transportation, and ID fees, and rights restoration help. Contact the central office to be routed to your local site.",
    description_es="Virginia CARES (Community Action Reentry System) es una red estatal de agencias de acción comunitaria que sirve a ciudadanos que regresan desde 1981, con programas previos a la liberación en 15 prisiones y 11 cárceles regionales y locales, y servicios posteriores en 43 localidades de Virginia. Los sitios locales ofrecen manejo de casos, preparación laboral, grupos de apoyo entre pares, ayuda de emergencia para alimentos, ropa, transporte y tarifas de identificación, y restauración de derechos.",
    address="108 Henry Street NW", city="Roanoke", phone="540-342-9344", email="",
    website="https://www.vacares.org",
    eligibility="People incarcerated in Virginia state or federal prisons or local and regional jails, and people recently released who reside in Virginia; family members may also seek guidance.",
    eligibility_es="Personas encarceladas en prisiones estatales o federales de Virginia o en cárceles locales y regionales, y personas recién liberadas que residen en Virginia; los familiares también pueden buscar orientación.",
    notes="Call 540-342-9344 to find the Virginia CARES site serving your locality; phone referrals and walk-ins accepted at local sites; Spanish-language assistance available.",
    notes_es="Llame al 540-342-9344 para encontrar el sitio de Virginia CARES que sirve su localidad; los sitios locales aceptan referencias telefónicas y visitas sin cita; asistencia en español disponible.",
    hours="Central office Monday–Friday business hours; local site hours vary",
    tags="statewide|reentry|case-management|peer-support|employment|rights-restoration",
    services="Pre-release workshops|Post-release case management|Job readiness training|Emergency aid|Rights restoration assistance",
    county="Roanoke City", served_counties="", coverage="statewide",
    _source="https://www.vacares.org/history.html", _source_type="nonprofit", _confidence="high",
)
add(
    name="Virginia DMV — ID Cards & DMV Connect",
    category="id-documentation", region="Statewide",
    description="The Virginia Department of Motor Vehicles issues the state ID cards and driver's licenses needed for employment, housing, and benefits after release. Through the DMV Connect mobile program, DMV teams visit VADOC facilities so people can obtain a Virginia ID—including REAL ID—about six months before release, and DMV Connect also brings ID, vital records ordering, and license services to community sites statewide. Fees apply, with loans available for indigent individuals in custody.",
    description_es="El Departamento de Vehículos Motorizados de Virginia emite las tarjetas de identificación estatales y licencias de conducir necesarias para empleo, vivienda y beneficios después de la liberación. Mediante el programa móvil DMV Connect, equipos del DMV visitan las instalaciones de VADOC para que las personas obtengan una identificación de Virginia—incluida REAL ID—unos seis meses antes de la liberación, y también llevan servicios de identificación y registros vitales a sitios comunitarios. Aplican tarifas.",
    address="", city="", phone="", email="", website="https://www.dmv.virginia.gov/locations/mobile-offices",
    eligibility="Virginia residents with required identity and residency documents; people in VADOC custody are scheduled through facility staff; standard DMV fees apply.",
    eligibility_es="Residentes de Virginia con los documentos requeridos de identidad y residencia; las personas en custodia de VADOC se programan a través del personal de la instalación; aplican tarifas estándar del DMV.",
    notes="Find DMV Connect visit schedules and customer service centers at dmv.virginia.gov; bring a certified birth certificate or passport plus proof of Virginia residency; DMV Connect can also order Virginia vital records by mail.",
    notes_es="Encuentre los horarios de visitas de DMV Connect y los centros de servicio en dmv.virginia.gov; traiga un certificado de nacimiento certificado o pasaporte más prueba de residencia en Virginia; DMV Connect también puede ordenar registros vitales por correo.",
    hours="Customer service center and DMV Connect visit hours vary; check dmv.virginia.gov",
    tags="statewide|id-documentation|DMV|drivers-license|DMV-connect|reentry",
    services="State ID card issuance|REAL ID issuance|Driver's license services|Vital records ordering|Mobile ID visits at correctional facilities",
    county="", served_counties="", coverage="statewide",
    _source="https://www.dmv.virginia.gov/locations/mobile-offices", _source_type="government", _confidence="high",
)
add(
    name="Virginia Veteran & Family Support (VVFS) — Department of Veterans Services",
    category="veterans", region="Statewide",
    description="Virginia Veteran and Family Support is the Department of Veterans Services program that coordinates behavioral health, rehabilitative services, and community resources for veterans and their families statewide. Its Justice Involved Services program assigns Veteran Justice Specialists who connect justice-involved veterans—in veteran treatment court dockets, in jail or prison within 120 days of release, or on community supervision—to housing, employment, treatment, and VA benefits. VVFS is not a crisis line.",
    description_es="Virginia Veteran and Family Support es el programa del Departamento de Servicios para Veteranos que coordina salud conductual, servicios de rehabilitación y recursos comunitarios para veteranos y sus familias en todo el estado. Su programa de Servicios para Personas Involucradas con la Justicia asigna especialistas que conectan a veteranos con antecedentes penales—en tribunales de tratamiento, en cárcel o prisión dentro de 120 días de la liberación, o bajo supervisión—con vivienda, empleo, tratamiento y beneficios del VA. No es una línea de crisis.",
    address="101 North 14th Street", city="Richmond", phone="1-844-838-7838", email="",
    website="https://www.dvs.virginia.gov/benefits-services/veteran-and-family-support",
    eligibility="Virginia-resident veterans of any era regardless of discharge status, Virginia National Guard and Reserve members, transitioning service members, and their families and caregivers.",
    eligibility_es="Veteranos residentes de Virginia de cualquier época sin importar el tipo de baja, miembros de la Guardia Nacional y la Reserva de Virginia, militares en transición y sus familias y cuidadores.",
    notes="Request services at vvn.dvs.virginia.gov or call 1-844-838-7838; for the Justice Involved Services program call 804-225-4734 or email justice.vvfs@dvs.virginia.gov; in crisis call or text 988.",
    notes_es="Solicite servicios en vvn.dvs.virginia.gov o llame al 1-844-838-7838; para el programa de Servicios para Personas Involucradas con la Justicia llame al 804-225-4734 o escriba a justice.vvfs@dvs.virginia.gov; en crisis llame o envíe un texto al 988.",
    hours="Monday–Friday business hours; services available in person, by phone, and virtually",
    tags="statewide|veterans|justice-involved-veterans|VA-benefits|peer-support|reentry",
    services="Veteran Justice Specialist connections|Care coordination|Peer recovery support|VA benefits linkages|Housing and employment referrals",
    county="Richmond City", served_counties="", coverage="statewide",
    _source="https://www.dvs.virginia.gov/benefits-services/veteran-and-family-support/justice-involved-veteran-support", _source_type="government", _confidence="high",
)
add(
    name="Federation of Virginia Food Banks",
    category="food-nutrition", region="Statewide",
    description="The Federation of Virginia Food Banks is the Feeding America state association coordinating Virginia's seven regional food banks and more than 1,100 partner pantries and distribution sites across the Commonwealth. The federation supports food sourcing, SNAP outreach, and hunger advocacy so that every Virginia locality has access to a regional food bank network. The federation itself is a coordinating body—food is distributed through member food banks and their local partner agencies.",
    description_es="La Federación de Bancos de Alimentos de Virginia es la asociación estatal de Feeding America que coordina los siete bancos de alimentos regionales de Virginia y más de 1,100 despensas y sitios de distribución asociados en todo el estado. La federación apoya el abastecimiento de alimentos, la difusión de SNAP y la defensa contra el hambre para que cada localidad tenga acceso a una red regional. La federación es un ente coordinador; los alimentos se distribuyen mediante los bancos miembros y sus agencias locales.",
    address="", city="", phone="", email="", website="https://vafoodbanks.org",
    eligibility="Open to Virginians facing food insecurity through member food banks and partner pantries; pantry-level requirements vary by site.",
    eligibility_es="Abierto a virginianos con inseguridad alimentaria a través de los bancos de alimentos miembros y despensas asociadas; los requisitos varían según el sitio.",
    notes="Find your regional food bank at vafoodbanks.org; dial 211 to locate the nearest pantry; apply for SNAP through CommonHelp or call 855-635-4370.",
    notes_es="Encuentre su banco de alimentos regional en vafoodbanks.org; marque 211 para ubicar la despensa más cercana; solicite SNAP mediante CommonHelp o llame al 855-635-4370.",
    hours="Member food bank and pantry hours vary",
    tags="statewide|food-nutrition|food-bank|feeding-america|SNAP|referral-only",
    services="Regional food bank network|Partner pantry locator|SNAP outreach|Hunger relief coordination",
    county="", served_counties="", coverage="statewide",
    _source="https://vafoodbanks.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="SAARA of Virginia — Peer Recovery Support",
    category="peer-support", region="Statewide",
    description="SAARA of Virginia (Substance Abuse and Addiction Recovery Alliance) is the statewide recovery community organization providing peer-led recovery groups, warmline support, recovery advocacy, and training for Certified Peer Recovery Specialists. SAARA peers also serve Richmond-area behavioral health and criminal court dockets, supporting justice-involved participants one-on-one through recovery. SAARA offers peer support and education—not clinical treatment or detox services.",
    description_es="SAARA of Virginia (Alianza de Recuperación de Adicciones y Abuso de Sustancias) es la organización comunitaria de recuperación estatal que ofrece grupos de recuperación dirigidos por pares, apoyo por línea cálida, defensa de la recuperación y capacitación para Especialistas Certificados en Recuperación entre Pares. Los pares de SAARA también sirven en tribunales conductuales y penales del área de Richmond, apoyando a participantes con antecedentes penales. SAARA ofrece apoyo entre pares y educación, no tratamiento clínico.",
    address="530 East Main Street, Suite 701", city="Richmond", phone="804-762-4445", email="info@saara.org",
    website="https://www.saara.org",
    eligibility="Open to Virginians in or seeking recovery from substance use disorders, their families, and community supporters; no criminal-record restrictions stated.",
    eligibility_es="Abierto a virginianos en recuperación o que buscan recuperarse de trastornos por uso de sustancias, sus familias y aliados comunitarios; sin restricciones de antecedentes penales indicadas.",
    notes="Visit saara.org for peer group schedules and CPRS training dates; SAARA affiliates operate in regions across Virginia including Richmond, Roanoke, Hampton Roads, and Northern Virginia.",
    notes_es="Visite saara.org para horarios de grupos de pares y fechas de capacitación CPRS; SAARA tiene afiliados en regiones de toda Virginia, incluidas Richmond, Roanoke, Hampton Roads y el norte de Virginia.",
    hours="Office Monday–Friday business hours; group schedules vary",
    tags="statewide|peer-support|recovery|substance-use|CPRS|advocacy",
    services="Peer-led recovery groups|Recovery warmline support|Peer Recovery Specialist training|Court docket peer support|Recovery advocacy",
    county="Richmond City", served_counties="", coverage="statewide",
    _source="https://www.saara.org/about", _source_type="nonprofit", _confidence="high",
)

# --- Phase 2: Major metro anchors ---
# Richmond metro
add(
    name="OAR of Richmond",
    category="reentry-organizations", region="Richmond metro",
    description="OAR of Richmond (Opportunity. Alliance. Reentry.) is the Richmond region's lead reentry organization, providing person-centered transition services during and after incarceration in the Richmond, Henrico, Chesterfield, and Hanover jails and for people returning from state and federal custody. Case managers help with employment readiness, ID and document fees, clothing, transportation, and community referrals. Intake is available for people released within roughly the past six months.",
    description_es="OAR of Richmond (Opportunity. Alliance. Reentry.) es la organización líder de reinserción de la región de Richmond, y ofrece servicios de transición centrados en la persona durante y después de la encarcelación en las cárceles de Richmond, Henrico, Chesterfield y Hanover y para quienes regresan de custodia estatal y federal. Los administradores de casos ayudan con preparación laboral, tarifas de identificación y documentos, ropa, transporte y referencias comunitarias. La admisión está disponible para personas liberadas en los últimos seis meses aproximadamente.",
    address="3111 West Clay Street", city="Richmond", phone="804-643-2746", email="info@oarric.org",
    website="https://www.oarric.org",
    eligibility="Adults impacted by the criminal legal system returning to the Richmond region; post-release intake generally within six months of release.",
    eligibility_es="Adultos afectados por el sistema legal penal que regresan a la región de Richmond; la admisión posterior a la liberación generalmente es dentro de los seis meses posteriores a la liberación.",
    notes="Complete intake in person; visiting hours Monday–Thursday 8:30 a.m.–12:00 p.m. and 1:00–3:30 p.m.; closed Fridays; call 804-643-2746 before your first visit.",
    notes_es="Complete la admisión en persona; horario de visitas de lunes a jueves de 8:30 a.m. a 12:00 p.m. y de 1:00 a 3:30 p.m.; cerrado los viernes; llame al 804-643-2746 antes de su primera visita.",
    hours="Monday–Thursday, 8:30 a.m.–12:00 p.m. and 1:00–3:30 p.m.; closed Fridays",
    tags="richmond|henrico|chesterfield|reentry|case-management|employment",
    services="Post-release case management|Employment readiness|ID and document assistance|Clothing and transportation aid|Community referrals",
    county="Richmond City", served_counties="Richmond City|Henrico|Chesterfield|Hanover|Petersburg", coverage="multi",
    _source="https://www.oarric.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="REAL LIFE — Recovery & Reentry Program",
    category="housing", region="Richmond metro",
    description="REAL LIFE is a Richmond nonprofit bridging incarceration, homelessness, and substance use disorder through eleven structured recovery houses, an East End community center, and intensive case management. Residents complete 20–30 hours of weekly programming using a behavior modification curriculum, then receive employment and education navigation with connections to more than 100 employer partners. The program primarily serves people in reentry from across Virginia and requires full participation.",
    description_es="REAL LIFE es una organización sin fines de lucro de Richmond que atiende la encarcelación, la falta de vivienda y los trastornos por uso de sustancias mediante once casas de recuperación estructuradas, un centro comunitario en el East End y manejo intensivo de casos. Los residentes completan de 20 a 30 horas semanales de programación con un currículo de modificación de conducta, y luego reciben navegación de empleo y educación con conexiones a más de 100 empleadores aliados. Sirve principalmente a personas en reinserción de toda Virginia y requiere participación completa.",
    address="", city="Richmond", phone="", email="",
    website="https://reallifeprogram.org",
    eligibility="Adults 18 and older exiting incarceration, homelessness, or addiction who are drug-free at entry and willing to commit to the structured residential program; participants come from across Virginia.",
    eligibility_es="Adultos de 18 años o más que salen de la encarcelación, la falta de vivienda o la adicción, libres de drogas al ingresar y dispuestos a comprometerse con el programa residencial estructurado; los participantes provienen de toda Virginia.",
    notes="Apply for recovery housing through the forms at reallifeprogram.org; an initial stabilization period restricts outside appointments before the employment search phase begins.",
    notes_es="Solicite vivienda de recuperación mediante los formularios en reallifeprogram.org; un período inicial de estabilización restringe las citas externas antes de que comience la fase de búsqueda de empleo.",
    hours="Residential program 24/7; contact for community center hours",
    tags="richmond|housing|recovery|reentry|SUD|case-management",
    services="Structured recovery housing|Intensive case management|Behavior modification programming|Employment navigation|Education support",
    county="Richmond City", served_counties="Richmond City", coverage="single",
    _source="https://reallifeprogram.org/about/", _source_type="nonprofit", _confidence="high",
)
add(
    name="Boaz & Ruth — Transitional Jobs & Training",
    category="employment", region="Richmond metro",
    description="Boaz & Ruth rebuilds lives and the Highland Park community in Richmond through a transitional jobs and training program for formerly incarcerated men and women. Trainees practice job and life skills in the organization's social enterprises along the Highland Park commercial corridor, paired with mentoring, Jobs for Life classes, and community connection activities. Fewer than 10% of program graduates have returned to incarceration, and most gain full-time employment during or shortly after the program.",
    description_es="Boaz & Ruth reconstruye vidas y la comunidad de Highland Park en Richmond mediante un programa de empleos transicionales y capacitación para hombres y mujeres anteriormente encarcelados. Los participantes practican habilidades laborales y de vida en las empresas sociales de la organización en el corredor comercial de Highland Park, junto con mentoría, clases Jobs for Life y actividades de conexión comunitaria. Menos del 10% de los graduados ha vuelto a la encarcelación y la mayoría obtiene empleo de tiempo completo.",
    address="3030 Meadowbridge Road", city="Richmond", phone="804-329-4900", email="",
    website="https://www.boazandruth.com",
    eligibility="Formerly incarcerated and unemployed or under-employed adults seeking transitional work and training; program-specific enrollment requirements apply.",
    eligibility_es="Adultos anteriormente encarcelados y desempleados o subempleados que buscan trabajo transicional y capacitación; aplican requisitos de inscripción específicos del programa.",
    notes="Call 804-329-4900 for training program enrollment; social enterprise sites in Highland Park serve as hands-on training labs.",
    notes_es="Llame al 804-329-4900 para inscribirse en el programa de capacitación; los sitios de empresas sociales en Highland Park sirven como laboratorios prácticos.",
    hours="Monday–Friday business hours; enterprise hours vary",
    tags="richmond|employment|transitional-jobs|reentry|fair-chance|job-training",
    services="Transitional jobs|Job and life skills training|Jobs for Life classes|Mentoring|Employment placement support",
    county="Richmond City", served_counties="Richmond City", coverage="single",
    _source="https://www.boazandruth.com", _source_type="nonprofit", _confidence="high",
)
add(
    name="CARITAS — The Healing Place",
    category="substance-use-treatment", region="Richmond metro",
    description="The Healing Place is a long-term, peer-driven residential recovery program offered free of charge by CARITAS to men and women with substance use disorders in the greater Richmond area, including many people arriving directly from incarceration. The program combines on-demand residential recovery, workforce development, a transitional sober living community, and an active alumni network. Admission is first-come, first-served with an in-person pre-screening at the appropriate campus.",
    description_es="The Healing Place es un programa residencial de recuperación a largo plazo, dirigido por pares y gratuito, ofrecido por CARITAS a hombres y mujeres con trastornos por uso de sustancias en el área metropolitana de Richmond, incluidas muchas personas que llegan directamente de la encarcelación. El programa combina recuperación residencial bajo demanda, desarrollo laboral, una comunidad de vivienda sobria transicional y una red activa de exalumnos. La admisión es por orden de llegada con una preevaluación en persona.",
    address="700 Dinwiddie Avenue", city="Richmond", phone="804-230-1184", email="",
    website="https://caritasva.org/the-healing-place/",
    eligibility="Adults 18 and older with substance use disorders able to physically participate; men served at the Dinwiddie Avenue campus and women at 2220 Stockton Street; no fee.",
    eligibility_es="Adultos de 18 años o más con trastornos por uso de sustancias capaces de participar físicamente; los hombres son atendidos en el campus de Dinwiddie Avenue y las mujeres en 2220 Stockton Street; sin costo.",
    notes="Call 804-230-1184 for the men's program or 804-418-3049 for the women's program; complete pre-screening in person at the campus; for emergency shelter call the Homeless Connection Line at 804-972-0813.",
    notes_es="Llame al 804-230-1184 para el programa de hombres o al 804-418-3049 para el de mujeres; complete la preevaluación en persona en el campus; para refugio de emergencia llame a la Homeless Connection Line al 804-972-0813.",
    hours="Residential program 24/7; intake Monday–Friday business hours",
    tags="richmond|chesterfield|henrico|substance-use|recovery|housing|peer-support",
    services="Long-term residential recovery|Peer-driven programming|Workforce development|Transitional sober living|Alumni recovery support",
    county="Richmond City", served_counties="Richmond City|Chesterfield|Henrico|Hanover", coverage="multi",
    _source="https://caritasva.org/the-healing-place/", _source_type="nonprofit", _confidence="high",
)
add(
    name="CARITAS Works — Workforce Development",
    category="employment", region="Richmond metro",
    description="CARITAS Works is a six-week intensive workforce development program in Richmond for adults with significant employment barriers, including criminal records, homelessness, and recovery histories. Participants build professional skills, practice interviewing, earn credentials, and connect with Richmond-area employers willing to hire program graduates. The program is part of the CARITAS continuum that also includes shelter, recovery, and furniture bank services for the region.",
    description_es="CARITAS Works es un programa intensivo de desarrollo laboral de seis semanas en Richmond para adultos con barreras significativas de empleo, incluidos antecedentes penales, falta de vivienda e historiales de recuperación. Los participantes desarrollan habilidades profesionales, practican entrevistas, obtienen credenciales y se conectan con empleadores del área de Richmond dispuestos a contratar a los graduados. Forma parte del continuo de CARITAS, que también incluye refugio, recuperación y un banco de muebles.",
    address="2220 Stockton Street", city="Richmond", phone="804-612-1752", email="mmilio@caritasva.org",
    website="https://caritasva.org/i-need-help/",
    eligibility="Adults in the Richmond region with significant barriers to employment, including justice involvement, homelessness, or substance use recovery.",
    eligibility_es="Adultos de la región de Richmond con barreras significativas para el empleo, incluidas la participación en el sistema de justicia, la falta de vivienda o la recuperación del uso de sustancias.",
    notes="Contact mmilio@caritasva.org or 804-612-1752 to apply; cohorts run on a class schedule, so ask about the next start date.",
    notes_es="Contacte a mmilio@caritasva.org o al 804-612-1752 para solicitar; las cohortes siguen un calendario de clases, pregunte por la próxima fecha de inicio.",
    hours="Class schedule varies by cohort; office Monday–Friday business hours",
    tags="richmond|employment|job-training|fair-chance|reentry|workforce",
    services="Six-week job readiness training|Professional skills classes|Interview preparation|Employer connections|Career coaching",
    county="Richmond City", served_counties="Richmond City|Chesterfield|Henrico|Hanover", coverage="multi",
    _source="https://caritasva.org/i-need-help/", _source_type="nonprofit", _confidence="high",
)
add(
    name="Goodwill of Central and Coastal Virginia — Reentry & Career Services",
    category="employment", region="Richmond metro & Hampton Roads",
    description="Goodwill of Central and Coastal Virginia operates community employment centers across the Richmond region and Hampton Roads offering free career services with dedicated reentry support for citizens returning from incarceration. Staff help with career planning, resumes and interviews, disclosing a criminal record to employers, the federal bonding program, restoration of civil rights, and guidance on record expungement, plus job fairs that include fair-chance employers.",
    description_es="Goodwill de Virginia Central y Costera opera centros comunitarios de empleo en la región de Richmond y Hampton Roads que ofrecen servicios de carrera gratuitos con apoyo dedicado de reinserción para ciudadanos que regresan de la encarcelación. El personal ayuda con planificación de carrera, currículums y entrevistas, cómo divulgar antecedentes penales a empleadores, el programa federal de fianzas, la restauración de derechos civiles y orientación sobre expungación, además de ferias de empleo con empleadores de segunda oportunidad.",
    address="6301 Midlothian Turnpike", city="Richmond", phone="804-745-6300", email="",
    website="https://goodwillvirginia.org",
    eligibility="Job seekers with barriers to employment including criminal histories, disabilities, limited work experience, or outdated skills; services are free.",
    eligibility_es="Buscadores de empleo con barreras, incluidos antecedentes penales, discapacidades, experiencia laboral limitada o habilidades desactualizadas; los servicios son gratuitos.",
    notes="Call 804-745-6300 in Central Virginia or 757-248-9405 in Hampton Roads (1911 Saville Row, Hampton); registration required for reentry workshops.",
    notes_es="Llame al 804-745-6300 en Virginia Central o al 757-248-9405 en Hampton Roads (1911 Saville Row, Hampton); se requiere registro para los talleres de reinserción.",
    hours="Monday–Friday, 8:00 a.m.–4:30 p.m.; center hours vary",
    tags="richmond|hampton|newport-news|norfolk|employment|fair-chance|reentry|job-training",
    services="Career planning|Resume and interview preparation|Criminal record disclosure coaching|Federal bonding guidance|Reentry workshops",
    county="Richmond City", served_counties="Richmond City|Henrico|Chesterfield|Hampton|Newport News|Norfolk", coverage="multi",
    _source="https://goodwillvirginia.org/governor-mcauliffe-hosts-re-entry-resource-fair-at-goodwills-richmond-support-center/", _source_type="nonprofit", _confidence="high",
)
add(
    name="Daily Planet Health Services",
    category="healthcare", region="Richmond metro",
    description="Daily Planet Health Services is a federally qualified health center in Richmond serving people experiencing homelessness or housing instability—including many returning from incarceration—along with the broader community facing barriers to care. Integrated services include primary medical care, mental health and substance use disorder treatment, dental care, pharmacy counseling, case management, and medical respite, delivered across multiple sites regardless of insurance status.",
    description_es="Daily Planet Health Services es un centro de salud calificado federalmente en Richmond que atiende a personas sin hogar o con inestabilidad de vivienda—incluidas muchas que regresan de la encarcelación—y a la comunidad en general que enfrenta barreras de atención. Los servicios integrados incluyen atención médica primaria, tratamiento de salud mental y uso de sustancias, atención dental, consejería de farmacia, manejo de casos y descanso médico, en varios sitios sin importar el estado del seguro.",
    address="517 West Grace Street", city="Richmond", phone="804-783-2505", email="",
    website="https://dailyplanetva.org",
    eligibility="Anyone regardless of housing, financial, or insurance status; primary population is people experiencing homelessness or housing instability; sliding fees determined at registration.",
    eligibility_es="Cualquier persona sin importar su situación de vivienda, financiera o de seguro; la población principal son personas sin hogar o con inestabilidad de vivienda; tarifas móviles determinadas al registrarse.",
    notes="Register in person 8–11:30 a.m. and 1–3 p.m. Monday–Friday or by phone at 804-783-2505; walk-in medical care at 511 West Grace Street; bring ID and proof of income if available.",
    notes_es="Regístrese en persona de 8 a 11:30 a.m. y de 1 a 3 p.m. de lunes a viernes o por teléfono al 804-783-2505; atención médica sin cita en 511 West Grace Street; traiga identificación y prueba de ingresos si las tiene.",
    hours="Monday–Friday, 8:30 a.m.–4:30 p.m.; 24/7 after-hours phone coverage",
    tags="richmond|healthcare|FQHC|homeless|mental-health|substance-use|walk-in",
    services="Primary medical care|Behavioral health treatment|Substance use disorder services|Dental care|Case management",
    county="Richmond City", served_counties="Richmond City|Henrico|Chesterfield", coverage="multi",
    _source="https://nhchc.org/grantee-directory/the-daily-planet-2/", _source_type="nonprofit", _confidence="high",
)
add(
    name="Feed More — Central Virginia Food Bank",
    category="food-nutrition", region="Central Virginia — 30+ localities",
    description="Feed More is Central Virginia's Feeding America food bank, collecting and distributing food through nearly 300 partner pantries, soup kitchens, and mobile distributions across a 34-locality service area stretching from the Northern Neck to the North Carolina border. Its Help Line connects neighbors—including people rebuilding after incarceration—to nearby food pantries and helps with SNAP applications. Feed More distributes through partners rather than serving walk-in clients at its warehouse.",
    description_es="Feed More es el banco de alimentos de Feeding America para Virginia Central, y recolecta y distribuye alimentos a través de casi 300 despensas asociadas, comedores y distribuciones móviles en un área de servicio de 34 localidades que se extiende desde el Northern Neck hasta la frontera con Carolina del Norte. Su línea de ayuda conecta a los vecinos—incluidas personas que se reconstruyen tras la encarcelación—con despensas cercanas y ayuda con solicitudes de SNAP. Distribuye mediante aliados, no atiende directamente en su almacén.",
    address="8020 Villa Park Drive", city="Richmond", phone="804-521-2500", email="",
    website="https://feedmore.org",
    eligibility="Residents of Feed More's 34-city-and-county Central Virginia service area facing food insecurity; partner pantry requirements vary by site.",
    eligibility_es="Residentes del área de servicio de 34 ciudades y condados de Feed More en Virginia Central que enfrentan inseguridad alimentaria; los requisitos de las despensas asociadas varían según el sitio.",
    notes="Call the Help Line at 804-237-8617 (Mon–Fri 9 a.m.–4 p.m.) to find a nearby pantry or get SNAP application help; use the online agency locator at feedmore.org.",
    notes_es="Llame a la línea de ayuda al 804-237-8617 (lun–vie 9 a.m.–4 p.m.) para encontrar una despensa cercana u obtener ayuda con la solicitud de SNAP; use el localizador de agencias en feedmore.org.",
    hours="Help Line Monday–Friday, 9:00 a.m.–4:00 p.m.; pantry hours vary",
    tags="richmond|central-virginia|food-nutrition|food-bank|SNAP|pantry",
    services="Partner pantry network|Food assistance locator|SNAP application help|Mobile pantry distributions|Meals on Wheels",
    county="Henrico",
    served_counties="Amelia|Brunswick|Charles City|Chesterfield|Colonial Heights|Cumberland|Dinwiddie|Emporia|Goochland|Greensville|Halifax|Henrico|Hopewell|King and Queen|King William|Lancaster|Louisa|Lunenburg|Mecklenburg|Middlesex|New Kent|Northumberland|Nottoway|Petersburg|Powhatan|Prince Edward|Prince George|Richmond City|Sussex|Westmoreland",
    coverage="multi",
    _source="https://feedmore.org/help-line/", _source_type="nonprofit", _confidence="high",
)
add(
    name="The Fountain Fund — Central Virginia",
    category="financial-assistance", region="Charlottesville & Richmond",
    description="The Fountain Fund is a nonprofit lender providing low-interest microloans and financial coaching to formerly incarcerated people in Central Virginia, with lending based in Charlottesville and expanded into Richmond. Loans up to $5,000 for consumers (and larger amounts for businesses) can pay court debt, work expenses, transportation, rental move-in costs, or child support, at rates near 5% regardless of conviction type. Borrowers build credit while working toward self-determined goals.",
    description_es="The Fountain Fund es un prestamista sin fines de lucro que ofrece microcréditos de bajo interés y asesoría financiera a personas anteriormente encarceladas en Virginia Central, con préstamos basados en Charlottesville y expandidos a Richmond. Los préstamos de hasta $5,000 para consumidores (y montos mayores para negocios) pueden pagar deudas judiciales, gastos laborales, transporte, costos de mudanza o manutención infantil, con tasas cercanas al 5% sin importar el tipo de condena. Los prestatarios construyen crédito.",
    address="", city="Charlottesville", phone="", email="",
    website="https://www.fountainfund.org",
    eligibility="Formerly incarcerated adults in the Central Virginia lending area with a demonstrated ability to repay; no restrictions based on conviction type or length of incarceration.",
    eligibility_es="Adultos anteriormente encarcelados en el área de préstamos de Virginia Central con capacidad demostrada de pago; sin restricciones por tipo de condena o duración de la encarcelación.",
    notes="Submit the Central Virginia loan inquiry form at fountainfund.org; review the FAQs and lending policies first; an ACH automatic-payment discount lowers the rate to 3%.",
    notes_es="Envíe el formulario de consulta de préstamo de Virginia Central en fountainfund.org; revise primero las preguntas frecuentes y las políticas de préstamo; el descuento por pago automático ACH baja la tasa al 3%.",
    hours="Online inquiries 24/7; staff respond during business hours",
    tags="charlottesville|richmond|financial-assistance|microloans|credit-building|reentry",
    services="Low-interest consumer microloans|Small business loans|Financial coaching|Credit building|Court debt payoff loans",
    county="Charlottesville", served_counties="Charlottesville|Albemarle|Richmond City", coverage="multi",
    _source="https://www.fountainfund.org/what-we-do", _source_type="nonprofit", _confidence="high",
)

# Hampton Roads
add(
    name="STEP UP, Inc. — Hampton Roads Reentry Employment",
    category="employment", region="Hampton Roads",
    description="STEP UP, Inc. is a Norfolk-based nonprofit providing pre-release and post-incarceration services across Hampton Roads, Western Tidewater, and nearby localities. Staff meet participants in jails and prisons before release and continue after return home with job skills training, resume help, employment placement, and referrals for housing, food, clothing, transportation, and treatment. Norfolk's re-entry resource guides list STEP UP for justice-involved job training.",
    description_es="STEP UP, Inc. es una organización sin fines de lucro con sede en Norfolk que ofrece servicios previos y posteriores a la encarcelación en Hampton Roads, Western Tidewater y localidades cercanas. El personal se reúne con participantes en cárceles y prisiones antes de la liberación y continúa después del regreso con capacitación laboral, ayuda con currículums, colocación de empleo y referencias de vivienda, alimentos, ropa, transporte y tratamiento.",
    address="5900 East Virginia Beach Boulevard, Suite 102", city="Norfolk", phone="757-588-3151", email="info@stepupincorporated.org",
    website="",
    eligibility="People incarcerated in or released from correctional facilities who are returning to Hampton Roads localities; referrals from jails, prisons, probation, and community organizations accepted.",
    eligibility_es="Personas encarceladas o liberadas de instalaciones correccionales que regresan a las localidades de Hampton Roads; se aceptan referencias de cárceles, prisiones, probatoria y organizaciones comunitarias.",
    notes="Call 757-588-3151 or email info@stepupincorporated.org for intake; stepupincorporated.org was unavailable at re-audit—use phone or email. Pre-release participants are often enrolled through jail programming such as the Norfolk Sheriff's Pathway programs.",
    notes_es="Llame al 757-588-3151 o escriba a info@stepupincorporated.org; stepupincorporated.org no estaba disponible en la reauditoría. Los participantes previos a la liberación a menudo se inscriben mediante programación carcelaria como Pathway del alguacil de Norfolk.",
    hours="Monday–Friday business hours",
    tags="norfolk|hampton-roads|employment|reentry|job-placement|pre-release",
    services="Pre-release job readiness classes|Post-release job placement|Resume and interview help|Employment training|Support service referrals",
    county="Norfolk",
    served_counties="Norfolk|Virginia Beach|Chesapeake|Suffolk|Hampton|Newport News|Isle of Wight|James City|York|Williamsburg|Franklin City",
    coverage="multi",
    _source="https://norfolk.gov/DocumentCenter/View/58588/Clothing-Education--Training-Employment-Food-and-Housing-Assistance-Guide-Book", _source_type="government", _confidence="high",
)
add(
    name="The Up Center — Family Support & Counseling",
    category="family-children", region="Hampton Roads",
    description="The Up Center is a Norfolk-based nonprofit providing more than 20 support services for children and families across South Hampton Roads, including mental health and substance use counseling, fatherhood support through the Dad2Dads program, parenting education, youth mentoring, and housing and financial counseling. Families navigating a parent's incarceration or reentry can access counseling and father-engagement programming; the center has historically run Second Chance Act fatherhood reentry programs.",
    description_es="The Up Center es una organización sin fines de lucro con sede en Norfolk que ofrece más de 20 servicios de apoyo para niños y familias en South Hampton Roads, incluidos consejería de salud mental y uso de sustancias, apoyo a la paternidad mediante el programa Dad2Dads, educación para padres, mentoría juvenil y consejería de vivienda y finanzas. Las familias que atraviesan la encarcelación o reinserción de un padre pueden acceder a consejería y programas de participación paterna.",
    address="580 East Main Street, Suite 400", city="Norfolk", phone="757-354-3819", email="",
    website="https://theupcenter.org",
    eligibility="Children, parents, and families in South Hampton Roads; program-specific requirements vary; Dad2Dads fatherhood services are free.",
    eligibility_es="Niños, padres y familias en South Hampton Roads; los requisitos varían según el programa; los servicios de paternidad Dad2Dads son gratuitos.",
    notes="Call 757-354-3819 or use the new-client application at theupcenter.org; Dads Under Construction groups meet the first and third Tuesdays, 6–7:30 p.m.",
    notes_es="Llame al 757-354-3819 o use la solicitud de cliente nuevo en theupcenter.org; los grupos Dads Under Construction se reúnen el primer y tercer martes de 6 a 7:30 p.m.",
    hours="Monday–Friday business hours; group schedules vary",
    tags="norfolk|hampton-roads|family-children|fatherhood|counseling|mental-health",
    services="Family and mental health counseling|Dad2Dads fatherhood support|Parenting education|Housing and financial counseling|Youth mentoring",
    county="Norfolk", served_counties="Norfolk|Portsmouth|Chesapeake|Suffolk|Virginia Beach", coverage="multi",
    _source="https://theupcenter.org/about-us/", _source_type="nonprofit", _confidence="high",
)
add(
    name="Union Mission Ministries — Norfolk",
    category="housing", region="Norfolk",
    description="Union Mission Ministries operates Norfolk's largest emergency shelter campus, open 24 hours with the Bashford Men's Shelter, the Grace Place women's shelter, and family accommodations. Guests receive meals, clothing, showers, case management, job-readiness and life-skills training, benefits assistance, and housing and employment referrals, with the RECLAIM transitional housing track for men needing longer support. The faith-based ministry cannot provide hotel vouchers or rent payments.",
    description_es="Union Mission Ministries opera el campus de refugio de emergencia más grande de Norfolk, abierto las 24 horas, con el refugio para hombres Bashford, el refugio para mujeres Grace Place y alojamiento familiar. Los huéspedes reciben comidas, ropa, duchas, manejo de casos, capacitación laboral y de habilidades para la vida, asistencia con beneficios y referencias de vivienda y empleo, con el programa transicional RECLAIM para hombres que necesitan apoyo más prolongado. El ministerio no ofrece vales de hotel ni pagos de renta.",
    address="5100 East Virginia Beach Boulevard", city="Norfolk", phone="757-627-8686", email="",
    website="https://www.unionmissionministries.org",
    eligibility="Adults and families experiencing homelessness in the Norfolk area; no profession of faith required to receive shelter, meals, or services.",
    eligibility_es="Adultos y familias sin hogar en el área de Norfolk; no se requiere profesión de fe para recibir refugio, comidas o servicios.",
    notes="Call 757-627-8686 for shelter availability—ext. 200 for men, ext. 331 for women; the campus is open 24 hours; for regional housing crisis help call 757-587-4202.",
    notes_es="Llame al 757-627-8686 para disponibilidad de refugio—ext. 200 para hombres, ext. 331 para mujeres; el campus está abierto las 24 horas; para ayuda regional de crisis de vivienda llame al 757-587-4202.",
    hours="Open 24 hours daily",
    tags="norfolk|housing|shelter|meals|case-management|reentry",
    services="Emergency shelter|Meals and clothing|Case management|Job readiness training|Transitional housing (RECLAIM)",
    county="Norfolk", served_counties="Norfolk", coverage="single",
    _source="https://www.unionmissionministries.org/get-help/", _source_type="nonprofit", _confidence="high",
)
add(
    name="Hampton Roads Community Health Center",
    category="healthcare", region="Portsmouth & Norfolk",
    description="Hampton Roads Community Health Center is a federally qualified health center with clinics in Portsmouth and Norfolk providing primary medical care, dental care, behavioral health, and an in-house pharmacy with free prescription delivery. All sites schedule through one central number, and a mobile dental unit travels across Portsmouth, Norfolk, and Suffolk to reach low-income residents where they are. New patients, including uninsured adults returning from incarceration, are accepted with sliding fees.",
    description_es="Hampton Roads Community Health Center es un centro de salud calificado federalmente con clínicas en Portsmouth y Norfolk que ofrece atención médica primaria, atención dental, salud conductual y una farmacia interna con entrega gratuita de recetas. Todos los sitios agendan mediante un número central, y una unidad dental móvil recorre Portsmouth, Norfolk y Suffolk para llegar a los residentes de bajos ingresos. Se aceptan pacientes nuevos, incluidos adultos sin seguro que regresan de la encarcelación, con tarifas móviles.",
    address="1541 High Street", city="Portsmouth", phone="757-393-6363", email="",
    website="https://www.hrchc.org",
    eligibility="Open to Hampton Roads residents regardless of insurance status; sliding fee discounts based on income; Medicaid, Medicare, and private insurance accepted.",
    eligibility_es="Abierto a residentes de Hampton Roads sin importar el estado del seguro; descuentos de tarifa móvil según ingresos; se aceptan Medicaid, Medicare y seguros privados.",
    notes="Call 757-393-6363 to schedule at any location; the Portsmouth site at 1541 High Street offers medical, dental, behavioral health, and pharmacy under one roof.",
    notes_es="Llame al 757-393-6363 para agendar en cualquier ubicación; el sitio de Portsmouth en 1541 High Street ofrece servicios médicos, dentales, de salud conductual y farmacia en un solo lugar.",
    hours="Monday–Friday, 7:30 a.m.–5:30 p.m.; site hours vary",
    tags="portsmouth|norfolk|healthcare|FQHC|dental|behavioral-health|sliding-scale",
    services="Primary medical care|Dental care|Behavioral health services|In-house pharmacy|Mobile dental outreach",
    county="Portsmouth", served_counties="Portsmouth|Norfolk|Suffolk", coverage="multi",
    _source="https://www.hrchc.org/service-locations.html", _source_type="nonprofit", _confidence="high",
)
add(
    name="Foodbank of Southeastern Virginia and the Eastern Shore",
    category="food-nutrition", region="Hampton Roads & Eastern Shore",
    description="The Foodbank of Southeastern Virginia and the Eastern Shore is the Feeding America food bank serving eleven cities and counties across South Hampton Roads, Western Tidewater, and the Eastern Shore since 1981. It distributes food through a large network of partner pantries, mobile pantries, and community programs, and helps neighbors connect to SNAP and other benefits. Food reaches households through partner agencies located throughout the 4,745-square-mile service area.",
    description_es="El Foodbank of Southeastern Virginia and the Eastern Shore es el banco de alimentos de Feeding America que sirve a once ciudades y condados de South Hampton Roads, Western Tidewater y la Costa Este desde 1981. Distribuye alimentos a través de una amplia red de despensas asociadas, despensas móviles y programas comunitarios, y ayuda a los vecinos a conectarse con SNAP y otros beneficios. Los alimentos llegan a los hogares mediante agencias asociadas en toda el área de servicio.",
    address="800 Tidewater Drive", city="Norfolk", phone="757-627-6599", email="",
    website="https://foodbankonline.org",
    eligibility="Residents of the Foodbank's eleven-locality service area facing food insecurity; partner pantry requirements vary by site.",
    eligibility_es="Residentes del área de servicio de once localidades del banco de alimentos que enfrentan inseguridad alimentaria; los requisitos de las despensas asociadas varían según el sitio.",
    notes="Use the pantry locator at foodbankonline.org or dial 211 to find nearby distributions; mobile pantry schedules are posted online.",
    notes_es="Use el localizador de despensas en foodbankonline.org o marque 211 para encontrar distribuciones cercanas; los horarios de las despensas móviles se publican en línea.",
    hours="Office Monday–Friday business hours; pantry and mobile distribution hours vary",
    tags="norfolk|hampton-roads|eastern-shore|food-nutrition|food-bank|pantry",
    services="Partner pantry network|Mobile pantry distributions|SNAP outreach|Community feeding programs",
    county="Norfolk",
    served_counties="Norfolk|Portsmouth|Chesapeake|Suffolk|Franklin City|Virginia Beach|Southampton|Northampton|Sussex|Isle of Wight|Accomack",
    coverage="multi",
    _source="https://foodbankonline.org/wp-content/uploads/2026/01/PAM-Jan-2026.pdf", _source_type="nonprofit", _confidence="high",
)
add(
    name="Virginia Peninsula Foodbank",
    category="food-nutrition", region="Virginia Peninsula",
    description="The Virginia Peninsula Foodbank in Hampton provides hunger relief across nine Peninsula and Middle Peninsula localities through more than 170 partner agencies including food pantries, soup kitchens, shelters, and community centers. Neighbors can shop the Community Pantry in Newport News, find partner pantries through the online locator, or arrange emergency food assistance by appointment. The foodbank also runs mobile distributions and nutrition programs for children, seniors, and veterans.",
    description_es="El Virginia Peninsula Foodbank en Hampton brinda alivio contra el hambre en nueve localidades de la Península y la Península Media a través de más de 170 agencias asociadas, incluidas despensas, comedores, refugios y centros comunitarios. Los vecinos pueden usar la Despensa Comunitaria en Newport News, encontrar despensas asociadas con el localizador en línea o coordinar asistencia alimentaria de emergencia con cita. El banco también opera distribuciones móviles y programas de nutrición para niños, personas mayores y veteranos.",
    address="2401 Aluminum Avenue", city="Hampton", phone="757-596-7188", email="",
    website="https://hrfoodbank.org",
    eligibility="Residents of the Peninsula service area facing food insecurity; partner pantry requirements vary by site.",
    eligibility_es="Residentes del área de servicio de la Península que enfrentan inseguridad alimentaria; los requisitos de las despensas asociadas varían según el sitio.",
    notes="Visit the Community Pantry at 3509 Chestnut Avenue, Newport News during shopping hours; for emergency food call 757-596-7188 (Mon–Fri 1:30–3:30 p.m., appointments preferred).",
    notes_es="Visite la Despensa Comunitaria en 3509 Chestnut Avenue, Newport News durante el horario de compras; para alimentos de emergencia llame al 757-596-7188 (lun–vie 1:30–3:30 p.m., se prefieren citas).",
    hours="Office Monday–Friday business hours; emergency assistance 1:30–3:30 p.m. weekdays",
    tags="hampton|newport-news|peninsula|food-nutrition|food-bank|pantry",
    services="Community Pantry|Partner pantry locator|Emergency food assistance|Mobile pantry distributions|Child and senior nutrition programs",
    county="Hampton",
    served_counties="Hampton|Newport News|Poquoson|Williamsburg|Gloucester|James City|Mathews|Surry|York",
    coverage="multi",
    _source="https://hrfoodbank.org/need-food/", _source_type="nonprofit", _confidence="high",
)
add(
    name="Virginia Career Works — Norfolk Center",
    category="employment", region="Hampton Roads",
    description="The Virginia Career Works Norfolk center is the American Job Center serving the Hampton Roads workforce region with free job search assistance, career coaching, resume help, WIOA training referrals, and connections to hiring events. Staff serve all job seekers, including people with criminal records, and can point returning citizens to fair-chance employers, federal bonding, and the Work Opportunity Tax Credit that offsets hiring concerns for employers.",
    description_es="El centro Virginia Career Works de Norfolk es el Centro de Empleo Americano que sirve a la región laboral de Hampton Roads con ayuda gratuita para buscar empleo, orientación profesional, ayuda con currículums, referencias a capacitación WIOA y conexiones con eventos de contratación. El personal atiende a todos los buscadores de empleo, incluidas personas con antecedentes penales, y puede orientar a los ciudadanos que regresan hacia empleadores de segunda oportunidad, fianzas federales y el crédito fiscal WOTC.",
    address="861 Glenrock Road, Suite 100", city="Norfolk", phone="", email="",
    website="https://virginiacareerworks.com/locations/",
    eligibility="Open to job seekers in the Hampton Roads region including justice-involved individuals; core services are free.",
    eligibility_es="Abierto a buscadores de empleo en la región de Hampton Roads, incluidas personas con antecedentes penales; los servicios básicos son gratuitos.",
    notes="Check current hours through the center locator at virginiacareerworks.com/locations; register on the Virginia Workforce Connection before visiting to speed up services.",
    notes_es="Consulte los horarios actuales en el localizador de centros en virginiacareerworks.com/locations; regístrese en Virginia Workforce Connection antes de visitar para agilizar los servicios.",
    hours="Monday–Friday business hours; confirm via center locator",
    tags="norfolk|hampton-roads|employment|workforce|WIOA|fair-chance",
    services="Job search assistance|Career coaching|WIOA training referrals|Resume and interview help|Hiring events",
    county="Norfolk", served_counties="Norfolk", coverage="single",
    _source="https://virginiacareerworks.com/locations/", _source_type="government", _confidence="high",
)
add(
    name="Virginia Career Works — Hampton Center",
    category="employment", region="Virginia Peninsula",
    description="The Virginia Career Works Hampton center is the American Job Center for the Virginia Peninsula, offering free job search tools, career counseling, skills workshops, WIOA-funded training referrals, and unemployment insurance assistance. Peninsula job seekers with criminal records can get help framing their history for employers and connecting to fair-chance hiring initiatives, GED referrals, and supportive services through partner agencies co-located with the center.",
    description_es="El centro Virginia Career Works de Hampton es el Centro de Empleo Americano de la Península de Virginia, y ofrece herramientas gratuitas de búsqueda de empleo, consejería de carrera, talleres de habilidades, referencias a capacitación financiada por WIOA y asistencia con el seguro de desempleo. Los buscadores de empleo con antecedentes penales pueden recibir ayuda para presentar su historial a los empleadores y conectarse con iniciativas de contratación de segunda oportunidad, referencias de GED y servicios de apoyo.",
    address="600 Butler Farm Road, Suite B", city="Hampton", phone="", email="",
    website="https://virginiacareerworks.com/locations/",
    eligibility="Open to job seekers on the Virginia Peninsula including justice-involved individuals; core services are free.",
    eligibility_es="Abierto a buscadores de empleo en la Península de Virginia, incluidas personas con antecedentes penales; los servicios básicos son gratuitos.",
    notes="Check current hours through the center locator at virginiacareerworks.com/locations; bring ID for workshops and training enrollment when available.",
    notes_es="Consulte los horarios actuales en el localizador de centros en virginiacareerworks.com/locations; traiga identificación para talleres e inscripción en capacitación cuando sea posible.",
    hours="Monday–Friday business hours; confirm via center locator",
    tags="hampton|peninsula|employment|workforce|WIOA|fair-chance",
    services="Job search assistance|Career counseling|WIOA training referrals|Skills workshops|Unemployment insurance help",
    county="Hampton", served_counties="Hampton", coverage="single",
    _source="https://virginiacareerworks.com/locations/", _source_type="government", _confidence="high",
)

# Northern Virginia
add(
    name="OAR of Arlington, Alexandria and Falls Church",
    category="reentry-organizations", region="Northern Virginia",
    description="OAR of Arlington, Alexandria and Falls Church journeys with people impacted by the criminal legal system, running pre-release programs in the Arlington County Detention Facility, Alexandria's Truesdale Adult Detention Center, and Coffeewood Correctional Center, plus post-release reentry support at its Arlington office. Services include transition coaching, employment help, housing assistance, phones and laptops, food, clothing, and a weekly support group, along with community service alternative sentencing.",
    description_es="OAR de Arlington, Alexandria y Falls Church acompaña a personas afectadas por el sistema legal penal, con programas previos a la liberación en el Centro de Detención del Condado de Arlington, el Centro de Detención Truesdale de Alexandria y el Centro Correccional Coffeewood, además de apoyo de reinserción posterior a la liberación en su oficina de Arlington. Los servicios incluyen orientación de transición, ayuda de empleo, asistencia de vivienda, teléfonos y computadoras, alimentos, ropa y un grupo de apoyo semanal, junto con sentencias alternativas de servicio comunitario.",
    address="1400 N. Uhle Street, Suite 704", city="Arlington", phone="703-745-5441", email="info@oaronline.org",
    website="https://www.oaronline.org",
    eligibility="People returning to Arlington County, the City of Alexandria, or the City of Falls Church from incarceration and their families; post-release reentry referral generally within 90 days of release.",
    eligibility_es="Personas que regresan al Condado de Arlington, la Ciudad de Alexandria o la Ciudad de Falls Church tras la encarcelación y sus familias; la referencia de reinserción posterior a la liberación generalmente ocurre dentro de los 90 días posteriores a la liberación.",
    notes="Call 703-745-5441 or email info@oaronline.org; a separate organization, OAR NOVA, serves Fairfax, Loudoun, and Prince William counties.",
    notes_es="Llame al 703-745-5441 o escriba a info@oaronline.org; una organización separada, OAR NOVA, sirve a los condados de Fairfax, Loudoun y Prince William.",
    hours="Monday–Friday business hours",
    tags="arlington|alexandria|falls-church|reentry|employment|case-management",
    services="Pre-release reentry programming|Post-release coaching|Employment program|Housing and direct assistance|Weekly support group",
    county="Arlington", served_counties="Arlington|Alexandria|Falls Church", coverage="multi",
    _source="https://www.oaronline.org/about-us/history-overview", _source_type="nonprofit", _confidence="high",
)
add(
    name="Friends of Guest House — Women's Reentry Program",
    category="housing", region="Northern Virginia",
    description="Friends of Guest House in Alexandria is Northern Virginia's only 24/7 residential reentry program for women and the largest gender-responsive reentry program in Virginia. The free six-month residential program pairs each woman with a case manager for an individualized reentry plan covering healthcare, workforce development, life skills, GED tutoring, and family reconnection, followed by aftercare and a Second Chance transitional rental community. About 85% of graduates never return to incarceration.",
    description_es="Friends of Guest House en Alexandria es el único programa residencial de reinserción 24/7 para mujeres en el norte de Virginia y el programa de reinserción con enfoque de género más grande del estado. El programa residencial gratuito de seis meses asigna a cada mujer una administradora de casos con un plan individualizado que cubre atención médica, desarrollo laboral, habilidades para la vida, tutoría de GED y reconexión familiar, seguido de un programa de seguimiento y una comunidad transicional de renta. Cerca del 85% de las graduadas no vuelve a la encarcelación.",
    address="", city="Alexandria", phone="", email="",
    website="https://friendsofguesthouse.org",
    eligibility="Women 18 and older on Virginia state probation or parole and in compliance with supervision terms; application includes a background check, physical exam, and phone interview.",
    eligibility_es="Mujeres de 18 años o más en probatoria o libertad condicional estatal de Virginia y en cumplimiento de los términos de supervisión; la solicitud incluye verificación de antecedentes, examen físico y entrevista telefónica.",
    notes="Submit the client application through friendsofguesthouse.org before release when possible; residents complete an intake evaluation with the Alexandria Community Services Board on arrival.",
    notes_es="Envíe la solicitud de cliente en friendsofguesthouse.org antes de la liberación cuando sea posible; las residentes completan una evaluación de admisión con la Junta de Servicios Comunitarios de Alexandria al llegar.",
    hours="Residential program 24/7; office Monday–Friday business hours",
    tags="alexandria|arlington|fairfax|housing|women|reentry|case-management",
    services="Six-month residential reentry program|Case management|Workforce development|Aftercare program|Transitional rental housing",
    county="Alexandria", served_counties="Alexandria|Arlington|Fairfax|Fairfax City|Falls Church|Loudoun|Prince William", coverage="multi",
    _source="https://friendsofguesthouse.org/about/", _source_type="nonprofit", _confidence="high",
)
add(
    name="Legal Services of Northern Virginia",
    category="legal-aid", region="Northern Virginia",
    description="Legal Services of Northern Virginia is a nonprofit law firm providing free civil legal help to low-income, elderly, and disabled residents across Northern Virginia, with offices in Fairfax, Arlington, Alexandria, Leesburg, and the Route 1 corridor. Practice areas include housing, consumer, family, benefits, and a Second Chances initiative addressing barriers tied to criminal records. LSNV handles civil matters only—not criminal defense—and screens all applicants for financial eligibility.",
    description_es="Legal Services of Northern Virginia es un bufete sin fines de lucro que brinda ayuda legal civil gratuita a residentes de bajos ingresos, personas mayores y personas con discapacidades en el norte de Virginia, con oficinas en Fairfax, Arlington, Alexandria, Leesburg y el corredor de la Ruta 1. Las áreas de práctica incluyen vivienda, consumidor, familia, beneficios y una iniciativa de Segundas Oportunidades sobre barreras ligadas a antecedentes penales. LSNV atiende solo asuntos civiles y evalúa la elegibilidad financiera.",
    address="10700 Page Avenue, Suite 100", city="Fairfax", phone="703-778-6800", email="help@lsnv.org",
    website="https://lsnv.org",
    eligibility="Low-income, elderly, or disabled residents of Fairfax, Arlington, Loudoun, and Prince William counties and the cities of Alexandria, Falls Church, Fairfax, Manassas, and Manassas Park; financial eligibility screening required.",
    eligibility_es="Residentes de bajos ingresos, personas mayores o con discapacidades de los condados de Fairfax, Arlington, Loudoun y Prince William y las ciudades de Alexandria, Falls Church, Fairfax, Manassas y Manassas Park; se requiere evaluación de elegibilidad financiera.",
    notes="Apply online 24/7 at lsnv.org or call 703-778-6800 Monday–Thursday, 9:30 a.m.–12 p.m. and 1:30–3 p.m.; walk-in applications on Wednesdays only.",
    notes_es="Solicite en línea 24/7 en lsnv.org o llame al 703-778-6800 de lunes a jueves, de 9:30 a.m. a 12 p.m. y de 1:30 a 3 p.m.; solicitudes sin cita solo los miércoles.",
    hours="Intake Monday–Thursday, 9:30 a.m.–12:00 p.m. and 1:30–3:00 p.m.; online application 24/7",
    tags="fairfax|arlington|alexandria|prince-william|loudoun|legal-aid|second-chances",
    services="Civil legal representation|Housing legal help|Second Chances record-barrier assistance|Benefits advocacy|Consumer protection",
    county="Fairfax",
    served_counties="Fairfax|Arlington|Alexandria|Loudoun|Prince William|Falls Church|Fairfax City|Manassas|Manassas Park",
    coverage="multi",
    _source="https://lsnv.org/get-help/how-do-i-apply/", _source_type="nonprofit", _confidence="high",
)
add(
    name="Legal Aid Justice Center",
    category="legal-aid", region="Charlottesville, Richmond, Petersburg & Northern Virginia",
    description="The Legal Aid Justice Center provides free civil legal help to financially eligible Virginians from offices in Charlottesville, Richmond, Petersburg, and Falls Church, with a criminal legal system practice that runs expungement clinics and helps people seal eligible records under Virginia's record sealing laws taking effect July 1, 2026. LAJC also litigates on housing, benefits, immigration, and civil rights issues. It does not handle criminal defense cases.",
    description_es="El Legal Aid Justice Center brinda ayuda legal civil gratuita a virginianos financieramente elegibles desde oficinas en Charlottesville, Richmond, Petersburg y Falls Church, con una práctica del sistema legal penal que realiza clínicas de expungación y ayuda a sellar antecedentes elegibles bajo las leyes de sellado de Virginia vigentes desde el 1 de julio de 2026. LAJC también litiga sobre vivienda, beneficios, inmigración y derechos civiles. No atiende casos de defensa penal.",
    address="1000 Preston Avenue, Suite A", city="Charlottesville", phone="434-977-0553", email="",
    website="https://www.justice4all.org",
    eligibility="Financially eligible residents of LAJC's Charlottesville, Richmond, Petersburg, and Northern Virginia service areas, or people whose legal issue arose there; income screening applies.",
    eligibility_es="Residentes financieramente elegibles de las áreas de servicio de LAJC en Charlottesville, Richmond, Petersburg y el norte de Virginia, o personas cuyo asunto legal surgió allí; se aplica evaluación de ingresos.",
    notes="Call the office nearest you: Charlottesville 434-977-0553, Richmond 804-643-1086 (phone intakes Mon–Fri), Petersburg 804-862-2205, Falls Church 703-778-3450; watch justice4all.org for expungement clinic dates.",
    notes_es="Llame a la oficina más cercana: Charlottesville 434-977-0553, Richmond 804-643-1086 (admisión telefónica lun–vie), Petersburg 804-862-2205, Falls Church 703-778-3450; consulte justice4all.org para fechas de clínicas de expungación.",
    hours="Intake Monday–Friday business hours; leave a voicemail for a callback",
    tags="charlottesville|richmond|petersburg|falls-church|legal-aid|expungement|record-sealing",
    services="Expungement clinics|Record sealing assistance|Housing legal help|Benefits advocacy|Civil rights litigation",
    county="Charlottesville",
    served_counties="Charlottesville|Albemarle|Fluvanna|Greene|Louisa|Nelson|Richmond City|Henrico|Chesterfield|Hanover|New Kent|Goochland|Powhatan|Charles City|Petersburg|Hopewell|Colonial Heights|Dinwiddie|Prince George|Surry|Fairfax|Fairfax City|Falls Church|Alexandria|Loudoun|Arlington|Prince William|Stafford",
    coverage="multi",
    _source="https://www.justice4all.org/contact/", _source_type="nonprofit", _confidence="high",
)
add(
    name="Central Virginia Legal Aid Society",
    category="legal-aid", region="Richmond, Petersburg & Charlottesville",
    description="Central Virginia Legal Aid Society provides free civil legal assistance to low-income people in the cities of Richmond, Petersburg, Hopewell, Colonial Heights, and Charlottesville and fifteen surrounding counties. Attorneys and pro bono volunteers handle housing and eviction, public benefits, family law, consumer, and expungement-related civil matters, with offices in Richmond, Petersburg, and Charlottesville. CVLAS handles civil cases only and screens applicants for income eligibility.",
    description_es="Central Virginia Legal Aid Society brinda asistencia legal civil gratuita a personas de bajos ingresos en las ciudades de Richmond, Petersburg, Hopewell, Colonial Heights y Charlottesville y quince condados circundantes. Abogados y voluntarios pro bono atienden vivienda y desalojos, beneficios públicos, derecho familiar, asuntos de consumidor y asuntos civiles relacionados con la expungación, con oficinas en Richmond, Petersburg y Charlottesville. CVLAS atiende solo casos civiles y evalúa la elegibilidad de ingresos.",
    address="115 S. 15th Street, Suite 400", city="Richmond", phone="804-648-1012", email="",
    website="https://cvlas.org",
    eligibility="Low-income residents of the CVLAS service area or people with legal problems arising there; LSC income guidelines generally apply.",
    eligibility_es="Residentes de bajos ingresos del área de servicio de CVLAS o personas con problemas legales surgidos allí; generalmente aplican las pautas de ingresos LSC.",
    notes="Call Richmond 804-648-1012 or toll-free 800-868-1012; Charlottesville 434-296-8851 or 800-390-9982; Petersburg 804-862-1100; online intake available at cvlas.org.",
    notes_es="Llame a Richmond al 804-648-1012 o gratis al 800-868-1012; Charlottesville 434-296-8851 u 800-390-9982; Petersburg 804-862-1100; admisión en línea disponible en cvlas.org.",
    hours="Intake Monday–Friday business hours",
    tags="richmond|petersburg|charlottesville|legal-aid|eviction|benefits|low-income",
    services="Housing and eviction defense|Public benefits advocacy|Family law assistance|Consumer protection|Expungement-related civil help",
    county="Richmond City",
    served_counties="Richmond City|Petersburg|Hopewell|Colonial Heights|Charlottesville|Albemarle|Charles City|Chesterfield|Dinwiddie|Fluvanna|Goochland|Greene|Hanover|Henrico|Louisa|Nelson|New Kent|Powhatan|Prince George|Surry",
    coverage="multi",
    _source="https://cvlas.org/get-help", _source_type="nonprofit", _confidence="high",
)
add(
    name="Neighborhood Health — Northern Virginia FQHC",
    category="healthcare", region="Northern Virginia",
    description="Neighborhood Health is Northern Virginia's leading federally qualified health center, serving more than 40,000 patients at 15 clinics across Alexandria, Arlington, and Fairfax County. Services include adult primary care, pediatrics, dental care, behavioral health, and pharmacy assistance, with sliding fee discounts for uninsured and underinsured patients and help enrolling in Medicaid. Returning citizens without coverage can establish primary and behavioral health care regardless of ability to pay.",
    description_es="Neighborhood Health es el principal centro de salud calificado federalmente del norte de Virginia, y atiende a más de 40,000 pacientes en 15 clínicas en Alexandria, Arlington y el condado de Fairfax. Los servicios incluyen atención primaria para adultos, pediatría, atención dental, salud conductual y asistencia de farmacia, con descuentos de tarifa móvil para pacientes sin seguro y ayuda para inscribirse en Medicaid. Los ciudadanos que regresan sin cobertura pueden establecer atención primaria y conductual sin importar su capacidad de pago.",
    address="2 East Glebe Road", city="Alexandria", phone="", email="",
    website="https://neighborhoodhealthva.org",
    eligibility="Open to all Northern Virginia residents regardless of insurance status; sliding fee discounts based on household income; Medicaid, Medicare, and most private insurance accepted.",
    eligibility_es="Abierto a todos los residentes del norte de Virginia sin importar el estado del seguro; descuentos de tarifa móvil según los ingresos del hogar; se aceptan Medicaid, Medicare y la mayoría de los seguros privados.",
    notes="Find the nearest clinic and appointment lines at neighborhoodhealthva.org; bring proof of income to apply for the sliding fee discount; same-day and next-day appointments available at some sites.",
    notes_es="Encuentre la clínica más cercana y las líneas de citas en neighborhoodhealthva.org; traiga prueba de ingresos para solicitar el descuento de tarifa móvil; algunos sitios ofrecen citas para el mismo día o el siguiente.",
    hours="Clinic hours vary; evening and weekend options at some locations",
    tags="alexandria|arlington|fairfax|healthcare|FQHC|sliding-scale|behavioral-health",
    services="Adult primary care|Behavioral health services|Dental care|Medicaid enrollment help|Pharmacy assistance",
    county="Alexandria", served_counties="Alexandria|Arlington|Fairfax", coverage="multi",
    _source="https://neighborhoodhealthva.org/who-we-are/", _source_type="nonprofit", _confidence="high",
)
add(
    name="Virginia Career Works — Alexandria Center",
    category="employment", region="Northern Virginia",
    description="The Virginia Career Works Alexandria center on Cherokee Avenue is a Northern Virginia American Job Center offering free career counseling, job search assistance, workshops, WIOA training referrals, and access to hiring events for the Alexandria and Arlington area. Job seekers with criminal records receive the same free core services and can ask staff about fair-chance employers, federal bonding, and training scholarships that reduce barriers to reemployment after release.",
    description_es="El centro Virginia Career Works de Alexandria en Cherokee Avenue es un Centro de Empleo Americano del norte de Virginia que ofrece consejería de carrera gratuita, ayuda para buscar empleo, talleres, referencias a capacitación WIOA y acceso a eventos de contratación para el área de Alexandria y Arlington. Los buscadores de empleo con antecedentes penales reciben los mismos servicios básicos gratuitos y pueden preguntar al personal sobre empleadores de segunda oportunidad, fianzas federales y becas de capacitación.",
    address="5520 Cherokee Avenue, Suite 100", city="Alexandria", phone="", email="",
    website="https://virginiacareerworks.com/locations/",
    eligibility="Open to Northern Virginia job seekers including justice-involved individuals; core services are free.",
    eligibility_es="Abierto a buscadores de empleo del norte de Virginia, incluidas personas con antecedentes penales; los servicios básicos son gratuitos.",
    notes="Check current hours through the center locator at virginiacareerworks.com/locations; an Arlington County affiliate site at 2100 Washington Boulevard operates Thursdays only.",
    notes_es="Consulte los horarios actuales en el localizador de centros en virginiacareerworks.com/locations; un sitio afiliado del condado de Arlington en 2100 Washington Boulevard opera solo los jueves.",
    hours="Monday–Friday business hours; confirm via center locator",
    tags="alexandria|arlington|northern-virginia|employment|workforce|WIOA",
    services="Career counseling|Job search assistance|WIOA training referrals|Employment workshops|Hiring events",
    county="Alexandria", served_counties="Alexandria", coverage="single",
    _source="https://virginiacareerworks.com/locations/", _source_type="government", _confidence="high",
)
add(
    name="Virginia Career Works — Prince William Center",
    category="employment", region="Northern Virginia",
    description="The Virginia Career Works Prince William center in Woodbridge is the American Job Center serving greater Prince William County with free job search resources, career coaching, skills assessments, WIOA training referrals, and employer hiring events. Returning citizens in the Prince William, Manassas, and Manassas Park area can use the center's computers and staffed assistance to rebuild work histories, connect with training funds, and reach employers open to fair-chance hiring.",
    description_es="El centro Virginia Career Works de Prince William en Woodbridge es el Centro de Empleo Americano que sirve al área metropolitana del condado de Prince William con recursos gratuitos de búsqueda de empleo, orientación profesional, evaluaciones de habilidades, referencias a capacitación WIOA y eventos de contratación. Los ciudadanos que regresan en el área de Prince William, Manassas y Manassas Park pueden usar las computadoras y la asistencia del personal para reconstruir historiales laborales y llegar a empleadores abiertos a la contratación de segunda oportunidad.",
    address="13370 Minnieville Road", city="Woodbridge", phone="", email="",
    website="https://virginiacareerworks.com/locations/",
    eligibility="Open to job seekers in the Prince William area including justice-involved individuals; core services are free.",
    eligibility_es="Abierto a buscadores de empleo del área de Prince William, incluidas personas con antecedentes penales; los servicios básicos son gratuitos.",
    notes="Check current hours through the center locator at virginiacareerworks.com/locations; register on the Virginia Workforce Connection before visiting.",
    notes_es="Consulte los horarios actuales en el localizador de centros en virginiacareerworks.com/locations; regístrese en Virginia Workforce Connection antes de visitar.",
    hours="Monday–Friday business hours; confirm via center locator",
    tags="prince-william|woodbridge|manassas|employment|workforce|WIOA",
    services="Job search assistance|Career coaching|Skills assessments|WIOA training referrals|Hiring events",
    county="Prince William", served_counties="Prince William|Manassas|Manassas Park", coverage="multi",
    _source="https://virginiacareerworks.com/locations/", _source_type="government", _confidence="high",
)

# Roanoke Valley
add(
    name="TAP — Total Action for Progress Reentry Programs",
    category="reentry-organizations", region="Roanoke Valley & Alleghany Highlands",
    description="Total Action for Progress, the Roanoke Valley's community action agency, runs incarceration reentry programs including Virginia CARES, WINGS for women, and A Second Chance for the Alleghany Highlands. Staff help returning citizens within six months of release with job training and searches, interview preparation, transportation, and rights restoration, connecting participants to TAP's wider housing, education, and financial services. Participants outside the service area may enroll if they can reach a TAP office.",
    description_es="Total Action for Progress, la agencia de acción comunitaria del valle de Roanoke, opera programas de reinserción tras la encarcelación que incluyen Virginia CARES, WINGS para mujeres y A Second Chance para Alleghany Highlands. El personal ayuda a los ciudadanos que regresan dentro de los seis meses posteriores a la liberación con capacitación y búsqueda de empleo, preparación de entrevistas, transporte y restauración de derechos, conectándolos con los servicios más amplios de vivienda, educación y finanzas de TAP.",
    address="302 2nd Street SW", city="Roanoke", phone="540-777-4673", email="info@tapintohope.org",
    website="https://tapintohope.org/program/reentry-program/",
    eligibility="People within six months of release from incarceration, before or after release, living in the Roanoke Valley or Alleghany Highlands service areas or able to travel to a TAP office.",
    eligibility_es="Personas dentro de los seis meses previos o posteriores a la liberación de la encarcelación que viven en el valle de Roanoke o Alleghany Highlands o pueden trasladarse a una oficina de TAP.",
    notes="Call 540-777-4673 (540-777-HOPE) or use the contact form on the reentry program page; ask about WINGS for women and A Second Chance for Alleghany-area residents.",
    notes_es="Llame al 540-777-4673 (540-777-HOPE) o use el formulario de contacto en la página del programa de reinserción; pregunte por WINGS para mujeres y A Second Chance para residentes del área de Alleghany.",
    hours="Monday–Friday business hours",
    tags="roanoke|salem|alleghany|reentry|employment|rights-restoration|women",
    services="Job training and search help|Interview preparation|Transportation assistance|Rights restoration help|Case management",
    county="Roanoke City",
    served_counties="Roanoke City|Roanoke|Salem|Botetourt|Craig|Alleghany|Covington|Buena Vista|Lexington|Rockbridge",
    coverage="multi",
    _source="https://tapintohope.org/program/reentry-program/", _source_type="nonprofit", _confidence="high",
)
add(
    name="TAP This Valley Works — Adult Education & Career Training",
    category="education", region="Roanoke Valley",
    description="This Valley Works is Total Action for Progress's education and career development division, offering GED preparation, adult literacy, employment soft-skills classes, and the Center for Employment Training at the Roanoke Higher Education Center. Programs pair classes and certification preparation with coaches, advisors, and job placement partnerships with local employers, and they are designed for low-income adults including those rebuilding after incarceration. About 500 students graduate each year.",
    description_es="This Valley Works es la división de educación y desarrollo profesional de Total Action for Progress, y ofrece preparación para el GED, alfabetización de adultos, clases de habilidades laborales y el Centro de Capacitación para el Empleo en el Roanoke Higher Education Center. Los programas combinan clases y preparación de certificaciones con tutores, asesores y alianzas de colocación laboral con empleadores locales, y están diseñados para adultos de bajos ingresos, incluidos quienes se reconstruyen tras la encarcelación.",
    address="108 N. Jefferson Street", city="Roanoke", phone="540-777-4673", email="",
    website="https://tapintohope.org",
    eligibility="Low-income adults in the Roanoke Valley seeking GED preparation, literacy help, or career training; program-specific enrollment requirements apply.",
    eligibility_es="Adultos de bajos ingresos del valle de Roanoke que buscan preparación para el GED, ayuda de alfabetización o capacitación profesional; aplican requisitos de inscripción específicos del programa.",
    notes="Call 540-777-4673 to enroll; most classes meet at the Roanoke Higher Education Center; ask about certification test preparation and job placement support.",
    notes_es="Llame al 540-777-4673 para inscribirse; la mayoría de las clases se imparten en el Roanoke Higher Education Center; pregunte por la preparación de exámenes de certificación y el apoyo de colocación laboral.",
    hours="Class schedules vary; office Monday–Friday business hours",
    tags="roanoke|education|GED|adult-education|job-training|reentry",
    services="GED preparation|Adult literacy classes|Employment soft skills|Center for Employment Training|Job placement partnerships",
    county="Roanoke City", served_counties="Roanoke City", coverage="single",
    _source="https://www.education.edu/member/tap-this-valley-works/", _source_type="nonprofit", _confidence="high",
)
add(
    name="Rescue Mission of Roanoke",
    category="basic-needs", region="Roanoke Valley",
    description="The Rescue Mission of Roanoke is a comprehensive crisis intervention center open 365 days a year with 257 low-barrier emergency shelter beds for men, women, and families, three daily community meals open to anyone, a weekly food box distribution, the Fralin Free Clinic, and The Way Forward long-term residential recovery program supported by certified peer recovery specialists. No profession of faith is required to receive meals, shelter, medical care, or other services.",
    description_es="La Rescue Mission de Roanoke es un centro integral de intervención en crisis abierto los 365 días del año, con 257 camas de refugio de emergencia de baja barrera para hombres, mujeres y familias, tres comidas comunitarias diarias abiertas a cualquiera, una distribución semanal de cajas de alimentos, la Clínica Gratuita Fralin y el programa residencial de recuperación a largo plazo The Way Forward apoyado por especialistas certificados en recuperación entre pares. No se requiere profesión de fe para recibir servicios.",
    address="402 Fourth Street SE", city="Roanoke", phone="540-343-7227", email="",
    website="https://rescuemission.net",
    eligibility="Anyone in need may eat at the Mission; shelter guests must participate in case management to continue services; The Way Forward serves adults seeking recovery from substance use disorder.",
    eligibility_es="Cualquier persona necesitada puede comer en la Misión; los huéspedes del refugio deben participar en el manejo de casos para continuar los servicios; The Way Forward atiende a adultos que buscan recuperarse del trastorno por uso de sustancias.",
    notes="Shelter is open 3:00 p.m.–9:00 a.m. with daily intakes; call 540-343-7227; food boxes Wednesdays and Thursdays 1–3 p.m.; Fralin Free Clinic at 321 Tazewell Avenue SE, 540-777-7671.",
    notes_es="El refugio abre de 3:00 p.m. a 9:00 a.m. con admisiones diarias; llame al 540-343-7227; cajas de alimentos miércoles y jueves de 1 a 3 p.m.; Clínica Gratuita Fralin en 321 Tazewell Avenue SE, 540-777-7671.",
    hours="Meals daily; shelter intake daily from 3:00 p.m.; office Monday–Saturday",
    tags="roanoke|basic-needs|shelter|meals|free-clinic|recovery",
    services="Emergency shelter|Daily community meals|Food box distribution|Free medical clinic|Long-term residential recovery",
    county="Roanoke City",
    served_counties="Roanoke City|Roanoke|Salem|Covington|Alleghany|Botetourt|Craig|Floyd|Franklin",
    coverage="multi",
    _source="https://rescuemission.net/faq/", _source_type="nonprofit", _confidence="high",
)
add(
    name="Blue Ridge Legal Services",
    category="legal-aid", region="Shenandoah & Roanoke Valleys",
    description="Blue Ridge Legal Services is the nonprofit legal aid society providing free civil legal assistance to low-income residents of the Shenandoah and Roanoke Valleys through offices in Harrisonburg, Roanoke, Lexington, and Winchester plus a Staunton outreach site. Attorneys handle housing, public benefits, family, and consumer matters that stabilize households after incarceration, and the Roanoke office performs intake for the Legal Aid Society of Roanoke Valley as well. Civil matters only.",
    description_es="Blue Ridge Legal Services es la sociedad de asistencia legal sin fines de lucro que brinda ayuda legal civil gratuita a residentes de bajos ingresos de los valles de Shenandoah y Roanoke mediante oficinas en Harrisonburg, Roanoke, Lexington y Winchester, además de un sitio de atención en Staunton. Los abogados atienden asuntos de vivienda, beneficios públicos, familia y consumidor que estabilizan a los hogares tras la encarcelación, y la oficina de Roanoke realiza la admisión también para la Legal Aid Society of Roanoke Valley. Solo asuntos civiles.",
    address="204 N. High Street", city="Harrisonburg", phone="540-433-1830", email="",
    website="https://brls.org",
    eligibility="Low-income residents of the Shenandoah Valley and Roanoke Valley service area; income eligibility screening required.",
    eligibility_es="Residentes de bajos ingresos del área de servicio de los valles de Shenandoah y Roanoke; se requiere evaluación de elegibilidad de ingresos.",
    notes="Harrisonburg intake 540-433-1830 (Mon–Thu 9 a.m.–12:45 p.m.) or toll-free 800-237-0141; Roanoke office 540-344-2080; Lexington 540-463-7334; online applications accepted at brls.org.",
    notes_es="Admisión en Harrisonburg 540-433-1830 (lun–jue 9 a.m.–12:45 p.m.) o gratis al 800-237-0141; oficina de Roanoke 540-344-2080; Lexington 540-463-7334; se aceptan solicitudes en línea en brls.org.",
    hours="Intake hours vary by office; online application 24/7",
    tags="harrisonburg|roanoke|winchester|lexington|legal-aid|low-income|shenandoah-valley",
    services="Civil legal representation|Housing legal help|Public benefits advocacy|Family law assistance|Consumer protection",
    county="Harrisonburg",
    served_counties="Harrisonburg|Staunton|Waynesboro|Augusta|Highland|Page|Rockingham|Roanoke City|Salem|Bedford|Botetourt|Craig|Franklin|Roanoke|Buena Vista|Covington|Lexington|Alleghany|Bath|Rockbridge|Winchester|Clarke|Frederick|Shenandoah|Warren",
    coverage="multi",
    _source="https://brls.org/areas-served-office-locations/", _source_type="nonprofit", _confidence="high",
)
add(
    name="Virginia Career Works — Roanoke Center",
    category="employment", region="Roanoke Valley",
    description="The Virginia Career Works Roanoke center on South Jefferson Street is the American Job Center for the Roanoke Valley, providing free job search assistance, career coaching, workshops, WIOA training referrals, and hiring events. Staff serve all job seekers, including people returning from incarceration, and can connect returning citizens to fair-chance employers, federal bonding information, and partner programs such as TAP and Virginia CARES located nearby in downtown Roanoke.",
    description_es="El centro Virginia Career Works de Roanoke en South Jefferson Street es el Centro de Empleo Americano del valle de Roanoke, y ofrece ayuda gratuita para buscar empleo, orientación profesional, talleres, referencias a capacitación WIOA y eventos de contratación. El personal atiende a todos los buscadores de empleo, incluidas las personas que regresan de la encarcelación, y puede conectarlos con empleadores de segunda oportunidad, información de fianzas federales y programas aliados como TAP y Virginia CARES en el centro de Roanoke.",
    address="707 South Jefferson Street", city="Roanoke", phone="", email="",
    website="https://virginiacareerworks.com/locations/",
    eligibility="Open to Roanoke Valley job seekers including justice-involved individuals; core services are free.",
    eligibility_es="Abierto a buscadores de empleo del valle de Roanoke, incluidas personas con antecedentes penales; los servicios básicos son gratuitos.",
    notes="Check current hours through the center locator at virginiacareerworks.com/locations; register on the Virginia Workforce Connection before visiting.",
    notes_es="Consulte los horarios actuales en el localizador de centros en virginiacareerworks.com/locations; regístrese en Virginia Workforce Connection antes de visitar.",
    hours="Monday–Friday business hours; confirm via center locator",
    tags="roanoke|employment|workforce|WIOA|fair-chance",
    services="Job search assistance|Career coaching|WIOA training referrals|Employment workshops|Hiring events",
    county="Roanoke City", served_counties="Roanoke City", coverage="single",
    _source="https://virginiacareerworks.com/locations/", _source_type="government", _confidence="high",
)

# Lynchburg
add(
    name="Miriam's House — Lynchburg Housing Programs",
    category="housing", region="Lynchburg",
    description="Miriam's House works to end homelessness in the Lynchburg community through housing-first programs, including a family emergency shelter at 409 Magnolia Street opened in early 2026 and the Community First rapid re-housing program that pairs short-term rental assistance with in-home case management. Households leaving incarceration into homelessness can be screened through the community's centralized intake line. Services focus on families with children, youth, and chronically homeless individuals.",
    description_es="Miriam's House trabaja para acabar con la falta de vivienda en la comunidad de Lynchburg mediante programas de vivienda primero, incluidos un refugio familiar de emergencia en 409 Magnolia Street abierto a inicios de 2026 y el programa de realojamiento rápido Community First, que combina asistencia de renta a corto plazo con manejo de casos en el hogar. Los hogares que salen de la encarcelación hacia la falta de vivienda pueden ser evaluados mediante la línea centralizada de admisión. Se enfoca en familias con niños, jóvenes y personas sin hogar crónicas.",
    address="", city="Lynchburg", phone="434-427-2442", email="",
    website="https://www.miriamshouse.org",
    eligibility="Households experiencing homelessness in the Lynchburg community, with priority programs for families with children, unaccompanied youth, and chronically homeless individuals.",
    eligibility_es="Hogares sin vivienda en la comunidad de Lynchburg, con programas prioritarios para familias con niños, jóvenes no acompañados y personas sin hogar crónicas.",
    notes="Call the centralized homeless intake line (CHIA) at 434-427-2442 to be screened for shelter and housing programs; the family shelter provides case management, housing navigation, and basic needs.",
    notes_es="Llame a la línea centralizada de admisión (CHIA) al 434-427-2442 para ser evaluado para refugio y programas de vivienda; el refugio familiar ofrece manejo de casos, navegación de vivienda y necesidades básicas.",
    hours="Intake line business hours; shelter operates 24/7",
    tags="lynchburg|housing|shelter|rapid-rehousing|families|homeless",
    services="Family emergency shelter|Rapid re-housing assistance|In-home case management|Housing navigation|Homelessness prevention",
    county="Lynchburg", served_counties="Lynchburg", coverage="single",
    _source="https://www.miriamshouse.org/our-work", _source_type="nonprofit", _confidence="high",
)
add(
    name="Virginia Career Works — Lynchburg Center",
    category="employment", region="Lynchburg region",
    description="The Virginia Career Works Lynchburg center on Odd Fellows Road is the American Job Center for the Lynchburg region, offering free job search help, career coaching, skills workshops, WIOA-funded training referrals, and connections to area employers. People with criminal records returning to Lynchburg and surrounding counties can use center computers, get help explaining their history to employers, and ask about fair-chance hiring, federal bonding, and GED and training partners.",
    description_es="El centro Virginia Career Works de Lynchburg en Odd Fellows Road es el Centro de Empleo Americano de la región de Lynchburg, y ofrece ayuda gratuita de búsqueda de empleo, orientación profesional, talleres de habilidades, referencias a capacitación financiada por WIOA y conexiones con empleadores del área. Las personas con antecedentes penales que regresan a Lynchburg y los condados circundantes pueden usar las computadoras del centro, recibir ayuda para explicar su historial a los empleadores y preguntar sobre contratación de segunda oportunidad y fianzas federales.",
    address="3125 Odd Fellows Road", city="Lynchburg", phone="", email="",
    website="https://virginiacareerworks.com/locations/",
    eligibility="Open to Lynchburg-region job seekers including justice-involved individuals; core services are free.",
    eligibility_es="Abierto a buscadores de empleo de la región de Lynchburg, incluidas personas con antecedentes penales; los servicios básicos son gratuitos.",
    notes="Check current hours through the center locator at virginiacareerworks.com/locations; register on the Virginia Workforce Connection before visiting.",
    notes_es="Consulte los horarios actuales en el localizador de centros en virginiacareerworks.com/locations; regístrese en Virginia Workforce Connection antes de visitar.",
    hours="Monday–Friday business hours; confirm via center locator",
    tags="lynchburg|employment|workforce|WIOA|fair-chance",
    services="Job search assistance|Career coaching|WIOA training referrals|Skills workshops|Employer connections",
    county="Lynchburg", served_counties="Lynchburg", coverage="single",
    _source="https://virginiacareerworks.com/locations/", _source_type="government", _confidence="high",
)

# Charlottesville
add(
    name="The Haven — Charlottesville Day Shelter & Housing",
    category="basic-needs", region="Charlottesville & Albemarle",
    description="The Haven is a low-barrier day shelter at 112 West Market Street in downtown Charlottesville, open every morning of the year with breakfast, showers, laundry, a mailing address, storage, and computer access for anyone experiencing homelessness—including people just released from incarceration with nowhere to go. The Haven also administers Housing First programs (rapid re-housing, homelessness prevention, and a housing fund) and runs the region's coordinated entry Homeless Information Line.",
    description_es="The Haven es un refugio diurno de baja barrera en 112 West Market Street en el centro de Charlottesville, abierto todas las mañanas del año con desayuno, duchas, lavandería, dirección postal, almacenamiento y acceso a computadoras para cualquier persona sin hogar—incluidas personas recién liberadas de la encarcelación sin dónde ir. The Haven también administra programas de Vivienda Primero (realojamiento rápido, prevención de la falta de vivienda y un fondo de vivienda) y opera la Línea de Información para Personas sin Hogar de entrada coordinada de la región.",
    address="112 West Market Street", city="Charlottesville", phone="434-973-1234", email="operations@thehaven.org",
    website="https://www.thehaven.org",
    eligibility="Day shelter open to anyone in need; housing program screening requires literal homelessness or imminent housing loss per coordinated entry criteria.",
    eligibility_es="Refugio diurno abierto a cualquier persona necesitada; la evaluación para programas de vivienda requiere falta de vivienda literal o pérdida inminente de vivienda según los criterios de entrada coordinada.",
    notes="Day shelter open Mon–Fri 7 a.m.–5 p.m. and weekends 7 a.m.–noon; for housing screening call the Homeless Information Line at 434-207-2328 and leave a voicemail; for overnight shelter see PACEM.",
    notes_es="Refugio diurno abierto lun–vie de 7 a.m. a 5 p.m. y fines de semana de 7 a.m. a mediodía; para evaluación de vivienda llame a la Línea de Información al 434-207-2328 y deje un mensaje de voz; para refugio nocturno consulte PACEM.",
    hours="Monday–Friday, 7:00 a.m.–5:00 p.m.; Saturday–Sunday, 7:00 a.m.–12:00 p.m.",
    tags="charlottesville|albemarle|basic-needs|day-shelter|housing|homeless",
    services="Day shelter services|Showers and laundry|Mailing address|Rapid re-housing programs|Coordinated entry screening",
    county="Charlottesville",
    served_counties="Charlottesville|Albemarle|Fluvanna|Greene|Louisa|Nelson",
    coverage="multi",
    _source="https://search.211virginia.org/search/b48ecec5-9a1b-5ab0-9c0b-b313f70471ac", _source_type="directory", _confidence="high",
)
add(
    name="Virginia Career Works — Charlottesville Center",
    category="employment", region="Charlottesville & Albemarle",
    description="The Virginia Career Works Charlottesville center at Glenwood Station is the American Job Center for the Charlottesville area, offering free job search assistance, career coaching, workshops, WIOA training referrals, and employer hiring events. Justice-involved job seekers returning to Charlottesville and surrounding counties can access the same free services and ask staff about fair-chance employers, federal bonding, and reentry partners such as OAR and the Fountain Fund in the region.",
    description_es="El centro Virginia Career Works de Charlottesville en Glenwood Station es el Centro de Empleo Americano del área de Charlottesville, y ofrece ayuda gratuita de búsqueda de empleo, orientación profesional, talleres, referencias a capacitación WIOA y eventos de contratación con empleadores. Los buscadores de empleo con antecedentes penales que regresan a Charlottesville y los condados circundantes pueden acceder a los mismos servicios gratuitos y preguntar al personal sobre empleadores de segunda oportunidad, fianzas federales y aliados de reinserción de la región.",
    address="944 Glenwood Station Lane, Suite 103", city="Charlottesville", phone="", email="",
    website="https://virginiacareerworks.com/locations/",
    eligibility="Open to Charlottesville-area job seekers including justice-involved individuals; core services are free.",
    eligibility_es="Abierto a buscadores de empleo del área de Charlottesville, incluidas personas con antecedentes penales; los servicios básicos son gratuitos.",
    notes="Check current hours through the center locator at virginiacareerworks.com/locations; register on the Virginia Workforce Connection before visiting.",
    notes_es="Consulte los horarios actuales en el localizador de centros en virginiacareerworks.com/locations; regístrese en Virginia Workforce Connection antes de visitar.",
    hours="Monday–Friday business hours; confirm via center locator",
    tags="charlottesville|albemarle|employment|workforce|WIOA|fair-chance",
    services="Job search assistance|Career coaching|WIOA training referrals|Employment workshops|Hiring events",
    county="Charlottesville", served_counties="Charlottesville", coverage="single",
    _source="https://virginiacareerworks.com/locations/", _source_type="government", _confidence="high",
)

# County DSS benefits offices (mechanical rows from sync + registry).
from county_benefits_registry import register_county_benefits_virginia

_existing_fa = {
    e["county"]
    for e in ENTRIES
    if e["category"] == "financial-assistance" and e.get("county")
}
register_county_benefits_virginia(add, _existing_fa)

# Phase 4 expansion — housing, healthcare, SUD, peer support, basic needs, family, transportation.
from virginia_phase4_expansion import register_phase4

register_phase4(add)

# Category minimum fill — probation-parole, legal-aid, education, veterans, etc.
from virginia_category_fill import register_category_fill

register_category_fill(add)

# Thin-locality depth — second pin beyond DSS for rural Tier A counties.
from virginia_thin_counties import register_thin_counties

register_thin_counties(add)

from virginia_tier_a_closure import register_tier_a_closure
register_tier_a_closure(add)

# Phase 3b gap-fill is wired here in a later pass:
# from phase3b_gapfill import register_phase3b_virginia
# register_phase3b_virginia(add, ENTRIES)


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
