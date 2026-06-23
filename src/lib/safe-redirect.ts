/** Allow only same-origin relative paths (blocks open redirects via //host). */
export function safeInternalPath(
  path: string | null | undefined,
  fallback = "/"
): string {
  if (!path) return fallback;

  const trimmed = path.trim();
  if (
    !trimmed.startsWith("/") ||
    trimmed.startsWith("//") ||
    trimmed.includes("\\") ||
    trimmed.includes("@")
  ) {
    return fallback;
  }

  return trimmed;
}
