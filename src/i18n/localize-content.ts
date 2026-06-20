import type { Announcement, Category, Faq, Resource } from "@/types";
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

function categorySlug(categoryId: string, slug?: string) {
  return slug ?? CATEGORY_SLUG_BY_ID[categoryId] ?? categoryId;
}

export function localizeCategories(categories: Category[], locale: Locale): Category[] {
  if (locale === "en") return categories;

  const { t, messages } = createTranslator(locale);

  return categories.map((category) => {
    const slug = categorySlug(category.id, category.slug);
    const localized = messages.categories[slug as keyof typeof messages.categories];
    if (!localized) return category;

    return {
      ...category,
      name: localized.name,
      description: localized.description,
    };
  });
}

export function localizeResource(resource: Resource, locale: Locale, index?: number): Resource {
  if (resource.id.startsWith("res-ky-")) {
    if (locale === "es" && resource.description_es) {
      return { ...resource, description: resource.description_es };
    }
    return resource;
  }

  if (locale === "en") return resource;

  const { t, messages } = createTranslator(locale);
  const slug = categorySlug(resource.category_id, resource.category?.slug);
  const template = messages.resourceTemplates[slug as keyof typeof messages.resourceTemplates];
  const category = messages.categories[slug as keyof typeof messages.categories];

  if (!template || !category) return resource;

  const resourceIndex =
    index ?? (resource.id.startsWith("res-") ? Number.parseInt(resource.id.slice(4), 10) - 1 : 0);
  const prefixIndex = resourceIndex % template.namePrefixes.length;
  const namePrefix = template.namePrefixes[prefixIndex] ?? resource.name.split(" – ")[0];
  const city = resource.city ?? "";
  const state = resource.state ?? "";
  const suffix = city ? ` – ${city}` : "";

  const localizedCategory = {
    ...resource.category!,
    name: category.name,
    description: category.description,
  };

  return {
    ...resource,
    name: `${namePrefix}${suffix}`,
    description: `${template.description} ${t("mock.servingCommunities", { city, state })}`,
    eligibility: template.eligibility,
    services: [...template.services],
    hours:
      slug === "emergency-assistance" ? template.hoursEmergency : template.hoursStandard,
    category: resource.category ? localizedCategory : resource.category,
  };
}

export function localizeResources(resources: Resource[], locale: Locale): Resource[] {
  return resources.map((resource, index) => localizeResource(resource, locale, index));
}

export function localizeFaqs(faqs: Faq[], locale: Locale): Faq[] {
  if (locale === "en") return faqs;

  const { t, messages } = createTranslator(locale);
  const faqKeys = ["faq1", "faq2", "faq3", "faq4", "faq5"] as const;

  return faqs.map((faq, index) => {
    const key = faqKeys[index];
    if (!key) return faq;
    const localized = messages.faqs[key];
    return {
      ...faq,
      question: localized.question,
      answer: localized.answer,
      category:
        localized.category === "general"
          ? t("faq.general")
          : localized.category === "usingTheSite"
            ? t("faq.usingTheSite")
            : faq.category,
    };
  });
}

export function localizeAnnouncements(
  announcements: Announcement[],
  locale: Locale
): Announcement[] {
  if (locale === "en") return announcements;

  const { t } = createTranslator(locale);

  return announcements.map((announcement, index) => {
    if (index !== 0) return announcement;
    return {
      ...announcement,
      title: t("mock.announcementTitle"),
      content: t("mock.announcementContent"),
    };
  });
}

export function getLocalizedHomepage(
  homepage: Record<string, string>,
  locale: Locale
): Record<string, string> {
  if (locale === "en") return homepage;

  const { t } = createTranslator(locale);
  return {
    ...homepage,
    hero_headline: t("home.heroHeadline"),
    hero_subheadline: t("home.heroSubheadline"),
    hero_headline_highlight: t("home.heroHighlight"),
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
