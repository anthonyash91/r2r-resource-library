"use client";

import { useEffect } from "react";
import { usePathname, useSearchParams } from "next/navigation";
import { hasActiveResourceFilters } from "@/lib/resource-filter-params";
import {
  RESOURCE_RESULTS_HASH,
  RESOURCE_RESULTS_ID,
} from "@/lib/resources-page";

function scrollToResourceResults() {
  const tryScroll = (attempts = 0) => {
    const target = document.getElementById(RESOURCE_RESULTS_ID);
    if (target) {
      target.scrollIntoView({ block: "start" });
      return;
    }

    if (attempts < 12) {
      window.requestAnimationFrame(() => tryScroll(attempts + 1));
    }
  };

  tryScroll();
}

export function ScrollToResourceResults() {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const filterKey = searchParams.toString();

  useEffect(() => {
    if (pathname !== "/resources") return;

    const shouldScroll =
      window.location.hash === RESOURCE_RESULTS_HASH ||
      hasActiveResourceFilters(searchParams);

    if (!shouldScroll) return;

    scrollToResourceResults();
  }, [pathname, filterKey, searchParams]);

  return null;
}
