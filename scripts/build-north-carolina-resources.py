#!/usr/bin/env python3
"""Generate north-carolina-resources.csv and north-carolina-research-log.csv.

RESOURCES_UUID_PREFIX comment d9000001
"""
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES_PATH = ROOT / "data" / "north-carolina-resources.csv"
LOG_PATH = ROOT / "data" / "north-carolina-research-log.csv"
DATE = "2026-06-25"

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
    name="NCDAC — Reentry Services",
    category="state-agency", region="Statewide",
    description="The North Carolina Department of Adult Correction coordinates statewide reentry planning, pre-release programming, and community partner connections for individuals preparing to leave state custody or under community supervision. Staff work with local DSS offices, NC Works career centers, and treatment providers on housing, employment, and benefits navigation before and after release. This office provides planning and referrals—not a walk-in crisis line or emergency cash provider.",
    description_es="El Departamento de Corrección para Adultos de Carolina del Norte coordina planificación estatal de reinserción, programación previa a la liberación y conexiones con aliados comunitarios para personas que preparan salir de custodia estatal o bajo supervisión comunitaria. El personal trabaja con oficinas DSS locales, centros NC Works y proveedores de tratamiento sobre vivienda, empleo y beneficios. Esta oficina ofrece planificación y referencias, no es una línea de crisis ni proveedor de efectivo de emergencia.",
    address="2020 Yonkers Road", city="Raleigh", phone="919-716-3200", email="",
    website="https://www.dac.nc.gov/reentry-services",
    eligibility="Individuals in NCDAC custody or recently released seeking state reentry coordination; community partners seeking NCDAC engagement.",
    eligibility_es="Personas en custodia de NCDAC o recién liberadas que buscan coordinación estatal de reinserción; aliados comunitarios.",
    notes="Visit dac.nc.gov/reentry-services; coordinate through facility reentry staff and assigned community supervision officer after release.",
    notes_es="Visite dac.nc.gov/reentry-services; coordine a través del personal de reinserción de la instalación y el oficial de supervisión asignado.",
    hours="State office Monday–Friday business hours",
    tags="statewide|reentry|NCDAC|DOC|pre-release|parole",
    services="Pre-release planning|Transitional programming coordination|Community partner referrals|Reentry resource navigation|Supervision linkage",
    county="Wake", served_counties="", coverage="statewide",
    _source="https://www.dac.nc.gov/reentry-services", _source_type="government", _confidence="high",
)
add(
    name="ePASS — North Carolina Benefits Portal",
    category="financial-assistance", region="Statewide",
    description="ePASS is North Carolina's official online portal for applying for and managing Medicaid, NC Health Choice, SNAP food assistance, Work First cash benefits, child care subsidies, and energy assistance through county Department of Social Services offices. Justice-involved North Carolinians can apply for health coverage and food support after release; county DSS staff assist with verification and redetermination at all 100 county offices.",
    description_es="ePASS es el portal en línea oficial de Carolina del Norte para solicitar y administrar Medicaid, NC Health Choice, SNAP, beneficios en efectivo Work First, subsidios de cuidado infantil y asistencia energética a través de oficinas DSS del condado. Personas en reinserción pueden solicitar cobertura de salud y apoyo alimentario después de la liberación; el personal DSS del condado ayuda con verificación.",
    address="", city="", phone="1-866-719-0141", email="", website="https://epass.nc.gov",
    eligibility="North Carolina residents meeting income and program requirements for Medicaid, SNAP, or cash assistance; criminal record generally not a barrier.",
    eligibility_es="Residentes de Carolina del Norte que cumplan requisitos de ingresos para Medicaid, SNAP o asistencia en efectivo; los antecedentes penales generalmente no son barrera.",
    notes="Apply online at epass.nc.gov; call 1-866-719-0141 for NC FAST help; visit your county DSS office for in-person assistance.",
    notes_es="Solicite en epass.nc.gov; llame al 1-866-719-0141; visite su oficina DSS del condado para asistencia presencial.",
    hours="Online 24/7; county DSS office hours vary",
    tags="statewide|benefits|SNAP|Medicaid|ePASS|online|reentry",
    services="Medicaid application|SNAP enrollment|Work First cash assistance|NC Health Choice enrollment|Benefits account management",
    county="", served_counties="", coverage="statewide",
    _source="https://epass.nc.gov", _source_type="government", _confidence="high",
)
add(
    name="NC FAST — Benefits Application Support",
    category="financial-assistance", region="Statewide",
    description="NC FAST (North Carolina Families Accessing Services through Technology) is the statewide benefits processing system used by all 100 county DSS offices for Medicaid, SNAP, Work First, and child care assistance applications. Returning citizens can apply online through ePASS or in person at their county DSS office with help establishing food and health benefits after release from NCDAC custody or county jails.",
    description_es="NC FAST es el sistema estatal de procesamiento de beneficios usado por las 100 oficinas DSS del condado para solicitudes de Medicaid, SNAP, Work First y asistencia de cuidado infantil. Los ciudadanos que regresan pueden solicitar en línea a través de ePASS o en persona en su oficina DSS del condado con ayuda para establecer beneficios alimentarios y de salud después de la liberación.",
    address="2001 Mail Service Center", city="Raleigh", phone="1-866-719-0141", email="",
    website="https://www.ncdhhs.gov/divisions/social-services/nc-fast",
    eligibility="North Carolina residents meeting income and household-size requirements; criminal record generally not a barrier to SNAP and Medicaid.",
    eligibility_es="Residentes de Carolina del Norte que cumplan requisitos de ingresos y tamaño del hogar; los antecedentes penales generalmente no son barrera para SNAP y Medicaid.",
    notes="Apply at epass.nc.gov or visit your county DSS office; call 1-866-719-0141; bring ID and release documents.",
    notes_es="Solicite en epass.nc.gov o visite su oficina DSS del condado; llame al 1-866-719-0141; traiga identificación y documentos de liberación.",
    hours="County DSS offices typically Monday–Friday business hours",
    tags="statewide|benefits|SNAP|Medicaid|NC-FAST|reentry",
    services="SNAP enrollment|Medicaid application|Work First cash assistance|County DSS referrals|Document verification",
    county="Wake", served_counties="", coverage="statewide",
    _source="https://www.ncdhhs.gov/divisions/social-services/nc-fast", _source_type="government", _confidence="high",
)
add(
    name="NC 211",
    category="state-agency", region="Statewide",
    description="NC 211 is a free statewide information and referral service connecting residents to health and human services including housing, food, utilities, employment, and crisis support across all 100 counties. United Way-supported navigators help callers find local programs by need and ZIP code through nc211.org and the 211 phone line. NC 211 is a referral service—not a direct-service provider.",
    description_es="NC 211 es un servicio gratuito de información y referencia estatal que conecta a residentes con servicios de salud y humanos incluyendo vivienda, alimentos, servicios públicos, empleo y apoyo en crisis en los 100 condados. Navegadores apoyados por United Way ayudan a encontrar programas locales por necesidad y código postal. Es un servicio de referencia, no un proveedor directo.",
    address="", city="", phone="211", email="", website="https://nc211.org",
    eligibility="Open to all North Carolina residents; no criminal-record restrictions stated.",
    eligibility_es="Abierto a todos los residentes de Carolina del Norte; sin restricciones de antecedentes indicadas.",
    notes="Dial 211 from any North Carolina phone; search resources online at nc211.org; text your ZIP code to 898-211.",
    notes_es="Marque 211 desde cualquier teléfono de Carolina del Norte; busque recursos en nc211.org; envíe su código postal al 898-211.",
    hours="Available during published service hours; check nc211.org",
    tags="statewide|hotline|211|referral-only|basic-needs",
    services="Information and referral|Housing resource navigation|Benefits referrals|Crisis resource connections",
    county="", served_counties="", coverage="statewide",
    _source="https://nc211.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Legal Aid of North Carolina — Statewide Helpline",
    category="legal-aid", region="Statewide",
    description="Legal Aid of North Carolina is the state's primary nonprofit civil legal aid provider serving low-income North Carolinians with housing, public benefits, family law, and criminal record relief assistance including expungement under North Carolina statutes. Centralized intake at 1-866-219-5262 routes callers to regional offices—not criminal defense representation.",
    description_es="Legal Aid of North Carolina es el principal proveedor sin fines de lucro de asistencia legal civil del estado que sirve a carolinenses de bajos ingresos con vivienda, beneficios públicos, derecho familiar y alivio de antecedentes penales incluida expungación. La admisión centralizada al 1-866-219-5262 enruta a oficinas regionales, no defensa penal.",
    address="224 S. Dawson Street", city="Raleigh", phone="1-866-219-5262", email="",
    website="https://www.legalaidnc.org",
    eligibility="Low-income North Carolina residents with non-criminal legal problems; LSC income limits apply; offense-type restrictions may apply for record relief.",
    eligibility_es="Residentes de Carolina del Norte de bajos ingresos con problemas legales no penales; aplican límites de ingresos LSC; pueden aplicar restricciones por tipo de delito para alivio de antecedentes.",
    notes="Apply online at legalaidnc.org or call 1-866-219-5262; regional offices serve specific counties listed on the website.",
    notes_es="Solicite en legalaidnc.org o llame al 1-866-219-5262; las oficinas regionales sirven condados específicos listados en el sitio web.",
    hours="Intake Monday–Friday business hours; online application 24/7",
    tags="statewide|legal-aid|low-income|expungement|hotline",
    services="Civil legal representation|Expungement assistance|Housing legal aid|Benefits advocacy|Regional office referrals",
    county="Wake", served_counties="", coverage="statewide",
    _source="https://www.legalaidnc.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="NCWorks — Statewide Workforce System",
    category="employment", region="Statewide",
    description="NCWorks is North Carolina's statewide workforce system connecting job seekers—including justice-involved North Carolinians—to NCWorks Career Centers, career coaching, unemployment services, and WIOA training referrals through regional workforce boards covering all 100 counties. Fair-chance employment partners and NC Second Chance initiatives coordinate through NCWorks offices for returning citizens seeking sustainable employment.",
    description_es="NCWorks es el sistema estatal de fuerza laboral de Carolina del Norte que conecta a buscadores de empleo—incluidos carolinenses con antecedentes penales—a Centros de Carrera NCWorks, coaching de carrera, servicios de desempleo y referencias de capacitación WIOA a través de juntas regionales en los 100 condados. Las iniciativas de empleo de segunda oportunidad se coordinan a través de oficinas NCWorks.",
    address="313 Chapanoke Road", city="Raleigh", phone="1-888-622-4473", email="",
    website="https://www.ncworks.gov",
    eligibility="Open to North Carolina job seekers including justice-involved individuals; core career center services are free.",
    eligibility_es="Abierto a buscadores de empleo de Carolina del Norte incluidas personas con antecedentes penales; servicios básicos del centro de carrera son gratuitos.",
    notes="Find your nearest NCWorks Career Center at ncworks.gov/offices; register at ncworks.gov for job search tools.",
    notes_es="Encuentre su Centro de Carrera NCWorks más cercano en ncworks.gov/offices; regístrese en ncworks.gov.",
    hours="Career centers Monday–Friday business hours",
    tags="statewide|employment|NCWorks|WIOA|fair-chance|reentry",
    services="Job search assistance|Career coaching|WIOA training referrals|Unemployment services|Fair-chance employment navigation",
    county="Wake", served_counties="", coverage="statewide",
    _source="https://www.ncworks.gov", _source_type="government", _confidence="high",
)
add(
    name="NC Division of Vocational Rehabilitation Services (DVRS)",
    category="employment", region="Statewide",
    description="The North Carolina Division of Vocational Rehabilitation Services helps North Carolinians with disabilities—including justice-involved individuals with qualifying disabilities—prepare for, obtain, and maintain employment through counseling, training, job placement, and employer partnerships at offices statewide. DVRS coordinates with NCWorks and NCDAC reentry programs for disability employment supports after release.",
    description_es="La División de Servicios de Rehabilitación Vocacional de Carolina del Norte ayuda a carolinenses con discapacidades—incluidas personas con antecedentes penales con discapacidades calificadas—a prepararse, obtener y mantener empleo a través de consejería, capacitación, colocación laboral y alianzas con empleadores. DVRS coordina con NCWorks y programas de reinserción de NCDAC.",
    address="2806 Mail Service Center", city="Raleigh", phone="1-800-689-9090", email="",
    website="https://www.ncdhhs.gov/divisions/dvrs",
    eligibility="North Carolina residents with physical or mental disabilities that create employment barriers; eligibility determined through DVRS assessment.",
    eligibility_es="Residentes de Carolina del Norte con discapacidades físicas o mentales que crean barreras laborales; elegibilidad determinada por evaluación DVRS.",
    notes="Apply at ncdhhs.gov/dvrs or call 1-800-689-9090; offices listed at ncdhhs.gov/dvrs/contact-us.",
    notes_es="Solicite en ncdhhs.gov/dvrs o llame al 1-800-689-9090; oficinas en ncdhhs.gov/dvrs/contact-us.",
    hours="State and regional offices Monday–Friday business hours",
    tags="statewide|employment|DVRS|disability|reentry|WIOA",
    services="Vocational counseling|Job placement|Skills training|Employer partnerships|Disability employment supports",
    county="Wake", served_counties="", coverage="statewide",
    _source="https://www.ncdhhs.gov/divisions/dvrs", _source_type="government", _confidence="high",
)
add(
    name="NC Crisis Solutions — Behavioral Health Crisis",
    category="healthcare", region="Statewide",
    description="NC Crisis Solutions is the North Carolina Department of Health and Human Services initiative connecting residents to behavioral health crisis services including mobile crisis teams, facility-based crisis centers, and 988 Suicide and Crisis Lifeline support statewide. Justice-involved individuals experiencing mental health or substance use emergencies can access free crisis response through local managed care organizations—not reentry housing or benefits intake.",
    description_es="NC Crisis Solutions es la iniciativa del Departamento de Salud y Servicios Humanos de Carolina del Norte que conecta a residentes con servicios de crisis de salud conductual incluyendo equipos de crisis móviles, centros de crisis y apoyo de la Línea 988 en todo el estado. Personas con antecedentes penales en emergencias de salud mental o uso de sustancias pueden acceder a respuesta de crisis gratuita.",
    address="", city="", phone="988", email="", website="https://www.ncdhhs.gov/about/department-initiatives/nc-crisis-solutions",
    eligibility="Open to anyone in North Carolina experiencing a mental health, substance use, or developmental disability crisis.",
    eligibility_es="Abierto a cualquier persona en Carolina del Norte en crisis de salud mental, uso de sustancias o discapacidad del desarrollo.",
    notes="Call or text 988; contact your local LME-MCO for mobile crisis; visit ncdhhs.gov NC Crisis Solutions for county resources.",
    notes_es="Llame o envíe texto al 988; contacte su LME-MCO local para crisis móvil; visite ncdhhs.gov NC Crisis Solutions.",
    hours="Available 24/7 via 988",
    tags="statewide|hotline|crisis|mental-health|988|NC-Crisis-Solutions",
    services="Crisis counseling|Mental health referrals|Mobile crisis team dispatch|Substance use crisis support",
    county="", served_counties="", coverage="statewide",
    _source="https://www.ncdhhs.gov/about/department-initiatives/nc-crisis-solutions", _source_type="government", _confidence="high",
)
add(
    name="988 Suicide & Crisis Lifeline — North Carolina",
    category="healthcare", region="Statewide",
    description="Free confidential 24/7 crisis support for people experiencing mental health emergencies, suicidal thoughts, or substance use crises in North Carolina. Trained specialists provide immediate support and can connect callers to local mobile crisis teams through NC Crisis Solutions partners. Available to anyone—not reentry-specific but essential for justice-involved individuals in crisis.",
    description_es="Apoyo gratuito y confidencial 24/7 para emergencias de salud mental, pensamientos suicidas o crisis por uso de sustancias en Carolina del Norte. Especialistas capacitados ofrecen apoyo inmediato y conexión a equipos de crisis móviles a través de aliados de NC Crisis Solutions. Disponible para cualquier persona, esencial para personas con antecedentes penales en crisis.",
    address="", city="", phone="988", email="", website="https://988lifeline.org",
    eligibility="Open to anyone in North Carolina experiencing a mental health or suicide crisis; no eligibility restrictions.",
    eligibility_es="Abierto a cualquier persona en Carolina del Norte en crisis de salud mental o suicidio; sin restricciones.",
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
    description="Free confidential 24/7 treatment referral and information service for individuals and families facing mental health or substance use disorders. Provides referrals to local treatment facilities and community organizations in North Carolina and nationwide. Spanish-language support available through trained specialists for justice-involved individuals seeking SUD or mental health treatment after release.",
    description_es="Servicio gratuito y confidencial 24/7 de referencia e información para personas y familias con trastornos de salud mental o uso de sustancias. Proporciona referencias a centros de tratamiento locales en Carolina del Norte y a nivel nacional. Soporte en español disponible para personas con antecedentes penales que buscan tratamiento después de la liberación.",
    address="", city="", phone="800-662-4357", email="", website="https://www.samhsa.gov/find-help/national-helpline",
    eligibility="Open to anyone in the United States seeking substance use or mental health treatment information and referrals.",
    eligibility_es="Abierto a cualquier persona en Estados Unidos que busque información y referencias de tratamiento.",
    notes="TTY 800-487-4889; also use FindTreatment.gov to search North Carolina providers online.",
    notes_es="TTY 800-487-4889; también use FindTreatment.gov para buscar proveedores en Carolina del Norte.",
    hours="Available 24/7",
    tags="statewide|hotline|substance-use|treatment-referral|national",
    services="Treatment referrals|Substance use information|Mental health resource navigation",
    county="", served_counties="", coverage="statewide",
    _source="https://www.samhsa.gov/find-help/national-helpline", _source_type="government", _confidence="high",
)
add(
    name="FindTreatment.gov — North Carolina Provider Search",
    category="substance-use-treatment", region="Statewide",
    description="SAMHSA's online treatment locator helping North Carolina residents find substance use and mental health treatment providers by location, service type, and payment options including Medicaid. Justice-involved individuals can search outpatient, residential, and MAT providers before or after release from NCDAC custody or county jails across all 100 counties.",
    description_es="Localizador en línea de SAMHSA que ayuda a residentes de Carolina del Norte a encontrar proveedores de tratamiento de uso de sustancias y salud mental por ubicación, tipo de servicio y opciones de pago incluido Medicaid. Personas con antecedentes penales pueden buscar proveedores ambulatorios, residenciales y TMO antes o después de la liberación.",
    address="", city="", phone="", email="", website="https://findtreatment.gov",
    eligibility="Open to anyone searching for treatment; provider admission rules vary.",
    eligibility_es="Abierto a cualquier persona que busque tratamiento; las reglas de admisión varían según el proveedor.",
    notes="Search findtreatment.gov by North Carolina county or city; filter for MAT, outpatient, or residential services.",
    notes_es="Busque en findtreatment.gov por condado o ciudad de Carolina del Norte; filtre por TMO, ambulatorio o residencial.",
    hours="Website 24/7",
    tags="statewide|substance-use|online|MAT|treatment-locator",
    services="Treatment provider search|MAT locator|Outpatient program finder|Residential program finder",
    county="", served_counties="", coverage="statewide",
    _source="https://findtreatment.gov", _source_type="government", _confidence="high",
)
add(
    name="NC Division of Motor Vehicles — ID Services",
    category="id-documentation", region="Statewide",
    description="The North Carolina Division of Motor Vehicles issues state ID cards and driver's licenses required for employment, housing, and benefits enrollment after release. Returning citizens can apply for a North Carolina ID at driver license offices statewide with proof of identity and residency. Not a vital records office—contact county Register of Deeds for birth certificates.",
    description_es="La División de Vehículos Motorizados de Carolina del Norte emite tarjetas de identificación estatal y licencias de conducir necesarias para empleo, vivienda e inscripción en beneficios después de la liberación. Los ciudadanos que regresan pueden solicitar una identificación en oficinas de licencias con prueba de identidad y residencia. No es oficina de registros vitales.",
    address="1100 New Bern Avenue", city="Raleigh", phone="919-715-7000", email="",
    website="https://www.ncdot.gov/dmv",
    eligibility="North Carolina residents with required identity and residency documentation; fees apply for ID cards and licenses.",
    eligibility_es="Residentes de Carolina del Norte con documentación requerida de identidad y residencia; aplican tarifas para tarjetas de identificación.",
    notes="Find driver license offices at ncdot.gov/dmv/offices; bring certified birth certificate or passport plus proof of North Carolina residency.",
    notes_es="Encuentre oficinas en ncdot.gov/dmv/offices; traiga certificado de nacimiento o pasaporte más prueba de residencia.",
    hours="Driver license office hours vary; check ncdot.gov/dmv",
    tags="statewide|id-documentation|DMV|drivers-license|reentry",
    services="State ID card issuance|Driver's license services|ID renewal|Driver license office locator",
    county="Wake", served_counties="", coverage="statewide",
    _source="https://www.ncdot.gov/dmv", _source_type="government", _confidence="high",
)
add(
    name="NC Vital Records — Birth & Death Certificates",
    category="id-documentation", region="Statewide",
    description="The North Carolina Vital Records office processes requests for birth and death certificates needed for state ID, Medicaid, and employment applications after release. Returning citizens can order certified copies online, by mail, or through county Register of Deeds offices with acceptable identification. Processing times vary—order early in reentry planning.",
    description_es="La oficina de Registros Vitales de Carolina del Norte procesa solicitudes de certificados de nacimiento y defunción necesarios para identificación estatal, Medicaid y solicitudes de empleo después de la liberación. Los ciudadanos que regresan pueden ordenar copias certificadas en línea, por correo o a través de oficinas del Registro de Actos del condado.",
    address="225 N. McDowell Street", city="Raleigh", phone="919-733-3000", email="",
    website="https://www.ncdhhs.gov/divisions/public-health/vital-records",
    eligibility="Individuals with legal right to request the record; acceptable ID required; fees apply per certificate.",
    eligibility_es="Personas con derecho legal a solicitar el registro; se requiere identificación aceptable; aplican tarifas por certificado.",
    notes="Order online at vitalrecords.nc.gov or call 919-733-3000; county Register of Deeds offices also issue birth certificates.",
    notes_es="Ordene en vitalrecords.nc.gov o llame al 919-733-3000; las oficinas del Registro de Actos del condado también emiten certificados.",
    hours="Monday–Friday, 8:00 a.m.–5:00 p.m. ET",
    tags="statewide|id-documentation|vital-records|birth-certificate",
    services="Birth certificate orders|Death certificate orders|Online vital records requests|Certified copy processing",
    county="Wake", served_counties="", coverage="statewide",
    _source="https://www.ncdhhs.gov/divisions/public-health/vital-records", _source_type="government", _confidence="high",
)
add(
    name="NC Department of Military and Veterans Affairs — Statewide",
    category="veterans", region="Statewide",
    description="The North Carolina Department of Military and Veterans Affairs helps justice-involved veterans access VA benefits, disability claims, employment programs, and housing resources through county veterans service offices across all 100 counties. Veterans released from incarceration may qualify for VA health care, vocational rehabilitation, and veterans treatment court supports. Benefits navigation and advocacy—not emergency shelter.",
    description_es="El Departamento de Asuntos Militares y de Veteranos de Carolina del Norte ayuda a veteranos con antecedentes penales a acceder a beneficios del VA, reclamaciones de discapacidad, programas de empleo y recursos de vivienda a través de oficinas de servicios para veteranos del condado en los 100 condados. Los veteranos liberados pueden calificar para atención médica del VA y tribunales de tratamiento para veteranos.",
    address="1315 Mail Service Center", city="Raleigh", phone="919-733-3851", email="",
    website="https://www.ncdva.nc.gov",
    eligibility="Honorably discharged or qualifying North Carolina veterans and their dependents; service documentation required.",
    eligibility_es="Veteranos de Carolina del Norte con baja honorable o calificados y sus dependientes; se requiere documentación de servicio.",
    notes="Find your county veterans service office at ncdva.nc.gov; free benefits claims assistance at all 100 county offices.",
    notes_es="Encuentre su oficina de servicios para veteranos del condado en ncdva.nc.gov; asistencia gratuita con reclamaciones.",
    hours="County offices Monday–Friday business hours",
    tags="statewide|veterans|VA-benefits|reentry|justice-involved-veterans",
    services="VA benefits claims assistance|Disability claims navigation|Employment program referrals|Veterans treatment court support",
    county="Wake", served_counties="", coverage="statewide",
    _source="https://www.ncdva.nc.gov", _source_type="government", _confidence="high",
)
add(
    name="NC Second Chance Alliance",
    category="reentry-organizations", region="Statewide",
    description="The NC Second Chance Alliance is a statewide coalition of service providers, faith communities, businesses, and community leaders advocating for fair-chance policies and connecting justice-involved North Carolinians to housing, employment, and legal resources. The alliance coordinates local reentry networks and policy advocacy—not direct emergency services at the state office.",
    description_es="La Alianza de Segunda Oportunidad de NC es una coalición estatal de proveedores de servicios, comunidades de fe, empresas y líderes comunitarios que abogan por políticas de segunda oportunidad y conectan a carolinenses con antecedentes penales con recursos de vivienda, empleo y legales. La alianza coordina redes locales de reinserción, no servicios de emergencia directos.",
    address="224 S. Dawson Street", city="Raleigh", phone="", email="info@ncsecondchance.org",
    website="https://ncsecondchance.org",
    eligibility="Justice-involved North Carolina residents and community partners seeking reentry coalition connections and fair-chance policy information.",
    eligibility_es="Residentes de Carolina del Norte con antecedentes penales y aliados comunitarios que buscan conexiones con coaliciones de reinserción.",
    notes="Visit ncsecondchance.org for member organizations and local reentry partner directory; contact info@ncsecondchance.org for coalition information.",
    notes_es="Visite ncsecondchance.org para organizaciones miembros y directorio de aliados locales; contacte info@ncsecondchance.org.",
    hours="Contact for current hours",
    tags="statewide|reentry|coalition|fair-chance|referral-only",
    services="Coalition coordination|Fair-chance policy advocacy|Local reentry partner directory|Community networking",
    county="Wake", served_counties="", coverage="statewide",
    _source="https://ncsecondchance.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="NC Justice Center — Fair Chance Employment Project",
    category="reentry-organizations", region="Statewide",
    description="The North Carolina Justice Center Fair Chance Employment Project advocates for policies and practices that expand job opportunities for people with criminal records and connects returning citizens to legal resources, benefits navigation, and workforce partners across North Carolina. Staff provide policy education and referral navigation—not direct cash assistance or emergency housing.",
    description_es="El Proyecto de Empleo de Segunda Oportunidad del Centro de Justicia de Carolina del Norte aboga por políticas que expanden oportunidades laborales para personas con antecedentes penales y conecta a quienes regresan con recursos legales, navegación de beneficios y aliados de fuerza laboral. El personal ofrece educación de políticas y referencias, no asistencia en efectivo ni vivienda de emergencia.",
    address="224 S. Dawson Street", city="Raleigh", phone="919-856-2570", email="",
    website="https://www.ncjustice.org",
    eligibility="Justice-involved North Carolina residents and advocates seeking fair-chance employment policy information and legal referrals.",
    eligibility_es="Residentes de Carolina del Norte con antecedentes penales y defensores que buscan información sobre empleo de segunda oportunidad y referencias legales.",
    notes="Visit ncjustice.org for fair-chance resources; connects to Legal Aid of NC and local workforce partners.",
    notes_es="Visite ncjustice.org para recursos de segunda oportunidad; conecta con Legal Aid of NC y aliados de fuerza laboral.",
    hours="Monday–Friday business hours",
    tags="statewide|reentry|fair-chance|policy|referral-only",
    services="Fair-chance policy advocacy|Legal resource referrals|Workforce partner navigation|Benefits education",
    county="Wake", served_counties="", coverage="statewide",
    _source="https://www.ncjustice.org", _source_type="nonprofit", _confidence="high",
)

# --- Phase 2: Major metro anchors ---
add(
    name="Center for Community Transitions — Charlotte",
    category="reentry-organizations", region="Charlotte / Mecklenburg County",
    description="Center for Community Transitions is Charlotte's leading reentry organization providing transitional housing, employment training, life skills, and family reunification services for justice-involved women and men returning to Mecklenburg County after incarceration. CCT operates residential and community-based programs with case management connecting participants to NCWorks, DSS benefits, and local employers. Direct services—not a statewide hotline.",
    description_es="Center for Community Transitions es la principal organización de reinserción de Charlotte que ofrece vivienda transicional, capacitación laboral, habilidades para la vida y reunificación familiar para mujeres y hombres con antecedentes penales que regresan al condado Mecklenburg. CCT opera programas residenciales y comunitarios con manejo de casos conectando participantes con NCWorks, beneficios DSS y empleadores locales.",
    address="801 E. Fourth Street", city="Charlotte", phone="704-375-1722", email="",
    website="https://centerforcommunitytransitions.org",
    eligibility="Justice-involved adults returning to Mecklenburg County; program-specific requirements for residential tracks.",
    eligibility_es="Adultos con antecedentes penales que regresan al condado Mecklenburg; requisitos específicos del programa para programas residenciales.",
    notes="Call 704-375-1722 for intake; programs include Charlotte's only reentry-specific transitional housing for women.",
    notes_es="Llame al 704-375-1722 para admisión; programas incluyen la única vivienda transicional de reinserción para mujeres en Charlotte.",
    hours="Contact for program hours",
    tags="charlotte|mecklenburg|reentry|housing|employment|reentry-organizations",
    services="Transitional housing|Employment training|Life skills|Family reunification|Case management",
    county="Mecklenburg", served_counties="Mecklenburg", coverage="single",
    _source="https://centerforcommunitytransitions.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="StepUp Ministry — Raleigh Reentry",
    category="reentry-organizations", region="Raleigh / Wake County",
    description="StepUp Ministry helps justice-involved and low-income adults in Wake County achieve stable employment and self-sufficiency through job readiness classes, one-on-one coaching, and supportive services including referrals to housing and benefits partners. Multiple Raleigh-area offices serve returning citizens from Wake County Jail and state custody with fair-chance employer connections. Direct coaching services—not emergency shelter.",
    description_es="StepUp Ministry ayuda a adultos con antecedentes penales y de bajos ingresos en el condado Wake a lograr empleo estable y autosuficiencia mediante clases de preparación laboral, coaching individual y servicios de apoyo incluidas referencias a aliados de vivienda y beneficios. Múltiples oficinas en el área de Raleigh sirven a ciudadanos que regresan de la cárcel del condado Wake.",
    address="1012 Oberlin Road", city="Raleigh", phone="919-834-7634", email="",
    website="https://stepupministry.org",
    eligibility="Low-income Wake County adults including justice-involved individuals seeking employment and stability.",
    eligibility_es="Adultos de bajos ingresos del condado Wake incluidas personas con antecedentes penales que buscan empleo y estabilidad.",
    notes="Call 919-834-7634 for enrollment; connects to NCWorks Raleigh and Wake County reentry partners.",
    notes_es="Llame al 919-834-7634 para inscripción; conecta con NCWorks Raleigh y aliados de reinserción del condado Wake.",
    hours="Monday–Friday business hours; class schedules vary",
    tags="raleigh|wake|reentry|employment|job-readiness",
    services="Job readiness classes|One-on-one coaching|Fair-chance employer connections|Housing referrals|Benefits navigation",
    county="Wake", served_counties="Wake", coverage="single",
    _source="https://stepupministry.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="TROSA — Durham",
    category="housing", region="Durham / Durham County",
    description="TROSA is a multi-year residential recovery program in Durham providing free housing, vocational training, counseling, and job placement for people with substance use disorders including justice-involved adults referred from courts, probation, and prisons across North Carolina. Participants live on campus while completing therapeutic programming and workforce development—not a short-term emergency shelter.",
    description_es="TROSA es un programa residencial de recuperación de varios años en Durham que ofrece vivienda gratuita, capacitación vocacional, consejería y colocación laboral para personas con trastornos por uso de sustancias incluidos adultos con antecedentes penales referidos por tribunales, probatoria y prisiones. Los participantes viven en el campus mientras completan programación terapéutica.",
    address="1820 James Street", city="Durham", phone="919-956-8886", email="",
    website="https://www.trosainc.org",
    eligibility="Adults with substance use disorders willing to commit to multi-year residential recovery; justice referrals accepted per program policy.",
    eligibility_es="Adultos con trastornos por uso de sustancias dispuestos a comprometerse con recuperación residencial de varios años; referencias de justicia aceptadas según política.",
    notes="Call 919-956-8886 for admissions; free program including housing, meals, and job training on Durham campus.",
    notes_es="Llame al 919-956-8886 para admisiones; programa gratuito incluyendo vivienda, comidas y capacitación laboral.",
    hours="Residential program; contact admissions for intake",
    tags="durham|housing|recovery|SUD|reentry|vocational-training",
    services="Residential recovery housing|Vocational training|Counseling|Job placement|Substance use treatment",
    county="Durham", served_counties="Durham", coverage="single",
    _source="https://www.trosainc.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Healing Transitions — Raleigh",
    category="housing", region="Raleigh / Wake County",
    description="Healing Transitions is a peer-based recovery community in Raleigh offering non-medical detox, residential recovery housing, and workforce programming for unhoused adults with substance use disorders including returning citizens from Wake County Jail. The campus provides meals, case management, and connections to NCWorks and local employers—not a medical hospital or psychiatric facility.",
    description_es="Healing Transitions es una comunidad de recuperación basada en pares en Raleigh que ofrece desintoxicación no médica, vivienda de recuperación residencial y programación de fuerza laboral para adultos sin hogar con trastornos por uso de sustancias incluidos ciudadanos que regresan de la cárcel del condado Wake. El campus proporciona comidas, manejo de casos y conexiones con NCWorks.",
    address="1251 Goode Street", city="Raleigh", phone="919-838-7654", email="",
    website="https://healing-transitions.org",
    eligibility="Adults with substance use disorders seeking recovery; justice-involved individuals welcome per program policy.",
    eligibility_es="Adultos con trastornos por uso de sustancias que buscan recuperación; personas con antecedentes penales bienvenidas según política.",
    notes="Call 919-838-7654 for intake; 24/7 walk-in detox available; connects to Wake County reentry and employment partners.",
    notes_es="Llame al 919-838-7654 para admisión; desintoxicación sin cita 24/7 disponible; conecta con aliados de reinserción del condado Wake.",
    hours="24/7 walk-in detox; residential program hours vary",
    tags="raleigh|wake|housing|recovery|SUD|peer-support|reentry",
    services="Non-medical detox|Residential recovery housing|Peer support|Workforce programming|Case management",
    county="Wake", served_counties="Wake", coverage="single",
    _source="https://healing-transitions.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Urban Ministries of Wake County — Open Door Clinic",
    category="healthcare", region="Raleigh / Wake County",
    description="Urban Ministries of Wake County operates the Open Door Clinic and crisis assistance programs serving uninsured and low-income Wake County residents including returning citizens needing primary care, prescription assistance, and emergency food support after release. The clinic provides sliding-fee healthcare and connects patients to DSS benefits and NCWorks—not a psychiatric crisis center.",
    description_es="Urban Ministries of Wake County opera la Clínica Open Door y programas de asistencia en crisis sirviendo a residentes del condado Wake sin seguro y de bajos ingresos incluidos ciudadanos que regresan que necesitan atención primaria, asistencia con recetas y apoyo alimentario de emergencia. La clínica ofrece atención médica con tarifa móvil y conecta pacientes con beneficios DSS.",
    address="1390 Capital Boulevard", city="Raleigh", phone="919-836-1642", email="",
    website="https://urbanmin.org",
    eligibility="Uninsured and low-income Wake County residents; justice-involved individuals welcome for clinic and crisis assistance.",
    eligibility_es="Residentes del condado Wake sin seguro y de bajos ingresos; personas con antecedentes penales bienvenidas para clínica y asistencia.",
    notes="Call 919-836-1642 for clinic appointments; crisis assistance available for food and utility needs.",
    notes_es="Llame al 919-836-1642 para citas de clínica; asistencia en crisis disponible para alimentos y servicios públicos.",
    hours="Clinic Monday–Friday; call for crisis assistance hours",
    tags="raleigh|wake|healthcare|clinic|basic-needs|reentry",
    services="Primary care|Prescription assistance|Crisis food assistance|Utility assistance|Benefits referrals",
    county="Wake", served_counties="Wake", coverage="single",
    _source="https://urbanmin.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Good Shepherd Center — Wilmington",
    category="basic-needs", region="Wilmington / New Hanover County",
    description="Good Shepherd Center in Wilmington provides emergency shelter, meals, case management, and reentry resource navigation for unhoused adults in New Hanover County including returning citizens recently released from local jail or state custody. Direct services at the Wilmington campus include day shelter access and connections to coastal North Carolina housing and employment partners—not a statewide hotline.",
    description_es="Good Shepherd Center en Wilmington proporciona refugio de emergencia, comidas, manejo de casos y navegación de recursos de reinserción para adultos sin hogar en el condado New Hanover incluidos ciudadanos que regresan recién liberados de la cárcel local o custodia estatal. Servicios directos incluyen acceso a refugio diurno y conexiones con aliados de vivienda y empleo.",
    address="811 Martin Street", city="Wilmington", phone="910-763-4424", email="",
    website="https://goodshepherdcenter.org",
    eligibility="Unhoused adults in New Hanover County; justice-involved individuals welcome for shelter and navigation services.",
    eligibility_es="Adultos sin hogar en el condado New Hanover; personas con antecedentes penales bienvenidas para refugio y navegación.",
    notes="Call 910-763-4424 for intake; connects to NCWorks Wilmington and New Hanover reentry partners.",
    notes_es="Llame al 910-763-4424 para admisión; conecta con NCWorks Wilmington y aliados de reinserción de New Hanover.",
    hours="Contact for shelter and day services hours",
    tags="wilmington|new-hanover|basic-needs|shelter|reentry|meals",
    services="Emergency shelter|Day shelter|Meals|Case management|Reentry resource navigation",
    county="New Hanover", served_counties="New Hanover", coverage="single",
    _source="https://goodshepherdcenter.org", _source_type="nonprofit", _confidence="high",
)

# --- Phase 3/4: Program-level expansion ---
from north_carolina_phase4_expansion import register_phase4
register_phase4(add)

from north_carolina_rural_depth import register_rural_depth
register_rural_depth(add)

from north_carolina_category_fill import register_category_fill
register_category_fill(add)

from north_carolina_thin_counties import register_thin_counties
register_thin_counties(add)

from north_carolina_tier_a_closure import register_tier_a_closure
register_tier_a_closure(add)

from phase3b_gapfill import register_phase3b_north_carolina
register_phase3b_north_carolina(add, ENTRIES)


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
