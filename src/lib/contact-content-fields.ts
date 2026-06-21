export const EDITABLE_CONTACT_CONTENT_FIELDS = [
  "contact_hero_title",
  "contact_hero_description",
  "contact_form_title",
  "contact_other_ways_title",
  "contact_response_time_title",
  "contact_response_time_body",
  "contact_help_faqs_title",
  "contact_help_faqs_desc",
  "contact_help_resources_title",
  "contact_help_resources_desc",
  "contact_help_suggest_title",
  "contact_help_suggest_desc",
] as const;

export type EditableContactContentField = (typeof EDITABLE_CONTACT_CONTENT_FIELDS)[number];

export type ContactContentFormValues = Record<EditableContactContentField, string>;

export type ContactPageContent = {
  heroTitle: string;
  heroDescription: string;
  formTitle: string;
  otherWaysTitle: string;
  responseTimeTitle: string;
  responseTimeBody: string;
  helpLinks: {
    faqs: { title: string; description: string };
    resources: { title: string; description: string };
    suggest: { title: string; description: string };
  };
};
