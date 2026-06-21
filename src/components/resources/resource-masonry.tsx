import { cn } from "@/lib/utils";
import type { Resource } from "@/types";
import { ResourceCard } from "./resource-card";

interface ResourceMasonryProps {
  resources: Resource[];
  columns?: 1 | 2 | 3;
  showSave?: boolean;
  variant?: "default" | "compact";
  className?: string;
}

const columnClasses: Record<1 | 2 | 3, string> = {
  1: "columns-1",
  2: "columns-1 sm:columns-2",
  3: "columns-1 sm:columns-2 lg:columns-3",
};

export function ResourceMasonry({
  resources,
  columns = 3,
  showSave,
  variant = "default",
  className,
}: ResourceMasonryProps) {
  const isCompact = variant === "compact";

  return (
    <div className={cn(columnClasses[columns], isCompact ? "gap-4" : "gap-6", className)}>
      {resources.map((resource) => (
        <div key={resource.id} className={cn("break-inside-avoid", isCompact ? "mb-4 p-2" : "mb-6")}>
          <ResourceCard resource={resource} showSave={showSave} variant={variant} />
        </div>
      ))}
    </div>
  );
}
