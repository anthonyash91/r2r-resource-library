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
}

export function FooterBrandingLockup({
  brandName,
  tagline,
  className,
}: FooterBrandingLockupProps) {
  return (
    <div className={cn("flex min-w-0 items-center", siteBrandLockupGapClass, className)}>
      <SiteLogoMark variant="white" />
      <div className={cn("flex min-w-0 flex-col justify-center", siteBrandTextOffsetClass)}>
        <span className={cn(siteBrandTitleClass, "text-[var(--footer-foreground)]")}>
          {brandName}
        </span>
        <span className={cn(siteBrandTaglineClass, "footer-tagline font-medium")}>
          {tagline}
        </span>
      </div>
    </div>
  );
}
