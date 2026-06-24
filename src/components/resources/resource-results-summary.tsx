import type { ReactNode } from "react";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

type Translator = (key: string, params?: Record<string, string | number>) => string;

export function formatMainResultsHint(t: Translator, filterLabels: string[]): string {
  if (filterLabels.length === 0) {
    return t("resources.resultsHintEmpty");
  }
  return t("resources.resultsHint", { filters: filterLabels.join(", ") });
}

export function appendFilterLabelsToHint(hint: string, filterLabels: string[]): string {
  if (filterLabels.length === 0) {
    const hintBase = hint.replace(/\.$/, "");
    return `${hintBase}.`;
  }
  const hintBase = hint.replace(/\.$/, "");
  return `${hintBase}: ${filterLabels.join(", ")}`;
}

interface ResourceResultsSectionProps {
  heading: string;
  hint: string;
  count: number;
  children: ReactNode;
}

export function ResourceResultsHeader({
  heading,
  hint,
  count,
  headingId = "search-results-heading",
}: {
  heading: string;
  hint: string;
  count: number;
  headingId?: string;
}) {
  return (
    <header className="mb-4 space-y-2">
      <div className="flex flex-wrap items-center gap-3">
        <h2 id={headingId} className="text-xl font-bold text-foreground">
          {heading}
        </h2>
        <Badge variant="primary" className="shrink-0 tabular-nums">
          {count}
        </Badge>
      </div>
      <p className="text-base text-muted-foreground">{hint}</p>
    </header>
  );
}

export function ResourceResultsSection({
  heading,
  hint,
  count,
  children,
}: ResourceResultsSectionProps) {
  return (
    <section aria-labelledby="search-results-heading">
      <ResourceResultsHeader heading={heading} hint={hint} count={count} />
      {children}
    </section>
  );
}
