"use client";

import Link from "next/link";
import { MapPin, Phone, Globe } from "lucide-react";
import type { Resource } from "@/types";
import { CategoryBadge } from "@/components/resources/category-badge";
import { StatewideBadge } from "@/components/resources/statewide-badge";
import { SaveResourceButton } from "@/components/resources/save-resource-button";
import { Card } from "@/components/ui/card";
import { formatPhone, formatWebsiteDisplay, truncateDescriptionPreview, cn } from "@/lib/utils";
import { useSaved } from "@/lib/saved-context";
import { useAuth } from "@/lib/auth-context";
import { useTranslations } from "@/i18n/locale-context";

interface ResourceCardProps {
  resource: Resource;
  showSave?: boolean;
  variant?: "default" | "compact";
}

export function ResourceCard({
  resource,
  showSave = true,
  variant = "default",
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

  const locationLine =
    [resource.address, resource.city, resource.state].filter(Boolean).join(", ") || null;

  const hasContactInfo =
    locationLine ||
    resource.phone ||
    resource.website;

  const descriptionPreview = truncateDescriptionPreview(
    resource.description,
    resource.id,
    isCompact ? { min: 65, max: 105 } : { min: 95, max: 145 }
  );

  return (
    <Card className={isCompact ? "p-5 sm:p-6" : undefined}>
      <div
        className={cn(
          "items-start gap-x-2",
          showSave && !isCompact ? "grid grid-cols-[1fr_auto]" : "flex flex-wrap gap-2",
          isCompact ? "mb-2" : "mb-3"
        )}
      >
        <div className="flex min-w-0 flex-wrap items-center gap-2">
          {resource.category && (
            <CategoryBadge category={resource.category} size={isCompact ? "sm" : "default"} />
          )}
          <StatewideBadge resource={resource} size={isCompact ? "sm" : "default"} />
        </div>
        {showSave && !isCompact && (
          <SaveResourceButton
            saved={saved}
            onClick={handleSave}
            className="shrink-0"
            ariaLabel={
              saved
                ? t("resources.removeSaveAria", { name: resource.name })
                : t("resources.saveAria", { name: resource.name })
            }
          />
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
          "text-muted-foreground leading-relaxed",
          isCompact ? "mb-0 text-sm" : "mb-0 text-base"
        )}
      >
        {descriptionPreview}
      </p>

      {hasContactInfo && (
        <div
          className={cn(
            "space-y-1.5 border-t border-border text-muted-foreground",
            isCompact ? "mb-3 mt-3 pt-3 text-xs" : "mb-4 mt-4 space-y-2 pt-4 text-sm"
          )}
        >
          {locationLine && (
            <p className="flex min-w-0 items-center gap-2">
              <MapPin
                className={cn("shrink-0 text-primary", isCompact ? "h-3.5 w-3.5" : "h-4 w-4")}
                aria-hidden="true"
              />
              <span className="min-w-0 truncate" title={locationLine}>
                {locationLine}
              </span>
            </p>
          )}
          {!isCompact && resource.phone && (
            <p className="flex items-center gap-2">
              <Phone className="h-4 w-4 shrink-0 text-primary" aria-hidden="true" />
              {formatPhone(resource.phone)}
            </p>
          )}
          {!isCompact && resource.website && (
            <p className="flex min-w-0 items-center gap-2">
              <Globe className="h-4 w-4 shrink-0 text-primary" aria-hidden="true" />
              <a
                href={resource.website}
                target="_blank"
                rel="noopener noreferrer"
                title={formatWebsiteDisplay(resource.website)}
                className="min-w-0 truncate text-primary hover:underline"
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
