import type { ReactNode } from "react";
import { Badge } from "@/components/ui/badge";

interface ResourceResultsSectionProps {
  heading: string;
  hint: string;
  count: number;
  children: ReactNode;
}

export function ResourceResultsSection({
  heading,
  hint,
  count,
  children,
}: ResourceResultsSectionProps) {
  return (
    <section aria-labelledby="search-results-heading">
      <header className="mb-4 space-y-2">
        <div className="flex flex-wrap items-center gap-3">
          <h2 id="search-results-heading" className="text-xl font-bold text-foreground">
            {heading}
          </h2>
          <Badge variant="primary" className="shrink-0 tabular-nums">
            {count}
          </Badge>
        </div>
        <p className="text-base text-muted-foreground">{hint}</p>
      </header>
      {children}
    </section>
  );
}
