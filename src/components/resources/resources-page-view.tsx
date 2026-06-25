"use client";

import type { Category, Resource } from "@/types";
import { ResourcesHeroSection } from "@/components/home/hero-section";
import { RecommendedResourcesSectionClient } from "@/components/resources/recommended-resources-section-client";
import { ResourcesResultsIsland } from "@/components/resources/resources-results-island";
import { ResourceResultsGridSkeleton } from "@/components/resources/resources-page-skeleton";
import {
  EMPTY_RESOURCE_FILTER_OPTIONS,
} from "@/components/resources/use-resource-filter-options";
import { LibraryDisclaimer } from "@/components/resources/library-disclaimer";
import { ScrollToResourceResults } from "@/components/resources/scroll-to-resource-results";
import { cn, pageSectionPadding, sectionDividerTop, sectionStackGap, pageSectionBandClassForIndex } from "@/lib/utils";
import { RESOURCE_RESULTS_ID } from "@/lib/resources-page";
import type { ResourcesBootstrapPayload } from "@/lib/resources-bootstrap";

interface ResourcesPageViewProps {
  loadingLabel: string;
  initialBootstrap?: ResourcesBootstrapPayload;
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

export function ResourcesPageView({
  loadingLabel: _loadingLabel,
  initialBootstrap,
}: ResourcesPageViewProps) {
  if (!initialBootstrap) {
    return <ResourcesPageInstantShell loadingLabel={_loadingLabel} />;
  }

  const resolvedParams = initialBootstrap.params;
  const defaultStateLabel = resolvedParams.state?.trim() || "Kentucky";

  return (
    <>
      <ResourcesHeroSection
        states={initialBootstrap.states}
        globalOptions={initialBootstrap.globalOptions}
        appliedOptions={initialBootstrap.appliedOptions}
      />

      <div className={cn(pageSectionBandClassForIndex(0), pageSectionPadding)}>
        <div className={cn("mx-auto max-w-7xl", sectionStackGap)}>
          <ScrollToResourceResults />

          {initialBootstrap.recommended.length ? (
            <RecommendedResourcesSectionClient
              resources={initialBootstrap.recommended}
              county={initialBootstrap.preferences.county}
            />
          ) : null}

          <div
            id={RESOURCE_RESULTS_ID}
            className={cn(
              "scroll-mt-[var(--site-header-offset)]",
              sectionStackGap,
              initialBootstrap.recommended.length > 0 && sectionDividerTop
            )}
          >
            <ResourcesResultsIsland
              initialResources={initialBootstrap.resources}
              initialZipSearch={initialBootstrap.zipSearch}
              initialParams={resolvedParams}
              categories={initialBootstrap.categories}
              defaultStateLabel={defaultStateLabel}
            />
          </div>
        </div>

        <LibraryDisclaimer variant="detail" className="mt-6 sm:mt-8" />
      </div>
    </>
  );
}
