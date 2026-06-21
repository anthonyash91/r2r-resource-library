import type { Category } from "@/types";

/** Legacy mock category slugs mapped to current Kentucky directory slugs. */
const CATEGORY_SLUG_ALIASES: Record<string, string> = {
  "food-assistance": "food-nutrition",
  "substance-abuse-recovery": "substance-use-treatment",
  "identification-documents": "id-documentation",
  "family-services": "family-children",
  "veterans-services": "veterans",
  "community-support-programs": "reentry-organizations",
  "emergency-assistance": "basic-needs",
};

export function resolveCategoryMessageSlug(slug: string): string {
  return CATEGORY_SLUG_ALIASES[slug] ?? slug;
}

export function getCategoryLabel(
  category: Pick<Category, "name" | "slug">,
  t: (key: string) => string
): string {
  const messageSlug = resolveCategoryMessageSlug(category.slug);
  const key = `categories.${messageSlug}.name`;
  const translated = t(key);
  return translated === key ? category.name : translated;
}
