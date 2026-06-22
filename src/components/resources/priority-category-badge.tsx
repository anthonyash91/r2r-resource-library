"use client";

import Link from "next/link";
import { CategoryIcon } from "@/lib/category-icons";
import { resourceBadgeClass } from "@/components/layout/site-branding-styles";
import { buildResourcesPageHref } from "@/lib/resources-page";
import { cn } from "@/lib/utils";
import { useTranslations } from "@/i18n/locale-context";
import type { OnboardingPrioritySlug } from "@/lib/user-preferences/constants";

const PRIORITY_CATEGORY_ICONS: Record<OnboardingPrioritySlug, string> = {
  housing: "home",
  employment: "briefcase",
  "id-documentation": "id-card",
  "financial-assistance": "dollar-sign",
  "substance-use-treatment": "shield",
  "legal-aid": "scale",
  healthcare: "heart-pulse",
  "food-nutrition": "utensils",
  education: "graduation-cap",
  "reentry-organizations": "handshake",
};

interface PriorityCategoryBadgeProps {
  slug: string;
}

export function PriorityCategoryBadge({ slug }: PriorityCategoryBadgeProps) {
  const { t } = useTranslations();
  const icon = PRIORITY_CATEGORY_ICONS[slug as OnboardingPrioritySlug] ?? "search";

  return (
    <Link
      href={buildResourcesPageHref({ category: slug })}
      className={cn(
        resourceBadgeClass,
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
      )}
    >
      <CategoryIcon icon={icon} />
      {t(`onboarding.priorities.${slug}`)}
    </Link>
  );
}
