export const EDITABLE_SITE_CONTENT_FIELDS = [
  "hero_headline",
  "hero_subheadline",
  "hero_headline_highlight",
  "nav_brand_name",
  "nav_tagline",
  "footer_tagline",
  "footer_description",
] as const;

export type EditableSiteContentField = (typeof EDITABLE_SITE_CONTENT_FIELDS)[number];

export type SiteContentFormValues = Record<EditableSiteContentField, string>;
