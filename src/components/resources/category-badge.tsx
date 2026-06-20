import { Badge } from "@/components/ui/badge";
import { CategoryIcon } from "@/lib/category-icons";
import type { Category } from "@/types";

interface CategoryBadgeProps {
  category: Pick<Category, "name" | "icon">;
}

export function CategoryBadge({ category }: CategoryBadgeProps) {
  return (
    <Badge variant="primary" className="gap-1.5">
      <CategoryIcon icon={category.icon} className="h-3.5 w-3.5" aria-hidden="true" />
      {category.name}
    </Badge>
  );
}
