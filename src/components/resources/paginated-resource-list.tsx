"use client";

import { useEffect, useState } from "react";
import type { Resource } from "@/types";
import { ResourceMasonry } from "@/components/resources/resource-masonry";
import { Button } from "@/components/ui/button";
import { useTranslations } from "@/i18n/locale-context";

const PAGE_SIZE = 30;

interface PaginatedResourceListProps {
  resources: Resource[];
}

export function PaginatedResourceList({ resources }: PaginatedResourceListProps) {
  const { t } = useTranslations();
  const [visibleCount, setVisibleCount] = useState(PAGE_SIZE);
  const listSignature = resources.map((resource) => resource.id).join("\0");

  useEffect(() => {
    setVisibleCount(PAGE_SIZE);
  }, [listSignature]);

  const visible = resources.slice(0, visibleCount);
  const hasMore = visibleCount < resources.length;

  if (resources.length === 0) {
    return null;
  }

  return (
    <>
      <ResourceMasonry resources={visible} contained />

      {resources.length > PAGE_SIZE ? (
        <div className="mt-10 flex flex-col items-center gap-3">
          <p className="text-base text-muted-foreground" aria-live="polite">
            {t("resources.showingCount", { visible: visible.length, total: resources.length })}
          </p>
          {hasMore ? (
            <Button
              size="lg"
              variant="outline"
              onClick={() => setVisibleCount((count) => count + PAGE_SIZE)}
            >
              {t("resources.loadMore")}
            </Button>
          ) : null}
        </div>
      ) : null}
    </>
  );
}
