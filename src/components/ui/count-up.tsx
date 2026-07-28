"use client";

import { useEffect, useRef, useState } from "react";
import { cn } from "@/lib/utils";

interface CountUpProps {
  value: string;
  className?: string;
  durationMs?: number;
}

function parseCountValue(raw: string) {
  const trimmed = raw.trim();
  const match = trimmed.match(/^([\d,]+(?:\.\d+)?)(.*)$/);
  if (!match) return null;
  return {
    target: Number.parseFloat(match[1].replace(/,/g, "")),
    suffix: match[2],
    useCommas: match[1].includes(","),
  };
}

function formatCount(n: number, useCommas: boolean) {
  const rounded = Math.round(n);
  return useCommas ? rounded.toLocaleString() : String(rounded);
}

export function CountUp({ value, className, durationMs = 1300 }: CountUpProps) {
  const ref = useRef<HTMLSpanElement>(null);
  const [display, setDisplay] = useState(value);
  const hasAnimated = useRef(false);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      setDisplay(value);
      return;
    }

    const parsed = parseCountValue(value);
    if (!parsed) {
      setDisplay(value);
      return;
    }

    const run = () => {
      if (hasAnimated.current) return;
      hasAnimated.current = true;

      const { target, suffix, useCommas } = parsed;
      const start = performance.now();

      const tick = (now: number) => {
        const t = Math.min(1, (now - start) / durationMs);
        const eased = 1 - (1 - t) ** 3;
        setDisplay(`${formatCount(target * eased, useCommas)}${suffix}`);
        if (t < 1) requestAnimationFrame(tick);
      };

      requestAnimationFrame(tick);
    };

    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          run();
          observer.disconnect();
        }
      },
      { threshold: 0.12, rootMargin: "0px 0px -7% 0px" }
    );

    observer.observe(el);
    return () => observer.disconnect();
  }, [durationMs, value]);

  return (
    <span ref={ref} className={cn(className)}>
      {display}
    </span>
  );
}
