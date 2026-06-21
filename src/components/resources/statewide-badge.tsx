"use client";

import Link from "next/link";
import { Map } from "lucide-react";
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
      href="/resources?coverage=statewide"
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
        <Map
          className={cn("shrink-0", isSmall ? "h-3 w-3" : "h-3.5 w-3.5")}
          aria-hidden="true"
        />
        {t("resources.coverageStatewide")}
      </span>
    </Link>
  );
}
