"use client";

import { useEffect, useMemo, useState } from "react";
import { cn } from "@/lib/utils";
import type { Resource } from "@/types";
import { ScrollReveal } from "@/components/ui/scroll-reveal";
import { ResourceCard } from "./resource-card";

const STAGGER_MS = 60;
const STAGGER_CAP = 8;

interface ResourceMasonryProps {
  resources: Resource[];
  columns?: 1 | 2 | 3;
  showSave?: boolean;
  variant?: "default" | "compact";
  /**
   * - masonry: CSS columns (balanced heights; items may reflow when the list grows)
   * - columns: fixed round-robin columns (stable positions when loading more)
   * - grid: uniform rows
   */
  layout?: "grid" | "masonry" | "columns";
  /** Inset panels: keep masonry but preserve parent padding (no negative trailing margin). */
  contained?: boolean;
  className?: string;
  animate?: boolean;
  /** Stagger delays restart from this index (load-more batches). */
  staggerFromIndex?: number;
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

function useResponsiveColumnCount(maxColumns: 1 | 2 | 3): number {
  const [count, setCount] = useState(maxColumns);

  useEffect(() => {
    if (maxColumns === 1) {
      setCount(1);
      return;
    }

    const smQuery = window.matchMedia("(min-width: 640px)");
    const lgQuery = window.matchMedia("(min-width: 1024px)");

    const update = () => {
      if (maxColumns === 2) {
        setCount(smQuery.matches ? 2 : 1);
        return;
      }

      setCount(lgQuery.matches ? 3 : smQuery.matches ? 2 : 1);
    };

    update();
    smQuery.addEventListener("change", update);
    if (maxColumns === 3) {
      lgQuery.addEventListener("change", update);
    }

    return () => {
      smQuery.removeEventListener("change", update);
      if (maxColumns === 3) {
        lgQuery.removeEventListener("change", update);
      }
    };
  }, [maxColumns]);

  return count;
}

function splitIntoStableColumns<T>(items: T[], columnCount: number): T[][] {
  const columns = Array.from({ length: columnCount }, () => [] as T[]);
  items.forEach((item, index) => {
    columns[index % columnCount].push(item);
  });
  return columns;
}

function cardRevealDelay(index: number, staggerFromIndex: number): number {
  const staggerIndex = index >= staggerFromIndex ? index - staggerFromIndex : index;
  return Math.min(staggerIndex, STAGGER_CAP - 1) * STAGGER_MS;
}

function AnimatedResourceCard({
  resource,
  index,
  showSave,
  variant,
  animate,
  staggerFromIndex,
  wrapperClassName,
}: {
  resource: Resource;
  index: number;
  showSave?: boolean;
  variant: "default" | "compact";
  animate: boolean;
  staggerFromIndex: number;
  wrapperClassName: string;
}) {
  const card = (
    <ResourceCard resource={resource} showSave={showSave} variant={variant} />
  );

  if (!animate) {
    return <div className={wrapperClassName}>{card}</div>;
  }

  return (
    <ScrollReveal
      variant="fade-up"
      delay={cardRevealDelay(index, staggerFromIndex)}
      revealOnMountIfVisible
      revealOnScrollDownOnly
      threshold={0.05}
      rootMargin="0px 0px -32px 0px"
      className={wrapperClassName}
    >
      {card}
    </ScrollReveal>
  );
}

export function ResourceMasonry({
  resources,
  columns = 3,
  showSave,
  variant = "default",
  layout = "masonry",
  contained = false,
  className,
  animate = true,
  staggerFromIndex = 0,
}: ResourceMasonryProps) {
  const isCompact = variant === "compact";
  const gapClass = isCompact ? "gap-4" : "gap-6";
  const columnCount = useResponsiveColumnCount(columns);

  const stableColumns = useMemo(() => {
    const indexed = resources.map((resource, index) => ({ resource, index }));
    return splitIntoStableColumns(indexed, columnCount);
  }, [resources, columnCount]);

  if (layout === "columns") {
    return (
      <div className={cn("flex items-start", gapClass, className)}>
        {stableColumns.map((column, columnIndex) => (
          <div
            key={columnIndex}
            className={cn("flex min-w-0 flex-1 flex-col", gapClass)}
          >
            {column.map(({ resource, index }) => (
              <AnimatedResourceCard
                key={resource.id}
                resource={resource}
                index={index}
                showSave={showSave}
                variant={variant}
                animate={animate}
                staggerFromIndex={staggerFromIndex}
                wrapperClassName={cn("w-full min-w-0", isCompact ? "p-2" : undefined)}
              />
            ))}
          </div>
        ))}
      </div>
    );
  }

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
        {resources.map((resource, index) => (
          <AnimatedResourceCard
            key={resource.id}
            resource={resource}
            index={index}
            showSave={showSave}
            variant={variant}
            animate={animate}
            staggerFromIndex={staggerFromIndex}
            wrapperClassName={cn(
              "w-full max-w-full break-inside-avoid",
              isCompact ? "mb-4 p-2" : "mb-6"
            )}
          />
        ))}
      </div>
    );
  }

  return (
    <div
      className={cn("grid items-stretch", gridColumnClasses[columns], gapClass, className)}
    >
      {resources.map((resource, index) => (
        <AnimatedResourceCard
          key={resource.id}
          resource={resource}
          index={index}
          showSave={showSave}
          variant={variant}
          animate={animate}
          staggerFromIndex={staggerFromIndex}
          wrapperClassName={cn("min-w-0", isCompact ? "p-2" : "flex h-full flex-col")}
        />
      ))}
    </div>
  );
}
