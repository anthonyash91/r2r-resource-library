"use client";

import { Heart } from "lucide-react";
import { cn } from "@/lib/utils";
import { useTranslations } from "@/i18n/locale-context";

interface SaveResourceButtonProps {
  saved: boolean;
  onClick: (e: React.MouseEvent) => void;
  ariaLabel: string;
  className?: string;
}

export function SaveResourceButton({
  saved,
  onClick,
  ariaLabel,
  className,
}: SaveResourceButtonProps) {
  const { t } = useTranslations();
  const saveLabel = t("common.save");
  const savedLabel = t("common.saved");

  return (
    <button
      type="button"
      onClick={onClick}
      aria-label={ariaLabel}
      aria-pressed={saved}
      className={cn(
        "inline-flex shrink-0 cursor-pointer items-center justify-center gap-1.5 rounded-full border border-primary px-3 py-1 text-sm font-medium transition-colors",
        "focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring",
        saved
          ? "bg-primary text-primary-foreground hover:bg-primary-hover"
          : "bg-transparent text-primary hover:bg-primary/10",
        className
      )}
    >
      <Heart className={cn("h-3.5 w-3.5 shrink-0", saved && "fill-current")} aria-hidden="true" />
      <span className="inline-grid place-items-center [&>span]:col-start-1 [&>span]:row-start-1">
        <span aria-hidden className="invisible">
          {saveLabel}
        </span>
        <span aria-hidden className="invisible">
          {savedLabel}
        </span>
        <span>{saved ? savedLabel : saveLabel}</span>
      </span>
    </button>
  );
}
