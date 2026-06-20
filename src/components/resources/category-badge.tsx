import Link from "next/link";
import { Badge } from "@/components/ui/badge";
import { CategoryIcon } from "@/lib/category-icons";
import { cn } from "@/lib/utils";
import type { Category } from "@/types";

interface CategoryBadgeProps {
  category: Pick<Category, "name" | "icon" | "slug">;
  size?: "default" | "sm";
}

export function CategoryBadge({ category, size = "default" }: CategoryBadgeProps) {
  const isSmall = size === "sm";

  return (
    <Link
      href={`/resources?category=${category.slug}`}
      className="inline-flex items-center rounded-full focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
    >
      <Badge
        variant="primary"
        className={cn(
          "transition-colors hover:bg-primary/20",
          isSmall
            ? "gap-1 px-2.5 py-1.5 text-xs"
            : "gap-1.5 px-3 py-1 text-sm font-medium leading-normal border border-transparent"
        )}
      >
        <CategoryIcon
          icon={category.icon}
          className={cn("shrink-0", isSmall ? "h-3 w-3" : "h-3.5 w-3.5")}
          aria-hidden="true"
        />
        <span className={isSmall ? "leading-none" : undefined}>{category.name}</span>
      </Badge>
    </Link>
  );
}
