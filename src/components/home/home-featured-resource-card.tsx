"use client";

import Link from "next/link";
import { Globe, MapPin, Phone } from "lucide-react";
import type { Resource } from "@/types";
import { useSaved } from "@/lib/saved-context";
import { useAuth } from "@/lib/auth-context";
import { useSignInHref } from "@/hooks/use-sign-in-href";
import { useCategoryLabel } from "@/i18n/use-category-label";
import { useTranslations } from "@/i18n/locale-context";
import { cn, formatPhone, formatWebsiteDisplay, truncateDescriptionPreview } from "@/lib/utils";
import { getResourceIntakeSignals } from "@/lib/intake-signals";

interface HomeFeaturedResourceCardProps {
  resource: Resource;
}

export function HomeFeaturedResourceCard({ resource }: HomeFeaturedResourceCardProps) {
  const { t } = useTranslations();
  const getCategoryLabel = useCategoryLabel();
  const categoryLabel = resource.category ? getCategoryLabel(resource.category) : null;
  const { isSaved, toggleSave } = useSaved();
  const { user } = useAuth();
  const signInHref = useSignInHref();
  const saved = isSaved(resource.id);
  const signals = getResourceIntakeSignals(resource);

  const locationLine =
    [resource.address, resource.city, resource.state].filter(Boolean).join(", ") || null;

  const statusLabel = signals.includes("referral_required")
    ? t("home.featuredByAppointment")
    : signals.includes("walk_in_ok")
      ? t("home.mockOpenNow")
      : null;

  const statusColor = signals.includes("referral_required") ? "text-[#E59400]" : "text-[#22835D]";
  const statusDot = signals.includes("referral_required") ? "bg-[#E59400]" : "bg-[#22835D]";

  const handleSave = () => {
    if (!user) {
      window.location.href = signInHref;
      return;
    }
    toggleSave(resource.id);
  };

  return (
    <article className="flex flex-col rounded-[16px] border border-[var(--line)] bg-white p-[22px]">
      <div className="font-heading text-[18px] font-bold leading-[1.25] text-foreground">
        {resource.name}
      </div>

      <div className="mt-[9px] flex flex-wrap items-center gap-[9px] font-sans text-[13px] font-semibold leading-none">
        {categoryLabel ? (
          <span className="font-bold text-[var(--accent-ink)]">{categoryLabel}</span>
        ) : null}
        {categoryLabel && statusLabel ? (
          <span className="h-[3px] w-[3px] rounded-full bg-[#C7C5D2]" aria-hidden="true" />
        ) : null}
        {statusLabel ? (
          <span className={cn("inline-flex items-center gap-[5px]", statusColor)}>
            <span className={cn("h-[7px] w-[7px] rounded-full", statusDot)} aria-hidden="true" />
            {statusLabel}
          </span>
        ) : null}
      </div>

      <p className="mt-[13px] line-clamp-2 font-sans text-[14px] font-normal leading-[1.55] text-muted-foreground">
        {truncateDescriptionPreview(resource.description, resource.id, { min: 80, max: 140 })}
      </p>

      <div className="mt-[13px] flex flex-col gap-2 font-sans text-[13.5px] font-normal leading-[1.4] text-muted-foreground">
        {locationLine ? (
          <div className="flex items-center gap-[9px]">
            <MapPin className="h-[15px] w-[15px] shrink-0 text-[#9aa0b4]" aria-hidden="true" />
            <span>{locationLine}</span>
          </div>
        ) : null}
        {resource.phone ? (
          <div className="flex items-center gap-[9px]">
            <Phone className="h-[15px] w-[15px] shrink-0 text-[#9aa0b4]" aria-hidden="true" />
            <span>{formatPhone(resource.phone)}</span>
          </div>
        ) : null}
        {resource.website ? (
          <div className="flex items-center gap-[9px]">
            <Globe className="h-[15px] w-[15px] shrink-0 text-[#9aa0b4]" aria-hidden="true" />
            <span className="font-semibold text-[var(--accent-ink)]">
              {formatWebsiteDisplay(resource.website)}
            </span>
          </div>
        ) : null}
      </div>

      <div className="mt-[18px] flex gap-[10px]">
        <Link
          href={`/resources/${resource.id}`}
          className="flex flex-1 items-center justify-center rounded-[9px] bg-primary px-3 py-3 text-center font-heading text-[13px] font-bold leading-none text-primary-foreground"
        >
          {t("home.featuredDetails")}
        </Link>
        <button
          type="button"
          onClick={handleSave}
          aria-pressed={saved}
          className="flex flex-1 items-center justify-center rounded-[9px] border-[1.5px] border-[var(--line)] bg-white px-3 py-3 text-center font-heading text-[13px] font-bold leading-none text-foreground"
        >
          {saved ? t("common.saved") : t("common.save")}
        </button>
      </div>
    </article>
  );
}
