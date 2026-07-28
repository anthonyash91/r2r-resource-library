"use client";

import { cn } from "@/lib/utils";
import { SiteBrandMark } from "@/components/layout/site-brand-mark";
import {
  siteBrandLockupGapClass,
  siteBrandNavTitleColorClass,
  siteBrandTitleClass,
} from "@/components/layout/site-branding-styles";

const HEADER_COMPACT_TRANSITION =
  "transition-[height,min-height,width,transform,font-size,line-height,opacity] duration-200 ease-out motion-reduce:transition-none";

interface HeaderBrandingLockupProps {
  brandName: string;
  compact?: boolean;
  className?: string;
}

export function HeaderBrandingLockup({
  brandName,
  compact = false,
  className,
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
      <SiteBrandMark compact={compact} />
      <span
        className={cn(
          "truncate font-heading font-extrabold tracking-tight",
          siteBrandNavTitleColorClass,
          HEADER_COMPACT_TRANSITION,
          compact ? "text-base" : siteBrandTitleClass
        )}
      >
        {brandName}
      </span>
    </div>
  );
}
