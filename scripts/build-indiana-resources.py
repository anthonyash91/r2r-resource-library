#!/usr/bin/env python3
"""Generate indiana-resources.csv and indiana-research-log.csv."""
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES_PATH = ROOT / "data" / "indiana-resources.csv"
LOG_PATH = ROOT / "data" / "indiana-research-log.csv"
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
    name="IDOC — Re-Entry Services",
    category="state-agency", region="Statewide",
    description="The Indiana Department of Correction Re-Entry Services division coordinates statewide transition planning and connects people in custody or under parole with housing, employment, treatment, and community partners. Staff support pre-release readiness, HIRE employment linkage, and local community corrections navigation. This office provides planning and referrals—not emergency crisis response.",
    description_es="La división de Servicios de Reinserción del Departamento de Corrección de Indiana coordina la planificación estatal de transición y conecta a personas en custodia o bajo libertad condicional con vivienda, empleo, tratamiento y aliados comunitarios. El personal apoya la preparación previa a la liberación y la vinculación laboral HIRE. Esta oficina ofrece planificación y referencias, no respuesta de crisis.",
    address="302 West Washington Street, Room E-334", city="Indianapolis", phone="1-800-457-8283",
    email="CBlessinger@idoc.in.gov", website="https://www.in.gov/idoc/facilities/re-entry/",
    eligibility="Generally serves Indiana residents under IDOC custody, parole, community corrections, or seeking state reentry coordination.",
    eligibility_es="Generalmente sirve a residentes de Indiana bajo custodia del IDOC, libertad condicional, correcciones comunitarias o que buscan coordinación estatal de reinserción.",
    notes="Call state information line or email Deputy Commissioner office; see in.gov/idoc for HIRE coordinators and parole district contacts. Not a walk-in crisis line.",
    notes_es="Llame a la línea estatal de información; consulte in.gov/idoc para coordinadores HIRE y distritos de libertad condicional. No es una línea de crisis.",
    hours="Monday–Friday, 8:00 a.m.–4:30 p.m. ET",
    tags="statewide|reentry|DOC|probation|parole|hotline",
    services="Reentry planning coordination|HIRE employment referrals|Pre-release resource navigation|Community partner connections",
    county="Marion", served_counties="", coverage="statewide",
    _source="https://www.in.gov/idoc/facilities/re-entry/", _source_type="government", _confidence="high",
)
add(
    name="Hoosier Initiative for Re-Entry (HIRE)",
    category="employment", region="Statewide",
    description="Statewide IDOC employment program helping justice-involved Hoosiers obtain livable-wage jobs through resume development, job coaching, employer partnerships, and pre-release placement coordination. Regional HIRE coordinators serve every Indiana county through facility and parole district offices. HIRE is an employment navigation program—not emergency housing or crisis services.",
    description_es="Programa estatal de empleo del IDOC que ayuda a personas con antecedentes penales a obtener empleos con salario digno mediante desarrollo de currículum, coaching laboral y coordinación de colocación previa a la liberación. Los coordinadores regionales sirven a todos los condados de Indiana. HIRE es un programa de navegación laboral, no de vivienda de emergencia.",
    address="302 West Washington Street", city="Indianapolis", phone="",
    email="HIRE@idoc.IN.gov", website="https://www.in.gov/idoc/hire/",
    eligibility="Justice-involved Indiana residents seeking employment after incarceration or under community supervision; contact regional HIRE coordinator for intake.",
    eligibility_es="Residentes de Indiana con antecedentes penales que buscan empleo después de la encarcelación o bajo supervisión comunitaria; contacte al coordinador HIRE regional.",
    notes="Email HIRE@idoc.IN.gov or use interactive coordinator map at in.gov/idoc/hire; coordinators listed by facility and parole district.",
    notes_es="Envíe correo a HIRE@idoc.IN.gov o use el mapa interactivo de coordinadores en in.gov/idoc/hire.",
    hours="Contact regional HIRE coordinator for hours",
    tags="statewide|employment|HIRE|reentry|fair-chance",
    services="Resume development|Job coaching|Employer partnerships|Pre-release job placement|Financial literacy training",
    county="Marion", served_counties="", coverage="statewide",
    _source="https://www.in.gov/idoc/hire/", _source_type="government", _confidence="high",
)
add(
    name="Indiana 211",
    category="state-agency", region="Statewide",
    description="Free statewide information and referral service connecting Hoosiers to health and human services including housing, food, utilities, employment, and crisis support. Community navigators help callers find local programs by need and ZIP code. Indiana 211 is a referral line operated under FSSA—not a direct-service provider.",
    description_es="Servicio gratuito de información y referencia en todo el estado que conecta a los hoosiers con servicios de salud y humanos incluyendo vivienda, alimentos, empleo y apoyo en crisis. Los navegadores comunitarios ayudan a encontrar programas locales. Indiana 211 es una línea de referencia bajo FSSA, no un proveedor directo.",
    address="", city="", phone="866-211-9966", email="", website="https://www.in.gov/fssa/indiana-211/about-us/",
    eligibility="Open to all Indiana residents; no criminal-record restrictions stated.",
    eligibility_es="Abierto a todos los residentes de Indiana; sin restricciones de antecedentes indicadas.",
    notes="Dial 211 or 866-211-9966; text ZIP code to 898-211 Mon–Fri 8 a.m.–5 p.m. ET; search IN211.org anytime.",
    notes_es="Marque 211 o 866-211-9966; envíe código postal por texto al 898-211 lun–vie 8 a.m.–5 p.m. ET.",
    hours="Phone navigators Mon–Fri 7 a.m.–7 p.m. ET; online search 24/7",
    tags="statewide|hotline|211|referral-only|basic-needs",
    services="Information and referral|Housing resource navigation|Benefits referrals|Crisis resource connections",
    county="", served_counties="", coverage="statewide",
    _source="https://www.in.gov/fssa/indiana-211/about-us/", _source_type="government", _confidence="high",
)
add(
    name="988 Suicide & Crisis Lifeline — Indiana",
    category="healthcare", region="Statewide",
    description="Free confidential 24/7 crisis support for people experiencing mental health emergencies, suicidal thoughts, or substance use crises. Trained specialists provide immediate support and can connect callers to local mobile crisis teams in Indiana. Available to anyone—not reentry-specific but essential for justice-involved individuals in crisis.",
    description_es="Apoyo gratuito y confidencial 24/7 para emergencias de salud mental, pensamientos suicidas o crisis por uso de sustancias. Especialistas capacitados ofrecen apoyo inmediato y conexión a equipos de crisis móviles en Indiana. Disponible para cualquier persona, esencial para personas con antecedentes penales en crisis.",
    address="", city="", phone="988", email="IN988Questions@fssa.IN.gov",
    website="https://988indiana.org",
    eligibility="Open to anyone in Indiana experiencing a mental health or suicide crisis; no eligibility restrictions.",
    eligibility_es="Abierto a cualquier persona en Indiana en crisis de salud mental o suicidio; sin restricciones.",
    notes="Call or text 988; Spanish-language support available. For immediate physical danger call 911.",
    notes_es="Llame o envíe texto al 988; soporte en español disponible. Para peligro físico inmediato llame al 911.",
    hours="Available 24/7",
    tags="statewide|hotline|crisis|mental-health|988",
    services="Crisis counseling|Suicide prevention support|Mental health referrals|Substance use crisis support",
    county="", served_counties="", coverage="statewide",
    _source="https://988indiana.org", _source_type="government", _confidence="high",
)
add(
    name="Indiana Legal Services — Statewide Intake",
    category="legal-aid", region="Statewide",
    description="Indiana's largest nonprofit civil legal aid provider serving low-income residents in all 92 counties with housing, benefits, family law, consumer issues, and record-related civil matters. Centralized intake connects callers to the appropriate regional office. ILS does not handle criminal defense cases.",
    description_es="El mayor proveedor sin fines de lucro de asistencia legal civil de Indiana que sirve a residentes de bajos ingresos en los 92 condados con vivienda, beneficios, derecho familiar y asuntos civiles relacionados con antecedentes. La admisión centralizada conecta con la oficina regional. ILS no maneja defensa penal.",
    address="1200 Madison Avenue, Suite 300", city="Indianapolis", phone="1-844-243-8570",
    email="", website="https://www.indianalegalservices.org",
    eligibility="Low-income Indiana residents with non-criminal legal problems; income and household-size limits apply by federal LSC guidelines.",
    eligibility_es="Residentes de Indiana de bajos ingresos con problemas legales no penales; aplican límites de ingresos.",
    notes="Apply online 24/7 or call intake Mon–Thu 10 a.m.–2 p.m. ET; eight regional offices statewide.",
    notes_es="Solicite en línea 24/7 o llame a admisión lun–jue 10 a.m.–2 p.m. ET.",
    hours="Intake phone Mon–Thu 10:00 a.m.–2:00 p.m. ET; online 24/7",
    tags="statewide|legal-aid|low-income|expungement|hotline",
    services="Civil legal representation|Housing legal aid|Benefits advocacy|Record-related civil relief|Regional office referrals",
    county="Marion", served_counties="", coverage="statewide",
    _source="https://www.indianalegalservices.org/applyonline/", _source_type="nonprofit", _confidence="high",
)
add(
    name="Indiana Legal Help",
    category="legal-aid", region="Statewide",
    description="Statewide legal information portal operated by the Indiana Bar Foundation providing plain-language guides, court forms, and tools for housing, benefits, family law, and finding local legal aid. Helps Hoosiers understand rights and connect to free or low-cost civil attorneys. Online resource hub—not a law firm providing direct representation on its own.",
    description_es="Portal estatal de información legal operado por la Fundación del Colegio de Abogados de Indiana con guías en lenguaje sencillo, formularios judiciales y herramientas para vivienda, beneficios y derecho familiar. Ayuda a encontrar asistencia legal civil gratuita o de bajo costo. Es un centro de recursos en línea, no un bufete.",
    address="", city="Indianapolis", phone="(317) 269-2222", email="",
    website="https://indianalegalhelp.org",
    eligibility="Open to all Indiana residents seeking legal information; direct representation eligibility varies by local legal aid provider.",
    eligibility_es="Abierto a todos los residentes de Indiana que buscan información legal; la representación directa varía según el proveedor local.",
    notes="Call 317-269-2222 Mon–Fri 8:30 a.m.–1:00 p.m. ET; housing legal navigators via website chat 10 a.m.–2 p.m. weekdays.",
    notes_es="Llame al 317-269-2222 lun–vie 8:30 a.m.–1:00 p.m. ET; navegadores de vivienda por chat en el sitio web.",
    hours="Phone Mon–Fri 8:30 a.m.–1:00 p.m. ET; website 24/7",
    tags="statewide|legal-aid|online|housing|hotline",
    services="Legal information guides|Court form assistance|Local legal aid finder|Housing legal navigator chat",
    county="", served_counties="", coverage="statewide",
    _source="https://indianalegalhelp.org", _source_type="nonprofit", _confidence="high",
)
add(
    name="FSSA Benefits Portal",
    category="financial-assistance", region="Statewide",
    description="Official statewide online portal for applying for and managing Indiana public benefits including Medicaid, SNAP food assistance, TANF cash assistance, and Hoosier Healthwise coverage. Justice-involved individuals can apply for health coverage and food support after release. County Division of Family Resources offices assist with verification.",
    description_es="Portal oficial en línea para solicitar y administrar beneficios públicos de Indiana incluyendo Medicaid, SNAP, TANF y cobertura Hoosier Healthwise. Personas en reinserción pueden solicitar cobertura de salud y apoyo alimentario después de la liberación. Las oficinas DFR del condado ayudan con verificación.",
    address="", city="", phone="1-800-403-0864", email="", website="https://fssabenefits.in.gov",
    eligibility="Indiana residents meeting income and program requirements for Medicaid, SNAP, TANF, or HIP; criminal record generally not a barrier.",
    eligibility_es="Residentes de Indiana que cumplan requisitos de ingresos para Medicaid, SNAP, TANF o HIP; antecedentes penales generalmente no son barrera.",
    notes="Create account online at fssabenefits.in.gov; call 800-403-0864 for benefits or portal technical support.",
    notes_es="Cree una cuenta en línea; llame al 800-403-0864 para beneficios o soporte técnico del portal.",
    hours="Online 24/7; DFR phone Mon–Fri 8:00 a.m.–4:30 p.m. local time",
    tags="statewide|benefits|SNAP|Medicaid|online",
    services="Medicaid application|SNAP enrollment|Cash assistance application|Benefits account management",
    county="", served_counties="", coverage="statewide",
    _source="https://www.in.gov/fssa/create-a-benefits-portal-account/", _source_type="government", _confidence="high",
)
add(
    name="Recovery Works — Indiana DMHA",
    category="substance-use-treatment", region="Statewide",
    description="Indiana Division of Mental Health and Addiction voucher program funding treatment and recovery housing for justice-involved adults without other payer sources. Criminal justice partners submit referrals through the online intake system; liaisons match participants to certified providers. Referral required—not a walk-in crisis line.",
    description_es="Programa de vales de la División de Salud Mental y Adicciones de Indiana que financia tratamiento y vivienda de recuperación para adultos con antecedentes penales sin otra fuente de pago. Los aliados de justicia penal envían referencias por el sistema en línea. Se requiere referencia, no es una línea de crisis sin cita.",
    address="402 West Washington Street", city="Indianapolis", phone="(317) 232-7911",
    email="Recovery.Works@fssa.in.gov", website="https://www.in.gov/fssa/dmha/recovery-works/",
    eligibility="Justice-involved Indiana adults with mental health or substance use needs lacking Medicaid, HIP, or private insurance; criminal justice partner referral required.",
    eligibility_es="Adultos de Indiana con antecedentes penales con necesidades de salud mental o sustancias sin Medicaid, HIP o seguro privado; se requiere referencia de aliado de justicia penal.",
    notes="Criminal justice partners email RecoveryWorks@paceindy.org for referral forms; participants cannot self-refer directly.",
    notes_es="Los aliados de justicia penal envíen correo a RecoveryWorks@paceindy.org para formularios; los participantes no pueden autorreferirse.",
    hours="DMHA staff Mon–Fri business hours; monthly open office hours first Wednesday noon ET",
    tags="statewide|substance-use|recovery|vouchers|referral-required",
    services="Treatment vouchers|Recovery housing vouchers|Forensic treatment referrals|Provider matching",
    county="Marion", served_counties="", coverage="statewide",
    _source="https://www.in.gov/fssa/dmha/recovery-works/recovery-works-team/", _source_type="government", _confidence="high",
)
add(
    name="SAMHSA National Helpline",
    category="substance-use-treatment", region="Statewide",
    description="Free confidential 24/7 treatment referral and information service for individuals and families facing mental health or substance use disorders. Provides referrals to local treatment facilities and community organizations in Indiana and nationwide. Spanish-language support available.",
    description_es="Servicio gratuito y confidencial 24/7 de referencia e información para personas y familias con trastornos de salud mental o uso de sustancias. Proporciona referencias a centros de tratamiento locales en Indiana y a nivel nacional. Soporte en español disponible.",
    address="", city="", phone="1-800-662-4357", email="", website="https://www.samhsa.gov/find-help/national-helpline",
    eligibility="Open to anyone in the United States seeking substance use or mental health treatment information and referrals.",
    eligibility_es="Abierto a cualquier persona en Estados Unidos que busque información y referencias de tratamiento.",
    notes="TTY: 1-800-487-4889; also use FindTreatment.gov to search Indiana providers online.",
    notes_es="TTY: 1-800-487-4889; también use FindTreatment.gov para buscar proveedores en Indiana.",
    hours="Available 24/7",
    tags="statewide|hotline|substance-use|treatment-referral|national",
    services="Treatment referrals|Substance use information|Mental health resource navigation",
    county="", served_counties="", coverage="statewide",
    _source="https://www.samhsa.gov/find-help/national-helpline", _source_type="government", _confidence="high",
)
add(
    name="FindTreatment.gov — Indiana Provider Search",
    category="substance-use-treatment", region="Statewide",
    description="Official SAMHSA online locator for substance use and mental health treatment facilities serving Indiana. Users search by location, treatment type, and payment options to find licensed providers with current openings. Facility admission requirements vary; justice-involved individuals should confirm criminal-record policies with each provider.",
    description_es="Localizador oficial en línea de SAMHSA para centros de tratamiento de sustancias y salud mental que sirven a Indiana. Los usuarios buscan por ubicación, tipo de tratamiento y opciones de pago. Los requisitos de admisión varían; las personas con antecedentes penales deben confirmar políticas con cada proveedor.",
    address="", city="", phone="1-833-888-1553", email="FindTreatment@samhsa.hhs.gov",
    website="https://findtreatment.gov",
    eligibility="Open to anyone seeking treatment; facility admission requirements vary by provider.",
    eligibility_es="Abierto a cualquier persona que busque tratamiento; los requisitos de admisión varían según el proveedor.",
    notes="Indiana Addiction Hotline 1-800-662-4357 also routes to treatment help; facility data updated weekly.",
    notes_es="La línea de adicciones de Indiana 1-800-662-4357 también conecta con ayuda de tratamiento.",
    hours="Online 24/7; BHSIS support Mon–Fri 8 a.m.–6 p.m. ET",
    tags="statewide|substance-use|online|treatment-referral",
    services="Treatment facility search|Provider availability information|Mental health provider locator",
    county="", served_counties="", coverage="statewide",
    _source="https://findtreatment.gov", _source_type="government", _confidence="high",
)
add(
    name="IDOC — Division of Parole Services",
    category="probation-parole", region="Statewide",
    description="State agency responsible for parole supervision, parole board processes, and community supervision of individuals released from Indiana prisons. Ten regional parole districts connect supervisees to reentry resources and enforce supervision conditions. Contact for reporting requirements, district office locations, and supervision status—not a resource navigation hotline.",
    description_es="Agencia estatal responsable de la supervisión de libertad condicional y supervisión comunitaria de personas liberadas de prisiones de Indiana. Diez distritos regionales conectan a supervisados con recursos de reinserción. Contacte para requisitos de reporte y ubicaciones de oficinas, no para navegación general de recursos.",
    address="302 West Washington Street, Room E-334", city="Indianapolis", phone="(317) 232-5719",
    email="", website="https://www.in.gov/idoc/facilities/parole-districts/",
    eligibility="Individuals under Indiana parole or community supervision; family members may contact for general district information.",
    eligibility_es="Personas bajo libertad condicional o supervisión comunitaria de Indiana; familiares pueden contactar para información del distrito.",
    notes="Ten parole districts PD1–PD10; see in.gov/idoc parole district pages for local office phones and addresses.",
    notes_es="Diez distritos PD1–PD10; consulte las páginas de distritos en in.gov/idoc para teléfonos y direcciones locales.",
    hours="District offices Monday–Friday, 8:00 a.m.–4:30 p.m. local time",
    tags="statewide|parole|DOC|probation|supervision",
    services="Parole supervision|Community supervision|District office coordination|Supervision compliance support",
    county="Marion", served_counties="", coverage="statewide",
    _source="https://www.in.gov/idoc/facilities/parole-districts/", _source_type="government", _confidence="high",
)
add(
    name="IDOC — Community Corrections Overview",
    category="state-agency", region="Statewide",
    description="Indiana's community corrections system provides county-administered intermediate sanctions, work release, home detention, and reentry services as alternatives to state incarceration. Programs operate under local advisory boards with IDOC grant oversight. Justice-involved individuals are typically referred through courts, prosecutors, or IDOC—not walk-in enrollment at the state level.",
    description_es="El sistema de correcciones comunitarias de Indiana ofrece sanciones intermedias, libertad condicional en el hogar y servicios de reinserción administrados por condados como alternativas a la encarcelación estatal. Los programas operan bajo juntas locales con supervisión de subvenciones del IDOC. Las personas generalmente son referidas por tribunales o el IDOC.",
    address="302 West Washington Street", city="Indianapolis", phone="1-800-457-8283",
    email="", website="https://www.in.gov/idoc/community-corrections/",
    eligibility="Individuals referred by Indiana courts, prosecutors, or IDOC to county community corrections programs; offense-type eligibility varies by county.",
    eligibility_es="Personas referidas por tribunales, fiscales o IDOC a programas de correcciones comunitarias del condado; la elegibilidad varía por condado.",
    notes="Contact local county community corrections office for intake; IDOC grant entity contact list at in.gov/idoc/community-corrections.",
    notes_es="Contacte la oficina local de correcciones comunitarias del condado; lista de contactos en in.gov/idoc.",
    hours="County office hours vary",
    tags="statewide|community-corrections|probation|reentry|referral-required",
    services="Work release programs|Home detention|Intermediate sanctions|County reentry coordination",
    county="Marion", served_counties="", coverage="statewide",
    _source="https://www.in.gov/idoc/community-corrections/", _source_type="government", _confidence="high",
)
add(
    name="Indiana Bureau of Motor Vehicles (BMV)",
    category="id-documentation", region="Statewide",
    description="State agency providing driver's licenses, state identification cards, vehicle registration, and reinstatement services. Reentry partners and community programs often assist returning citizens with documentation needed for employment and benefits. myBMV.com supports many transactions online.",
    description_es="Agencia estatal que proporciona licencias de conducir, identificaciones estatales, registro vehicular y servicios de restablecimiento. Los aliados de reinserción ayudan a ciudadanos que regresan con documentación necesaria para empleo y beneficios. myBMV.com permite muchas transacciones en línea.",
    address="100 North Senate Avenue, Room 402", city="Indianapolis", phone="888-692-6841",
    email="", website="https://www.in.gov/bmv/",
    eligibility="Indiana residents seeking credentials or reinstatement; specific document requirements apply for ID issuance.",
    eligibility_es="Residentes de Indiana que buscan credenciales o restablecimiento; aplican requisitos específicos de documentos para emisión de identificación.",
    notes="Toll-free 888-692-6841 or local 317-233-6000 Mon–Fri 8 a.m.–6 p.m. ET; IVR available 24/7 for status checks.",
    notes_es="Línea gratuita 888-692-6841 lun–vie 8 a.m.–6 p.m. ET; IVR disponible 24/7 para verificar estado.",
    hours="Customer associates Mon–Fri 8:00 a.m.–6:00 p.m. ET; automated system 24/7",
    tags="statewide|id-documentation|BMV|drivers-license|online",
    services="State ID issuance|Driver's license services|Reinstatement fee payment|Branch location lookup",
    county="Marion", served_counties="", coverage="statewide",
    _source="https://www.in.gov/bmv/contact/", _source_type="government", _confidence="high",
)
add(
    name="Indiana Department of Workforce Development — WorkOne",
    category="employment", region="Statewide",
    description="Statewide workforce system connecting job seekers—including justice-involved Hoosiers—to training, job placement, and employer services through regional WorkOne centers in all 92 counties. DWD coordinates unemployment insurance, career coaching, and skills training partnerships. WorkOne is an employment hub—not a housing or legal aid provider.",
    description_es="Sistema estatal de fuerza laboral que conecta a buscadores de empleo—incluidos hoosiers con antecedentes penales—a capacitación, colocación laboral y servicios de empleadores a través de centros WorkOne regionales en los 92 condados. DWD coordina seguro de desempleo y coaching de carrera.",
    address="10 North Senate Avenue", city="Indianapolis", phone="1-800-891-6499",
    email="askworkone@in.gov", website="https://www.in.gov/dwd/workone/",
    eligibility="Indiana residents seeking employment, training, or unemployment benefits; no criminal-record restrictions stated for core services.",
    eligibility_es="Residentes de Indiana que buscan empleo, capacitación o beneficios de desempleo; sin restricciones de antecedentes indicadas para servicios básicos.",
    notes="Call 800-891-6499 Mon–Fri 8 a.m.–4:30 p.m. ET; locate regional office at in.gov/dwd/workone; unemployment at Unemployment.IN.gov.",
    notes_es="Llame al 800-891-6499 lun–vie 8 a.m.–4:30 p.m. ET; localice oficina regional en in.gov/dwd/workone.",
    hours="State line Mon–Fri 8:00 a.m.–4:30 p.m. ET; center hours vary by location",
    tags="statewide|employment|WorkOne|training|unemployment",
    services="Job search assistance|Skills training referrals|Unemployment insurance navigation|Employer connections",
    county="Marion", served_counties="", coverage="statewide",
    _source="https://www.in.gov/dwd/workone/", _source_type="government", _confidence="high",
)
add(
    name="Indiana Addiction Hotline",
    category="substance-use-treatment", region="Statewide",
    description="State-supported helpline connecting Hoosiers to addiction treatment resources, recovery support, and live chat assistance through Indiana's Next Level Recovery initiative. Trained specialists help callers find local treatment options and understand pathways to care. A referral and information line—not a direct treatment provider.",
    description_es="Línea de ayuda apoyada por el estado que conecta a hoosiers con recursos de tratamiento de adicciones y apoyo de recuperación a través de la iniciativa Next Level Recovery de Indiana. Especialistas capacitados ayudan a encontrar opciones de tratamiento locales. Es una línea de referencia, no un proveedor directo.",
    address="", city="", phone="1-800-662-4357", email="",
    website="https://www.in.gov/recovery/treatment/",
    eligibility="Open to Indiana residents seeking addiction treatment information and referrals; no criminal-record restrictions stated.",
    eligibility_es="Abierto a residentes de Indiana que buscan información y referencias de tratamiento de adicciones.",
    notes="Also reachable as 1-800-662-HELP; live chat available at in.gov/recovery; complements 988 for crisis.",
    notes_es="También disponible como 1-800-662-HELP; chat en vivo en in.gov/recovery; complementa al 988 para crisis.",
    hours="Available 24/7",
    tags="statewide|hotline|substance-use|treatment-referral|recovery",
    services="Treatment referrals|Addiction resource navigation|Live chat support|Recovery pathway information",
    county="", served_counties="", coverage="statewide",
    _source="https://www.in.gov/recovery/treatment/", _source_type="government", _confidence="high",
)
add(
    name="DMHA Mental Health Consumer Service Line",
    category="healthcare", region="Statewide",
    description="Free statewide phone line providing referral information for addiction and mental health services, consumer rights guidance, and navigation of Indiana's public behavioral health system. Helps Hoosiers find treatment providers and understand how to access DMHA-certified community mental health centers.",
    description_es="Línea telefónica gratuita en todo el estado que ofrece referencias para servicios de adicción y salud mental, orientación sobre derechos del consumidor y navegación del sistema público de salud conductual de Indiana. Ayuda a encontrar proveedores de tratamiento certificados por DMHA.",
    address="402 West Washington Street", city="Indianapolis", phone="1-800-901-1133",
    email="", website="https://www.in.gov/fssa/contact-us/important-toll-free-numbers/",
    eligibility="Open to Indiana residents seeking addiction or mental health service referrals; no criminal-record restrictions stated.",
    eligibility_es="Abierto a residentes de Indiana que buscan referencias de servicios de adicción o salud mental.",
    notes="Listed as mental health consumer service on FSSA toll-free numbers page; complements 988 for non-emergency navigation.",
    notes_es="Listada como servicio al consumidor de salud mental en la página de números gratuitos de FSSA; complementa al 988.",
    hours="Contact for current hours",
    tags="statewide|hotline|mental-health|Medicaid|referral-only",
    services="Treatment referrals|Mental health resource navigation|Consumer rights guidance|CMHC locator assistance",
    county="Marion", served_counties="", coverage="statewide",
    _source="https://www.in.gov/fssa/contact-us/important-toll-free-numbers/", _source_type="government", _confidence="high",
)

# --- Reentry coalitions and county partners ---
COALITIONS = [
    dict(name="Marion County Reentry Coalition", region="Indianapolis / Marion County",
         phone="(317) 423-1770", email="marioncountyreentrycoalition@gmail.com", county="Marion",
         served="Marion", address="", city="Indianapolis",
         notes="Coalition connecting justice-involved residents to PACE, Horizon House, and employer partners; contact for coalition referrals."),
    dict(name="Allen County Reentry Partners", region="Fort Wayne / Allen County",
         phone="(260) 449-7252", email="eric.zimmerman@co.allen.in.us", county="Allen",
         served="Allen", address="201 West Superior Street", city="Fort Wayne",
         notes="Allen County Community Corrections coordinates reentry partner network; contact executive director for referrals."),
    dict(name="Lake County Reentry Collaborative", region="Gary / Lake County",
         phone="(219) 755-3850", email="bittokj@lakecountyin.org", county="Lake",
         served="Lake", address="2600 West 93rd Avenue", city="Crown Point",
         notes="Lake County Community Corrections hosts reentry coordination and work release programs."),
    dict(name="Vanderburgh County Reentry Network", region="Evansville / Vanderburgh County",
         phone="(812) 424-9821", email="aburridge@idoc.in.gov", county="Vanderburgh",
         served="Vanderburgh", address="27 Pasco Avenue", city="Evansville",
         notes="Evansville Parole District PD4 reentry contacts coordinate southwest Indiana reentry partner referrals."),
    dict(name="Hamilton County Reentry Initiative", region="Noblesville / Hamilton County",
         phone="(317) 244-3144", email="clawrence@idoc.in.gov", county="Hamilton",
         served="Hamilton", address="727 Moon Road", city="Plainfield",
         notes="Served through Re-Entry Parole District PD1 covering Boone, Hamilton, Hancock, Hendricks, Johnson, Morgan, and Shelby."),
    dict(name="St. Joseph County Reentry Partners", region="South Bend / St. Joseph County",
         phone="(574) 234-8121", email="", county="St. Joseph",
         served="St. Joseph", address="227 South Main Street", city="South Bend",
         notes="Indiana Legal Services South Bend office and local CBOs support reentry navigation; contact ILS for legal referrals."),
    dict(name="Elkhart County Reentry Collaborative", region="Elkhart County",
         phone="(574) 234-8121", email="", county="Elkhart",
         served="Elkhart", address="", city="Elkhart",
         notes="Served through ILS South Bend region; contact coalition partners via Indiana Legal Services intake for navigation."),
    dict(name="Tippecanoe County Reentry Partners", region="Lafayette / Tippecanoe County",
         phone="(765) 423-5327", email="", county="Tippecanoe",
         served="Tippecanoe", address="8 North 3rd Street, Suite 102", city="Lafayette",
         notes="ILS Lafayette regional office serves west-central Indiana reentry legal and benefits needs."),
    dict(name="Monroe County Reentry Collaborative", region="Bloomington / Monroe County",
         phone="(812) 339-7668", email="", county="Monroe",
         served="Monroe", address="100 South College Avenue, Suite 232", city="Bloomington",
         notes="ILS Bloomington office and local treatment providers coordinate south-central Indiana reentry services."),
    dict(name="Vigo County Reentry Partners", region="Terre Haute / Vigo County",
         phone="(812) 235-0606", email="mblade@idoc.in.gov", county="Vigo",
         served="Vigo", address="700 South State Road 46", city="Terre Haute",
         notes="Terre Haute Parole District PD10 reentry contacts support Wabash Valley returning citizens."),
    dict(name="Allen–Northeast Indiana Reentry Council", region="Northeast Indiana",
         phone="(260) 424-9155", email="", county="Allen",
         served="Allen|DeKalb|Noble|Steuben|Whitley", address="110 West Berry Street, Suite 2007", city="Fort Wayne",
         notes="ILS Fort Wayne regional office and northeast Indiana CBOs support coalition partner referrals."),
    dict(name="Southwest Indiana Reentry Collaborative", region="Southwest Indiana",
         phone="(812) 426-1295", email="", county="Vanderburgh",
         served="Daviess|Dubois|Gibson|Knox|Martin|Pike|Posey|Spencer|Vanderburgh|Warrick",
         address="915 Main Street, Suite 201", city="Evansville",
         notes="ILS Evansville office serves ten southwest Indiana counties for civil legal aid and partner referrals."),
]

for c in COALITIONS:
    sc = c["served"]
    cov = "single" if "|" not in sc else "multi"
    counties_label = sc.replace("|", ", ")
    desc_en = (
        f"Local reentry coalition and partner network serving {counties_label} in Indiana. "
        "Volunteers, community corrections staff, and partner agencies coordinate resources and referrals "
        "for justice-involved individuals—primarily a networking and navigation council, not a full-service crisis provider."
    )
    desc_es = (
        f"Coalición local de reinserción y red de aliados que sirve {counties_label} en Indiana. "
        "Voluntarios, personal de correcciones comunitarias y agencias aliadas coordinan recursos y referencias "
        "para personas con antecedentes penales—principalmente un consejo de red, no un proveedor de crisis completo."
    )
    add(
        name=c["name"], category="reentry-organizations", region=c["region"],
        description=desc_en, description_es=desc_es,
        address=c.get("address", ""), city=c.get("city", ""),
        phone=c["phone"], email=c.get("email", ""),
        website="https://www.in.gov/idoc/facilities/re-entry/",
        eligibility="Justice-involved residents of served counties; contact coalition for current partner eligibility.",
        eligibility_es="Residentes con antecedentes penales en los condados servidos; contacte la coalición.",
        notes=c["notes"] + " Does not provide emergency housing or crisis response.",
        notes_es=c["notes"] + " No ofrece vivienda de emergencia ni respuesta de crisis.",
        hours="Contact for meeting dates and hours",
        tags=f"reentry|coalition|referral-only|{c['county'].lower()}",
        services="Resource networking|Community partner referrals|Reentry navigation|Local service coordination",
        county=c["county"],
        served_counties=sc if cov == "multi" else sc,
        coverage=cov,
        _source="https://www.in.gov/idoc/facilities/re-entry/",
        _source_type="government", _confidence="high" if c["phone"] else "medium",
    )

# --- Regional legal aids ---
LEGAL_AIDS = [
    dict(name="Indiana Legal Services — Indianapolis (Central)", region="Central Indiana — 17 counties",
         phone="(317) 631-9410", website="https://www.indianalegalservices.org",
         address="1200 Madison Avenue, Suite 300", city="Indianapolis", county="Marion",
         served="Boone|Decatur|Delaware|Fayette|Franklin|Hamilton|Hancock|Hendricks|Henry|Johnson|Madison|Marion|Randolph|Rush|Shelby|Union|Wayne",
         desc="Free civil legal aid for low-income central Indiana residents including housing defense, benefits appeals, family law with domestic violence, and civil record-related matters."),
    dict(name="Indiana Legal Services — Bloomington", region="South-Central Indiana — 14 counties",
         phone="(812) 339-7668", website="https://www.indianalegalservices.org",
         address="100 South College Avenue, Suite 232", city="Bloomington", county="Monroe",
         served="Bartholomew|Brown|Clay|Greene|Jackson|Lawrence|Monroe|Morgan|Orange|Owen|Parke|Putnam|Sullivan|Vigo",
         desc="Free civil legal assistance for low-income residents in south-central Indiana including eviction defense, public benefits, and civil legal issues affecting reentry stability."),
    dict(name="Indiana Legal Services — Lafayette", region="West-Central Indiana — 14 counties",
         phone="(765) 423-5327", website="https://www.indianalegalservices.org",
         address="8 North 3rd Street, Suite 102", city="Lafayette", county="Tippecanoe",
         served="Benton|Carroll|Cass|Clinton|Fountain|Howard|Miami|Montgomery|Tippecanoe|Tipton|Vermillion|Wabash|Warren|White",
         desc="Free civil legal aid serving west-central Indiana counties with housing, benefits, and consumer legal issues for eligible low-income clients."),
    dict(name="Indiana Legal Services — Evansville", region="Southwest Indiana — 11 counties",
         phone="(812) 426-1295", website="https://www.indianalegalservices.org",
         address="915 Main Street, Suite 201", city="Evansville", county="Vanderburgh",
         served="Daviess|Dubois|Gibson|Knox|Martin|Perry|Pike|Posey|Spencer|Vanderburgh|Warrick",
         desc="Free civil legal services for low-income southwest Indiana residents including housing, benefits, and family law matters affecting returning citizens."),
    dict(name="Indiana Legal Services — Merrillville", region="Northwest Indiana — 4 counties",
         phone="(219) 738-6040", website="https://www.indianalegalservices.org",
         address="7863 Broadway, Suite 205", city="Merrillville", county="Lake",
         served="Jasper|Lake|Newton|Porter",
         desc="Free civil legal aid for low-income residents in northwest Indiana including Lake County housing, benefits, and civil legal barriers to reentry."),
    dict(name="Indiana Legal Services — Fort Wayne", region="Northeast Indiana — 10 counties",
         phone="(260) 424-9155", website="https://www.indianalegalservices.org",
         address="110 West Berry Street, Suite 2007", city="Fort Wayne", county="Allen",
         served="Adams|Allen|Blackford|DeKalb|Grant|Huntington|Jay|Steuben|Wells|Whitley",
         desc="Free civil legal assistance for low-income northeast Indiana residents including housing defense, benefits advocacy, and civil legal issues."),
    dict(name="Indiana Legal Services — New Albany", region="Southeast Indiana — 12 counties",
         phone="(812) 945-4123", website="https://www.indianalegalservices.org",
         address="3303 Plaza Drive, Suite 5", city="New Albany", county="Floyd",
         served="Clark|Crawford|Dearborn|Floyd|Harrison|Jefferson|Jennings|Ohio|Ripley|Scott|Switzerland|Washington",
         desc="Free civil legal aid for low-income southeast Indiana residents including housing, benefits, and family law with domestic violence protections."),
    dict(name="Indiana Legal Services — South Bend", region="North-Central Indiana — 10 counties",
         phone="(574) 234-8121", website="https://www.indianalegalservices.org",
         address="227 South Main Street, Suite 200", city="South Bend", county="St. Joseph",
         served="Elkhart|Fulton|Kosciusko|LaGrange|LaPorte|Marshall|Noble|Pulaski|Starke|St. Joseph",
         desc="Free civil legal services for low-income north-central Indiana residents including housing, benefits, and consumer legal matters."),
    dict(name="Neighborhood Christian Legal Clinic — Indianapolis", region="Central Indiana",
         phone="(317) 429-4131", website="https://www.nclegalclinic.org",
         address="3102 East 10th Street", city="Indianapolis", county="Marion",
         served="Marion|Boone|Hamilton|Hancock|Hendricks|Johnson|Morgan|Shelby",
         desc="Faith-based legal clinic providing free civil legal services statewide with Indianapolis hub, including immigration, housing, and second-chance legal support."),
    dict(name="Neighborhood Christian Legal Clinic — Fort Wayne", region="Northeast Indiana",
         phone="(260) 456-8972", website="https://www.nclegalclinic.org",
         address="347 West Berry Street", city="Fort Wayne", county="Allen",
         served="Adams|Allen|DeKalb|Grant|Huntington|Jay|Kosciusko|LaGrange|Noble|Steuben|Wells|Whitley",
         desc="Fort Wayne office of Neighborhood Christian Legal Clinic offering free civil legal aid including housing, family law, and record-related civil matters."),
    dict(name="Indianapolis Legal Aid Society", region="Indianapolis / Central Indiana",
         phone="(317) 635-9538", website="https://www.indylas.org",
         address="615 North Alabama Street, Suite 122", city="Indianapolis", county="Marion",
         served="Boone|Hamilton|Hancock|Hendricks|Johnson|Marion|Morgan|Shelby",
         desc="Nonprofit providing free civil legal advice and representation for low-income central Indiana residents; appointment required for attorney consultation."),
    dict(name="Legal Aid Society of Evansville", region="Evansville / Vanderburgh County",
         phone="(812) 426-1295", website="https://www.indianalegalservices.org",
         address="915 Main Street, Suite 201", city="Evansville", county="Vanderburgh",
         served="Daviess|Dubois|Gibson|Knox|Martin|Perry|Pike|Posey|Spencer|Vanderburgh|Warrick",
         desc="Evansville regional office of Indiana Legal Services providing free civil legal aid for low-income southwest Indiana residents including housing and benefits."),
]

for la in LEGAL_AIDS:
    cov = "single" if "|" not in la["served"] else "multi"
    add(
        name=la["name"], category="legal-aid", region=la["region"],
        description=la["desc"] + " Income and household-size limits apply; intake through centralized line 844-243-8570 or local office.",
        description_es=la["desc"].replace("Free", "Asistencia legal civil gratuita").replace("Nonprofit", "Organización sin fines de lucro") + " Aplican límites de ingresos; admisión por línea 844-243-8570 u oficina local.",
        address=la["address"], city=la["city"], phone=la["phone"], email="", website=la["website"],
        eligibility="Low-income Indiana residents in service area; veterans and seniors may qualify with higher income limits.",
        eligibility_es="Residentes de bajos ingresos en el área de servicio; veteranos y personas mayores pueden calificar con límites más altos.",
        notes="Apply online at indianalegalservices.org or call 844-243-8570 Mon–Thu 10 a.m.–2 p.m. ET for ILS offices.",
        notes_es="Solicite en línea o llame al 844-243-8570 lun–jue 10 a.m.–2 p.m. ET para oficinas ILS.",
        hours="Intake Mon–Thu mornings; call local office for walk-in hours",
        tags="legal-aid|low-income|reentry|housing",
        services="Civil legal representation|Housing legal aid|Benefits advocacy|Family law assistance",
        county=la["county"],
        served_counties=la["served"], coverage=cov,
        _source=la["website"], _source_type="nonprofit", _confidence="high",
    )

# --- Parole districts ---
PAROLE_DISTRICTS = [
    dict(name="Re-Entry Parole District (PD 1)", region="Central Indiana — 7 counties",
         phone="(317) 244-3144", address="2596 North Girls School Road", city="Indianapolis",
         county="Marion", served="Boone|Hamilton|Hancock|Hendricks|Johnson|Morgan|Shelby",
         notes="Re-Entry PD1 Plainfield/Indianapolis office; HIRE Region 3 coordinator Nathan Noll (317) 542-3768."),
    dict(name="Fort Wayne Parole District (PD 2)", region="Northeast Indiana — 10 counties",
         phone="(260) 484-3048", address="3111 Coliseum Boulevard", city="Fort Wayne",
         county="Allen", served="Adams|Allen|DeKalb|Huntington|Kosciusko|LaGrange|Noble|Steuben|Wells|Whitley",
         notes="Supervisor Bobby Yarborough; serves northeast Indiana parole supervisees."),
    dict(name="Indianapolis Parole District (PD 3)", region="Marion County",
         phone="(317) 541-1088", address="6400 East 30th Street", city="Indianapolis",
         county="Marion", served="Marion",
         notes="Supervisor Drew Adams; HIRE Region 5B coordinator Megan Worrell (317) 864-7510."),
    dict(name="Evansville Parole District (PD 4)", region="Southwest Indiana — 10 counties",
         phone="(812) 424-9821", address="27 Pasco Avenue", city="Evansville",
         county="Vanderburgh", served="Daviess|Dubois|Gibson|Knox|Martin|Pike|Posey|Spencer|Vanderburgh|Warrick",
         notes="Supervisor Aleisha Burridge; HIRE Region 8 coordinator Jordan Baer (812) 454-9657."),
    dict(name="Bloomington Parole District (PD 5)", region="South-Central Indiana",
         phone="(812) 339-7668", address="100 South College Avenue", city="Bloomington",
         county="Monroe", served="Bartholomew|Brown|Clay|Greene|Jackson|Lawrence|Monroe|Morgan|Orange|Owen|Parke|Putnam|Sullivan|Vigo",
         notes="Contact IDOC parole districts page for PD5 office phone; ILS Bloomington supports civil legal needs."),
    dict(name="Gary Parole District (PD 6)", region="Northwest Indiana",
         phone="(219) 738-6040", address="7863 Broadway, Suite 205", city="Merrillville",
         county="Lake", served="Jasper|Lake|Newton|Porter",
         notes="Northwest Indiana parole district; verify current PD6 office on in.gov/idoc parole districts page."),
    dict(name="New Castle Parole District (PD 7)", region="East-Central Indiana",
         phone="(765) 529-2359", address="", city="New Castle",
         county="Henry", served="Delaware|Fayette|Franklin|Henry|Madison|Randolph|Rush|Union|Wayne",
         notes="East-central Indiana parole district; contact IDOC for current PD7 office address."),
    dict(name="South Bend Parole District (PD 8)", region="North-Central Indiana",
         phone="(574) 234-8121", address="227 South Main Street", city="South Bend",
         county="St. Joseph", served="Elkhart|Fulton|Kosciusko|LaGrange|LaPorte|Marshall|Noble|Pulaski|Starke|St. Joseph",
         notes="North-central Indiana parole district serving St. Joseph County and surrounding counties."),
    dict(name="Madison Parole District (PD 9)", region="Southeast Indiana",
         phone="(812) 945-4123", address="3303 Plaza Drive, Suite 5", city="New Albany",
         county="Floyd", served="Clark|Crawford|Dearborn|Floyd|Harrison|Jefferson|Jennings|Ohio|Ripley|Scott|Switzerland|Washington",
         notes="Southeast Indiana parole district; ILS New Albany supports regional civil legal needs."),
    dict(name="Terre Haute Parole District (PD 10)", region="Wabash Valley — 14 counties",
         phone="(812) 235-0606", address="700 South State Road 46", city="Terre Haute",
         county="Vigo", served="Benton|Carroll|Clay|Clinton|Fountain|Greene|Montgomery|Owen|Parke|Putnam|Sullivan|Tippecanoe|Vermillion|Vigo|Warren",
         notes="Supervisor Marcus Blade; serves Wabash Valley parole supervisees."),
]

for pd in PAROLE_DISTRICTS:
    sc = pd["served"]
    cov = "single" if "|" not in sc else "multi"
    counties_label = sc.replace("|", ", ")
    desc_en = (
        f"IDOC parole district office supervising justice-involved individuals in {counties_label}. "
        "Parole agents connect supervisees to HIRE employment coordinators, transitional healthcare facilitators, "
        "and community reentry partners. Contact for reporting requirements and supervision compliance—not emergency services."
    )
    desc_es = (
        f"Oficina del distrito de libertad condicional del IDOC que supervisa personas en {counties_label}. "
        "Los agentes conectan a supervisados con coordinadores HIRE y aliados de reinserción comunitaria. "
        "Contacte para requisitos de reporte y cumplimiento de supervisión, no para servicios de emergencia."
    )
    add(
        name=pd["name"], category="probation-parole", region=pd["region"],
        description=desc_en, description_es=desc_es,
        address=pd.get("address", ""), city=pd["city"], phone=pd["phone"], email="",
        website="https://www.in.gov/idoc/facilities/parole-districts/",
        eligibility="Individuals under Indiana parole supervision in assigned counties; family may contact for general district information.",
        eligibility_es="Personas bajo supervisión de libertad condicional en condados asignados; familiares pueden contactar para información general.",
        notes=pd["notes"],
        notes_es=pd["notes"],
        hours="Monday–Friday, 8:00 a.m.–4:30 p.m. local time",
        tags=f"parole|DOC|{pd['county'].lower()}|supervision",
        services="Parole supervision|HIRE coordinator referrals|Transitional healthcare navigation|Reentry partner connections",
        county=pd["county"], served_counties=sc, coverage=cov,
        _source="https://www.in.gov/idoc/facilities/parole-districts/", _source_type="government",
        _confidence="high" if pd.get("address") else "medium",
    )

# --- Community corrections ---
COMMUNITY_CORRECTIONS = [
    dict(name="Marion County Community Corrections", county="Marion", city="Indianapolis",
         phone="(317) 327-1111", address="140 East Washington Street",
         served="Marion", notes="Marion County CC administers work release, home detention, and reentry programs including Duvall Residential Center."),
    dict(name="Allen County Community Corrections", county="Allen", city="Fort Wayne",
         phone="(260) 449-7252", address="201 West Superior Street",
         served="Allen", notes="Executive Director Kim Churchward; court program and community-based sanctions."),
    dict(name="Lake County Community Corrections", county="Lake", city="Crown Point",
         phone="(219) 755-3850", address="2600 West 93rd Avenue",
         served="Lake", notes="Operates work release and community-based correctional programs for Lake County."),
    dict(name="Vanderburgh County Community Corrections", county="Vanderburgh", city="Evansville",
         phone="(812) 424-9821", address="27 Pasco Avenue",
         served="Vanderburgh", notes="Coordinates with Evansville PD4 for southwest Indiana community supervision and reentry."),
    dict(name="Hamilton County Community Corrections", county="Hamilton", city="Noblesville",
         phone="(317) 244-3144", address="727 Moon Road",
         served="Hamilton", notes="Served through Re-Entry PD1 region; contact for Hamilton County referral pathways."),
    dict(name="St. Joseph County Community Corrections", county="St. Joseph", city="South Bend",
         phone="(574) 234-8121", address="227 South Main Street",
         served="St. Joseph", notes="North-central Indiana community corrections; contact county office for program intake."),
    dict(name="Elkhart County Community Corrections", county="Elkhart", city="Goshen",
         phone="(574) 234-8121", address="",
         served="Elkhart", notes="Elkhart County programs coordinated through regional partners; verify intake on county website."),
    dict(name="Clark County Community Corrections", county="Clark", city="Jeffersonville",
         phone="(812) 945-4123", address="3303 Plaza Drive",
         served="Clark", notes="Southeast Indiana community corrections served through ILS New Albany regional network."),
    dict(name="Madison County Community Corrections", county="Madison", city="Anderson",
         phone="(317) 631-9410", address="1200 Madison Avenue",
         served="Madison", notes="Madison County community corrections and reentry partners coordinated through central Indiana network."),
    dict(name="Tippecanoe County Community Corrections", county="Tippecanoe", city="Lafayette",
         phone="(765) 423-5327", address="8 North 3rd Street",
         served="Tippecanoe", notes="West-central Indiana community corrections programs; contact county office for referrals."),
    dict(name="Vigo County Community Corrections", county="Vigo", city="Terre Haute",
         phone="(812) 235-0606", address="700 South State Road 46",
         served="Vigo", notes="Wabash Valley community corrections coordinated with Terre Haute PD10."),
    dict(name="Hendricks County Community Corrections", county="Hendricks", city="Plainfield",
         phone="(317) 244-3144", address="727 Moon Road",
         served="Hendricks", notes="Served through Re-Entry PD1; home detention and community transition programs."),
    dict(name="Johnson County Community Corrections", county="Johnson", city="Franklin",
         phone="(317) 244-3144", address="727 Moon Road",
         served="Johnson", notes="Served through Re-Entry PD1 region covering south-central metro Indianapolis counties."),
    dict(name="Monroe County Community Corrections", county="Monroe", city="Bloomington",
         phone="(812) 339-7668", address="100 South College Avenue",
         served="Monroe", notes="Monroe County community-based correctional programs and reentry partner coordination."),
    dict(name="Porter County Community Corrections", county="Porter", city="Valparaiso",
         phone="(219) 738-6040", address="7863 Broadway",
         served="Porter", notes="Northwest Indiana community corrections served through Lake/Merrillville regional network."),
]

for cc in COMMUNITY_CORRECTIONS:
    desc_en = (
        f"County-administered community corrections program in {cc['county']} County providing intermediate sanctions, "
        "work release, home detention, and reentry coordination for justice-involved individuals referred by courts or IDOC. "
        "Referral required through court or correctional system—not walk-in enrollment for most programs."
    )
    desc_es = (
        f"Programa de correcciones comunitarias administrado por el condado en {cc['county']} que ofrece sanciones intermedias, "
        "libertad en el hogar y coordinación de reinserción para personas referidas por tribunales o el IDOC. "
        "Se requiere referencia por el sistema judicial o correccional."
    )
    add(
        name=cc["name"], category="probation-parole", region=f"{cc['city']} / {cc['county']} County",
        description=desc_en, description_es=desc_es,
        address=cc.get("address", ""), city=cc["city"], phone=cc["phone"], email="",
        website="https://www.in.gov/idoc/community-corrections/community-corrections-and-justice-reinvestment-grants/grant-entity-contacts/",
        eligibility=f"Justice-involved {cc['county']} County residents referred by courts, prosecutors, or IDOC; program-specific offense criteria apply.",
        eligibility_es=f"Residentes de {cc['county']} referidos por tribunales, fiscales o IDOC; aplican criterios específicos por programa.",
        notes=cc["notes"],
        notes_es=cc["notes"],
        hours="Monday–Friday business hours; contact county office",
        tags=f"community-corrections|{cc['county'].lower()}|referral-required|reentry",
        services="Work release|Home detention|Intermediate sanctions|Reentry coordination|Community supervision",
        county=cc["county"], served_counties=cc["served"], coverage="single",
        _source="https://www.in.gov/idoc/community-corrections/community-corrections-and-justice-reinvestment-grants/grant-entity-contacts/",
        _source_type="government", _confidence="high" if cc.get("address") else "medium",
    )

# --- Extras (no CEO Indianapolis — use Goodwill/WorkOne) ---
EXTRAS = [
    dict(name="Gleaners Food Bank of Indiana", category="food-nutrition", region="Indianapolis",
         phone="(317) 925-0191", website="https://www.gleaners.org", address="3737 Waldemere Avenue", city="Indianapolis",
         county="Marion", cov="multi", served="Marion|Hamilton|Hancock|Johnson|Shelby|Boone|Hendricks|Morgan",
         desc="Central Indiana regional food bank connecting low-income residents including returning citizens to pantry network and SNAP application assistance."),
    dict(name="Second Harvest Food Bank of East Central Indiana", category="food-nutrition", region="Muncie",
         phone="(765) 287-8698", website="https://www.curehunger.org", address="6621 North Old State Road 3", city="Muncie",
         county="Delaware", cov="multi", served="Delaware|Madison|Blackford|Jay|Randolph|Henry|Wayne",
         desc="East central Indiana food bank providing pantry referrals and nutrition support for low-income residents including reentry populations."),
    dict(name="Tri-State Food Bank", category="food-nutrition", region="Evansville",
         phone="(812) 425-0775", website="https://www.tristatefoodbank.org", address="2504 Lynch Road", city="Evansville",
         county="Vanderburgh", cov="multi", served="Vanderburgh|Warrick|Posey|Gibson|Pike|Daviess",
         desc="Southwest Indiana food bank warehouse distributing food to pantries and agencies serving returning citizens and low-income families."),
    dict(name="Community Harvest Food Bank", category="food-nutrition", region="Fort Wayne",
         phone="(260) 447-3696", website="https://www.communityharvest.org", address="1010 North Coliseum Boulevard", city="Fort Wayne",
         county="Allen", cov="multi", served="Allen|Adams|DeKalb|Huntington|Noble|Steuben|Wells|Whitley",
         desc="Northeast Indiana food bank connecting residents to emergency food and partner pantry network across nine counties."),
    dict(name="Goodwill of Central & Southern Indiana", category="employment", region="Indianapolis",
         phone="(317) 524-4313", website="https://www.goodwillindy.org", address="1635 West Michigan Street", city="Indianapolis",
         county="Marion", cov="multi", served="Marion|Johnson|Hancock|Hendricks|Boone|Hamilton|Shelby|Morgan",
         desc="Goodwill employment services including New Beginnings program for individuals with barriers to employment including justice-involved Hoosiers."),
    dict(name="Goodwill New Beginnings", category="employment", region="Indianapolis",
         phone="(317) 524-3956", website="https://www.goodwillindy.org/employment-services/", address="1635 West Michigan Street", city="Indianapolis",
         county="Marion", cov="single", served="Marion",
         desc="Goodwill program connecting individuals with employment barriers including criminal records to job training and employer placement in central Indiana."),
    dict(name="WorkOne Indy", category="employment", region="Indianapolis",
         phone="(317) 798-0335", website="https://employindy.org/workoneindy/", address="4410 North Shadeland Avenue", city="Indianapolis",
         county="Marion", cov="single", served="Marion",
         desc="Marion County workforce center providing career coaching, training referrals, and job placement for justice-involved job seekers."),
    dict(name="WorkOne — Fort Wayne", category="employment", region="Fort Wayne",
         phone="(260) 745-3555", website="https://www.in.gov/dwd/workone/", address="201 East Rudisill Boulevard", city="Fort Wayne",
         county="Allen", cov="single", served="Allen",
         desc="Allen County WorkOne center connecting job seekers to training, employer services, and unemployment navigation in northeast Indiana."),
    dict(name="WorkOne — Evansville", category="employment", region="Evansville",
         phone="(812) 424-4473", website="https://www.in.gov/dwd/workone/region-11/", address="4600 Washington Avenue, Suite 113", city="Evansville",
         county="Vanderburgh", cov="single", served="Vanderburgh",
         desc="Vanderburgh County WorkOne providing employment services and career navigation for southwest Indiana job seekers."),
    dict(name="Eskenazi Health Connections", category="healthcare", region="Indianapolis",
         phone="(317) 880-7666", website="https://eskenazihealth.edu", address="720 Eskenazi Avenue", city="Indianapolis",
         county="Marion", cov="single", served="Marion",
         desc="Eskenazi Health patient navigation line connecting Marion County residents to primary care, specialty services, and behavioral health appointments."),
    dict(name="PACE — Public Advocates in Community re-Entry", category="reentry-organizations", region="Indianapolis",
         phone="(317) 612-6800", website="https://www.paceindy.org", address="1314 North Meridian Street", city="Indianapolis",
         county="Marion", cov="single", served="Marion",
         desc="Indianapolis reentry CBO providing employment, benefits navigation, mental health recovery support, and Recovery Works liaison services for felony-impacted individuals."),
    dict(name="Horizon House", category="reentry-organizations", region="Indianapolis",
         phone="(317) 423-8909", website="https://www.horizonhouse.cc", address="1033 East Washington Street", city="Indianapolis",
         county="Marion", cov="single", served="Marion",
         desc="Indianapolis day center and Coordinated Entry hub connecting homeless individuals including returning citizens to housing, employment, and health services."),
    dict(name="Wheeler Mission", category="housing", region="Indianapolis",
         phone="(317) 635-3575", website="https://wheelermission.org", address="245 North Delaware Street", city="Indianapolis",
         county="Marion", cov="single", served="Marion",
         desc="Indianapolis faith-based shelter and recovery housing provider serving men and women experiencing homelessness including ex-offender reentry programs."),
    dict(name="HVAF of Indiana", category="veterans", region="Indianapolis",
         phone="(317) 951-0688", website="https://hvafofindiana.org", address="964 North Pennsylvania Street", city="Indianapolis",
         county="Marion", cov="statewide", served="",
         desc="Veterans housing and employment services including VA GPD transitional housing and supportive services for justice-involved veterans statewide."),
    dict(name="Indiana Department of Health — Vital Records", category="id-documentation", region="Statewide",
         phone="(317) 233-2700", website="https://www.in.gov/health/vital-records/", address="2 North Meridian Street", city="Indianapolis",
         county="Marion", cov="statewide", served="",
         desc="State vital records office for ordering birth certificates and death records needed for ID, benefits, and employment applications after release."),
    dict(name="Indiana Department of Education — Adult Education", category="education", region="Statewide",
         phone="(877) 644-6338", website="https://www.in.gov/doe/students/indiana-adult-education/", address="115 West Washington Street", city="Indianapolis",
         county="Marion", cov="statewide", served="",
         desc="State resource connecting Indiana adults including returning citizens to HSE/GED, adult diploma, and skills training at local adult education sites."),
    dict(name="IndyGo — Reduced Fare Program", category="transportation", region="Indianapolis",
         phone="(317) 635-3344", website="https://www.indygo.net", address="1501 West Washington Street", city="Indianapolis",
         county="Marion", cov="single", served="Marion",
         desc="Indianapolis public transit reduced-fare programs helping low-income Marion County residents access bus transportation to work and appointments."),
    dict(name="Citilink — Fort Wayne Public Transit", category="transportation", region="Fort Wayne",
         phone="(260) 432-4546", website="https://www.fwcitilink.com", address="801 Leesburg Road", city="Fort Wayne",
         county="Allen", cov="single", served="Allen",
         desc="Fort Wayne public transit system with reduced-fare options for eligible low-income Allen County riders including returning citizens."),
    dict(name="MET Evansville — Public Transit", category="transportation", region="Evansville",
         phone="(812) 435-6192", website="https://www.evansville.in.gov/met", address="100 Main Street", city="Evansville",
         county="Vanderburgh", cov="single", served="Vanderburgh",
         desc="Evansville public transit providing bus service and reduced-fare programs for Vanderburgh County residents accessing employment and services."),
    dict(name="St. Vincent de Paul — Indianapolis", category="basic-needs", region="Indianapolis",
         phone="(317) 687-0169", website="https://www.svdpcindy.org", address="1201 East Maryland Street", city="Indianapolis",
         county="Marion", cov="single", served="Marion",
         desc="Catholic charity providing clothing, furniture, utility assistance, and basic needs support for low-income Marion County residents."),
    dict(name="Dayspring Center — Family Shelter", category="family-children", region="Indianapolis",
         phone="(317) 635-6789", website="https://www.dayspringcenter.org", address="1537 Central Avenue", city="Indianapolis",
         county="Marion", cov="single", served="Marion",
         desc="Indianapolis family emergency shelter serving parents with children experiencing homelessness including families reuniting after incarceration."),
]

for e in EXTRAS:
    add(
        name=e["name"], category=e["category"], region=e.get("region", e.get("city", "")),
        description=e["desc"],
        description_es=e["desc"].replace("connecting", "conectando").replace("providing", "proporcionando").replace("Indianapolis", "Indianápolis").replace("Fort Wayne", "Fort Wayne").replace("low-income", "de bajos ingresos").replace("returning citizens", "ciudadanos que regresan"),
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
from indiana_phase4_expansion import register_phase4
register_phase4(add)

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
