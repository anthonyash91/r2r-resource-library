#!/usr/bin/env python3
"""Generate illinois-resources.csv and illinois-research-log.csv.

RESOURCES_UUID_PREFIX comment d6000001
"""
import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES_PATH = ROOT / "data" / "illinois-resources.csv"
LOG_PATH = ROOT / "data" / "illinois-research-log.csv"
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

add(
    name='IDOC — Reentry Programs & Services', category='state-agency', region='Statewide',
    description='The Illinois Department of Corrections Reentry Programs division coordinates statewide reentry services including Reentry Summits, the Incarcerated Veterans Transition Program, transitional housing units, and community provider partnerships for prisoners, parolees, and probationers. IDOC connects returning citizens to housing, employment, treatment, and benefits resources through parole agents and published program directories—not a walk-in crisis line.',
    description_es='IDOC — Reentry Programs & Services coordina servicios de reinserción y recursos estatales para residentes de Illinois, incluidas personas con antecedentes penales que reconstruyen estabilidad después de la encarcelación. Contacte el programa para confirmar pasos de admisión y documentos requeridos.',
    address='1301 Concordia Court', city='Springfield', phone='217-558-2200', email='', website='https://idoc.illinois.gov/programs/reentry.html',
    eligibility='Illinois residents meeting program requirements; criminal record generally not a barrier to information and referral services.',
    eligibility_es='Residentes de Illinois que cumplan requisitos del programa; los antecedentes penales generalmente no son barrera para información y referencias.',
    notes='Verify current hours at https://idoc.illinois.gov/programs/reentry.html or call 217-558-2200.',
    notes_es='Verifique horarios actuales en https://idoc.illinois.gov/programs/reentry.html o llame al 217-558-2200.',
    hours='Contact for current hours',
    tags='statewide|illinois|reentry|state-agency',
    services='Information and referral|Partner referrals|Reentry navigation',
    county='Sangamon', served_counties='', coverage='statewide',
    _source='https://idoc.illinois.gov/programs/reentry.html', _source_type='government', _confidence='high',
)
add(
    name='ABE — Application for Benefits Eligibility', category='financial-assistance', region='Statewide',
    description='ABE is Illinois\'s official statewide portal for applying for and managing Medicaid, SNAP food assistance, TANF cash benefits, and child care subsidies through IDHS. Justice-involved individuals can apply for health coverage and food support after release; county Family Community Resource Centers assist with verification and redetermination.',
    description_es='ABE — Application for Benefits Eligibility coordina servicios de reinserción y recursos estatales para residentes de Illinois, incluidas personas con antecedentes penales que reconstruyen estabilidad después de la encarcelación. Contacte el programa para confirmar pasos de admisión y documentos requeridos.',
    address='', city='', phone='1-800-843-6154', email='', website='https://abe.illinois.gov',
    eligibility='Illinois residents meeting program requirements; criminal record generally not a barrier to information and referral services.',
    eligibility_es='Residentes de Illinois que cumplan requisitos del programa; los antecedentes penales generalmente no son barrera para información y referencias.',
    notes='Verify current hours at https://abe.illinois.gov or call 1-800-843-6154.',
    notes_es='Verifique horarios actuales en https://abe.illinois.gov o llame al 1-800-843-6154.',
    hours='Contact for current hours',
    tags='statewide|illinois|reentry|financial-assistance',
    services='Information and referral|Partner referrals|Reentry navigation',
    county='', served_counties='', coverage='statewide',
    _source='https://abe.illinois.gov', _source_type='government', _confidence='high',
)
add(
    name='211 Illinois', category='state-agency', region='Statewide',
    description='211 Illinois is a free statewide information and referral service connecting Illinois residents to health and human services including housing, food, utilities, employment, and crisis support. United Way-supported navigators help callers find local programs by need and ZIP code. 211 Illinois is a referral line—not a direct-service provider.',
    description_es='211 Illinois coordina servicios de reinserción y recursos estatales para residentes de Illinois, incluidas personas con antecedentes penales que reconstruyen estabilidad después de la encarcelación. Contacte el programa para confirmar pasos de admisión y documentos requeridos.',
    address='', city='', phone='211', email='', website='https://search.211illinois.org',
    eligibility='Illinois residents meeting program requirements; criminal record generally not a barrier to information and referral services.',
    eligibility_es='Residentes de Illinois que cumplan requisitos del programa; los antecedentes penales generalmente no son barrera para información y referencias.',
    notes='Verify current hours at https://search.211illinois.org or call 211.',
    notes_es='Verifique horarios actuales en https://search.211illinois.org o llame al 211.',
    hours='Contact for current hours',
    tags='statewide|illinois|reentry|state-agency',
    services='Information and referral|Partner referrals|Reentry navigation',
    county='', served_counties='', coverage='statewide',
    _source='https://search.211illinois.org', _source_type='government', _confidence='high',
)
add(
    name='IDHS — Benefits & Family Services Overview', category='financial-assistance', region='Statewide',
    description='Illinois Department of Human Services administers SNAP, Medicaid, TANF, and child care assistance through Family Community Resource Centers in every county and the ABE online portal. IDHS Pre-Release Program accepts SNAP and medical applications from approved IDOC facilities within ten days of release.',
    description_es='IDHS — Benefits & Family Services Overview coordina servicios de reinserción y recursos estatales para residentes de Illinois, incluidas personas con antecedentes penales que reconstruyen estabilidad después de la encarcelación. Contacte el programa para confirmar pasos de admisión y documentos requeridos.',
    address='100 S. Grand Avenue East', city='Springfield', phone='1-800-843-6154', email='', website='https://www.dhs.state.il.us/page.aspx?item=29725',
    eligibility='Illinois residents meeting program requirements; criminal record generally not a barrier to information and referral services.',
    eligibility_es='Residentes de Illinois que cumplan requisitos del programa; los antecedentes penales generalmente no son barrera para información y referencias.',
    notes='Verify current hours at https://www.dhs.state.il.us/page.aspx?item=29725 or call 1-800-843-6154.',
    notes_es='Verifique horarios actuales en https://www.dhs.state.il.us/page.aspx?item=29725 o llame al 1-800-843-6154.',
    hours='Contact for current hours',
    tags='statewide|illinois|reentry|financial-assistance',
    services='Information and referral|Partner referrals|Reentry navigation',
    county='Sangamon', served_counties='', coverage='statewide',
    _source='https://www.dhs.state.il.us/page.aspx?item=29725', _source_type='government', _confidence='high',
)
add(
    name='Illinois Legal Aid Online', category='legal-aid', region='Statewide',
    description='Illinois Legal Aid Online is a statewide legal information portal providing plain-language guides, court forms, and self-help tools for housing, benefits, family law, and record relief. Helps residents understand civil legal options and connect to free attorneys through Legal Aid Chicago, Land of Lincoln, and Prairie State Legal Services.',
    description_es='Illinois Legal Aid Online coordina servicios de reinserción y recursos estatales para residentes de Illinois, incluidas personas con antecedentes penales que reconstruyen estabilidad después de la encarcelación. Contacte el programa para confirmar pasos de admisión y documentos requeridos.',
    address='', city='Chicago', phone='', email='', website='https://www.illinoislegalaid.org',
    eligibility='Illinois residents meeting program requirements; criminal record generally not a barrier to information and referral services.',
    eligibility_es='Residentes de Illinois que cumplan requisitos del programa; los antecedentes penales generalmente no son barrera para información y referencias.',
    notes='Verify current hours at https://www.illinoislegalaid.org or call .',
    notes_es='Verifique horarios actuales en https://www.illinoislegalaid.org o llame al .',
    hours='Contact for current hours',
    tags='statewide|illinois|reentry|legal-aid',
    services='Information and referral|Partner referrals|Reentry navigation',
    county='Cook', served_counties='', coverage='statewide',
    _source='https://www.illinoislegalaid.org', _source_type='government', _confidence='high',
)
add(
    name='CARPLS — Statewide Legal Aid Hotline', category='legal-aid', region='Cook County',
    description='CARPLS provides coordinated telephone legal advice and referrals for low-income Illinois residents with civil legal problems including eviction, benefits denials, and record-related matters. Serves as intake hub for Cook County with referrals to regional legal aid providers statewide—not criminal defense.',
    description_es='CARPLS — Statewide Legal Aid Hotline coordina servicios de reinserción y recursos estatales para residentes de Illinois, incluidas personas con antecedentes penales que reconstruyen estabilidad después de la encarcelación. Contacte el programa para confirmar pasos de admisión y documentos requeridos.',
    address='120 S. LaSalle Street', city='Chicago', phone='312-738-9200', email='', website='https://www.carpls.org',
    eligibility='Illinois residents meeting program requirements; criminal record generally not a barrier to information and referral services.',
    eligibility_es='Residentes de Illinois que cumplan requisitos del programa; los antecedentes penales generalmente no son barrera para información y referencias.',
    notes='Verify current hours at https://www.carpls.org or call 312-738-9200.',
    notes_es='Verifique horarios actuales en https://www.carpls.org o llame al 312-738-9200.',
    hours='Contact for current hours',
    tags='statewide|illinois|reentry|legal-aid',
    services='Information and referral|Partner referrals|Reentry navigation',
    county='Cook', served_counties='', coverage='statewide',
    _source='https://www.carpls.org', _source_type='government', _confidence='high',
)
add(
    name='IDES — Re-Entry Employment Service Program', category='employment', region='Statewide',
    description='Illinois Department of Employment Security Re-Entry Employment Service Program connects justice-involved job seekers to career coaching, skills training, and employer partnerships through Illinois workNet American Job Centers. Staff help remove record-related barriers and coordinate federal bonding and tax credit information for fair-chance hiring.',
    description_es='IDES — Re-Entry Employment Service Program coordina servicios de reinserción y recursos estatales para residentes de Illinois, incluidas personas con antecedentes penales que reconstruyen estabilidad después de la encarcelación. Contacte el programa para confirmar pasos de admisión y documentos requeridos.',
    address='100 W. Randolph Street', city='Chicago', phone='800-320-9513', email='', website='https://www.ides.illinois.gov/idesreentry.html',
    eligibility='Illinois residents meeting program requirements; criminal record generally not a barrier to information and referral services.',
    eligibility_es='Residentes de Illinois que cumplan requisitos del programa; los antecedentes penales generalmente no son barrera para información y referencias.',
    notes='Verify current hours at https://www.ides.illinois.gov/idesreentry.html or call 800-320-9513.',
    notes_es='Verifique horarios actuales en https://www.ides.illinois.gov/idesreentry.html o llame al 800-320-9513.',
    hours='Contact for current hours',
    tags='statewide|illinois|reentry|employment',
    services='Information and referral|Partner referrals|Reentry navigation',
    county='Cook', served_counties='', coverage='statewide',
    _source='https://www.ides.illinois.gov/idesreentry.html', _source_type='government', _confidence='high',
)
add(
    name='Illinois workNet — Statewide Portal', category='employment', region='Statewide',
    description='Illinois workNet is the statewide workforce portal connecting job seekers—including justice-involved Illinoisans—to American Job Center locations, career coaching, training referrals, and job postings in every Local Workforce Innovation Area. Core AJC services are free for job seekers statewide.',
    description_es='Illinois workNet — Statewide Portal coordina servicios de reinserción y recursos estatales para residentes de Illinois, incluidas personas con antecedentes penales que reconstruyen estabilidad después de la encarcelación. Contacte el programa para confirmar pasos de admisión y documentos requeridos.',
    address='', city='Springfield', phone='877-342-7533', email='', website='https://www.illinoisworknet.com',
    eligibility='Illinois residents meeting program requirements; criminal record generally not a barrier to information and referral services.',
    eligibility_es='Residentes de Illinois que cumplan requisitos del programa; los antecedentes penales generalmente no son barrera para información y referencias.',
    notes='Verify current hours at https://www.illinoisworknet.com or call 877-342-7533.',
    notes_es='Verifique horarios actuales en https://www.illinoisworknet.com o llame al 877-342-7533.',
    hours='Contact for current hours',
    tags='statewide|illinois|reentry|employment',
    services='Information and referral|Partner referrals|Reentry navigation',
    county='Sangamon', served_counties='', coverage='statewide',
    _source='https://www.illinoisworknet.com', _source_type='government', _confidence='high',
)
add(
    name='988 Suicide & Crisis Lifeline — Illinois', category='healthcare', region='Statewide',
    description='Free confidential 24/7 crisis support for people experiencing mental health emergencies, suicidal thoughts, or substance use crises. Trained specialists provide immediate support and can connect callers to local mobile crisis teams in Illinois. Available to anyone—not reentry-specific but essential for justice-involved individuals in crisis.',
    description_es='988 Suicide & Crisis Lifeline — Illinois coordina servicios de reinserción y recursos estatales para residentes de Illinois, incluidas personas con antecedentes penales que reconstruyen estabilidad después de la encarcelación. Contacte el programa para confirmar pasos de admisión y documentos requeridos.',
    address='', city='', phone='988', email='', website='https://988lifeline.org',
    eligibility='Illinois residents meeting program requirements; criminal record generally not a barrier to information and referral services.',
    eligibility_es='Residentes de Illinois que cumplan requisitos del programa; los antecedentes penales generalmente no son barrera para información y referencias.',
    notes='Verify current hours at https://988lifeline.org or call 988.',
    notes_es='Verifique horarios actuales en https://988lifeline.org o llame al 988.',
    hours='Contact for current hours',
    tags='statewide|illinois|reentry|healthcare',
    services='Information and referral|Partner referrals|Reentry navigation',
    county='', served_counties='', coverage='statewide',
    _source='https://988lifeline.org', _source_type='government', _confidence='high',
)
add(
    name='New Leaf Illinois — Record Relief Network', category='legal-aid', region='Statewide',
    description='New Leaf Illinois is a statewide network of legal aid organizations helping eligible Illinois residents seal or clear criminal records under state law. Navigators connect callers to free legal representation through partner organizations for expungement and sealing—not active criminal defense cases.',
    description_es='New Leaf Illinois — Record Relief Network coordina servicios de reinserción y recursos estatales para residentes de Illinois, incluidas personas con antecedentes penales que reconstruyen estabilidad después de la encarcelación. Contacte el programa para confirmar pasos de admisión y documentos requeridos.',
    address='', city='Chicago', phone='855-963-9532', email='', website='https://www.newleafillinois.org',
    eligibility='Illinois residents meeting program requirements; criminal record generally not a barrier to information and referral services.',
    eligibility_es='Residentes de Illinois que cumplan requisitos del programa; los antecedentes penales generalmente no son barrera para información y referencias.',
    notes='Verify current hours at https://www.newleafillinois.org or call 855-963-9532.',
    notes_es='Verifique horarios actuales en https://www.newleafillinois.org o llame al 855-963-9532.',
    hours='Contact for current hours',
    tags='statewide|illinois|reentry|legal-aid',
    services='Information and referral|Partner referrals|Reentry navigation',
    county='Cook', served_counties='', coverage='statewide',
    _source='https://www.newleafillinois.org', _source_type='government', _confidence='high',
)
add(
    name='IL-AFLAN — Illinois Armed Forces Legal Aid Network', category='veterans', region='Statewide',
    description='IL-AFLAN provides free civil legal assistance to Illinois veterans, service members, and families including justice-involved veterans navigating discharge upgrades, VA benefits, housing, and record-related civil matters. Hotline connects callers to pro bono attorneys—not VA medical emergency services.',
    description_es='IL-AFLAN — Illinois Armed Forces Legal Aid Network coordina servicios de reinserción y recursos estatales para residentes de Illinois, incluidas personas con antecedentes penales que reconstruyen estabilidad después de la encarcelación. Contacte el programa para confirmar pasos de admisión y documentos requeridos.',
    address='', city='Chicago', phone='855-452-3526', email='', website='https://www.ilaflan.org',
    eligibility='Illinois residents meeting program requirements; criminal record generally not a barrier to information and referral services.',
    eligibility_es='Residentes de Illinois que cumplan requisitos del programa; los antecedentes penales generalmente no son barrera para información y referencias.',
    notes='Verify current hours at https://www.ilaflan.org or call 855-452-3526.',
    notes_es='Verifique horarios actuales en https://www.ilaflan.org o llame al 855-452-3526.',
    hours='Contact for current hours',
    tags='statewide|illinois|reentry|veterans',
    services='Information and referral|Partner referrals|Reentry navigation',
    county='Cook', served_counties='', coverage='statewide',
    _source='https://www.ilaflan.org', _source_type='government', _confidence='high',
)
add(
    name='SAMHSA National Helpline', category='substance-use-treatment', region='Statewide',
    description='Free confidential 24/7 treatment referral and information service for individuals and families facing mental health or substance use disorders. Provides referrals to local treatment facilities and community organizations in Illinois and nationwide. Spanish-language support available through trained specialists.',
    description_es='SAMHSA National Helpline coordina servicios de reinserción y recursos estatales para residentes de Illinois, incluidas personas con antecedentes penales que reconstruyen estabilidad después de la encarcelación. Contacte el programa para confirmar pasos de admisión y documentos requeridos.',
    address='', city='', phone='800-662-4357', email='', website='https://www.samhsa.gov/find-help/national-helpline',
    eligibility='Illinois residents meeting program requirements; criminal record generally not a barrier to information and referral services.',
    eligibility_es='Residentes de Illinois que cumplan requisitos del programa; los antecedentes penales generalmente no son barrera para información y referencias.',
    notes='Verify current hours at https://www.samhsa.gov/find-help/national-helpline or call 800-662-4357.',
    notes_es='Verifique horarios actuales en https://www.samhsa.gov/find-help/national-helpline o llame al 800-662-4357.',
    hours='Contact for current hours',
    tags='statewide|illinois|reentry|substance-use-treatment',
    services='Information and referral|Partner referrals|Reentry navigation',
    county='', served_counties='', coverage='statewide',
    _source='https://www.samhsa.gov/find-help/national-helpline', _source_type='government', _confidence='high',
)
add(
    name='FindTreatment.gov — Illinois Provider Search', category='substance-use-treatment', region='Statewide',
    description='SAMHSA\'s online treatment locator helping Illinois residents find substance use and mental health treatment providers by location, service type, and payment options including Medicaid. Justice-involved individuals can search outpatient, residential, and MAT providers before or after release.',
    description_es='FindTreatment.gov — Illinois Provider Search coordina servicios de reinserción y recursos estatales para residentes de Illinois, incluidas personas con antecedentes penales que reconstruyen estabilidad después de la encarcelación. Contacte el programa para confirmar pasos de admisión y documentos requeridos.',
    address='', city='', phone='', email='', website='https://findtreatment.gov',
    eligibility='Illinois residents meeting program requirements; criminal record generally not a barrier to information and referral services.',
    eligibility_es='Residentes de Illinois que cumplan requisitos del programa; los antecedentes penales generalmente no son barrera para información y referencias.',
    notes='Verify current hours at https://findtreatment.gov or call .',
    notes_es='Verifique horarios actuales en https://findtreatment.gov o llame al .',
    hours='Contact for current hours',
    tags='statewide|illinois|reentry|substance-use-treatment',
    services='Information and referral|Partner referrals|Reentry navigation',
    county='', served_counties='', coverage='statewide',
    _source='https://findtreatment.gov', _source_type='government', _confidence='high',
)
add(
    name='IDHS — Pre-Release Benefits Program', category='financial-assistance', region='Statewide',
    description='IDHS Pre-Release Program allows approved IDOC facilities to submit SNAP and medical assistance applications within ten days of a person\'s release from incarceration, helping returning citizens establish food and health benefits before community reentry. Coordinated through facility reentry staff and county FCRC offices.',
    description_es='IDHS — Pre-Release Benefits Program coordina servicios de reinserción y recursos estatales para residentes de Illinois, incluidas personas con antecedentes penales que reconstruyen estabilidad después de la encarcelación. Contacte el programa para confirmar pasos de admisión y documentos requeridos.',
    address='100 S. Grand Avenue East', city='Springfield', phone='1-800-843-6154', email='', website='https://www.dhs.state.il.us/page.aspx?item=29725',
    eligibility='Illinois residents meeting program requirements; criminal record generally not a barrier to information and referral services.',
    eligibility_es='Residentes de Illinois que cumplan requisitos del programa; los antecedentes penales generalmente no son barrera para información y referencias.',
    notes='Verify current hours at https://www.dhs.state.il.us/page.aspx?item=29725 or call 1-800-843-6154.',
    notes_es='Verifique horarios actuales en https://www.dhs.state.il.us/page.aspx?item=29725 o llame al 1-800-843-6154.',
    hours='Contact for current hours',
    tags='statewide|illinois|reentry|financial-assistance',
    services='Information and referral|Partner referrals|Reentry navigation',
    county='Sangamon', served_counties='', coverage='statewide',
    _source='https://www.dhs.state.il.us/page.aspx?item=29725', _source_type='government', _confidence='high',
)
add(
    name='Illinois Department of Healthcare and Family Services — Medicaid', category='healthcare', region='Statewide',
    description='Illinois HFS administers Medicaid, All Kids, and managed care programs statewide helping returning citizens verify enrollment and connect to health plans after ABE application. Criminal record is generally not a barrier to Medicaid eligibility for income-qualified Illinois residents.',
    description_es='Illinois Department of Healthcare and Family Services — Medicaid coordina servicios de reinserción y recursos estatales para residentes de Illinois, incluidas personas con antecedentes penales que reconstruyen estabilidad después de la encarcelación. Contacte el programa para confirmar pasos de admisión y documentos requeridos.',
    address='201 S. LaSalle Street', city='Chicago', phone='800-226-0768', email='', website='https://www.hfs.illinois.gov',
    eligibility='Illinois residents meeting program requirements; criminal record generally not a barrier to information and referral services.',
    eligibility_es='Residentes de Illinois que cumplan requisitos del programa; los antecedentes penales generalmente no son barrera para información y referencias.',
    notes='Verify current hours at https://www.hfs.illinois.gov or call 800-226-0768.',
    notes_es='Verifique horarios actuales en https://www.hfs.illinois.gov o llame al 800-226-0768.',
    hours='Contact for current hours',
    tags='statewide|illinois|reentry|healthcare',
    services='Information and referral|Partner referrals|Reentry navigation',
    county='Cook', served_counties='', coverage='statewide',
    _source='https://www.hfs.illinois.gov', _source_type='government', _confidence='high',
)
add(
    name='Illinois Secretary of State — Driver & State ID Services', category='id-documentation', region='Statewide',
    description='Illinois Secretary of State provides REAL ID-compliant driver\'s licenses, state identification cards, and credential reinstatement at branch offices statewide. Reentry partners help returning citizens gather proof of identity and residency documents required for employment and ABE benefits after incarceration.',
    description_es='Illinois Secretary of State — Driver & State ID Services coordina servicios de reinserción y recursos estatales para residentes de Illinois, incluidas personas con antecedentes penales que reconstruyen estabilidad después de la encarcelación. Contacte el programa para confirmar pasos de admisión y documentos requeridos.',
    address='', city='Springfield', phone='888-SOS-ILLINO', email='', website='https://www.ilsos.gov',
    eligibility='Illinois residents meeting program requirements; criminal record generally not a barrier to information and referral services.',
    eligibility_es='Residentes de Illinois que cumplan requisitos del programa; los antecedentes penales generalmente no son barrera para información y referencias.',
    notes='Verify current hours at https://www.ilsos.gov or call 888-SOS-ILLINO.',
    notes_es='Verifique horarios actuales en https://www.ilsos.gov o llame al 888-SOS-ILLINO.',
    hours='Contact for current hours',
    tags='statewide|illinois|reentry|id-documentation',
    services='Information and referral|Partner referrals|Reentry navigation',
    county='Sangamon', served_counties='', coverage='statewide',
    _source='https://www.ilsos.gov', _source_type='government', _confidence='high',
)
add(
    name='Illinois Department of Veterans Affairs', category='veterans', region='Statewide',
    description='Illinois Department of Veterans Affairs connects veterans and families to federal VA benefits, state veteran programs, and county Veterans Service Officers statewide including justice-involved veterans navigating healthcare enrollment and benefits restoration after incarceration.',
    description_es='Illinois Department of Veterans Affairs coordina servicios de reinserción y recursos estatales para residentes de Illinois, incluidas personas con antecedentes penales que reconstruyen estabilidad después de la encarcelación. Contacte el programa para confirmar pasos de admisión y documentos requeridos.',
    address='833 S. Spring Street', city='Springfield', phone='800-437-9824', email='', website='https://www.illinois.gov/veterans',
    eligibility='Illinois residents meeting program requirements; criminal record generally not a barrier to information and referral services.',
    eligibility_es='Residentes de Illinois que cumplan requisitos del programa; los antecedentes penales generalmente no son barrera para información y referencias.',
    notes='Verify current hours at https://www.illinois.gov/veterans or call 800-437-9824.',
    notes_es='Verifique horarios actuales en https://www.illinois.gov/veterans o llame al 800-437-9824.',
    hours='Contact for current hours',
    tags='statewide|illinois|reentry|veterans',
    services='Information and referral|Partner referrals|Reentry navigation',
    county='Sangamon', served_counties='', coverage='statewide',
    _source='https://www.illinois.gov/veterans', _source_type='government', _confidence='high',
)
add(
    name='Illinois Housing Development Authority', category='housing', region='Statewide',
    description='Illinois Housing Development Authority provides affordable housing resources, rental assistance programs, and the Illinois Housing Search locator for low-income residents including returning citizens seeking income-restricted rental units and emergency rental assistance when programs are open.',
    description_es='Illinois Housing Development Authority coordina servicios de reinserción y recursos estatales para residentes de Illinois, incluidas personas con antecedentes penales que reconstruyen estabilidad después de la encarcelación. Contacte el programa para confirmar pasos de admisión y documentos requeridos.',
    address='111 E. Wacker Drive', city='Chicago', phone='312-386-8000', email='', website='https://www.ihda.org',
    eligibility='Illinois residents meeting program requirements; criminal record generally not a barrier to information and referral services.',
    eligibility_es='Residentes de Illinois que cumplan requisitos del programa; los antecedentes penales generalmente no son barrera para información y referencias.',
    notes='Verify current hours at https://www.ihda.org or call 312-386-8000.',
    notes_es='Verifique horarios actuales en https://www.ihda.org o llame al 312-386-8000.',
    hours='Contact for current hours',
    tags='statewide|illinois|reentry|housing',
    services='Information and referral|Partner referrals|Reentry navigation',
    county='Cook', served_counties='', coverage='statewide',
    _source='https://www.ihda.org', _source_type='government', _confidence='high',
)
add(
    name='Illinois Criminal Justice Information Authority', category='reentry-organizations', region='Statewide',
    description='ICJIA coordinates research, grant-funded reentry initiatives, and policy resources connecting Illinois communities to evidence-based reentry services through provider networks statewide—a navigation and policy hub, not an emergency shelter or cash assistance provider.',
    description_es='Illinois Criminal Justice Information Authority coordina servicios de reinserción y recursos estatales para residentes de Illinois, incluidas personas con antecedentes penales que reconstruyen estabilidad después de la encarcelación. Contacte el programa para confirmar pasos de admisión y documentos requeridos.',
    address='300 W. Adams Street', city='Chicago', phone='312-793-8550', email='', website='https://www.icjia.state.il.us',
    eligibility='Illinois residents meeting program requirements; criminal record generally not a barrier to information and referral services.',
    eligibility_es='Residentes de Illinois que cumplan requisitos del programa; los antecedentes penales generalmente no son barrera para información y referencias.',
    notes='Verify current hours at https://www.icjia.state.il.us or call 312-793-8550.',
    notes_es='Verifique horarios actuales en https://www.icjia.state.il.us o llame al 312-793-8550.',
    hours='Contact for current hours',
    tags='statewide|illinois|reentry|reentry-organizations',
    services='Information and referral|Partner referrals|Reentry navigation',
    county='Cook', served_counties='', coverage='statewide',
    _source='https://www.icjia.state.il.us', _source_type='government', _confidence='high',
)
add(
    name='Community Action Association of Illinois', category='basic-needs', region='Statewide',
    description='Illinois Community Action Association connects low-income residents to local Community Action Agencies in every county offering utility assistance, weatherization, emergency aid, and case management. Returning citizens can locate county CAA offices for basic needs support after release.',
    description_es='Community Action Association of Illinois coordina servicios de reinserción y recursos estatales para residentes de Illinois, incluidas personas con antecedentes penales que reconstruyen estabilidad después de la encarcelación. Contacte el programa para confirmar pasos de admisión y documentos requeridos.',
    address='2610 N. Walnut Street', city='Springfield', phone='217-528-8400', email='', website='https://www.icaaonline.org',
    eligibility='Illinois residents meeting program requirements; criminal record generally not a barrier to information and referral services.',
    eligibility_es='Residentes de Illinois que cumplan requisitos del programa; los antecedentes penales generalmente no son barrera para información y referencias.',
    notes='Verify current hours at https://www.icaaonline.org or call 217-528-8400.',
    notes_es='Verifique horarios actuales en https://www.icaaonline.org o llame al 217-528-8400.',
    hours='Contact for current hours',
    tags='statewide|illinois|reentry|basic-needs',
    services='Information and referral|Partner referrals|Reentry navigation',
    county='Sangamon', served_counties='', coverage='statewide',
    _source='https://www.icaaonline.org', _source_type='government', _confidence='high',
)

# --- Phase 3: Statewide specialty ---

add(
    name='Illinois Department of Human Services — Behavioral Health', category='healthcare', region='Statewide',
    description='IDHS coordinates publicly funded behavioral health and substance use disorder services through regional provider networks and Medicaid managed care plans helping justice-involved Illinoisans connect to treatment after release; for crisis call 988. Returning citizens should call ahead to confirm walk-in hours, referral requirements, and documents needed before visiting.', description_es='IDHS coordinates publicly funded behavioral health and substance use disorder services through regional provider networks and Medicaid managed care plans helping justice-involved Illinoisans connect to treatment after release; for crisis call 988. Los ciudadanos que regresan deben llamar con anticipación para confirmar horarios y documentos necesarios.',
    address='100 S. Grand Avenue East', city='Springfield', phone='217-782-3300', email='', website='https://www.dhs.state.il.us/page.aspx?item=29725',
    eligibility='Open to Illinois residents in the program service area; justice-involved individuals generally welcome.',
    eligibility_es='Abierto a residentes de Illinois en el área de servicio; personas con antecedentes penales generalmente son bienvenidas.',
    notes='Call 217-782-3300 to confirm current intake hours.',
    notes_es='Llame al 217-782-3300 para confirmar horarios de admisión.',
    hours='Contact for current hours', tags='illinois|reentry|sangamon', services='',
    county='Sangamon', served_counties='', coverage='statewide',
    _source='https://www.dhs.state.il.us/page.aspx?item=29725', _source_type='government', _confidence='high',
)
add(
    name='Illinois Coalition Against Domestic Violence', category='family-children', region='Statewide',
    description='Illinois Coalition Against Domestic Violence connects survivors to local domestic violence programs, shelter, and legal advocacy statewide including family members affected by partner violence during reentry; hotline available 24/7. Returning citizens should call ahead to confirm walk-in hours, referral requirements, and documents needed before visiting.', description_es='Illinois Coalition Against Domestic Violence connects survivors to local domestic violence programs, shelter, and legal advocacy statewide including family members affected by partner violence during reentry; hotline available 24/7. Los ciudadanos que regresan deben llamar con anticipación para confirmar horarios y documentos necesarios.',
    address='', city='Springfield', phone='877-863-6338', email='', website='https://www.ilcadv.org',
    eligibility='Open to Illinois residents in the program service area; justice-involved individuals generally welcome.',
    eligibility_es='Abierto a residentes de Illinois en el área de servicio; personas con antecedentes penales generalmente son bienvenidas.',
    notes='Call 877-863-6338 to confirm current intake hours.',
    notes_es='Llame al 877-863-6338 para confirmar horarios de admisión.',
    hours='Contact for current hours', tags='illinois|reentry|sangamon', services='',
    county='Sangamon', served_counties='', coverage='statewide',
    _source='https://www.ilcadv.org', _source_type='government', _confidence='high',
)
add(
    name='Illinois Adult Education — State Program Locator', category='education', region='Statewide',
    description='Illinois State Board of Education adult education directory connects returning citizens to local GED, high school equivalency, and English language programs at community colleges and community sites in every county. Returning citizens should call ahead to confirm walk-in hours, referral requirements, and documents needed before visiting.', description_es='Illinois State Board of Education adult education directory connects returning citizens to local GED, high school equivalency, and English language programs at community colleges and community sites in every county. Los ciudadanos que regresan deben llamar con anticipación para confirmar horarios y documentos necesarios.',
    address='', city='Springfield', phone='217-785-8774', email='', website='https://www2.illinois.gov/education/Pages/Adult-Education.aspx',
    eligibility='Open to Illinois residents in the program service area; justice-involved individuals generally welcome.',
    eligibility_es='Abierto a residentes de Illinois en el área de servicio; personas con antecedentes penales generalmente son bienvenidas.',
    notes='Call 217-785-8774 to confirm current intake hours.',
    notes_es='Llame al 217-785-8774 para confirmar horarios de admisión.',
    hours='Contact for current hours', tags='illinois|reentry|sangamon', services='',
    county='Sangamon', served_counties='', coverage='statewide',
    _source='https://www2.illinois.gov/education/Pages/Adult-Education.aspx', _source_type='government', _confidence='high',
)
add(
    name='Illinois Department of Transportation — Public Transit Resources', category='transportation', region='Statewide',
    description='Illinois DOT provides information on public transit systems statewide including reduced-fare programs for seniors, people with disabilities, and low-income riders returning citizens may use to reach employment and appointments. Returning citizens should call ahead to confirm walk-in hours, referral requirements, and documents needed before visiting.', description_es='Illinois DOT provides information on public transit systems statewide including reduced-fare programs for seniors, people with disabilities, and low-income riders returning citizens may use to reach employment and appointments. Los ciudadanos que regresan deben llamar con anticipación para confirmar horarios y documentos necesarios.',
    address='', city='Springfield', phone='217-782-7820', email='', website='https://www.idot.illinois.gov',
    eligibility='Open to Illinois residents in the program service area; justice-involved individuals generally welcome.',
    eligibility_es='Abierto a residentes de Illinois en el área de servicio; personas con antecedentes penales generalmente son bienvenidas.',
    notes='Call 217-782-7820 to confirm current intake hours.',
    notes_es='Llame al 217-782-7820 para confirmar horarios de admisión.',
    hours='Contact for current hours', tags='illinois|reentry|sangamon', services='',
    county='Sangamon', served_counties='', coverage='statewide',
    _source='https://www.idot.illinois.gov', _source_type='government', _confidence='high',
)
add(
    name='Illinois Peer Recovery Support Services', category='peer-support', region='Statewide',
    description='Illinois Certification Board maintains certified peer recovery specialists who provide mentoring and recovery coaching for justice-involved individuals in treatment and reentry programs statewide. Returning citizens should call ahead to confirm walk-in hours, referral requirements, and documents needed before visiting.', description_es='Illinois Certification Board maintains certified peer recovery specialists who provide mentoring and recovery coaching for justice-involved individuals in treatment and reentry programs statewide. Los ciudadanos que regresan deben llamar con anticipación para confirmar horarios y documentos necesarios.',
    address='401 E. Sangamon Avenue', city='Springfield', phone='217-528-7335', email='', website='https://www.illinoiscertificationboard.org',
    eligibility='Open to Illinois residents in the program service area; justice-involved individuals generally welcome.',
    eligibility_es='Abierto a residentes de Illinois en el área de servicio; personas con antecedentes penales generalmente son bienvenidas.',
    notes='Call 217-528-7335 to confirm current intake hours.',
    notes_es='Llame al 217-528-7335 para confirmar horarios de admisión.',
    hours='Contact for current hours', tags='illinois|reentry|sangamon', services='',
    county='Sangamon', served_counties='', coverage='statewide',
    _source='https://www.illinoiscertificationboard.org', _source_type='government', _confidence='high',
)
from illinois_phase4_expansion import register_phase4
register_phase4(add)

from phase3b_gapfill import register_phase3b_illinois
register_phase3b_illinois(add, ENTRIES)

from illinois_pass2_expansion import register_pass2
register_pass2(add)

from illinois_phase5_depth_expansion import register_phase5
register_phase5(add)

from illinois_rural_depth_expansion import register_rural_depth
register_rural_depth(add)

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
