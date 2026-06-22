import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/** Shared inset padding for panel headers and matched page blocks */
export const blockInsetPadding = "px-4 py-4 sm:px-5 sm:py-5";
export const blockInsetPaddingY = "py-4 sm:py-5";
export const blockInsetPaddingTop = "pt-4 sm:pt-5";
/** Tighter top / roomier bottom so the hero band looks balanced around the search bar */
/** Resources hero: extra bottom room for the search bar */
export const resourcesHeroPadding = "pt-[36px] pb-[44px] sm:pt-[40px] sm:pb-[48px]";
/** Standalone page heroes (About, Contact, FAQ): balanced vertical padding */
export const pageHeroPadding = "py-[40px] sm:py-[44px]";
/** Standard padding for page content sections below the hero */
export const pageSectionPadding = "px-4 py-12 sm:px-6 sm:py-14 lg:px-8 lg:py-16";
/** Vertical spacing between stacked page sections */
export const sectionStackGap = "space-y-6";
/** Standard h2 size for full-width page sections (home, dashboard, about, etc.) */
export const pageSectionHeadingClass = "text-3xl font-bold sm:text-4xl";

/** Descriptive line under a page section h2 */
export const pageSectionSubtitleClass = "text-lg text-muted-foreground";

/** Same size as section subtitles on dark hero bands */
export const pageSectionSubtitleOnHeroClass = "text-lg leading-relaxed text-primary-foreground/90";

/** Secondary heading within a page section (step titles, FAQ groups, detail blocks) */
export const pageSectionSubheadingClass = "text-xl font-bold sm:text-2xl text-foreground";
/** Teal checkmark color used across list/feature icons */
export const checkIconClass = "app-check-icon";

function stableHash(input: string): number {
  let hash = 2166136261;
  for (let i = 0; i < input.length; i++) {
    hash ^= input.charCodeAt(i);
    hash = Math.imul(hash, 16777619);
  }
  return hash >>> 0;
}

export function truncateDescriptionPreview(
  description: string,
  seed: string,
  { min = 95, max = 145 }: { min?: number; max?: number } = {}
): string {
  const text = description.trim();
  if (!text) return "";

  const limit = min + (stableHash(seed) % (max - min + 1));
  if (text.length <= limit) return text;

  const excerpt = text.slice(0, limit);
  const lastSpace = excerpt.lastIndexOf(" ");
  const breakAt = lastSpace > Math.floor(limit * 0.55) ? lastSpace : limit;

  return `${text.slice(0, breakAt).trimEnd()}…`;
}

export function formatPhone(phone: string | null | undefined): string {
  if (!phone) return "";
  const digits = phone.replace(/\D/g, "");
  if (digits.length === 10) {
    return `(${digits.slice(0, 3)}) ${digits.slice(3, 6)}-${digits.slice(6)}`;
  }
  return phone;
}

export function formatWebsiteDisplay(website: string | null | undefined): string {
  if (!website) return "";
  try {
    const url = new URL(website.includes("://") ? website : `https://${website}`);
    const host = url.hostname.replace(/^www\./i, "");
    const path = url.pathname === "/" ? "" : url.pathname;
    return `${host}${path}`.replace(/\/$/, "");
  } catch {
    return website
      .replace(/^https?:\/\//i, "")
      .replace(/^www\./i, "")
      .replace(/\/$/, "");
  }
}

export function formatDate(
  date: string | null | undefined,
  locale: "en" | "es" = "en"
): string {
  if (!date) return "";
  return new Date(date).toLocaleDateString(locale === "es" ? "es-US" : "en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/[^\w\s-]/g, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-")
    .trim();
}

export function getDirectionsUrl(address: string): string {
  return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(address)}`;
}

export function shareResource(name: string, url: string): void {
  if (typeof navigator !== "undefined" && navigator.share) {
    navigator.share({ title: name, url }).catch(() => {});
  } else if (typeof navigator !== "undefined") {
    navigator.clipboard?.writeText(url);
  }
}
