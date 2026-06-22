import { cn } from "@/lib/utils";
import type { Resource } from "@/types";
import { ResourceCard } from "./resource-card";

interface ResourceMasonryProps {
  resources: Resource[];
  columns?: 1 | 2 | 3;
  showSave?: boolean;
  variant?: "default" | "compact";
  layout?: "grid" | "masonry";
  /** Inset panels: keep masonry but preserve parent padding (no negative trailing margin). */
  contained?: boolean;
  className?: string;
}

const gridColumnClasses: Record<1 | 2 | 3, string> = {
  1: "grid-cols-1",
  2: "grid-cols-1 sm:grid-cols-2",
  3: "grid-cols-1 sm:grid-cols-2 lg:grid-cols-3",
};

const masonryColumnClasses: Record<1 | 2 | 3, string> = {
  1: "columns-1",
  2: "columns-1 sm:columns-2",
  3: "columns-1 sm:columns-2 lg:columns-3",
};

export function ResourceMasonry({
  resources,
  columns = 3,
  showSave,
  variant = "default",
  layout = "masonry",
  contained = false,
  className,
}: ResourceMasonryProps) {
  const isCompact = variant === "compact";
  const gapClass = isCompact ? "gap-4" : "gap-6";

  if (layout === "masonry") {
    return (
      <div
        className={cn(
          masonryColumnClasses[columns],
          gapClass,
          !contained && (isCompact ? "-mb-4" : "-mb-6"),
          className
        )}
      >
        {resources.map((resource) => (
          <div
            key={resource.id}
            className={cn(
              "w-full max-w-full break-inside-avoid",
              isCompact ? "mb-4 p-2" : "mb-6"
            )}
          >
            <ResourceCard resource={resource} showSave={showSave} variant={variant} />
          </div>
        ))}
      </div>
    );
  }

  return (
    <div
      className={cn("grid items-stretch", gridColumnClasses[columns], gapClass, className)}
    >
      {resources.map((resource) => (
        <div key={resource.id} className={cn("min-w-0", isCompact ? "p-2" : "flex h-full")}>
          <ResourceCard resource={resource} showSave={showSave} variant={variant} />
        </div>
      ))}
    </div>
  );
}
