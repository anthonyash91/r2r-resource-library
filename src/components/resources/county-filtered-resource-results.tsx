import type { Resource } from "@/types";
import { ResourceMasonry } from "@/components/resources/resource-masonry";
import { ResourceResultsSummary } from "@/components/resources/resource-results-summary";
import { cn, sectionStackGap } from "@/lib/utils";

interface CountyFilteredResourceResultsProps {
  county: string;
  local: Resource[];
  statewide: Resource[];
  summaryLabel: string;
  inCountyHeading: string;
  inCountyHint: string;
  statewideHeading: string;
  statewideHint: string;
  noLocalHint?: string;
}

export function CountyFilteredResourceResults({
  county,
  local,
  statewide,
  summaryLabel,
  inCountyHeading,
  inCountyHint,
  statewideHeading,
  statewideHint,
  noLocalHint,
}: CountyFilteredResourceResultsProps) {
  const total = local.length + statewide.length;
  const showNoLocalHint = local.length === 0 && Boolean(noLocalHint);

  return (
    <div className={sectionStackGap}>
      {!showNoLocalHint ? (
        <ResourceResultsSummary count={total} label={summaryLabel} />
      ) : null}

      {showNoLocalHint ? (
        <p className="rounded-xl border border-border bg-card px-4 py-3 text-base text-muted-foreground sm:px-5">
          {noLocalHint}
        </p>
      ) : null}

      {local.length > 0 ? (
        <section aria-labelledby="county-local-heading">
          <header className="mb-4 space-y-2">
            <h2 id="county-local-heading" className="text-xl font-bold text-foreground">
              {inCountyHeading}
            </h2>
            <p className="text-base text-muted-foreground">{inCountyHint}</p>
          </header>
          <ResourceMasonry resources={local} />
        </section>
      ) : null}

      {statewide.length > 0 ? (
        <section
          className={cn(local.length > 0 && "border-t border-border pt-6")}
          aria-labelledby="county-statewide-heading"
        >
          <header className="mb-4 space-y-2">
            <h2 id="county-statewide-heading" className="text-xl font-bold text-foreground">
              {statewideHeading}
            </h2>
            <p className="text-base text-muted-foreground">{statewideHint}</p>
          </header>
          <ResourceMasonry resources={statewide} />
        </section>
      ) : null}
    </div>
  );
}
