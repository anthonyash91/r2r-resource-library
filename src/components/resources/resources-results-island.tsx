"use client";

import { useEffect, useMemo, useState } from "react";
import type { Category, Resource } from "@/types";
import { PaginatedResourceList } from "@/components/resources/paginated-resource-list";
import { ResourceResultsSection, formatMainResultsHint } from "@/components/resources/resource-results-summary";
import { ResourceResultsGridSkeleton } from "@/components/resources/resources-page-skeleton";
import { CountyFilteredResourceResults } from "@/components/resources/county-filtered-resource-results";
import { ZipFilteredResourceResults } from "@/components/resources/zip-filtered-resource-results";
import { useResourceFilterDraft } from "@/components/resources/resource-filter-draft-context";
import { useTranslations } from "@/i18n/locale-context";
import type { ZipLocation } from "@/lib/resource-zip-search";
import { partitionResourcesByCountyFilter } from "@/lib/resource-coverage";
import { partitionResourcesByZip } from "@/lib/resource-zip-search";
import { buildResourceSearchFilterLabels } from "@/lib/resource-search-filter-labels";
import {
  resourcesPageParamsKey,
  type ResourcesPageSearchParams,
} from "@/lib/resources-page-filters";

interface ResourcesResultsIslandProps {
  initialResources: Resource[];
  initialZipSearch: ZipLocation | null;
  initialParams: ResourcesPageSearchParams;
  categories: Category[];
  defaultStateLabel: string;
}

interface ResourcesFetchResult {
  resources: Resource[];
  zipSearch: ZipLocation | null;
}

async function fetchResourcesForParams(
  params: ResourcesPageSearchParams
): Promise<ResourcesFetchResult> {
  const searchParams = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value?.trim()) searchParams.set(key, value.trim());
  }

  const response = await fetch(`/api/resources?${searchParams.toString()}`);
  if (!response.ok) {
    throw new Error("Failed to load resources");
  }

  return (await response.json()) as ResourcesFetchResult;
}

export function ResourcesResultsIsland({
  initialResources,
  initialZipSearch,
  initialParams,
  categories,
  defaultStateLabel,
}: ResourcesResultsIslandProps) {
  const { filterUrlRevision, clientAppliedParams } = useResourceFilterDraft();
  const { t } = useTranslations();
  const [resources, setResources] = useState(initialResources);
  const [zipSearch, setZipSearch] = useState<ZipLocation | null>(initialZipSearch);
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
      setZipSearch(initialZipSearch);
      return;
    }

    let cancelled = false;
    setIsFetching(true);

    fetchResourcesForParams(clientAppliedParams)
      .then((next) => {
        if (!cancelled) {
          setResources(next.resources);
          setZipSearch(next.zipSearch);
        }
      })
      .catch(() => {
        if (!cancelled) {
          setResources([]);
          setZipSearch(null);
        }
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
    initialZipSearch,
  ]);

  const selectedCounty = clientAppliedParams.county?.trim();
  const showCountySplit =
    Boolean(selectedCounty) &&
    clientAppliedParams.coverage !== "statewide" &&
    !zipSearch;

  const showZipSplit = Boolean(zipSearch);

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
  const zipSplitFilterLabels = buildResourceSearchFilterLabels(
    clientAppliedParams,
    categories,
    t,
    {
      excludeZip: true,
    }
  );
  const { local: localResults, statewide: statewideResults } = showCountySplit
    ? partitionResourcesByCountyFilter(resources, selectedCounty)
    : { local: resources, statewide: [] as Resource[] };

  const zipPartition = showZipSplit && zipSearch
    ? partitionResourcesByZip(resources, zipSearch)
    : { inZip: [], nearZip: [], statewide: [] };

  if (isFetching) {
    return (
      <div role="status" aria-live="polite" aria-busy="true">
        <ResourceResultsSection
          heading={resultsHeading}
          hint={resultsHint}
          count={resources.length}
        >
          <ResourceResultsGridSkeleton />
        </ResourceResultsSection>
      </div>
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

  if (showZipSplit && zipSearch) {
    const zipLabel = zipSearch.city
      ? t("resources.resultsZipLocationLabel", {
          zip: zipSearch.zip,
          city: zipSearch.city,
          state: zipSearch.state,
        })
      : zipSearch.zip;

    return (
      <ResourceResultsSection
        heading={resultsHeading}
        hint={resultsHint}
        count={resources.length}
      >
        <ZipFilteredResourceResults
          inZip={zipPartition.inZip}
          nearZip={zipPartition.nearZip}
          statewide={zipPartition.statewide}
          filterLabels={zipSplitFilterLabels}
          inZipHeading={t("resources.resultsInZipHeading", { zip: zipSearch.zip })}
          inZipHint={t("resources.resultsInZipHint", { location: zipLabel })}
          nearZipHeading={t("resources.resultsNearZipHeading", { zip: zipSearch.zip })}
          nearZipHint={t("resources.resultsNearZipHint", { location: zipLabel })}
          statewideHeading={t("resources.resultsStatewideHeading")}
          statewideHint={t("resources.resultsStatewideZipHint", {
            state: zipSearch.state,
            zip: zipSearch.zip,
          })}
          noInZipHint={
            zipPartition.inZip.length === 0
              ? t("resources.resultsNoLocalInZip", { zip: zipSearch.zip })
              : undefined
          }
        />
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
