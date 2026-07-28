import { cn } from "@/lib/utils";

interface SiteBrandMarkProps {
  className?: string;
  compact?: boolean;
}

/** Purple swoosh mark from the redesign (replaces the legacy green PNG in the header). */
export function SiteBrandMark({ className, compact = false }: SiteBrandMarkProps) {
  return (
    <span
      className={cn(
        "inline-flex shrink-0 items-center justify-center rounded-[9px] bg-primary",
        compact ? "h-7 w-7" : "h-[34px] w-[34px]",
        className
      )}
      aria-hidden="true"
    >
      <svg
        className={compact ? "h-4 w-4" : "h-5 w-5"}
        viewBox="0 0 24 24"
        fill="none"
        stroke="#fff"
        strokeWidth="2.1"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <path d="M4 19 C8 13 16 13 20 5" />
        <circle cx="20" cy="5" r="1.7" fill="#fff" stroke="none" />
      </svg>
    </span>
  );
}
