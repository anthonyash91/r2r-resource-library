import { cn } from "@/lib/utils";

/** Smooth hover/focus color changes — matches app buttons and links. */
export const HEADER_HOVER_TRANSITION =
  "transition-colors duration-200 ease-out motion-reduce:transition-none";

/** Compact header size changes. */
export const HEADER_SIZE_TRANSITION =
  "transition-[height,min-height,width,padding,font-size,line-height,box-shadow] duration-200 ease-out motion-reduce:transition-none";

export const HEADER_INTERACTIVE_TRANSITION = cn(
  "site-header-interactive",
  HEADER_HOVER_TRANSITION,
  HEADER_SIZE_TRANSITION
);

export const HEADER_SHELL_TRANSITION =
  "transition-[min-height,box-shadow] duration-200 ease-out motion-reduce:transition-none";

const headerNavTypography = "font-heading text-[15px] font-semibold leading-none";

export function headerNavLinkClass(isCompact: boolean, isActive: boolean) {
  return cn(
    "inline-flex shrink-0 cursor-pointer items-center justify-center whitespace-nowrap",
    HEADER_INTERACTIVE_TRANSITION,
    headerNavTypography,
    isCompact ? "text-sm" : "text-[15px]",
    "focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2",
    isActive
      ? "text-[var(--accent-ink)]"
      : "text-foreground hover:text-[var(--accent-ink)]"
  );
}

export function headerTextActionClass(isCompact: boolean) {
  return cn(
    "inline-flex shrink-0 cursor-pointer items-center justify-center whitespace-nowrap",
    HEADER_INTERACTIVE_TRANSITION,
    headerNavTypography,
    isCompact ? "text-sm" : "text-[15px]",
    "text-foreground hover:text-[var(--accent-ink)]",
    "focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2"
  );
}

export function headerCtaClass(isCompact: boolean) {
  return cn(
    "inline-flex h-auto min-h-0 shrink-0 cursor-pointer items-center justify-center whitespace-nowrap rounded-[9px] border-0 bg-[var(--coral)] font-heading font-bold leading-none text-white",
    HEADER_INTERACTIVE_TRANSITION,
    "hover:bg-[var(--coral-hover)]",
    "focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2",
    isCompact ? "px-3.5 py-1.5 text-[13px]" : "px-[18px] py-2 text-[14px]"
  );
}

export function headerOutlineActionClass(isCompact: boolean) {
  return cn(
    "inline-flex shrink-0 cursor-pointer items-center justify-center whitespace-nowrap rounded-[9px] border border-border bg-transparent font-heading font-semibold text-foreground",
    HEADER_INTERACTIVE_TRANSITION,
    "hover:bg-muted",
    "focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2",
    isCompact ? "px-3 py-2 text-sm" : "px-4 py-2.5 text-[15px]"
  );
}

export function headerIconActionClass(isCompact: boolean, isActive = false) {
  return cn(headerNavLinkClass(isCompact, isActive), "gap-1.5");
}

/** @deprecated Use headerTextActionClass or headerCtaClass — kept for language switcher sizing */
export function headerControlSizeClass(isCompact: boolean) {
  return isCompact ? "h-8 min-h-8 px-2 text-sm" : "h-9 min-h-9 px-3 text-[15px]";
}

/** @deprecated Use headerTextActionClass or headerCtaClass */
export function headerButtonSizeClass(isCompact: boolean) {
  return cn(HEADER_INTERACTIVE_TRANSITION, headerControlSizeClass(isCompact));
}

export function headerIconButtonClass(isCompact: boolean) {
  return cn(
    "inline-flex cursor-pointer items-center justify-center rounded-lg border border-border text-foreground",
    HEADER_INTERACTIVE_TRANSITION,
    "hover:bg-muted focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2",
    isCompact ? "h-8 w-8 min-h-8 min-w-8" : "h-9 w-9 min-h-9 min-w-9"
  );
}

export function headerMobileLinkClass(isActive: boolean) {
  return cn(
    "flex min-h-[44px] cursor-pointer items-center gap-3 rounded-xl px-4 py-2.5 text-base font-medium site-header-interactive",
    HEADER_HOVER_TRANSITION,
    "focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring",
    isActive
      ? "bg-secondary text-[var(--accent-ink)]"
      : "text-foreground hover:bg-muted"
  );
}

export function headerHomeLinkClass() {
  return cn(
    "flex min-w-0 shrink-0 items-center rounded-lg site-header-interactive",
    "transition-opacity duration-200 ease-out motion-reduce:transition-none",
    "hover:opacity-90 focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring"
  );
}
