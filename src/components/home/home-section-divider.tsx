import { cn } from "@/lib/utils";

/** Shared horizontal layout for light homepage sections. */
export const homeLightSectionShellClass = "mx-auto w-full max-w-[1180px] px-4 sm:px-9";

/** Shared centered homepage section subtitle — mt-4 below title, mb-11 (44px) below subtitle. */
export const homeSectionSubtitleClass =
  "mx-auto mt-4 mb-11 text-[17px] leading-relaxed text-muted-foreground";

/** Left-aligned homepage section subtitle (account comparison, etc.). */
export const homeSectionSubtitleLeftClass =
  "mt-4 text-[17px] leading-relaxed text-muted-foreground";

/** Max width for centered homepage section subtitles (+40px vs original 520px). */
export const homeSectionSubtitleMaxWidthClass = "max-w-[560px]";

/** Wider homepage section subtitles (featured, hero; +40px vs original 600px). */
export const homeSectionSubtitleWideMaxWidthClass = "max-w-[640px]";

/** Left-aligned / compact homepage subtitles (+40px vs original 420px). */
export const homeSectionSubtitleCompactMaxWidthClass = "max-w-[460px]";

/** Coverage map subtitle (+40px vs original 460px). */
export const homeSectionSubtitleCoverageMaxWidthClass = "max-w-[500px]";

/** Spacing for plain horizontal rules inside dark sections. */
export const homeSectionRuleSpacingClass = "py-12 sm:py-[60px]";

/** White-band air after a dark section (pairs with `.home-page-shell` flex gap). */
export const homeSectionAfterDarkBandClass = "mt-[60px]";

/** White-band air before a dark section (pairs with `.home-page-shell` flex gap). */
export const homeSectionBeforeDarkBandClass = "mb-[75px]";

/** Spacing around the divider above Services ("Everything you need"). */
export const homeSectionDividerServicesClass = "pt-[61px] pb-[51px] -mt-4 -mb-4 sm:-mt-6 sm:-mb-6";

/** Spacing around the divider above Featured resources. */
export const homeSectionDividerFeaturedClass = "pt-[53px] pb-[51px] -mt-4 -mb-4 sm:-mt-6 sm:-mb-6";

/** Cancels shell flex gap; 20px air above the divider line, flush below. */
export const homeSectionDividerFlushClass = "pt-[60px] pb-[51px] -mt-4 -mb-4 sm:-mt-6 sm:-mb-6";

interface HomeSectionDividerProps {
  className?: string;
}

/** Decorative divider — vertical spacing comes from `.home-page-shell` flex gap. */
export function HomeSectionDivider({ className }: HomeSectionDividerProps) {
  return (
    <div
      className={cn(
        "mx-auto flex w-full max-w-[1180px] items-center gap-[18px] px-4 sm:px-9",
        className
      )}
      aria-hidden="true"
    >
      <div className="h-px min-h-px min-w-0 flex-1 shrink-0 bg-gradient-to-r from-transparent to-[var(--line)]" />
      <div className="flex shrink-0 items-center gap-1.5">
        <span className="h-1.5 w-1.5 rounded-full bg-[#FFB35C]" />
        <span className="h-[7px] w-[7px] rounded-full bg-primary" />
        <span className="h-1.5 w-1.5 rounded-full bg-[var(--coral)]" />
      </div>
      <div className="h-px min-h-px min-w-0 flex-1 shrink-0 bg-gradient-to-l from-transparent to-[var(--line)]" />
    </div>
  );
}

/** Horizontal inset for rules placed directly on a section (not inside a padded shell). */
export const homeSectionRuleContainerClass = "mx-auto w-full max-w-[1180px] px-4 sm:px-9";

interface HomeSectionRuleProps {
  className?: string;
  variant?: "light" | "dark";
  /** When false, rule spans the full width of its parent (use inside an already padded shell). */
  inset?: boolean;
}

/** Plain horizontal rule with equal padding above and below. */
export function HomeSectionRule({
  className,
  variant = "light",
  inset = true,
}: HomeSectionRuleProps) {
  return (
    <div
      className={cn(
        inset && homeSectionRuleContainerClass,
        !inset && "w-full",
        homeSectionRuleSpacingClass,
        className
      )}
      aria-hidden="true"
    >
      <div
        className={cn("h-px w-full", variant === "dark" ? "bg-white/14" : "bg-[var(--line)]")}
      />
    </div>
  );
}
