#!/usr/bin/env python3
"""Generate mississippi-resources.csv and mississippi-research-log.csv.

RESOURCES_UUID_PREFIX comment df000001
"""
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES_PATH = ROOT / "data" / "mississippi-resources.csv"
LOG_PATH = ROOT / "data" / "mississippi-research-log.csv"
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
    name="MDOC — Reentry & Community Corrections",
    category="state-agency", region="Statewide",
    description="The Mississippi Department of Corrections coordinates statewide reentry planning, pre-release programming, and community corrections supervision for individuals preparing to leave MDOC custody or under probation and parole across all 82 counties. Reentry staff connect returning citizens to MDHS benefits through access.ms.gov, Mississippi Works job centers, Division of Medicaid enrollment, and local treatment and housing partners before and after release. This office provides planning and referrals—not a walk-in crisis line or emergency cash provider.",
    description_es="El Departamento de Correcciones de Mississippi coordina la planificación estatal de reinserción, programación previa a la liberación y supervisión de correcciones comunitarias para personas que se preparan para salir de custodia de MDOC o bajo probatoria y libertad condicional en los 82 condados. El personal de reinserción conecta a ciudadanos que regresan con beneficios MDHS a través de access.ms.gov, centros Mississippi Works e inscripción en Medicaid. Esta oficina ofrece planificación y referencias, no es una línea de crisis ni proveedor de efectivo de emergencia.",
    address="633 North State Street", city="Jackson", phone="601-359-5600", email="",
    website="https://www.mdoc.ms.gov",
    eligibility="Individuals in MDOC custody preparing for release or under community supervision; community partners seeking MDOC reentry engagement.",
    eligibility_es="Personas en custodia de MDOC que se preparan para la liberación o bajo supervisión comunitaria; aliados comunitarios que buscan coordinación de reinserción.",
    notes="Visit mdoc.ms.gov for reentry resources; coordinate through facility reentry staff and assigned probation or parole officer after release.",
    notes_es="Visite mdoc.ms.gov para recursos de reinserción; coordine a través del personal de reinserción de la instalación y el oficial de probatoria asignado.",
    hours="State office Monday–Friday business hours",
    tags="statewide|reentry|MDOC|DOC|pre-release|community-corrections",
    services="Pre-release planning|Community corrections coordination|Partner referrals|Reentry resource navigation|Supervision linkage",
    county="Hinds", served_counties="", coverage="statewide",
    _source="https://www.mdoc.ms.gov", _source_type="government", _confidence="high",
)
add(
    name="MDOC — Probation & Parole Field Operations",
    category="probation-parole", region="Statewide",
    description="MDOC Probation and Parole Field Operations supervises adults on probation and parole through regional field offices across Mississippi, connecting supervisees to employment, treatment, and housing referrals as conditions of release. Field officers coordinate with Mississippi Works, MDHS benefits offices, DMH community mental health centers, and local reentry nonprofits in every region. Contact your assigned officer—not a walk-in benefits or emergency housing intake center.",
    description_es="Operaciones de Campo de Probatoria y Libertad Condicional de MDOC supervisa adultos en probatoria y libertad condicional a través de oficinas regionales en Mississippi, conectando supervisados con empleo, tratamiento y vivienda según condiciones de liberación. Los oficiales coordinan con Mississippi Works, oficinas MDHS y centros comunitarios de salud mental DMH. Contacte a su oficial asignado; no es un centro de admisión de beneficios o vivienda de emergencia.",
    address="633 North State Street", city="Jackson", phone="601-359-5601", email="",
    website="https://www.mdoc.ms.gov/ProbationParole",
    eligibility="Adults under MDOC probation or parole supervision in Mississippi; report to assigned field officer.",
    eligibility_es="Adultos bajo supervisión probatoria o de libertad condicional de MDOC en Mississippi; reporte al oficial de campo asignado.",
    notes="Find regional field office contacts at mdoc.ms.gov; statewide information 601-359-5601; ask your officer about local reentry referrals.",
    notes_es="Encuentre contactos de oficinas regionales en mdoc.ms.gov; información estatal 601-359-5601; pregunte a su oficial sobre referencias locales.",
    hours="Field offices typically Monday–Friday business hours",
    tags="statewide|probation-parole|MDOC|parole|community-supervision|reentry",
    services="Probation supervision|Parole supervision|Community reporting|Treatment referrals|Reentry partner coordination",
    county="Hinds", served_counties="", coverage="statewide",
    _source="https://www.mdoc.ms.gov/ProbationParole", _source_type="government", _confidence="high",
)
add(
    name="access.ms.gov — MDHS Benefits Portal",
    category="financial-assistance", region="Statewide",
    description="access.ms.gov is Mississippi's official online portal for applying for and managing SNAP food assistance, Temporary Assistance for Needy Families (TANF) cash benefits, child care subsidies, and Medicaid application referrals through county MDHS Economic Assistance offices. Justice-involved Mississippians can apply for food and cash support after release from MDOC custody or county jails using the same account used by all 82 county MDHS offices statewide.",
    description_es="access.ms.gov es el portal en línea oficial de Mississippi para solicitar y administrar asistencia alimentaria SNAP, beneficios en efectivo TANF, subsidios de cuidado infantil y referencias de solicitud de Medicaid a través de oficinas de Asistencia Económica MDHS del condado. Los mississippianos en reinserción pueden solicitar apoyo alimentario y en efectivo después de la liberación.",
    address="", city="", phone="800-948-3050", email="", website="https://access.ms.gov",
    eligibility="Mississippi residents meeting income and household-size requirements for SNAP, TANF, or child care assistance; criminal record generally not a barrier to SNAP eligibility.",
    eligibility_es="Residentes de Mississippi que cumplan requisitos de ingresos y tamaño del hogar para SNAP, TANF o asistencia de cuidado infantil; los antecedentes penales generalmente no son barrera para SNAP.",
    notes="Apply online at access.ms.gov; call 800-948-3050 for SNAP/TANF customer service; visit your county MDHS office for in-person verification.",
    notes_es="Solicite en access.ms.gov; llame al 800-948-3050; visite su oficina MDHS del condado para verificación presencial.",
    hours="Online 24/7; county MDHS office hours vary",
    tags="statewide|benefits|SNAP|TANF|access-ms-gov|reentry",
    services="SNAP enrollment|TANF application|Child care subsidy applications|Medicaid referral|County MDHS office locator",
    county="", served_counties="", coverage="statewide",
    _source="https://access.ms.gov", _source_type="government", _confidence="high",
)
add(
    name="Mississippi Division of Medicaid",
    category="healthcare", region="Statewide",
    description="The Mississippi Division of Medicaid administers Medicaid and CHIP health coverage for eligible low-income residents statewide, including pregnant women, children, disabled adults, and certain low-income parents through managed care plans. Returning citizens can apply for Medicaid before or immediately after release to secure prescription and primary care coverage; recipient services staff help with enrollment questions and eligibility appeals by phone.",
    description_es="La División de Medicaid de Mississippi administra la cobertura Medicaid y CHIP para residentes elegibles de bajos ingresos en todo el estado, incluidas mujeres embarazadas, niños, adultos discapacitados y ciertos padres de bajos ingresos. Los ciudadanos que regresan pueden solicitar Medicaid antes o inmediatamente después de la liberación para asegurar cobertura de recetas y atención primaria.",
    address="550 High Street, Suite 1604", city="Jackson", phone="800-421-2408", email="",
    website="https://medicaid.ms.gov",
    eligibility="Mississippi residents meeting income and category requirements; Mississippi has not expanded Medicaid to all low-income adults.",
    eligibility_es="Residentes de Mississippi que cumplan requisitos de ingresos y categoría; Mississippi no ha expandido Medicaid a todos los adultos de bajos ingresos.",
    notes="Apply through access.ms.gov or call 800-421-2408; ask about disability-based categories and presumptive eligibility for pregnant applicants.",
    notes_es="Solicite a través de access.ms.gov o llame al 800-421-2408; pregunte sobre categorías por discapacidad y elegibilidad presuntiva para embarazadas.",
    hours="Recipient call center Monday–Friday, 8:00 a.m.–5:00 p.m. CT",
    tags="statewide|healthcare|Medicaid|health-insurance|reentry",
    services="Medicaid application assistance|Eligibility determination|Managed care plan navigation|Recipient services helpline|Appeals support",
    county="Hinds", served_counties="", coverage="statewide",
    _source="https://medicaid.ms.gov", _source_type="government", _confidence="high",
)
add(
    name="211 Mississippi",
    category="state-agency", region="Statewide",
    description="211 Mississippi is a free statewide information and referral service connecting residents to health and human services including housing, food, utilities, employment, and crisis support across all 82 counties. United Way-supported navigators help callers find local programs by need and ZIP code through ms211.org and by dialing 211 from any Mississippi phone. 211 Mississippi is a referral service—not a direct-service provider.",
    description_es="211 Mississippi es un servicio gratuito de información y referencia estatal que conecta a residentes con servicios de salud y humanos incluyendo vivienda, alimentos, servicios públicos, empleo y apoyo en crisis en los 82 condados. Navegadores apoyados por United Way ayudan a encontrar programas locales por necesidad y código postal. Es un servicio de referencia, no un proveedor directo.",
    address="", city="", phone="211", email="", website="https://www.ms211.org",
    eligibility="Open to all Mississippi residents; no criminal-record restrictions stated.",
    eligibility_es="Abierto a todos los residentes de Mississippi; sin restricciones de antecedentes indicadas.",
    notes="Dial 211 from any Mississippi phone; search resources online at ms211.org; text your ZIP code to 898-211 where available.",
    notes_es="Marque 211 desde cualquier teléfono de Mississippi; busque recursos en ms211.org; envíe su código postal al 898-211 donde esté disponible.",
    hours="Available during published service hours; check ms211.org",
    tags="statewide|hotline|211|referral-only|basic-needs",
    services="Information and referral|Housing resource navigation|Benefits referrals|Crisis resource connections|Local program search",
    county="", served_counties="", coverage="statewide",
    _source="https://www.ms211.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Mississippi Center for Legal Services — Statewide Intake",
    category="legal-aid", region="Statewide",
    description="Mississippi Center for Legal Services is the state's primary nonprofit civil legal aid provider serving low-income Mississippians with housing, public benefits, family law, and criminal record relief including expungement under Mississippi law. Centralized statewide intake at 1-800-498-1804 routes callers to regional offices in Jackson, Hattiesburg, Gulfport, Tupelo, and Greenwood—not criminal defense representation.",
    description_es="Mississippi Center for Legal Services es el principal proveedor sin fines de lucro de asistencia legal civil del estado que sirve a personas de bajos ingresos con vivienda, beneficios públicos, derecho familiar y alivio de antecedentes penales incluida la expungación bajo la ley de Mississippi. La admisión centralizada enruta a oficinas regionales, no defensa penal.",
    address="206 East Capitol Street, Suite 700", city="Jackson", phone="800-498-1804", email="",
    website="https://www.mslegalservices.org",
    eligibility="Low-income Mississippi residents with non-criminal legal problems; LSC income limits apply; offense-type restrictions may apply for record relief eligibility.",
    eligibility_es="Residentes de Mississippi de bajos ingresos con problemas legales no penales; aplican límites de ingresos LSC; pueden aplicar restricciones por tipo de delito para alivio de antecedentes.",
    notes="Apply online at mslegalservices.org or call 1-800-498-1804; regional offices serve specific counties listed on the website.",
    notes_es="Solicite en mslegalservices.org o llame al 1-800-498-1804; las oficinas regionales sirven condados específicos listados en el sitio web.",
    hours="Intake Monday–Friday business hours; online application 24/7",
    tags="statewide|legal-aid|low-income|expungement|hotline",
    services="Civil legal representation|Expungement assistance|Housing legal aid|Benefits advocacy|Regional office referrals",
    county="Hinds", served_counties="", coverage="statewide",
    _source="https://www.mslegalservices.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Mississippi Works — WIN Job Center Network",
    category="employment", region="Statewide",
    description="Mississippi Works is the statewide workforce development network operated through the Mississippi Department of Employment Security, connecting job seekers in all 82 counties to WIN Job Centers, career coaching, WIOA training referrals, and fair-chance employment navigation. Justice-involved adults leaving MDOC custody or county jails can register at msworks.ms.gov for free core services at local one-stop centers. Workforce services—not emergency cash or housing placement.",
    description_es="Mississippi Works es la red estatal de desarrollo de la fuerza laboral operada por el Departamento de Seguridad del Empleo de Mississippi, conectando buscadores de empleo en los 82 condados con centros WIN Job Center, coaching de carrera y referencias de capacitación WIOA. Los adultos con antecedentes penales pueden registrarse en msworks.ms.gov para servicios básicos gratuitos.",
    address="1230 Raymond Road", city="Jackson", phone="601-321-6000", email="",
    website="https://msworks.ms.gov",
    eligibility="Open to Mississippi job seekers including justice-involved individuals; core Mississippi Works services are free.",
    eligibility_es="Abierto a buscadores de empleo de Mississippi incluidas personas con antecedentes penales; servicios básicos gratuitos.",
    notes="Register at msworks.ms.gov; find your nearest WIN Job Center by ZIP code; pairs with MDHS benefits and MDRS vocational rehabilitation.",
    notes_es="Regístrese en msworks.ms.gov; encuentre su WIN Job Center más cercano por código postal; se vincula con beneficios MDHS y rehabilitación vocacional MDRS.",
    hours="WIN Job Centers typically Monday–Friday business hours",
    tags="statewide|employment|mississippi-works|WIN|WIOA|fair-chance|reentry",
    services="Career coaching|Resume assistance|WIOA training referrals|Job search tools|Fair-chance employment navigation",
    county="Hinds", served_counties="", coverage="statewide",
    _source="https://msworks.ms.gov", _source_type="government", _confidence="high",
)
add(
    name="MDRS — Vocational Rehabilitation Services",
    category="employment", region="Statewide",
    description="The Mississippi Department of Rehabilitation Services helps Mississippians with disabilities—including justice-involved individuals with qualifying disabilities—prepare for, obtain, and maintain employment through vocational counseling, assistive technology, training, and job placement at district offices statewide. VR counselors coordinate with Mississippi Works, Division of Medicaid behavioral health providers, and MDOC reentry staff on individualized employment plans. VR eligibility requires a documented disability affecting employment—not general reentry case management.",
    description_es="El Departamento de Servicios de Rehabilitación de Mississippi ayuda a mississippianos con discapacidades—incluidas personas con antecedentes penales con discapacidades calificadas—a prepararse, obtener y mantener empleo mediante consejería vocacional, tecnología de asistencia y colocación laboral. La elegibilidad VR requiere una discapacidad documentada que afecte el empleo.",
    address="1270 Eastover Drive", city="Jackson", phone="800-443-1000", email="",
    website="https://www.mdrs.ms.gov",
    eligibility="Mississippi residents with a physical or mental disability that is a substantial barrier to employment; justice-involved applicants welcome if VR eligible.",
    eligibility_es="Residentes de Mississippi con una discapacidad física o mental que sea una barrera sustancial al empleo; solicitantes con antecedentes penales bienvenidos si son elegibles para VR.",
    notes="Apply at mdrs.ms.gov or call 800-443-1000; district office locations listed on the MDRS website.",
    notes_es="Solicite en mdrs.ms.gov o llame al 800-443-1000; las ubicaciones de oficinas de distrito están en el sitio web de MDRS.",
    hours="District offices Monday–Friday business hours",
    tags="statewide|employment|MDRS|vocational-rehabilitation|disability|reentry",
    services="Vocational counseling|Job placement|Assistive technology|Skills training|Disability employment supports",
    county="Hinds", served_counties="", coverage="statewide",
    _source="https://www.mdrs.ms.gov", _source_type="government", _confidence="high",
)
add(
    name="Mississippi Veterans Affairs",
    category="veterans", region="Statewide",
    description="The Mississippi Veterans Affairs Board helps justice-involved veterans access VA benefits, disability claims, education benefits, and housing resources through county veterans service officers across all 82 counties. Veterans released from incarceration may qualify for VA health care, vocational rehabilitation, and veterans treatment court supports. Benefits navigation and claims advocacy—not emergency shelter.",
    description_es="La Junta de Asuntos de Veteranos de Mississippi ayuda a veteranos con antecedentes penales a acceder a beneficios del VA, reclamaciones de discapacidad, beneficios educativos y recursos de vivienda a través de oficiales de servicios para veteranos del condado en los 82 condados. Los veteranos liberados pueden calificar para atención médica del VA y tribunales de tratamiento para veteranos.",
    address="3463 Northside Drive", city="Jackson", phone="601-576-4850", email="",
    website="https://www.msva.ms.gov",
    eligibility="Honorably discharged or qualifying Mississippi veterans and their dependents; service documentation required.",
    eligibility_es="Veteranos de Mississippi con baja honorable o calificados y sus dependientes; se requiere documentación de servicio.",
    notes="Find your county veterans service officer at msva.ms.gov; free benefits claims assistance available at county offices statewide.",
    notes_es="Encuentre su oficial de servicios para veteranos del condado en msva.ms.gov; asistencia gratuita con reclamaciones disponible en oficinas del condado.",
    hours="County offices Monday–Friday business hours",
    tags="statewide|veterans|VA-benefits|reentry|justice-involved-veterans",
    services="VA benefits claims assistance|Disability claims navigation|Education benefits guidance|Veterans treatment court support|County VSO referrals",
    county="Hinds", served_counties="", coverage="statewide",
    _source="https://www.msva.ms.gov", _source_type="government", _confidence="high",
)
add(
    name="Mississippi DPS — Driver License Division",
    category="id-documentation", region="Statewide",
    description="The Mississippi Department of Public Safety Driver License Division issues state ID cards and driver's licenses required for employment, housing, and benefits enrollment after release. Returning citizens can apply for a Mississippi ID at driver license offices statewide with proof of identity and residency. Not a vital records office—contact MSDH Vital Records for birth certificates.",
    description_es="La División de Licencias de Conducir del Departamento de Seguridad Pública de Mississippi emite tarjetas de identificación estatal y licencias de conducir necesarias para empleo, vivienda e inscripción en beneficios después de la liberación. Los ciudadanos que regresan pueden solicitar una identificación de Mississippi en oficinas de licencias con prueba de identidad y residencia. No es oficina de registros vitales.",
    address="1900 East Woodrow Wilson Avenue", city="Jackson", phone="601-987-1272", email="",
    website="https://www.dps.ms.gov/driver-services",
    eligibility="Mississippi residents with required identity and residency documentation; fees apply for ID cards and licenses.",
    eligibility_es="Residentes de Mississippi con documentación requerida de identidad y residencia; aplican tarifas para tarjetas de identificación.",
    notes="Find driver license offices at dps.ms.gov; bring certified birth certificate or passport plus proof of Mississippi residency.",
    notes_es="Encuentre oficinas en dps.ms.gov; traiga certificado de nacimiento o pasaporte más prueba de residencia en Mississippi.",
    hours="Driver license office hours vary; check dps.ms.gov",
    tags="statewide|id-documentation|DPS|drivers-license|state-id|reentry",
    services="State ID card issuance|Driver's license services|ID renewal|Driver license office locator",
    county="Hinds", served_counties="", coverage="statewide",
    _source="https://www.dps.ms.gov/driver-services", _source_type="government", _confidence="high",
)
add(
    name="MSDH — Vital Records",
    category="id-documentation", region="Statewide",
    description="The Mississippi State Department of Health Vital Records office issues certified birth certificates, death certificates, and marriage records needed for state ID applications, benefits enrollment, and employment verification after release. Returning citizens can order records online, by mail, or in person at the Jackson office with valid identification. Vital records issuance—not a driver license or probation office.",
    description_es="La oficina de Registros Vitales del Departamento de Salud del Estado de Mississippi emite certificados de nacimiento, defunción y matrimonio necesarios para solicitudes de identificación estatal, inscripción en beneficios y verificación de empleo después de la liberación. Los ciudadanos que regresan pueden solicitar registros en línea, por correo o en persona.",
    address="222 Marketridge Drive", city="Ridgeland", phone="601-576-7981", email="",
    website="https://msdh.ms.gov/vitalrecords",
    eligibility="Individuals with valid ID requesting their own vital records or authorized family members; fees apply per certificate.",
    eligibility_es="Personas con identificación válida que soliciten sus propios registros vitales o familiares autorizados; aplican tarifas por certificado.",
    notes="Order online at msdh.ms.gov/vitalrecords; walk-in service at Ridgeland office; bring government-issued photo ID.",
    notes_es="Solicite en línea en msdh.ms.gov/vitalrecords; servicio presencial en la oficina de Ridgeland; traiga identificación con foto emitida por el gobierno.",
    hours="Monday–Friday business hours",
    tags="statewide|id-documentation|vital-records|birth-certificate|reentry",
    services="Birth certificate issuance|Death certificate issuance|Marriage record copies|Online ordering|In-person vital records service",
    county="Madison", served_counties="", coverage="statewide",
    _source="https://msdh.ms.gov/vitalrecords", _source_type="government", _confidence="high",
)
add(
    name="988 Suicide & Crisis Lifeline — Mississippi",
    category="healthcare", region="Statewide",
    description="Free confidential 24/7 crisis support for people experiencing mental health emergencies, suicidal thoughts, or substance use crises in Mississippi. Trained specialists provide immediate support and can connect callers to local mobile crisis teams through DMH Community Mental Health Center partners statewide. Available to anyone—not reentry-specific but essential for justice-involved individuals in crisis.",
    description_es="Apoyo gratuito y confidencial 24/7 para emergencias de salud mental, pensamientos suicidas o crisis por uso de sustancias en Mississippi. Especialistas capacitados ofrecen apoyo inmediato y conexión a equipos de crisis móviles a través de aliados de Centros Comunitarios de Salud Mental DMH. Disponible para cualquier persona, esencial para personas con antecedentes penales en crisis.",
    address="", city="", phone="988", email="", website="https://988lifeline.org",
    eligibility="Open to anyone in Mississippi experiencing a mental health or suicide crisis; no eligibility restrictions.",
    eligibility_es="Abierto a cualquier persona en Mississippi en crisis de salud mental o suicidio; sin restricciones.",
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
    description="Free confidential 24/7 treatment referral and information service for individuals and families facing mental health or substance use disorders. Provides referrals to local treatment facilities and community organizations in Mississippi and nationwide. Spanish-language support available through trained specialists for justice-involved individuals seeking SUD or mental health treatment after release.",
    description_es="Servicio gratuito y confidencial 24/7 de referencia e información para personas y familias con trastornos de salud mental o uso de sustancias. Proporciona referencias a centros de tratamiento locales en Mississippi y a nivel nacional. Soporte en español disponible para personas con antecedentes penales que buscan tratamiento después de la liberación.",
    address="", city="", phone="800-662-4357", email="",
    website="https://www.samhsa.gov/find-help/national-helpline",
    eligibility="Open to anyone in the United States seeking substance use or mental health treatment information and referrals.",
    eligibility_es="Abierto a cualquier persona en Estados Unidos que busque información y referencias de tratamiento.",
    notes="TTY 800-487-4889; also use FindTreatment.gov to search Mississippi providers online.",
    notes_es="TTY 800-487-4889; también use FindTreatment.gov para buscar proveedores en Mississippi.",
    hours="Available 24/7",
    tags="statewide|hotline|substance-use|treatment-referral|national",
    services="Treatment referrals|Substance use information|Mental health resource navigation",
    county="", served_counties="", coverage="statewide",
    _source="https://www.samhsa.gov/find-help/national-helpline", _source_type="government", _confidence="high",
)
add(
    name="FindTreatment.gov — Mississippi Provider Search",
    category="substance-use-treatment", region="Statewide",
    description="SAMHSA's online treatment locator helping Mississippi residents find substance use and mental health treatment providers by location, service type, and payment options including Medicaid. Justice-involved individuals can search outpatient, residential, and MAT providers before or after release from MDOC custody or county jails across all 82 counties.",
    description_es="Localizador en línea de SAMHSA que ayuda a residentes de Mississippi a encontrar proveedores de tratamiento de uso de sustancias y salud mental por ubicación, tipo de servicio y opciones de pago incluido Medicaid. Personas con antecedentes penales pueden buscar proveedores ambulatorios, residenciales y TMO antes o después de la liberación.",
    address="", city="", phone="", email="", website="https://findtreatment.gov",
    eligibility="Open to anyone searching for treatment; provider admission rules vary.",
    eligibility_es="Abierto a cualquier persona que busque tratamiento; las reglas de admisión varían según el proveedor.",
    notes="Search findtreatment.gov by Mississippi county or city; filter for MAT, outpatient, or residential services.",
    notes_es="Busque en findtreatment.gov por condado o ciudad de Mississippi; filtre por TMO, ambulatorio o residencial.",
    hours="Website 24/7",
    tags="statewide|substance-use|online|MAT|treatment-locator",
    services="Treatment provider search|MAT locator|Outpatient program finder|Residential program finder",
    county="", served_counties="", coverage="statewide",
    _source="https://findtreatment.gov", _source_type="government", _confidence="high",
)
add(
    name="Mississippi Department of Mental Health (DMH)",
    category="healthcare", region="Statewide",
    description="The Mississippi Department of Mental Health oversees the statewide network of Community Mental Health Centers and substance use treatment providers serving Mississippians with mental illness, substance use disorders, and developmental disabilities. DMH funds crisis services, peer support programs, and treatment coordination for justice-involved individuals through regional centers—not a direct crisis hotline itself.",
    description_es="El Departamento de Salud Mental de Mississippi supervisa la red estatal de Centros Comunitarios de Salud Mental y proveedores de tratamiento de uso de sustancias que sirven a mississippianos con enfermedades mentales, trastornos por uso de sustancias y discapacidades del desarrollo. DMH financia servicios de crisis y coordinación de tratamiento para personas con antecedentes penales.",
    address="1101 North West Street", city="Jackson", phone="601-359-1288", email="",
    website="https://dmh.ms.gov",
    eligibility="Mississippi residents seeking mental health, substance use, or developmental disability services; individual center eligibility and fees vary by income.",
    eligibility_es="Residentes de Mississippi que buscan servicios de salud mental, uso de sustancias o discapacidad del desarrollo; la elegibilidad y tarifas varían por centro e ingresos.",
    notes="Find your local Community Mental Health Center at dmh.ms.gov; call 988 for immediate crisis support statewide.",
    notes_es="Encuentre su Centro Comunitario de Salud Mental local en dmh.ms.gov; llame al 988 para apoyo inmediato en crisis en todo el estado.",
    hours="State office Monday–Friday business hours; local centers vary",
    tags="statewide|healthcare|DMH|mental-health|substance-use|reentry",
    services="Community mental health center referrals|Substance use treatment coordination|Crisis services funding|Peer support program oversight|Developmental disability services",
    county="Hinds", served_counties="", coverage="statewide",
    _source="https://dmh.ms.gov", _source_type="government", _confidence="high",
)
add(
    name="Mississippi Reentry Council",
    category="reentry-organizations", region="Statewide",
    description="The Mississippi Reentry Council coordinates state agencies, faith communities, and community-based providers around a shared statewide reentry strategy, connecting justice-involved Mississippians and local reentry coalitions to housing, employment, and treatment partners. The council convenes policy and coalition-building work through MDOC and community partners—not direct emergency services or a walk-in office for individuals seeking immediate help.",
    description_es="El Consejo de Reinserción de Mississippi coordina agencias estatales, comunidades de fe y proveedores comunitarios en torno a una estrategia estatal compartida de reinserción, conectando a mississippianos con antecedentes penales y coaliciones locales de reinserción con aliados de vivienda, empleo y tratamiento. El consejo convoca trabajo de política y coalición, no servicios de emergencia directos.",
    address="633 North State Street", city="Jackson", phone="601-359-5600", email="",
    website="https://www.mdoc.ms.gov",
    eligibility="Justice-involved Mississippi residents, agencies, and community partners seeking reentry coalition connections and statewide policy information.",
    eligibility_es="Residentes de Mississippi con antecedentes penales, agencias y aliados comunitarios que buscan conexiones con coaliciones de reinserción e información de políticas estatales.",
    notes="Contact MDOC Community Corrections for reentry partner directories; coordinate through local WIN Job Centers and county MDHS offices for direct services.",
    notes_es="Contacte Correcciones Comunitarias de MDOC para directorios de aliados de reinserción; coordine a través de WIN Job Centers locales y oficinas MDHS del condado.",
    hours="Contact for current meeting schedule",
    tags="statewide|reentry|coalition|policy|referral-only",
    services="Coalition coordination|Reentry policy advocacy|Local reentry partner directory|Interagency collaboration",
    county="Hinds", served_counties="", coverage="statewide",
    _source="https://www.mdoc.ms.gov", _source_type="government", _confidence="high",
)

# --- Phase 2: Major metro anchors ---
add(
    name="Stewpot Community Services — Jackson",
    category="basic-needs", region="Jackson / Hinds County",
    description="Stewpot Community Services operates a daytime community center, soup kitchen, and emergency assistance programs for people experiencing homelessness and poverty in Jackson and Hinds County, including returning citizens recently released from Hinds County Detention Center or MDOC custody without a fixed address. Staff help guests connect to shelter beds, access.ms.gov benefits, and Mississippi Works employment services.",
    description_es="Stewpot Community Services opera un centro comunitario diurno, comedor comunitario y programas de asistencia de emergencia para personas que enfrentan falta de vivienda y pobreza en Jackson y el condado Hinds, incluidos ciudadanos recién liberados de la cárcel del condado Hinds o custodia MDOC sin dirección fija. El personal ayuda a conectarse con refugio, beneficios access.ms.gov y servicios de empleo Mississippi Works.",
    address="1100 West Capitol Street", city="Jackson", phone="601-353-2759", email="",
    website="https://www.stewpot.org",
    eligibility="Adults experiencing homelessness or food insecurity in the Jackson area; walk-in day services available.",
    eligibility_es="Adultos sin hogar o con inseguridad alimentaria en el área de Jackson; servicios diurnos sin cita disponibles.",
    notes="Walk in during posted hours for meals and referrals; call 601-353-2759 to confirm current hours and services.",
    notes_es="Ingrese durante el horario publicado para comidas y referencias; llame al 601-353-2759 para confirmar el horario actual.",
    hours="Weekday daytime hours; call to confirm",
    tags="jackson|hinds|basic-needs|day-center|homelessness|reentry",
    services="Soup kitchen|Day center services|Emergency assistance referrals|Mail service|Benefits navigation",
    county="Hinds", served_counties="Hinds|Madison|Rankin", coverage="multi",
    _source="https://www.stewpot.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Gateway Rescue Mission — Jackson",
    category="housing", region="Jackson / Hinds County",
    description="Gateway Rescue Mission provides emergency shelter, meals, addiction recovery, and workforce programs for homeless men and women in the Jackson metro including justice-involved adults through faith-based life transformation programming. Graduates connect to Mississippi Works, Hinds Behavioral Health Services, and Catholic Charities housing partners. Faith-based shelter—not county probation.",
    description_es="Gateway Rescue Mission ofrece refugio de emergencia, comidas, recuperación de adicciones y programas laborales para hombres y mujeres sin hogar en el metro de Jackson incluidos adultos con antecedentes penales a través de programación de transformación de vida basada en la fe.",
    address="2717 Livingston Road", city="Jackson", phone="601-353-2751", email="",
    website="https://www.gatewaymission.org",
    eligibility="Homeless adults in the Jackson metro; justice-involved participants in recovery and shelter programs.",
    eligibility_es="Adultos sin hogar en el metro de Jackson; participantes con antecedentes penales en programas de refugio.",
    notes="Call 601-353-2751 for intake; recovery and shelter campus on Livingston Road.",
    notes_es="Llame al 601-353-2751 para admisión; campus de refugio y recuperación en Livingston Road.",
    hours="Shelter 24/7; intake during business hours",
    tags="jackson|hinds|housing|shelter|recovery|reentry",
    services="Emergency shelter|Addiction recovery|Workforce programs|Life skills|Faith-based support",
    county="Hinds", served_counties="Hinds", coverage="single",
    _source="https://www.gatewaymission.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Hinds Behavioral Health Services",
    category="healthcare", region="Jackson / Hinds County",
    description="Hinds Behavioral Health Services is the designated Community Mental Health Center for Hinds County, providing outpatient psychiatric care, substance use treatment, crisis intervention, and case management for justice-involved adults released from Hinds County Detention Center or MDOC custody. Sliding-fee services and Medicaid billing help ensure continuity of care after release.",
    description_es="Hinds Behavioral Health Services es el Centro Comunitario de Salud Mental designado para el condado Hinds, que ofrece atención psiquiátrica ambulatoria, tratamiento de uso de sustancias, intervención en crisis y manejo de casos para adultos con antecedentes penales liberados de la cárcel del condado Hinds o custodia MDOC.",
    address="3450 Highway 80 West", city="Jackson", phone="601-373-2147", email="",
    website="https://www.hindsbh.org",
    eligibility="Hinds County residents seeking mental health or substance use services; sliding-fee scale based on income; Medicaid accepted.",
    eligibility_es="Residentes del condado Hinds que buscan servicios de salud mental o uso de sustancias; escala de tarifas móviles según ingresos; se acepta Medicaid.",
    notes="Call 601-373-2147 for intake; ask about same-day crisis intervention for individuals recently released from custody.",
    notes_es="Llame al 601-373-2147 para admisión; pregunte sobre intervención en crisis el mismo día para personas recién liberadas.",
    hours="Monday–Friday, 8:00 a.m.–5:00 p.m.; crisis services vary",
    tags="jackson|hinds|healthcare|CMHC|mental-health|substance-use|reentry",
    services="Outpatient psychiatric care|Substance use treatment|Crisis intervention|Case management|Sliding-fee scale enrollment",
    county="Hinds", served_counties="Hinds", coverage="single",
    _source="https://www.hindsbh.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Catholic Charities — Jackson Housing & Reentry",
    category="housing", region="Jackson / Hinds County",
    description="Catholic Charities Jackson provides emergency rental assistance, rapid rehousing, and case management for low-income Hinds County households including returning citizens establishing stable tenancy after incarceration. Housing specialists coordinate with access.ms.gov benefits, Mississippi Works, and Hinds Behavioral Health for whole-person reentry support.",
    description_es="Catholic Charities Jackson ofrece asistencia de alquiler de emergencia, realojamiento rápido y manejo de casos para hogares de bajos ingresos del condado Hinds incluidos ciudadanos que regresan que establecen arrendamiento estable después de la encarcelación.",
    address="850 East River Place", city="Jackson", phone="601-355-8634", email="",
    website="https://www.catholiccharitiesjackson.org",
    eligibility="Low-income Hinds County residents facing housing instability; justice-involved adults may qualify for emergency rental and rehousing programs.",
    eligibility_es="Residentes de bajos ingresos del condado Hinds que enfrentan inestabilidad de vivienda; adultos con antecedentes penales pueden calificar para programas de alquiler de emergencia.",
    notes="Call 601-355-8634 for housing intake; not a walk-in emergency men's shelter.",
    notes_es="Llame al 601-355-8634 para admisión de vivienda; no es refugio de emergencia para hombres sin cita.",
    hours="Monday–Friday business hours",
    tags="jackson|hinds|housing|rapid-rehousing|reentry",
    services="Emergency rental assistance|Rapid rehousing|Case management|Benefits navigation|Employment referrals",
    county="Hinds", served_counties="Hinds", coverage="single",
    _source="https://www.catholiccharitiesjackson.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Open Doors Homeless Coalition — Gulf Coast",
    category="basic-needs", region="Gulfport / Harrison County",
    description="Open Doors Homeless Coalition leads the Gulf Coast Continuum of Care, operating coordinated entry, the regional Homeless Management Information System, and rapid rehousing programs for people experiencing homelessness across Harrison, Hancock, and Jackson counties. Returning citizens without stable housing can access a single point of entry connecting them to emergency shelter and permanent housing partners.",
    description_es="Open Doors Homeless Coalition lidera el Continuo de Cuidado de la Costa del Golfo, operando entrada coordinada y programas de realojamiento rápido para personas sin hogar en los condados Harrison, Hancock y Jackson. Los ciudadanos que regresan sin vivienda estable pueden acceder a un punto único de entrada.",
    address="11975 Seaway Road, Suite B220", city="Gulfport", phone="228-896-3355", email="",
    website="https://www.opendoorshomeless.org",
    eligibility="Individuals and families experiencing or at risk of homelessness on the Gulf Coast; coordinated entry assessment determines referral priority.",
    eligibility_es="Personas y familias que enfrentan o están en riesgo de falta de vivienda en la Costa del Golfo; la evaluación de entrada coordinada determina la prioridad.",
    notes="Call 228-896-3355 or visit opendoorshomeless.org to find a coordinated entry access point.",
    notes_es="Llame al 228-896-3355 o visite opendoorshomeless.org para encontrar un punto de acceso de entrada coordinada.",
    hours="Coordinated entry access points vary; check website",
    tags="gulfport|harrison|basic-needs|coordinated-entry|homelessness|reentry",
    services="Coordinated entry assessment|Rapid rehousing referrals|Homeless Management Information System|Regional provider network coordination",
    county="Harrison", served_counties="Harrison|Hancock|Jackson", coverage="multi",
    _source="https://www.opendoorshomeless.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Coastal Family Health Center — Gulfport",
    category="healthcare", region="Gulfport / Harrison County",
    description="Coastal Family Health Center operates Federally Qualified Health Center clinics across the Mississippi Gulf Coast providing primary care, behavioral health, dental services, and sliding-fee care for uninsured and Medicaid patients including justice-involved adults reestablishing healthcare after release from Harrison County Jail or MDOC custody.",
    description_es="Coastal Family Health Center opera clínicas FQHC en la Costa del Golfo de Mississippi que ofrecen atención primaria, salud conductual, servicios dentales y atención con tarifa móvil para pacientes sin seguro y Medicaid incluidos adultos con antecedentes penales.",
    address="4500 14th Street", city="Gulfport", phone="228-392-1633", email="",
    website="https://www.coastalfamilyhealth.org",
    eligibility="Gulf Coast residents of all ages; sliding scale with proof of income; Medicaid and Medicare accepted.",
    eligibility_es="Residentes de la Costa del Golfo de todas las edades; escala móvil con prueba de ingresos; se aceptan Medicaid y Medicare.",
    notes="Call 228-392-1633 for nearest clinic; multiple Gulf Coast locations; same-day sick visits at select sites.",
    notes_es="Llame al 228-392-1633 para la clínica más cercana; múltiples ubicaciones en la Costa del Golfo.",
    hours="Monday–Friday clinic hours; varies by location",
    tags="gulfport|harrison|healthcare|FQHC|primary-care|reentry",
    services="Primary care|Behavioral health|Dental care|Sliding-fee services|Pharmacy assistance",
    county="Harrison", served_counties="Harrison|Hancock|Jackson|Stone|George", coverage="multi",
    _source="https://www.coastalfamilyhealth.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Back Bay Mission — Biloxi",
    category="housing", region="Biloxi / Harrison County",
    description="Back Bay Mission provides emergency shelter, food pantry services, and case management for homeless and low-income residents on the Mississippi Gulf Coast including justice-involved adults returning from incarceration. Case managers connect clients to Open Doors coordinated entry, Coastal Family Health Center, and Mississippi Works Gulf Coast job centers.",
    description_es="Back Bay Mission ofrece refugio de emergencia, despensa de alimentos y manejo de casos para residentes sin hogar y de bajos ingresos en la Costa del Golfo de Mississippi incluidos adultos con antecedentes penales que regresan de la encarcelación.",
    address="319 Division Street", city="Biloxi", phone="228-432-0301", email="",
    website="https://www.backbaymission.org",
    eligibility="Homeless and low-income adults on the Gulf Coast; justice-involved clients welcome per program policy.",
    eligibility_es="Adultos sin hogar y de bajos ingresos en la Costa del Golfo; clientes con antecedentes penales bienvenidos según política.",
    notes="Call 228-432-0301 for shelter and food pantry intake; pairs with Open Doors and Coastal Family Health Center.",
    notes_es="Llame al 228-432-0301 para admisión de refugio y despensa; se vincula con Open Doors y Coastal Family Health Center.",
    hours="Shelter and pantry hours vary; call ahead",
    tags="biloxi|harrison|housing|shelter|food|reentry",
    services="Emergency shelter|Food pantry|Case management|Benefits navigation|Employment referrals",
    county="Harrison", served_counties="Harrison|Jackson", coverage="multi",
    _source="https://www.backbaymission.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Region II Mental Health Services — Tupelo",
    category="healthcare", region="Tupelo / Lee County",
    description="Region II Mental Health Services is the designated Community Mental Health Center for Lee, Pontotoc, and surrounding northeast Mississippi counties, providing outpatient psychiatric care, substance use treatment, and crisis intervention for justice-involved adults under MDOC supervision. Medicaid and sliding-fee services help returning citizens stabilize behavioral health after release.",
    description_es="Region II Mental Health Services es el Centro Comunitario de Salud Mental designado para Lee, Pontotoc y condados del noreste de Mississippi, que ofrece atención psiquiátrica ambulatoria, tratamiento de uso de sustancias e intervención en crisis para adultos con antecedentes penales bajo supervisión MDOC.",
    address="507 East Main Street", city="Tupelo", phone="662-841-8959", email="",
    website="https://www.regionii.org",
    eligibility="Lee County and Region II service area residents seeking mental health or substance use services; Medicaid and sliding-fee accepted.",
    eligibility_es="Residentes del condado Lee y área de servicio Region II que buscan servicios de salud mental o uso de sustancias; se aceptan Medicaid y tarifa móvil.",
    notes="Call 662-841-8959 for intake; crisis line available; pairs with MDOC Tupelo field office and WIN Job Center Tupelo.",
    notes_es="Llame al 662-841-8959 para admisión; línea de crisis disponible; se vincula con oficina MDOC Tupelo y WIN Job Center.",
    hours="Monday–Friday clinic hours; crisis services vary",
    tags="tupelo|lee|healthcare|CMHC|mental-health|substance-use|reentry",
    services="Outpatient psychiatric care|Substance use treatment|Crisis intervention|Case management|Probation referrals",
    county="Lee", served_counties="Lee|Pontotoc|Itawamba|Prentiss|Alcorn|Tishomingo", coverage="multi",
    _source="https://www.regionii.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Pine Belt Mental Healthcare Resources — Hattiesburg",
    category="healthcare", region="Hattiesburg / Forrest County",
    description="Pine Belt Mental Healthcare Resources serves Forrest, Lamar, and surrounding south Mississippi counties with outpatient mental health, substance use treatment, and crisis services for justice-involved adults referred by MDOC probation and drug courts. The Hattiesburg campus coordinates with Mississippi Works and Forrest County MDHS for reentry stabilization.",
    description_es="Pine Belt Mental Healthcare Resources sirve a Forrest, Lamar y condados del sur de Mississippi con salud mental ambulatoria, tratamiento de uso de sustancias y servicios de crisis para adultos con antecedentes penales referidos por probatoria MDOC y tribunales de drogas.",
    address="103 South 19th Avenue", city="Hattiesburg", phone="601-544-4641", email="",
    website="https://www.pbmhr.org",
    eligibility="Forrest County and Pine Belt service area residents; Medicaid and sliding-fee accepted; justice-involved clients welcome.",
    eligibility_es="Residentes del condado Forrest y área de servicio Pine Belt; se aceptan Medicaid y tarifa móvil; clientes con antecedentes penales bienvenidos.",
    notes="Call 601-544-4641 for intake; multiple Pine Belt locations; pairs with MDOC Hattiesburg field office.",
    notes_es="Llame al 601-544-4641 para admisión; múltiples ubicaciones Pine Belt; se vincula con oficina MDOC Hattiesburg.",
    hours="Monday–Friday clinic hours",
    tags="hattiesburg|forrest|healthcare|CMHC|mental-health|reentry",
    services="Outpatient mental health|Substance use treatment|Crisis services|Case management|Drug court referrals",
    county="Forrest", served_counties="Forrest|Lamar|Marion|Covington|Jefferson Davis|Perry", coverage="multi",
    _source="https://www.pbmhr.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Weems Community Mental Health Center — Meridian",
    category="healthcare", region="Meridian / Lauderdale County",
    description="Weems Community Mental Health Center provides outpatient psychiatric care, substance use treatment, and crisis intervention for Lauderdale, Clarke, and east-central Mississippi counties including justice-involved adults released from MDOC custody or Lauderdale County Jail. Sliding-fee and Medicaid services support behavioral health continuity after release.",
    description_es="Weems Community Mental Health Center ofrece atención psiquiátrica ambulatoria, tratamiento de uso de sustancias e intervención en crisis para los condados Lauderdale, Clarke y el centro-este de Mississippi incluidos adultos con antecedentes penales liberados de custodia MDOC o cárcel del condado Lauderdale.",
    address="1415 College Drive", city="Meridian", phone="601-483-4821", email="",
    website="https://www.weemsmh.com",
    eligibility="Lauderdale County and Weems service area residents; Medicaid and sliding-fee accepted.",
    eligibility_es="Residentes del condado Lauderdale y área de servicio Weems; se aceptan Medicaid y tarifa móvil.",
    notes="Call 601-483-4821 for intake; crisis services available; pairs with MDOC Meridian field office.",
    notes_es="Llame al 601-483-4821 para admisión; servicios de crisis disponibles; se vincula con oficina MDOC Meridian.",
    hours="Monday–Friday clinic hours",
    tags="meridian|lauderdale|healthcare|CMHC|mental-health|reentry",
    services="Outpatient psychiatric care|Substance use treatment|Crisis intervention|Case management|Probation referrals",
    county="Lauderdale", served_counties="Lauderdale|Clarke|Kemper|Neshoba|Newton", coverage="multi",
    _source="https://www.weemsmh.com", _source_type="nonprofit", _confidence="high",
)
add(
    name="Community Counseling Services — Columbus",
    category="healthcare", region="Columbus / Lowndes County",
    description="Community Counseling Services is the designated Community Mental Health Center for Lowndes, Oktibbeha, and surrounding Golden Triangle counties, providing outpatient mental health and substance use treatment for justice-involved adults under MDOC supervision. The Columbus office coordinates with Mississippi Works and local reentry partners for employment and benefits navigation.",
    description_es="Community Counseling Services es el Centro Comunitario de Salud Mental designado para Lowndes, Oktibbeha y condados del Triángulo Dorado, que ofrece salud mental ambulatoria y tratamiento de uso de sustancias para adultos con antecedentes penales bajo supervisión MDOC.",
    address="611 North Columbus Street", city="Columbus", phone="662-328-0023", email="",
    website="https://www.ccsms.org",
    eligibility="Lowndes County and Golden Triangle service area residents; Medicaid and sliding-fee accepted.",
    eligibility_es="Residentes del condado Lowndes y área del Triángulo Dorado; se aceptan Medicaid y tarifa móvil.",
    notes="Call 662-328-0023 for intake; also serves Starkville and West Point; pairs with MDOC Columbus field office.",
    notes_es="Llame al 662-328-0023 para admisión; también sirve Starkville y West Point; se vincula con oficina MDOC Columbus.",
    hours="Monday–Friday clinic hours",
    tags="columbus|lowndes|healthcare|CMHC|mental-health|reentry",
    services="Outpatient mental health|Substance use treatment|Crisis intervention|Case management|Employment referrals",
    county="Lowndes", served_counties="Lowndes|Oktibbeha|Clay|Noxubee", coverage="multi",
    _source="https://www.ccsms.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Delta Health Alliance — Greenville",
    category="healthcare", region="Greenville / Washington County",
    description="Delta Health Alliance operates community health programs and clinic partnerships across the Mississippi Delta including Washington County, providing primary care access, chronic disease management, and health navigation for uninsured and Medicaid patients such as returning citizens establishing medical care after release from MDOC custody or county jails.",
    description_es="Delta Health Alliance opera programas de salud comunitaria y alianzas con clínicas en el Delta de Mississippi incluyendo el condado Washington, proporcionando acceso a atención primaria y navegación de salud para pacientes sin seguro y Medicaid como ciudadanos que regresan.",
    address="141 South Main Street", city="Greenville", phone="662-335-0456", email="",
    website="https://www.deltahealthalliance.org",
    eligibility="Delta region residents including Washington County; sliding-fee and Medicaid patients welcome including justice-involved adults.",
    eligibility_es="Residentes de la región Delta incluyendo el condado Washington; pacientes con tarifa móvil y Medicaid bienvenidos incluidos adultos con antecedentes penales.",
    notes="Call 662-335-0456 for program information; pairs with Delta Regional Medical Center and WIN Job Center Greenville.",
    notes_es="Llame al 662-335-0456 para información del programa; se vincula con Delta Regional Medical Center y WIN Job Center Greenville.",
    hours="Monday–Friday business hours",
    tags="greenville|washington|healthcare|delta|rural|reentry",
    services="Primary care access|Chronic disease management|Health navigation|Community health programs|Medicaid enrollment referrals",
    county="Washington", served_counties="Washington|Bolivar|Sunflower|Leflore|Humphreys|Sharkey|Issaquena", coverage="multi",
    _source="https://www.deltahealthalliance.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Communicare — Oxford",
    category="healthcare", region="Oxford / Lafayette County",
    description="Communicare is the designated Community Mental Health Center for Lafayette, Marshall, and north Mississippi counties, providing outpatient psychiatric care, substance use treatment, and crisis intervention for justice-involved adults including those released from MDOC custody. The Oxford campus coordinates with Mississippi Works and University of Mississippi adult education partners.",
    description_es="Communicare es el Centro Comunitario de Salud Mental designado para Lafayette, Marshall y condados del norte de Mississippi, que ofrece atención psiquiátrica ambulatoria, tratamiento de uso de sustancias e intervención en crisis para adultos con antecedentes penales incluidos los liberados de custodia MDOC.",
    address="152 Highway 7 South", city="Oxford", phone="662-234-7521", email="",
    website="https://www.communicare.org",
    eligibility="Lafayette County and Communicare service area residents; Medicaid and sliding-fee accepted.",
    eligibility_es="Residentes del condado Lafayette y área de servicio Communicare; se aceptan Medicaid y tarifa móvil.",
    notes="Call 662-234-7521 for intake; multiple north Mississippi locations; pairs with MDOC Oxford field office.",
    notes_es="Llame al 662-234-7521 para admisión; múltiples ubicaciones del norte de Mississippi; se vincula con oficina MDOC Oxford.",
    hours="Monday–Friday clinic hours",
    tags="oxford|lafayette|healthcare|CMHC|mental-health|reentry",
    services="Outpatient psychiatric care|Substance use treatment|Crisis intervention|Case management|Probation referrals",
    county="Lafayette", served_counties="Lafayette|Marshall|Benton|Tippah|Union|Panola", coverage="multi",
    _source="https://www.communicare.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Mississippi WIN Job Center — Jackson Metro",
    category="employment", region="Jackson / Hinds County",
    description="The Jackson Metro WIN Job Center connects Hinds, Madison, and Rankin county job seekers—including justice-involved adults from Hinds County Detention Center and MDOC release—to resume coaching, WIOA training referrals, and fair-chance employer navigation. Staff link returning citizens to Hinds Behavioral Health, access.ms.gov benefits, and local reentry partners.",
    description_es="El WIN Job Center del Metro Jackson conecta buscadores de empleo de los condados Hinds, Madison y Rankin—incluidos adultos con antecedentes penales de la cárcel del condado Hinds y liberación MDOC—con coaching de currículum, referencias WIOA y navegación de empleo de segunda oportunidad.",
    address="1230 Raymond Road", city="Jackson", phone="601-321-6000", email="",
    website="https://msworks.ms.gov",
    eligibility="Open to metro Jackson job seekers including justice-involved individuals; core Mississippi Works services are free.",
    eligibility_es="Abierto a buscadores de empleo del metro Jackson incluidas personas con antecedentes penales; servicios básicos gratuitos.",
    notes="Register at msworks.ms.gov; call 601-321-6000; main state headquarters also serves as Jackson metro one-stop.",
    notes_es="Regístrese en msworks.ms.gov; llame al 601-321-6000; la sede estatal también sirve como one-stop del metro Jackson.",
    hours="Monday–Friday business hours",
    tags="jackson|hinds|employment|WIN|WIOA|fair-chance|reentry",
    services="Job search assistance|Resume coaching|WIOA training referrals|Fair-chance employment|Career workshops",
    county="Hinds", served_counties="Hinds|Madison|Rankin", coverage="multi",
    _source="https://msworks.ms.gov", _source_type="government", _confidence="high",
)
add(
    name="Mississippi WIN Job Center — Gulf Coast",
    category="employment", region="Gulfport / Harrison County",
    description="The Gulf Coast WIN Job Center in Gulfport connects Harrison, Hancock, and Jackson county job seekers including justice-involved adults to WIOA-funded training, resume assistance, and fair-chance employment navigation. Staff coordinate with Open Doors Homeless Coalition, Coastal Family Health Center, and MDOC Gulf Coast field offices.",
    description_es="El WIN Job Center de la Costa del Golfo en Gulfport conecta buscadores de empleo de los condados Harrison, Hancock y Jackson incluidos adultos con antecedentes penales con capacitación WIOA, ayuda con currículum y navegación de empleo de segunda oportunidad.",
    address="10205 Seaman Road", city="Gulfport", phone="228-864-4477", email="",
    website="https://msworks.ms.gov",
    eligibility="Open to Gulf Coast job seekers including justice-involved individuals; core services free.",
    eligibility_es="Abierto a buscadores de empleo de la Costa del Golfo incluidas personas con antecedentes penales; servicios básicos gratuitos.",
    notes="Register at msworks.ms.gov; call 228-864-4477; pairs with Back Bay Mission and Coastal Family Health Center.",
    notes_es="Regístrese en msworks.ms.gov; llame al 228-864-4477; se vincula con Back Bay Mission y Coastal Family Health Center.",
    hours="Monday–Friday business hours",
    tags="gulfport|harrison|employment|WIN|WIOA|reentry",
    services="Job search assistance|Resume coaching|WIOA referrals|Fair-chance employment|Career workshops",
    county="Harrison", served_counties="Harrison|Hancock|Jackson|Stone|George", coverage="multi",
    _source="https://msworks.ms.gov", _source_type="government", _confidence="high",
)
add(
    name="Mississippi WIN Job Center — Tupelo",
    category="employment", region="Tupelo / Lee County",
    description="The Tupelo WIN Job Center connects northeast Mississippi job seekers including justice-involved adults from Lee County Jail and MDOC release to WIOA training, resume assistance, and fair-chance employment navigation. Staff link returning citizens to Region II Mental Health Services and county MDHS offices.",
    description_es="El WIN Job Center de Tupelo conecta buscadores de empleo del noreste de Mississippi incluidos adultos con antecedentes penales con capacitación WIOA, ayuda con currículum y navegación de empleo de segunda oportunidad.",
    address="950 Industrial Park Road", city="Tupelo", phone="662-844-3333", email="",
    website="https://msworks.ms.gov",
    eligibility="Open to Lee County and northeast Mississippi job seekers including justice-involved individuals.",
    eligibility_es="Abierto a buscadores de empleo del condado Lee y noreste de Mississippi incluidas personas con antecedentes penales.",
    notes="Register at msworks.ms.gov; call 662-844-3333; pairs with Region II Mental Health and MDOC Tupelo field office.",
    notes_es="Regístrese en msworks.ms.gov; llame al 662-844-3333; se vincula con Region II Mental Health y oficina MDOC Tupelo.",
    hours="Monday–Friday business hours",
    tags="tupelo|lee|employment|WIN|WIOA|reentry",
    services="Job search assistance|Resume coaching|WIOA referrals|Fair-chance employment|Career coaching",
    county="Lee", served_counties="Lee|Prentiss|Itawamba|Pontotoc", coverage="multi",
    _source="https://msworks.ms.gov", _source_type="government", _confidence="high",
)
add(
    name="Mississippi WIN Job Center — Hattiesburg",
    category="employment", region="Hattiesburg / Forrest County",
    description="The Hattiesburg WIN Job Center connects Pine Belt job seekers including justice-involved adults to WIOA-funded training, resume assistance, and fair-chance employer connections. Staff coordinate with Pine Belt Mental Healthcare Resources and Forrest County MDHS for reentry stabilization.",
    description_es="El WIN Job Center de Hattiesburg conecta buscadores de empleo del Pine Belt incluidos adultos con antecedentes penales con capacitación WIOA, ayuda con currículum y conexiones con empleadores de segunda oportunidad.",
    address="1911 Arcadia Street", city="Hattiesburg", phone="601-544-1661", email="",
    website="https://msworks.ms.gov",
    eligibility="Open to Forrest County and Pine Belt job seekers including justice-involved individuals.",
    eligibility_es="Abierto a buscadores de empleo del condado Forrest y Pine Belt incluidas personas con antecedentes penales.",
    notes="Register at msworks.ms.gov; call 601-544-1661; pairs with Pine Belt Mental Healthcare and MDOC Hattiesburg field office.",
    notes_es="Regístrese en msworks.ms.gov; llame al 601-544-1661; se vincula con Pine Belt Mental Healthcare y oficina MDOC Hattiesburg.",
    hours="Monday–Friday business hours",
    tags="hattiesburg|forrest|employment|WIN|WIOA|reentry",
    services="Job search assistance|Resume coaching|WIOA referrals|Fair-chance employment|Career workshops",
    county="Forrest", served_counties="Forrest|Lamar|Marion|Covington", coverage="multi",
    _source="https://msworks.ms.gov", _source_type="government", _confidence="high",
)
add(
    name="Mississippi WIN Job Center — Meridian",
    category="employment", region="Meridian / Lauderdale County",
    description="The Meridian WIN Job Center connects east-central Mississippi job seekers including justice-involved adults to WIOA training, resume assistance, and fair-chance employment navigation. Staff link returning citizens to Weems Community Mental Health Center and Lauderdale County MDHS.",
    description_es="El WIN Job Center de Meridian conecta buscadores de empleo del centro-este de Mississippi incluidos adultos con antecedentes penales con capacitación WIOA y navegación de empleo de segunda oportunidad.",
    address="1200 22nd Avenue", city="Meridian", phone="601-484-0202", email="",
    website="https://msworks.ms.gov",
    eligibility="Open to Lauderdale County and east-central Mississippi job seekers including justice-involved individuals.",
    eligibility_es="Abierto a buscadores de empleo del condado Lauderdale y centro-este de Mississippi incluidas personas con antecedentes penales.",
    notes="Register at msworks.ms.gov; call 601-484-0202; pairs with Weems CMHC and MDOC Meridian field office.",
    notes_es="Regístrese en msworks.ms.gov; llame al 601-484-0202; se vincula con Weems CMHC y oficina MDOC Meridian.",
    hours="Monday–Friday business hours",
    tags="meridian|lauderdale|employment|WIN|WIOA|reentry",
    services="Job search assistance|Resume coaching|WIOA referrals|Fair-chance employment|Career coaching",
    county="Lauderdale", served_counties="Lauderdale|Clarke|Kemper|Neshoba", coverage="multi",
    _source="https://msworks.ms.gov", _source_type="government", _confidence="high",
)
add(
    name="Mississippi WIN Job Center — Columbus",
    category="employment", region="Columbus / Lowndes County",
    description="The Columbus WIN Job Center connects Golden Triangle job seekers including justice-involved adults from Lowndes County Jail and MDOC release to WIOA training, resume assistance, and fair-chance employment navigation. Staff coordinate with Community Counseling Services and local reentry partners.",
    description_es="El WIN Job Center de Columbus conecta buscadores de empleo del Triángulo Dorado incluidos adultos con antecedentes penales con capacitación WIOA y navegación de empleo de segunda oportunidad.",
    address="2330 Main Street", city="Columbus", phone="662-328-6876", email="",
    website="https://msworks.ms.gov",
    eligibility="Open to Lowndes County and Golden Triangle job seekers including justice-involved individuals.",
    eligibility_es="Abierto a buscadores de empleo del condado Lowndes y Triángulo Dorado incluidas personas con antecedentes penales.",
    notes="Register at msworks.ms.gov; call 662-328-6876; pairs with Community Counseling Services and MDOC Columbus field office.",
    notes_es="Regístrese en msworks.ms.gov; llame al 662-328-6876; se vincula con Community Counseling Services y oficina MDOC Columbus.",
    hours="Monday–Friday business hours",
    tags="columbus|lowndes|employment|WIN|WIOA|reentry",
    services="Job search assistance|Resume coaching|WIOA referrals|Fair-chance employment|Career workshops",
    county="Lowndes", served_counties="Lowndes|Oktibbeha|Clay", coverage="multi",
    _source="https://msworks.ms.gov", _source_type="government", _confidence="high",
)
add(
    name="Mississippi WIN Job Center — Greenville",
    category="employment", region="Greenville / Washington County",
    description="The Greenville WIN Job Center connects Delta region job seekers including justice-involved adults to WIOA-funded training, resume assistance, and fair-chance employment navigation in Washington and surrounding Delta counties. Staff link returning citizens to Delta Health Alliance and county MDHS offices.",
    description_es="El WIN Job Center de Greenville conecta buscadores de empleo de la región Delta incluidos adultos con antecedentes penales con capacitación WIOA y navegación de empleo de segunda oportunidad en Washington y condados Delta circundantes.",
    address="800 South Washington Avenue", city="Greenville", phone="662-335-3361", email="",
    website="https://msworks.ms.gov",
    eligibility="Open to Washington County and Delta region job seekers including justice-involved individuals.",
    eligibility_es="Abierto a buscadores de empleo del condado Washington y región Delta incluidas personas con antecedentes penales.",
    notes="Register at msworks.ms.gov; call 662-335-3361; pairs with Delta Health Alliance and Delta Regional Medical Center.",
    notes_es="Regístrese en msworks.ms.gov; llame al 662-335-3361; se vincula con Delta Health Alliance y Delta Regional Medical Center.",
    hours="Monday–Friday business hours",
    tags="greenville|washington|employment|WIN|WIOA|reentry|delta",
    services="Job search assistance|Resume coaching|WIOA referrals|Fair-chance employment|Career coaching",
    county="Washington", served_counties="Washington|Bolivar|Sunflower|Leflore", coverage="multi",
    _source="https://msworks.ms.gov", _source_type="government", _confidence="high",
)
add(
    name="Mississippi WIN Job Center — Oxford",
    category="employment", region="Oxford / Lafayette County",
    description="The Oxford WIN Job Center connects north Mississippi job seekers including justice-involved adults to WIOA training, resume assistance, and fair-chance employer navigation. Staff coordinate with Communicare, Mississippi Center for Legal Services Tupelo region, and Lafayette County MDHS.",
    description_es="El WIN Job Center de Oxford conecta buscadores de empleo del norte de Mississippi incluidos adultos con antecedentes penales con capacitación WIOA y navegación de empleo de segunda oportunidad.",
    address="1037 Jackson Avenue West", city="Oxford", phone="662-234-2911", email="",
    website="https://msworks.ms.gov",
    eligibility="Open to Lafayette County and north Mississippi job seekers including justice-involved individuals.",
    eligibility_es="Abierto a buscadores de empleo del condado Lafayette y norte de Mississippi incluidas personas con antecedentes penales.",
    notes="Register at msworks.ms.gov; call 662-234-2911; pairs with Communicare and MDOC Oxford field office.",
    notes_es="Regístrese en msworks.ms.gov; llame al 662-234-2911; se vincula con Communicare y oficina MDOC Oxford.",
    hours="Monday–Friday business hours",
    tags="oxford|lafayette|employment|WIN|WIOA|reentry",
    services="Job search assistance|Resume coaching|WIOA referrals|Fair-chance employment|Career coaching",
    county="Lafayette", served_counties="Lafayette|Marshall|Benton|Panola", coverage="multi",
    _source="https://msworks.ms.gov", _source_type="government", _confidence="high",
)

# --- County benefits + expansion modules ---
from county_benefits_registry import register_county_benefits_mississippi

_existing_fa = {
    e["county"]
    for e in ENTRIES
    if e["category"] == "financial-assistance" and e.get("county")
}
register_county_benefits_mississippi(add, _existing_fa)

from mississippi_phase4_expansion import register_phase4
register_phase4(add)

from mississippi_category_fill import register_category_fill
register_category_fill(add)

from mississippi_thin_counties import register_thin_counties
register_thin_counties(add)

from mississippi_gap_fill import register_gap_fill
register_gap_fill(add)

from mississippi_minimum_closure import register_minimum_closure
register_minimum_closure(add)

from mississippi_gap_fill import register_mechanical_tier_a
register_mechanical_tier_a(add)

from mississippi_gap_fill import register_tier_a_final
register_tier_a_final(add)


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
