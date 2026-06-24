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

export function headerControlSizeClass(isCompact: boolean) {
  return isCompact
    ? "h-9 min-h-9 px-3 text-sm leading-none"
    : "h-11 min-h-11 px-4 text-base leading-none";
}

export function headerNavLinkClass(isCompact: boolean, isActive: boolean) {
  return cn(
    "inline-flex shrink-0 cursor-pointer items-center justify-center whitespace-nowrap rounded-xl font-medium",
    HEADER_INTERACTIVE_TRANSITION,
    headerControlSizeClass(isCompact),
    "focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring",
    isActive
      ? "bg-secondary text-primary hover:bg-secondary/80"
      : "text-foreground hover:bg-muted"
  );
}

export function headerIconActionClass(isCompact: boolean, isActive = false) {
  return cn(headerNavLinkClass(isCompact, isActive), "gap-2");
}

export function headerButtonSizeClass(isCompact: boolean) {
  return cn(HEADER_INTERACTIVE_TRANSITION, headerControlSizeClass(isCompact));
}

export function headerIconButtonClass(isCompact: boolean) {
  return cn(
    "inline-flex cursor-pointer items-center justify-center rounded-xl border border-border text-foreground",
    HEADER_INTERACTIVE_TRANSITION,
    "hover:bg-muted focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2",
    isCompact ? "h-9 w-9 min-h-9 min-w-9" : "h-11 w-11 min-h-11 min-w-11"
  );
}

export function headerMobileLinkClass(isActive: boolean) {
  return cn(
    "flex min-h-[48px] cursor-pointer items-center gap-3 rounded-xl px-4 py-3 text-base font-medium site-header-interactive",
    HEADER_HOVER_TRANSITION,
    "focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring",
    isActive
      ? "bg-secondary text-primary hover:bg-secondary/80"
      : "text-foreground hover:bg-muted"
  );
}

export function headerHomeLinkClass() {
  return cn(
    "flex min-w-0 shrink-0 items-center gap-3 rounded-lg site-header-interactive",
    "transition-opacity duration-200 ease-out motion-reduce:transition-none",
    "hover:opacity-90 focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring"
  );
}
