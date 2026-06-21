export type LegalDocumentSlug = "privacy" | "terms";

export type LegalSectionConfig = {
  id: string;
  bullets?: readonly string[];
  contactLink?: boolean;
};

export const LEGAL_DOCUMENT_CONFIG: Record<
  LegalDocumentSlug,
  { prefix: string; sections: LegalSectionConfig[] }
> = {
  privacy: {
    prefix: "legal_privacy",
    sections: [
      { id: "s1" },
      { id: "s2", bullets: ["b1", "b2", "b3", "b4"] },
      { id: "s3" },
      { id: "s4" },
      { id: "s5", bullets: ["b1", "b2", "b3", "b4", "b5"] },
      { id: "s6", bullets: ["b1", "b2", "b3", "b4"] },
      { id: "s7" },
      { id: "s8" },
      { id: "s9", contactLink: true },
    ],
  },
  terms: {
    prefix: "legal_terms",
    sections: [
      { id: "s1" },
      { id: "s2" },
      { id: "s3" },
      { id: "s4", bullets: ["b1", "b2", "b3", "b4", "b5", "b6"] },
      { id: "s5" },
      { id: "s6" },
      { id: "s7" },
      { id: "s8" },
      { id: "s9" },
      { id: "s10", contactLink: true },
    ],
  },
};

export const ACCESSIBILITY_PRINCIPLE_KEYS = [
  "perceivable",
  "operable",
  "understandable",
  "robust",
] as const;

export const ACCESSIBILITY_FEATURE_KEYS = [
  "keyboard",
  "screenReader",
  "plainLanguage",
  "mobile",
] as const;

function buildLegalDocumentFields(slug: LegalDocumentSlug): string[] {
  const config = LEGAL_DOCUMENT_CONFIG[slug];
  const fields = [
    `${config.prefix}_title`,
    `${config.prefix}_description`,
    `${config.prefix}_intro`,
    `${config.prefix}_last_updated`,
    `${config.prefix}_contact_prompt`,
  ];

  for (const section of config.sections) {
    fields.push(`${config.prefix}_${section.id}_title`, `${config.prefix}_${section.id}_body`);
    for (const bullet of section.bullets ?? []) {
      fields.push(`${config.prefix}_${section.id}_bullet_${bullet}`);
    }
  }

  return fields;
}

export const EDITABLE_PRIVACY_CONTENT_FIELDS = buildLegalDocumentFields("privacy");
export const EDITABLE_TERMS_CONTENT_FIELDS = buildLegalDocumentFields("terms");

export const EDITABLE_ACCESSIBILITY_CONTENT_FIELDS = [
  "legal_accessibility_title",
  "legal_accessibility_description",
  "legal_accessibility_last_updated",
  "legal_accessibility_commitment_title",
  "legal_accessibility_commitment_p1",
  "legal_accessibility_commitment_p2",
  "legal_accessibility_wcag_title",
  ...ACCESSIBILITY_PRINCIPLE_KEYS.flatMap((key) => [
    `legal_accessibility_principle_${key}_title`,
    `legal_accessibility_principle_${key}_body`,
  ]),
  "legal_accessibility_features_title",
  ...ACCESSIBILITY_FEATURE_KEYS.flatMap((key) => [
    `legal_accessibility_feature_${key}_title`,
    `legal_accessibility_feature_${key}_body`,
  ]),
  "legal_accessibility_limitations_title",
  "legal_accessibility_limitations_body",
  "legal_accessibility_report_title",
  "legal_accessibility_report_body",
] as const;

export type LegalDocumentFormValues = Record<string, string>;
export type AccessibilityContentFormValues = Record<
  (typeof EDITABLE_ACCESSIBILITY_CONTENT_FIELDS)[number],
  string
>;
