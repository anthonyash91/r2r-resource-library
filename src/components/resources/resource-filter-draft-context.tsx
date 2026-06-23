"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { parseIntakeFilterParam, serializeIntakeFilterParam, type IntakeSignal } from "@/lib/intake-signals";
import { buildResourcesPageHref } from "@/lib/resources-page";

export interface ResourceFilterDraft {
  q: string;
  category: string;
  state: string;
  county: string;
  city: string;
  service: string;
  filter: string;
  intake: IntakeSignal[];
}

function draftFromSearchParams(searchParams: URLSearchParams): ResourceFilterDraft {
  return {
    q: searchParams.get("q") ?? "",
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

interface ResourceFilterDraftContextValue {
  draft: ResourceFilterDraft;
  applied: ResourceFilterDraft;
  setField: (key: keyof Omit<ResourceFilterDraft, "intake" | "q">, value: string) => void;
  setQuery: (q: string) => void;
  toggleIntake: (signal: IntakeSignal) => void;
  apply: (options?: { q?: string }) => void;
  clear: () => void;
  hasDraftFilters: boolean;
  hasAppliedFilters: boolean;
  hasPendingChanges: boolean;
}

const ResourceFilterDraftContext = createContext<ResourceFilterDraftContextValue | null>(null);

export function ResourceFilterDraftProvider({ children }: { children: ReactNode }) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const applied = useMemo(() => draftFromSearchParams(searchParams), [searchParams]);
  const [draft, setDraft] = useState(applied);

  useEffect(() => {
    setDraft(applied);
  }, [applied]);

  const setField = useCallback(
    (key: keyof Omit<ResourceFilterDraft, "intake" | "q">, value: string) => {
      setDraft((current) => {
        const next = { ...current, [key]: value };
        if (key === "state") {
          next.county = "";
          next.city = "";
        }
        if (key === "county") {
          next.city = "";
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

  const apply = useCallback(
    (options?: { q?: string }) => {
      const next = options?.q !== undefined ? { ...draft, q: options.q } : draft;
      router.push(buildResourcesPageHref(draftToParams(next), "results"), { scroll: false });
    },
    [draft, router]
  );

  const clear = useCallback(() => {
    router.push("/resources", { scroll: false });
  }, [router]);

  const hasDraftFilters = useMemo(() => {
    return Boolean(
      draft.category ||
        draft.state ||
        draft.county ||
        draft.city ||
        draft.service ||
        draft.filter ||
        draft.intake.length > 0
    );
  }, [draft]);

  const hasAppliedFilters = useMemo(() => {
    return Boolean(
      applied.category ||
        applied.state ||
        applied.county ||
        applied.city ||
        applied.service ||
        applied.filter ||
        applied.intake.length > 0 ||
        applied.q.trim()
    );
  }, [applied]);

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
      apply,
      clear,
      hasDraftFilters,
      hasAppliedFilters,
      hasPendingChanges,
    }),
    [apply, applied, clear, draft, hasAppliedFilters, hasDraftFilters, hasPendingChanges, setField, setQuery, toggleIntake]
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
