"use client";

import type { Resource } from "@/types";
import { PaginatedResourceList } from "@/components/resources/paginated-resource-list";
import { ResourceResultsHeader, appendFilterLabelsToHint } from "@/components/resources/resource-results-summary";
import { cn, sectionDividerTop, sectionStackGap } from "@/lib/utils";

interface ZipFilteredResourceResultsProps {
  inZip: Resource[];
  nearZip: Resource[];
  statewide: Resource[];
  inZipHeading: string;
  inZipHint: string;
  nearZipHeading: string;
  nearZipHint: string;
  statewideHeading: string;
  statewideHint: string;
  noInZipHint?: string;
  filterLabels?: string[];
}

export function ZipFilteredResourceResults({
  inZip,
  nearZip,
  statewide,
  inZipHeading,
  inZipHint,
  nearZipHeading,
  nearZipHint,
  statewideHeading,
  statewideHint,
  noInZipHint,
  filterLabels = [],
}: ZipFilteredResourceResultsProps) {
  const showNoInZipHint = inZip.length === 0 && Boolean(noInZipHint);

  return (
    <div className={sectionStackGap}>
      {showNoInZipHint ? (
        <p className="rounded-xl border border-border bg-card px-4 py-3 text-base text-muted-foreground sm:px-5">
          {noInZipHint}
        </p>
      ) : null}

      {inZip.length > 0 ? (
        <section aria-labelledby="zip-local-heading">
          <ResourceResultsHeader
            heading={inZipHeading}
            hint={appendFilterLabelsToHint(inZipHint, filterLabels)}
            count={inZip.length}
            headingId="zip-local-heading"
          />
          <PaginatedResourceList resources={inZip} />
        </section>
      ) : null}

      {nearZip.length > 0 ? (
        <section
          className={cn(inZip.length > 0 && sectionDividerTop)}
          aria-labelledby="zip-nearby-heading"
        >
          <ResourceResultsHeader
            heading={nearZipHeading}
            hint={appendFilterLabelsToHint(
              nearZipHint,
              inZip.length === 0 ? filterLabels : []
            )}
            count={nearZip.length}
            headingId="zip-nearby-heading"
          />
          <PaginatedResourceList resources={nearZip} />
        </section>
      ) : null}

      {statewide.length > 0 ? (
        <section
          className={cn((inZip.length > 0 || nearZip.length > 0) && sectionDividerTop)}
          aria-labelledby="zip-statewide-heading"
        >
          <ResourceResultsHeader
            heading={statewideHeading}
            hint={appendFilterLabelsToHint(
              statewideHint,
              inZip.length === 0 && nearZip.length === 0 ? filterLabels : []
            )}
            count={statewide.length}
            headingId="zip-statewide-heading"
          />
          <PaginatedResourceList resources={statewide} />
        </section>
      ) : null}
    </div>
  );
}
