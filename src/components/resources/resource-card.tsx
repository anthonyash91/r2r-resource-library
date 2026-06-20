"use client";

import Link from "next/link";
import { Heart, MapPin, Phone, Globe } from "lucide-react";
import type { Resource } from "@/types";
import { CategoryBadge } from "@/components/resources/category-badge";
import { Card } from "@/components/ui/card";
import { formatPhone, formatWebsiteDisplay, cn } from "@/lib/utils";
import { useSaved } from "@/lib/saved-context";
import { useAuth } from "@/lib/auth-context";
import { useTranslations } from "@/i18n/locale-context";

interface ResourceCardProps {
  resource: Resource;
  showSave?: boolean;
  variant?: "default" | "compact";
  clampDescription?: boolean;
}

export function ResourceCard({
  resource,
  showSave = true,
  variant = "default",
  clampDescription = false,
}: ResourceCardProps) {
  const { isSaved, toggleSave } = useSaved();
  const { user } = useAuth();
  const { t } = useTranslations();
  const saved = isSaved(resource.id);
  const isCompact = variant === "compact";

  const handleSave = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (!user) {
      window.location.href = "/login";
      return;
    }
    toggleSave(resource.id);
  };

  const hasContactInfo =
    resource.city ||
    resource.state ||
    resource.phone ||
    resource.website;

  return (
    <Card className={isCompact ? "p-4" : undefined}>
      <div className={cn("flex flex-wrap items-center justify-between gap-2", isCompact ? "mb-2" : "mb-3")}>
        <div className="flex flex-wrap items-center gap-2">
          {resource.category && (
            <CategoryBadge category={resource.category} size={isCompact ? "sm" : "default"} />
          )}
        </div>
        {showSave && !isCompact && (
          <button
            type="button"
            onClick={handleSave}
            aria-label={
              saved
                ? t("resources.removeSaveAria", { name: resource.name })
                : t("resources.saveAria", { name: resource.name })
            }
            aria-pressed={saved}
            className={cn(
              "inline-flex shrink-0 cursor-pointer items-center gap-1.5 rounded-full px-3 py-1 text-sm font-medium transition-colors",
              "focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring",
              saved
                ? "bg-primary text-primary-foreground hover:bg-primary-hover"
                : "border border-primary bg-transparent text-primary hover:bg-primary/10"
            )}
          >
            <Heart className={cn("h-3.5 w-3.5", saved && "fill-current")} aria-hidden="true" />
            {saved ? t("common.saved") : t("common.save")}
          </button>
        )}
      </div>

      <h3
        className={cn(
          "font-bold text-foreground",
          isCompact ? "mb-1.5 line-clamp-2 text-lg leading-snug" : "mb-2 text-xl"
        )}
      >
        {resource.name}
      </h3>
      <p
        className={cn(
          "text-muted-foreground",
          isCompact
            ? "mb-0 line-clamp-2 text-sm leading-relaxed"
            : cn("mb-0 text-base", clampDescription && "line-clamp-3 leading-relaxed")
        )}
      >
        {resource.description}
      </p>

      {hasContactInfo && (
        <div
          className={cn(
            "space-y-1.5 border-t border-border text-muted-foreground",
            isCompact ? "mb-3 mt-3 pt-3 text-xs" : "mb-4 mt-4 space-y-2 pt-4 text-sm"
          )}
        >
          {(resource.city || resource.state) && (
            <p className="flex items-center gap-2">
              <MapPin
                className={cn("shrink-0 text-primary", isCompact ? "h-3.5 w-3.5" : "h-4 w-4")}
                aria-hidden="true"
              />
              {[resource.city, resource.state].filter(Boolean).join(", ")}
            </p>
          )}
          {!isCompact && resource.phone && (
            <p className="flex items-center gap-2">
              <Phone className="h-4 w-4 shrink-0 text-primary" aria-hidden="true" />
              {formatPhone(resource.phone)}
            </p>
          )}
          {!isCompact && resource.website && (
            <p className="flex items-center gap-2">
              <Globe className="h-4 w-4 shrink-0 text-primary" aria-hidden="true" />
              <a
                href={resource.website}
                target="_blank"
                rel="noopener noreferrer"
                className="truncate text-primary hover:underline"
              >
                {formatWebsiteDisplay(resource.website)}
              </a>
            </p>
          )}
        </div>
      )}

      <Link
        href={`/resources/${resource.id}`}
        className={cn(
          "block w-full rounded-xl border-2 border-primary bg-transparent text-center font-semibold text-primary transition-colors",
          "hover:bg-secondary focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2",
          isCompact ? "px-3 py-1.5 text-xs" : "px-3 py-2 text-sm"
        )}
      >
        {t("resources.viewDetails")}
      </Link>
    </Card>
  );
}
