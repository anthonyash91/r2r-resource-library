"use client";

import Link from "next/link";
import { CategoryIcon } from "@/lib/category-icons";
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
      href={`/resources?category=${category.slug}`}
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
        <CategoryIcon
          icon={category.icon}
          className={cn("shrink-0", isSmall ? "h-3 w-3" : "h-3.5 w-3.5")}
          aria-hidden="true"
        />
        {categoryLabel(category)}
      </span>
    </Link>
  );
}
