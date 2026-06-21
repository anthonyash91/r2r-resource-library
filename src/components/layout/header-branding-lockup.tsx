"use client";

import { cn } from "@/lib/utils";
import { SiteLogoMark } from "@/components/layout/site-logo-mark";
import { RotatingNavTagline } from "@/components/layout/rotating-nav-tagline";
import {
  siteBrandLockupGapClass,
  siteBrandTextOffsetClass,
  siteBrandTitleClass,
} from "@/components/layout/site-branding-styles";

interface HeaderBrandingLockupProps {
  brandName: string;
  taglinePhrases: string[];
  textWrapperClassName?: string;
  className?: string;
}

export function HeaderBrandingLockup({
  brandName,
  taglinePhrases,
  textWrapperClassName,
  className,
}: HeaderBrandingLockupProps) {
  return (
    <div className={cn("flex min-w-0 items-center", siteBrandLockupGapClass, className)}>
      <SiteLogoMark variant="green" />
      <div className={cn("flex min-w-0 flex-col justify-center", siteBrandTextOffsetClass, textWrapperClassName)}>
        <span className={cn(siteBrandTitleClass, "text-primary")}>{brandName}</span>
        <RotatingNavTagline phrases={taglinePhrases} />
      </div>
    </div>
  );
}
