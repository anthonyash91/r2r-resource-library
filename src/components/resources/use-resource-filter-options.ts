"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import type { Category } from "@/types";
import type { IntakeSignal } from "@/lib/intake-signals";
import { INTAKE_SIGNALS } from "@/lib/intake-signals";
import type { ResourceFilterDraft } from "./resource-filter-draft-context";

export interface ResourceFilterOptions {
  cities: string[];
  counties: string[];
  countyCounts: Record<string, number>;
  services: string[];
  categories: Category[];
  categoryCounts: Record<string, number>;
  serviceCounts: Record<string, number>;
  intakeCounts: Record<IntakeSignal, number>;
}

interface FilterOptionsResponse {
  cities: string[];
  counties?: string[];
  countyCounts?: Record<string, number>;
  services: string[];
  categories: Pick<Category, "id" | "slug" | "name">[];
  categoryCounts?: Record<string, number>;
  serviceCounts?: Record<string, number>;
  intakeCounts?: Partial<Record<IntakeSignal, number>>;
}

const EMPTY_INTAKE_COUNTS = Object.fromEntries(
  INTAKE_SIGNALS.map((signal) => [signal, 0])
) as Record<IntakeSignal, number>;

export const EMPTY_RESOURCE_FILTER_OPTIONS: ResourceFilterOptions = {
  cities: [],
  counties: [],
  countyCounts: {},
  services: [],
  categories: [],
  categoryCounts: {},
  serviceCounts: {},
  intakeCounts: EMPTY_INTAKE_COUNTS,
};

const EMPTY_OPTIONS = EMPTY_RESOURCE_FILTER_OPTIONS;

export type ResourceFilterFacetDraft = Pick<
  ResourceFilterDraft,
  "state" | "county" | "city" | "category" | "service" | "intake"
>;

async function fetchFilterOptions(draft: ResourceFilterFacetDraft): Promise<ResourceFilterOptions> {
  const params = new URLSearchParams();
  if (draft.state) params.set("state", draft.state);
  if (draft.county) params.set("county", draft.county);
  if (draft.city) params.set("city", draft.city);
  if (draft.category) params.set("category", draft.category);
  if (draft.service) params.set("service", draft.service);
  if (draft.intake.length > 0) {
    params.set("intake", draft.intake.join("|"));
  }

  const response = await fetch(`/api/resources/filter-options?${params.toString()}`);
  if (!response.ok) {
    throw new Error("Failed to load filter options");
  }

  const data = (await response.json()) as FilterOptionsResponse;
  return {
    cities: data.cities,
    counties: data.counties ?? [],
    countyCounts: data.countyCounts ?? {},
    services: data.services,
    categories: data.categories as Category[],
    categoryCounts: data.categoryCounts ?? {},
    serviceCounts: data.serviceCounts ?? {},
    intakeCounts: {
      ...EMPTY_INTAKE_COUNTS,
      ...(data.intakeCounts ?? {}),
    },
  };
}

export function useResourceFilterOptions(
  draft: ResourceFilterFacetDraft,
  globalOptions: ResourceFilterOptions,
  appliedOptions: ResourceFilterOptions
) {
  const intakeKey = draft.intake.join("|");
  const requestKey = useMemo(
    () =>
      JSON.stringify({
        state: draft.state,
        county: draft.county,
        city: draft.city,
        category: draft.category,
        service: draft.service,
        intake: intakeKey,
      }),
    [draft.state, draft.county, draft.city, draft.category, draft.service, intakeKey]
  );
  const needsDynamicOptions = Boolean(
    draft.state ||
      draft.county ||
      draft.city ||
      draft.category ||
      draft.service ||
      intakeKey
  );
  const draftRef = useRef(draft);
  draftRef.current = draft;
  const globalOptionsRef = useRef(globalOptions);
  globalOptionsRef.current = globalOptions;

  const [options, setOptions] = useState<ResourceFilterOptions>(() =>
    needsDynamicOptions ? appliedOptions : globalOptions
  );
  const [isLoading, setIsLoading] = useState(false);
  const activeRequestRef = useRef(0);

  useEffect(() => {
    if (!needsDynamicOptions) {
      setOptions(globalOptionsRef.current);
      setIsLoading(false);
      return;
    }

    const requestId = ++activeRequestRef.current;
    setIsLoading(true);

    fetchFilterOptions(draftRef.current)
      .then((next) => {
        if (requestId !== activeRequestRef.current) return;
        setOptions(next);
      })
      .catch(() => {
        if (requestId !== activeRequestRef.current) return;
        setOptions(EMPTY_OPTIONS);
      })
      .finally(() => {
        if (requestId !== activeRequestRef.current) return;
        setIsLoading(false);
      });
  }, [needsDynamicOptions, requestKey]);

  return { options, isLoading, requestKey };
}

export function formatFilterOptionLabel(label: string, count?: number): string {
  if (count == null || count <= 0) return label;
  return `${label} (${count})`;
}
