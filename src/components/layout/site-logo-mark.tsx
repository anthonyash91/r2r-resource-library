import { cn } from "@/lib/utils";
import { siteBrandLogoClass } from "@/components/layout/site-branding-styles";

const LOGO_SOURCES = {
  green: "/green-logo.svg",
  white: "/white-logo.svg",
} as const;

interface SiteLogoMarkProps {
  variant: keyof typeof LOGO_SOURCES;
  className?: string;
}

export function SiteLogoMark({ variant, className }: SiteLogoMarkProps) {
  return (
    // eslint-disable-next-line @next/next/no-img-element
    <img
      src={LOGO_SOURCES[variant]}
      alt=""
      className={cn("block shrink-0 object-contain", siteBrandLogoClass, className)}
      aria-hidden="true"
    />
  );
}
