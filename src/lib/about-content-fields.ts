export const ABOUT_AUDIENCE_KEYS = [
  "about_audience_1",
  "about_audience_2",
  "about_audience_3",
  "about_audience_4",
  "about_audience_5",
  "about_audience_6",
] as const;

export const ABOUT_SERVE_CARD_KEYS = [
  "housing",
  "employment",
  "healthcare",
  "legal",
] as const;

export const ABOUT_VALUE_KEYS = [
  "dignity",
  "accessibility",
  "community",
  "trust",
] as const;

export const EDITABLE_ABOUT_CONTENT_FIELDS = [
  "about_hero_title",
  "about_hero_description",
  "about_mission_title",
  "about_mission_p1",
  "about_mission_p2",
  "about_mission_p3",
  "about_serve_title",
  "about_serve_intro",
  ...ABOUT_AUDIENCE_KEYS,
  ...ABOUT_SERVE_CARD_KEYS.flatMap((key) => [
    `about_serve_${key}_title`,
    `about_serve_${key}_desc`,
  ]),
  "about_values_title",
  "about_values_subtitle",
  ...ABOUT_VALUE_KEYS.flatMap((key) => [
    `about_values_${key}_title`,
    `about_values_${key}_body`,
  ]),
  "about_cta_title",
  "about_cta_subtitle",
  "about_cta_browse",
  "about_cta_contact",
] as const;

export type EditableAboutContentField = (typeof EDITABLE_ABOUT_CONTENT_FIELDS)[number];

export type AboutContentFormValues = Record<EditableAboutContentField, string>;

export type AboutPageContent = {
  heroTitle: string;
  heroDescription: string;
  missionTitle: string;
  missionP1: string;
  missionP2: string;
  missionP3: string;
  serveTitle: string;
  serveIntro: string;
  audience: string[];
  serveCards: Record<
    (typeof ABOUT_SERVE_CARD_KEYS)[number],
    { title: string; description: string }
  >;
  valuesTitle: string;
  valuesSubtitle: string;
  values: Record<
    (typeof ABOUT_VALUE_KEYS)[number],
    { title: string; body: string }
  >;
  ctaTitle: string;
  ctaSubtitle: string;
  ctaBrowse: string;
  ctaContact: string;
};
