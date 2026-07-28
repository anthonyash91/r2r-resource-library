#!/usr/bin/env python3
"""Generate wisconsin-resources.csv and wisconsin-research-log.csv.

RESOURCES_UUID_PREFIX comment e0000001
"""
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES_PATH = ROOT / "data" / "wisconsin-resources.csv"
LOG_PATH = ROOT / "data" / "wisconsin-research-log.csv"
DATE = "2026-07-07"

COLUMNS = [
    "id", "name", "category", "region", "description", "description_es",
    "address", "city", "phone", "email", "website", "eligibility", "eligibility_es",
    "notes", "notes_es", "hours", "tags", "services", "county", "served_counties", "coverage",
]
LOG_COLUMNS = ["source_url", "source_type", "date_accessed", "confidence", "notes", "id_reference"]

ENTRIES = []


def add(**kw):
    ENTRIES.append(kw)


# --- Phase 1: Statewide backbone (~18 rows) ---
add(
    name="WDOC — Reentry & Community Corrections",
    category="state-agency", region="Statewide",
    description="The Wisconsin Department of Corrections Division of Community Corrections coordinates statewide reentry planning, pre-release programming, and community supervision for individuals preparing to leave WDOC custody or under probation and extended supervision across all 72 counties. Reentry staff connect returning citizens to ACCESS Wisconsin benefits, Job Center of Wisconsin employment services, ForwardHealth/BadgerCare Plus enrollment, and local treatment and housing partners before and after release. This office provides planning and referrals—not a walk-in crisis line or emergency cash provider.",
    description_es="El Departamento de Correcciones de Wisconsin, División de Correcciones Comunitarias, coordina la planificación estatal de reinserción, programación previa a la liberación y supervisión comunitaria para personas que se preparan para salir de custodia de WDOC o bajo probatoria y supervisión extendida en los 72 condados. El personal de reinserción conecta a ciudadanos que regresan con beneficios ACCESS Wisconsin, centros Job Center of Wisconsin e inscripción en ForwardHealth/BadgerCare Plus. Esta oficina ofrece planificación y referencias, no es una línea de crisis ni proveedor de efectivo de emergencia.",
    address="3099 East Washington Avenue", city="Madison", phone="608-240-5000", email="",
    website="https://doc.wi.gov",
    eligibility="Individuals in WDOC custody preparing for release or under community supervision; community partners seeking WDOC reentry engagement.",
    eligibility_es="Personas en custodia de WDOC que se preparan para la liberación o bajo supervisión comunitaria; aliados comunitarios que buscan coordinación de reinserción.",
    notes="Visit doc.wi.gov for reentry resources; coordinate through facility reentry staff and assigned probation or parole agent after release.",
    notes_es="Visite doc.wi.gov para recursos de reinserción; coordine a través del personal de reinserción de la instalación y el agente de probatoria asignado.",
    hours="State office Monday–Friday business hours",
    tags="statewide|reentry|WDOC|DOC|pre-release|community-corrections",
    services="Pre-release planning|Community corrections coordination|Partner referrals|Reentry resource navigation|Supervision linkage",
    county="Dane", served_counties="", coverage="statewide",
    _source="https://doc.wi.gov", _source_type="government", _confidence="high",
)
add(
    name="WDOC — Probation & Parole Field Operations",
    category="probation-parole", region="Statewide",
    description="WDOC Probation and Parole Field Operations supervises adults on probation, parole, and extended supervision through regional field offices across Wisconsin, connecting supervisees to employment, treatment, and housing referrals as conditions of release. Field agents coordinate with Job Center of Wisconsin, county DHS benefits offices, Comprehensive Community Services providers, and local reentry nonprofits in every region. Contact your assigned agent—not a walk-in benefits or emergency housing intake center.",
    description_es="Operaciones de Campo de Probatoria y Libertad Condicional de WDOC supervisa adultos en probatoria, libertad condicional y supervisión extendida a través de oficinas regionales en Wisconsin, conectando supervisados con empleo, tratamiento y vivienda según condiciones de liberación. Los agentes coordinan con Job Center of Wisconsin, oficinas DHS del condado y proveedores CCS. Contacte a su agente asignado; no es un centro de admisión de beneficios o vivienda de emergencia.",
    address="3099 East Washington Avenue", city="Madison", phone="608-240-5000", email="",
    website="https://doc.wi.gov/Pages/OffenderInformation/ProbationParole.aspx",
    eligibility="Adults under WDOC probation, parole, or extended supervision in Wisconsin; report to assigned field agent.",
    eligibility_es="Adultos bajo supervisión probatoria, de libertad condicional o supervisión extendida de WDOC en Wisconsin; reporte al agente de campo asignado.",
    notes="Find regional field office contacts at doc.wi.gov; ask your agent about local reentry referrals and treatment requirements.",
    notes_es="Encuentre contactos de oficinas regionales en doc.wi.gov; pregunte a su agente sobre referencias locales de reinserción.",
    hours="Field offices typically Monday–Friday business hours",
    tags="statewide|probation-parole|WDOC|parole|community-supervision|reentry",
    services="Probation supervision|Parole supervision|Extended supervision reporting|Treatment referrals|Reentry partner coordination",
    county="Dane", served_counties="", coverage="statewide",
    _source="https://doc.wi.gov/Pages/OffenderInformation/ProbationParole.aspx", _source_type="government", _confidence="high",
)
add(
    name="ACCESS Wisconsin — Benefits Portal",
    category="financial-assistance", region="Statewide",
    description="ACCESS Wisconsin is the official online portal for applying for and managing FoodShare (SNAP) nutrition assistance, Wisconsin Works (W-2) cash benefits, child care subsidies, and BadgerCare Plus Medicaid applications through county DHS Eligibility Management offices. Justice-involved Wisconsinites can apply for food and health coverage after release from WDOC custody or county jails using the same account used by all 72 county DHS offices statewide.",
    description_es="ACCESS Wisconsin es el portal en línea oficial para solicitar y administrar asistencia alimentaria FoodShare (SNAP), beneficios en efectivo Wisconsin Works (W-2), subsidios de cuidado infantil y solicitudes de Medicaid BadgerCare Plus a través de oficinas de Gestión de Elegibilidad DHS del condado. Los habitantes de Wisconsin en reinserción pueden solicitar apoyo alimentario y de salud después de la liberación.",
    address="", city="", phone="1-800-362-3002", email="", website="https://access.wi.gov",
    eligibility="Wisconsin residents meeting income and household-size requirements for FoodShare, W-2, or BadgerCare Plus; criminal record generally not a barrier to FoodShare eligibility.",
    eligibility_es="Residentes de Wisconsin que cumplan requisitos de ingresos y tamaño del hogar para FoodShare, W-2 o BadgerCare Plus; los antecedentes penales generalmente no son barrera para FoodShare.",
    notes="Apply online at access.wi.gov; call 1-800-362-3002 for ACCESS customer service; visit your county DHS EM office for in-person verification.",
    notes_es="Solicite en access.wi.gov; llame al 1-800-362-3002; visite su oficina DHS EM del condado para verificación presencial.",
    hours="Online 24/7; county DHS office hours vary",
    tags="statewide|benefits|FoodShare|SNAP|ACCESS-Wisconsin|reentry",
    services="FoodShare enrollment|W-2 application|Child care subsidy applications|BadgerCare Plus referral|County DHS office locator",
    county="", served_counties="", coverage="statewide",
    _source="https://access.wi.gov", _source_type="government", _confidence="high",
)
add(
    name="ForwardHealth — BadgerCare Plus",
    category="healthcare", region="Statewide",
    description="ForwardHealth administers BadgerCare Plus and Medicaid health coverage for eligible low-income Wisconsin residents statewide, including pregnant women, children, disabled adults, and adults under the Medicaid expansion population through managed care organizations. Returning citizens can apply for BadgerCare Plus before or immediately after release to secure prescription and primary care coverage; member services staff help with enrollment questions and eligibility appeals by phone.",
    description_es="ForwardHealth administra BadgerCare Plus y cobertura Medicaid para residentes elegibles de bajos ingresos en todo Wisconsin, incluidas mujeres embarazadas, niños, adultos discapacitados y adultos bajo la población de expansión de Medicaid. Los ciudadanos que regresan pueden solicitar BadgerCare Plus antes o inmediatamente después de la liberación para asegurar cobertura de recetas y atención primaria.",
    address="1 West Wilson Street", city="Madison", phone="800-362-3002", email="",
    website="https://www.dhs.wisconsin.gov/badgercareplus/index.htm",
    eligibility="Wisconsin residents meeting income and category requirements for BadgerCare Plus or Medicaid; Wisconsin has expanded Medicaid to low-income adults.",
    eligibility_es="Residentes de Wisconsin que cumplan requisitos de ingresos y categoría para BadgerCare Plus o Medicaid; Wisconsin ha expandido Medicaid a adultos de bajos ingresos.",
    notes="Apply through access.wi.gov; call 800-362-3002; ask about presumptive eligibility and disability-based categories.",
    notes_es="Solicite a través de access.wi.gov o llame al 800-362-3002; pregunte sobre elegibilidad presuntiva y categorías por discapacidad.",
    hours="Member services Monday–Friday business hours",
    tags="statewide|healthcare|BadgerCare|Medicaid|ForwardHealth|reentry",
    services="BadgerCare Plus application assistance|Eligibility determination|Managed care navigation|Member services helpline|Appeals support",
    county="Dane", served_counties="", coverage="statewide",
    _source="https://www.dhs.wisconsin.gov/badgercareplus/index.htm", _source_type="government", _confidence="high",
)
add(
    name="211 Wisconsin",
    category="state-agency", region="Statewide",
    description="211 Wisconsin is a free statewide information and referral service connecting residents to health and human services including housing, food, utilities, employment, and crisis support across all 72 counties. United Way–supported navigators help callers find local programs by need and ZIP code through 211wisconsin.org and by dialing 211 from any Wisconsin phone. 211 Wisconsin is a referral service—not a direct-service provider.",
    description_es="211 Wisconsin es un servicio gratuito de información y referencia estatal que conecta a residentes con servicios de salud y humanos incluyendo vivienda, alimentos, servicios públicos, empleo y apoyo en crisis en los 72 condados. Navegadores apoyados por United Way ayudan a encontrar programas locales por necesidad y código postal. Es un servicio de referencia, no un proveedor directo.",
    address="", city="", phone="211", email="", website="https://211wisconsin.org",
    eligibility="Open to all Wisconsin residents; no criminal-record restrictions stated.",
    eligibility_es="Abierto a todos los residentes de Wisconsin; sin restricciones de antecedentes indicadas.",
    notes="Dial 211 from any Wisconsin phone; search resources online at 211wisconsin.org; text your ZIP code to 898-211 where available.",
    notes_es="Marque 211 desde cualquier teléfono de Wisconsin; busque recursos en 211wisconsin.org; envíe su código postal al 898-211 donde esté disponible.",
    hours="Available 24/7 in most areas; check 211wisconsin.org",
    tags="statewide|hotline|211|referral-only|basic-needs",
    services="Information and referral|Housing resource navigation|Benefits referrals|Crisis resource connections|Local program search",
    county="", served_counties="", coverage="statewide",
    _source="https://211wisconsin.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Legal Action of Wisconsin — Statewide Intake",
    category="legal-aid", region="Statewide",
    description="Legal Action of Wisconsin is the state's primary nonprofit civil legal aid provider serving low-income Wisconsinites with housing, public benefits, family law, and criminal record relief including expungement and pardon guidance under Wisconsin law. Centralized statewide intake routes callers to regional offices in Milwaukee, Madison, Green Bay, and Wausau—not criminal defense representation.",
    description_es="Legal Action of Wisconsin es el principal proveedor sin fines de lucro de asistencia legal civil del estado que sirve a personas de bajos ingresos con vivienda, beneficios públicos, derecho familiar y alivio de antecedentes penales incluida orientación sobre expungación y perdón bajo la ley de Wisconsin. La admisión centralizada enruta a oficinas regionales, no defensa penal.",
    address="230 West Wells Street, Suite 800", city="Milwaukee", phone="888-278-0633", email="",
    website="https://www.legalaction.org",
    eligibility="Low-income Wisconsin residents with non-criminal legal problems; LSC income limits apply; offense-type restrictions may apply for record relief eligibility.",
    eligibility_es="Residentes de Wisconsin de bajos ingresos con problemas legales no penales; aplican límites de ingresos LSC; pueden aplicar restricciones por tipo de delito para alivio de antecedentes.",
    notes="Apply online at legalaction.org or call 888-278-0633; regional offices serve specific counties listed on the website.",
    notes_es="Solicite en legalaction.org o llame al 888-278-0633; las oficinas regionales sirven condados específicos listados en el sitio web.",
    hours="Intake Monday–Friday business hours; online application 24/7",
    tags="statewide|legal-aid|low-income|expungement|hotline",
    services="Civil legal representation|Expungement assistance|Housing legal aid|Benefits advocacy|Regional office referrals",
    county="Milwaukee", served_counties="", coverage="statewide",
    _source="https://www.legalaction.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Wisconsin Judicare — Northern Wisconsin Legal Aid",
    category="legal-aid", region="Statewide",
    description="Wisconsin Judicare provides free civil legal services to low-income residents in northern and central Wisconsin counties including housing, public benefits, family law, and record relief matters. Justice-involved adults in rural Wisconsin can access Judicare attorneys through county intake—not criminal defense. Serves counties not covered by Legal Action of Wisconsin regional offices.",
    description_es="Wisconsin Judicare ofrece servicios legales civiles gratuitos a residentes de bajos ingresos en condados del norte y centro de Wisconsin incluyendo vivienda, beneficios, derecho familiar y alivio de antecedentes. Los adultos con antecedentes penales en Wisconsin rural pueden acceder a abogados de Judicare a través de admisión del condado, no defensa penal.",
    address="300 Third Street, Suite 300", city="Wausau", phone="800-472-1639", email="",
    website="https://www.judicare.org",
    eligibility="Low-income residents in Judicare service counties; income and household-size limits apply; non-criminal legal matters only.",
    eligibility_es="Residentes de bajos ingresos en condados de servicio de Judicare; aplican límites de ingresos; solo asuntos legales no penales.",
    notes="Call 800-472-1639 for intake; office locator at judicare.org; pairs with county DHS and Job Center offices.",
    notes_es="Llame al 800-472-1639 para admisión; localizador de oficinas en judicare.org; se vincula con oficinas DHS y Job Center del condado.",
    hours="Intake Monday–Friday business hours",
    tags="statewide|legal-aid|northern-wisconsin|rural|expungement",
    services="Civil legal representation|Housing legal aid|Benefits advocacy|Family law assistance|Record relief guidance",
    county="Marathon", served_counties="", coverage="statewide",
    _source="https://www.judicare.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Job Center of Wisconsin — Statewide Network",
    category="employment", region="Statewide",
    description="Job Center of Wisconsin is the statewide workforce development network operated through the Wisconsin Department of Workforce Development, connecting job seekers in all 72 counties to career coaching, WIOA training referrals, and fair-chance employment navigation. Justice-involved adults leaving WDOC custody or county jails can register at wisconsinjobcenter.org for free core services at local one-stop centers. Workforce services—not emergency cash or housing placement.",
    description_es="Job Center of Wisconsin es la red estatal de desarrollo de la fuerza laboral operada por el Departamento de Desarrollo de la Fuerza Laboral de Wisconsin, conectando buscadores de empleo en los 72 condados con coaching de carrera y referencias de capacitación WIOA. Los adultos con antecedentes penales pueden registrarse en wisconsinjobcenter.org para servicios básicos gratuitos.",
    address="201 East Washington Avenue", city="Madison", phone="888-258-9966", email="",
    website="https://www.wisconsinjobcenter.org",
    eligibility="Open to Wisconsin job seekers including justice-involved individuals; core Job Center services are free.",
    eligibility_es="Abierto a buscadores de empleo de Wisconsin incluidas personas con antecedentes penales; servicios básicos gratuitos.",
    notes="Register at wisconsinjobcenter.org; find your nearest Job Center by ZIP code; pairs with ACCESS Wisconsin benefits and DVR vocational rehabilitation.",
    notes_es="Regístrese en wisconsinjobcenter.org; encuentre su Job Center más cercano por código postal; se vincula con beneficios ACCESS Wisconsin y rehabilitación vocacional DVR.",
    hours="Job Centers typically Monday–Friday business hours",
    tags="statewide|employment|job-center|WIOA|fair-chance|reentry",
    services="Career coaching|Resume assistance|WIOA training referrals|Job search tools|Fair-chance employment navigation",
    county="Dane", served_counties="", coverage="statewide",
    _source="https://www.wisconsinjobcenter.org", _source_type="government", _confidence="high",
)
add(
    name="DVR — Division of Vocational Rehabilitation",
    category="employment", region="Statewide",
    description="The Wisconsin Division of Vocational Rehabilitation helps Wisconsinites with disabilities—including justice-involved individuals with qualifying disabilities—prepare for, obtain, and maintain employment through vocational counseling, assistive technology, training, and job placement at district offices statewide. DVR counselors coordinate with Job Center of Wisconsin, ForwardHealth behavioral health providers, and WDOC reentry staff on individualized employment plans. DVR eligibility requires a documented disability affecting employment—not general reentry case management.",
    description_es="La División de Rehabilitación Vocacional de Wisconsin ayuda a habitantes de Wisconsin con discapacidades—incluidas personas con antecedentes penales con discapacidades calificadas—a prepararse, obtener y mantener empleo mediante consejería vocacional, tecnología de asistencia y colocación laboral. La elegibilidad DVR requiere una discapacidad documentada que afecte el empleo.",
    address="201 East Washington Avenue", city="Madison", phone="800-442-3477", email="",
    website="https://dwd.wisconsin.gov/dvr",
    eligibility="Wisconsin residents with a physical or mental disability that is a substantial barrier to employment; justice-involved applicants welcome if DVR eligible.",
    eligibility_es="Residentes de Wisconsin con una discapacidad física o mental que sea una barrera sustancial al empleo; solicitantes con antecedentes penales bienvenidos si son elegibles para DVR.",
    notes="Apply at dwd.wisconsin.gov/dvr or call 800-442-3477; district office locations listed on the DVR website.",
    notes_es="Solicite en dwd.wisconsin.gov/dvr o llame al 800-442-3477; las ubicaciones de oficinas de distrito están en el sitio web de DVR.",
    hours="District offices Monday–Friday business hours",
    tags="statewide|employment|DVR|vocational-rehabilitation|disability|reentry",
    services="Vocational counseling|Job placement|Assistive technology|Skills training|Disability employment supports",
    county="Dane", served_counties="", coverage="statewide",
    _source="https://dwd.wisconsin.gov/dvr", _source_type="government", _confidence="high",
)
add(
    name="Wisconsin Department of Veterans Affairs (WDVA)",
    category="veterans", region="Statewide",
    description="The Wisconsin Department of Veterans Affairs helps justice-involved veterans access VA benefits, disability claims, education benefits, and housing resources through county veterans service officers across all 72 counties. Veterans released from incarceration may qualify for VA health care, vocational rehabilitation, and veterans treatment court supports. Benefits navigation and claims advocacy—not emergency shelter.",
    description_es="El Departamento de Asuntos de Veteranos de Wisconsin ayuda a veteranos con antecedentes penales a acceder a beneficios del VA, reclamaciones de discapacidad, beneficios educativos y recursos de vivienda a través de oficiales de servicios para veteranos del condado en los 72 condados. Los veteranos liberados pueden calificar para atención médica del VA y tribunales de tratamiento para veteranos.",
    address="201 West Washington Avenue", city="Madison", phone="800-947-8387", email="",
    website="https://dva.wisconsin.gov",
    eligibility="Honorably discharged or qualifying Wisconsin veterans and their dependents; service documentation required.",
    eligibility_es="Veteranos de Wisconsin con baja honorable o calificados y sus dependientes; se requiere documentación de servicio.",
    notes="Find your county veterans service officer at dva.wisconsin.gov; free benefits claims assistance available at county offices statewide.",
    notes_es="Encuentre su oficial de servicios para veteranos del condado en dva.wisconsin.gov; asistencia gratuita con reclamaciones disponible en oficinas del condado.",
    hours="County offices Monday–Friday business hours",
    tags="statewide|veterans|VA-benefits|reentry|justice-involved-veterans",
    services="VA benefits claims assistance|Disability claims navigation|Education benefits guidance|Veterans treatment court support|County VSO referrals",
    county="Dane", served_counties="", coverage="statewide",
    _source="https://dva.wisconsin.gov", _source_type="government", _confidence="high",
)
add(
    name="WisDOT — Division of Motor Vehicles",
    category="id-documentation", region="Statewide",
    description="The Wisconsin Department of Transportation Division of Motor Vehicles issues state ID cards and driver's licenses required for employment, housing, and benefits enrollment after release. Returning citizens can apply for a Wisconsin ID at DMV service centers statewide with proof of identity and residency. Not a vital records office—contact Wisconsin Vital Records or your county Register of Deeds for birth certificates.",
    description_es="La División de Vehículos Motorizados del Departamento de Transporte de Wisconsin emite tarjetas de identificación estatal y licencias de conducir necesarias para empleo, vivienda e inscripción en beneficios después de la liberación. Los ciudadanos que regresan pueden solicitar una identificación de Wisconsin en centros de servicio DMV con prueba de identidad y residencia. No es oficina de registros vitales.",
    address="4802 Sheboygan Avenue", city="Madison", phone="608-264-7447", email="",
    website="https://wisdot.gov/Pages/dmv/index.aspx",
    eligibility="Wisconsin residents with required identity and residency documentation; fees apply for ID cards and licenses.",
    eligibility_es="Residentes de Wisconsin con documentación requerida de identidad y residencia; aplican tarifas para tarjetas de identificación.",
    notes="Find DMV service centers at wisdot.gov; bring certified birth certificate or passport plus proof of Wisconsin residency.",
    notes_es="Encuentre centros de servicio DMV en wisdot.gov; traiga certificado de nacimiento o pasaporte más prueba de residencia en Wisconsin.",
    hours="DMV service center hours vary; check wisdot.gov",
    tags="statewide|id-documentation|DMV|drivers-license|state-id|reentry",
    services="State ID card issuance|Driver's license services|ID renewal|DMV service center locator",
    county="Dane", served_counties="", coverage="statewide",
    _source="https://wisdot.gov/Pages/dmv/index.aspx", _source_type="government", _confidence="high",
)
add(
    name="Wisconsin Vital Records",
    category="id-documentation", region="Statewide",
    description="The Wisconsin Department of Health Services Vital Records office issues certified birth certificates, death certificates, and marriage records needed for state ID applications, benefits enrollment, and employment verification after release. Returning citizens can order records online, by mail, or in person with valid identification. Vital records issuance—not a driver license or probation office.",
    description_es="La oficina de Registros Vitales del Departamento de Servicios de Salud de Wisconsin emite certificados de nacimiento, defunción y matrimonio necesarios para solicitudes de identificación estatal, inscripción en beneficios y verificación de empleo después de la liberación. Los ciudadanos que regresan pueden solicitar registros en línea, por correo o en persona.",
    address="1 West Wilson Street, Room 158", city="Madison", phone="608-266-1371", email="",
    website="https://www.dhs.wisconsin.gov/vitalrecords/index.htm",
    eligibility="Individuals with valid ID requesting their own vital records or authorized family members; fees apply per certificate.",
    eligibility_es="Personas con identificación válida que soliciten sus propios registros vitales o familiares autorizados; aplican tarifas por certificado.",
    notes="Order online at dhs.wisconsin.gov/vitalrecords; some records available through county Register of Deeds offices.",
    notes_es="Solicite en línea en dhs.wisconsin.gov/vitalrecords; algunos registros disponibles a través de oficinas del Registro de Actos del condado.",
    hours="Monday–Friday business hours",
    tags="statewide|id-documentation|vital-records|birth-certificate|reentry",
    services="Birth certificate issuance|Death certificate issuance|Marriage record copies|Online ordering|In-person vital records service",
    county="Dane", served_counties="", coverage="statewide",
    _source="https://www.dhs.wisconsin.gov/vitalrecords/index.htm", _source_type="government", _confidence="high",
)
add(
    name="988 Suicide & Crisis Lifeline — Wisconsin",
    category="healthcare", region="Statewide",
    description="Free confidential 24/7 crisis support for people experiencing mental health emergencies, suicidal thoughts, or substance use crises in Wisconsin. Trained specialists provide immediate support and can connect callers to local mobile crisis teams through county crisis services partners statewide. Available to anyone—not reentry-specific but essential for justice-involved individuals in crisis.",
    description_es="Apoyo gratuito y confidencial 24/7 para emergencias de salud mental, pensamientos suicidas o crisis por uso de sustancias en Wisconsin. Especialistas capacitados ofrecen apoyo inmediato y conexión a equipos de crisis móviles a través de aliados de servicios de crisis del condado. Disponible para cualquier persona, esencial para personas con antecedentes penales en crisis.",
    address="", city="", phone="988", email="", website="https://988lifeline.org",
    eligibility="Open to anyone in Wisconsin experiencing a mental health or suicide crisis; no eligibility restrictions.",
    eligibility_es="Abierto a cualquier persona en Wisconsin en crisis de salud mental o suicidio; sin restricciones.",
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
    description="Free confidential 24/7 treatment referral and information service for individuals and families facing mental health or substance use disorders. Provides referrals to local treatment facilities and community organizations in Wisconsin and nationwide. Spanish-language support available through trained specialists for justice-involved individuals seeking SUD or mental health treatment after release.",
    description_es="Servicio gratuito y confidencial 24/7 de referencia e información para personas y familias con trastornos de salud mental o uso de sustancias. Proporciona referencias a centros de tratamiento locales en Wisconsin y a nivel nacional. Soporte en español disponible para personas con antecedentes penales que buscan tratamiento después de la liberación.",
    address="", city="", phone="800-662-4357", email="",
    website="https://www.samhsa.gov/find-help/national-helpline",
    eligibility="Open to anyone in the United States seeking substance use or mental health treatment information and referrals.",
    eligibility_es="Abierto a cualquier persona en Estados Unidos que busque información y referencias de tratamiento.",
    notes="TTY 800-487-4889; also use FindTreatment.gov to search Wisconsin providers online.",
    notes_es="TTY 800-487-4889; también use FindTreatment.gov para buscar proveedores en Wisconsin.",
    hours="Available 24/7",
    tags="statewide|hotline|substance-use|treatment-referral|national",
    services="Treatment referrals|Substance use information|Mental health resource navigation",
    county="", served_counties="", coverage="statewide",
    _source="https://www.samhsa.gov/find-help/national-helpline", _source_type="government", _confidence="high",
)
add(
    name="FindTreatment.gov — Wisconsin Provider Search",
    category="substance-use-treatment", region="Statewide",
    description="SAMHSA's online treatment locator helping Wisconsin residents find substance use and mental health treatment providers by location, service type, and payment options including BadgerCare Plus Medicaid. Justice-involved individuals can search outpatient, residential, and MAT providers before or after release from WDOC custody or county jails across all 72 counties.",
    description_es="Localizador en línea de SAMHSA que ayuda a residentes de Wisconsin a encontrar proveedores de tratamiento de uso de sustancias y salud mental por ubicación, tipo de servicio y opciones de pago incluido BadgerCare Plus Medicaid. Personas con antecedentes penales pueden buscar proveedores ambulatorios, residenciales y TMO antes o después de la liberación.",
    address="", city="", phone="", email="", website="https://findtreatment.gov",
    eligibility="Open to anyone searching for treatment; provider admission rules vary.",
    eligibility_es="Abierto a cualquier persona que busque tratamiento; las reglas de admisión varían según el proveedor.",
    notes="Search findtreatment.gov by Wisconsin county or city; filter for MAT, outpatient, or residential services.",
    notes_es="Busque en findtreatment.gov por condado o ciudad de Wisconsin; filtre por TMO, ambulatorio o residencial.",
    hours="Website 24/7",
    tags="statewide|substance-use|online|MAT|treatment-locator",
    services="Treatment provider search|MAT locator|Outpatient program finder|Residential program finder",
    county="", served_counties="", coverage="statewide",
    _source="https://findtreatment.gov", _source_type="government", _confidence="high",
)
add(
    name="Wisconsin DHS — Comprehensive Community Services (CCS)",
    category="healthcare", region="Statewide",
    description="The Wisconsin Department of Health Services Comprehensive Community Services program provides community-based mental health and substance use recovery supports including peer specialists, psychosocial rehabilitation, and care coordination for eligible adults in participating counties. Justice-involved individuals with serious mental illness or substance use disorders may access CCS through county mental health or substance use agencies after release—not a direct crisis hotline itself.",
    description_es="El programa de Servicios Comunitarios Integrales del Departamento de Servicios de Salud de Wisconsin ofrece apoyos comunitarios de salud mental y recuperación de uso de sustancias incluidos especialistas entre pares, rehabilitación psicosocial y coordinación de atención para adultos elegibles en condados participantes. Personas con antecedentes penales pueden acceder a CCS a través de agencias de salud mental del condado después de la liberación.",
    address="1 West Wilson Street", city="Madison", phone="608-266-2717", email="",
    website="https://www.dhs.wisconsin.gov/ccs/index.htm",
    eligibility="Wisconsin adults in participating counties with serious mental illness or substance use disorders meeting CCS eligibility; county enrollment required.",
    eligibility_es="Adultos de Wisconsin en condados participantes con enfermedad mental grave o trastornos por uso de sustancias que cumplan elegibilidad CCS; se requiere inscripción del condado.",
    notes="Contact your county mental health or substance use agency; call 988 for immediate crisis support statewide.",
    notes_es="Contacte su agencia de salud mental o uso de sustancias del condado; llame al 988 para apoyo inmediato en crisis en todo el estado.",
    hours="State office Monday–Friday business hours; county CCS hours vary",
    tags="statewide|healthcare|CCS|mental-health|substance-use|reentry",
    services="Peer specialist services|Psychosocial rehabilitation|Care coordination|Substance use recovery supports|County CCS enrollment",
    county="Dane", served_counties="", coverage="statewide",
    _source="https://www.dhs.wisconsin.gov/ccs/index.htm", _source_type="government", _confidence="high",
)
add(
    name="Wisconsin Community Services — Statewide Reentry",
    category="reentry-organizations", region="Statewide",
    description="Wisconsin Community Services is a statewide nonprofit providing reentry case management, employment navigation, behavioral health referrals, and housing support for justice-involved adults returning from WDOC custody and county jails across Wisconsin. WCS partners with Job Center of Wisconsin, ACCESS Wisconsin benefits offices, and local treatment providers—not a walk-in emergency shelter or crisis line.",
    description_es="Wisconsin Community Services es una organización sin fines de lucro estatal que ofrece manejo de casos de reinserción, navegación laboral, referencias de salud conductual y apoyo de vivienda para adultos con antecedentes penales que regresan de custodia WDOC y cárceles del condado en Wisconsin. WCS se asocia con Job Center of Wisconsin y oficinas ACCESS Wisconsin, no es refugio de emergencia ni línea de crisis.",
    address="3737 West Wisconsin Avenue", city="Milwaukee", phone="414-290-6800", email="",
    website="https://www.wiscs.org",
    eligibility="Justice-involved Wisconsin adults referred by WDOC, courts, or community partners; program eligibility varies by site.",
    eligibility_es="Adultos de Wisconsin con antecedentes penales referidos por WDOC, tribunales o aliados comunitarios; la elegibilidad del programa varía según el sitio.",
    notes="Contact WCS at 414-290-6800 for program referrals; coordinate through assigned WDOC agent for DOC-linked services.",
    notes_es="Contacte WCS al 414-290-6800 para referencias del programa; coordine a través del agente WDOC asignado para servicios vinculados al DOC.",
    hours="Monday–Friday business hours; program hours vary",
    tags="statewide|reentry|case-management|employment|referral-only",
    services="Reentry case management|Employment navigation|Behavioral health referrals|Housing support|Benefits navigation",
    county="Milwaukee", served_counties="", coverage="statewide",
    _source="https://www.wiscs.org", _source_type="nonprofit", _confidence="high",
)

# --- Phase 2: Major metro anchors (~12 rows) ---
add(
    name="Guest House of Milwaukee",
    category="housing", region="Milwaukee / Milwaukee County",
    description="Guest House of Milwaukee provides emergency shelter, meals, case management, and housing navigation for men experiencing homelessness in Milwaukee County including returning citizens recently released from Milwaukee County Jail or WDOC custody without a fixed address. Staff help guests connect to shelter beds, ACCESS Wisconsin benefits, Job Center of Wisconsin employment services, and Sixteenth Street Community Health Centers for medical care.",
    description_es="Guest House of Milwaukee ofrece refugio de emergencia, comidas, manejo de casos y navegación de vivienda para hombres que enfrentan falta de vivienda en el condado Milwaukee incluidos ciudadanos recién liberados de la cárcel del condado Milwaukee o custodia WDOC sin dirección fija. El personal ayuda a conectarse con refugio, beneficios ACCESS Wisconsin y servicios de empleo Job Center of Wisconsin.",
    address="1216 North 13th Street", city="Milwaukee", phone="414-645-8000", email="",
    website="https://www.guesthouseofmilwaukee.org",
    eligibility="Homeless men in Milwaukee County; walk-in intake during posted hours; justice-involved guests welcome per program policy.",
    eligibility_es="Hombres sin hogar en el condado Milwaukee; admisión sin cita durante horario publicado; huéspedes con antecedentes penales bienvenidos según política del programa.",
    notes="Call 414-645-8000 for intake; pairs with Community Advocates and Hope House for extended housing programs.",
    notes_es="Llame al 414-645-8000 para admisión; se vincula con Community Advocates y Hope House para programas de vivienda extendidos.",
    hours="Intake during posted business hours; shelter 24/7",
    tags="milwaukee|housing|emergency-shelter|men|reentry",
    services="Emergency shelter|Meals|Case management|Housing navigation|Benefits referrals",
    county="Milwaukee", served_counties="Milwaukee", coverage="single",
    _source="https://www.guesthouseofmilwaukee.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Hope House of Milwaukee",
    category="housing", region="Milwaukee / Milwaukee County",
    description="Hope House of Milwaukee provides emergency shelter, transitional housing, and supportive services for families and single adults experiencing homelessness in Milwaukee including justice-involved adults rebuilding stable housing after incarceration. Case managers connect residents to ACCESS Wisconsin, Job Center of Wisconsin, and Legal Action of Wisconsin for benefits, employment, and tenant-rights support.",
    description_es="Hope House of Milwaukee ofrece refugio de emergencia, vivienda transicional y servicios de apoyo para familias y adultos solteros sin hogar en Milwaukee incluidos adultos con antecedentes penales que reconstruyen vivienda estable después de la encarcelación.",
    address="742 North James Lovell Street", city="Milwaukee", phone="414-671-6111", email="",
    website="https://www.hopehousemke.org",
    eligibility="Families and adults experiencing homelessness in Milwaukee; justice-involved participants may qualify for transitional programs.",
    eligibility_es="Familias y adultos sin hogar en Milwaukee; participantes con antecedentes penales pueden calificar para programas transicionales.",
    notes="Call 414-671-6111 for intake; coordinated entry partner in Milwaukee Continuum of Care.",
    notes_es="Llame al 414-671-6111 para admisión; aliado de entrada coordinada en el Continuo de Cuidado de Milwaukee.",
    hours="Shelter and intake hours vary; call ahead",
    tags="milwaukee|housing|transitional|families|reentry",
    services="Emergency shelter|Transitional housing|Case management|Benefits navigation|Employment referrals",
    county="Milwaukee", served_counties="Milwaukee", coverage="single",
    _source="https://www.hopehousemke.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Community Advocates — Milwaukee",
    category="basic-needs", region="Milwaukee / Milwaukee County",
    description="Community Advocates operates Milwaukee's central access point for homelessness prevention, emergency rental assistance, and basic-needs navigation for low-income Milwaukee County households including returning citizens establishing stable tenancy after release. Housing specialists coordinate with ACCESS Wisconsin benefits, Job Center of Wisconsin, and Wisconsin Community Services for whole-person reentry support.",
    description_es="Community Advocates opera el punto central de acceso de Milwaukee para prevención de falta de vivienda, asistencia de alquiler de emergencia y navegación de necesidades básicas para hogares de bajos ingresos del condado Milwaukee incluidos ciudadanos que regresan que establecen arrendamiento estable después de la liberación.",
    address="728 North James Lovell Street", city="Milwaukee", phone="414-933-8585", email="",
    website="https://communityadvocates.net",
    eligibility="Low-income Milwaukee County residents facing housing instability or basic-needs crises; justice-involved adults may qualify for emergency assistance.",
    eligibility_es="Residentes de bajos ingresos del condado Milwaukee que enfrentan inestabilidad de vivienda o crisis de necesidades básicas; adultos con antecedentes penales pueden calificar para asistencia de emergencia.",
    notes="Call 414-933-8585 for housing and basic-needs intake; not a walk-in men's emergency shelter.",
    notes_es="Llame al 414-933-8585 para admisión de vivienda y necesidades básicas; no es refugio de emergencia para hombres sin cita.",
    hours="Monday–Friday business hours",
    tags="milwaukee|basic-needs|rental-assistance|homelessness|reentry",
    services="Emergency rental assistance|Homelessness prevention|Basic-needs navigation|Benefits referrals|Coordinated entry",
    county="Milwaukee", served_counties="Milwaukee", coverage="single",
    _source="https://communityadvocates.net", _source_type="nonprofit", _confidence="high",
)
add(
    name="Sixteenth Street Community Health Centers — Milwaukee",
    category="healthcare", region="Milwaukee / Milwaukee County",
    description="Sixteenth Street Community Health Centers operate Federally Qualified Health Center clinics across Milwaukee providing primary care, behavioral health, dental services, and sliding-fee care for uninsured and BadgerCare Plus patients including justice-involved adults reestablishing healthcare after release from Milwaukee County Jail or WDOC custody.",
    description_es="Sixteenth Street Community Health Centers opera clínicas FQHC en Milwaukee que ofrecen atención primaria, salud conductual, servicios dentales y atención con tarifa móvil para pacientes sin seguro y BadgerCare Plus incluidos adultos con antecedentes penales.",
    address="1032 South Cesar E. Chavez Drive", city="Milwaukee", phone="414-672-1353", email="",
    website="https://sschc.org",
    eligibility="Milwaukee residents of all ages; sliding scale with proof of income; BadgerCare Plus and Medicare accepted.",
    eligibility_es="Residentes de Milwaukee de todas las edades; escala móvil con prueba de ingresos; se aceptan BadgerCare Plus y Medicare.",
    notes="Call 414-672-1353 for nearest clinic; multiple Milwaukee locations; same-day sick visits at select sites.",
    notes_es="Llame al 414-672-1353 para la clínica más cercana; múltiples ubicaciones en Milwaukee.",
    hours="Monday–Friday clinic hours; varies by location",
    tags="milwaukee|healthcare|FQHC|primary-care|reentry",
    services="Primary care|Behavioral health|Dental care|Sliding-fee services|Pharmacy assistance",
    county="Milwaukee", served_counties="Milwaukee", coverage="single",
    _source="https://sschc.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="JustDane — Madison Reentry Services",
    category="reentry-organizations", region="Madison / Dane County",
    description="JustDane provides reentry case management, housing navigation, employment support, and family reunification services for justice-involved adults returning to the Madison area from WDOC custody and Dane County Jail. Staff connect participants to Job Center of Wisconsin, Porchlight housing programs, ACCESS Wisconsin benefits, and Dane County Comprehensive Community Services partners.",
    description_es="JustDane ofrece manejo de casos de reinserción, navegación de vivienda, apoyo laboral y servicios de reunificación familiar para adultos con antecedentes penales que regresan al área de Madison de custodia WDOC y la cárcel del condado Dane. El personal conecta participantes con Job Center of Wisconsin, programas de vivienda Porchlight y beneficios ACCESS Wisconsin.",
    address="1202 Williamson Street", city="Madison", phone="608-256-6327", email="",
    website="https://justdane.org",
    eligibility="Justice-involved adults in the Madison and Dane County area; referral from WDOC, courts, or self-referral per program.",
    eligibility_es="Adultos con antecedentes penales en el área de Madison y el condado Dane; referencia de WDOC, tribunales o autorreferencia según el programa.",
    notes="Call 608-256-6327 for program intake; pairs with Porchlight and Wisconsin Community Services.",
    notes_es="Llame al 608-256-6327 para admisión al programa; se vincula con Porchlight y Wisconsin Community Services.",
    hours="Monday–Friday business hours",
    tags="madison|dane|reentry|case-management|housing|employment",
    services="Reentry case management|Housing navigation|Employment support|Family reunification|Benefits navigation",
    county="Dane", served_counties="Dane", coverage="single",
    _source="https://justdane.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Porchlight Inc — Madison",
    category="housing", region="Madison / Dane County",
    description="Porchlight Inc provides emergency shelter, permanent supportive housing, and case management for homeless and low-income adults in the Madison area including justice-involved adults returning from WDOC custody or Dane County Jail. Case managers connect clients to JustDane reentry services, Job Center of Wisconsin, and Dane County DHS benefits offices.",
    description_es="Porchlight Inc ofrece refugio de emergencia, vivienda de apoyo permanente y manejo de casos para adultos sin hogar y de bajos ingresos en el área de Madison incluidos adultos con antecedentes penales que regresan de custodia WDOC o la cárcel del condado Dane.",
    address="303 Lathrop Street", city="Madison", phone="608-257-0915", email="",
    website="https://porchlightinc.org",
    eligibility="Homeless and low-income adults in Dane County; justice-involved clients welcome per program policy.",
    eligibility_es="Adultos sin hogar y de bajos ingresos en el condado Dane; clientes con antecedentes penales bienvenidos según política del programa.",
    notes="Call 608-257-0915 for shelter and housing intake; pairs with JustDane and ACCESS Wisconsin.",
    notes_es="Llame al 608-257-0915 para admisión de refugio y vivienda; se vincula con JustDane y ACCESS Wisconsin.",
    hours="Shelter and intake hours vary; call ahead",
    tags="madison|dane|housing|shelter|supportive-housing|reentry",
    services="Emergency shelter|Permanent supportive housing|Case management|Benefits navigation|Employment referrals",
    county="Dane", served_counties="Dane", coverage="single",
    _source="https://porchlightinc.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="NEW Community Shelter — Green Bay",
    category="housing", region="Green Bay / Brown County",
    description="NEW Community Shelter provides emergency shelter, meals, and case management for homeless adults in the Green Bay and Brown County area including returning citizens recently released from Brown County Jail or WDOC custody. Staff connect guests to Job Center of Wisconsin Green Bay, county DHS benefits, and regional treatment partners for reentry stabilization.",
    description_es="NEW Community Shelter ofrece refugio de emergencia, comidas y manejo de casos para adultos sin hogar en el área de Green Bay y el condado Brown incluidos ciudadanos recién liberados de la cárcel del condado Brown o custodia WDOC.",
    address="301 Mather Street", city="Green Bay", phone="920-437-3766", email="",
    website="https://www.newcommunityshelter.org",
    eligibility="Homeless adults in the Green Bay area; walk-in or call for intake assessment; justice-involved guests welcome.",
    eligibility_es="Adultos sin hogar en el área de Green Bay; ingrese sin cita o llame para evaluación de admisión; huéspedes con antecedentes penales bienvenidos.",
    notes="Call 920-437-3766 for intake; pairs with Feeding America Eastern Wisconsin and Job Center Green Bay.",
    notes_es="Llame al 920-437-3766 para admisión; se vincula con Feeding America Eastern Wisconsin y Job Center Green Bay.",
    hours="Shelter 24/7; intake during business hours",
    tags="green-bay|brown|housing|emergency-shelter|reentry",
    services="Emergency shelter|Meals|Case management|Benefits navigation|Employment referrals",
    county="Brown", served_counties="Brown", coverage="single",
    _source="https://www.newcommunityshelter.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="HALO Inc — Kenosha Homeless Services",
    category="housing", region="Kenosha / Kenosha County",
    description="HALO Inc (Homeless Assistance Leadership Organization) provides emergency shelter, rapid rehousing, and case management for homeless individuals and families in Kenosha County including justice-involved adults returning from WDOC custody or Kenosha County Jail. Case managers connect clients to Job Center of Wisconsin Kenosha, ACCESS Wisconsin benefits, and Racine/Kenosha treatment partners.",
    description_es="HALO Inc (Organización de Liderazgo de Asistencia a Personas sin Hogar) ofrece refugio de emergencia, realojamiento rápido y manejo de casos para personas y familias sin hogar en el condado Kenosha incluidos adultos con antecedentes penales que regresan de custodia WDOC o la cárcel del condado Kenosha.",
    address="8600 Sheridan Road", city="Kenosha", phone="262-658-1717", email="",
    website="https://www.haloinc.org",
    eligibility="Homeless individuals and families in Kenosha County; coordinated entry assessment determines program referral.",
    eligibility_es="Personas y familias sin hogar en el condado Kenosha; la evaluación de entrada coordinada determina la referencia del programa.",
    notes="Call 262-658-1717 for intake; pairs with WDOC Region 2 field office and Job Center Kenosha.",
    notes_es="Llame al 262-658-1717 para admisión; se vincula con oficina de campo WDOC Región 2 y Job Center Kenosha.",
    hours="Shelter and intake hours vary; call ahead",
    tags="kenosha|housing|emergency-shelter|rapid-rehousing|reentry",
    services="Emergency shelter|Rapid rehousing|Case management|Benefits navigation|Employment referrals",
    county="Kenosha", served_counties="Kenosha", coverage="single",
    _source="https://www.haloinc.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Hope Center Racine — Homeless Services",
    category="housing", region="Racine / Racine County",
    description="Hope Center Racine provides daytime services, emergency shelter referrals, meals, and case management for homeless and low-income adults in Racine County including justice-involved adults returning from Racine County Jail or WDOC custody. Staff connect clients to Job Center of Wisconsin Racine, ACCESS Wisconsin benefits, and HALO Kenosha for regional housing coordination.",
    description_es="Hope Center Racine ofrece servicios diurnos, referencias de refugio de emergencia, comidas y manejo de casos para adultos sin hogar y de bajos ingresos en el condado Racine incluidos adultos con antecedentes penales que regresan de la cárcel del condado Racine o custodia WDOC.",
    address="504 Marquette Street", city="Racine", phone="262-636-9279", email="",
    website="https://www.hopecenterracine.org",
    eligibility="Homeless and low-income adults in Racine County; justice-involved clients welcome per intake.",
    eligibility_es="Adultos sin hogar y de bajos ingresos en el condado Racine; clientes con antecedentes penales bienvenidos según admisión.",
    notes="Call 262-636-9279 for services; daytime center and shelter referral partner; pairs with Job Center Racine.",
    notes_es="Llame al 262-636-9279 para servicios; centro diurno y aliado de referencia de refugio; se vincula con Job Center Racine.",
    hours="Daytime center hours; call for current schedule",
    tags="racine|housing|day-center|basic-needs|reentry",
    services="Daytime services|Emergency shelter referrals|Meals|Case management|Employment referrals",
    county="Racine", served_counties="Racine", coverage="single",
    _source="https://www.hopecenterracine.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Job Center of Wisconsin — Milwaukee",
    category="employment", region="Milwaukee / Milwaukee County",
    description="The Milwaukee Job Center connects Milwaukee County job seekers—including justice-involved adults from Milwaukee County Jail and WDOC release—to resume coaching, WIOA training referrals, and fair-chance employer navigation. Staff link returning citizens to Sixteenth Street Community Health Centers, ACCESS Wisconsin benefits, and Wisconsin Community Services reentry partners.",
    description_es="El Job Center de Milwaukee conecta buscadores de empleo del condado Milwaukee—incluidos adultos con antecedentes penales de la cárcel del condado Milwaukee y liberación WDOC—con coaching de currículum, referencias WIOA y navegación de empleo de segunda oportunidad.",
    address="2342 North 27th Street", city="Milwaukee", phone="414-385-6920", email="",
    website="https://www.wisconsinjobcenter.org",
    eligibility="Open to Milwaukee County job seekers including justice-involved individuals; core Job Center services are free.",
    eligibility_es="Abierto a buscadores de empleo del condado Milwaukee incluidas personas con antecedentes penales; servicios básicos gratuitos.",
    notes="Register at wisconsinjobcenter.org; call 414-385-6920; pairs with Guest House and Community Advocates.",
    notes_es="Regístrese en wisconsinjobcenter.org; llame al 414-385-6920; se vincula con Guest House y Community Advocates.",
    hours="Monday–Friday business hours",
    tags="milwaukee|employment|job-center|WIOA|fair-chance|reentry",
    services="Job search assistance|Resume coaching|WIOA training referrals|Fair-chance employment|Career workshops",
    county="Milwaukee", served_counties="Milwaukee", coverage="single",
    _source="https://www.wisconsinjobcenter.org", _source_type="government", _confidence="high",
)
add(
    name="Job Center of Wisconsin — Madison",
    category="employment", region="Madison / Dane County",
    description="The Madison Job Center connects Dane County job seekers including justice-involved adults to WIOA-funded training, resume assistance, and fair-chance employment navigation. Staff coordinate with JustDane, Porchlight, and Dane County DHS for reentry stabilization.",
    description_es="El Job Center de Madison conecta buscadores de empleo del condado Dane incluidos adultos con antecedentes penales con capacitación WIOA, ayuda con currículum y navegación de empleo de segunda oportunidad.",
    address="1810 Wright Street", city="Madison", phone="608-242-7400", email="",
    website="https://www.wisconsinjobcenter.org",
    eligibility="Open to Dane County job seekers including justice-involved individuals; core services free.",
    eligibility_es="Abierto a buscadores de empleo del condado Dane incluidas personas con antecedentes penales; servicios básicos gratuitos.",
    notes="Register at wisconsinjobcenter.org; call 608-242-7400; pairs with JustDane and Porchlight.",
    notes_es="Regístrese en wisconsinjobcenter.org; llame al 608-242-7400; se vincula con JustDane y Porchlight.",
    hours="Monday–Friday business hours",
    tags="madison|dane|employment|job-center|WIOA|reentry",
    services="Job search assistance|Resume coaching|WIOA referrals|Fair-chance employment|Career coaching",
    county="Dane", served_counties="Dane", coverage="single",
    _source="https://www.wisconsinjobcenter.org", _source_type="government", _confidence="high",
)
add(
    name="Job Center of Wisconsin — Green Bay",
    category="employment", region="Green Bay / Brown County",
    description="The Green Bay Job Center connects Brown County and northeast Wisconsin job seekers including justice-involved adults to WIOA training, resume assistance, and fair-chance employer connections. Staff coordinate with NEW Community Shelter and county DHS offices for reentry stabilization.",
    description_es="El Job Center de Green Bay conecta buscadores de empleo del condado Brown y noreste de Wisconsin incluidos adultos con antecedentes penales con capacitación WIOA y conexiones con empleadores de segunda oportunidad.",
    address="701 Cherry Street", city="Green Bay", phone="920-448-6760", email="",
    website="https://www.wisconsinjobcenter.org",
    eligibility="Open to Brown County and northeast Wisconsin job seekers including justice-involved individuals.",
    eligibility_es="Abierto a buscadores de empleo del condado Brown y noreste de Wisconsin incluidas personas con antecedentes penales.",
    notes="Register at wisconsinjobcenter.org; call 920-448-6760; pairs with NEW Community Shelter and Feeding America Eastern Wisconsin.",
    notes_es="Regístrese en wisconsinjobcenter.org; llame al 920-448-6760; se vincula con NEW Community Shelter.",
    hours="Monday–Friday business hours",
    tags="green-bay|brown|employment|job-center|WIOA|reentry",
    services="Job search assistance|Resume coaching|WIOA referrals|Fair-chance employment|Career workshops",
    county="Brown", served_counties="Brown|Outagamie|Winnebago|Kewaunee|Door", coverage="multi",
    _source="https://www.wisconsinjobcenter.org", _source_type="government", _confidence="high",
)

# --- County benefits + expansion modules ---
from county_benefits_registry import register_county_benefits_wisconsin

_existing_fa = {
    e["county"]
    for e in ENTRIES
    if e["category"] == "financial-assistance" and e.get("county")
}
register_county_benefits_wisconsin(add, _existing_fa)

from wisconsin_phase4_expansion import register_phase4
register_phase4(add)

from wisconsin_category_fill import register_category_fill
register_category_fill(add)

from wisconsin_mechanical_depth import register_mechanical_depth
register_mechanical_depth(add)

from wisconsin_gap_fill import register_gap_fill
register_gap_fill(add)


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
