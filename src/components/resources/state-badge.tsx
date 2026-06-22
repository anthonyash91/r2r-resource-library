"use client";

import Link from "next/link";
import { Landmark } from "lucide-react";
import {
  resourceBadgeClass,
  resourceBadgeSmClass,
} from "@/components/layout/site-branding-styles";
import { buildResourcesPageHref } from "@/lib/resources-page";
import { cn } from "@/lib/utils";
import { useTranslations } from "@/i18n/locale-context";

interface StateBadgeProps {
  state: string;
  size?: "default" | "sm";
}

export function StateBadge({ state, size = "default" }: StateBadgeProps) {
  const { t } = useTranslations();
  const isSmall = size === "sm";

  if (!state.trim()) return null;

  return (
    <Link
      href={buildResourcesPageHref({ state }, "results")}
      className={cn(
        isSmall ? resourceBadgeSmClass : resourceBadgeClass,
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
      )}
      aria-label={t("resources.stateBadgeAria", { state })}
    >
      <Landmark aria-hidden="true" />
      {state}
    </Link>
  );
}
