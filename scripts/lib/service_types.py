"""Canonical service type taxonomy and normalization for resource CSVs."""
from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

_ALIASES_PATH = Path(__file__).with_name("service_aliases.json")

from .service_canonical_consolidation import CANONICAL_CONSOLIDATION, consolidate_canonical

# ---------------------------------------------------------------------------
# Legacy canonical labels (rules may still emit these before consolidation)
# ---------------------------------------------------------------------------

LEGACY_CANONICAL_SERVICES: tuple[str, ...] = (
    "12-step programs",
    "Accessibility services",
    "Addiction medicine",
    "Addiction recovery support",
    "Addiction treatment referrals",
    "Adult education",
    "Adult literacy and ESL",
    "Advocacy",
    "Affordable housing",
    "Aftercare planning",
    "Alternative to incarceration",
    "Anger management",
    "Application assistance",
    "Apprenticeships",
    "Banking access",
    "Basic needs assistance",
    "Behavioral health services",
    "Benefits advocacy",
    "Benefits appeals",
    "Benefits enrollment",
    "Benefits navigation",
    "Bereavement support",
    "Birth certificate assistance",
    "Budgeting and financial coaching",
    "Bus pass assistance",
    "Career counseling",
    "Career training and certifications",
    "Case management",
    "Cash assistance (TANF)",
    "Child care assistance",
    "Child support services",
    "Children's services",
    "Chronic care management",
    "Civil legal representation",
    "Civil rights advocacy",
    "Clothing assistance",
    "Coalition coordination",
    "Community meals",
    "Community supervision",
    "Computer and digital literacy",
    "Consumer legal help",
    "Co-parenting support",
    "Counseling",
    "Court advocacy",
    "Court compliance support",
    "Crisis services",
    "Dental services",
    "Detox services",
    "Developmental disability services",
    "Document assistance",
    "Domestic violence support",
    "Driver's license services",
    "Emergency financial assistance",
    "Emergency food assistance",
    "Emergency shelter",
    "Employment assistance",
    "Expungement assistance",
    "Family reunification support",
    "Food pantry access",
    "GED and high school equivalency",
    "Health insurance enrollment",
    "Homeownership assistance",
    "Housing legal aid",
    "Housing navigation",
    "ID assistance",
    "Information and referral",
    "Interview preparation",
    "Job placement",
    "Job readiness training",
    "Landlord outreach",
    "Legal aid referrals",
    "MAT referrals",
    "Medicaid enrollment",
    "Mental health referrals",
    "Outpatient treatment",
    "Parenting services",
    "Partner referrals",
    "Peer support",
    "Primary medical care",
    "Probation and parole supervision",
    "Reentry navigation",
    "Rent and utility assistance",
    "Residential treatment",
    "Resume help",
    "Senior services",
    "Skills training",
    "Sliding-fee care",
    "SNAP enrollment",
    "Social Security assistance",
    "Sober living housing",
    "Spiritual support",
    "Substance use counseling",
    "Substance use screening",
    "Substance use treatment",
    "Support groups",
    "Supportive housing",
    "Transitional housing",
    "Transportation assistance",
    "Transitional healthcare navigation",
    "Trauma-informed counseling",
    "Unemployment assistance",
    "VA benefits navigation",
    "Veterans services",
    "Vocational rehabilitation",
    "Vital records services",
    "Voting rights assistance",
    "Women's health services",
    "Work release programs",
    "Workforce development",
    "Youth mentoring",
)

# User-facing filter labels after merging near-duplicates
CANONICAL_SERVICES: tuple[str, ...] = tuple(
    sorted({consolidate_canonical(label) for label in LEGACY_CANONICAL_SERVICES})
)

LEGACY_CANONICAL_SET = frozenset(LEGACY_CANONICAL_SERVICES)
CANONICAL_SET = frozenset(CANONICAL_SERVICES)

# ---------------------------------------------------------------------------
# Rule-based classification (first match wins; more specific rules first)
# ---------------------------------------------------------------------------

_RULE_SPECS: tuple[tuple[str, str], ...] = (
    # Exact standalone overrides
    ("Partner referrals", r"^community support$"),
    ("Partner referrals", r"^referrals$"),
    ("Partner referrals", r"^resource referrals$"),
    ("Partner referrals", r"^resource-specific services$"),
    ("Partner referrals", r"^community referrals$"),
    ("Partner referrals", r"^agency referrals$"),
    ("Partner referrals", r"^benefits referrals$"),
    ("Partner referrals", r"^benefits office referrals$"),
    ("Partner referrals", r"^case referrals$"),
    ("Partner referrals", r"^specialty referrals$"),
    ("Partner referrals", r"^training referrals$"),
    ("Partner referrals", r"^career referrals$"),
    ("Partner referrals", r"^career training referrals$"),
    ("Partner referrals", r"^skills training referrals$"),
    ("Partner referrals", r"^workforce certification referrals$"),
    ("Partner referrals", r"^workforce referrals$"),
    ("Partner referrals", r"^training program referrals$"),
    ("Partner referrals", r"^training program connections$"),
    ("Partner referrals", r"^employer placement referrals$"),
    ("Partner referrals", r"^employer placement connections$"),
    ("Partner referrals", r"^employer connections$"),
    ("Partner referrals", r"^employer partnerships$"),
    ("Partner referrals", r"^employer outreach$"),
    ("Partner referrals", r"^employer networking$"),
    ("Partner referrals", r"^employer recruiting support$"),
    ("Partner referrals", r"^employer recruitment support$"),
    ("Partner referrals", r"^employer services$"),
    ("Partner referrals", r"^employer job matching$"),
    ("Partner referrals", r"^second-chance employer connections$"),
    ("Partner referrals", r"^coalition partner referrals$"),
    ("Partner referrals", r"^community partner referrals$"),
    ("Partner referrals", r"^community partner connections$"),
    ("Partner referrals", r"^community partner networking$"),
    ("Partner referrals", r"^community partnership navigation$"),
    ("Partner referrals", r"^community resource connections$"),
    ("Partner referrals", r"^community resource navigation$"),
    ("Partner referrals", r"^community resource referrals$"),
    ("Partner referrals", r"^community reentry referrals$"),
    ("Partner referrals", r"^community recovery navigation$"),
    ("Partner referrals", r"^community agency networking$"),
    ("Partner referrals", r"^community connections$"),
    ("Partner referrals", r"^community integration support$"),
    ("Partner referrals", r"^community reintegration$"),
    ("Partner referrals", r"^community donations$"),
    ("Partner referrals", r"^community events$"),
    ("Partner referrals", r"^community organizing$"),
    ("Partner referrals", r"^community planning support$"),
    ("Partner referrals", r"^community-based classes$"),
    ("Partner referrals", r"^congregation network$"),
    ("Partner referrals", r"^congregation partnerships$"),
    ("Partner referrals", r"^church partnerships$"),
    ("Partner referrals", r"^volunteer network$"),
    ("Partner referrals", r"^sponsor connections$"),
    ("Partner referrals", r"^sponsorship connections$"),
    ("Partner referrals", r"^alumni network$"),
    ("Partner referrals", r"^242 partner agency network$"),
    ("Partner referrals", r"^service provider connections$"),
    ("Partner referrals", r"^service provider network$"),
    ("Partner referrals", r"^agency partnerships$"),
    ("Partner referrals", r"^agency collaboration$"),
    ("Partner referrals", r"^agency voucher programs$"),
    ("Partner referrals", r"^drc partner referrals$"),
    ("Partner referrals", r"^drc referrals$"),
    ("Partner referrals", r"^dcbs referrals$"),
    ("Partner referrals", r"^dcbs office referrals$"),
    ("Partner referrals", r"^dhs referrals$"),
    ("Partner referrals", r"^county office referrals$"),
    ("Partner referrals", r"^regional office referrals$"),
    ("Partner referrals", r"^regional office appointments$"),
    ("Partner referrals", r"^regional partner networking$"),
    ("Partner referrals", r"^regional resource coordination$"),
    ("Partner referrals", r"^regional satellite outreach$"),
    ("Partner referrals", r"^regional field office services$"),
    ("Partner referrals", r"^regional coalition referrals$"),
    ("Partner referrals", r"^regional reentry coordinator referrals$"),
    ("Partner referrals", r"^district office coordination$"),
    ("Partner referrals", r"^district office referral$"),
    ("Partner referrals", r"^central office information$"),
    ("Partner referrals", r"^branch location lookup$"),
    ("Partner referrals", r"^county program locator$"),
    ("Partner referrals", r"^satellite office network$"),
    ("Partner referrals", r"^appointment scheduling$"),
    ("Partner referrals", r"^appointment scheduling referral$"),
    ("Partner referrals", r"^referral services$"),
    ("Partner referrals", r"^referral form guidance$"),
    ("Partner referrals", r"^referral and transportation coordination$"),
    ("Partner referrals", r"^referral-based suiting appointments$"),
    ("Partner referrals", r"^referrals to reentry services$"),
    ("Partner referrals", r"^referral to reentry supports$"),
    ("Partner referrals", r"^statewide referrals$"),
    ("Partner referrals", r"^statewide intake coordination$"),
    ("Partner referrals", r"^statewide intake routing$"),
    ("Partner referrals", r"^statewide specialty court directory$"),
    ("Partner referrals", r"^statewide vacancy navigation$"),
    ("Partner referrals", r"^statewide clinic events$"),
    ("Partner referrals", r"^resource navigation$"),
    ("Partner referrals", r"^resource networking$"),
    ("Partner referrals", r"^resource platform support$"),
    ("Partner referrals", r"^resource sharing$"),
    ("Partner referrals", r"^resource coordination$"),
    ("Partner referrals", r"^information and referral$"),
    ("Partner referrals", r"^social service referrals$"),
    ("Partner referrals", r"^social service navigation$"),
    ("Partner referrals", r"^continuing care and employment referrals$"),
    ("Partner referrals", r"^crisis referrals$"),
    ("Partner referrals", r"^crisis resource connections$"),
    ("Partner referrals", r"^crisis intervention referrals$"),
    ("Partner referrals", r"^crisis support referrals$"),
    ("Partner referrals", r"^warm line referrals$"),
    ("Partner referrals", r"^weatherization referrals$"),
    ("Partner referrals", r"^utility and housing referrals$"),
    ("Partner referrals", r"^employment and housing referrals$"),
    ("Partner referrals", r"^housing referrals$"),
    ("Partner referrals", r"^shelter referrals$"),
    ("Partner referrals", r"^transitional housing referrals$"),
    ("Partner referrals", r"^supportive housing referrals$"),
    ("Partner referrals", r"^emergency shelter referrals$"),
    ("Partner referrals", r"^emergency shelter connections$"),
    ("Partner referrals", r"^emergency resource navigation$"),
    ("Partner referrals", r"^emergency food resource navigation$"),
    ("Partner referrals", r"^community meal program referrals$"),
    ("Partner referrals", r"^food pantry referrals$"),
    ("Partner referrals", r"^furniture referrals$"),
    ("Partner referrals", r"^career coaching referrals$"),
    ("Partner referrals", r"^career training referrals$"),
    ("Partner referrals", r"^reentry program referrals$"),
    ("Partner referrals", r"^reentry coalition referrals$"),
    ("Partner referrals", r"^reentry case management referrals$"),
    ("Partner referrals", r"^reentry partner referrals$"),
    ("Partner referrals", r"^reentry partner connections$"),
    ("Partner referrals", r"^reentry resource connections$"),
    ("Partner referrals", r"^reentry resource referrals$"),
    ("Partner referrals", r"^reentry referrals$"),
    ("Partner referrals", r"^reentry service navigation$"),
    ("Partner referrals", r"^reentry resource information$"),
    ("Partner referrals", r"^reentry resource fairs$"),
    ("Partner referrals", r"^reentry information sharing$"),
    ("Partner referrals", r"^tdoc partner networking$"),
    ("Partner referrals", r"^dress for success partner referrals$"),
    ("Partner referrals", r"^certified low-fee checking account referrals$"),
    ("Partner referrals", r"^legal aid referrals$"),
    ("Partner referrals", r"^local legal aid finder$"),
    ("Partner referrals", r"^county legal aid routing$"),
    ("Partner referrals", r"^expungement clinic referrals$"),
    ("Partner referrals", r"^counseling referrals$"),
    ("Partner referrals", r"^behavioral health referrals$"),
    ("Partner referrals", r"^mental health referrals$"),
    ("Partner referrals", r"^substance use referrals$"),
    ("Partner referrals", r"^substance use and mental health referrals$"),
    ("Partner referrals", r"^addiction treatment referrals$"),
    ("Partner referrals", r"^treatment referrals$"),
    ("Partner referrals", r"^residential treatment referrals$"),
    ("Partner referrals", r"^peer support referrals$"),
    ("Partner referrals", r"^vjo specialist referrals$"),
    ("Partner referrals", r"^va benefits referrals$"),
    ("Partner referrals", r"^va healthcare referrals$"),
    ("Partner referrals", r"^va housing program referrals$"),
    ("Partner referrals", r"^employment services referral$"),
    ("Partner referrals", r"^esl and literacy referrals$"),
    ("Partner referrals", r"^testing referral information$"),
    ("Partner referrals", r"^telehealth provider search$"),
    ("Partner referrals", r"^treatment facility search$"),
    ("Partner referrals", r"^treatment facility search by zip code$"),
    ("Partner referrals", r"^regional mh authority locator$"),
    ("Partner referrals", r"^cmhc locator assistance$"),
    ("Partner referrals", r"^regional cmhc hub$"),
    ("Partner referrals", r"^regional vso network$"),
    ("Partner referrals", r"^driver services center locator$"),
    ("Partner referrals", r"^certified residence directory$"),
    ("Partner referrals", r"^area meeting directories$"),
    ("Partner referrals", r"^board contact routing$"),
    ("Partner referrals", r"^unclaimed property search$"),
    ("Partner referrals", r"^voter registration partnerships$"),
    ("Partner referrals", r"^voter registration resources$"),
    ("Partner referrals", r"^connection to local va resources$"),
    ("Partner referrals", r"^cincinnati cross-river connections$"),
    ("Partner referrals", r"^mydrive online portal$"),
    ("Partner referrals", r"^online case management portal$"),
    ("Partner referrals", r"^text-based navigation$"),
    ("Partner referrals", r"^text and chat support$"),
    ("Partner referrals", r"^spanish-language helpline support$"),
    ("Partner referrals", r"^spanish-language services$"),
    ("Partner referrals", r"^virtual and in-person instruction$"),
    ("Partner referrals", r"^technology programs$"),
    ("Partner referrals", r"^small business incubation$"),
    ("Partner referrals", r"^business and employer services$"),
    ("Partner referrals", r"^economic mobility programming$"),
    ("Partner referrals", r"^wellness programs$"),
    ("Partner referrals", r"^character development$"),
    ("Partner referrals", r"^advisory board meetings$"),
    ("Partner referrals", r"^donation center services$"),
    ("Partner referrals", r"^donation intake$"),
    ("Partner referrals", r"^will-call pickup$"),
    ("Partner referrals", r"^stand-down events$"),
    ("Partner referrals", r"^workshops$"),
    ("Partner referrals", r"^scholarship information$"),
    ("Partner referrals", r"^certified clinic information$"),
    ("Partner referrals", r"^tenncare provider$"),
    ("Partner referrals", r"^tenncare services$"),
    ("Partner referrals", r"^walk-in service$"),
    ("Partner referrals", r"^walk-in reporting \(call to confirm\)$"),
    ("Partner referrals", r"^street outreach$"),
    ("Partner referrals", r"^mobile outreach$"),
    ("Partner referrals", r"^outreach$"),
    ("Partner referrals", r"^networking$"),
    ("Partner referrals", r"^linkages$"),
    ("Partner referrals", r"^linkage$"),
    ("Partner referrals", r"^connections$"),
    ("Partner referrals", r"^coordination$"),
    ("Partner referrals", r"^network coordination$"),
    ("Partner referrals", r"^case coordination tools$"),
    ("Partner referrals", r"^community coordination$"),
    ("Partner referrals", r"^community control$"),
    ("Partner referrals", r"^community confinement$"),
    ("Partner referrals", r"^community recovery mentoring$"),
    ("Partner referrals", r"^community legal clinics$"),
    ("Partner referrals", r"^community support associate training$"),

    # Crisis (before generic counseling)
    ("Crisis services", r"crisis|988\b|24/7|24-7|mobile crisis|crisis line|crisis hotline|crisis helpline|crisis intervention|crisis counsel|crisis support|crisis stabil|crisis system|crisis utility|walk-in crisis|safe off the streets|crru residential crisis|suicide prevention|overdose|988 press 1 veteran|24/7 homeless veteran triage|24/7 referral helpline|benefits navigation hotline|same-day behavioral health urgent care"),

    # MAT (distinct from outpatient/residential)
    ("MAT referrals", r"\bmat referrals\b|medication-assisted treatment|\bmat\b"),

    # Medicaid / SNAP / TANF
    ("Medicaid enrollment", r"medicaid|tenncare|hoosier healthwise|\bhip\b|kynect medicaid|pre-release medicaid|medicaid billing|medicaid information|medicaid screening|medicaid and insurance|insurance and medicaid|combined benefits application with medicaid|snap and medicaid enrollment"),
    ("SNAP enrollment", r"\bsnap\b|food stamp|ebt card|nutrition assistance|kynect.*snap|snap food assistance|snap information|snap benefits|snap application"),
    ("Cash assistance (TANF)", r"\btanf\b|ktap|k-tap|cash assist|families first|snap and ktap"),

    # Benefits
    ("Benefits navigation", r"benefits nav|employment and benefits|reentry benefits|housing and benefits|kynect benefits|benefits connections|benefits counseling|benefits information|benefits account|benefits verification|coverage nav|social service nav"),
    ("Benefits enrollment", r"benefits enroll|benefits assistance|benefits application|benefits claims|benefits case management"),
    ("Benefits advocacy", r"benefits advoc|benefits appeals"),

    # VA
    ("VA benefits navigation", r"va benefits|veterans benefits nav|vjo |veterans justice outreach|veterans treatment court|988 press 1 veteran|va gpd|va health|va medical|va healthcare|va housing program|va treatment|va case management|va claims|va disability|connection to local va|transportation to va|vjo case coordination|vjo coordination|vjo outreach|va benefits linkage|va benefits and treatment|va medical care linkage|va treatment coordination|va treatment enrollment|va health care enrollment|va disability claims|vr&e chapter 31|veterans crisis line connection"),
    ("Veterans services", r"veterans service|veterans resource|veterans advocacy|veterans employment|veterans priority|veterans and disability|women veterans|stand-down|veterans specialty court|veterans high school|court and jail outreach to veterans|court and jail veteran identification|alternative sentencing for veterans|homeless veteran|veterans priority service"),

    # Resume / interview / career
    ("Resume help", r"resume|curriculum vitae|\bcv\b"),
    ("Interview preparation", r"interview prep|interview coach|interview help|interview workshop|interview assist"),
    ("Career counseling", r"career (coach|counsel|navig|advis|path|develop|service|center|connection|readiness|bridge|assessment|placement|referral|services|pathways|training pathways|technical)|american job center|workone|work ready certificate|work therapy program|comprehensive job seeker|recovery-informed career|employment reentry navigation|workforce reentry navigation|career-technical"),

    # Reentry (specific before generic referrals)
    ("Reentry navigation", r"reentry (nav|coord|outreach|planning|programming|support|application|information|case|health|peer|partner|resource|service|legal|coalition|coordinator|toolkit|court|service center|focused|program)|re-entry|re entry|restored citizen|jail to job|aspire pre-release|release bag|release-day|justice-involved|local reentry|county reentry|regional reentry|doc-contracted rsc|doc-affiliated|site reentry|workforce reentry|in-jail reentry|jail reentry|community reentry advocacy|reentry and family|reentry behavioral health|reentry health coverage|reentry peer workforce|reentry planning coordination|reentry program coordination|reentry resource coordination|reentry case coordination|reentry case navigation|reentry coalition meetings|reentry legal clinics|reentry-focused clinical|kentucky reentry toolkit|reentry service center oversight|reentry court\b|ged and jail to job"),

    # Expungement / legal
    ("Expungement assistance", r"expungement|record seal|clean slate|record relief|cqe application|cqe assist|drug felony eligibility|collateral consequence|criminal record barrier|automatic restoration|record sealing|free expungement|expungement clinic|expungement eligibility|expungement screening|expungement information|expungement help|expungement representation|attorney record review|select litigation against government licensing barriers|barrier relief assistance|barrier-reduction|criminal record employment support|background checks\b"),
    ("Civil legal representation", r"civil legal|free civil legal|civil representation|domestic violence legal|disaster legal|senior legal|legal representation|court representation|domestic violence protection|sexual assault forensic|protection order|consumer legal|county legal aid|housing legal aid|record relief legal|free civil legal services|domestic violence legal help|domestic violence legal aid"),
    ("Legal aid referrals", r"legal aid referral|legal aid finder|legal aid routing|legal clinic|community legal clinic|reentry legal clinics|county legal aid routing|local legal aid finder"),
    ("Consumer legal help", r"consumer law|consumer protection|consumer rights|consumer legal"),
    ("Housing legal aid", r"housing legal aid|tenant rights|tenant services"),
    ("Civil rights advocacy", r"civil right|voting rights educ|voter registration|civil rights restoration|black lung|workers' right|systemic barrier advocacy|advocacy\b|community reentry advocacy|civil rights cases|civil rights representation"),

    # Probation / parole / supervision
    ("Probation and parole supervision", r"probation|parole|supervision|community correction|community supervision|reporting appointment|reporting compliance|reporting requirement|check-in|compliance monitor|compliance support|conditional discharge|judicial supervision|officer case|case officer|capital region|eastern ky|western ky|lincoln trail|multi-county|ne kentucky|se ky|purchase region|rural reentry supervision|felony probation|doc supervision|community control monitoring|supervision policy|supervision status|supervision compliance|reporting and check-ins|scheduled reporting|walk-in reporting|weekly house accountability|structured programming|pretrial|pre-trial|court liaison|court form assistance|court compliance|treatment compliance monitoring|supervised substance use treatment|dui assessments|casey's law assessment|specialty court coordination|certified drug court|mental health court|drug court|statewide specialty court|work release programs|work release\b|alternative sentencing|alternative-to-incarceration|alternative to incarceration|corrections education|county jail|jail program|in-jail|college courses in prison|educational good-time|community confinement|community control\b|judicial case management|officer case management|case officer contact|case officer management|doc supervision coordination|compliant reporting|reporting appointments|multi-county probation|multi-county supervision|multi-county western|western kentucky intake|purchase region case management|se ky regional supervision|ne kentucky probation|eastern ky probation|eastern ky supervision|western ky probation|capital region supervision|lincoln trail region|felony probation and parole|community supervision compliance|community supervision support|supervision compliance support|rural county access points|satellite classes in|satellite outreach in"),

    # Peer / recovery / 12-step
    ("Peer support", r"peer support|peer mentor|peer recovery|certified peer|adult peer support|peer workforce|recovery coaching|community recovery mentor|peer mentorship|peer mentor support|peer support groups|peer support certification|phase i peer|certified peer specialists|certified peer support"),
    ("12-step programs", r"12-step|twelve.step|sober180"),
    ("Support groups", r"support groups\b|12-step support|12-step programming|12-step introduction|12-step recovery|group support"),
    ("Addiction recovery support", r"addiction recovery|addiction resource navigation|addiction recovery programming|recovery support|relapse prevention|aftercare planning|aftercare\b|continuing care|community recovery mentoring|sober living recovery program"),
    ("Addiction medicine", r"addiction medicine\b"),
    ("Addiction treatment referrals", r"addiction treatment referrals|treatment referrals|treatment vouchers|treatment facility|treatment coordination|findhelpnow|redline|substance use referrals|substance use and mental health referrals|warm line referrals"),

    # Substance use treatment tiers
    ("Detox services", r"detox\b|detox and residential"),
    ("Residential treatment", r"residential treatment|residential crisis|residential recovery program|residential substance use|residential recovery\b|women's residential treatment|women's residential recovery|crru residential|detox and residential treatment|detox and residential crisis|supervised substance use treatment|residential crisis stabilization"),
    ("Outpatient treatment", r"outpatient treatment|outpatient\b|\biop\b|intensive outpatient|substance use and iop|same-day behavioral"),
    ("Substance use treatment", r"substance use treatment|substance abuse treatment|substance use services|substance abuse programming|inpatient|court-referred treatment|substance use and mental health treatment compliance"),
    ("Substance use counseling", r"substance use counseling|substance use crisis support|substance use information"),
    ("Substance use screening", r"substance use screening|eligibility screening\b|dui assessments and education"),

    # Housing tiers
    ("Emergency shelter", r"emergency shelter|emergency men's shelter|emergency overnight|women's shelter|seasonal shelter|day shelter|shelter bed|shelter network|emergency shelter and meals|women and children's day shelter|safe off the streets entry|democratic self-run housing"),
    ("Transitional housing", r"transitional housing|transitional living|transitional reentry|residential reentry housing|residential transitional|women and children's housing|youth and adult housing|transitional housing for women"),
    ("Supportive housing", r"supportive housing|sober living|structured sober|sober housing|recovery residence|halfway|oxford house|women's recovery residence|structured sober living for men|sober living placement"),
    ("Affordable housing", r"affordable housing|section 8|county-based housing listings|statewide vacancy|coc funding navigation|housing listings"),
    ("Homeownership assistance", r"down payment assistance|homeownership|home buyer|homebuyer"),
    ("Rent and utility assistance", r"rent assist|rental assist|utility assist|utility bill|utility help|utility payment|emergency rent|utility and rent|subsidy payments|weatherization\b|crisis utility|utility and housing|emergency rent help|subsidy payments to utility vendors"),
    ("Housing navigation", r"housing nav|coordinated entry|rehousing|ssvf rapid rehousing|landlord outreach|housing case management|county-based housing|housing listings|regional food bank distribution|county-based pantry locator|emergency shelter network|emergency shelter bed reservations"),
    ("Landlord outreach", r"landlord outreach|employer outreach\b|tenant rights|tenant services"),

    # Food
    ("Food pantry access", r"food pantry|client-choice food|emergency food distribution|pantry locator|rural community food|regional food bank|county-based pantry|emergency food resource navigation|emergency food and clothing"),
    ("Community meals", r"community meal|daily meal|daily community meal|senior meal|daily weekly and monthly passes|children allowed"),

    # Employment / workforce
    ("Job placement", r"job placement|employment placement|employer placement|fair-chance job|second-chance job|ex-offender job|free job search|employer job matching|hiring event|job fair|labor exchange|work experience placements|employment services\b|employment assistance\b|employment navigation|fair-chance employment|site reentry employment|retention support|employer placement connections|free job search and placement|free job search assistance|employment services referral|employment and benefits links|employment barrier relief|employment reentry|work experience|internships\b|internship\b"),
    ("Job readiness training", r"job readiness|job search assistance|job search support|job training|job development|work readiness|case management and job readiness|workforce reentry support for women|job readiness workshops|job readiness training|skills assessment and intake|skills assessment\b|workforce program intake|workforce preparation|workforce readiness|work readiness\b|employment barrier|resume and placement|resume and skills workshops"),
    ("Workforce development", r"workforce develop|workforce education|workforce network|workforce pathway|workforce workshop|workforce training|workforce connection|workforce credentials|workforce certification|workforce bridge|workforce partnerships|workforce partnership|wioa|economic mobility|comprehensive job seeker|american job center|workone|business and employer|employer services\b|employer recruiting|employer recruitment|employer connections\b|employer partnerships\b|employer networking\b|employer job matching|second-chance employer|fair-chance employment navigation|employment and benefits navigation|employment and housing referrals|employment services\b|employment assistance\b|employment placement\b|employment navigation\b|employment reentry navigation|workforce reentry support|workforce reentry navigation|workforce and college transition|college and career readiness|college transition support|college transition\b|college placement prep|college enrollment pathway|workforce and college|career bridge programs|career-technical bridge|career-technical education|career-technical pathways|career training pathways|career training\b|career certifications|career placement|career readiness|career readiness support|career connections|career development|career pathways|career pathway counseling|career services\b|career center services|career assessment|career training referrals|career certifications|career-technical|technical certificates|technical training|trade certificates|training program connections|training program referrals|training referrals\b|certification prep|certification support|certification verification|skills certification|skills development|skills training\b|skills training referrals|skills assessment|skills workshop|workforce skills training|workforce certification pathways|workforce certification programs|workforce credential pathways|workforce certificates|workforce workshops|workforce education|workplace certification training|vocational certificates|vocational certifications|vocational skills training|vocational training and internships|technology workforce training|technology programs|welding training|culinary arts training|cdl preparation|apprenticeships\b|apprenticeship\b|internships\b|internship\b|work experience placements|scholarship information|ceu upload guidance|certified clinic information|virtual and in-person instruction|chromebook and stipend|college courses in prison|satellite classes|satellite outreach in|satellite class|education pathway|educational pathway|hoosier youth|youth build|youth employment programs|site reentry employment support|work therapy program|work ready certificate|vr&e chapter 31 employment|wioa training accounts|wioa training funding|wioa training referrals"),
    ("Career training and certifications", r"career train|career cert|career-tech|career technical|workforce cert|workforce credential|wioa|vocational cert|technical cert|trade cert|certification prep|certification support|certification verif|cdl prep|welding|culinary|apprenticeship|internship|college course|college enrollment|college transition|college placement|college and career|workforce and college|workforce bridge|workforce education|workforce certification|technical training|trade certificates|skills cert|ceu upload|certified clinic|training program|education pathway|satellite class|technology workforce|chromebook|scholarship|career-technical|vocational cert|vocational training|vocational certificates|workplace certification|workforce certification|workforce credential|workforce certificates|workforce skills|skills certification|skills development|skills training|skills workshop|skills assessment|certification prep|certification support|certification verification|cdl preparation|welding training|culinary arts|apprenticeships|internships|work experience|wioa training|vr&e|technical certificates|trade certificates|career certifications|career training|career bridge|career-technical bridge|career-technical education|career-technical pathways|career training pathways|career training referrals|workforce certification pathways|workforce certification programs|workforce credential pathways|workforce workshops|workforce skills training|workplace certification training|technology programs|technology workforce training|virtual and in-person instruction|chromebook and stipend incentives|college courses in prison|satellite classes|satellite outreach|education pathway|educational pathway|hoosier youth|youth build|youth employment|site reentry employment|work therapy|work ready certificate"),
    ("Vocational rehabilitation", r"vocational rehab|vocational service|vocational skill|vocational training|vocational assist|vr&e|chapter 31|vocational rehabilitation claims|vocational assistance and housing linkage|vocational certificates|vocational certifications|vocational skills training|vocational training and internships|vocational services\b"),
    ("Skills training", r"skills train|skills develop|skills assess|skills cert|skills workshop|computer training|digital literacy|technical training|trade cert|certification prep|certification support|welding|culinary|cdl prep|apprenticeship|digital and mobile|computer and digital|technology programs|technology workforce|workplace certification|skills certification|skills development|skills training|skills workshop|skills assessment|skills assessment and intake|digital literacy instruction|computer training|technology workforce training|workplace certification training|welding training|culinary arts training|cdl preparation|apprenticeships|certification prep|certification support|certification verification|technical training|trade certificates|technical certificates|skills certification|skills development|skills training|skills workshop|skills assessment|skills assessment and intake|ceu upload guidance|certified clinic information|virtual and in-person instruction|chromebook and stipend incentives|workforce skills training|workforce certification|workforce credential|workforce certificates|workforce workshops|workforce skills|workplace certification training|technology programs|technology workforce training|digital literacy instruction|computer training|digital and mobile banking|digital literacy\b|computer training\b|technology programs\b|technology workforce training\b|workplace certification training\b|skills certification\b|skills development\b|skills training\b|skills workshop\b|skills assessment\b|skills assessment and intake\b|certification prep\b|certification support\b|certification verification\b|technical training\b|trade certificates\b|technical certificates\b|welding training\b|culinary arts training\b|cdl preparation\b|apprenticeships\b|internships\b|work experience placements\b|scholarship information\b|ceu upload guidance\b|certified clinic information\b|virtual and in-person instruction\b|chromebook and stipend incentives\b|college courses in prison\b|satellite classes\b|satellite outreach in\b|satellite class\b|education pathway\b|educational pathway\b|hoosier youth\b|youth build\b|youth employment programs\b|site reentry employment support\b|work therapy program\b|work ready certificate\b|vr&e chapter 31 employment\b|wioa training accounts\b|wioa training funding\b|wioa training referrals\b|workforce certification pathways\b|workforce certification programs\b|workforce credential pathways\b|workforce certificates\b|workforce workshops\b|workforce skills training\b|workplace certification training\b|technology programs\b|technology workforce training\b|digital literacy instruction\b|computer training\b|digital and mobile banking\b|digital literacy\b|computer training\b|technology programs\b|technology workforce training\b|workplace certification training\b|skills certification\b|skills development\b|skills training\b|skills workshop\b|skills assessment\b|skills assessment and intake\b|certification prep\b|certification support\b|certification verification\b|technical training\b|trade certificates\b|technical certificates\b|welding training\b|culinary arts training\b|cdl preparation\b|apprenticeships\b|internships\b|work experience placements\b|scholarship information\b|ceu upload guidance\b|certified clinic information\b|virtual and in-person instruction\b|chromebook and stipend incentives\b|college courses in prison\b|satellite classes\b|satellite outreach in\b|satellite class\b|education pathway\b|educational pathway\b|hoosier youth\b|youth build\b|youth employment programs\b|site reentry employment support\b|work therapy program\b|work ready certificate\b|vr&e chapter 31 employment\b|wioa training accounts\b|wioa training funding\b|wioa training referrals\b|workforce certification pathways\b|workforce certification programs\b|workforce credential pathways\b|workforce certificates\b|workforce workshops\b|workforce skills training\b|workplace certification training\b|technology programs\b|technology workforce training\b|digital literacy instruction\b|computer training\b|digital and mobile banking\b"),
    ("Unemployment assistance", r"unemployment"),
    ("Employment assistance", r"employment assist|employment service|employment placement|employment navigation|labor|hiring|employment and benefits|employment barrier|employment reentry|employment services\b"),

    # Education
    ("GED and high school equivalency", r"ged |high school equivalency|adult diploma|adult high school|county jail ged|corrections education|educational good-time|in-jail.*ged|jail.*education|aspire pre-release|diploma program|adult diploma programs|adult diploma\b|county jail adult education|county jail programming|county jail g ed|corrections education in|veterans high school diploma"),
    ("Adult education", r"adult education|corrections education|county jail adult|college courses in prison|in-jail.*class|jail.*class|community-based classes|virtual and in-person instruction|early childhood education|head start|college enrollment|college transition|college placement|college courses|college and career|workforce and college|college transition support|college placement prep|college enrollment pathway|corrections education in county jails|corrections education in jails|corrections education in jails and prisons|county jail programming|in-jail reentry classes|satellite classes|education pathway|educational pathway|hoosier youth|youth build|youth employment|early childhood|head start and case management"),
    ("Adult literacy and ESL", r"adult literacy|\besl\b|english as a second|citizenship class|literacy|family literacy|college remediation|esl and|adult literacy and esl|esl classes|esl programs|esl and citizenship|esl and college|esl and family|esl and workforce|esl and literacy"),

    # Child / family
    ("Child care assistance", r"child care|childcare|ccap|daycare|child care cert|child care subsid|child care assistance\b|childcare assistance\b"),
    ("Parenting services", r"parenting|co-parenting|head start|early childhood|child advocacy|family reunification|reunification|foster|kinship|head start and case management"),
    ("Children's services", r"children's service|children's support|children's counsel|child support order|youth employment|youth mentor|youth and adult|child advocacy|children allowed|children's counseling|child support order establishment"),
    ("Youth mentoring", r"youth mentor|\bsoy\b|mentoring\b|spiritual mentorship|youth mentoring"),
    ("Family reunification support", r"family reunification|reunification|reunification resources|reunification support|foster|kinship"),
    ("Child support services", r"child support order|child support order establishment|wage withholding enforcement"),

    # Case management
    ("Case management", r"case manag|case coord|ryan white|care coord|evidence-based case|purchase region case|benefits case|housing case|judicial case|officer case|post-release case|online case management|care coordination|case management linkage|case management for low-income|career counseling and case management|head start and case management|housing case management|post-release case management|purchase region case management|reentry case management|benefits case management|ryan white case management|case management and job readiness|case management for low-income households|case management linkage|evidence-based case management|online case management portal|care coordination\b|care regardless of income|case coordination tools"),

    # Health
    ("Primary medical care", r"primary medical|uninsured patient|charity care|same-day behavioral|urgent care|specialty care|chronic care|chronic disease|women's health|dental|telehealth|testing\b|std|sti |medical care|health service|healthcare|health care|tenncare provider|clinic information|dental care|dental services|specialty care|chronic care management|chronic disease management|women's health services|women's health\b|dental services\b|dental care\b|testing coordination|testing support|testing fee waiver|std testing|sti testing|telehealth options|telehealth provider|same-day behavioral health urgent care|uninsured patient care|charity care\b|primary medical care\b|specialty care\b|chronic care\b|chronic disease management\b|chronic care management\b|women's health\b|dental\b|testing\b|std testing\b|sti testing and treatment\b|telehealth\b|medical\b|health services\b|healthcare\b|health care\b|clinic\b|tenncare services\b|tenncare provider\b|certified clinic information\b"),
    ("Sliding-fee care", r"sliding.fee|sliding scale|sliding-fee|sliding scale fees|sliding-fee scale|sliding-fee services|sliding-fee care\b|sliding scale\b|sliding-fee scale\b|sliding-fee services\b|sliding-fee care\b|sliding scale fees\b|sliding-fee\b|sliding fee scale\b|sliding fee\b|sliding-fee services\b|sliding-fee care\b|sliding scale fees\b|sliding-fee scale\b|sliding scale\b|sliding-fee\b|sliding fee scale\b|sliding fee\b|sliding-fee services\b|sliding-fee care\b|sliding scale fees\b|sliding-fee scale\b|sliding scale\b|sliding-fee\b|sliding fee scale\b|sliding fee\b|sliding-fee services\b|sliding-fee care\b|sliding scale fees\b|sliding-fee scale\b|sliding scale\b|care regardless of income"),
    ("Behavioral health services", r"behavioral health service|behavioral health coord|behavioral health support|mental health service|mental health support|psychiatric|psychological|therapy service|behavioral health\b|behavioral health coordination|behavioral health services\b|behavioral health support\b|mental health services\b|mental health support\b|reentry-focused clinical services|reentry behavioral health linkage|jail reentry behavioral health linkage|jail reentry mental health linkage|behavioral health coordination\b|behavioral health services\b|behavioral health support\b|mental health services\b|mental health support\b|psychiatric\b|psychological\b|therapy services\b|reentry-focused clinical\b|reentry behavioral health\b|jail reentry behavioral health\b|jail reentry mental health\b"),
    ("Mental health referrals", r"mental health referral|behavioral health referral|counseling referral|crisis referral|mental health referrals\b|behavioral health referrals\b|counseling referrals\b|crisis referrals\b|crisis intervention referrals\b|crisis support referrals\b|warm line referrals\b|substance use and mental health referrals\b|mental health referral\b|behavioral health referral\b|counseling referral\b|crisis referral\b|mental health referrals\b|behavioral health referrals\b|counseling referrals\b|crisis referrals\b|crisis intervention referrals\b|crisis support referrals\b|warm line referrals\b|substance use and mental health referrals\b"),
    ("Counseling", r"counseling|counselling|therapy\b|trauma counsel|trauma-informed|bereavement|grief|domestic violence counsel|children's counsel|family counsel|anger management|spanish-language counselor|counseling\b|therapy\b|trauma counseling|trauma-informed care|bereavement counseling|bereavement support|domestic violence counseling|children's counseling|family counseling|anger management\b|spanish-language counselors\b|counseling referrals\b|counseling\b|therapy\b|trauma counseling\b|trauma-informed care\b|bereavement counseling\b|bereavement support\b|domestic violence counseling\b|children's counseling\b|family counseling\b|anger management\b|spanish-language counselors\b"),
    ("Trauma-informed counseling", r"trauma-informed|trauma counseling|trauma counsel"),
    ("Bereavement support", r"bereavement|grief"),
    ("Health insurance enrollment", r"health insurance|health coverage|insurance enrollment|transitional healthcare|reentry health coverage|coverage navigation|transitional healthcare navigation|health insurance enrollment\b|health coverage navigation\b|insurance enrollment\b|transitional healthcare navigation\b|reentry health coverage navigation\b|coverage navigation\b|health insurance\b|health coverage\b|insurance enrollment\b|transitional healthcare\b|reentry health coverage\b|coverage navigation\b|transitional healthcare navigation\b|reentry health coverage navigation\b|health insurance enrollment\b|health coverage navigation\b|insurance enrollment\b|transitional healthcare navigation\b|reentry health coverage navigation\b|coverage navigation\b|combined benefits application with medicaid\b|medicaid and insurance billing\b|insurance and medicaid billing\b|medicaid and insurance\b|insurance and medicaid\b|medicaid billing assistance\b|billing assistance\b|claims assistance\b|redetermination assistance\b|benefits claims assistance\b|benefits verification\b|benefits account management\b"),

    # Documents / IDs
    ("Birth certificate assistance", r"birth certificate"),
    ("Vital records services", r"vital record|death cert|death record|death marriage divorce|marriage record|divorce record|vital records orders|vital records verification|death certificates\b|death record copies\b|death marriage divorce records\b|marriage records\b|divorce records\b|vital records\b|vital records orders\b|vital records verification\b|death certificates\b|death record copies\b|death marriage divorce records\b|marriage records\b|divorce records\b|vital records\b|vital records orders\b|vital records verification\b"),
    ("Document assistance", r"document|document upload|document navigation|document verification|document copies|document fees|ssn verification|document navigation\b|document upload assistance\b|document verification\b|document copies\b|document fees info\b|document assistance\b|document navigation\b|document upload\b|document verification\b|document copies\b|document fees\b|document assistance\b|document navigation\b|document upload\b|document verification\b|document copies\b|document fees\b|id and vital records assistance\b|id and birth certificate vouchers\b|webcheck services\b|testing fee waiver assistance\b|testing referral information\b|testing coordination\b|testing support\b|testing\b|automatic restoration verification\b|ssn and card information\b|ssn verification\b|social security card replacement\b|social security cards\b|ssn and card information\b|ssn verification\b|social security card replacement\b|social security cards\b|certified birth certificates\b|birth certificate orders\b|birth certificate issuance\b|birth certificates\b|birth certificate help\b|birth certificate assistance\b|birth certificate orders\b|birth certificate issuance\b|birth certificates\b|birth certificate help\b|birth certificate assistance\b"),
    ("ID assistance", r"\bid assist|\bid help|\bid application|state id card|state id issuance|state id assistance|identification assist|identification help|id and birth certificate|id and vital records|id application guidance|state id cards\b|state id issuance\b|state id assistance\b|id application guidance\b|id and birth certificate vouchers\b|id and vital records assistance\b|id assistance\b|id help\b|id application\b|state id\b|identification assist\b|identification help\b|id and birth certificate\b|id and vital records\b|id application guidance\b|state id cards\b|state id issuance\b|state id assistance\b|id application guidance\b|id and birth certificate vouchers\b|id and vital records assistance\b|id assistance\b|id help\b|id application\b|state id\b|identification assist\b|identification help\b"),
    ("Driver's license services", r"driver's license|driver service|license reinstate|mydrive|driver services center|suspension requirement|driver's licenses\b|driver's license services\b|driver's license reinstatement\b|driver services center locator\b|mydrive online portal\b|suspension requirement guidance\b|driver's license\b|driver service\b|license reinstate\b|mydrive\b|driver services center\b|suspension requirement\b|driver's licenses\b|driver's license services\b|driver's license reinstatement\b|driver services center locator\b|mydrive online portal\b|suspension requirement guidance\b|driver's license\b|driver service\b|license reinstate\b|mydrive\b|driver services center\b|suspension requirement\b"),
    ("Social Security assistance", r"social security|ssn |retirement and disability application|disability compensation claim|social security card|ssn and card|ssn verification|disability compensation claims\b|retirement and disability applications\b|social security cards\b|social security card replacement\b|ssn and card information\b|ssn verification\b|social security\b|ssn\b|retirement and disability\b|disability compensation\b|social security card\b|ssn and card\b|ssn verification\b|disability compensation claims\b|retirement and disability applications\b|social security cards\b|social security card replacement\b|ssn and card information\b|ssn verification\b"),

    # Transportation
    ("Bus pass assistance", r"bus pass|reduced.fare bus|reduced-fare transit|daily weekly and monthly|half fare|reduced and half fares|reduced fare programs|reduced fares|reduced-fare bus passes|token transit|tarc3 paratransit|daily weekly and monthly passes|reduced and half fares\b|reduced fare programs\b|reduced fares\b|reduced-fare bus passes\b|reduced-fare transit\b|bus pass assistance\b|bus pass\b|reduced fare\b|half fare\b|daily weekly and monthly passes\b|token transit mobile payment\b|tarc3 paratransit\b|reduced and half fares\b|reduced fare programs\b|reduced fares\b|reduced-fare bus passes\b|reduced-fare transit\b|bus pass assistance\b|bus pass\b|reduced fare\b|half fare\b|daily weekly and monthly passes\b|token transit mobile payment\b|tarc3 paratransit\b"),
    ("Transportation assistance", r"transportation assist|transportation coord|transportation to treatment|work and appointment transportation|affordable transit|route planning|bus route|transit center|downtown transit|travel and transfer|referral and transportation|transportation\b|transportation assistance\b|transportation coordination\b|transportation to va\b|transportation to treatment\b|work and appointment transportation\b|affordable transit\b|route planning and schedules\b|bus routes\b|bus service\b|downtown transit center\b|travel and transfer requests\b|referral and transportation coordination\b|transportation and senior services info\b|transportation\b|transportation assistance\b|transportation coordination\b|transportation to va\b|transportation to treatment\b|work and appointment transportation\b|affordable transit\b|route planning and schedules\b|bus routes\b|bus service\b|downtown transit center\b|travel and transfer requests\b|referral and transportation coordination\b|transportation and senior services info\b"),

    # Basic needs / clothing / financial
    ("Clothing assistance", r"clothing assist|clothing closet|clothing distribution|clothing voucher|affordable thrift|dress for success|referral-based suiting|emergency food and clothing|clothing\b|clothing and hygiene|clothing distribution to partners|affordable thrift store clothing|hygiene supplies|clothing assistance\b|clothing closet\b|clothing distribution\b|clothing vouchers\b|affordable thrift\b|dress for success\b|referral-based suiting appointments\b|emergency food and clothing\b|clothing\b|clothing and hygiene distribution\b|clothing distribution to partners\b|affordable thrift store clothing\b|hygiene supplies\b|clothing assistance\b|clothing closet\b|clothing distribution\b|clothing vouchers\b|affordable thrift\b|dress for success\b|referral-based suiting appointments\b|emergency food and clothing\b|clothing\b|clothing and hygiene distribution\b|clothing distribution to partners\b|affordable thrift store clothing\b|hygiene supplies\b"),
    ("Basic needs assistance", r"basic need|emergency basic|hygiene|furniture|release bag|personal care|showers|laundry|agency voucher|seasonal distributions|release-day support|emergency aid|emergency assist|emergency services\b|emergency assessment|emergency care|emergency assistance|emergency basic needs|basic needs assistance|basic needs support|basic needs\b|emergency basic needs\b|hygiene supplies\b|furniture referrals\b|release bags\b|release-day support items\b|personal care\b|showers\b|laundry\b|agency voucher programs\b|seasonal distributions\b|emergency aid\b|emergency assist\b|emergency services\b|emergency assessment\b|emergency care\b|emergency assistance\b|emergency basic needs\b|basic needs assistance\b|basic needs support\b|basic needs\b|emergency basic needs\b|hygiene supplies\b|furniture referrals\b|release bags\b|release-day support items\b|personal care\b|showers\b|laundry\b|agency voucher programs\b|seasonal distributions\b|emergency aid\b|emergency assist\b|emergency services\b|emergency assessment\b|emergency care\b|emergency assistance\b|emergency basic needs\b|basic needs assistance\b|basic needs support\b|basic needs\b|emergency basic needs\b|hygiene supplies\b|furniture referrals\b|release bags\b|release-day support items\b|personal care\b|showers\b|laundry\b|agency voucher programs\b|seasonal distributions\b"),
    ("Emergency financial assistance", r"emergency financial|emergency aid|emergency assist|crisis financial|barrier relief|credit build|credit repair|debt management|billing assist|claims assist|redetermination|fee payment|reinstatement fee|wage withholding|unclaimed property|subsidy payment|emergency financial assistance|emergency financial aid|emergency financial help|crisis financial assistance|barrier relief assistance|barrier-reduction coaching|barrier-reduction support|credit building|credit repair\b|debt management\b|billing assistance\b|claims assistance\b|redetermination assistance\b|fee waiver|reinstatement fee payment|wage withholding enforcement|unclaimed property search|subsidy payments|emergency financial assistance\b|emergency financial aid\b|emergency financial help\b|crisis financial assistance\b|barrier relief assistance\b|barrier-reduction coaching\b|barrier-reduction support\b|credit building\b|credit repair\b|debt management\b|billing assistance\b|claims assistance\b|redetermination assistance\b|testing fee waiver assistance\b|reinstatement fee payment\b|wage withholding enforcement\b|unclaimed property search\b|subsidy payments to utility vendors\b|emergency financial assistance\b|emergency financial aid\b|emergency financial help\b|crisis financial assistance\b|barrier relief assistance\b|barrier-reduction coaching\b|barrier-reduction support\b|credit building\b|credit repair\b|debt management\b|billing assistance\b|claims assistance\b|redetermination assistance\b|testing fee waiver assistance\b|reinstatement fee payment\b|wage withholding enforcement\b|unclaimed property search\b|subsidy payments to utility vendors\b"),
    ("Banking access", r"banking access|chexsystems|20/20 second-chance|checking account|account upgrade|digital and mobile banking|visa debit|chexsystems-friendly banking|banking access\b|chexsystems\b|20/20 second-chance checking\b|checking account\b|account upgrade pathway\b|digital and mobile banking\b|visa debit card\b|chexsystems-friendly banking connections\b|certified low-fee checking account referrals\b|banking access\b|chexsystems\b|20/20 second-chance checking\b|checking account\b|account upgrade pathway\b|digital and mobile banking\b|visa debit card\b|chexsystems-friendly banking connections\b|certified low-fee checking account referrals\b"),
    ("Budgeting and financial coaching", r"budgeting|financial coach|financial literacy|debt management|credit build|credit repair|budgeting\b|financial coaching\b|financial literacy\b|debt management\b|credit building\b|credit repair\b|budgeting\b|financial coaching\b|financial literacy\b|debt management\b|credit building\b|credit repair\b"),

    # Application / info
    ("Application assistance", r"application assist|application help|application prep|eligibility screening|intake coord|intake routing|benefits application|combined benefits|application assistance\b|application help\b|application preparation\b|eligibility screening\b|intake coordination\b|intake routing\b|benefits application\b|combined benefits application\b|application assistance\b|application help\b|application preparation\b|eligibility screening\b|intake coordination\b|intake routing\b|benefits application\b|combined benefits application\b|cash assistance application\b|snap application assistance\b|snap application help\b|snap application information\b|medicaid enrollment assistance\b|medicaid enrollment help\b|medicaid enrollment support\b|benefits enrollment assistance\b|benefits enrollment\b|benefits assistance\b|redetermination assistance\b|cqe application processing\b|cqe assistance\b|voting rights eligibility screening\b|expungement eligibility screening\b|expungement screening\b|skills assessment and intake\b|workforce program intake\b|court and jail referral intake\b|restored citizen intake\b|statewide intake coordination\b|statewide intake routing\b|western kentucky intake\b|donation intake\b|client-choice food pantry\b|referral form guidance\b|referral-based suiting appointments\b|appointment scheduling\b|appointment scheduling referral\b|walk-in service\b|walk-in reporting\b|scheduled reporting\b|reporting appointments\b|reporting and check-ins\b|reporting compliance\b|reporting requirement information\b|compliant reporting\b|conditional discharge reporting\b|community supervision compliance\b|supervision compliance support\b|supervision status verification\b|supervision policy guidance\b|treatment compliance monitoring\b|compliance monitoring\b|compliance support\b|court compliance monitoring\b|court compliance\b|community control monitoring\b|community supervision compliance\b|community supervision support\b|community supervision\b|community control\b|community confinement\b|community coordination\b|community connections\b|community donations\b|community events\b|community integration support\b|community organizing\b|community planning support\b|community reintegration\b|community-based classes\b|community recovery mentoring\b|community recovery navigation\b|community reentry advocacy\b|community reentry referrals\b|community referrals\b|community resource connections\b|community resource navigation\b|community resource referrals\b|community support\b|community support associate training\b|community supervision\b|community supervision compliance\b|community supervision support\b|community control\b|community confinement\b|community coordination\b|community connections\b|community donations\b|community events\b|community integration support\b|community organizing\b|community planning support\b|community reintegration\b|community-based classes\b|community recovery mentoring\b|community recovery navigation\b|community reentry advocacy\b|community reentry referrals\b|community referrals\b|community resource connections\b|community resource navigation\b|community resource referrals\b|community support\b|community support associate training\b"),
    ("Information and referral", r"^information$|^information and referral$|211\b|central office information|state agency|statewide resource connection"),

    # Other services
    ("Coalition coordination", r"coalition coord|coalition meeting|coalition network|east region coalition|west region coalition|regional coalition coord|reentry coalition meetings|coalition coordination\b|coalition meetings\b|coalition network coordination\b|coalition partner referrals\b|east region coalition coordination\b|west region coalition coordination\b|regional coalition coordination\b|regional coalition referrals\b|reentry coalition meetings\b|reentry coalition referrals\b|tdoc partner networking\b|coalition coordination\b|coalition meetings\b|coalition network coordination\b|coalition partner referrals\b|east region coalition coordination\b|west region coalition coordination\b|regional coalition coordination\b|regional coalition referrals\b|reentry coalition meetings\b|reentry coalition referrals\b|tdoc partner networking\b"),
    ("Community supervision", r"^community supervision$"),
    ("Court advocacy", r"court advocacy|court and jail outreach"),
    ("Court compliance support", r"court compliance|compliance monitor|treatment compliance|supervised substance|court compliance monitoring|court compliance\b|compliance monitoring\b|compliance support\b|treatment compliance monitoring\b|supervised substance use treatment\b|court compliance monitoring\b|court compliance\b|compliance monitoring\b|compliance support\b|treatment compliance monitoring\b|supervised substance use treatment\b"),
    ("Aftercare planning", r"aftercare|continuing care|relapse prevention|aftercare planning\b|aftercare\b|continuing care and employment referrals\b|relapse prevention\b|aftercare planning\b|aftercare\b|continuing care and employment referrals\b|relapse prevention\b"),
    ("Alternative to incarceration", r"alternative to incarceration|alternative-to-incarceration|alternative sentencing|drug court|specialty court|mental health court|certified drug court|casey's law|dui assess|court-referred|pretrial|pre-trial|reentry court|specialty court coordination|certified drug court programs|statewide specialty court directory|alternative sentencing for veterans|alternative-to-incarceration coordination|alternative to incarceration\b|alternative-to-incarceration\b|alternative sentencing\b|drug court\b|specialty court\b|mental health court\b|certified drug court\b|casey's law\b|dui assess\b|court-referred treatment\b|pretrial\b|pre-trial\b|reentry court\b|specialty court coordination\b|certified drug court programs\b|statewide specialty court directory\b|alternative sentencing for veterans\b|alternative-to-incarceration coordination\b"),
    ("Work release programs", r"work release program|work release programs|work release\b"),
    ("Domestic violence support", r"domestic violence(?! legal)|safe planning|protection order|domestic violence support\b|domestic violence counseling\b|safety planning\b|domestic violence protection orders\b|domestic violence support\b|domestic violence counseling\b|safety planning\b|domestic violence protection orders\b"),
    ("Developmental disability services", r"developmental disability|disability service|disability compensation|senior and disability|accessibility|developmental disability services\b|developmental disability support\b|disability compensation claims\b|senior and disability services\b|accessibility\b|accessibility services\b|developmental disability services\b|developmental disability support\b|disability compensation claims\b|senior and disability services\b|accessibility\b|accessibility services\b"),
    ("Senior services", r"senior service|senior meal|senior and aging|senior and child nutrition|senior legal|aging service|transportation and senior|senior services\b|senior meals\b|senior and aging services\b|senior and child nutrition programs\b|senior legal assistance\b|senior and disability services\b|transportation and senior services info\b|senior services\b|senior meals\b|senior and aging services\b|senior and child nutrition programs\b|senior legal assistance\b|senior and disability services\b|transportation and senior services info\b"),
    ("Women's health services", r"women's health|women's recovery|women's residential|women's shelter|women and children|women veterans resources|women's health services\b|women's recovery residence\b|women's residential recovery\b|women's residential treatment\b|women's shelter\b|women and children's day shelter\b|women and children's housing\b|women veterans resources\b|women's health services\b|women's recovery residence\b|women's residential recovery\b|women's residential treatment\b|women's shelter\b|women and children's day shelter\b|women and children's housing\b|women veterans resources\b"),
    ("Spiritual support", r"spiritual care|spiritual mentorship|congregation|church partner|faith-based|religious|worship|chapel|spiritual support\b|spiritual care\b|spiritual mentorship\b|congregation network\b|congregation partnerships\b|church partnerships\b|spiritual support\b|spiritual care\b|spiritual mentorship\b|congregation network\b|congregation partnerships\b|church partnerships\b"),
    ("Advocacy", r"^advocacy$|community reentry advocacy|systemic barrier advocacy|advocacy\b|community reentry advocacy\b|systemic barrier advocacy\b|veterans advocacy\b|civil rights advocacy\b|benefits advocacy\b|court advocacy\b|child advocacy\b|advocacy\b|community reentry advocacy\b|systemic barrier advocacy\b|veterans advocacy\b|civil rights advocacy\b|benefits advocacy\b|court advocacy\b|child advocacy\b"),
    ("Accessibility services", r"^accessibility$|^accessibility services$"),
    ("Anger management", r"^anger management$"),
    ("Co-parenting support", r"co-parenting|co-parenting support\b"),
    ("Computer and digital literacy", r"computer training|digital literacy|digital and mobile|chromebook|computer and digital literacy\b|digital literacy instruction\b|computer training\b|digital and mobile banking\b|digital literacy\b|technology programs\b|technology workforce training\b|computer and digital literacy\b|digital literacy instruction\b|computer training\b|digital and mobile banking\b|digital literacy\b|technology programs\b|technology workforce training\b"),
    ("Voting rights assistance", r"voting rights|voter registration|civil rights restoration|automatic restoration|voting rights assistance\b|voting rights education\b|voting rights eligibility screening\b|voter registration partnerships\b|voter registration resources\b|civil rights restoration applications\b|automatic restoration verification\b|voting rights assistance\b|voting rights education\b|voting rights eligibility screening\b|voter registration partnerships\b|voter registration resources\b|civil rights restoration applications\b|automatic restoration verification\b"),
    ("Sober living housing", r"sober living|structured sober|sober housing|recovery residence|halfway|oxford house|phase i peer recovery|sober180|women's recovery residence|sober living recovery program|structured sober living for men|sober living placement assistance|structured sober living\b|sober housing\b|recovery residence\b|halfway house\b|oxford house\b|phase i peer recovery\b|sober180 curriculum\b|women's recovery residence\b|sober living recovery program\b|structured sober living for men\b|sober living placement assistance\b|structured sober living\b|sober housing\b|recovery residence\b|halfway house\b|oxford house\b|phase i peer recovery\b|sober180 curriculum\b|women's recovery residence\b|sober living recovery program\b|structured sober living for men\b|sober living placement assistance\b"),
    ("Emergency food assistance", r"emergency food(?! distribution| resource)|daily meal|community meal|daily community meal|senior meal|meal program|emergency food assistance\b|emergency food\b|daily meals\b|community meals\b|daily community meals\b|senior meals\b|meal program\b|emergency food assistance\b|emergency food\b|daily meals\b|community meals\b|daily community meals\b|senior meals\b|meal program\b"),
    ("Partner referrals", r"referral|partner connection|partner network|community partner|agency referral|resource connection|resource coordination|resource navigation|statewide referral|employer connection|employer partnership|network coordination|linkage|connections to|service provider|coalition partner|training referral|specialty referral|workforce referral|career referral|skills training referral|housing referral|shelter referral|food pantry referral|community meal program referral|employer placement|second-chance employer|242 partner|congregation|church partner|volunteer network|sponsor connection|alumni network|stand-down|provider network|office referral|dcbs|dhs referral|drc referral|regional office|county office|district office|central office|field office|branch location|county program locator|satellite office|appointment scheduling|provider search|facility search|clinic directory|telehealth provider|statewide intake|portal|mydrive|token transit|route planning|bus route|transit center|unclaimed property|voter registration partner|text-based nav|text and chat|spanish-language helpline|online portal|virtual and in-person|technology program|small business|business and employer|economic mobility|wellness program|character development|spiritual mentorship|advisory board|community agency|community organizing|community planning|community events|community donations|community integration|community reintegration|community-based class|community recovery nav|community resource|community connection|community referral|community confinement|community control|networking\b|outreach\b|linkages\b|resource networking|resource sharing|resource platform|resource-specific|generic|networking|outreach|connections|coordination|information sharing|resource fairs|fairs\b|events\b|meetings\b|directories\b|locator\b|lookup\b|routing\b|scheduling\b|portal\b|platform\b|support items\b|network\b|partnerships\b|collaboration\b|connections\b|coordination\b|information\b|sharing\b|fairs\b|events\b|meetings\b|directories\b|locator\b|lookup\b|routing\b|scheduling\b|portal\b|platform\b|support items\b|network\b|partnerships\b|collaboration\b"),
)

RULES: tuple[tuple[str, re.Pattern[str]], ...] = tuple(
    (canonical, re.compile(pattern, re.IGNORECASE))
    for canonical, pattern in _RULE_SPECS
)

# Manual overrides keyed by alias_key(raw) — see service_type_overrides.py
from lib.service_type_overrides import EXACT_OVERRIDES, FALLBACK_RULES


def alias_key(value: str) -> str:
    """Normalize a service string for alias lookup."""
    return re.sub(r"\s+", " ", value.strip().lower())


def classify_by_rules(raw: str) -> str | None:
    """Classify a raw service string using ordered regex rules."""
    if raw in LEGACY_CANONICAL_SET:
        return consolidate_canonical(raw)
    if raw in CANONICAL_SET:
        return raw
    lowered = raw.lower().strip()
    for canonical, pattern in RULES:
        if pattern.search(lowered):
            return consolidate_canonical(canonical)
    return None


def classify_with_fallback(raw: str) -> str | None:
    """Classify using primary rules, exact overrides, then fallback patterns."""
    key = alias_key(raw)
    if key in EXACT_OVERRIDES:
        return consolidate_canonical(EXACT_OVERRIDES[key])
    primary = classify_by_rules(raw)
    if primary:
        return primary
    if raw in LEGACY_CANONICAL_SET or raw in CANONICAL_SET:
        return consolidate_canonical(raw)
    lowered = raw.lower().strip()
    for canonical, pattern in FALLBACK_RULES:
        if pattern.search(lowered):
            return consolidate_canonical(canonical)
    return None


def _load_service_aliases() -> dict[str, str]:
    if not _ALIASES_PATH.exists():
        return {}
    data = json.loads(_ALIASES_PATH.read_text(encoding="utf-8"))
    return {str(k): str(v) for k, v in data.items()}


SERVICE_ALIASES: dict[str, str] = _load_service_aliases()


def normalize_service(value: str) -> str:
    """Trim, apply alias map, and return canonical service name."""
    trimmed = value.strip()
    if not trimmed:
        return ""
    key = alias_key(trimmed)
    if key in SERVICE_ALIASES:
        return consolidate_canonical(SERVICE_ALIASES[key])
    classified = classify_with_fallback(trimmed)
    if classified:
        return classified
    return consolidate_canonical(trimmed)


def normalize_services_field(raw: str) -> str:
    """Split on ``|``, normalize each token, dedupe preserving order."""
    if not raw or not raw.strip():
        return ""
    seen: set[str] = set()
    normalized: list[str] = []
    for part in raw.split("|"):
        canonical = normalize_service(part)
        if not canonical or canonical in seen:
            continue
        seen.add(canonical)
        normalized.append(canonical)
    return "|".join(normalized)


def collect_services_from_csv(csv_paths: list[str | Path]) -> set[str]:
    services: set[str] = set()
    for csv_path in csv_paths:
        path = Path(csv_path)
        if not path.exists():
            continue
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames or "services" not in reader.fieldnames:
                continue
            for row in reader:
                for part in (row.get("services") or "").split("|"):
                    value = part.strip()
                    if value:
                        services.add(value)
    return services


def is_mapped(raw: str) -> bool:
    key = alias_key(raw)
    if key in SERVICE_ALIASES:
        return True
    return classify_with_fallback(raw) is not None


def unmapped_services(csv_paths: list[str | Path]) -> list[str]:
    return sorted(s for s in collect_services_from_csv(csv_paths) if not is_mapped(s))


@dataclass
class ServiceAuditReport:
    csv_paths: list[str]
    unique_before: int
    unique_after: int
    canonical_types_used: int
    total_occurrences_before: int
    total_occurrences_after: int
    merges: list[tuple[str, str, int]] = field(default_factory=list)
    unmapped: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "csv_paths": self.csv_paths,
            "unique_before": self.unique_before,
            "unique_after": self.unique_after,
            "canonical_types_used": self.canonical_types_used,
            "total_occurrences_before": self.total_occurrences_before,
            "total_occurrences_after": self.total_occurrences_after,
            "top_merges": [
                {"from": src, "to": dst, "count": count}
                for src, dst, count in self.merges[:30]
            ],
            "unmapped": self.unmapped,
        }


def audit_services(csv_paths: list[str | Path]) -> ServiceAuditReport:
    """Compare raw vs normalized service strings across CSV files."""
    before_counts: dict[str, int] = {}
    after_counts: dict[str, int] = {}
    merge_counts: dict[tuple[str, str], int] = {}
    paths_used: list[str] = []

    for csv_path in csv_paths:
        path = Path(csv_path)
        if not path.exists():
            continue
        paths_used.append(str(path))
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if not reader.fieldnames or "services" not in reader.fieldnames:
                continue
            for row in reader:
                for part in (row.get("services") or "").split("|"):
                    raw = part.strip()
                    if not raw:
                        continue
                    canonical = normalize_service(raw)
                    before_counts[raw] = before_counts.get(raw, 0) + 1
                    after_counts[canonical] = after_counts.get(canonical, 0) + 1
                    if alias_key(raw) != alias_key(canonical):
                        key = (raw, canonical)
                        merge_counts[key] = merge_counts.get(key, 0) + 1

    merges = sorted(
        ((src, dst, count) for (src, dst), count in merge_counts.items()),
        key=lambda item: item[2],
        reverse=True,
    )

    return ServiceAuditReport(
        csv_paths=paths_used,
        unique_before=len(before_counts),
        unique_after=len(after_counts),
        canonical_types_used=len(after_counts),
        total_occurrences_before=sum(before_counts.values()),
        total_occurrences_after=sum(after_counts.values()),
        merges=merges,
        unmapped=unmapped_services(csv_paths),
    )
