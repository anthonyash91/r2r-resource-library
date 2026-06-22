"use client";

import Link from "next/link";
import { MapPinned } from "lucide-react";
import {
  resourceBadgeClass,
  resourceBadgeSmClass,
} from "@/components/layout/site-branding-styles";
import { buildResourcesPageHref } from "@/lib/resources-page";
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
      href={buildResourcesPageHref({ coverage: "multi" }, "results")}
      className={cn(
        isSmall ? resourceBadgeSmClass : resourceBadgeClass,
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
      )}
    >
      <MapPinned aria-hidden="true" />
      {t("resources.coverageRegional")}
    </Link>
  );
}
