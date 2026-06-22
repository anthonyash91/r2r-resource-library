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

function readHeaderHeight(): number {
  const header = document.querySelector("header");
  return header?.getBoundingClientRect().height ?? 80;
}

function scrollToElement(elementId: string) {
  let disposed = false;
  let resizeObserver: ResizeObserver | null = null;
  let fallbackTimer: ReturnType<typeof setTimeout> | null = null;

  const cleanup = () => {
    disposed = true;
    resizeObserver?.disconnect();
    if (fallbackTimer) clearTimeout(fallbackTimer);
  };

  const scrollOnce = () => {
    const target = document.getElementById(elementId);
    if (!target || disposed) return false;

    const headerHeight = readHeaderHeight();
    const top =
      target.getBoundingClientRect().top + window.scrollY - headerHeight - 12;

    window.scrollTo({ top: Math.max(0, top), behavior: "auto" });
    return true;
  };

  const watchRecommendedLayout = () => {
    if (!scrollOnce()) return;

    const recommended = document.getElementById(RECOMMENDED_RESOURCES_ID);
    if (!recommended) {
      cleanup();
      return;
    }

    let lastHeight = recommended.getBoundingClientRect().height;
    let stableFrames = 0;

    resizeObserver = new ResizeObserver(() => {
      if (disposed) return;

      const height = recommended.getBoundingClientRect().height;
      if (height !== lastHeight) {
        lastHeight = height;
        stableFrames = 0;
        scrollOnce();
        return;
      }

      stableFrames += 1;
      if (stableFrames >= 2) {
        cleanup();
      }
    });

    resizeObserver.observe(recommended);
    fallbackTimer = setTimeout(cleanup, 500);
  };

  const tryScroll = (attempts = 0) => {
    const target = document.getElementById(elementId);
    if (!target) {
      if (attempts < 24) {
        window.requestAnimationFrame(() => tryScroll(attempts + 1));
      }
      return;
    }

    requestAnimationFrame(() => {
      requestAnimationFrame(watchRecommendedLayout);
    });
  };

  tryScroll();

  return cleanup;
}

export function ScrollToResourceResults() {
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const filterKey = searchParams.toString();

  useEffect(() => {
    if (pathname !== "/resources") return;

    let cleanupScroll: (() => void) | undefined;

    if (window.location.hash === RECOMMENDED_RESOURCES_HASH) {
      cleanupScroll = scrollToElement(RECOMMENDED_RESOURCES_ID);
      return () => cleanupScroll?.();
    }

    const shouldScroll =
      window.location.hash === RESOURCE_RESULTS_HASH ||
      hasActiveResourceFilters(searchParams);

    if (!shouldScroll) return;

    cleanupScroll = scrollToElement(RESOURCE_RESULTS_ID);

    return () => cleanupScroll?.();
  }, [pathname, filterKey, searchParams]);

  return null;
}
