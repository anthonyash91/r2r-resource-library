"use client";

import Link from "next/link";
import { CategoryIcon } from "@/lib/category-icons";
import {
  resourceBadgeClass,
  resourceBadgeSmClass,
} from "@/components/layout/site-branding-styles";
import { buildResourcesPageHref } from "@/lib/resources-page";
import { cn } from "@/lib/utils";
import type { Category } from "@/types";
import { useCategoryLabel } from "@/i18n/use-category-label";

interface CategoryBadgeProps {
  category: Pick<Category, "name" | "icon" | "slug">;
  size?: "default" | "sm";
}

export function CategoryBadge({ category, size = "default" }: CategoryBadgeProps) {
  const categoryLabel = useCategoryLabel();
  const isSmall = size === "sm";

  return (
    <Link
      href={buildResourcesPageHref({ category: category.slug })}
      className={cn(
        isSmall ? resourceBadgeSmClass : resourceBadgeClass,
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
      )}
    >
      <CategoryIcon icon={category.icon} aria-hidden="true" />
      {categoryLabel(category)}
    </Link>
  );
}
