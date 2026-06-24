"use client";

import { cn } from "@/lib/utils";
import { SiteLogoMark } from "@/components/layout/site-logo-mark";
import { RotatingNavTagline } from "@/components/layout/rotating-nav-tagline";
import {
  siteBrandLockupGapClass,
  siteBrandNavTitleColorClass,
  siteBrandTextOffsetClass,
  siteBrandTitleClass,
} from "@/components/layout/site-branding-styles";

const HEADER_COMPACT_TRANSITION =
  "transition-[height,min-height,width,transform,font-size,line-height,opacity,grid-template-rows] duration-200 ease-out motion-reduce:transition-none";

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
    <div
      className={cn(
        "flex min-w-0 items-center",
        siteBrandLockupGapClass,
        HEADER_COMPACT_TRANSITION,
        className
      )}
    >
      <SiteLogoMark
        variant="green"
        className={cn(HEADER_COMPACT_TRANSITION, compact ? "h-8 w-auto" : "h-10 w-auto")}
      />
      <div
        className={cn(
          "flex min-w-0 flex-col justify-center",
          HEADER_COMPACT_TRANSITION,
          compact ? "translate-y-0" : siteBrandTextOffsetClass,
          textWrapperClassName
        )}
      >
        <span
          className={cn(
            "block truncate font-bold",
            HEADER_COMPACT_TRANSITION,
            siteBrandNavTitleColorClass,
            compact ? "h-8 text-base leading-8" : siteBrandTitleClass
          )}
        >
          {brandName}
        </span>
        <div
          className={cn(
            "grid overflow-hidden",
            HEADER_COMPACT_TRANSITION,
            compact ? "grid-rows-[0fr] opacity-0" : "grid-rows-[1fr] opacity-100"
          )}
          aria-hidden={compact}
        >
          <div className="min-h-0">
            <RotatingNavTagline phrases={taglinePhrases} />
          </div>
        </div>
      </div>
    </div>
  );
}
