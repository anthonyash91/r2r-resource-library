"""Merge near-duplicate canonical service labels into a smaller user-facing set."""

from __future__ import annotations

# Intermediate labels (rules / legacy CSV) → final filter label
CANONICAL_CONSOLIDATION: dict[str, str] = {
    # Navigation & coordination
    "Information and referral": "Partner referrals",
    "Legal aid referrals": "Partner referrals",
    "Coalition coordination": "Reentry navigation",
    "Case management": "Reentry navigation",
    "Aftercare planning": "Reentry navigation",
    # Benefits (keep SNAP / Medicaid / TANF as program-specific)
    "Benefits enrollment": "Benefits navigation",
    "Benefits advocacy": "Benefits navigation",
    "Benefits appeals": "Benefits navigation",
    "Application assistance": "Benefits navigation",
    "Health insurance enrollment": "Benefits navigation",
    "Social Security assistance": "Benefits navigation",
    "VA benefits navigation": "Benefits navigation",
    "Unemployment assistance": "Benefits navigation",
    "Advocacy": "Benefits navigation",
    # Employment
    "Job placement": "Employment assistance",
    "Career counseling": "Employment assistance",
    "Interview preparation": "Job readiness training",
    "Resume help": "Job readiness training",
    "Skills training": "Job readiness training",
    "Career training and certifications": "Job readiness training",
    "Apprenticeships": "Workforce development",
    "Vocational rehabilitation": "Workforce development",
    # Documents & IDs
    "Birth certificate assistance": "Document assistance",
    "ID assistance": "Document assistance",
    "Driver's license services": "Document assistance",
    "Vital records services": "Document assistance",
    # Food
    "Emergency food assistance": "Food pantry access",
    "Community meals": "Food pantry access",
    # Financial / basic needs
    "Emergency financial assistance": "Rent and utility assistance",
    "Budgeting and financial coaching": "Basic needs assistance",
    "Banking access": "Basic needs assistance",
    # Legal
    "Consumer legal help": "Civil legal representation",
    "Court advocacy": "Civil legal representation",
    # Supervision
    "Alternative to incarceration": "Community supervision",
    "Work release programs": "Community supervision",
    # Housing
    "Affordable housing": "Supportive housing",
    "Homeownership assistance": "Housing navigation",
    "Landlord outreach": "Housing navigation",
    # Education
    "Adult education": "GED and high school equivalency",
    "Adult literacy and ESL": "GED and high school equivalency",
    # Behavioral health
    "Mental health referrals": "Behavioral health services",
    "Trauma-informed counseling": "Counseling",
    "Anger management": "Counseling",
    "Bereavement support": "Counseling",
    # Substance use
    "Substance use counseling": "Substance use treatment",
    "Substance use screening": "Substance use treatment",
    "Outpatient treatment": "Substance use treatment",
    "Residential treatment": "Substance use treatment",
    "Detox services": "Substance use treatment",
    "Addiction recovery support": "Substance use treatment",
    "Addiction medicine": "Substance use treatment",
    "MAT referrals": "Addiction treatment referrals",
    "12-step programs": "Support groups",
    "Peer support": "Support groups",
    # Healthcare
    "Transitional healthcare navigation": "Primary medical care",
    "Sliding-fee care": "Primary medical care",
    "Dental services": "Primary medical care",
    "Chronic care management": "Primary medical care",
    # Family & youth
    "Youth mentoring": "Children's services",
    "Co-parenting support": "Parenting services",
    "Child support services": "Parenting services",
}


def consolidate_canonical(label: str) -> str:
    """Return the user-facing label for a classified service name."""
    trimmed = label.strip()
    if not trimmed:
        return ""
    return CANONICAL_CONSOLIDATION.get(trimmed, trimmed)
