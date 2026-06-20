import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
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
