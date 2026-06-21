import {
  ABOUT_AUDIENCE_KEYS,
  ABOUT_SERVE_CARD_KEYS,
  ABOUT_VALUE_KEYS,
  EDITABLE_ABOUT_CONTENT_FIELDS,
  type AboutContentFormValues,
  type AboutPageContent,
} from "@/lib/about-content-fields";
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

export function buildAboutContentDefaults(
  translate: (key: string) => string
): AboutContentFormValues {
  return {
    about_hero_title: translate("about.defaultTitle"),
    about_hero_description: translate("about.description"),
    about_mission_title: translate("about.missionTitle"),
    about_mission_p1: translate("about.missionP1"),
    about_mission_p2: translate("about.missionP2"),
    about_mission_p3: translate("about.missionP3"),
    about_serve_title: translate("about.serveTitle"),
    about_serve_intro: translate("about.serveIntro"),
    about_audience_1: translate("about.audience.item1"),
    about_audience_2: translate("about.audience.item2"),
    about_audience_3: translate("about.audience.item3"),
    about_audience_4: translate("about.audience.item4"),
    about_audience_5: translate("about.audience.item5"),
    about_audience_6: translate("about.audience.item6"),
    about_serve_housing_title: translate("about.serveCards.housing.title"),
    about_serve_housing_desc: translate("about.serveCards.housing.desc"),
    about_serve_employment_title: translate("about.serveCards.employment.title"),
    about_serve_employment_desc: translate("about.serveCards.employment.desc"),
    about_serve_healthcare_title: translate("about.serveCards.healthcare.title"),
    about_serve_healthcare_desc: translate("about.serveCards.healthcare.desc"),
    about_serve_legal_title: translate("about.serveCards.legal.title"),
    about_serve_legal_desc: translate("about.serveCards.legal.desc"),
    about_values_title: translate("about.valuesTitle"),
    about_values_subtitle: translate("about.valuesSubtitle"),
    about_values_dignity_title: translate("about.values.dignity.title"),
    about_values_dignity_body: translate("about.values.dignity.body"),
    about_values_accessibility_title: translate("about.values.accessibility.title"),
    about_values_accessibility_body: translate("about.values.accessibility.body"),
    about_values_community_title: translate("about.values.community.title"),
    about_values_community_body: translate("about.values.community.body"),
    about_values_trust_title: translate("about.values.trust.title"),
    about_values_trust_body: translate("about.values.trust.body"),
    about_cta_title: translate("about.ctaTitle"),
    about_cta_subtitle: translate("about.ctaSubtitle"),
    about_cta_browse: translate("about.ctaBrowse"),
    about_cta_contact: translate("about.ctaContact"),
  };
}

export function resolveAboutPageContent(
  store: Record<string, string>,
  locale: Locale
): AboutPageContent {
  const { t } = createTranslator(locale);
  const defaults = buildAboutContentDefaults(t);

  return {
    heroTitle: pickField(store, "about_hero_title", locale, defaults.about_hero_title),
    heroDescription: pickField(
      store,
      "about_hero_description",
      locale,
      defaults.about_hero_description
    ),
    missionTitle: pickField(store, "about_mission_title", locale, defaults.about_mission_title),
    missionP1: pickField(store, "about_mission_p1", locale, defaults.about_mission_p1),
    missionP2: pickField(store, "about_mission_p2", locale, defaults.about_mission_p2),
    missionP3: pickField(store, "about_mission_p3", locale, defaults.about_mission_p3),
    serveTitle: pickField(store, "about_serve_title", locale, defaults.about_serve_title),
    serveIntro: pickField(store, "about_serve_intro", locale, defaults.about_serve_intro),
    audience: ABOUT_AUDIENCE_KEYS.map((key) =>
      pickField(store, key, locale, defaults[key])
    ),
    serveCards: Object.fromEntries(
      ABOUT_SERVE_CARD_KEYS.map((key) => [
        key,
        {
          title: pickField(
            store,
            `about_serve_${key}_title`,
            locale,
            defaults[`about_serve_${key}_title` as EditableAboutContentField]
          ),
          description: pickField(
            store,
            `about_serve_${key}_desc`,
            locale,
            defaults[`about_serve_${key}_desc` as EditableAboutContentField]
          ),
        },
      ])
    ) as AboutPageContent["serveCards"],
    valuesTitle: pickField(store, "about_values_title", locale, defaults.about_values_title),
    valuesSubtitle: pickField(
      store,
      "about_values_subtitle",
      locale,
      defaults.about_values_subtitle
    ),
    values: Object.fromEntries(
      ABOUT_VALUE_KEYS.map((key) => [
        key,
        {
          title: pickField(
            store,
            `about_values_${key}_title`,
            locale,
            defaults[`about_values_${key}_title` as EditableAboutContentField]
          ),
          body: pickField(
            store,
            `about_values_${key}_body`,
            locale,
            defaults[`about_values_${key}_body` as EditableAboutContentField]
          ),
        },
      ])
    ) as AboutPageContent["values"],
    ctaTitle: pickField(store, "about_cta_title", locale, defaults.about_cta_title),
    ctaSubtitle: pickField(store, "about_cta_subtitle", locale, defaults.about_cta_subtitle),
    ctaBrowse: pickField(store, "about_cta_browse", locale, defaults.about_cta_browse),
    ctaContact: pickField(store, "about_cta_contact", locale, defaults.about_cta_contact),
  };
}

export function getAboutContentAdminValues(
  store: Record<string, string>,
  locale: Locale
): AboutContentFormValues {
  const defaults = buildAboutContentDefaults(createTranslator(locale).t);

  return EDITABLE_ABOUT_CONTENT_FIELDS.reduce((acc, field) => {
    acc[field] = store[field] || defaults[field];
    return acc;
  }, {} as AboutContentFormValues);
}

export { EDITABLE_ABOUT_CONTENT_FIELDS };
