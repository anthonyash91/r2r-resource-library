import { normalizeSearchQuery } from "@/lib/resource-search";

export interface ParsedZipSearchQuery {
  zip: string;
  textQuery?: string;
}

/** Extract a 5-digit ZIP and optional keyword from a search box value. */
export function parseZipFromSearchQuery(query: string): ParsedZipSearchQuery | null {
  const normalized = normalizeSearchQuery(query);
  if (!normalized) return null;

  const leading = normalized.match(/^(\d{5})(?:-\d{4})?(?:\s+(.+))?$/);
  if (leading) {
    return {
      zip: leading[1],
      textQuery: leading[2]?.trim() || undefined,
    };
  }

  const trailing = normalized.match(/^(.+?)\s+(\d{5})(?:-\d{4})?$/);
  if (trailing) {
    const textQuery = trailing[1].trim();
    return {
      zip: trailing[2],
      textQuery: textQuery || undefined,
    };
  }

  return null;
}

export function resourcesSearchParamsFromQuery(
  query: string
): { zip?: string; q?: string } {
  const { q, zip } = searchDraftFieldsFromQuery(query);
  const result: { zip?: string; q?: string } = {};
  if (zip) result.zip = zip;
  if (q) result.q = q;
  return result;
}

/** Normalize a search box value into draft fields, clearing ZIP when absent. */
export function searchDraftFieldsFromQuery(query: string): { q: string; zip: string } {
  const trimmed = query.trim();
  if (!trimmed) return { q: "", zip: "" };

  const parsed = parseZipFromSearchQuery(trimmed);
  if (parsed) {
    return {
      zip: parsed.zip,
      q: parsed.textQuery ?? "",
    };
  }

  return { q: trimmed, zip: "" };
}

export function formatZipSearchDisplayValue(zip?: string, q?: string): string {
  if (!zip?.trim()) return q?.trim() ?? "";
  if (!q?.trim()) return zip.trim();
  return `${zip.trim()} ${q.trim()}`;
}
