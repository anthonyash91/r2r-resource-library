import { cn } from "@/lib/utils";
import { SiteLogoMark } from "@/components/layout/site-logo-mark";
import {
  siteBrandLockupGapClass,
  siteBrandTaglineClass,
  siteBrandTextOffsetClass,
  siteBrandTitleClass,
} from "@/components/layout/site-branding-styles";

interface FooterBrandingLockupProps {
  brandName: string;
  tagline: string;
  className?: string;
  variant?: "default" | "compact";
}

export function FooterBrandingLockup({
  brandName,
  tagline,
  className,
  variant = "default",
}: FooterBrandingLockupProps) {
  const isCompact = variant === "compact";

  return (
    <div className={cn("flex min-w-0 items-center", siteBrandLockupGapClass, className)}>
      <SiteLogoMark variant="white" className={isCompact ? "h-8 w-8" : undefined} />
      <div className={cn("flex min-w-0 flex-col justify-center", !isCompact && siteBrandTextOffsetClass)}>
        <span
          className={cn(
            isCompact
              ? "font-heading text-[18px] font-extrabold leading-none text-[var(--footer-foreground)]"
              : cn(siteBrandTitleClass, "text-[var(--footer-foreground)]")
          )}
        >
          {brandName}
        </span>
        {!isCompact ? (
          <span className={cn(siteBrandTaglineClass, "footer-tagline font-medium")}>{tagline}</span>
        ) : null}
      </div>
    </div>
  );
}
