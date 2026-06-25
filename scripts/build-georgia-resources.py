#!/usr/bin/env python3
"""Generate georgia-resources.csv and georgia-research-log.csv.

RESOURCES_UUID_PREFIX comment d8000001
"""
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES_PATH = ROOT / "data" / "georgia-resources.csv"
LOG_PATH = ROOT / "data" / "georgia-research-log.csv"
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
    name="Georgia Department of Corrections — Reentry Services",
    category="state-agency", region="Statewide",
    description="The Georgia Department of Corrections Reentry Services unit coordinates statewide pre-release planning, transitional programming, and community partner connections for individuals preparing to leave GDC custody. Staff work with the Department of Community Supervision, local nonprofits, and workforce agencies on housing, employment, and treatment referrals before and after release. This office provides planning and referrals—not a walk-in crisis line or emergency cash provider.",
    description_es="La unidad de Servicios de Reinserción del Departamento de Correcciones de Georgia coordina planificación previa a la liberación, programación de transición y conexiones con aliados comunitarios para personas que preparan salir de custodia de GDC. El personal trabaja con Supervisión Comunitaria, organizaciones locales y agencias de fuerza laboral sobre vivienda, empleo y referencias de tratamiento. Esta oficina ofrece planificación y referencias, no es una línea de crisis ni proveedor de efectivo de emergencia.",
    address="300 Patrol Road", city="Forsyth", phone="478-992-5247", email="",
    website="https://gdc.georgia.gov/reentry-services",
    eligibility="Individuals in GDC custody or recently released seeking state reentry coordination; community partners seeking GDC engagement.",
    eligibility_es="Personas en custodia de GDC o recién liberadas que buscan coordinación estatal de reinserción; aliados comunitarios.",
    notes="Visit gdc.georgia.gov/reentry-services; coordinate through facility reentry staff and assigned DCS officer after release.",
    notes_es="Visite gdc.georgia.gov/reentry-services; coordine a través del personal de reinserción de la instalación y el oficial de DCS asignado.",
    hours="State office Monday–Friday business hours",
    tags="statewide|reentry|GDC|DOC|pre-release|parole",
    services="Pre-release planning|Transitional programming coordination|Community partner referrals|Reentry resource navigation|DCS linkage",
    county="Monroe", served_counties="", coverage="statewide",
    _source="https://gdc.georgia.gov/reentry-services", _source_type="government", _confidence="high",
)
add(
    name="Georgia Board of Pardons and Paroles — Statewide",
    category="probation-parole", region="Statewide",
    description="The Georgia State Board of Pardons and Paroles supervises parole decisions, clemency petitions, and community supervision policy for adults released from Georgia prisons. Field offices across Georgia manage parole reporting, supervision compliance, and referrals to reentry partners for returning citizens. Contact your assigned parole officer or regional office—not emergency housing or crisis services.",
    description_es="La Junta Estatal de Indultos y Libertad Condicional de Georgia supervisa decisiones de libertad condicional, peticiones de clemencia y política de supervisión comunitaria para adultos liberados de prisiones de Georgia. Las oficinas de campo gestionan reportes de libertad condicional, cumplimiento de supervisión y referencias a aliados de reinserción. Contacte a su oficial de libertad condicional asignado, no es vivienda de emergencia.",
    address="2 Martin Luther King Jr. Drive SE", city="Atlanta", phone="404-656-5651", email="",
    website="https://pap.georgia.gov",
    eligibility="Individuals under Georgia parole supervision or seeking clemency or pardon information; victims may register for notification services.",
    eligibility_es="Personas bajo supervisión de libertad condicional de Georgia o que buscan información sobre clemencia o indulto.",
    notes="Find regional field offices at pap.georgia.gov/locations; report to assigned parole officer per supervision conditions.",
    notes_es="Encuentre oficinas regionales en pap.georgia.gov/locations; reporte al oficial de libertad condicional asignado.",
    hours="State office Monday–Friday, 8:00 a.m.–5:00 p.m. ET",
    tags="statewide|parole|probation-parole|BPP|reentry",
    services="Parole supervision coordination|Clemency and pardon information|Field office referrals|Supervision compliance guidance",
    county="Fulton", served_counties="", coverage="statewide",
    _source="https://pap.georgia.gov", _source_type="government", _confidence="high",
)
add(
    name="COMPASS — Georgia Benefits Portal",
    category="financial-assistance", region="Statewide",
    description="COMPASS is Georgia's official statewide online portal for applying for and managing Medicaid, PeachCare for Kids, SNAP food assistance, TANF cash benefits, child care subsidies, and energy assistance through the Department of Human Services Division of Family & Children Services. Justice-involved Georgians can apply for health coverage and food support after release; county DFCS offices assist with verification and redetermination.",
    description_es="COMPASS es el portal en línea oficial de Georgia para solicitar y administrar Medicaid, PeachCare, SNAP, asistencia en efectivo TANF, subsidios de cuidado infantil y asistencia energética a través de DFCS. Personas en reinserción pueden solicitar cobertura de salud y apoyo alimentario después de la liberación; las oficinas DFCS del condado ayudan con verificación.",
    address="", city="", phone="1-877-423-4746", email="", website="https://compass.ga.gov",
    eligibility="Georgia residents meeting income and program requirements for Medicaid, SNAP, or cash assistance; criminal record generally not a barrier.",
    eligibility_es="Residentes de Georgia que cumplan requisitos de ingresos para Medicaid, SNAP o asistencia en efectivo; los antecedentes penales generalmente no son barrera.",
    notes="Apply online at compass.ga.gov; call 1-877-423-4746 for DFCS Customer Contact Center; county offices at dfcs.georgia.gov/locations.",
    notes_es="Solicite en compass.ga.gov; llame al 1-877-423-4746; oficinas del condado en dfcs.georgia.gov/locations.",
    hours="Online 24/7; DFCS office hours vary by county",
    tags="statewide|benefits|SNAP|Medicaid|COMPASS|online|reentry",
    services="Medicaid application|SNAP enrollment|Cash assistance application|PeachCare enrollment|Benefits account management",
    county="", served_counties="", coverage="statewide",
    _source="https://compass.ga.gov", _source_type="government", _confidence="high",
)
add(
    name="DFCS — Family Assistance & Benefits Overview",
    category="financial-assistance", region="Statewide",
    description="The Georgia Division of Family & Children Services administers SNAP, Medicaid, PeachCare, TANF, and child care assistance through county DFCS offices in all 159 counties and the COMPASS online portal. DFCS helps returning citizens establish food and health benefits after release from GDC custody or county jails with local staff assisting document verification.",
    description_es="La División de Servicios Familiares y para Niños de Georgia administra SNAP, Medicaid, PeachCare, TANF y asistencia de cuidado infantil a través de oficinas DFCS en los 159 condados y el portal COMPASS. DFCS ayuda a ciudadanos que regresan a establecer beneficios alimentarios y de salud después de la liberación con personal local que asiste con verificación de documentos.",
    address="2 Peachtree Street NW", city="Atlanta", phone="1-877-423-4746", email="",
    website="https://dfcs.georgia.gov",
    eligibility="Georgia residents meeting income and household-size requirements; criminal record generally not a barrier to SNAP and Medicaid.",
    eligibility_es="Residentes de Georgia que cumplan requisitos de ingresos y tamaño del hogar; los antecedentes penales generalmente no son barrera para SNAP y Medicaid.",
    notes="Apply at compass.ga.gov or visit your county DFCS office; call 1-877-423-4746; bring ID and release documents.",
    notes_es="Solicite en compass.ga.gov o visite su oficina DFCS del condado; llame al 1-877-423-4746; traiga identificación y documentos de liberación.",
    hours="County offices typically Tuesday–Thursday, 9:00 a.m.–4:00 p.m. ET",
    tags="statewide|benefits|SNAP|Medicaid|DFCS|reentry",
    services="SNAP enrollment|Medicaid application|Cash assistance|TANF|County field office referrals",
    county="Fulton", served_counties="", coverage="statewide",
    _source="https://dfcs.georgia.gov", _source_type="government", _confidence="high",
)
add(
    name="211 Georgia",
    category="state-agency", region="Statewide",
    description="211 Georgia is a free statewide information and referral service connecting residents to health and human services including housing, food, utilities, employment, and crisis support across all 159 counties. United Way-supported navigators help callers find local programs by need and ZIP code. 211 Georgia is a referral line—not a direct-service provider.",
    description_es="211 Georgia es un servicio gratuito de información y referencia estatal que conecta a residentes con servicios de salud y humanos incluyendo vivienda, alimentos, servicios públicos, empleo y apoyo en crisis en los 159 condados. Navegadores apoyados por United Way ayudan a encontrar programas locales por necesidad y código postal. Es una línea de referencia, no un proveedor directo.",
    address="", city="", phone="211", email="", website="https://georgia211.org",
    eligibility="Open to all Georgia residents; no criminal-record restrictions stated.",
    eligibility_es="Abierto a todos los residentes de Georgia; sin restricciones de antecedentes indicadas.",
    notes="Dial 211 from any Georgia phone; search resources online at georgia211.org; available for information and referral.",
    notes_es="Marque 211 desde cualquier teléfono de Georgia; busque recursos en georgia211.org.",
    hours="Available during published service hours; check georgia211.org",
    tags="statewide|hotline|211|referral-only|basic-needs",
    services="Information and referral|Housing resource navigation|Benefits referrals|Crisis resource connections",
    county="", served_counties="", coverage="statewide",
    _source="https://georgia211.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Georgia Legal Services Program — Statewide Intake",
    category="legal-aid", region="Statewide",
    description="Georgia Legal Services Program is the state's primary nonprofit civil legal aid provider serving low-income Georgians outside metro Atlanta with housing, public benefits, family law, and criminal record restriction assistance under Georgia's record restriction statutes. Centralized intake routes callers to regional offices—not criminal defense.",
    description_es="Georgia Legal Services Program es el principal proveedor sin fines de lucro de asistencia legal civil del estado que sirve a georgianos de bajos ingresos fuera del área metropolitana de Atlanta con vivienda, beneficios públicos, derecho familiar y restricción de registros penales. La admisión centralizada enruta a oficinas regionales, no defensa penal.",
    address="104 Marietta Street NW", city="Atlanta", phone="1-800-498-9469", email="",
    website="https://www.glsp.org",
    eligibility="Low-income Georgia residents outside Fulton, DeKalb, Clayton, Cobb, and Gwinnett with non-criminal legal problems; LSC income limits apply.",
    eligibility_es="Residentes de Georgia de bajos ingresos fuera de Fulton, DeKalb, Clayton, Cobb y Gwinnett con problemas legales no penales; aplican límites de ingresos LSC.",
    notes="Apply online at glsp.org or call 1-800-498-9469; metro Atlanta residents use Atlanta Legal Aid at atlantalegalaid.org.",
    notes_es="Solicite en glsp.org o llame al 1-800-498-9469; residentes del metro de Atlanta usen Atlanta Legal Aid.",
    hours="Intake Monday–Friday business hours; online application 24/7",
    tags="statewide|legal-aid|low-income|record-restriction|hotline",
    services="Civil legal representation|Record restriction assistance|Housing legal aid|Benefits advocacy|Regional office referrals",
    county="Fulton", served_counties="", coverage="statewide",
    _source="https://www.glsp.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Georgia Department of Labor — WorkSource Georgia",
    category="employment", region="Statewide",
    description="WorkSource Georgia is the statewide workforce system connecting job seekers—including justice-involved Georgians—to American Job Centers, career coaching, unemployment services, and WIOA training referrals through regional career centers covering all 159 counties. Georgia CALLS fair-chance employer partnerships and GVRA disability employment supports are coordinated through WorkSource partners.",
    description_es="WorkSource Georgia es el sistema estatal de fuerza laboral que conecta a buscadores de empleo—incluidos georgianos con antecedentes penales—a Centros de Empleo Americanos, coaching de carrera, servicios de desempleo y referencias de capacitación WIOA a través de centros de carrera regionales en los 159 condados. Las alianzas de empleo justo de Georgia CALLS se coordinan a través de aliados WorkSource.",
    address="148 Andrew Young International Boulevard NE", city="Atlanta", phone="404-232-3000", email="",
    website="https://dol.georgia.gov/worksource-georgia",
    eligibility="Open to Georgia job seekers including justice-involved individuals; core career center services are free.",
    eligibility_es="Abierto a buscadores de empleo de Georgia incluidas personas con antecedentes penales; servicios básicos del centro de carrera son gratuitos.",
    notes="Find your nearest career center at dol.georgia.gov/locations/career-center; register at employgeorgia.com.",
    notes_es="Encuentre su centro de carrera más cercano en dol.georgia.gov/locations/career-center; regístrese en employgeorgia.com.",
    hours="Career centers Monday–Friday business hours",
    tags="statewide|employment|WorkSource|AJC|WIOA|Georgia-CALLS",
    services="Job search assistance|Career coaching|WIOA training referrals|Unemployment services|Fair-chance employment navigation",
    county="Fulton", served_counties="", coverage="statewide",
    _source="https://dol.georgia.gov/worksource-georgia", _source_type="government", _confidence="high",
)
add(
    name="Georgia Vocational Rehabilitation Agency — Statewide",
    category="employment", region="Statewide",
    description="The Georgia Vocational Rehabilitation Agency helps Georgians with disabilities—including justice-involved individuals with qualifying disabilities—prepare for, obtain, and maintain employment through counseling, training, job placement, and employer partnerships. GVRA offices statewide coordinate with WorkSource Georgia and DCS reentry programs. An employment rehabilitation agency—not emergency cash or housing.",
    description_es="La Agencia de Rehabilitación Vocacional de Georgia ayuda a georgianos con discapacidades—incluidas personas con antecedentes penales con discapacidades calificadas—a prepararse, obtener y mantener empleo a través de consejería, capacitación, colocación laboral y alianzas con empleadores. Las oficinas GVRA en todo el estado coordinan con WorkSource Georgia y programas de reinserción de DCS.",
    address="1600 Clarendon Avenue", city="Atlanta", phone="844-367-4872", email="",
    website="https://gvra.georgia.gov",
    eligibility="Georgia residents with physical or mental disabilities that create employment barriers; eligibility determined through GVRA assessment.",
    eligibility_es="Residentes de Georgia con discapacidades físicas o mentales que crean barreras laborales; elegibilidad determinada por evaluación GVRA.",
    notes="Apply at gvra.georgia.gov or call 844-367-4872; offices listed at gvra.georgia.gov/about/locations.",
    notes_es="Solicite en gvra.georgia.gov o llame al 844-367-4872; oficinas en gvra.georgia.gov/about/locations.",
    hours="State and regional offices Monday–Friday business hours",
    tags="statewide|employment|GVRA|disability|reentry|WIOA",
    services="Vocational counseling|Job placement|Skills training|Employer partnerships|Disability employment supports",
    county="Fulton", served_counties="", coverage="statewide",
    _source="https://gvra.georgia.gov", _source_type="government", _confidence="high",
)
add(
    name="Georgia Crisis & Access Line (GCAL)",
    category="healthcare", region="Statewide",
    description="The Georgia Crisis & Access Line provides free confidential 24/7 crisis intervention, mental health support, and substance use crisis referrals for Georgia residents. Trained specialists connect callers to local mobile crisis teams and treatment providers statewide. Essential for justice-involved individuals experiencing behavioral health emergencies—not a reentry housing or benefits line.",
    description_es="La Línea de Crisis y Acceso de Georgia ofrece intervención de crisis gratuita y confidencial 24/7, apoyo de salud mental y referencias de crisis por uso de sustancias para residentes de Georgia. Especialistas capacitados conectan a llamantes con equipos de crisis móviles y proveedores de tratamiento. Esencial para personas con antecedentes penales en emergencias de salud conductual.",
    address="", city="", phone="800-715-4225", email="", website="https://www.mygcal.com",
    eligibility="Open to anyone in Georgia experiencing a mental health, substance use, or developmental disability crisis.",
    eligibility_es="Abierto a cualquier persona en Georgia en crisis de salud mental, uso de sustancias o discapacidad del desarrollo.",
    notes="Call 800-715-4225 or text GA to 741741; also dial 988 for Suicide & Crisis Lifeline; Spanish-language support available.",
    notes_es="Llame al 800-715-4225 o envíe GA al 741741; también marque 988; soporte en español disponible.",
    hours="Available 24/7",
    tags="statewide|hotline|crisis|mental-health|GCAL|988",
    services="Crisis counseling|Mental health referrals|Substance use crisis support|Mobile crisis team dispatch",
    county="", served_counties="", coverage="statewide",
    _source="https://www.mygcal.com", _source_type="government", _confidence="high",
)
add(
    name="988 Suicide & Crisis Lifeline — Georgia",
    category="healthcare", region="Statewide",
    description="Free confidential 24/7 crisis support for people experiencing mental health emergencies, suicidal thoughts, or substance use crises in Georgia. Trained specialists provide immediate support and can connect callers to local mobile crisis teams through GCAL. Available to anyone—not reentry-specific but essential for justice-involved individuals in crisis.",
    description_es="Apoyo gratuito y confidencial 24/7 para emergencias de salud mental, pensamientos suicidas o crisis por uso de sustancias en Georgia. Especialistas capacitados ofrecen apoyo inmediato y conexión a equipos de crisis móviles a través de GCAL. Disponible para cualquier persona, esencial para personas con antecedentes penales en crisis.",
    address="", city="", phone="988", email="", website="https://988lifeline.org",
    eligibility="Open to anyone in Georgia experiencing a mental health or suicide crisis; no eligibility restrictions.",
    eligibility_es="Abierto a cualquier persona en Georgia en crisis de salud mental o suicidio; sin restricciones.",
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
    description="Free confidential 24/7 treatment referral and information service for individuals and families facing mental health or substance use disorders. Provides referrals to local treatment facilities and community organizations in Georgia and nationwide. Spanish-language support available through trained specialists.",
    description_es="Servicio gratuito y confidencial 24/7 de referencia e información para personas y familias con trastornos de salud mental o uso de sustancias. Proporciona referencias a centros de tratamiento locales en Georgia y a nivel nacional. Soporte en español disponible.",
    address="", city="", phone="800-662-4357", email="", website="https://www.samhsa.gov/find-help/national-helpline",
    eligibility="Open to anyone in the United States seeking substance use or mental health treatment information and referrals.",
    eligibility_es="Abierto a cualquier persona en Estados Unidos que busque información y referencias de tratamiento.",
    notes="TTY 800-487-4889; also use FindTreatment.gov to search Georgia providers online.",
    notes_es="TTY 800-487-4889; también use FindTreatment.gov para buscar proveedores en Georgia.",
    hours="Available 24/7",
    tags="statewide|hotline|substance-use|treatment-referral|national",
    services="Treatment referrals|Substance use information|Mental health resource navigation",
    county="", served_counties="", coverage="statewide",
    _source="https://www.samhsa.gov/find-help/national-helpline", _source_type="government", _confidence="high",
)
add(
    name="FindTreatment.gov — Georgia Provider Search",
    category="substance-use-treatment", region="Statewide",
    description="SAMHSA's online treatment locator helping Georgia residents find substance use and mental health treatment providers by location, service type, and payment options including Medicaid. Justice-involved individuals can search outpatient, residential, and MAT providers before or after release from GDC custody or county jails.",
    description_es="Localizador en línea de SAMHSA que ayuda a residentes de Georgia a encontrar proveedores de tratamiento de uso de sustancias y salud mental por ubicación, tipo de servicio y opciones de pago incluido Medicaid. Personas con antecedentes penales pueden buscar proveedores ambulatorios, residenciales y TMO antes o después de la liberación.",
    address="", city="", phone="", email="", website="https://findtreatment.gov",
    eligibility="Open to anyone searching for treatment; provider admission rules vary.",
    eligibility_es="Abierto a cualquier persona que busque tratamiento; las reglas de admisión varían según el proveedor.",
    notes="Search findtreatment.gov by Georgia county or city; filter for MAT, outpatient, or residential services.",
    notes_es="Busque en findtreatment.gov por condado o ciudad de Georgia; filtre por TMO, ambulatorio o residencial.",
    hours="Website 24/7",
    tags="statewide|substance-use|online|MAT|treatment-locator",
    services="Treatment provider search|MAT locator|Outpatient program finder|Residential program finder",
    county="", served_counties="", coverage="statewide",
    _source="https://findtreatment.gov", _source_type="government", _confidence="high",
)
add(
    name="Georgia Department of Driver Services — ID Services",
    category="id-documentation", region="Statewide",
    description="Georgia Department of Driver Services issues state ID cards and driver's licenses required for employment, housing, and benefits enrollment after release. Returning citizens can apply for a Georgia ID at Customer Service Centers statewide with proof of identity and residency. Not a vital records office—contact county probate court for birth certificates.",
    description_es="El Departamento de Servicios de Conductores de Georgia emite tarjetas de identificación estatal y licencias de conducir necesarias para empleo, vivienda e inscripción en beneficios después de la liberación. Los ciudadanos que regresan pueden solicitar una identificación de Georgia en Centros de Servicio al Cliente con prueba de identidad y residencia. No es oficina de registros vitales.",
    address="2206 East View Parkway", city="Conyers", phone="678-413-8400", email="",
    website="https://dds.georgia.gov",
    eligibility="Georgia residents with required identity and residency documentation; fees apply for ID cards and licenses.",
    eligibility_es="Residentes de Georgia con documentación requerida de identidad y residencia; aplican tarifas para tarjetas de identificación.",
    notes="Find Customer Service Centers at dds.georgia.gov/locations; bring certified birth certificate or passport plus proof of Georgia residency.",
    notes_es="Encuentre Centros de Servicio en dds.georgia.gov/locations; traiga certificado de nacimiento o pasaporte más prueba de residencia.",
    hours="Customer Service Center hours vary; check dds.georgia.gov",
    tags="statewide|id-documentation|DDS|drivers-license|reentry",
    services="State ID card issuance|Driver's license services|ID renewal|Customer Service Center locator",
    county="Rockdale", served_counties="", coverage="statewide",
    _source="https://dds.georgia.gov", _source_type="government", _confidence="high",
)
add(
    name="Georgia Department of Public Health — Vital Records",
    category="id-documentation", region="Statewide",
    description="Georgia Department of Public Health Vital Records office processes requests for birth and death certificates needed for state ID, Medicaid, and employment applications after release. Returning citizens can order certified copies online or by mail with acceptable identification. Processing times vary—order early in reentry planning.",
    description_es="La oficina de Registros Vitales del Departamento de Salud Pública de Georgia procesa solicitudes de certificados de nacimiento y defunción necesarios para identificación estatal, Medicaid y solicitudes de empleo después de la liberación. Los ciudadanos que regresan pueden ordenar copias certificadas en línea o por correo con identificación aceptable.",
    address="1680 Phoenix Boulevard", city="Atlanta", phone="404-679-4702", email="",
    website="https://dph.georgia.gov/vital-records",
    eligibility="Individuals with legal right to request the record; acceptable ID required; fees apply per certificate.",
    eligibility_es="Personas con derecho legal a solicitar el registro; se requiere identificación aceptable; aplican tarifas por certificado.",
    notes="Order online at dph.georgia.gov/vital-records or call 404-679-4702; allow processing time before ID appointments.",
    notes_es="Ordene en línea en dph.georgia.gov/vital-records o llame al 404-679-4702; permita tiempo de procesamiento antes de citas de identificación.",
    hours="Monday–Friday, 8:00 a.m.–4:30 p.m. ET",
    tags="statewide|id-documentation|vital-records|birth-certificate",
    services="Birth certificate orders|Death certificate orders|Online vital records requests|Certified copy processing",
    county="Fulton", served_counties="", coverage="statewide",
    _source="https://dph.georgia.gov/vital-records", _source_type="government", _confidence="high",
)
add(
    name="Georgia Department of Veterans Service — Reentry Supports",
    category="veterans", region="Statewide",
    description="The Georgia Department of Veterans Service helps justice-involved veterans access VA benefits, disability claims, employment programs, and housing resources through county veterans service offices in every county. Veterans released from incarceration may qualify for VA health care, vocational rehabilitation, and veteran treatment court supports. Not emergency shelter—benefits navigation and advocacy.",
    description_es="El Departamento de Servicios para Veteranos de Georgia ayuda a veteranos con antecedentes penales a acceder a beneficios del VA, reclamaciones de discapacidad, programas de empleo y recursos de vivienda a través de oficinas de servicios para veteranos del condado. Los veteranos liberados de la encarcelación pueden calificar para atención médica del VA y tribunales de tratamiento para veteranos.",
    address="270 Washington Street SW", city="Atlanta", phone="404-656-2300", email="",
    website="https://veterans.georgia.gov",
    eligibility="Honorably discharged or qualifying Georgia veterans and their dependents; service documentation required.",
    eligibility_es="Veteranos de Georgia con baja honorable o calificados y sus dependientes; se requiere documentación de servicio.",
    notes="Find your county veterans service office at veterans.georgia.gov/find-your-cvs-office; free benefits claims assistance.",
    notes_es="Encuentre su oficina de servicios para veteranos del condado en veterans.georgia.gov; asistencia gratuita con reclamaciones.",
    hours="County offices Monday–Friday business hours",
    tags="statewide|veterans|VA-benefits|reentry|justice-involved-veterans",
    services="VA benefits claims assistance|Disability claims navigation|Employment program referrals|Veterans treatment court support",
    county="Fulton", served_counties="", coverage="statewide",
    _source="https://veterans.georgia.gov", _source_type="government", _confidence="high",
)

# --- Phase 2: Major metros (program-level anchors) ---
add(
    name="Action Ministries — Reentry & Housing (Atlanta)",
    category="reentry-organizations", region="Atlanta / Fulton County",
    description="Action Ministries (Action Pact) provides housing navigation, emergency assistance, and workforce supports for individuals and families experiencing homelessness and poverty in metro Atlanta including returning citizens seeking stable housing and employment after incarceration. Programs include transitional housing referrals, utility assistance, and job readiness—not a walk-in emergency shelter at all locations.",
    description_es="Action Ministries (Action Pact) ofrece navegación de vivienda, asistencia de emergencia y apoyos de fuerza laboral para personas y familias sin hogar y en pobreza en el metro de Atlanta, incluidos ciudadanos que regresan que buscan vivienda estable y empleo después de la encarcelación. Los programas incluyen referencias de vivienda transicional, asistencia de servicios públicos y preparación laboral.",
    address="1700 Century Circle NE", city="Atlanta", phone="404-881-1991", email="",
    website="https://actionministries.net",
    eligibility="Low-income metro Atlanta residents including justice-involved individuals; program-specific requirements vary.",
    eligibility_es="Residentes de bajos ingresos del metro de Atlanta incluidas personas con antecedentes penales; los requisitos varían según el programa.",
    notes="Visit actionministries.net or call 404-881-1991 for program intake; multiple metro locations serve Fulton and surrounding counties.",
    notes_es="Visite actionministries.net o llame al 404-881-1991 para admisión; múltiples ubicaciones sirven Fulton y condados circundantes.",
    hours="Contact for current hours",
    tags="atlanta|fulton|reentry|housing|employment|reentry-organizations",
    services="Housing navigation|Emergency assistance|Workforce supports|Transitional housing referrals|Utility assistance",
    county="Fulton", served_counties="Fulton|DeKalb|Cobb|Gwinnett", coverage="multi",
    _source="https://actionministries.net", _source_type="nonprofit", _confidence="high",
)
add(
    name="Crossroads Community Ministries — Atlanta",
    category="basic-needs", region="Atlanta / Fulton County",
    description="Crossroads Community Ministries at the Atlanta Day Shelter provides meals, mail service, case management, and reentry resource navigation for unhoused adults in downtown Atlanta including returning citizens recently released from Fulton County Jail or state custody. Direct services at the day shelter—not overnight housing at this location.",
    description_es="Crossroads Community Ministries en el Refugio Diurno de Atlanta proporciona comidas, servicio de correo, manejo de casos y navegación de recursos de reinserción para adultos sin hogar en el centro de Atlanta, incluidos ciudadanos que regresan recién liberados de la cárcel del condado Fulton o custodia estatal. Servicios directos en el refugio diurno, no vivienda nocturna en esta ubicación.",
    address="420 Courtland Street NE", city="Atlanta", phone="404-681-5777", email="",
    website="https://www.crossroadsatlanta.org",
    eligibility="Unhoused adults in metro Atlanta; justice-involved individuals welcome for day services and navigation.",
    eligibility_es="Adultos sin hogar en el metro de Atlanta; personas con antecedentes penales bienvenidas para servicios diurnos.",
    notes="Day shelter services; call 404-681-5777 for hours; connects to housing and employment partners in Fulton County.",
    notes_es="Servicios de refugio diurno; llame al 404-681-5777; conecta con aliados de vivienda y empleo en el condado Fulton.",
    hours="Monday–Friday day shelter hours; call for schedule",
    tags="atlanta|fulton|basic-needs|day-shelter|reentry|meals",
    services="Day shelter meals|Mail service|Case management|Reentry resource navigation|Hygiene access",
    county="Fulton", served_counties="Fulton", coverage="single",
    _source="https://www.crossroadsatlanta.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Union Mission — Savannah Reentry Services",
    category="reentry-organizations", region="Savannah / Chatham County",
    description="Union Mission in Savannah provides emergency shelter, transitional housing, behavioral health, and workforce development for individuals experiencing homelessness including justice-involved adults returning to Chatham County after incarceration. Staff coordinate with Georgia DCS, local courts, and employers on reentry plans. Direct services at Savannah campus—not a statewide hotline.",
    description_es="Union Mission en Savannah ofrece refugio de emergencia, vivienda transicional, salud conductual y desarrollo de fuerza laboral para personas sin hogar, incluidos adultos con antecedentes penales que regresan al condado Chatham después de la encarcelación. El personal coordina con DCS de Georgia, tribunales locales y empleadores en planes de reinserción.",
    address="120 Fahm Street", city="Savannah", phone="912-232-1979", email="",
    website="https://www.unionmission.org",
    eligibility="Adults experiencing homelessness or housing instability in Chatham County; justice-involved individuals accepted per program policy.",
    eligibility_es="Adultos sin hogar o con inestabilidad de vivienda en el condado Chatham; personas con antecedentes penales aceptadas según política del programa.",
    notes="Call 912-232-1979 for intake; multiple Savannah programs include shelter, recovery housing, and employment services.",
    notes_es="Llame al 912-232-1979 para admisión; múltiples programas en Savannah incluyen refugio, vivienda de recuperación y empleo.",
    hours="Contact for program hours",
    tags="savannah|chatham|reentry|housing|workforce|reentry-organizations",
    services="Emergency shelter|Transitional housing|Behavioral health|Workforce development|Reentry case management",
    county="Chatham", served_counties="Chatham", coverage="single",
    _source="https://www.unionmission.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Valley Rescue Mission — Columbus",
    category="housing", region="Columbus / Muscogee County",
    description="Valley Rescue Mission in Columbus provides emergency shelter, recovery housing, meals, and life recovery programming for men and women experiencing homelessness including returning citizens released from Muscogee County Jail or nearby state prisons. Faith-based direct services with case management and workforce preparation—not a DCS referral-only program.",
    description_es="Valley Rescue Mission en Columbus ofrece refugio de emergencia, vivienda de recuperación, comidas y programación de recuperación de vida para hombres y mujeres sin hogar, incluidos ciudadanos que regresan liberados de la cárcel del condado Muscogee o prisiones estatales cercanas. Servicios directos con manejo de casos y preparación laboral.",
    address="2901 2nd Avenue", city="Columbus", phone="706-327-3259", email="",
    website="https://www.valleyrescuemission.org",
    eligibility="Adults experiencing homelessness in Columbus-Muscogee area; program-specific requirements for recovery housing.",
    eligibility_es="Adultos sin hogar en el área Columbus-Muscogee; requisitos específicos del programa para vivienda de recuperación.",
    notes="Call 706-327-3259 for intake; men's and women's programs available; connects to WorkSource Columbus career center.",
    notes_es="Llame al 706-327-3259 para admisión; programas para hombres y mujeres disponibles; conecta con WorkSource Columbus.",
    hours="Contact for intake hours",
    tags="columbus|muscogee|housing|shelter|recovery|reentry",
    services="Emergency shelter|Recovery housing|Meals|Life recovery programming|Case management|Workforce preparation",
    county="Muscogee", served_counties="Muscogee", coverage="single",
    _source="https://www.valleyrescuemission.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Golden Harvest Food Bank — Augusta",
    category="food-nutrition", region="Augusta / CSRA",
    description="Golden Harvest Food Bank serves the Central Savannah River Area with food pantry partnerships, mobile food distributions, and SNAP application assistance for low-income residents including returning citizens reestablishing food security in Richmond, Columbia, Burke, and surrounding counties. A regional food bank—not a walk-in emergency shelter.",
    description_es="Golden Harvest Food Bank sirve el Área Central del Río Savannah con alianzas de despensas de alimentos, distribuciones móviles y asistencia para solicitudes de SNAP para residentes de bajos ingresos, incluidos ciudadanos que regresan que restablecen seguridad alimentaria en Richmond, Columbia, Burke y condados circundantes.",
    address="3310 Commerce Drive", city="Augusta", phone="706-736-1199", email="",
    website="https://www.goldenharvest.org",
    eligibility="Low-income residents of CSRA counties; partner pantries may have additional requirements.",
    eligibility_es="Residentes de bajos ingresos de condados del CSRA; las despensas aliadas pueden tener requisitos adicionales.",
    notes="Find partner pantries at goldenharvest.org; call 706-736-1199; SNAP outreach available in service area.",
    notes_es="Encuentre despensas aliadas en goldenharvest.org; llame al 706-736-1199; alcance de SNAP disponible.",
    hours="Food bank Monday–Friday business hours; pantry hours vary",
    tags="augusta|richmond|food-bank|SNAP|CSRA|reentry",
    services="Food pantry network|Mobile food distribution|SNAP application assistance|Partner agency referrals|Nutrition programs",
    county="Richmond", served_counties="Richmond|Columbia|Burke|McDuffie|Jefferson|Glascock|Warren|Taliaferro|Lincoln|Wilkes", coverage="multi",
    _source="https://www.goldenharvest.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="Macon-Bibb Economic Opportunity Council — Reentry",
    category="reentry-organizations", region="Macon / Bibb County",
    description="Macon-Bibb Economic Opportunity Council provides workforce development, emergency assistance, Head Start referrals, and community action programs for low-income Bibb County residents including justice-involved adults seeking employment and stability after release from local jail or state custody. A community action agency—not emergency overnight shelter.",
    description_es="Macon-Bibb Economic Opportunity Council ofrece desarrollo de fuerza laboral, asistencia de emergencia, referencias Head Start y programas de acción comunitaria para residentes de bajos ingresos del condado Bibb, incluidos adultos con antecedentes penales que buscan empleo y estabilidad después de la liberación.",
    address="653 Second Street", city="Macon", phone="478-745-0035", email="",
    website="https://www.mbeoc.org",
    eligibility="Low-income Macon-Bibb County residents; program-specific income guidelines apply.",
    eligibility_es="Residentes de bajos ingresos del condado Macon-Bibb; aplican pautas de ingresos específicas del programa.",
    notes="Call 478-745-0035 for intake; connects to WorkSource Macon and local reentry partners.",
    notes_es="Llame al 478-745-0035 para admisión; conecta con WorkSource Macon y aliados locales de reinserción.",
    hours="Monday–Friday business hours",
    tags="macon|bibb|reentry|workforce|community-action",
    services="Workforce development|Emergency assistance|Community action programs|Head Start referrals|Reentry partner navigation",
    county="Bibb", served_counties="Bibb", coverage="single",
    _source="https://www.mbeoc.org", _source_type="nonprofit", _confidence="high",
)

# --- Phase 3/4: Program-level expansion ---
from georgia_phase4_expansion import register_phase4
register_phase4(add)

from georgia_rural_depth import register_rural_depth
register_rural_depth(add)

from georgia_category_fill import register_category_fill
register_category_fill(add)

from phase3b_gapfill import register_phase3b_georgia
register_phase3b_georgia(add, ENTRIES)

from georgia_polish import register_polish
register_polish(add)


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
