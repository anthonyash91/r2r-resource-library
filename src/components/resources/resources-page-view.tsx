"use client";

import { useEffect, useRef, useState } from "react";
import type { Category, Resource } from "@/types";
import { ResourcesHeroSection } from "@/components/home/hero-section";
import { RecommendedResourcesSectionClient } from "@/components/resources/recommended-resources-section-client";
import { ResourcesResultsIsland } from "@/components/resources/resources-results-island";
import { ResourceResultsGridSkeleton } from "@/components/resources/resources-page-skeleton";
import { useResourceFilterDraft } from "@/components/resources/resource-filter-draft-context";
import {
  EMPTY_RESOURCE_FILTER_OPTIONS,
  type ResourceFilterOptions,
} from "@/components/resources/use-resource-filter-options";
import { LibraryDisclaimer } from "@/components/resources/library-disclaimer";
import { ScrollToResourceResults } from "@/components/resources/scroll-to-resource-results";
import { cn, pageSectionPadding, sectionDividerTop, sectionStackGap, pageSectionBandClassForIndex } from "@/lib/utils";
import { RESOURCE_RESULTS_ID } from "@/lib/resources-page";
import type { ResourcesPageSearchParams } from "@/lib/resources-page-filters";

interface BootstrapPayload {
  resources: Resource[];
  categories: Category[];
  states: string[];
  globalOptions: ResourceFilterOptions;
  appliedOptions: ResourceFilterOptions;
  recommended: Resource[];
  preferences: {
    county: string | null;
    state: string | null;
    priorityCategories: string[];
  };
  params: ResourcesPageSearchParams;
}

interface ResourcesPageViewProps {
  loadingLabel: string;
}

export function ResourcesPageInstantShell({ loadingLabel }: ResourcesPageViewProps) {
  return (
    <>
      <ResourcesHeroSection
        states={[]}
        globalOptions={EMPTY_RESOURCE_FILTER_OPTIONS}
        appliedOptions={EMPTY_RESOURCE_FILTER_OPTIONS}
      />

      <div className={cn(pageSectionBandClassForIndex(0), pageSectionPadding)}>
        <div className={cn("mx-auto max-w-7xl", sectionStackGap)}>
          <div
            id={RESOURCE_RESULTS_ID}
            className={cn("scroll-mt-[var(--site-header-offset)]", sectionStackGap)}
          >
            <div role="status" aria-live="polite" aria-busy="true" aria-label={loadingLabel}>
              <ResourceResultsGridSkeleton />
            </div>
          </div>
        </div>
      </div>
    </>
  );
}

export function ResourcesPageView({ loadingLabel }: ResourcesPageViewProps) {
  const { clientAppliedParams, isFilterUrlReady } = useResourceFilterDraft();
  const [bootstrap, setBootstrap] = useState<BootstrapPayload | null>(null);
  const fetchedRef = useRef(false);

  useEffect(() => {
    if (!isFilterUrlReady || fetchedRef.current) return;

    fetchedRef.current = true;

    let cancelled = false;
    const searchParams = new URLSearchParams();
    for (const [key, value] of Object.entries(clientAppliedParams)) {
      if (value?.trim()) searchParams.set(key, value.trim());
    }

    void fetch(`/api/resources/bootstrap?${searchParams.toString()}`)
      .then((response) => {
        if (!response.ok) throw new Error("Failed to load resources page");
        return response.json() as Promise<BootstrapPayload>;
      })
      .then((data) => {
        if (cancelled) return;
        setBootstrap(data);
      })
      .catch(() => {
        if (cancelled) return;
        setBootstrap(null);
      });

    return () => {
      cancelled = true;
    };
  }, [clientAppliedParams, isFilterUrlReady]);

  const resolvedParams = bootstrap?.params ?? clientAppliedParams;
  const defaultStateLabel = resolvedParams.state?.trim() || "Kentucky";

  return (
    <>
      <ResourcesHeroSection
        states={bootstrap?.states ?? []}
        globalOptions={bootstrap?.globalOptions ?? EMPTY_RESOURCE_FILTER_OPTIONS}
        appliedOptions={bootstrap?.appliedOptions ?? EMPTY_RESOURCE_FILTER_OPTIONS}
      />

      <div className={cn(pageSectionBandClassForIndex(0), pageSectionPadding)}>
        <div className={cn("mx-auto max-w-7xl", sectionStackGap)}>
          <ScrollToResourceResults />

          {bootstrap?.recommended.length ? (
            <RecommendedResourcesSectionClient
              resources={bootstrap.recommended}
              county={bootstrap.preferences.county}
            />
          ) : null}

          <div
            id={RESOURCE_RESULTS_ID}
            className={cn(
              "scroll-mt-[var(--site-header-offset)]",
              sectionStackGap,
              (bootstrap?.recommended.length ?? 0) > 0 && sectionDividerTop
            )}
          >
            {bootstrap ? (
              <ResourcesResultsIsland
                initialResources={bootstrap.resources}
                initialParams={resolvedParams}
                categories={bootstrap.categories}
                defaultStateLabel={defaultStateLabel}
              />
            ) : (
              <div role="status" aria-live="polite" aria-busy="true" aria-label={loadingLabel}>
                <ResourceResultsGridSkeleton />
              </div>
            )}
          </div>
        </div>

        {bootstrap ? (
          <LibraryDisclaimer variant="detail" className="mt-6 sm:mt-8" />
        ) : null}
      </div>
    </>
  );
}
