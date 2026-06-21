export type SitePageKind = "template" | "dedicated";

export type SitePageDefinition = {
  slug: string;
  labelKey: string;
  publicPath: string;
  kind: SitePageKind;
  editHref?: string;
  editLabelKey?: string;
  noteKey?: string;
};

export const SITE_PAGE_DEFINITIONS: SitePageDefinition[] = [
  {
    slug: "about",
    labelKey: "admin.pages.about",
    publicPath: "/about",
    kind: "template",
    editHref: "/admin/about",
    editLabelKey: "admin.pages.editAbout",
  },
  {
    slug: "contact",
    labelKey: "admin.pages.contact",
    publicPath: "/contact",
    kind: "template",
    editHref: "/admin/contact",
    editLabelKey: "admin.pages.editContact",
    noteKey: "admin.pages.contactNote",
  },
  {
    slug: "faq",
    labelKey: "admin.pages.faq",
    publicPath: "/faq",
    kind: "dedicated",
    editHref: "/admin/faqs",
    editLabelKey: "admin.pages.editFaqs",
  },
  {
    slug: "privacy",
    labelKey: "admin.pages.privacy",
    publicPath: "/privacy",
    kind: "template",
    editHref: "/admin/legal/privacy",
    editLabelKey: "admin.pages.editPrivacy",
  },
  {
    slug: "terms",
    labelKey: "admin.pages.terms",
    publicPath: "/terms",
    kind: "template",
    editHref: "/admin/legal/terms",
    editLabelKey: "admin.pages.editTerms",
  },
  {
    slug: "accessibility",
    labelKey: "admin.pages.accessibility",
    publicPath: "/accessibility",
    kind: "template",
    editHref: "/admin/legal/accessibility",
    editLabelKey: "admin.pages.editAccessibility",
  },
];

export const TEMPLATE_MANAGED_SLUGS = new Set(
  SITE_PAGE_DEFINITIONS.filter((page) => page.kind === "template").map((page) => page.slug)
);
