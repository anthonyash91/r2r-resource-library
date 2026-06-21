const SESSION_KEY = "reentry_session_id";
const VIEW_DEDUPE_PREFIX = "reentry_view_logged:";

export function getOrCreateSessionId(): string {
  if (typeof window === "undefined") return "";

  let sessionId = localStorage.getItem(SESSION_KEY);
  if (!sessionId) {
    sessionId = crypto.randomUUID();
    localStorage.setItem(SESSION_KEY, sessionId);
  }
  return sessionId;
}

export function hasLoggedViewThisSession(resourceId: string): boolean {
  if (typeof window === "undefined") return false;
  return sessionStorage.getItem(`${VIEW_DEDUPE_PREFIX}${resourceId}`) === "1";
}

export function markViewLoggedThisSession(resourceId: string): void {
  if (typeof window === "undefined") return;
  sessionStorage.setItem(`${VIEW_DEDUPE_PREFIX}${resourceId}`, "1");
}

export function clearViewLoggedThisSession(resourceId: string): void {
  if (typeof window === "undefined") return;
  sessionStorage.removeItem(`${VIEW_DEDUPE_PREFIX}${resourceId}`);
}
