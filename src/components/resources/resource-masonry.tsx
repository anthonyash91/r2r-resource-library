import { cn } from "@/lib/utils";
import type { Resource } from "@/types";
import { ResourceCard } from "./resource-card";

interface ResourceMasonryProps {
  resources: Resource[];
  columns?: 1 | 2 | 3;
  showSave?: boolean;
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
  className,
}: ResourceMasonryProps) {
  return (
    <div className={cn(columnClasses[columns], "gap-6", className)}>
      {resources.map((resource) => (
        <div key={resource.id} className="mb-6 break-inside-avoid">
          <ResourceCard resource={resource} showSave={showSave} />
        </div>
      ))}
    </div>
  );
}
