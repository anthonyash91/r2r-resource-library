import type { Announcement, Category, Faq, Resource } from "@/types";
import { resolveCategoryMessageSlug } from "./category-label";
import { createTranslator } from "./translator";
import type { Locale } from "./types";

const CATEGORY_SLUG_BY_ID: Record<string, string> = {
  "cat-housing": "housing",
  "cat-employment": "employment",
  "cat-food": "food-assistance",
  "cat-healthcare": "healthcare",
  "cat-mental-health": "mental-health",
  "cat-recovery": "substance-abuse-recovery",
  "cat-transportation": "transportation",
  "cat-education": "education",
  "cat-financial": "financial-assistance",
  "cat-legal": "legal-aid",
  "cat-id": "identification-documents",
  "cat-family": "family-services",
  "cat-veterans": "veterans-services",
  "cat-disability": "disability-services",
  "cat-community": "community-support-programs",
  "cat-emergency": "emergency-assistance",
};

function categoryMessageSlug(categoryId: string, slug?: string): string {
  const resolved = slug ?? CATEGORY_SLUG_BY_ID[categoryId] ?? categoryId;
  return resolveCategoryMessageSlug(resolved);
}

export function localizeCategory(category: Category, locale: Locale): Category {
  if (locale === "en") return category;

  const { messages } = createTranslator(locale);
  const slug = categoryMessageSlug(category.id, category.slug);
  const localized = messages.categories[slug as keyof typeof messages.categories];
  if (!localized) return category;

  return {
    ...category,
    name: localized.name,
    description: localized.description,
  };
}

export function localizeCategories(categories: Category[], locale: Locale): Category[] {
  if (locale === "en") return categories;
  return categories.map((category) => localizeCategory(category, locale));
}

export function localizeResource(resource: Resource, locale: Locale, index?: number): Resource {
  if (locale === "en") return resource;

  const localizedCategory = resource.category
    ? localizeCategory(resource.category, locale)
    : resource.category;

  const hasDbLocalization =
    resource.id.startsWith("res-ky-") ||
    resource.id.startsWith("d1000001-") ||
    Boolean(resource.description_es || resource.eligibility_es || resource.notes_es);

  if (hasDbLocalization) {
    return {
      ...resource,
      ...(resource.description_es ? { description: resource.description_es } : {}),
      ...(resource.eligibility_es ? { eligibility: resource.eligibility_es } : {}),
      ...(resource.notes_es ? { notes: resource.notes_es } : {}),
      ...(localizedCategory ? { category: localizedCategory } : {}),
    };
  }

  const { t, messages } = createTranslator(locale);
  const slug = categoryMessageSlug(resource.category_id, resource.category?.slug);
  const template = messages.resourceTemplates[slug as keyof typeof messages.resourceTemplates];
  const category = messages.categories[slug as keyof typeof messages.categories];

  if (!template || !category) {
    return {
      ...resource,
      ...(localizedCategory ? { category: localizedCategory } : {}),
    };
  }

  const resourceIndex =
    index ?? (resource.id.startsWith("res-") ? Number.parseInt(resource.id.slice(4), 10) - 1 : 0);
  const prefixIndex = resourceIndex % template.namePrefixes.length;
  const namePrefix = template.namePrefixes[prefixIndex] ?? resource.name.split(" – ")[0];
  const city = resource.city ?? "";
  const state = resource.state ?? "";
  const suffix = city ? ` – ${city}` : "";

  return {
    ...resource,
    name: `${namePrefix}${suffix}`,
    description: `${template.description} ${t("mock.servingCommunities", { city, state })}`,
    eligibility: template.eligibility,
    services: [...template.services],
    hours:
      slug === "emergency-assistance" ? template.hoursEmergency : template.hoursStandard,
    category: localizedCategory ?? resource.category,
  };
}

export function localizeResources(resources: Resource[], locale: Locale): Resource[] {
  return resources.map((resource, index) => localizeResource(resource, locale, index));
}

export function localizeFaqs(faqs: Faq[], locale: Locale): Faq[] {
  return faqs;
}

export function localizeAnnouncements(
  announcements: Announcement[],
  _locale: Locale
): Announcement[] {
  return announcements;
}

export function getLocalizedHomepage(
  homepage: Record<string, string>,
  locale: Locale
): Record<string, string> {
  const { t } = createTranslator(locale);

  if (locale === "es") {
    return {
      ...homepage,
      hero_headline:
        homepage.hero_headline_es || homepage.hero_headline || t("home.heroHeadline"),
      hero_subheadline:
        homepage.hero_subheadline_es ||
        homepage.hero_subheadline ||
        t("home.heroSubheadline"),
      hero_headline_highlight:
        homepage.hero_headline_highlight_es ||
        homepage.hero_headline_highlight ||
        t("home.heroHighlight"),
    };
  }

  return {
    ...homepage,
    hero_headline: homepage.hero_headline || t("home.heroHeadline"),
    hero_subheadline: homepage.hero_subheadline || t("home.heroSubheadline"),
    hero_headline_highlight:
      homepage.hero_headline_highlight || t("home.heroHighlight"),
  };
}

export type SiteBranding = {
  brandName: string;
  navTagline: string;
  footerTagline: string;
  footerDescription: string;
};

function pickLocalizedSiteField(
  homepage: Record<string, string>,
  key: string,
  locale: Locale,
  fallbackKey: string
): string {
  const { t } = createTranslator(locale);

  if (locale === "es") {
    return homepage[`${key}_es`] || homepage[key] || t(fallbackKey);
  }

  return homepage[key] || t(fallbackKey);
}

export function resolveSiteBranding(
  homepage: Record<string, string>,
  locale: Locale
): SiteBranding {
  return {
    brandName: pickLocalizedSiteField(homepage, "nav_brand_name", locale, "nav.brandName"),
    navTagline: pickLocalizedSiteField(homepage, "nav_tagline", locale, "nav.tagline"),
    footerTagline: pickLocalizedSiteField(homepage, "footer_tagline", locale, "footer.tagline"),
    footerDescription: pickLocalizedSiteField(
      homepage,
      "footer_description",
      locale,
      "footer.description"
    ),
  };
}

type DayKey = keyof ReturnType<typeof createTranslator>["messages"]["days"];

const FULL_DAY_NAMES: [string, DayKey][] = [
  ["Sunday", "sun"],
  ["Saturday", "sat"],
  ["Thursday", "thu"],
  ["Wednesday", "wed"],
  ["Tuesday", "tue"],
  ["Monday", "mon"],
  ["Friday", "fri"],
  ["Domingo", "sun"],
  ["Sábado", "sat"],
  ["Miércoles", "wed"],
  ["Martes", "tue"],
  ["Jueves", "thu"],
  ["Viernes", "fri"],
  ["Lunes", "mon"],
];

export function formatOperatingHours(hours: string, locale: Locale): string {
  const { messages } = createTranslator(locale);
  const abbrev = messages.days;

  return FULL_DAY_NAMES.reduce(
    (result, [fullName, key]) =>
      result.replace(new RegExp(`\\b${fullName}\\b`, "gi"), abbrev[key]),
    hours
  );
}

export function localizeDayLabels(days: string[], locale: Locale): string[] {
  if (locale === "en") return days;

  const { messages } = createTranslator(locale);
  const map: Record<string, string> = {
    Mon: messages.days.mon,
    Tue: messages.days.tue,
    Wed: messages.days.wed,
    Thu: messages.days.thu,
    Fri: messages.days.fri,
    Sat: messages.days.sat,
    Sun: messages.days.sun,
  };

  return days.map((day) => map[day] ?? day);
}

export function localizeFaqCategory(category: string | null, locale: Locale): string {
  if (!category || locale === "en") return category ?? "";
  const { t } = createTranslator(locale);
  if (category === "General") return t("faq.general");
  if (category === "Using the Site") return t("faq.usingTheSite");
  return category;
}
