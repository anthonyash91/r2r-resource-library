"use client";

import { useEffect } from "react";
import { usePathname, useSearchParams } from "next/navigation";
import { hasActiveResourceFilters } from "@/lib/resource-filter-params";
import {
  RECOMMENDED_RESOURCES_HASH,
  RECOMMENDED_RESOURCES_ID,
  RESOURCE_RESULTS_HASH,
  RESOURCE_RESULTS_ID,
} from "@/lib/resources-page";

function scrollToElement(elementId: string) {
  const tryScroll = (attempts = 0) => {
    const target = document.getElementById(elementId);
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

    if (window.location.hash === RECOMMENDED_RESOURCES_HASH) {
      scrollToElement(RECOMMENDED_RESOURCES_ID);
      return;
    }

    const shouldScroll =
      window.location.hash === RESOURCE_RESULTS_HASH ||
      hasActiveResourceFilters(searchParams);

    if (!shouldScroll) return;

    scrollToElement(RESOURCE_RESULTS_ID);
  }, [pathname, filterKey, searchParams]);

  return null;
}
