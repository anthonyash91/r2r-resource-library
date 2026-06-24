import type { Resource } from "@/types";
import { PaginatedResourceList } from "@/components/resources/paginated-resource-list";
import { ResourceResultsHeader, appendFilterLabelsToHint } from "@/components/resources/resource-results-summary";
import { cn, sectionDividerTop, sectionStackGap } from "@/lib/utils";

interface CountyFilteredResourceResultsProps {
  local: Resource[];
  statewide: Resource[];
  inCountyHeading: string;
  inCountyHint: string;
  statewideHeading: string;
  statewideHint: string;
  noLocalHint?: string;
  filterLabels?: string[];
}

export function CountyFilteredResourceResults({
  local,
  statewide,
  inCountyHeading,
  inCountyHint,
  statewideHeading,
  statewideHint,
  noLocalHint,
  filterLabels = [],
}: CountyFilteredResourceResultsProps) {
  const showNoLocalHint = local.length === 0 && Boolean(noLocalHint);

  return (
    <div className={sectionStackGap}>
      {showNoLocalHint ? (
        <p className="rounded-xl border border-border bg-card px-4 py-3 text-base text-muted-foreground sm:px-5">
          {noLocalHint}
        </p>
      ) : null}

      {local.length > 0 ? (
        <section aria-labelledby="county-local-heading">
          <ResourceResultsHeader
            heading={inCountyHeading}
            hint={appendFilterLabelsToHint(inCountyHint, filterLabels)}
            count={local.length}
            headingId="county-local-heading"
          />
          <PaginatedResourceList resources={local} />
        </section>
      ) : null}

      {statewide.length > 0 ? (
        <section
          className={cn(local.length > 0 && sectionDividerTop)}
          aria-labelledby="county-statewide-heading"
        >
          <ResourceResultsHeader
            heading={statewideHeading}
            hint={appendFilterLabelsToHint(
              statewideHint,
              local.length === 0 ? filterLabels : []
            )}
            count={statewide.length}
            headingId="county-statewide-heading"
          />
          <PaginatedResourceList resources={statewide} />
        </section>
      ) : null}
    </div>
  );
}
