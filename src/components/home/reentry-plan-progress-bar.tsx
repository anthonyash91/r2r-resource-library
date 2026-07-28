"use client";

import { useEffect, useRef } from "react";
import { cn } from "@/lib/utils";

interface ReentryPlanProgressBarProps {
  className?: string;
}

export function ReentryPlanProgressBar({ className }: ReentryPlanProgressBarProps) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      el.classList.add("reentry-plan-progress-fill--visible");
      return;
    }

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          el.classList.add("reentry-plan-progress-fill--visible");
          observer.disconnect();
        }
      },
      { threshold: 0.12, rootMargin: "0px 0px -7% 0px" }
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, []);

  return (
    <div
      ref={ref}
      className={cn("reentry-plan-progress-fill h-full rounded-[5px] bg-primary", className)}
    />
  );
}
