"use client";

import { useEffect } from "react";
import { usePathname, useSearchParams } from "next/navigation";
import {
  parseResourcesPageScrollTarget,
  RECOMMENDED_RESOURCES_ID,
  RESOURCE_RESULTS_ID,
  RESOURCES_PAGE_SCROLL_PARAM,
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

  const clearScrollIntent = () => {
    const params = new URLSearchParams(window.location.search);
    const hadScrollParam = params.has(RESOURCES_PAGE_SCROLL_PARAM);
    const hadHash = Boolean(window.location.hash);

    if (!hadScrollParam && !hadHash) return;

    params.delete(RESOURCES_PAGE_SCROLL_PARAM);
    const qs = params.toString();
    window.history.replaceState(
      null,
      "",
      `${window.location.pathname}${qs ? `?${qs}` : ""}`
    );
  };

  const watchRecommendedLayout = () => {
    if (!scrollOnce()) return;

    const recommended = document.getElementById(RECOMMENDED_RESOURCES_ID);
    if (!recommended) {
      clearScrollIntent();
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
        clearScrollIntent();
        cleanup();
      }
    });

    resizeObserver.observe(recommended);
    fallbackTimer = setTimeout(() => {
      clearScrollIntent();
      cleanup();
    }, 500);
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

    const scrollTarget = parseResourcesPageScrollTarget(
      searchParams,
      window.location.hash
    );

    let cleanupScroll: (() => void) | undefined;

    if (scrollTarget === "recommended") {
      cleanupScroll = scrollToElement(RECOMMENDED_RESOURCES_ID);
      return () => cleanupScroll?.();
    }

    if (scrollTarget === "results") {
      cleanupScroll = scrollToElement(RESOURCE_RESULTS_ID);
      return () => cleanupScroll?.();
    }
  }, [pathname, filterKey]);

  return null;
}
