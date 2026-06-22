import { RECOMMENDED_RESOURCES_HASH } from "@/lib/resources-page";

export const RECOMMENDED_PANEL_STORAGE_KEY = "reentry_resources_recommended_open";

export const RECOMMENDED_PANEL_OPEN_EVENT = "reentry-recommended-open-change";

export function getRecommendedPanelOpen(hash = ""): boolean {
  if (typeof window === "undefined") return true;
  if (hash === RECOMMENDED_RESOURCES_HASH) return true;

  try {
    const stored = window.localStorage.getItem(RECOMMENDED_PANEL_STORAGE_KEY);
    if (stored === "0") return false;
  } catch {
    // ignore
  }

  return true;
}

export function setRecommendedPanelOpen(open: boolean): void {
  try {
    window.localStorage.setItem(RECOMMENDED_PANEL_STORAGE_KEY, open ? "1" : "0");
  } catch {
    // ignore
  }

  window.dispatchEvent(new Event(RECOMMENDED_PANEL_OPEN_EVENT));
}

export function subscribeRecommendedPanelOpen(callback: () => void): () => void {
  const onStorage = (event: StorageEvent) => {
    if (event.key === RECOMMENDED_PANEL_STORAGE_KEY) callback();
  };

  window.addEventListener("storage", onStorage);
  window.addEventListener(RECOMMENDED_PANEL_OPEN_EVENT, callback);

  return () => {
    window.removeEventListener("storage", onStorage);
    window.removeEventListener(RECOMMENDED_PANEL_OPEN_EVENT, callback);
  };
}
