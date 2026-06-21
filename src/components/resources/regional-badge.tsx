"use client";

import Link from "next/link";
import { MapPinned } from "lucide-react";
import { cn } from "@/lib/utils";
import { useTranslations } from "@/i18n/locale-context";
import { isRegionalResource } from "@/lib/resource-coverage";
import type { Resource } from "@/types";

interface RegionalBadgeProps {
  resource: Pick<Resource, "coverage">;
  size?: "default" | "sm";
}

export function RegionalBadge({ resource, size = "default" }: RegionalBadgeProps) {
  const { t } = useTranslations();

  if (!isRegionalResource(resource)) return null;

  const isSmall = size === "sm";

  return (
    <Link
      href="/resources?coverage=multi"
      className="inline-flex rounded-full focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
    >
      <span
        className={cn(
          "app-badge inline-flex items-center rounded-full font-medium transition-colors",
          isSmall
            ? "gap-1 px-2.5 py-1.5 text-xs"
            : "gap-1.5 px-3 py-1 text-sm"
        )}
      >
        <MapPinned
          className={cn("shrink-0", isSmall ? "h-3 w-3" : "h-3.5 w-3.5")}
          aria-hidden="true"
        />
        {t("resources.coverageRegional")}
      </span>
    </Link>
  );
}
