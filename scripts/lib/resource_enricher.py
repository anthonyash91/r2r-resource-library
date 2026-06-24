"""Expand resource CSV rows to publication-ready narrative depth (Kentucky parity)."""
from __future__ import annotations

import re
from typing import Any

from intake_signals import classify_intake_signals_heuristic, serialize_intake_signals
from lib.service_types import normalize_services_field

STATE_PRESETS: dict[str, dict[str, str]] = {
    "Kentucky": {
        "name": "Kentucky",
        "demonym": "Kentuckians",
        "demonym_es": "kentuckianos",
        "throughout": "throughout Kentucky",
        "throughout_es": "en todo Kentucky",
        "counties_n": "Kentucky counties",
        "counties_n_es": "condados de Kentucky",
        "adults": "Kentucky adults",
        "adults_es": "adultos en Kentucky",
        "residents": "Kentucky residents",
        "residents_es": "residentes de Kentucky",
        "tag": "kentucky",
    },
    "Ohio": {
        "name": "Ohio",
        "demonym": "Ohioans",
        "demonym_es": "ohianos",
        "throughout": "throughout Ohio",
        "throughout_es": "en todo Ohio",
        "counties_n": "Ohio counties",
        "counties_n_es": "condados de Ohio",
        "adults": "Ohio adults",
        "adults_es": "adultos en Ohio",
        "residents": "Ohio residents",
        "residents_es": "residentes de Ohio",
        "tag": "ohio",
    },
    "Indiana": {
        "name": "Indiana",
        "demonym": "Hoosiers",
        "demonym_es": "hoosiers",
        "throughout": "throughout Indiana",
        "throughout_es": "en todo Indiana",
        "counties_n": "Indiana counties",
        "counties_n_es": "condados de Indiana",
        "adults": "Indiana adults",
        "adults_es": "adultos en Indiana",
        "residents": "Indiana residents",
        "residents_es": "residentes de Indiana",
        "tag": "indiana",
    },
    "Tennessee": {
        "name": "Tennessee",
        "demonym": "Tennesseans",
        "demonym_es": "tennesseanos",
        "throughout": "throughout Tennessee",
        "throughout_es": "en todo Tennessee",
        "counties_n": "Tennessee counties",
        "counties_n_es": "condados de Tennessee",
        "adults": "Tennessee adults",
        "adults_es": "adultos en Tennessee",
        "residents": "Tennessee residents",
        "residents_es": "residentes de Tennessee",
        "tag": "tennessee",
    },
    "Michigan": {
        "name": "Michigan",
        "demonym": "Michigan residents",
        "demonym_es": "residentes de Michigan",
        "throughout": "throughout Michigan",
        "throughout_es": "en todo Michigan",
        "counties_n": "Michigan counties",
        "counties_n_es": "condados de Michigan",
        "adults": "Michigan adults",
        "adults_es": "adultos en Michigan",
        "residents": "Michigan residents",
        "residents_es": "residentes de Michigan",
        "tag": "michigan",
    },
}

_STATE = STATE_PRESETS["Ohio"]


def configure_enricher_state(state: str) -> None:
    global _STATE
    _STATE = STATE_PRESETS.get(state, STATE_PRESETS["Kentucky"])


def infer_state_from_csv_path(path: str) -> str:
    stem = path.lower()
    if "michigan" in stem:
        return "Michigan"
    if "tennessee" in stem:
        return "Tennessee"
    if "indiana" in stem:
        return "Indiana"
    if "ohio" in stem:
        return "Ohio"
    return "Kentucky"


def _category_reentry_hints() -> dict[str, tuple[str, str]]:
    s = _STATE
    base = dict(CATEGORY_REENTRY_TEMPLATE)
    en, es = base["education"]
    base["education"] = (
        en.replace("STATE adults", s["adults"]),
        es.replace("adultos en STATE", s["adults_es"]),
    )
    return base


CATEGORY_REENTRY_TEMPLATE = {
    "housing": (
        "Resources may include case management, sobriety requirements, or referral from corrections partners—confirm admission steps before visiting.",
        "Los recursos pueden incluir manejo de casos, requisitos de sobriedad o referencia de socios correccionales—confirme los pasos de admisión antes de visitar.",
    ),
    "employment": (
        "Staff help justice-involved job seekers build work history, remove record-related barriers, and connect to fair-chance employers in the region.",
        "El personal ayuda a quienes buscan empleo con antecedentes penales a construir historial laboral, reducir barreras por antecedentes y conectarse con empleadores de segunda oportunidad.",
    ),
    "healthcare": (
        "Services are available on a sliding fee or Medicaid basis for eligible patients; bring ID and release paperwork when establishing care after incarceration.",
        "Los servicios están disponibles con tarifa móvil o Medicaid para pacientes elegibles; lleve identificación y documentos de liberación al establecer atención después de la encarcelación.",
    ),
    "legal-aid": (
        "Representation is limited to civil legal matters—not active criminal cases. Income, household size, and offense type determine eligibility for record relief.",
        "La representación se limita a asuntos legales civiles—no casos penales activos. Ingresos, tamaño del hogar y tipo de delito determinan la elegibilidad para alivio de antecedentes.",
    ),
    "substance-use-treatment": (
        "Treatment may require assessment, insurance or Medicaid enrollment, and referral from courts or corrections for some beds—call intake to confirm openings.",
        "El tratamiento puede requerir evaluación, seguro o Medicaid y referencia de tribunales o correcciones para algunas plazas—llame a admisión para confirmar disponibilidad.",
    ),
    "education": (
        "Classes are typically free or low-cost for STATE adults; orientation may be required before enrollment in GED or vocational tracks.",
        "Las clases suelen ser gratuitas o de bajo costo para adultos en STATE; puede requerirse orientación antes de inscribirse en GED o capacitación vocacional.",
    ),
    "veterans": (
        "VA eligibility and discharge status affect which benefits apply; ask specifically for justice-involved veteran or VJO/HCRV services when calling.",
        "La elegibilidad del VA y el tipo de baja afectan qué beneficios aplican; pida específicamente servicios VJO/HCRV o para veteranos en el sistema de justicia al llamar.",
    ),
    "financial-assistance": (
        "Bring proof of identity, income, and release or residency documents when applying at a county office or online portal.",
        "Lleve prueba de identidad, ingresos y documentos de liberación o residencia al solicitar en una oficina del condado o portal en línea.",
    ),
    "food-nutrition": (
        "Food assistance does not usually require a criminal-record disclosure; staff can help with SNAP applications and pantry locations by ZIP code.",
        "La asistencia alimentaria generalmente no requiere declarar antecedentes penales; el personal puede ayudar con solicitudes SNAP y ubicaciones de despensas por código postal.",
    ),
    "basic-needs": (
        "Availability varies by season and donations; call ahead when possible to confirm clothing, hygiene kits, or furniture pickup hours.",
        "La disponibilidad varía según la temporada y donaciones; llame cuando sea posible para confirmar horarios de ropa, kits de higiene o muebles.",
    ),
    "probation-parole": (
        "This office handles supervision compliance and reporting—not emergency reentry navigation; ask your officer for referrals to local reentry partners.",
        "Esta oficina maneja cumplimiento de supervisión e informes—no navegación de crisis de reinserción; pida a su oficial referencias a aliados locales de reinserción.",
    ),
    "id-documentation": (
        "Fees, proof of identity, and residency documents apply; reentry resources and legal aid partners often help gather required paperwork.",
        "Aplican tarifas, prueba de identidad y documentos de residencia; recursos de reinserción y aliados legales suelen ayudar a reunir el papeleo requerido.",
    ),
    "transportation": (
        "Reduced-fare resources typically require application and proof of income or disability; IDs are needed to receive a pass or card.",
        "Los recursos de tarifa reducida suelen requerir solicitud y prueba de ingresos o discapacidad; se necesita identificación para recibir un pase o tarjeta.",
    ),
    "family-children": (
        "Family resources may require participation in treatment or parenting classes; custody status affects some reunification services.",
        "Los recursos familiares pueden requerir participación en tratamiento o clases de crianza; el estado de custodia afecta algunos servicios de reunificación.",
    ),
    "peer-support": (
        "Peer specialists with lived experience offer mentoring and recovery support; certification requirements vary by resource.",
        "Especialistas pares con experiencia vivida ofrecen mentoría y apoyo en recuperación; los requisitos de certificación varían según el recurso.",
    ),
    "state-agency": (
        "State offices provide information and referrals statewide; county and nonprofit partners deliver most direct services.",
        "Las oficinas estatales ofrecen información y referencias en todo el estado; socios del condado y sin fines de lucro prestan la mayoría de servicios directos.",
    ),
    "reentry-organizations": (
        "Coalition and navigator resources connect returning citizens to local partners—they rarely provide emergency shelter, cash aid, or 24/7 crisis response on their own.",
        "Las coaliciones y recursos de navegación conectan a ciudadanos que regresan con aliados locales—rara vez ofrecen refugio de emergencia, efectivo o respuesta de crisis 24/7 por sí solos.",
    ),
}

GENERIC_ELIGIBILITY = (
    "STATE residents in service area; contact this resource for current eligibility requirements.",
    "Contact this resource for current eligibility requirements.",
    "Justice-involved residents of served counties; contact coalition for current partner eligibility.",
)
GENERIC_NOTES_EN = (
    "Verify current hours and intake process on website or by phone.",
    "Contact for current hours",
    "Contact for meeting dates and hours",
)
BOILERPLATE_DESC = (
    " Contact this resource for current intake.",
    "Contact this resource for current intake.",
)


def _clean(text: str) -> str:
    t = (text or "").strip()
    for b in BOILERPLATE_DESC:
        t = t.replace(b, "").strip()
    t = re.sub(r"\s+", " ", t)
    return t


def _is_generic_eligibility(text: str) -> bool:
    t = (text or "").strip()
    generic = tuple(
        g.replace("STATE", _STATE["name"]) for g in GENERIC_ELIGIBILITY
    )
    return not t or t in generic or "contact this resource for current eligibility" in t.lower()


def _is_generic_notes(text: str) -> bool:
    t = (text or "").strip()
    return not t or t in GENERIC_NOTES_EN or t.startswith("Verify current hours")


def _area_phrase(row: dict[str, str]) -> tuple[str, str]:
    served = (row.get("served_counties") or "").strip()
    county = (row.get("county") or "").strip()
    city = (row.get("city") or "").strip()
    coverage = (row.get("coverage") or "single").strip()
    region = (row.get("region") or "").strip()

    if coverage == "statewide":
        return _STATE["throughout"], _STATE["throughout_es"]
    if served:
        counties = [c.strip() for c in served.split("|") if c.strip()]
        if len(counties) == 1:
            return f"{counties[0]} County", f"condado de {counties[0]}"
        if len(counties) <= 4:
            en = ", ".join(counties[:-1]) + f", and {counties[-1]} counties"
            es = ", ".join(counties[:-1]) + f" y {counties[-1]}"
            return en, f"los condados {es}"
        return f"{len(counties)} {_STATE['counties_n']}", f"{len(counties)} {_STATE['counties_n_es']}"
    if county:
        loc = f"{county} County" + (f" ({city})" if city else "")
        es_loc = f"condado de {county}" + (f" ({city})" if city else "")
        return loc, es_loc
    if region:
        return region, region
    return "the local area", "el área local"


def _is_coalition(row: dict[str, str]) -> bool:
    name = (row.get("name") or "").lower()
    tags = (row.get("tags") or "").lower()
    desc = (row.get("description") or "").lower()
    return "coalition" in name or "coalition" in tags or "networking council" in desc


def _is_referral_hub(row: dict[str, str]) -> bool:
    desc = (row.get("description") or "").lower()
    tags = (row.get("tags") or "").lower()
    return (
        "referral" in desc
        or "referral-only" in tags
        or "portal" in desc
        or "directory" in desc
        or "does not provide direct" in desc
        or "not a direct" in desc
    )


def _direct_service_hint(category: str) -> bool:
    return category in {
        "housing",
        "employment",
        "healthcare",
        "legal-aid",
        "substance-use-treatment",
        "education",
        "basic-needs",
        "peer-support",
    }


def _is_broken_spanish(text: str) -> bool:
    t = (text or "").strip()
    if not t:
        return True
    english_markers = (
        " free ",
        " noncriminal",
        "Provides ",
        "Contact this resource",
        "Proporciona free",
        "Gratuita noncriminal",
        " networking coalition",
    )
    lower = f" {t} "
    return any(m.lower() in lower.lower() for m in english_markers)


def expand_description(row: dict[str, str]) -> tuple[str, str]:
    name = row.get("name", "").strip()
    category = row.get("category", "").strip()
    base = _clean(row.get("description", ""))
    base_es = _clean(row.get("description_es", ""))
    area_en, area_es = _area_phrase(row)
    cat_hint_en, cat_hint_es = _category_reentry_hints().get(category, _category_reentry_hints()["reentry-organizations"])

    substantial_en = len(base) >= 340 and "Contact this resource for current intake" not in base
    needs_es_rebuild = _is_broken_spanish(base_es) or not base_es

    if substantial_en and not needs_es_rebuild:
        if "reentry" not in base.lower() and "justice" not in base.lower():
            extra_en = f" This resource supports {_STATE['demonym']} navigating reentry in {area_en}."
            extra_es = f" Este recurso apoya a {_STATE['demonym_es']} en reinserción en {area_es}."
            return base + extra_en, base_es + extra_es
        return base, base_es

    if substantial_en and needs_es_rebuild:
        # Keep strong EN; rebuild ES from category template
        es = (
            f"{name} sirve a adultos con antecedentes penales y familias que reconstruyen estabilidad en {area_es}. "
            f"{cat_hint_es} "
            f"Contacte este recurso para confirmar pasos de admisión, documentos requeridos y si aceptan visitas sin cita o referencias."
        )
        if category == "legal-aid":
            es = (
                f"{name} ofrece asistencia legal civil gratuita o de bajo costo para residentes de bajos ingresos en {area_es}. "
                f"Los abogados ayudan con sellado o eliminación de antecedentes, desalojos, beneficios y otros asuntos civiles—no casos penales activos. "
                f"{cat_hint_es} "
                f"Contacte la oficina para evaluar elegibilidad por ingresos, tipo de delito y documentación requerida."
            )
        return base, es

    if _is_coalition(row):
        en = (
            f"{name} is a regional reentry coalition serving {area_en}. "
            f"Partner agencies, faith communities, and workforce organizations meet regularly to share resources and warm referrals for people leaving jail or prison, on probation or parole, and their families. "
            f"Coordinators help returning citizens connect to housing, employment, treatment, legal aid, and benefits through local partners. "
            f"This is primarily a networking and navigation council—not an emergency shelter, cash assistance, or crisis line."
        )
        es = (
            f"{name} es una coalición regional de reinserción que sirve {area_es}. "
            f"Agencias aliadas, comunidades de fe y organizaciones laborales se reúnen para compartir recursos y referencias directas para personas que salen de la cárcel o prisión, en libertad condicional o vigilada, y sus familias. "
            f"Los coordinadores ayudan a conectar a ciudadanos que regresan con vivienda, empleo, tratamiento, asistencia legal y beneficios a través de aliados locales. "
            f"Es principalmente un consejo de red y navegación—no un refugio de emergencia, asistencia en efectivo ni línea de crisis."
        )
        return en, es

    if _is_referral_hub(row):
        en = (
            f"{name} is a statewide or regional referral resource for {_STATE['demonym']} affected by the criminal justice system. "
            f"{base} Users can search by location, service type, or need to find active providers in {area_en}. "
            f"Specialists or online tools help match people to housing, treatment, employment, legal aid, or benefits resources operated by other organizations. "
            f"This entry describes a navigation hub—staff here do not replace direct services at partner agencies."
        )
        es = (
            f"{name} es un recurso de referencia estatal o regional para {_STATE['demonym_es']} afectados por el sistema de justicia penal. "
            f"Los usuarios pueden buscar por ubicación, tipo de servicio o necesidad para encontrar proveedores activos en {area_es}. "
            f"Herramientas en línea o especialistas ayudan a conectar con vivienda, tratamiento, empleo, asistencia legal o beneficios operados por otras organizaciones. "
            f"Esta entrada describe un centro de navegación—el personal no reemplaza servicios directos en agencias aliadas."
        )
        return en, es

    en = (
        f"{name} serves justice-involved adults and families rebuilding stability after incarceration in {area_en}. "
        f"{base} "
        f"{cat_hint_en} "
        f"Contact this resource to confirm current intake steps, required documents, and whether walk-ins or referrals are accepted."
    )
    if category == "legal-aid":
        es = (
            f"{name} ofrece asistencia legal civil gratuita o de bajo costo para residentes de bajos ingresos en {area_es}. "
            f"Los abogados ayudan con sellado o eliminación de antecedentes, desalojos, beneficios y otros asuntos civiles—no casos penales activos. "
            f"{cat_hint_es} "
            f"Contacte la oficina para confirmar pasos de admisión, documentos requeridos y si aceptan visitas sin cita o referencias."
        )
    else:
        es = (
            f"{name} sirve a adultos con antecedentes penales y familias que reconstruyen estabilidad después de la encarcelación en {area_es}. "
            f"{cat_hint_es} "
            f"Contacte este recurso para confirmar pasos de admisión, documentos requeridos y si aceptan visitas sin cita o referencias."
        )
    return en, es


def expand_eligibility(row: dict[str, str]) -> tuple[str, str]:
    if not _is_generic_eligibility(row.get("eligibility", "")):
        en = row.get("eligibility", "").strip()
        es = row.get("eligibility_es", "").strip() or en
        return en, es

    category = row.get("category", "")
    area_en, area_es = _area_phrase(row)
    name = row.get("name", "")

    if _is_coalition(row):
        en = f"Justice-involved residents of {area_en} and family members seeking local reentry partner referrals; coalition does not determine partner agency eligibility."
        es = f"Residentes con antecedentes penales de {area_es} y familiares que buscan referencias de aliados locales de reinserción; la coalición no determina la elegibilidad de agencias aliadas."
    elif category == "legal-aid":
        en = f"Low-income {_STATE['residents']} in {area_en}; income and household limits apply. Record sealing and expungement eligibility depends on offense type, waiting periods, and case outcome."
        es = f"{_STATE['residents_es'].capitalize()} de bajos ingresos en {area_es}; aplican límites de ingresos y hogar. La elegibilidad para sellado o eliminación de antecedentes depende del tipo de delito, períodos de espera y resultado del caso."
    elif category == "housing":
        en = f"Adults in {area_en} who are homeless, leaving incarceration, or in recovery; resources may require sobriety, income limits, or DOC/court referral."
        es = f"Adultos en {area_es} sin hogar, que salen de la encarcelación o en recuperación; los recursos pueden requerir sobriedad, límites de ingresos o referencia del DOC/tribunal."
    elif category == "employment":
        en = f"Job seekers in {area_en} with criminal records, including people recently released or on supervision; some training slots require referral partners."
        es = f"Personas que buscan empleo en {area_es} con antecedentes penales, incluidas personas recién liberadas o bajo supervisión; algunas plazas de capacitación requieren referencia de aliados."
    elif category == "veterans":
        en = "U.S. military veterans in contact with courts, jails, or prisons; VA medical and benefits eligibility depends on discharge status and service history."
        es = "Veteranos de las fuerzas armadas de EE.UU. en contacto con tribunales, cárceles o prisiones; la elegibilidad médica y de beneficios del VA depende del tipo de baja e historial de servicio."
    elif category == "state-agency" or row.get("coverage") == "statewide":
        en = f"{_STATE['residents'].capitalize()} meeting resource requirements for {name}; criminal record is generally not a barrier to information and referral services."
        es = f"{_STATE['residents_es'].capitalize()} que cumplan los requisitos del recurso para {name}; los antecedentes penales generalmente no son barrera para información y referencias."
    else:
        en = f"Residents of {area_en} who are justice-involved or recently released; resource-specific income, referral, or offense-type rules may apply—confirm at intake."
        es = f"Residentes de {area_es} con antecedentes penales o recién liberados; pueden aplicar reglas de ingresos, referencia o tipo de delito—confirme en la admisión."

    return en, es


def expand_notes(row: dict[str, str]) -> tuple[str, str]:
    if not _is_generic_notes(row.get("notes", "")):
        notes_en = row.get("notes", "").strip()
        notes_es = row.get("notes_es", "").strip()
        # Fix duplicated EN in ES notes for coalitions
        if notes_es.startswith("Networking coalition") and "No ofrece" not in notes_es:
            pass
        if notes_en and notes_es and notes_en == notes_es.split(".")[0]:
            notes_es = notes_en  # will be replaced below if needed
        if len(notes_es) > 20 and notes_es != notes_en:
            return notes_en, notes_es

    phone = (row.get("phone") or "").strip()
    website = (row.get("website") or "").strip()
    email = (row.get("email") or "").strip()
    hours = (row.get("hours") or "").strip()
    name = row.get("name", "")

    contact_parts = []
    if phone:
        contact_parts.append(f"call {phone}")
    if website:
        contact_parts.append(f"visit {website}")
    if email:
        contact_parts.append(f"email {email}")
    contact = "; ".join(contact_parts) if contact_parts else "contact this resource directly"

    en = f"For current intake, {contact}. {hours + '.' if hours and not hours.endswith('.') else hours or 'Hours vary—confirm before visiting.'}"
    if _is_coalition(row):
        en += " Coalition meetings and partner lists change—ask for the latest referral sheet."
    elif _direct_service_hint(row.get("category", "")):
        en += " Bring photo ID, proof of release or supervision, and any court paperwork when applying."

    es_contact = contact.replace("call", "llame al").replace("visit", "visite").replace("email", "correo")
    es = f"Para admisión actual, {es_contact}. {hours + '.' if hours else 'Horario variable—confirme antes de visitar.'}"
    if _is_coalition(row):
        es += " Las reuniones de coalición y listas de aliados cambian—pida la hoja de referencias más reciente."
    elif _direct_service_hint(row.get("category", "")):
        es += " Lleve identificación con foto, prueba de liberación o supervisión y documentos judiciales al solicitar."

    return en, es


def expand_services(row: dict[str, str]) -> str:
    existing = [s.strip() for s in (row.get("services") or "").split("|") if s.strip()]
    generic = {"Partner referrals", "Community support", "Resource-specific services"}
    if existing and not generic.issuperset(set(existing)):
        return normalize_services_field(row.get("services", ""))

    category = row.get("category", "")
    mapping = {
        "housing": "Emergency shelter|Transitional housing|Case management|Housing navigation|Landlord outreach",
        "employment": "Job readiness training|Resume help|Skills training|Job placement|Partner referrals",
        "healthcare": "Primary medical care|Behavioral health services|Medicaid enrollment|Sliding-fee care",
        "legal-aid": "Expungement assistance|Housing legal aid|Benefits advocacy|Civil legal representation",
        "education": "GED and high school equivalency|Adult education|Career training and certifications|Career counseling",
        "veterans": "VA benefits navigation|Veterans services|Addiction treatment referrals|Partner referrals",
        "food-nutrition": "Food pantry access|SNAP enrollment|Emergency food assistance",
        "financial-assistance": "Benefits enrollment|Medicaid enrollment|SNAP enrollment|Case management",
        "substance-use-treatment": "Outpatient treatment|Residential treatment|MAT referrals|Addiction recovery support",
        "basic-needs": "Clothing assistance|Basic needs assistance|Emergency financial assistance|Partner referrals",
        "probation-parole": "Probation and parole supervision|Court compliance support|Partner referrals",
        "id-documentation": "ID assistance|Birth certificate assistance|Document assistance",
        "transportation": "Bus pass assistance|Transportation assistance",
        "peer-support": "Peer support|Addiction recovery support|Support groups",
        "family-children": "Family reunification support|Parenting services|Case management",
        "reentry-organizations": "Reentry navigation|Partner referrals|Coalition coordination|Partner referrals",
        "state-agency": "Information and referral|Partner referrals|Partner referrals",
    }
    return normalize_services_field(mapping.get(category, "Reentry navigation|Partner referrals|Partner referrals"))


def expand_tags(row: dict[str, str]) -> str:
    existing = [t.strip() for t in (row.get("tags") or "").split("|") if t.strip()]
    if len(existing) >= 5:
        return row.get("tags", "")
    extras = ["reentry", _STATE["tag"]]
    county = (row.get("county") or "").strip().lower()
    if county:
        extras.append(county.replace(" ", "-"))
    category = row.get("category", "")
    if category and category not in existing:
        extras.append(category.replace("_", "-"))
    merged = existing + [e for e in extras if e not in existing]
    return "|".join(merged[:8])


def is_publication_ready(row: dict[str, str]) -> bool:
    """Skip narrative expansion when the CSV row already meets publication standards."""
    desc = (row.get("description") or "").strip()
    desc_es = (row.get("description_es") or "").strip()
    if len(desc) < 340 or len(desc_es) < 280:
        return False
    if any(b.lower() in desc.lower() for b in BOILERPLATE_DESC):
        return False
    if "contact this resource for current intake" in desc.lower():
        return False
    if _is_generic_eligibility(row.get("eligibility", "")):
        return False
    if _is_generic_notes(row.get("notes", "")):
        return False
    services = [s.strip() for s in (row.get("services") or "").split("|") if s.strip()]
    if not services or {"Partner referrals", "Community support"}.issuperset(set(services)):
        return False
    return True


def enrich_row(row: dict[str, str]) -> dict[str, str]:
    if is_publication_ready(row):
        out = dict(row)
        out["intake_signals"] = serialize_intake_signals(classify_intake_signals_heuristic(out))
        return out

    desc_en, desc_es = expand_description(row)
    elig_en, elig_es = expand_eligibility(row)
    notes_en, notes_es = expand_notes(row)
    out = dict(row)
    out["description"] = desc_en
    out["description_es"] = desc_es
    out["eligibility"] = elig_en
    out["eligibility_es"] = elig_es
    out["notes"] = notes_en
    out["notes_es"] = notes_es
    out["services"] = expand_services(row)
    out["tags"] = expand_tags(row)
    if not out.get("hours") or out["hours"] == "Contact for current hours":
        out["hours"] = "Contact for current hours; confirm before visiting"
    out["intake_signals"] = serialize_intake_signals(classify_intake_signals_heuristic(out))
    return out
