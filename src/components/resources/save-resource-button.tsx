"use client";

import { BookmarkMinus, BookmarkPlus } from "lucide-react";
import { resourceBadgeClass } from "@/components/layout/site-branding-styles";
import { cn } from "@/lib/utils";
import { useTranslations } from "@/i18n/locale-context";

interface SaveResourceButtonProps {
  saved: boolean;
  onClick: (e: React.MouseEvent) => void;
  ariaLabel: string;
  showLabel?: boolean;
  className?: string;
}

export function SaveResourceButton({
  saved,
  onClick,
  ariaLabel,
  showLabel = false,
  className,
}: SaveResourceButtonProps) {
  const { t } = useTranslations();
  const label = saved ? t("common.saved") : t("common.save");

  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={ariaLabel}
      aria-pressed={saved}
      className={cn(
        showLabel ? resourceBadgeClass : "save-resource-button",
        "shrink-0 cursor-pointer focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring",
        saved && "save-resource-button--saved",
        className
      )}
    >
      {saved ? (
        <BookmarkMinus aria-hidden="true" />
      ) : (
        <BookmarkPlus aria-hidden="true" />
      )}
      {showLabel ? <span>{label}</span> : null}
    </button>
  );
}
