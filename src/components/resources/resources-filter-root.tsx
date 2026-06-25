"use client";

import type { ReactNode } from "react";
import type { ResourcesPageSearchParams } from "@/lib/resources-page-filters";
import { ResourceFilterDraftProvider } from "./resource-filter-draft-context";

export function ResourcesFilterRoot({
  children,
  initialAppliedParams,
}: {
  children: ReactNode;
  initialAppliedParams?: ResourcesPageSearchParams;
}) {
  return (
    <ResourceFilterDraftProvider initialAppliedParams={initialAppliedParams}>
      {children}
    </ResourceFilterDraftProvider>
  );
}
