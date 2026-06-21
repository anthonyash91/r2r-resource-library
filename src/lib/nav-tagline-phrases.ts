const SENTENCE_SPLIT = /(?<=[.!?])\s+/;

export function parseNavTaglinePhrases(
  tagline: string,
  fallbacks: readonly string[]
): string[] {
  const parts = tagline
    .split(SENTENCE_SPLIT)
    .map((part) => part.trim())
    .filter(Boolean);

  if (parts.length >= 2) return parts;
  if (tagline.trim()) return [tagline.trim()];
  return [...fallbacks];
}
