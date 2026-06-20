import { ListFilter } from "lucide-react";
import { Badge } from "@/components/ui/badge";

interface ResourceResultsSummaryProps {
  count: number;
  label: string;
}

export function ResourceResultsSummary({ count, label }: ResourceResultsSummaryProps) {
  return (
    <div
      className="flex flex-wrap items-center gap-3 rounded-xl border border-border bg-card px-4 py-3 sm:px-5"
      role="status"
      aria-live="polite"
    >
      <ListFilter className="h-5 w-5 shrink-0 text-primary" aria-hidden="true" />
      <p className="min-w-0 flex-1 text-sm leading-snug text-muted-foreground sm:text-base">{label}</p>
      <Badge variant="primary" className="shrink-0 tabular-nums">
        {count}
      </Badge>
    </div>
  );
}
