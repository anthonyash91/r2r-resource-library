"use client";

import Link from "next/link";
import { Map } from "lucide-react";
import {
  resourceBadgeClass,
  resourceBadgeSmClass,
} from "@/components/layout/site-branding-styles";
import { buildResourcesPageHref } from "@/lib/resources-page";
import { cn } from "@/lib/utils";
import { useTranslations } from "@/i18n/locale-context";
import { isStatewideResource } from "@/lib/resource-coverage";
import type { Resource } from "@/types";

interface StatewideBadgeProps {
  resource: Pick<Resource, "coverage" | "tags">;
  size?: "default" | "sm";
}

export function StatewideBadge({ resource, size = "default" }: StatewideBadgeProps) {
  const { t } = useTranslations();

  if (!isStatewideResource(resource)) return null;

  const isSmall = size === "sm";

  return (
    <Link
      href={buildResourcesPageHref({ coverage: "statewide" }, "results")}
      className={cn(
        isSmall ? resourceBadgeSmClass : resourceBadgeClass,
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
      )}
    >
      <Map aria-hidden="true" />
      {t("resources.coverageStatewide")}
    </Link>
  );
}
