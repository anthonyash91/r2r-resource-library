"use client";

import { useState } from "react";
import type { Resource } from "@/types";
import { ResourceMasonry } from "@/components/resources/resource-masonry";
import { Button } from "@/components/ui/button";
import { useTranslations } from "@/i18n/locale-context";

const PAGE_SIZE = 20;

interface PaginatedResourceListProps {
  resources: Resource[];
}

export function PaginatedResourceList({ resources }: PaginatedResourceListProps) {
  const { t } = useTranslations();
  const [visibleCount, setVisibleCount] = useState(PAGE_SIZE);

  const visible = resources.slice(0, visibleCount);
  const hasMore = visibleCount < resources.length;

  return (
    <>
      <ResourceMasonry resources={visible} />

      <div className="mt-10 flex flex-col items-center gap-3">
        <p className="text-base text-muted-foreground" aria-live="polite">
          {t("resources.showingCount", { visible: visible.length, total: resources.length })}
        </p>
        {hasMore && (
          <Button
            size="lg"
            variant="outline"
            onClick={() => setVisibleCount((count) => count + PAGE_SIZE)}
          >
            {t("resources.loadMore")}
          </Button>
        )}
      </div>
    </>
  );
}
