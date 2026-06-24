import { KENTUCKY_CATEGORIES } from "../src/lib/kentucky/categories";

export const CATEGORY_UUID = Object.fromEntries(
  KENTUCKY_CATEGORIES.map((category, index) => [
    category.slug,
    `c1000001-${String(index + 1).padStart(4, "0")}-4000-8000-000000000001`,
  ])
);

const CATEGORY_ALIASES: Record<string, string> = {
  "state agency": "state-agency",
  housing: "housing",
  employment: "employment",
  healthcare: "healthcare",
  "health care": "healthcare",
  "mental health": "healthcare",
  "substance use": "substance-use-treatment",
  "substance use treatment": "substance-use-treatment",
  recovery: "substance-use-treatment",
  "legal aid": "legal-aid",
  legal: "legal-aid",
  "food & nutrition": "food-nutrition",
  "food assistance": "food-nutrition",
  food: "food-nutrition",
  "id & documentation": "id-documentation",
  identification: "id-documentation",
  ids: "id-documentation",
  "financial assistance": "financial-assistance",
  financial: "financial-assistance",
  transportation: "transportation",
  transit: "transportation",
  "family & children": "family-children",
  family: "family-children",
  "peer support": "peer-support",
  education: "education",
  veterans: "veterans",
  "basic needs": "basic-needs",
  "probation & parole": "probation-parole",
  probation: "probation-parole",
  parole: "probation-parole",
  "reentry organizations": "reentry-organizations",
  reentry: "reentry-organizations",
  nonprofit: "reentry-organizations",
};

function normalizeKey(value: string) {
  return value.trim().toLowerCase().replace(/\s+/g, " ");
}

export function resolveCategorySlug(raw: string): string | null {
  const key = normalizeKey(raw);
  if (!key) return null;

  if (CATEGORY_UUID[key]) return key;

  const alias = CATEGORY_ALIASES[key];
  if (alias) return alias;

  const bySlug = KENTUCKY_CATEGORIES.find((c) => normalizeKey(c.slug) === key);
  if (bySlug) return bySlug.slug;

  const byName = KENTUCKY_CATEGORIES.find((c) => normalizeKey(c.name) === key);
  if (byName) return byName.slug;

  const byPartial = KENTUCKY_CATEGORIES.find(
    (c) => key.includes(normalizeKey(c.name)) || normalizeKey(c.name).includes(key)
  );
  return byPartial?.slug ?? null;
}

export function resolveCategoryId(raw: string): string | null {
  const slug = resolveCategorySlug(raw);
  return slug ? CATEGORY_UUID[slug] : null;
}
