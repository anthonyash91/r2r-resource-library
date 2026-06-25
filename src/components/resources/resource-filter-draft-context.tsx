"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useLayoutEffect,
  useMemo,
  useRef,
  useState,
  type ReactNode,
} from "react";
import { useSearchParams } from "next/navigation";
import { parseIntakeFilterParam, serializeIntakeFilterParam, type IntakeSignal } from "@/lib/intake-signals";
import { hasActiveResourceFilters } from "@/lib/resource-filter-params";
import { searchDraftFieldsFromQuery } from "@/lib/resources-search-params";
import {
  buildResourcesPageClearedHref,
  buildResourcesPageHref,
  isResourcesBrowseAllView,
  resourcesPageQueryWithPreferenceDefaults,
} from "@/lib/resources-page";
import type { ResourcesPageSearchParams } from "@/lib/resources-page-filters";
import {
  EMPTY_PREFERENCES,
  hasCompletedOnboarding,
  readClientPreferences,
} from "@/lib/user-preferences";

export interface ResourceFilterDraft {
  q: string;
  zip: string;
  category: string;
  state: string;
  county: string;
  city: string;
  service: string;
  filter: string;
  intake: IntakeSignal[];
}

const EMPTY_DRAFT: ResourceFilterDraft = {
  q: "",
  zip: "",
  category: "",
  state: "",
  county: "",
  city: "",
  service: "",
  filter: "",
  intake: [],
};

function draftFromPageParams(params: ResourcesPageSearchParams): ResourceFilterDraft {
  const searchParams = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (typeof value === "string" && value.trim()) {
      searchParams.set(key, value.trim());
    }
  }
  return draftFromSearchParams(searchParams);
}

function draftFromSearchParams(searchParams: URLSearchParams): ResourceFilterDraft {
  return {
    q: searchParams.get("q") ?? "",
    zip: searchParams.get("zip") ?? "",
    category: searchParams.get("category") ?? "",
    state: searchParams.get("state") ?? "",
    county: searchParams.get("county") ?? "",
    city: searchParams.get("city") ?? "",
    service: searchParams.get("service") ?? "",
    filter: searchParams.get("filter") ?? "",
    intake: parseIntakeFilterParam(searchParams.get("intake")),
  };
}

function draftToParams(draft: ResourceFilterDraft): URLSearchParams {
  const params = new URLSearchParams();
  if (draft.zip.trim()) params.set("zip", draft.zip.trim());
  if (draft.q.trim()) params.set("q", draft.q.trim());
  if (draft.category) params.set("category", draft.category);
  if (draft.state) params.set("state", draft.state);
  if (draft.county) params.set("county", draft.county);
  if (draft.city) params.set("city", draft.city);
  if (draft.service) params.set("service", draft.service);
  if (draft.filter) params.set("filter", draft.filter);
  if (draft.intake.length > 0) {
    params.set("intake", serializeIntakeFilterParam(draft.intake));
  }
  return params;
}

function draftToPageParams(draft: ResourceFilterDraft): ResourcesPageSearchParams {
  const params: ResourcesPageSearchParams = {};
  if (draft.zip.trim()) params.zip = draft.zip.trim();
  if (draft.q.trim()) params.q = draft.q.trim();
  if (draft.category) params.category = draft.category;
  if (draft.state) params.state = draft.state;
  if (draft.county) params.county = draft.county;
  if (draft.city) params.city = draft.city;
  if (draft.service) params.service = draft.service;
  if (draft.filter) params.filter = draft.filter;
  if (draft.intake.length > 0) {
    params.intake = serializeIntakeFilterParam(draft.intake);
  }
  return params;
}

function draftParamsKey(draft: ResourceFilterDraft): string {
  return JSON.stringify(draftToPageParams(draft));
}

interface ResourceFilterDraftContextValue {
  draft: ResourceFilterDraft;
  applied: ResourceFilterDraft;
  setField: (key: keyof Omit<ResourceFilterDraft, "intake" | "q">, value: string) => void;
  setQuery: (q: string) => void;
  toggleIntake: (signal: IntakeSignal) => void;
  setIntake: (intake: IntakeSignal[]) => void;
  apply: (options?: { q?: string }) => void;
  clear: () => void;
  hasDraftFilters: boolean;
  hasAppliedFilters: boolean;
  hasPendingChanges: boolean;
  /** Bumped when filters are updated without a router navigation. */
  filterUrlRevision: number;
  /** True after clear until the next router-driven search param change. */
  urlCleared: boolean;
  /** True after preference defaults / URL hydration on mount. */
  isFilterUrlReady: boolean;
  /** Effective filter params for client-side fetches (avoids stale router searchParams). */
  clientAppliedParams: ResourcesPageSearchParams;
}

const ResourceFilterDraftContext = createContext<ResourceFilterDraftContextValue | null>(null);

export function ResourceFilterDraftProvider({
  children,
  initialAppliedParams,
}: {
  children: ReactNode;
  initialAppliedParams?: ResourcesPageSearchParams;
}) {
  const searchParams = useSearchParams();
  const serverApplied = useMemo(
    () => (initialAppliedParams ? draftFromPageParams(initialAppliedParams) : null),
    [initialAppliedParams]
  );
  const routerApplied = useMemo(() => draftFromSearchParams(searchParams), [searchParams]);
  const [draft, setDraft] = useState(() => serverApplied ?? routerApplied);
  const [filterUrlRevision, setFilterUrlRevision] = useState(0);
  const [urlCleared, setUrlCleared] = useState(false);
  const [urlAppliedDraft, setUrlAppliedDraft] = useState<ResourceFilterDraft | null>(
    () => serverApplied
  );
  const [isFilterUrlReady, setIsFilterUrlReady] = useState(Boolean(serverApplied));
  const preferenceDefaultsAppliedRef = useRef(false);
  const skipNextRouterSyncRef = useRef(false);

  const applied = useMemo(() => {
    if (urlCleared) return EMPTY_DRAFT;
    if (urlAppliedDraft) return urlAppliedDraft;
    return routerApplied;
  }, [routerApplied, urlAppliedDraft, urlCleared]);

  const clientAppliedParams = useMemo<ResourcesPageSearchParams>(() => {
    if (urlCleared) return {};
    return draftToPageParams(applied);
  }, [applied, urlCleared]);

  useLayoutEffect(() => {
    if (preferenceDefaultsAppliedRef.current) return;
    preferenceDefaultsAppliedRef.current = true;

    if (serverApplied) {
      setIsFilterUrlReady(true);
      return;
    }

    const params = Object.fromEntries(searchParams.entries()) as Partial<
      Record<string, string | undefined>
    >;

    if (!isResourcesBrowseAllView(params) && !params.state?.trim()) {
      const prefs = readClientPreferences() ?? EMPTY_PREFERENCES;
      if (hasCompletedOnboarding(prefs) && prefs.state) {
        const defaultQuery = resourcesPageQueryWithPreferenceDefaults(params, prefs);
        if (defaultQuery) {
          const nextApplied = draftFromSearchParams(new URLSearchParams(defaultQuery));
          skipNextRouterSyncRef.current = true;
          setUrlCleared(false);
          setUrlAppliedDraft(nextApplied);
          setDraft(nextApplied);
          setFilterUrlRevision((revision) => revision + 1);
          window.history.replaceState(window.history.state, "", `/resources?${defaultQuery}`);
        }
      }
    }

    setIsFilterUrlReady(true);
  }, [searchParams, serverApplied]);

  const routerAppliedKey = useMemo(() => draftParamsKey(routerApplied), [routerApplied]);
  const isInitialRouterSyncRef = useRef(true);

  useEffect(() => {
    if (isInitialRouterSyncRef.current) {
      isInitialRouterSyncRef.current = false;
      return;
    }
    if (skipNextRouterSyncRef.current) {
      skipNextRouterSyncRef.current = false;
      return;
    }
    setUrlAppliedDraft(null);
    setUrlCleared(false);
    setDraft(routerApplied);
  }, [routerAppliedKey, routerApplied]);

  useEffect(() => {
    const handlePopState = () => {
      const nextApplied = draftFromSearchParams(new URLSearchParams(window.location.search));
      setUrlAppliedDraft(null);
      setUrlCleared(false);
      setDraft(nextApplied);
      setFilterUrlRevision((revision) => revision + 1);
    };

    window.addEventListener("popstate", handlePopState);
    return () => window.removeEventListener("popstate", handlePopState);
  }, []);

  const setField = useCallback(
    (key: keyof Omit<ResourceFilterDraft, "intake" | "q">, value: string) => {
      setDraft((current) => {
        const next = { ...current, [key]: value };
        if (key === "state") {
          next.county = "";
          next.city = "";
          next.service = "";
          next.category = "";
        }
        if (key === "county") {
          next.city = "";
          next.service = "";
        }
        return next;
      });
    },
    []
  );

  const setQuery = useCallback((q: string) => {
    setDraft((current) => ({ ...current, q }));
  }, []);

  const toggleIntake = useCallback((signal: IntakeSignal) => {
    setDraft((current) => {
      const intake = current.intake.includes(signal)
        ? current.intake.filter((item) => item !== signal)
        : [...current.intake, signal];
      return { ...current, intake };
    });
  }, []);

  const setIntake = useCallback((intake: IntakeSignal[]) => {
    setDraft((current) => ({ ...current, intake }));
  }, []);

  const apply = useCallback(
    (options?: { q?: string }) => {
      setUrlCleared(false);
      const next =
        options?.q !== undefined
          ? {
              ...draft,
              ...searchDraftFieldsFromQuery(options.q),
            }
          : draft;
      skipNextRouterSyncRef.current = true;
      setDraft(next);
      setUrlAppliedDraft(next);
      setFilterUrlRevision((revision) => revision + 1);
      const href = buildResourcesPageHref(draftToParams(next), "results");
      window.history.pushState(window.history.state, "", href);
    },
    [draft]
  );

  const clear = useCallback(() => {
    setDraft(EMPTY_DRAFT);
    setUrlAppliedDraft(null);
    if (!hasActiveResourceFilters(searchParams)) return;

    setUrlCleared(true);
    setFilterUrlRevision((revision) => revision + 1);
    const href = buildResourcesPageClearedHref();
    window.history.replaceState(window.history.state, "", href);
  }, [searchParams]);

  const hasDraftFilters = useMemo(() => {
    return Boolean(
      draft.category ||
        draft.zip ||
        draft.state ||
        draft.county ||
        draft.city ||
        draft.service ||
        draft.filter ||
        draft.intake.length > 0
    );
  }, [draft]);

  const hasAppliedFilters = useMemo(() => {
    if (urlCleared) return false;
    return Boolean(
      applied.category ||
        applied.state ||
        applied.county ||
        applied.city ||
        applied.service ||
        applied.filter ||
        applied.intake.length > 0 ||
        applied.zip.trim() ||
        applied.q.trim()
    );
  }, [applied, urlCleared]);

  const hasPendingChanges = useMemo(() => {
    return JSON.stringify(draft) !== JSON.stringify(applied);
  }, [applied, draft]);

  const value = useMemo(
    () => ({
      draft,
      applied,
      setField,
      setQuery,
      toggleIntake,
      setIntake,
      apply,
      clear,
      hasDraftFilters,
      hasAppliedFilters,
      hasPendingChanges,
      filterUrlRevision,
      urlCleared,
      isFilterUrlReady,
      clientAppliedParams,
    }),
    [
      apply,
      applied,
      clear,
      clientAppliedParams,
      draft,
      filterUrlRevision,
      hasAppliedFilters,
      hasDraftFilters,
      hasPendingChanges,
      setField,
      setIntake,
      setQuery,
      toggleIntake,
      urlCleared,
      isFilterUrlReady,
    ]
  );

  return (
    <ResourceFilterDraftContext.Provider value={value}>{children}</ResourceFilterDraftContext.Provider>
  );
}

export function useResourceFilterDraft(): ResourceFilterDraftContextValue {
  const context = useContext(ResourceFilterDraftContext);
  if (!context) {
    throw new Error("useResourceFilterDraft must be used within ResourceFilterDraftProvider");
  }
  return context;
}

export function useResourceFilterDraftOptional(): ResourceFilterDraftContextValue | null {
  return useContext(ResourceFilterDraftContext);
}
