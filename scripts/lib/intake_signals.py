"""Heuristic intake signal classifier for resource CSV rows.

Keep in sync with scripts/lib/classify-intake-signals.ts (TypeScript twin).
"""
from __future__ import annotations

import re
from typing import TypedDict

INTAKE_SIGNALS = (
    "accepts_criminal_record",
    "referral_required",
    "walk_in_ok",
)

EXCLUDE_ALL_SIGNALS = (
    r"\b988\b",
    r"suicide.*crisis",
    r"crisis text line",
    r"crisis lifeline",
    r"\bhotline\b",
    r"phone line",
    r"navigation hub",
    r"information portal",
    r"online resource hub",
    r"not reentry-specific",
    r"available to anyone",
    r"referral resource for ohioans",
    r"this entry describes a navigation hub",
    r"does not replace direct services",
    r"state offices provide information and referrals statewide",
    r"findtreatment\.gov",
    r"samhsa online locator",
    r"official samhsa",
    r"provider search",
)

ACCEPTS_CRIMINAL_RECORD = (
    r"justice[- ]involved",
    r"criminal record",
    r"\bfelony\b",
    r"\breentry\b",
    r"expungement",
    r"fair[- ]chance",
    r"returning citizen",
    r"formerly incarcerat",
    r"released from (?:prison|incarceration)",
    r"people with convictions",
    r"record seal",
    r"record relief",
    r"halfway house",
    r"reentry service center",
    r"transitional work",
    r"doc[- ]contract",
    r"parole eligib",
    r"veterans treatment court",
    r"drug court",
    r"restored citizen",
)

ACCEPTS_CRIMINAL_RECORD_BLOCK = (
    r"criminal record is (?:generally )?not a barrier",
    r"does not usually require a criminal-record disclosure",
    r"available to anyone in",
    r"open to all(?: ohio| kentucky)?",
    r"all ohioans",
    r"all kentuckians",
    r"information and referral only",
)

REFERRAL_REQUIRED = (
    r"referral required",
    r"requires (?:an )?(?:institutional )?referral",
    r"by referral only",
    r"referral from (?:doc|the bureau|corrections|courts|parole|p(?:&|&amp;)p)",
    r"institutional referral",
    r"through the court system only",
    r"access is through the court",
    r"court[- ]ordered",
    r"court referral",
    r"referral through the court",
    r"must be referred",
    r"parole officer referral",
    r"referral from corrections",
    r"referral from courts",
    r"doc[- ]approved",
    r"state inmates near parole",
)

REFERRAL_BLOCK = (
    r"self[- ]referral",
    r"no referral required",
    r"open self-referral",
)

WALK_IN_OK = (
    r"walk[- ]in (?:hours|services|clinic|intake|welcome)",
    r"drop[- ]in (?:hours|services|clinic)",
    r"no appointment (?:necessary|required|needed)",
    r"open intake hours",
    r"for walk-in services",
    r"second chance community legal clinic",
)

WALK_IN_BLOCK = (
    r"appointment required",
    r"by appointment only",
    r"call for appointment",
    r"not a walk-in",
    r"registration opens before",
    r"intake typically requires",
    r"central intake required before",
    r"whether walk-ins or referrals are accepted",
    r"walk-ins or referrals",
    r"confirm current intake steps",
)


class ResourceRow(TypedDict, total=False):
    name: str
    category: str
    description: str
    eligibility: str
    notes: str
    services: str
    tags: str


def _corpus(row: ResourceRow) -> str:
    parts = [
        row.get("name") or "",
        row.get("category") or "",
        row.get("description") or "",
        row.get("eligibility") or "",
        row.get("notes") or "",
        row.get("services") or "",
        row.get("tags") or "",
    ]
    return " ".join(p for p in parts if p).lower()


def _matches_any(text: str, patterns: tuple[str, ...]) -> bool:
    return any(re.search(pattern, text) for pattern in patterns)


def classify_intake_signals_heuristic(row: ResourceRow) -> list[str]:
    text = _corpus(row)
    signals: list[str] = []

    if _matches_any(text, EXCLUDE_ALL_SIGNALS):
        return signals

    if (
        _matches_any(text, ACCEPTS_CRIMINAL_RECORD)
        and not _matches_any(text, ACCEPTS_CRIMINAL_RECORD_BLOCK)
    ):
        signals.append("accepts_criminal_record")

    if _matches_any(text, REFERRAL_REQUIRED) and not _matches_any(text, REFERRAL_BLOCK):
        signals.append("referral_required")

    if (
        _matches_any(text, WALK_IN_OK)
        and not _matches_any(text, WALK_IN_BLOCK)
        and "referral_required" not in signals
    ):
        signals.append("walk_in_ok")

    return [s for s in signals if s in INTAKE_SIGNALS]


def serialize_intake_signals(signals: list[str]) -> str:
    return "|".join(signals)
