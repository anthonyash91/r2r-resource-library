"use client";

import type { ReactNode } from "react";
import { ResourceFilterDraftProvider } from "./resource-filter-draft-context";

export function ResourcesFilterRoot({ children }: { children: ReactNode }) {
  return <ResourceFilterDraftProvider>{children}</ResourceFilterDraftProvider>;
}
