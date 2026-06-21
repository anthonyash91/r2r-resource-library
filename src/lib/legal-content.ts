import { createTranslator } from "@/i18n/translator";
import type { Locale } from "@/i18n/types";
import type { LegalSection } from "@/components/legal/legal-document-view";
import {
  ACCESSIBILITY_FEATURE_KEYS,
  ACCESSIBILITY_PRINCIPLE_KEYS,
  EDITABLE_ACCESSIBILITY_CONTENT_FIELDS,
  EDITABLE_PRIVACY_CONTENT_FIELDS,
  EDITABLE_TERMS_CONTENT_FIELDS,
  LEGAL_DOCUMENT_CONFIG,
  type AccessibilityContentFormValues,
  type LegalDocumentSlug,
} from "@/lib/legal-content-fields";

function pickField(
  store: Record<string, string>,
  key: string,
  locale: Locale,
  fallback: string
): string {
  if (locale === "es") {
    return store[`${key}_es`] || store[key] || fallback;
  }
  return store[key] || fallback;
}

function legalDocI18nPrefix(slug: LegalDocumentSlug): string {
  return slug === "privacy" ? "legal.privacy" : "legal.terms";
}

export function buildLegalDocumentDefaults(
  slug: LegalDocumentSlug,
  translate: (key: string) => string
): Record<string, string> {
  const config = LEGAL_DOCUMENT_CONFIG[slug];
  const prefix = config.prefix;
  const docKey = legalDocI18nPrefix(slug);

  const values: Record<string, string> = {
    [`${prefix}_title`]: translate(`${docKey}.title`),
    [`${prefix}_description`]: translate(`${docKey}.description`),
    [`${prefix}_intro`]: translate(`${docKey}.intro`),
    [`${prefix}_last_updated`]: translate(`${docKey}.lastUpdatedDate`),
    [`${prefix}_contact_prompt`]: translate(`${docKey}.contactPrompt`),
  };

  for (const section of config.sections) {
    values[`${prefix}_${section.id}_title`] = translate(`${docKey}.sections.${section.id}.title`);
    values[`${prefix}_${section.id}_body`] = translate(`${docKey}.sections.${section.id}.body`);
    for (const bullet of section.bullets ?? []) {
      values[`${prefix}_${section.id}_bullet_${bullet}`] = translate(
        `${docKey}.sections.${section.id}.bullets.${bullet}`
      );
    }
  }

  return values;
}

export function buildAccessibilityContentDefaults(
  translate: (key: string) => string
): AccessibilityContentFormValues {
  const values = {
    legal_accessibility_title: translate("legal.accessibility.title"),
    legal_accessibility_description: translate("legal.accessibility.description"),
    legal_accessibility_last_updated: translate("legal.accessibility.lastUpdatedDate"),
    legal_accessibility_commitment_title: translate("legal.accessibility.commitmentTitle"),
    legal_accessibility_commitment_p1: translate("legal.accessibility.commitmentP1"),
    legal_accessibility_commitment_p2: translate("legal.accessibility.commitmentP2"),
    legal_accessibility_wcag_title: translate("legal.accessibility.wcagTitle"),
    legal_accessibility_limitations_title: translate("legal.accessibility.limitationsTitle"),
    legal_accessibility_limitations_body: translate("legal.accessibility.limitationsBody"),
    legal_accessibility_report_title: translate("legal.accessibility.reportTitle"),
    legal_accessibility_report_body: translate("legal.accessibility.reportBody"),
    legal_accessibility_features_title: translate("legal.accessibility.featuresTitle"),
  } as AccessibilityContentFormValues;

  for (const key of ACCESSIBILITY_PRINCIPLE_KEYS) {
    values[`legal_accessibility_principle_${key}_title`] = translate(
      `legal.accessibility.principles.${key}.title`
    );
    values[`legal_accessibility_principle_${key}_body`] = translate(
      `legal.accessibility.principles.${key}.body`
    );
  }

  for (const key of ACCESSIBILITY_FEATURE_KEYS) {
    values[`legal_accessibility_feature_${key}_title`] = translate(
      `legal.accessibility.features.${key}.title`
    );
    values[`legal_accessibility_feature_${key}_body`] = translate(
      `legal.accessibility.features.${key}.body`
    );
  }

  return values;
}

export type LegalDocumentPageContent = {
  title: string;
  description: string;
  intro: string;
  lastUpdatedDate: string;
  contactPrompt: string;
  sections: LegalSection[];
};

export type AccessibilityPageContent = {
  title: string;
  description: string;
  lastUpdatedDate: string;
  commitmentTitle: string;
  commitmentP1: string;
  commitmentP2: string;
  wcagTitle: string;
  principles: { key: (typeof ACCESSIBILITY_PRINCIPLE_KEYS)[number]; title: string; body: string }[];
  featuresTitle: string;
  features: { key: (typeof ACCESSIBILITY_FEATURE_KEYS)[number]; title: string; body: string }[];
  limitationsTitle: string;
  limitationsBody: string;
  reportTitle: string;
  reportBody: string;
};

export function resolveLegalDocumentContent(
  slug: LegalDocumentSlug,
  store: Record<string, string>,
  locale: Locale
): LegalDocumentPageContent {
  const { t } = createTranslator(locale);
  const defaults = buildLegalDocumentDefaults(slug, t);
  const config = LEGAL_DOCUMENT_CONFIG[slug];
  const prefix = config.prefix;

  const pick = (key: string) => pickField(store, key, locale, defaults[key] ?? "");

  const sections: LegalSection[] = config.sections.map((section) => {
    const body = pick(`${prefix}_${section.id}_body`);
    return {
      title: pick(`${prefix}_${section.id}_title`),
      paragraphs: body.length > 0 ? [body] : undefined,
      bullets: section.bullets?.map((bullet) => pick(`${prefix}_${section.id}_bullet_${bullet}`)),
      contactLink: section.contactLink,
    };
  });

  return {
    title: pick(`${prefix}_title`),
    description: pick(`${prefix}_description`),
    intro: pick(`${prefix}_intro`),
    lastUpdatedDate: pick(`${prefix}_last_updated`),
    contactPrompt: pick(`${prefix}_contact_prompt`),
    sections,
  };
}

export function resolveAccessibilityPageContent(
  store: Record<string, string>,
  locale: Locale
): AccessibilityPageContent {
  const { t } = createTranslator(locale);
  const defaults = buildAccessibilityContentDefaults(t);
  const pick = (key: keyof AccessibilityContentFormValues) =>
    pickField(store, key, locale, defaults[key]);

  return {
    title: pick("legal_accessibility_title"),
    description: pick("legal_accessibility_description"),
    lastUpdatedDate: pick("legal_accessibility_last_updated"),
    commitmentTitle: pick("legal_accessibility_commitment_title"),
    commitmentP1: pick("legal_accessibility_commitment_p1"),
    commitmentP2: pick("legal_accessibility_commitment_p2"),
    wcagTitle: pick("legal_accessibility_wcag_title"),
    principles: ACCESSIBILITY_PRINCIPLE_KEYS.map((key) => ({
      key,
      title: pick(`legal_accessibility_principle_${key}_title`),
      body: pick(`legal_accessibility_principle_${key}_body`),
    })),
    featuresTitle: pick("legal_accessibility_features_title"),
    features: ACCESSIBILITY_FEATURE_KEYS.map((key) => ({
      key,
      title: pick(`legal_accessibility_feature_${key}_title`),
      body: pick(`legal_accessibility_feature_${key}_body`),
    })),
    limitationsTitle: pick("legal_accessibility_limitations_title"),
    limitationsBody: pick("legal_accessibility_limitations_body"),
    reportTitle: pick("legal_accessibility_report_title"),
    reportBody: pick("legal_accessibility_report_body"),
  };
}

export function getLegalDocumentAdminValues(
  slug: LegalDocumentSlug,
  store: Record<string, string>,
  locale: Locale
): Record<string, string> {
  const defaults = buildLegalDocumentDefaults(slug, createTranslator(locale).t);
  const fields = slug === "privacy" ? EDITABLE_PRIVACY_CONTENT_FIELDS : EDITABLE_TERMS_CONTENT_FIELDS;

  return fields.reduce(
    (acc, field) => {
      acc[field] = store[field] || defaults[field] || "";
      return acc;
    },
    {} as Record<string, string>
  );
}

export function getAccessibilityContentAdminValues(
  store: Record<string, string>,
  locale: Locale
): AccessibilityContentFormValues {
  const defaults = buildAccessibilityContentDefaults(createTranslator(locale).t);

  return EDITABLE_ACCESSIBILITY_CONTENT_FIELDS.reduce((acc, field) => {
    acc[field] = store[field] || defaults[field];
    return acc;
  }, {} as AccessibilityContentFormValues);
}

export function getEditableFieldsForLegalDocument(
  slug: LegalDocumentSlug
): readonly string[] {
  return slug === "privacy" ? EDITABLE_PRIVACY_CONTENT_FIELDS : EDITABLE_TERMS_CONTENT_FIELDS;
}

export {
  EDITABLE_ACCESSIBILITY_CONTENT_FIELDS,
  EDITABLE_PRIVACY_CONTENT_FIELDS,
  EDITABLE_TERMS_CONTENT_FIELDS,
  LEGAL_DOCUMENT_CONFIG,
};
