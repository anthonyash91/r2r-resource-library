"use client";

import { useEffect, useRef, useState, type CSSProperties, type ReactNode } from "react";
import { cn } from "@/lib/utils";

export type ScrollRevealVariant =
  | "fade-up"
  | "fade-down"
  | "fade-in"
  | "zoom-in"
  | "slide-left"
  | "slide-right"
  | "blur-up";

interface ScrollRevealProps {
  children: ReactNode;
  className?: string;
  variant?: ScrollRevealVariant;
  /** Stagger delay in milliseconds */
  delay?: number;
  once?: boolean;
  threshold?: number;
  rootMargin?: string;
  /** Reveal immediately after mount when already in the viewport (e.g. load-more batch). */
  revealOnMountIfVisible?: boolean;
  /** Only reveal while the user is scrolling down. */
  revealOnScrollDownOnly?: boolean;
}

function parseRootMarginBottom(rootMargin: string): number {
  const parts = rootMargin.trim().split(/\s+/);
  const bottom = parts.length >= 3 ? parts[2] : parts[0];
  const match = bottom.match(/^(-?\d+(?:\.\d+)?)(px|rem|em)?$/);
  if (!match) return 0;

  const value = Number.parseFloat(match[1]);
  const unit = match[2] ?? "px";

  if (unit === "rem" || unit === "em") {
    const fontSize =
      Number.parseFloat(getComputedStyle(document.documentElement).fontSize) || 16;
    return value * fontSize;
  }

  return value;
}

export function ScrollReveal({
  children,
  className,
  variant = "fade-up",
  delay = 0,
  once = true,
  threshold = 0.08,
  rootMargin = "0px 0px -48px 0px",
  revealOnMountIfVisible = false,
  revealOnScrollDownOnly = false,
}: ScrollRevealProps) {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);
  const revealedRef = useRef(false);
  const lastScrollYRef = useRef(0);

  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      setVisible(true);
      return;
    }

    const element = ref.current;
    if (!element) return;

    lastScrollYRef.current = window.scrollY;
    const bottomInset = Math.abs(parseRootMarginBottom(rootMargin));

    const isInViewport = () => {
      const rect = element.getBoundingClientRect();
      return rect.top < window.innerHeight - bottomInset && rect.bottom > 0;
    };

    const reveal = () => {
      if (revealedRef.current) return false;
      revealedRef.current = true;
      setVisible(true);
      return true;
    };

    const tryReveal = () => {
      if (revealedRef.current || !isInViewport()) return false;
      return reveal();
    };

    let observer: IntersectionObserver | undefined;

    const onScroll = () => {
      if (revealedRef.current) return;

      const currentY = window.scrollY;
      const scrollingDown = currentY > lastScrollYRef.current;
      lastScrollYRef.current = currentY;

      if (revealOnScrollDownOnly && !scrollingDown) return;

      if (tryReveal() && once) {
        observer?.disconnect();
      }
    };

    const scheduleLayoutCheck = () => {
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          if (tryReveal() && once) {
            observer?.disconnect();
          }
        });
      });
    };

    const frame = requestAnimationFrame(() => {
      if (!revealOnScrollDownOnly) {
        observer = new IntersectionObserver(
          ([entry]) => {
            if (entry.isIntersecting) {
              if (reveal() && once) observer?.disconnect();
            } else if (!once) {
              revealedRef.current = false;
              setVisible(false);
            }
          },
          { threshold, rootMargin }
        );

        observer.observe(element);
      }

      if (revealOnMountIfVisible) {
        scheduleLayoutCheck();
      }
    });

    window.addEventListener("scroll", onScroll, { passive: true });

    const resizeObserver =
      revealOnMountIfVisible
        ? new ResizeObserver(() => {
            if (revealedRef.current) return;
            if (tryReveal() && once) {
              observer?.disconnect();
            }
          })
        : null;

    if (resizeObserver) {
      resizeObserver.observe(element);
    }

    return () => {
      cancelAnimationFrame(frame);
      observer?.disconnect();
      resizeObserver?.disconnect();
      window.removeEventListener("scroll", onScroll);
    };
  }, [
    revealOnMountIfVisible,
    revealOnScrollDownOnly,
    once,
    threshold,
    rootMargin,
  ]);

  const style = { "--scroll-reveal-delay": `${delay}ms` } as CSSProperties;

  return (
    <div
      ref={ref}
      className={cn(
        "scroll-reveal",
        `scroll-reveal--${variant}`,
        visible && "scroll-reveal--visible",
        className
      )}
      style={style}
    >
      {children}
    </div>
  );
}
