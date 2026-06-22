export type BreadcrumbItem = {
  href: string;
  label: string;
};

const HIDDEN_PATHS = new Set(["/", "/login", "/signup"]);

const SEGMENT_KEYS: Record<string, string> = {
  about: "about.title",
  contact: "contact.title",
  faq: "faq.heading",
  privacy: "legal.privacy.title",
  terms: "legal.terms.title",
  accessibility: "legal.accessibility.title",
  saved: "saved.title",
  dashboard: "dashboard.title",
  admin: "admin.portal",
  categories: "admin.categories",
  users: "admin.users",
  cms: "admin.sitePages",
  announcements: "admin.announcements",
  faqs: "admin.faqs",
  homepage: "admin.homepage",
};

function segmentLabel(
  segment: string,
  segments: string[],
  translate: (key: string) => string
): string | null {
  if (segment === "resources") {
    return segments[0] === "admin"
      ? translate("admin.resources")
      : translate("nav.findResources");
  }

  const key = SEGMENT_KEYS[segment];
  return key ? translate(key) : null;
}

export function buildBreadcrumbs(
  pathname: string,
  translate: (key: string) => string,
  currentLabel: string | null
): BreadcrumbItem[] | null {
  if (HIDDEN_PATHS.has(pathname)) return null;

  const segments = pathname.split("/").filter(Boolean);
  if (segments.length === 0) return null;
  if (segments[0] === "admin") return null;

  const items: BreadcrumbItem[] = [{ href: "/", label: translate("breadcrumb.home") }];
  let path = "";

  for (let i = 0; i < segments.length; i++) {
    const segment = segments[i];
    const next = segments[i + 1];
    path += `/${segment}`;

    if (next === "edit") continue;

    if (segment === "edit") {
      items.push({
        href: path,
        label: currentLabel ?? translate("admin.editResourceTitle"),
      });
      continue;
    }

    if (segment === "new") {
      const label =
        segments[i - 1] === "resources"
          ? translate("admin.addResource")
          : translate("admin.newPage");
      items.push({ href: path, label });
      continue;
    }

    if (segments[0] === "resources" && segments.length === 2 && i === 1) {
      items.push({
        href: path,
        label: currentLabel ?? translate("breadcrumb.resourceDetail"),
      });
      continue;
    }

    const label = segmentLabel(segment, segments, translate);
    if (label) {
      items.push({ href: path, label });
    }
  }

  return items.length > 1 ? items : null;
}
