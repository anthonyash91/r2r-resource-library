"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { cn } from "@/lib/utils";

interface RotatingNavTaglineProps {
  phrases: string[];
  className?: string;
  intervalMs?: number;
}

/** Matches Tailwind `h-5` / `leading-5` (1.25rem). */
const LINE_HEIGHT = "1.25rem";
const TRANSITION_MS = 500;

export function RotatingNavTagline({
  phrases,
  className,
  intervalMs = 3500,
}: RotatingNavTaglineProps) {
  const [index, setIndex] = useState(0);
  const [animate, setAnimate] = useState(true);
  const [reduceMotion, setReduceMotion] = useState(false);

  const items = useMemo(
    () => phrases.map((phrase) => phrase.trim()).filter(Boolean),
    [phrases]
  );

  const loopItems = useMemo(
    () => (items.length > 1 ? [...items, items[0]] : items),
    [items]
  );

  useEffect(() => {
    const media = window.matchMedia("(prefers-reduced-motion: reduce)");
    const update = () => setReduceMotion(media.matches);
    update();
    media.addEventListener("change", update);
    return () => media.removeEventListener("change", update);
  }, []);

  useEffect(() => {
    if (items.length <= 1 || reduceMotion) return;

    const timer = window.setInterval(() => {
      setIndex((current) => (current >= items.length ? current : current + 1));
    }, intervalMs);

    return () => window.clearInterval(timer);
  }, [items.length, intervalMs, reduceMotion]);

  const handleTransitionEnd = useCallback(() => {
    if (items.length <= 1) return;

    if (index === items.length) {
      setAnimate(false);
      setIndex(0);
      requestAnimationFrame(() => {
        requestAnimationFrame(() => setAnimate(true));
      });
    }
  }, [index, items.length]);

  if (items.length === 0) return null;

  if (items.length === 1) {
    return (
      <span className={cn("block truncate text-sm leading-5 text-muted-foreground", className)}>
        {items[0]}
      </span>
    );
  }

  return (
    <span
      className={cn(
        "block overflow-hidden text-sm leading-5 text-muted-foreground",
        className
      )}
      style={{ height: LINE_HEIGHT }}
    >
      <span className="sr-only">{items.join(" ")}</span>
      <span
        aria-hidden="true"
        onTransitionEnd={animate ? handleTransitionEnd : undefined}
        className={cn(
          "block ease-in-out motion-reduce:transition-none",
          animate && !reduceMotion ? "transition-transform duration-500" : ""
        )}
        style={{
          transform: `translateY(calc(-${index} * ${LINE_HEIGHT}))`,
          transitionDuration: animate && !reduceMotion ? `${TRANSITION_MS}ms` : "0ms",
        }}
      >
        {loopItems.map((phrase, itemIndex) => (
          <span
            key={`${phrase}-${itemIndex}`}
            className="block truncate whitespace-nowrap"
            style={{ height: LINE_HEIGHT, lineHeight: LINE_HEIGHT }}
          >
            {phrase}
          </span>
        ))}
      </span>
    </span>
  );
}
