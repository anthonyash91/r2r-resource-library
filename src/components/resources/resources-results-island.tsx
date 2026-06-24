"use client";

import { useEffect, useMemo, useState } from "react";
import type { Category, Resource } from "@/types";
import { PaginatedResourceList } from "@/components/resources/paginated-resource-list";
import { ResourceResultsSection, formatMainResultsHint } from "@/components/resources/resource-results-summary";
import { ResourceResultsGridSkeleton } from "@/components/resources/resources-page-skeleton";
import { CountyFilteredResourceResults } from "@/components/resources/county-filtered-resource-results";
import { useResourceFilterDraft } from "@/components/resources/resource-filter-draft-context";
import { useTranslations } from "@/i18n/locale-context";
import { partitionResourcesByCountyFilter } from "@/lib/resource-coverage";
import { buildResourceSearchFilterLabels } from "@/lib/resource-search-filter-labels";
import {
  resourcesPageParamsKey,
  type ResourcesPageSearchParams,
} from "@/lib/resources-page-filters";

interface ResourcesResultsIslandProps {
  initialResources: Resource[];
  initialParams: ResourcesPageSearchParams;
  categories: Category[];
  defaultStateLabel: string;
}

async function fetchResourcesForParams(
  params: ResourcesPageSearchParams
): Promise<Resource[]> {
  const searchParams = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value?.trim()) searchParams.set(key, value.trim());
  }

  const response = await fetch(`/api/resources?${searchParams.toString()}`);
  if (!response.ok) {
    throw new Error("Failed to load resources");
  }

  const data = (await response.json()) as { resources: Resource[] };
  return data.resources;
}

export function ResourcesResultsIsland({
  initialResources,
  initialParams,
  categories,
  defaultStateLabel,
}: ResourcesResultsIslandProps) {
  const { filterUrlRevision, clientAppliedParams } = useResourceFilterDraft();
  const { t } = useTranslations();
  const [resources, setResources] = useState(initialResources);
  const [isFetching, setIsFetching] = useState(false);

  const effectiveParamsKey = useMemo(
    () => resourcesPageParamsKey(clientAppliedParams),
    [clientAppliedParams]
  );
  const initialParamsKey = useMemo(
    () => resourcesPageParamsKey(initialParams),
    [initialParams]
  );

  useEffect(() => {
    if (effectiveParamsKey === initialParamsKey) {
      setResources(initialResources);
      return;
    }

    let cancelled = false;
    setIsFetching(true);

    fetchResourcesForParams(clientAppliedParams)
      .then((next) => {
        if (!cancelled) setResources(next);
      })
      .catch(() => {
        if (!cancelled) setResources([]);
      })
      .finally(() => {
        if (!cancelled) setIsFetching(false);
      });

    return () => {
      cancelled = true;
    };
  }, [
    clientAppliedParams,
    effectiveParamsKey,
    filterUrlRevision,
    initialParamsKey,
    initialResources,
  ]);

  const selectedCounty = clientAppliedParams.county?.trim();
  const showCountySplit =
    Boolean(selectedCounty) && clientAppliedParams.coverage !== "statewide";

  const resultsHeading = t("resources.resultsSummary");
  const filterLabels = buildResourceSearchFilterLabels(clientAppliedParams, categories, t);
  const resultsHint = formatMainResultsHint(t, filterLabels);
  const countySplitFilterLabels = buildResourceSearchFilterLabels(
    clientAppliedParams,
    categories,
    t,
    {
      excludeCounty: true,
    }
  );
  const { local: localResults, statewide: statewideResults } = showCountySplit
    ? partitionResourcesByCountyFilter(resources, selectedCounty)
    : { local: resources, statewide: [] as Resource[] };

  if (isFetching && resources.length === 0) {
    return (
      <ResourceResultsSection
        heading={resultsHeading}
        hint={resultsHint}
        count={0}
      >
        <ResourceResultsGridSkeleton />
      </ResourceResultsSection>
    );
  }

  if (resources.length === 0) {
    return (
      <ResourceResultsSection
        heading={resultsHeading}
        hint={resultsHint}
        count={0}
      >
        <div className="rounded-xl border border-border bg-card p-12 text-center">
          <h3 className="mb-2 text-xl font-bold">{t("resources.noResults")}</h3>
          <p className="text-base text-muted-foreground">{t("resources.noResultsHint")}</p>
        </div>
      </ResourceResultsSection>
    );
  }

  if (showCountySplit) {
    return (
      <CountyFilteredResourceResults
        local={localResults}
        statewide={statewideResults}
        filterLabels={countySplitFilterLabels}
        inCountyHeading={t("resources.resultsInCountyHeading", {
          county: selectedCounty!,
        })}
        inCountyHint={t("resources.resultsInCountyHint", {
          county: selectedCounty!,
        })}
        statewideHeading={t("resources.resultsStatewideHeading")}
        statewideHint={t("resources.resultsStatewideHint", {
          county: selectedCounty!,
          state: clientAppliedParams.state?.trim() || defaultStateLabel,
        })}
        noLocalHint={
          localResults.length === 0
            ? t("resources.resultsNoLocalInCounty", { county: selectedCounty! })
            : undefined
        }
      />
    );
  }

  return (
    <ResourceResultsSection
      heading={resultsHeading}
      hint={resultsHint}
      count={resources.length}
    >
      <PaginatedResourceList resources={resources} />
    </ResourceResultsSection>
  );
}
