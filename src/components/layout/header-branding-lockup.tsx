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
  compact?: boolean;
}

export function HeaderBrandingLockup({
  brandName,
  taglinePhrases,
  textWrapperClassName,
  className,
  compact = false,
}: HeaderBrandingLockupProps) {
  return (
    <div className={cn("flex min-w-0 items-center", siteBrandLockupGapClass, className)}>
      <SiteLogoMark
        variant="green"
        className={cn("transition-[height,width] duration-200 ease-out", compact ? "h-8" : "h-10")}
      />
      <div
        className={cn(
          "flex min-w-0 flex-col justify-center",
          !compact && siteBrandTextOffsetClass,
          textWrapperClassName
        )}
      >
        <span
          className={cn(
            "block truncate font-bold text-primary transition-[font-size,line-height,height] duration-200 ease-out",
            compact ? "h-8 text-base leading-8" : siteBrandTitleClass
          )}
        >
          {brandName}
        </span>
        {!compact ? (
          <RotatingNavTagline phrases={taglinePhrases} />
        ) : null}
      </div>
    </div>
  );
}
