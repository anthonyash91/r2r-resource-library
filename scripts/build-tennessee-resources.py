#!/usr/bin/env python3
"""Generate tennessee-resources.csv and tennessee-research-log.csv."""
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES_PATH = ROOT / "data" / "tennessee-resources.csv"
LOG_PATH = ROOT / "data" / "tennessee-research-log.csv"
DATE = "2026-06-22"

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
    name="TDOC — Reentry Services",
    category="state-agency", region="Statewide",
    description="The Tennessee Department of Correction Reentry Office coordinates statewide transition planning and connects people in custody or under community supervision with identification, employment, housing, veterans benefits, and local partners. Director Victoria Ricci's team supports pre-release readiness and community resource navigation across Tennessee. This office provides planning and referrals—not emergency crisis response.",
    description_es="La Oficina de Reinserción del Departamento de Corrección de Tennessee coordina la planificación estatal de transición y conecta a personas en custodia o bajo supervisión comunitaria con identificación, empleo, vivienda, beneficios para veteranos y aliados locales. El equipo de la directora Victoria Ricci apoya la preparación previa a la liberación en todo el estado. Esta oficina ofrece planificación y referencias, no respuesta de crisis.",
    address="320 Sixth Avenue North", city="Nashville", phone="629-203-0151",
    email="Victoria.R.Ricci@tn.gov", website="https://www.tn.gov/correction/redirect---rehabilitation/reentry-services.html",
    eligibility="Generally serves Tennessee residents under TDOC custody, parole, probation, or seeking state reentry coordination.",
    eligibility_es="Generalmente sirve a residentes de Tennessee bajo custodia del TDOC, libertad condicional, libertad probatoria o que buscan coordinación estatal de reinserción.",
    notes="Contact Director Victoria Ricci at 629-203-0151 or Victoria.R.Ricci@tn.gov; see tn.gov/correction for TREC regional contacts and approved transitional housing lists.",
    notes_es="Contacte a la directora Victoria Ricci al 629-203-0151; consulte tn.gov/correction para contactos regionales TREC y listas de vivienda transicional aprobada.",
    hours="Monday–Friday, 8:00 a.m.–4:30 p.m. CT",
    tags="statewide|reentry|DOC|probation|parole|hotline",
    services="Reentry planning coordination|ID and vital records assistance|Employment and housing referrals|Veterans benefits navigation",
    county="Davidson", served_counties="", coverage="statewide",
    _source="https://www.tn.gov/correction/redirect---rehabilitation/reentry-services.html", _source_type="government", _confidence="high",
)
add(
    name="Tennessee Office of Offender Reentry (TOOR)",
    category="employment", region="Statewide",
    description="State workforce initiative connecting justice-involved Tennesseans to employment, training, and employer partnerships through American Job Centers and the Jobs4TN platform. TOOR coordinates fair-chance hiring outreach and links probation and parole officers to employment specialists statewide. An employment navigation program—not emergency housing or crisis services.",
    description_es="Iniciativa estatal de fuerza laboral que conecta a personas con antecedentes penales en Tennessee con empleo, capacitación y aliados empleadores a través de Centros de Empleo Americanos y la plataforma Jobs4TN. TOOR coordina contratación de segunda oportunidad y vincula oficiales de libertad condicional con especialistas en empleo. Es un programa de navegación laboral, no de vivienda de emergencia.",
    address="220 French Landing Drive", city="Nashville", phone="",
    email="Reentry@tn.gov", website="https://www.tn.gov/workforce/reentrytn.html",
    eligibility="Justice-involved Tennessee residents seeking employment after incarceration or under community supervision; contact regional workforce partners for intake.",
    eligibility_es="Residentes de Tennessee con antecedentes penales que buscan empleo después de la encarcelación o bajo supervisión comunitaria; contacte aliados regionales de fuerza laboral.",
    notes="Email Reentry@tn.gov or visit tn.gov/workforce/reentrytn; probation officers may refer supervisees to local American Job Centers and Jobs4TN.gov.",
    notes_es="Envíe correo a Reentry@tn.gov o visite tn.gov/workforce/reentrytn; los oficiales de libertad condicional pueden referir a Centros de Empleo locales.",
    hours="Contact regional workforce board for hours",
    tags="statewide|employment|reentry|fair-chance|Jobs4TN",
    services="Employment specialist referrals|Jobs4TN registration|Employer partnership navigation|Pre-release job readiness coordination",
    county="Davidson", served_counties="", coverage="statewide",
    _source="https://www.tn.gov/workforce/reentrytn.html", _source_type="government", _confidence="high",
)
add(
    name="Tennessee Reentry Collaborative (TREC)",
    category="reentry-organizations", region="Statewide",
    description="TDOC initiative uniting state, local, and nonprofit agencies to build community pathways for parolees, probationers, and returning citizens across Tennessee. TREC regional administrators coordinate coalitions, resource fairs, and partner referrals in East, Middle, and West regions. A collaborative network—not a direct-service crisis provider.",
    description_es="Iniciativa del TDOC que une agencias estatales, locales y sin fines de lucro para crear caminos comunitarios para personas en libertad condicional y ciudadanos que regresan en Tennessee. Los administradores regionales TREC coordinan coaliciones, ferias de recursos y referencias en las regiones Este, Central y Oeste. Es una red colaborativa, no un proveedor directo de crisis.",
    address="320 Sixth Avenue North", city="Nashville", phone="",
    email="Reentry.Collaborative@tn.gov", website="https://www.tn.gov/correction/redirect---rehabilitation/tennessee-reentry-collaborative--trec-.html",
    eligibility="Justice-involved Tennessee residents and community partners seeking local reentry coalition connections.",
    eligibility_es="Residentes de Tennessee con antecedentes penales y aliados comunitarios que buscan conexiones con coaliciones locales de reinserción.",
    notes="Contact East Sara Hodges 423-353-0971, Middle Shaundra Davis 615-587-5639, or West April Buckner 901-229-8024 for regional coalition information.",
    notes_es="Contacte Este Sara Hodges 423-353-0971, Centro Shaundra Davis 615-587-5639 u Oeste April Buckner 901-229-8024 para información regional.",
    hours="Regional administrators Monday–Friday business hours",
    tags="statewide|reentry|coalition|TREC|referral-only",
    services="Regional coalition coordination|Community partner networking|Reentry resource fairs|Local referral navigation",
    county="Davidson", served_counties="", coverage="statewide",
    _source="https://www.tn.gov/correction/redirect---rehabilitation/tennessee-reentry-collaborative--trec-.html", _source_type="government", _confidence="high",
)
add(
    name="TREC — East Region",
    category="reentry-organizations", region="East Tennessee",
    description="Tennessee Reentry Collaborative East Region administrator connecting justice-involved residents in upper East Tennessee and the Tri-Cities to local reentry coalitions, TDOC community supervision partners, and employment resources. Sara Hodges coordinates regional outreach and community agency partnerships for successful reintegration. Contact for coalition referrals—not emergency housing or crisis response.",
    description_es="Administradora regional TREC del Este que conecta a residentes con antecedentes penales en el este alto de Tennessee y las Tri-Cities con coaliciones locales de reinserción, aliados de supervisión comunitaria del TDOC y recursos de empleo. Sara Hodges coordina alcance regional y alianzas comunitarias. Contacte para referencias de coalición, no para vivienda de emergencia.",
    address="", city="Knoxville", phone="423-353-0971",
    email="Sara.Hodges@tn.gov", website="https://www.tn.gov/correction/redirect---rehabilitation/tennessee-reentry-collaborative--trec-.html",
    eligibility="Justice-involved residents in TDOC East Region counties; community partners seeking TREC engagement.",
    eligibility_es="Residentes con antecedentes penales en condados de la región Este del TDOC; aliados comunitarios que buscan participar en TREC.",
    notes="Correctional Administrator Sara Hodges serves East Tennessee; email Sara.Hodges@tn.gov for coalition and partner referrals.",
    notes_es="La administradora correccional Sara Hodges sirve el este de Tennessee; envíe correo a Sara.Hodges@tn.gov para referencias.",
    hours="Monday–Friday business hours",
    tags="east-tennessee|reentry|coalition|TREC|referral-only",
    services="East region coalition coordination|Community partner referrals|Reentry outreach|TDOC partner networking",
    county="Knox", served_counties="", coverage="statewide",
    _source="https://www.tn.gov/correction/redirect---rehabilitation/tennessee-reentry-collaborative--trec-.html", _source_type="government", _confidence="high",
)
add(
    name="TREC — Middle Region",
    category="reentry-organizations", region="Middle Tennessee",
    description="Tennessee Reentry Collaborative Middle Region administrator linking justice-involved residents in Nashville, Murfreesboro, Clarksville, and surrounding counties to local reentry partners, Day Reporting Centers, and workforce programs. Shaundra Davis coordinates regional coalition activity and community supervision reentry supports. Contact for regional navigation—not a walk-in crisis line.",
    description_es="Administradora regional TREC del Centro que vincula a residentes con antecedentes penales en Nashville, Murfreesboro, Clarksville y condados circundantes con aliados locales de reinserción, Centros de Reporte Diurno y programas de fuerza laboral. Shaundra Davis coordina actividad de coalición regional. Contacte para navegación regional, no es una línea de crisis.",
    address="", city="Nashville", phone="615-587-5639",
    email="Shaundra.D.Davis@tn.gov", website="https://www.tn.gov/correction/redirect---rehabilitation/tennessee-reentry-collaborative--trec-.html",
    eligibility="Justice-involved residents in TDOC Middle Region counties; community partners seeking TREC engagement.",
    eligibility_es="Residentes con antecedentes penales en condados de la región Central del TDOC; aliados comunitarios que buscan participar en TREC.",
    notes="Correctional Administrator Shaundra Davis serves Middle Tennessee including Davidson and Rutherford counties.",
    notes_es="La administradora correccional Shaundra Davis sirve el centro de Tennessee incluyendo los condados Davidson y Rutherford.",
    hours="Monday–Friday business hours",
    tags="middle-tennessee|reentry|coalition|TREC|nashville",
    services="Middle region coalition coordination|DRC partner referrals|Workforce reentry navigation|Community agency networking",
    county="Davidson", served_counties="", coverage="statewide",
    _source="https://www.tn.gov/correction/redirect---rehabilitation/tennessee-reentry-collaborative--trec-.html", _source_type="government", _confidence="high",
)
add(
    name="TREC — West Region",
    category="reentry-organizations", region="West Tennessee",
    description="Tennessee Reentry Collaborative West Region administrator connecting justice-involved residents in Memphis, Jackson, and West Tennessee to MSCOR, local coalitions, and employment partners. April Buckner coordinates regional reentry outreach and links supervisees to community resource centers and fair-chance employers. Contact for regional referrals—not emergency services.",
    description_es="Administradora regional TREC del Oeste que conecta a residentes con antecedentes penales en Memphis, Jackson y el oeste de Tennessee con MSCOR, coaliciones locales y aliados de empleo. April Buckner coordina alcance regional de reinserción y vincula supervisados con centros de recursos comunitarios. Contacte para referencias regionales, no para servicios de emergencia.",
    address="", city="Memphis", phone="901-229-8024",
    email="April.Buckner@tn.gov", website="https://www.tn.gov/correction/redirect---rehabilitation/tennessee-reentry-collaborative--trec-.html",
    eligibility="Justice-involved residents in TDOC West Region counties; community partners seeking TREC engagement.",
    eligibility_es="Residentes con antecedentes penales en condados de la región Oeste del TDOC; aliados comunitarios que buscan participar en TREC.",
    notes="Correctional Administrator April Buckner serves West Tennessee including Shelby and Madison counties; partners with MSCOR in Memphis.",
    notes_es="La administradora correccional April Buckner sirve el oeste de Tennessee incluyendo Shelby y Madison; aliada con MSCOR en Memphis.",
    hours="Monday–Friday business hours",
    tags="west-tennessee|reentry|coalition|TREC|memphis",
    services="West region coalition coordination|MSCOR partner referrals|Employment reentry navigation|Community resource connections",
    county="Shelby", served_counties="", coverage="statewide",
    _source="https://www.tn.gov/correction/redirect---rehabilitation/tennessee-reentry-collaborative--trec-.html", _source_type="government", _confidence="high",
)
add(
    name="Tennessee 211",
    category="state-agency", region="Statewide",
    description="Free statewide information and referral service connecting Tennesseans to health and human services including housing, food, utilities, employment, and crisis support. United Way–supported navigators help callers find local programs by need and ZIP code. Tennessee 211 is a referral line—not a direct-service provider.",
    description_es="Servicio gratuito de información y referencia en todo el estado que conecta a los habitantes de Tennessee con servicios de salud y humanos incluyendo vivienda, alimentos, empleo y apoyo en crisis. Navegadores apoyados por United Way ayudan a encontrar programas locales. Tennessee 211 es una línea de referencia, no un proveedor directo.",
    address="", city="", phone="211", email="", website="https://www.uwtn.org/tn-211",
    eligibility="Open to all Tennessee residents; no criminal-record restrictions stated.",
    eligibility_es="Abierto a todos los residentes de Tennessee; sin restricciones de antecedentes indicadas.",
    notes="Dial 211 from any Tennessee phone; search resources online at uwtn.org/tn-211; available 24/7 for information and referral.",
    notes_es="Marque 211 desde cualquier teléfono de Tennessee; busque recursos en línea en uwtn.org/tn-211; disponible 24/7.",
    hours="Available 24/7",
    tags="statewide|hotline|211|referral-only|basic-needs",
    services="Information and referral|Housing resource navigation|Benefits referrals|Crisis resource connections",
    county="", served_counties="", coverage="statewide",
    _source="https://www.uwtn.org/tn-211", _source_type="nonprofit", _confidence="high",
)
add(
    name="988 Suicide & Crisis Lifeline — Tennessee",
    category="healthcare", region="Statewide",
    description="Free confidential 24/7 crisis support for people experiencing mental health emergencies, suicidal thoughts, or substance use crises. Trained specialists provide immediate support and can connect callers to local mobile crisis teams in Tennessee. Available to anyone—not reentry-specific but essential for justice-involved individuals in crisis.",
    description_es="Apoyo gratuito y confidencial 24/7 para emergencias de salud mental, pensamientos suicidas o crisis por uso de sustancias. Especialistas capacitados ofrecen apoyo inmediato y conexión a equipos de crisis móviles en Tennessee. Disponible para cualquier persona, esencial para personas con antecedentes penales en crisis.",
    address="", city="", phone="988", email="",
    website="https://988lifeline.org",
    eligibility="Open to anyone in Tennessee experiencing a mental health or suicide crisis; no eligibility restrictions.",
    eligibility_es="Abierto a cualquier persona en Tennessee en crisis de salud mental o suicidio; sin restricciones.",
    notes="Call or text 988; Spanish-language support available. For immediate physical danger call 911.",
    notes_es="Llame o envíe texto al 988; soporte en español disponible. Para peligro físico inmediato llame al 911.",
    hours="Available 24/7",
    tags="statewide|hotline|crisis|mental-health|988",
    services="Crisis counseling|Suicide prevention support|Mental health referrals|Substance use crisis support",
    county="", served_counties="", coverage="statewide",
    _source="https://988lifeline.org", _source_type="government", _confidence="high",
)
add(
    name="Help4TN — Legal & Social Services Helpline",
    category="legal-aid", region="Statewide",
    description="Free statewide helpline operated by Tennessee Alliance for Legal Services connecting low-income residents to civil legal aid, benefits information, and social service referrals. Specialists help callers understand options for housing, family law, consumer issues, and finding local attorneys. A referral and information line—not a criminal defense provider.",
    description_es="Línea de ayuda gratuita en todo el estado operada por Tennessee Alliance for Legal Services que conecta a residentes de bajos ingresos con asistencia legal civil, información de beneficios y referencias de servicios sociales. Los especialistas ayudan con opciones de vivienda, derecho familiar y búsqueda de abogados locales. Es una línea de referencia, no defensa penal.",
    address="", city="Nashville", phone="844-435-7486", email="",
    website="https://www.help4tn.org",
    eligibility="Open to Tennessee residents seeking civil legal information and referrals; direct representation eligibility varies by local legal aid provider.",
    eligibility_es="Abierto a residentes de Tennessee que buscan información legal civil y referencias; la representación directa varía según el proveedor local.",
    notes="Call 844-435-7486 or chat at help4tn.org; connects callers to LAS, LAET, WTLS, and MALS regional offices by county.",
    notes_es="Llame al 844-435-7486 o use el chat en help4tn.org; conecta con oficinas regionales LAS, LAET, WTLS y MALS según el condado.",
    hours="Monday–Friday business hours; online chat available",
    tags="statewide|legal-aid|hotline|referral-only|benefits",
    services="Legal aid referrals|Benefits information|Social service navigation|County legal aid routing",
    county="", served_counties="", coverage="statewide",
    _source="https://www.help4tn.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Legal Aid Society of Middle Tennessee — Statewide Intake",
    category="legal-aid", region="Statewide",
    description="Nonprofit civil legal aid provider serving low-income residents across 48 Middle Tennessee counties with housing, benefits, family law, consumer issues, and civil record-related matters. Centralized intake at 800-238-1443 connects callers to Nashville, Murfreesboro, Columbia, and Cookeville offices. Does not handle criminal defense cases.",
    description_es="Proveedor sin fines de lucro de asistencia legal civil que sirve a residentes de bajos ingresos en 48 condados del centro de Tennessee con vivienda, beneficios, derecho familiar y asuntos civiles relacionados con antecedentes. La admisión centralizada al 800-238-1443 conecta con oficinas regionales. No maneja defensa penal.",
    address="1321 Murfreesboro Pike, Suite 400", city="Nashville", phone="800-238-1443",
    email="", website="https://las.org",
    eligibility="Low-income Tennessee residents in service area with non-criminal legal problems; income and household-size limits apply.",
    eligibility_es="Residentes de bajos ingresos en el área de servicio con problemas legales no penales; aplican límites de ingresos.",
    notes="Call 800-238-1443 before visiting; appointment required for attorney meetings; apply online at las.org/get-help.",
    notes_es="Llame al 800-238-1443 antes de visitar; se requiere cita para reuniones con abogados; solicite en línea en las.org.",
    hours="Intake phone Monday–Friday business hours; online application 24/7",
    tags="statewide|legal-aid|low-income|housing|hotline",
    services="Civil legal representation|Housing legal aid|Benefits advocacy|Eviction defense|Regional office referrals",
    county="Davidson", served_counties="", coverage="statewide",
    _source="https://las.org/get-help/", _source_type="nonprofit", _confidence="high",
)
add(
    name="Legal Aid of East Tennessee — Statewide Intake",
    category="legal-aid", region="Statewide",
    description="Nonprofit civil legal aid serving low-income residents in 26 East Tennessee counties including Knoxville, Chattanooga, Johnson City, and the Tri-Cities with housing, benefits, domestic violence, and consumer legal matters. Knoxville office intake at 865-637-0484; eviction hotline 866-333-1505 for eligible counties. Does not provide criminal defense.",
    description_es="Asistencia legal civil sin fines de lucro para residentes de bajos ingresos en 26 condados del este de Tennessee incluyendo Knoxville, Chattanooga y Johnson City con vivienda, beneficios y violencia doméstica. Admisión en Knoxville al 865-637-0484; línea de desalojo 866-333-1505. No proporciona defensa penal.",
    address="607 West Summit Hill Drive SW", city="Knoxville", phone="865-637-0484",
    email="", website="https://www.laet.org",
    eligibility="Low-income residents in 26-county East Tennessee service area; income limits apply by federal LSC guidelines.",
    eligibility_es="Residentes de bajos ingresos en el área de 26 condados del este de Tennessee; aplican límites de ingresos federales.",
    notes="Apply online at laet.org or call county office; eviction hotline 866-333-1505 for landlord-tenant emergencies in listed counties.",
    notes_es="Solicite en línea en laet.org o llame a la oficina del condado; línea de desalojo 866-333-1505 para emergencias de arrendador-inquilino.",
    hours="Office hours vary by location; online application 24/7",
    tags="statewide|legal-aid|east-tennessee|eviction|low-income",
    services="Civil legal representation|Eviction prevention|Benefits advocacy|Domestic violence legal aid|Regional office referrals",
    county="Knox", served_counties="", coverage="statewide",
    _source="https://www.laet.org/contact-us/", _source_type="nonprofit", _confidence="high",
)
add(
    name="West Tennessee Legal Services — Statewide Intake",
    category="legal-aid", region="Statewide",
    description="Nonprofit civil legal aid serving 17 West Tennessee counties including Memphis, Jackson, and surrounding rural communities with housing, benefits, family law, and consumer matters affecting reentry stability. Call 800-372-8346 for intake; Memphis-area cases served from regional offices. Does not handle criminal cases.",
    description_es="Asistencia legal civil sin fines de lucro en 17 condados del oeste de Tennessee incluyendo Memphis y Jackson con vivienda, beneficios y derecho familiar que afectan la estabilidad en reinserción. Llame al 800-372-8346 para admisión. No maneja casos penales.",
    address="210 West Tennessee Street", city="Jackson", phone="800-372-8346",
    email="", website="https://www.wtls.org",
    eligibility="Low-income residents in WTLS 17-county service area; veterans and seniors may qualify with higher income limits.",
    eligibility_es="Residentes de bajos ingresos en el área de 17 condados de WTLS; veteranos y personas mayores pueden calificar con límites más altos.",
    notes="Call 800-372-8346 for intake; WTLS assumed Shelby County civil cases after mid-2024; verify county coverage at wtls.org.",
    notes_es="Llame al 800-372-8346 para admisión; WTLS asumió casos civiles del condado Shelby después de mediados de 2024.",
    hours="Intake Monday–Friday business hours",
    tags="statewide|legal-aid|west-tennessee|memphis|low-income",
    services="Civil legal representation|Housing legal aid|Benefits advocacy|Family law assistance|Consumer legal help",
    county="Madison", served_counties="", coverage="statewide",
    _source="https://www.wtls.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Memphis Area Legal Services — Intake",
    category="legal-aid", region="Memphis / Shelby County",
    description="Nonprofit civil legal aid historically serving Shelby County low-income residents with housing, domestic violence, foreclosure, and benefits matters. Verify current intake routing with Help4TN or WTLS as West Tennessee Legal Services expanded Memphis-area coverage in 2024. Does not provide criminal defense representation.",
    description_es="Asistencia legal civil sin fines de lucro que históricamente sirvió a residentes de bajos ingresos del condado Shelby con vivienda, violencia doméstica y beneficios. Verifique la admisión actual con Help4TN o WTLS ya que West Tennessee Legal Services amplió cobertura en Memphis en 2024. No proporciona defensa penal.",
    address="22 North Front Street, Suite 900", city="Memphis", phone="901-523-8822",
    email="", website="https://malsi.org",
    eligibility="Low-income Shelby County residents with qualifying civil legal problems; contact intake for current eligibility and routing.",
    eligibility_es="Residentes de bajos ingresos del condado Shelby con problemas legales civiles calificados; contacte admisión para elegibilidad actual.",
    notes="Call 901-523-8822 or Help4TN 844-435-7486 to confirm current intake path; WTLS may handle some Shelby County matters.",
    notes_es="Llame al 901-523-8822 o Help4TN 844-435-7486 para confirmar la ruta de admisión actual.",
    hours="Intake Monday–Friday business hours",
    tags="memphis|shelby|legal-aid|low-income|housing",
    services="Civil legal representation|Housing legal aid|Domestic violence legal help|Benefits advocacy",
    county="Shelby", served_counties="Shelby", coverage="single",
    _source="https://malsi.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="TN Department of Human Services — Benefits Portal",
    category="financial-assistance", region="Statewide",
    description="Official statewide portal for applying for and managing Tennessee public benefits including TennCare Medicaid, SNAP food assistance, TANF cash assistance, and child care subsidies. Justice-involved individuals can apply for health coverage and food support after release. County DHS offices assist with verification and redetermination.",
    description_es="Portal oficial estatal para solicitar y administrar beneficios públicos de Tennessee incluyendo TennCare Medicaid, SNAP, TANF y subsidios de cuidado infantil. Personas en reinserción pueden solicitar cobertura de salud y apoyo alimentario después de la liberación. Las oficinas DHS del condado ayudan con verificación.",
    address="", city="", phone="866-311-4287", email="", website="https://www.tn.gov/humanservices/for-families/tenncare.html",
    eligibility="Tennessee residents meeting income and program requirements for TennCare, SNAP, TANF, or child care; criminal record generally not a barrier.",
    eligibility_es="Residentes de Tennessee que cumplan requisitos de ingresos para TennCare, SNAP, TANF o cuidado infantil; antecedentes penales generalmente no son barrera.",
    notes="Apply online at tn.gov/humanservices; call 866-311-4287 for TennCare or county DHS office for SNAP and TANF assistance.",
    notes_es="Solicite en línea en tn.gov/humanservices; llame al 866-311-4287 para TennCare o a la oficina DHS del condado para SNAP y TANF.",
    hours="Online 24/7; county office hours vary",
    tags="statewide|benefits|SNAP|TennCare|online",
    services="Medicaid application|SNAP enrollment|Cash assistance application|Benefits account management",
    county="", served_counties="", coverage="statewide",
    _source="https://www.tn.gov/humanservices/for-families/tenncare.html", _source_type="government", _confidence="high",
)
add(
    name="Tennessee Department of Safety & Homeland Security — Driver Services",
    category="id-documentation", region="Statewide",
    description="State agency providing REAL ID–compliant driver's licenses, photo identification cards, and reinstatement services at driver service centers across Tennessee. Reentry partners and TDOC assist returning citizens with documentation needed for employment and benefits. Online services available at tn.gov/safety for many transactions.",
    description_es="Agencia estatal que proporciona licencias de conducir compatibles con REAL ID, tarjetas de identificación con foto y servicios de restablecimiento en centros de servicios al conductor en Tennessee. Los aliados de reinserción y el TDOC ayudan a ciudadanos que regresan con documentación necesaria para empleo y beneficios.",
    address="1150 Foster Avenue", city="Nashville", phone="615-251-5166",
    email="", website="https://www.tn.gov/safety/driver-services.html",
    eligibility="Tennessee residents seeking credentials or reinstatement; specific document requirements apply for ID issuance after incarceration.",
    eligibility_es="Residentes de Tennessee que buscan credenciales o restablecimiento; aplican requisitos específicos de documentos para emisión de identificación.",
    notes="Call 615-251-5166 or locate nearest Driver Services Center at tn.gov/safety; TDOC Reentry Office assists with vital records for ID.",
    notes_es="Llame al 615-251-5166 o localice el centro más cercano en tn.gov/safety; la Oficina de Reinserción del TDOC ayuda con registros vitales.",
    hours="Driver Services Center hours vary by location",
    tags="statewide|id-documentation|drivers-license|REAL-ID|online",
    services="State ID issuance|Driver's license services|Reinstatement fee payment|Driver Services Center locator",
    county="Davidson", served_counties="", coverage="statewide",
    _source="https://www.tn.gov/safety/driver-services.html", _source_type="government", _confidence="high",
)
add(
    name="American Job Centers — Jobs4TN",
    category="employment", region="Statewide",
    description="Statewide workforce system connecting job seekers—including justice-involved Tennesseans—to training, job placement, and employer services through American Job Centers in every county. Jobs4TN.gov supports resume building, job fairs, and unemployment filing. Veterans receive priority service through Disabled Veterans Outreach Program specialists at comprehensive centers.",
    description_es="Sistema estatal de fuerza laboral que conecta a buscadores de empleo—incluidas personas con antecedentes penales en Tennessee—a capacitación, colocación laboral y servicios de empleadores a través de Centros de Empleo Americanos. Jobs4TN.gov apoya currículums, ferias de empleo y desempleo. Los veteranos reciben servicio prioritario.",
    address="220 French Landing Drive", city="Nashville", phone="844-224-5818",
    email="", website="https://www.jobs4tn.gov",
    eligibility="Tennessee residents seeking employment, training, or unemployment benefits; no criminal-record restrictions stated for core services.",
    eligibility_es="Residentes de Tennessee que buscan empleo, capacitación o beneficios de desempleo; sin restricciones de antecedentes indicadas para servicios básicos.",
    notes="Register at jobs4tn.gov; call Jobs4TN Help Desk 844-224-5818 Mon–Fri 8 a.m.–4:30 p.m. CT; locate AJC at careeronestop.org.",
    notes_es="Regístrese en jobs4tn.gov; llame a la mesa de ayuda 844-224-5818 lun–vie 8 a.m.–4:30 p.m. CT.",
    hours="Help desk Mon–Fri 8:00 a.m.–4:30 p.m. CT; center hours vary",
    tags="statewide|employment|Jobs4TN|AJC|veterans-priority",
    services="Job search assistance|Skills training referrals|Unemployment insurance navigation|Veterans employment services",
    county="Davidson", served_counties="", coverage="statewide",
    _source="https://www.tn.gov/workforce/jobs-and-education.html", _source_type="government", _confidence="high",
)
add(
    name="TDOC — Community Supervision",
    category="probation-parole", region="Statewide",
    description="State agency responsible for probation and parole supervision of individuals released from Tennessee prisons and jails. District field offices across Tennessee connect supervisees to reentry resources, Day Reporting Centers, and compliance reporting. Contact for reporting requirements and district office locations—not a general resource navigation hotline.",
    description_es="Agencia estatal responsable de la supervisión de libertad probatoria y condicional de personas liberadas de prisiones de Tennessee. Las oficinas de distrito conectan a supervisados con recursos de reinserción y Centros de Reporte Diurno. Contacte para requisitos de reporte y ubicaciones de oficinas, no para navegación general de recursos.",
    address="320 Sixth Avenue North", city="Nashville", phone="866-506-7225",
    email="", website="https://www.tn.gov/correction/community-supervision.html",
    eligibility="Individuals under Tennessee probation or parole supervision; family members may contact for general district information.",
    eligibility_es="Personas bajo supervisión de libertad probatoria o condicional de Tennessee; familiares pueden contactar para información del distrito.",
    notes="Compliant Reporting Supervision line 866-506-7225; see tn.gov/correction field office directory for district phones and addresses.",
    notes_es="Línea de supervisión de reporte conforme 866-506-7225; consulte el directorio de oficinas de campo en tn.gov/correction.",
    hours="District offices Monday–Friday business hours",
    tags="statewide|parole|probation|DOC|supervision",
    services="Probation and parole supervision|District office coordination|DRC referrals|Supervision compliance support",
    county="Davidson", served_counties="", coverage="statewide",
    _source="https://www.tn.gov/correction/cs/field-office-directory.html", _source_type="government", _confidence="high",
)
add(
    name="SAMHSA National Helpline",
    category="substance-use-treatment", region="Statewide",
    description="Free confidential 24/7 treatment referral and information service for individuals and families facing mental health or substance use disorders. Provides referrals to local treatment facilities and community organizations in Tennessee and nationwide. Spanish-language support available through trained specialists.",
    description_es="Servicio gratuito y confidencial 24/7 de referencia e información para personas y familias con trastornos de salud mental o uso de sustancias. Proporciona referencias a centros de tratamiento locales en Tennessee y a nivel nacional. Soporte en español disponible.",
    address="", city="", phone="800-662-4357", email="", website="https://www.samhsa.gov/find-help/national-helpline",
    eligibility="Open to anyone in the United States seeking substance use or mental health treatment information and referrals.",
    eligibility_es="Abierto a cualquier persona en Estados Unidos que busque información y referencias de tratamiento.",
    notes="TTY 800-487-4889; also use FindTreatment.gov to search Tennessee providers online.",
    notes_es="TTY 800-487-4889; también use FindTreatment.gov para buscar proveedores en Tennessee.",
    hours="Available 24/7",
    tags="statewide|hotline|substance-use|treatment-referral|national",
    services="Treatment referrals|Substance use information|Mental health resource navigation",
    county="", served_counties="", coverage="statewide",
    _source="https://www.samhsa.gov/find-help/national-helpline", _source_type="government", _confidence="high",
)
add(
    name="FindTreatment.gov — Tennessee Provider Search",
    category="substance-use-treatment", region="Statewide",
    description="Official SAMHSA online locator for substance use and mental health treatment facilities serving Tennessee. Users search by location, treatment type, and payment options to find licensed providers with current openings. Facility admission requirements vary; justice-involved individuals should confirm criminal-record policies with each provider.",
    description_es="Localizador oficial en línea de SAMHSA para centros de tratamiento de sustancias y salud mental que sirven a Tennessee. Los usuarios buscan por ubicación, tipo de tratamiento y opciones de pago. Los requisitos de admisión varían; las personas con antecedentes penales deben confirmar políticas con cada proveedor.",
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
    name="Tennessee Department of Mental Health — Crisis Services",
    category="healthcare", region="Statewide",
    description="State behavioral health agency coordinating crisis services, treatment referrals, and certified community behavioral health clinics across Tennessee. TDMHSAS supports the 988 lifeline and regional mental health authorities serving justice-involved individuals needing outpatient behavioral health care after release.",
    description_es="Agencia estatal de salud conductual que coordina servicios de crisis, referencias de tratamiento y clínicas comunitarias certificadas en Tennessee. TDMHSAS apoya la línea 988 y autoridades regionales de salud mental que sirven a personas con antecedentes penales que necesitan atención ambulatoria después de la liberación.",
    address="500 Deaderick Street, 6th Floor", city="Nashville", phone="615-532-6500",
    email="", website="https://www.tn.gov/behavioral-health.html",
    eligibility="Tennessee residents seeking publicly funded behavioral health services; eligibility varies by program and regional mental health provider.",
    eligibility_es="Residentes de Tennessee que buscan servicios públicos de salud conductual; la elegibilidad varía según programa y proveedor regional.",
    notes="For immediate crisis call 988; for non-emergency treatment navigation contact regional mental health authority or 211.",
    notes_es="Para crisis inmediata llame al 988; para navegación de tratamiento no urgente contacte la autoridad regional de salud mental o 211.",
    hours="State office Mon–Fri business hours; 988 available 24/7",
    tags="statewide|mental-health|crisis|Medicaid|referral-only",
    services="Crisis system coordination|Treatment referrals|Regional MH authority locator|Certified clinic information",
    county="Davidson", served_counties="", coverage="statewide",
    _source="https://www.tn.gov/behavioral-health.html", _source_type="government", _confidence="high",
)
add(
    name="Tennessee REDLINE — Substance Use Referrals",
    category="state-agency", region="Statewide",
    description="State-supported 24/7 helpline operated under TDMHSAS contract providing confidential substance use disorder treatment referrals, problem gambling resources, and text-based navigation for Tennesseans and families. Calltakers connect justice-involved callers to licensed treatment providers statewide. A referral and information line—not a direct treatment provider.",
    description_es="Línea de ayuda estatal 24/7 bajo contrato de TDMHSAS que ofrece referencias confidenciales de tratamiento de trastornos por uso de sustancias, recursos de juego problemático y navegación por texto para habitantes de Tennessee y familias. Los operadores conectan a personas con antecedentes penales con proveedores de tratamiento licenciados. Es una línea de referencia, no un proveedor directo.",
    address="", city="", phone="800-889-9789", email="",
    website="https://www.tn.gov/behavioral-health/substance-abuse-services/prevention/tennessee-redline.html",
    eligibility="Open to all Tennessee residents seeking substance use or problem gambling treatment information and referrals.",
    eligibility_es="Abierto a todos los residentes de Tennessee que buscan información y referencias de tratamiento de sustancias o juego problemático.",
    notes="Call or text 800-889-9789 anytime; complements 988 for mental health crisis and FindTreatment.gov provider search.",
    notes_es="Llame o envíe texto al 800-889-9789 en cualquier momento; complementa al 988 para crisis de salud mental y FindTreatment.gov.",
    hours="Available 24/7",
    tags="statewide|hotline|substance-use|treatment-referral|REDLINE",
    services="Treatment referrals|Problem gambling resources|Text-based navigation|Provider matching",
    county="", served_counties="", coverage="statewide",
    _source="https://www.tn.gov/behavioral-health/substance-abuse-services/prevention/tennessee-redline.html", _source_type="government", _confidence="high",
)
add(
    name="TDOC — Compliant Reporting Supervision Line",
    category="state-agency", region="Statewide",
    description="Statewide automated phone line for individuals under Tennessee Department of Correction community supervision to report compliance, verify reporting requirements, and access supervision-related information. Used by probationers and parolees for scheduled check-ins when directed by supervising officers. Not a resource navigation or crisis hotline.",
    description_es="Línea telefónica automatizada estatal para personas bajo supervisión comunitaria del Departamento de Corrección de Tennessee para reportar cumplimiento, verificar requisitos de reporte y acceder a información de supervisión. La usan personas en libertad probatoria o condicional según indiquen sus oficiales. No es una línea de navegación de recursos ni de crisis.",
    address="", city="", phone="866-506-7225", email="",
    website="https://www.tn.gov/correction/community-supervision.html",
    eligibility="Individuals under TDOC probation or parole supervision with compliant reporting requirements assigned by supervising officer.",
    eligibility_es="Personas bajo supervisión de libertad probatoria o condicional del TDOC con requisitos de reporte de cumplimiento asignados por el oficial supervisor.",
    notes="Listed on tn.gov/correction community supervision page; contact local field office for officer-specific reporting instructions.",
    notes_es="Listada en la página de supervisión comunitaria de tn.gov/correction; contacte la oficina local para instrucciones específicas del oficial.",
    hours="Automated line available 24/7; officer support during business hours",
    tags="statewide|probation|parole|DOC|supervision|hotline",
    services="Compliant reporting|Supervision status verification|Reporting requirement information",
    county="", served_counties="", coverage="statewide",
    _source="https://www.tn.gov/correction/community-supervision.html", _source_type="government", _confidence="high",
)

# --- Day Reporting / Community Resource Centers ---
DRCS = [
    dict(name="Nashville Day Reporting Center / Community Resource Center", region="Nashville / Davidson County",
         phone="615-770-1835", address="900 Madison Square", city="Madison", county="Davidson", served="Davidson",
         director="Travis Davis", email="Travis.Davis@tn.gov",
         notes="Intensive outpatient alternative to incarceration with on-site Community Resource Center for supervisees and recently released individuals."),
    dict(name="Knoxville Day Reporting Center / Community Resource Center", region="Knoxville / Knox County",
         phone="865-403-1630", address="8417 Kingston Pike", city="Knoxville", county="Knox", served="Knox",
         director="", email="",
         notes="East Tennessee DRC/CRC providing substance use treatment, job readiness, and community resource navigation; TDOC transportation grant available."),
    dict(name="Memphis Day Reporting Center", region="Memphis / Shelby County",
         phone="901-537-5333", address="1991 Corporate Avenue", city="Memphis", county="Shelby", served="Shelby",
         director="", email="",
         notes="West Tennessee DRC; Memphis Community Resource Center services provided through MSCOR partnership at 1362 Mississippi Blvd."),
    dict(name="Murfreesboro Day Reporting Center / Community Resource Center", region="Murfreesboro / Rutherford County",
         phone="615-907-4525", address="1938 Southpointe Way", city="Murfreesboro", county="Rutherford", served="Rutherford",
         director="Richard Boyd", email="Richard.Boyd@tn.gov",
         notes="Middle Tennessee DRC/CRC with three-phase intensive outpatient program; Director Richard Boyd."),
    dict(name="Jackson Day Reporting Center / Community Resource Center", region="Jackson / Madison County",
         phone="731-421-6884", address="237 North Highland Avenue", city="Jackson", county="Madison", served="Madison",
         director="", email="",
         notes="West Tennessee DRC/CRC serving Madison County; TDOC transportation grant available as needed."),
    dict(name="Johnson City Day Reporting Center / Community Resource Center", region="Johnson City / Washington County",
         phone="423-434-3033", address="3011 Browns Mill Road, Suite 14", city="Johnson City", county="Washington", served="Washington",
         director="", email="",
         notes="Upper East Tennessee DRC/CRC serving Washington County and Tri-Cities area; transportation grant available."),
    dict(name="Chattanooga Community Resource Center", region="Chattanooga / Hamilton County",
         phone="423-634-0971", address="1250 Market Street, Suite 103", city="Chattanooga", county="Hamilton", served="Hamilton",
         director="", email="",
         notes="Chattanooga CRC connecting supervisees and recently released individuals to employment, treatment, and community partners."),
]

for d in DRCS:
    desc_en = (
        f"TDOC Day Reporting Center and Community Resource Center serving {d['county']} County with intensive outpatient "
        "substance use treatment, cognitive behavioral programming, job readiness, and one-stop reentry resource navigation "
        "for individuals on community supervision or recently released. Court or TDOC referral typically required for DRC enrollment; "
        "CRC walk-in services may be available for eligible supervisees."
    )
    desc_es = (
        f"Centro de Reporte Diurno y Centro de Recursos Comunitarios del TDOC que sirve al condado {d['county']} con tratamiento "
        "ambulatorio intensivo de sustancias, programación cognitivo-conductual, preparación laboral y navegación de recursos de "
        "reinserción para personas bajo supervisión comunitaria o recién liberadas. Generalmente se requiere referencia del tribunal o TDOC."
    )
    add(
        name=d["name"], category="substance-use-treatment", region=d["region"],
        description=desc_en, description_es=desc_es,
        address=d["address"], city=d["city"], phone=d["phone"],
        email=d.get("email", ""), website="https://www.tn.gov/correction/redirect---rehabilitation/day-reporting.html",
        eligibility="TDOC supervisees with substance use needs referred by courts or probation/parole; CRC open to supervisees and some recently released individuals.",
        eligibility_es="Supervisados del TDOC con necesidades de sustancias referidos por tribunales o libertad condicional; CRC abierto a supervisados y algunos recién liberados.",
        notes=d["notes"],
        notes_es=d["notes"],
        hours="Monday–Friday business hours; contact center for program schedule",
        tags=f"drc|crc|{d['county'].lower()}|substance-use|reentry",
        services="Intensive outpatient treatment|Job readiness training|Community resource navigation|Peer recovery support|Case management",
        county=d["county"], served_counties=d["served"], coverage="single",
        _source="https://www.tn.gov/correction/redirect---rehabilitation/day-reporting/day-reporting-community-resource-center-locations.html",
        _source_type="government", _confidence="high",
    )

add(
    name="Memphis & Shelby County Office of Reentry (MSCOR)",
    category="reentry-organizations", region="Memphis / Shelby County",
    description="Joint TDOC and Shelby County one-stop reentry center connecting formerly incarcerated individuals to employment, vocational training, housing, identification, benefits, and family reunification services. MSCOR serves as Memphis Community Resource Center partner and offers FOCUSED earn-while-you-learn training. Walk-in and referral intake available.",
    description_es="Centro de reinserción conjunto del TDOC y el condado Shelby que conecta a personas anteriormente encarceladas con empleo, capacitación vocacional, vivienda, identificación, beneficios y reunificación familiar. MSCOR sirve como aliado del Centro de Recursos Comunitarios de Memphis y ofrece capacitación FOCUSED. Admisión con o sin cita previa.",
    address="1362 Mississippi Boulevard", city="Memphis", phone="901-222-4550",
    email="re-entrymemphis@shelbycountytn.gov", website="https://www.scofficeofreentry.com",
    eligibility="Shelby County residents with criminal records seeking reentry employment, training, and stabilization services.",
    eligibility_es="Residentes del condado Shelby con antecedentes penales que buscan empleo, capacitación y servicios de estabilización en reinserción.",
    notes="Call 901-222-4550 or visit scofficeofreentry.com; FOCUSED program applications online; partners include HopeWorks and Workforce Mid-South.",
    notes_es="Llame al 901-222-4550 o visite scofficeofreentry.com; solicitudes del programa FOCUSED en línea.",
    hours="Monday–Friday business hours; verify event hours for job fairs",
    tags="memphis|shelby|reentry|MSCOR|employment",
    services="Employment navigation|Vocational training|FOCUSED earn-while-you-learn|ID replacement|Housing referrals|Family reunification",
    county="Shelby", served_counties="Shelby", coverage="single",
    _source="https://www.scofficeofreentry.com", _source_type="government", _confidence="high",
)

# --- Reentry coalitions ---
COALITIONS = [
    dict(name="Davidson County Reentry Council", region="Nashville / Davidson County",
         phone="615-880-2366", email="", county="Davidson", served="Davidson", city="Nashville",
         address="700 Second Avenue South", notes="Metro Social Services hosts Davidson County reentry coordination and partner referrals."),
    dict(name="Rutherford County Reentry Coalition", region="Murfreesboro / Rutherford County",
         phone="615-907-4525", email="", county="Rutherford", served="Rutherford", city="Murfreesboro",
         address="1938 Southpointe Way", notes="Coordinates with Murfreesboro DRC/CRC for regional reentry partner network."),
    dict(name="Knox County Reentry Coalition", region="Knoxville / Knox County",
         phone="865-403-1630", email="", county="Knox", served="Knox", city="Knoxville",
         address="8417 Kingston Pike", notes="East Tennessee reentry partners coordinated through Knoxville DRC/CRC and TREC East."),
    dict(name="Hamilton County Reentry Collaborative", region="Chattanooga / Hamilton County",
         phone="423-634-0971", email="", county="Hamilton", served="Hamilton", city="Chattanooga",
         address="1250 Market Street", notes="Chattanooga CRC and local CBOs support southeast Tennessee reentry navigation."),
    dict(name="Shelby County Reentry Network", region="Memphis / Shelby County",
         phone="901-222-4550", email="re-entrymemphis@shelbycountytn.gov", county="Shelby", served="Shelby", city="Memphis",
         address="1362 Mississippi Boulevard", notes="MSCOR anchors Shelby County reentry partner network and employer connections."),
    dict(name="Montgomery County Reentry Partners", region="Clarksville / Montgomery County",
         phone="931-648-5718", email="", county="Montgomery", served="Montgomery", city="Clarksville",
         address="350 Pageant Lane", notes="Fort Campbell corridor reentry partners coordinated through local workforce and corrections network."),
    dict(name="Madison County Reentry Collaborative", region="Jackson / Madison County",
         phone="731-421-6884", email="", county="Madison", served="Madison", city="Jackson",
         address="237 North Highland Avenue", notes="West Tennessee reentry coordination through Jackson DRC/CRC and WTLS legal aid."),
    dict(name="Washington County Reentry Partners", region="Johnson City / Washington County",
         phone="423-434-3033", email="", county="Washington", served="Washington", city="Johnson City",
         address="3011 Browns Mill Road", notes="Tri-Cities reentry partners coordinated through Johnson City DRC/CRC and LAET."),
    dict(name="Tri-Cities Reentry Collaborative", region="Tri-Cities — Northeast Tennessee",
         phone="423-928-8311", email="", county="Washington", served="Washington|Sullivan|Carter|Johnson|Unicoi|Greene|Hawkins",
         address="207 East Main Street", city="Johnson City",
         notes="LAET Johnson City office and regional CBOs support upper East Tennessee reentry legal and service navigation."),
]

for c in COALITIONS:
    sc = c["served"]
    cov = "single" if "|" not in sc else "multi"
    counties_label = sc.replace("|", ", ")
    desc_en = (
        f"Local reentry coalition and partner network serving {counties_label} in Tennessee. "
        "Community corrections staff, nonprofits, and workforce partners coordinate resources and referrals "
        "for justice-involved individuals—primarily a networking and navigation council, not a full-service crisis provider."
    )
    desc_es = (
        f"Coalición local de reinserción y red de aliados que sirve {counties_label} en Tennessee. "
        "Personal de correcciones comunitarias, organizaciones sin fines de lucro y aliados de fuerza laboral coordinan recursos "
        "para personas con antecedentes penales—principalmente un consejo de red, no un proveedor de crisis completo."
    )
    add(
        name=c["name"], category="reentry-organizations", region=c["region"],
        description=desc_en, description_es=desc_es,
        address=c.get("address", ""), city=c.get("city", ""),
        phone=c["phone"], email=c.get("email", ""),
        website="https://www.tn.gov/correction/redirect---rehabilitation/reentry-services.html",
        eligibility="Justice-involved residents of served counties; contact coalition for current partner eligibility.",
        eligibility_es="Residentes con antecedentes penales en los condados servidos; contacte la coalición.",
        notes=c["notes"] + " Does not provide emergency housing or crisis response.",
        notes_es=c["notes"] + " No ofrece vivienda de emergencia ni respuesta de crisis.",
        hours="Contact for meeting dates and hours",
        tags=f"reentry|coalition|referral-only|{c['county'].lower()}",
        services="Resource networking|Community partner referrals|Reentry navigation|Local service coordination",
        county=c["county"], served_counties=sc if cov == "multi" else sc, coverage=cov,
        _source="https://www.tn.gov/correction/redirect---rehabilitation/tennessee-reentry-collaborative--trec-.html",
        _source_type="government", _confidence="high",
    )

# --- Regional legal aid offices ---
LEGAL_AIDS = [
    dict(name="Legal Aid Society — Nashville Office", region="Middle Tennessee — Davidson County",
         phone="615-244-6610", website="https://las.org", address="1321 Murfreesboro Pike, Suite 400", city="Nashville",
         county="Davidson", served="Davidson|Williamson|Sumner|Robertson|Cheatham|Dickson",
         desc="Free civil legal aid for low-income Nashville-area residents including eviction defense, public benefits appeals, and family law affecting reentry stability."),
    dict(name="Legal Aid Society — Murfreesboro Office", region="Middle Tennessee — Rutherford County",
         phone="615-890-0905", website="https://las.org", address="502 South Academy Street", city="Murfreesboro",
         county="Rutherford", served="Rutherford|Bedford|Coffee|Warren|Cannon|DeKalb|Smith|Macon|Trousdale",
         desc="Free civil legal assistance for low-income Middle Tennessee residents including housing, benefits, and consumer legal barriers to reentry."),
    dict(name="Legal Aid Society — Columbia Office", region="Middle Tennessee — Maury County",
         phone="931-381-5533", website="https://las.org", address="1223 Trotwood Avenue, Suite 2", city="Columbia",
         county="Maury", served="Maury|Giles|Hickman|Lawrence|Lewis|Marshall|Perry|Wayne|Lincoln|Moore|Franklin",
         desc="Free civil legal aid serving south-central Middle Tennessee counties with housing, benefits, and family law for eligible clients."),
    dict(name="Legal Aid Society — Cookeville Office", region="Middle Tennessee — Putnam County",
         phone="931-528-7436", website="https://las.org", address="1100 England Drive, Suite 1", city="Cookeville",
         county="Putnam", served="Putnam|Clay|Cumberland|Fentress|Jackson|Overton|Pickett|White|Van Buren|Grundy|Sequatchie|Bledsoe",
         desc="Free civil legal services for low-income Upper Cumberland residents including housing defense and benefits advocacy."),
    dict(name="Legal Aid of East Tennessee — Knoxville Office", region="East Tennessee — Knox County",
         phone="865-637-0484", website="https://www.laet.org", address="607 West Summit Hill Drive SW", city="Knoxville",
         county="Knox", served="Knox|Loudon|Sevier",
         desc="Free civil legal aid for low-income Knoxville-area residents including eviction prevention, benefits, and domestic violence protections."),
    dict(name="Legal Aid of East Tennessee — Chattanooga Office", region="East Tennessee — Hamilton County",
         phone="423-756-4013", website="https://www.laet.org", address="100 West Martin Luther King Boulevard, Suite 402", city="Chattanooga",
         county="Hamilton", served="Hamilton|Marion|Bledsoe|Rhea|Sequatchie",
         desc="Free civil legal services for low-income Chattanooga-area residents including housing, benefits, and family law matters."),
    dict(name="Legal Aid of East Tennessee — Johnson City Office", region="Tri-Cities — Washington County",
         phone="423-928-8311", website="https://www.laet.org", address="207 East Main Street, Suite 3C", city="Johnson City",
         county="Washington", served="Washington|Carter|Hancock|Hawkins|Johnson|Sullivan|Unicoi",
         desc="Free civil legal aid for low-income Tri-Cities residents including housing, benefits, and consumer legal issues affecting reentry."),
    dict(name="Legal Aid of East Tennessee — Morristown Office", region="East Tennessee — Hamblen County",
         phone="423-587-4850", website="https://www.laet.org", address="1001 West 2nd North Street", city="Morristown",
         county="Hamblen", served="Hamblen|Cocke|Grainger|Greene|Jefferson",
         desc="Free civil legal assistance for low-income northeast Tennessee residents including housing and benefits advocacy."),
    dict(name="West Tennessee Legal Services — Jackson Office", region="West Tennessee — Madison County",
         phone="731-423-0616", website="https://www.wtls.org", address="210 West Tennessee Street", city="Jackson",
         county="Madison", served="Madison|Chester|Hardeman|Haywood|Henderson|McNairy|Decatur|Hardin",
         desc="Free civil legal aid for low-income West Tennessee residents including housing, benefits, and family law barriers to reentry."),
    dict(name="West Tennessee Legal Services — Memphis Office", region="West Tennessee — Shelby County",
         phone="800-372-8346", website="https://www.wtls.org", address="1661 Aaron Brenner Drive, Suite 100", city="Memphis",
         county="Shelby", served="Shelby|Fayette|Lauderdale|Tipton",
         desc="Free civil legal services for low-income Memphis-area residents including eviction defense and benefits appeals affecting returning citizens."),
]

for la in LEGAL_AIDS:
    cov = "single" if "|" not in la["served"] else "multi"
    add(
        name=la["name"], category="legal-aid", region=la["region"],
        description=la["desc"] + " Income and household-size limits apply; call centralized intake 800-238-1443 (LAS) or county office before visiting.",
        description_es=la["desc"].replace("Free", "Asistencia legal civil gratuita") + " Aplican límites de ingresos; llame a admisión centralizada u oficina local antes de visitar.",
        address=la["address"], city=la["city"], phone=la["phone"], email="", website=la["website"],
        eligibility="Low-income Tennessee residents in service area; veterans and seniors may qualify with higher income limits.",
        eligibility_es="Residentes de bajos ingresos en el área de servicio; veteranos y personas mayores pueden calificar con límites más altos.",
        notes="Apply online or call Help4TN 844-435-7486 for county routing; appointment required for attorney consultation.",
        notes_es="Solicite en línea o llame a Help4TN 844-435-7486 para enrutamiento por condado; se requiere cita para consulta con abogado.",
        hours="Intake during business hours; call local office for walk-in availability",
        tags="legal-aid|low-income|reentry|housing",
        services="Civil legal representation|Housing legal aid|Benefits advocacy|Family law assistance",
        county=la["county"], served_counties=la["served"], coverage=cov,
        _source=la["website"], _source_type="nonprofit", _confidence="high",
    )

# --- TDOC community supervision districts ---
DISTRICTS = [
    dict(name="TDOC Community Supervision — District 40 (Davidson)", region="Nashville / Davidson County",
         phone="615-253-7400", address="220 Blanton Avenue", city="Nashville", county="Davidson", served="Davidson",
         notes="Primary Nashville probation and parole district office; additional reporting site at 212 Pavilion Boulevard."),
    dict(name="TDOC Community Supervision — District 70 (Shelby)", region="Memphis / Shelby County",
         phone="901-543-7361", address="40 South Main Street, Suite 211", city="Memphis", county="Shelby", served="Shelby",
         notes="Shelby County supervision hub at One Commerce Square; satellite offices on Overton Crossing and Crump Boulevard."),
    dict(name="TDOC Community Supervision — District 20 (Knox)", region="Knoxville / Knox County",
         phone="865-582-2000", address="1426 Elm Street", city="Knoxville", county="Knox",
         served="Knox|Claiborne|Cocke|Grainger|Hancock|Jefferson|Sevier|Union",
         notes="District 20 field office supervises probation and parole for Knox and surrounding East Tennessee counties listed in served_counties."),
    dict(name="TDOC Community Supervision — District 10 (Hamilton)", region="Chattanooga / Hamilton County",
         phone="423-634-0971", address="1250 Market Street, Suite 103", city="Chattanooga", county="Hamilton", served="Hamilton",
         notes="Chattanooga district office co-located with Community Resource Center."),
    dict(name="TDOC Community Supervision — District 50 (Rutherford)", region="Murfreesboro / Rutherford County",
         phone="615-907-4525", address="1938 Southpointe Way", city="Murfreesboro", county="Rutherford", served="Rutherford",
         notes="Co-located with Murfreesboro DRC/CRC for integrated supervision and treatment referrals."),
    dict(name="TDOC Community Supervision — District 60 (Montgomery)", region="Clarksville / Montgomery County",
         phone="931-648-5718", address="350 Pageant Lane, Suite 201", city="Clarksville", county="Montgomery", served="Montgomery",
         notes="Serves Clarksville and Fort Campbell corridor supervisees."),
    dict(name="TDOC Community Supervision — District 80 (Madison)", region="Jackson / Madison County",
         phone="731-421-6884", address="237 North Highland Avenue", city="Jackson", county="Madison", served="Madison",
         notes="Co-located with Jackson DRC/CRC serving West Tennessee supervisees."),
    dict(name="TDOC Community Supervision — District 30 (Washington)", region="Johnson City / Washington County",
         phone="423-434-3033", address="3011 Browns Mill Road, Suite 14", city="Johnson City", county="Washington", served="Washington",
         notes="Tri-Cities supervision office co-located with Johnson City DRC/CRC."),
    dict(name="TDOC Community Supervision — District 45 (Williamson)", region="Franklin / Williamson County",
         phone="615-790-5840", address="2468 Fairbrook Drive", city="Franklin", county="Williamson", served="Williamson",
         notes="Middle Tennessee suburban supervision district south of Nashville."),
    dict(name="TDOC Community Supervision — District 55 (Sumner)", region="Gallatin / Sumner County",
         phone="615-452-0580", address="355 North Belvedere Drive, Suite 308", city="Gallatin", county="Sumner", served="Sumner",
         notes="North of Nashville supervision district serving Sumner County supervisees."),
]

for pd in DISTRICTS:
    sc = pd["served"]
    cov = "single" if "|" not in sc else "multi"
    counties_label = sc.replace("|", ", ")
    desc_en = (
        f"TDOC community supervision district office supervising probation and parole in {counties_label}. "
        "Officers connect supervisees to Day Reporting Centers, American Job Centers, and local reentry partners. "
        "Contact for reporting requirements and supervision compliance—not emergency services."
    )
    desc_es = (
        f"Oficina del distrito de supervisión comunitaria del TDOC que supervisa libertad probatoria y condicional en {counties_label}. "
        "Los oficiales conectan a supervisados con Centros de Reporte Diurno y aliados de reinserción. "
        "Contacte para requisitos de reporte, no para servicios de emergencia."
    )
    add(
        name=pd["name"], category="probation-parole", region=pd["region"],
        description=desc_en, description_es=desc_es,
        address=pd.get("address", ""), city=pd["city"], phone=pd["phone"], email="",
        website="https://www.tn.gov/correction/cs/field-office-directory.html",
        eligibility="Individuals under Tennessee probation or parole supervision in assigned counties.",
        eligibility_es="Personas bajo supervisión de libertad probatoria o condicional en condados asignados.",
        notes=pd["notes"],
        notes_es=pd["notes"],
        hours="Monday–Friday business hours",
        tags=f"parole|probation|{pd['county'].lower()}|supervision|TDOC",
        services="Probation and parole supervision|DRC referrals|Employment specialist referrals|Reentry partner connections",
        county=pd["county"], served_counties=sc, coverage=cov,
        _source="https://www.tn.gov/correction/cs/field-office-directory.html", _source_type="government", _confidence="high",
    )

# --- Food banks and extras ---
EXTRAS = [
    dict(name="Second Harvest Food Bank of Middle Tennessee", category="food-nutrition", region="Nashville",
         phone="615-329-3491", website="https://www.secondharvestmidtn.org", address="331 Great Circle Road", city="Nashville",
         county="Davidson", cov="multi", served="Davidson|Williamson|Rutherford|Sumner|Wilson|Robertson|Cheatham|Dickson",
         desc="Regional food bank connecting low-income Middle Tennessee residents including returning citizens to partner pantries, mobile distributions, and SNAP application assistance."),
    dict(name="Mid-South Food Bank", category="food-nutrition", region="Memphis",
         phone="901-527-1515", website="https://www.midsouthfoodbank.org", address="3865 South Perkins Road", city="Memphis",
         county="Shelby", cov="multi", served="Shelby|Fayette|Tipton|Lauderdale|Haywood|Crockett|Chester|Hardeman",
         desc="Memphis regional food bank distributing to pantries and agencies serving returning citizens and low-income families across the Mid-South."),
    dict(name="Second Harvest Food Bank of East Tennessee", category="food-nutrition", region="Knoxville",
         phone="865-521-0000", website="https://secondharvestetn.org", address="136 Harvest Lane", city="Maryville",
         county="Blount", cov="multi", served="Knox|Blount|Loudon|Sevier|Anderson|Roane|Monroe|McMinn",
         desc="East Tennessee food bank connecting residents to emergency food and partner pantry network including justice-involved individuals."),
    dict(name="Chattanooga Area Food Bank", category="food-nutrition", region="Chattanooga",
         phone="423-622-1800", website="https://chattfoodbank.org", address="2009 Curtain Pole Road", city="Chattanooga",
         county="Hamilton", cov="multi", served="Hamilton|Marion|Sequatchie|Bledsoe|Rhea|Meigs|McMinn|Bradley",
         desc="Southeast Tennessee food bank providing pantry referrals and nutrition support for low-income residents including reentry populations."),
    dict(name="American Job Center — Nashville", category="employment", region="Nashville",
         phone="615-253-8920", website="https://nm-wb.com", address="2845 Elm Hill Pike", city="Nashville",
         county="Davidson", cov="single", served="Davidson",
         desc="Davidson County comprehensive American Job Center providing career coaching, training referrals, and DVOP veterans employment services."),
    dict(name="American Job Center — Memphis", category="employment", region="Memphis",
         phone="901-543-6570", website="https://www.midsouthwb.org", address="939 South Third Street", city="Memphis",
         county="Shelby", cov="single", served="Shelby",
         desc="Shelby County workforce center connecting job seekers to training, employer services, and unemployment navigation in Memphis."),
    dict(name="American Job Center — Knoxville", category="employment", region="Knoxville",
         phone="865-594-5500", website="https://www.etnwb.com", address="1610 University Avenue", city="Knoxville",
         county="Knox", cov="single", served="Knox",
         desc="Knox County American Job Center providing employment services and career navigation for East Tennessee job seekers."),
    dict(name="HopeWorks — Reentry Services", category="reentry-organizations", region="Memphis",
         phone="901-272-3700", website="https://www.whyhopeworks.org", address="3337 Summer Avenue", city="Memphis",
         county="Shelby", cov="single", served="Shelby",
         desc="Memphis nonprofit providing prison reentry case management, Forgiveness House transitional housing, HiSET/GED, and Hope2Hire job skills for justice-involved residents."),
    dict(name="Project Return — Nashville", category="reentry-organizations", region="Nashville",
         phone="615-256-8712", website="https://www.projectreturninc.org", address="109 South 11th Street", city="Nashville",
         county="Davidson", cov="single", served="Davidson",
         desc="Nashville reentry CBO connecting formerly incarcerated individuals to employment, housing stabilization, and peer support in Davidson County."),
    dict(name="TN Department of Health — Vital Records", category="id-documentation", region="Statewide",
         phone="615-741-1763", website="https://www.tn.gov/health/health-program-areas/vital-records.html", address="710 James Robertson Parkway", city="Nashville",
         county="Davidson", cov="statewide", served="",
         desc="State vital records office for ordering birth certificates and death records needed for state ID, TennCare, and employment applications after release."),
    dict(name="Tennessee Department of Education — Adult Education", category="education", region="Statewide",
         phone="800-531-1515", website="https://www.tn.gov/education/districts/health-and-safety/adult-education.html", address="710 James Robertson Parkway", city="Nashville",
         county="Davidson", cov="statewide", served="",
         desc="State resource connecting Tennessee adults including returning citizens to HiSET/GED, adult diploma, and skills training at local adult education sites."),
    dict(name="WeGo Public Transit — Reduced Fare", category="transportation", region="Nashville",
         phone="615-880-3970", website="https://www.wegotransit.com", address="430 Myatt Drive", city="Madison",
         county="Davidson", cov="single", served="Davidson",
         desc="Nashville public transit reduced-fare programs helping low-income Davidson County residents access bus transportation to work and appointments."),
    dict(name="MATA — Memphis Public Transit", category="transportation", region="Memphis",
         phone="901-274-6282", website="https://www.matatransit.com", address="1370 Levee Road", city="Memphis",
         county="Shelby", cov="single", served="Shelby",
         desc="Memphis public transit providing bus service and reduced-fare options for Shelby County riders accessing employment and reentry services."),
    dict(name="Knoxville Area Transit — KAT", category="transportation", region="Knoxville",
         phone="865-637-3000", website="https://www.katbus.com", address="301 Church Avenue", city="Knoxville",
         county="Knox", cov="single", served="Knox",
         desc="Knoxville public transit with reduced-fare programs for eligible low-income Knox County riders including returning citizens."),
]

for e in EXTRAS:
    add(
        name=e["name"], category=e["category"], region=e.get("region", e.get("city", "")),
        description=e["desc"],
        description_es=e["desc"].replace("connecting", "conectando").replace("providing", "proporcionando").replace("Nashville", "Nashville").replace("Memphis", "Memphis").replace("low-income", "de bajos ingresos").replace("returning citizens", "ciudadanos que regresan").replace("justice-involved", "con antecedentes penales"),
        address=e.get("address", ""), city=e["city"], phone=e["phone"], email="", website=e["website"],
        eligibility="Contact program for current eligibility; justice-involved individuals generally welcome at listed services.",
        eligibility_es="Contacte el programa para elegibilidad actual; personas con antecedentes penales generalmente son bienvenidas.",
        notes="Verify current intake hours and referral requirements by phone before visiting.",
        notes_es="Verifique horarios de admisión y requisitos de referencia por teléfono antes de visitar.",
        hours="Contact for current hours",
        tags=f"reentry|{e.get('county', 'statewide').lower() or 'statewide'}",
        services="",
        county=e.get("county", ""),
        served_counties=e.get("served", ""), coverage=e["cov"],
        _source=e["website"], _source_type="nonprofit", _confidence="high",
    )

# --- Phase 4: Program-level expansion ---
from tennessee_phase4_expansion import register_phase4
register_phase4(add)

from phase3b_gapfill import register_phase3b_tennessee
register_phase3b_tennessee(add, ENTRIES)

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
