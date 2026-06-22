import type { Resource } from "@/types";
import { PaginatedResourceList } from "@/components/resources/paginated-resource-list";
import { Badge } from "@/components/ui/badge";
import { cn, sectionDividerTop, sectionStackGap } from "@/lib/utils";

interface CountyFilteredResourceResultsProps {
  local: Resource[];
  statewide: Resource[];
  inCountyHeading: string;
  inCountyHint: string;
  statewideHeading: string;
  statewideHint: string;
  noLocalHint?: string;
}

export function CountyFilteredResourceResults({
  local,
  statewide,
  inCountyHeading,
  inCountyHint,
  statewideHeading,
  statewideHint,
  noLocalHint,
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
          <header className="mb-4 space-y-2">
            <div className="flex flex-wrap items-center gap-3">
              <h2 id="county-local-heading" className="text-xl font-bold text-foreground">
                {inCountyHeading}
              </h2>
              <Badge variant="primary" className="shrink-0 tabular-nums">
                {local.length}
              </Badge>
            </div>
            <p className="text-base text-muted-foreground">{inCountyHint}</p>
          </header>
          <PaginatedResourceList resources={local} />
        </section>
      ) : null}

      {statewide.length > 0 ? (
        <section
          className={cn(local.length > 0 && sectionDividerTop)}
          aria-labelledby="county-statewide-heading"
        >
          <header className="mb-4 space-y-2">
            <div className="flex flex-wrap items-center gap-3">
              <h2 id="county-statewide-heading" className="text-xl font-bold text-foreground">
                {statewideHeading}
              </h2>
              <Badge variant="primary" className="shrink-0 tabular-nums">
                {statewide.length}
              </Badge>
            </div>
            <p className="text-base text-muted-foreground">{statewideHint}</p>
          </header>
          <PaginatedResourceList resources={statewide} />
        </section>
      ) : null}
    </div>
  );
}
