import {
  EDITABLE_CONTACT_CONTENT_FIELDS,
  type ContactContentFormValues,
  type ContactPageContent,
} from "@/lib/contact-content-fields";
import { createTranslator } from "@/i18n/translator";
import type { Locale } from "@/i18n/types";

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

export function buildContactContentDefaults(
  translate: (key: string, params?: Record<string, string | number>) => string
): ContactContentFormValues {
  return {
    contact_hero_title: translate("contact.defaultTitle"),
    contact_hero_description: translate("contact.description"),
    contact_form_title: translate("contact.formTitle"),
    contact_other_ways_title: translate("contact.otherWaysTitle"),
    contact_response_time_title: translate("contact.responseTimeTitle"),
    contact_response_time_body: translate("contact.responseTimeBody", {
      timeframe: translate("contact.responseTimeframe"),
    }),
    contact_help_faqs_title: translate("contact.helpLinks.faqsTitle"),
    contact_help_faqs_desc: translate("contact.helpLinks.faqsDesc"),
    contact_help_resources_title: translate("contact.helpLinks.resourcesTitle"),
    contact_help_resources_desc: translate("contact.helpLinks.resourcesDesc"),
    contact_help_suggest_title: translate("contact.helpLinks.suggestTitle"),
    contact_help_suggest_desc: translate("contact.helpLinks.suggestDesc"),
  };
}

export function resolveContactPageContent(
  store: Record<string, string>,
  locale: Locale
): ContactPageContent {
  const { t } = createTranslator(locale);
  const defaults = buildContactContentDefaults(t);

  return {
    heroTitle: pickField(store, "contact_hero_title", locale, defaults.contact_hero_title),
    heroDescription: pickField(
      store,
      "contact_hero_description",
      locale,
      defaults.contact_hero_description
    ),
    formTitle: pickField(store, "contact_form_title", locale, defaults.contact_form_title),
    otherWaysTitle: pickField(
      store,
      "contact_other_ways_title",
      locale,
      defaults.contact_other_ways_title
    ),
    responseTimeTitle: pickField(
      store,
      "contact_response_time_title",
      locale,
      defaults.contact_response_time_title
    ),
    responseTimeBody: pickField(
      store,
      "contact_response_time_body",
      locale,
      defaults.contact_response_time_body
    ),
    helpLinks: {
      faqs: {
        title: pickField(store, "contact_help_faqs_title", locale, defaults.contact_help_faqs_title),
        description: pickField(
          store,
          "contact_help_faqs_desc",
          locale,
          defaults.contact_help_faqs_desc
        ),
      },
      resources: {
        title: pickField(
          store,
          "contact_help_resources_title",
          locale,
          defaults.contact_help_resources_title
        ),
        description: pickField(
          store,
          "contact_help_resources_desc",
          locale,
          defaults.contact_help_resources_desc
        ),
      },
      suggest: {
        title: pickField(
          store,
          "contact_help_suggest_title",
          locale,
          defaults.contact_help_suggest_title
        ),
        description: pickField(
          store,
          "contact_help_suggest_desc",
          locale,
          defaults.contact_help_suggest_desc
        ),
      },
    },
  };
}

export function getContactContentAdminValues(
  store: Record<string, string>,
  locale: Locale
): ContactContentFormValues {
  const defaults = buildContactContentDefaults(createTranslator(locale).t);

  return EDITABLE_CONTACT_CONTENT_FIELDS.reduce((acc, field) => {
    acc[field] = store[field] || defaults[field];
    return acc;
  }, {} as ContactContentFormValues);
}

export { EDITABLE_CONTACT_CONTENT_FIELDS };
