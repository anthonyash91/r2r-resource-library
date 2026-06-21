"use client";

import { useCallback } from "react";
import type { Category } from "@/types";
import { getCategoryLabel } from "./category-label";
import { useTranslations } from "./locale-context";

export function useCategoryLabel() {
  const { t } = useTranslations();

  return useCallback(
    (category: Pick<Category, "name" | "slug">) => getCategoryLabel(category, t),
    [t]
  );
}
