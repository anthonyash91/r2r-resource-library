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
}

export function ResourceCard({ resource, showSave = true }: ResourceCardProps) {
  const { isSaved, toggleSave } = useSaved();
  const { user } = useAuth();
  const { t } = useTranslations();
  const saved = isSaved(resource.id);

  const handleSave = (e: React.MouseEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (!user) {
      window.location.href = "/login";
      return;
    }
    toggleSave(resource.id);
  };

  return (
    <Card className="transition-shadow hover:shadow-md">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
        <div className="flex flex-wrap items-center gap-2">
          {resource.category && (
            <CategoryBadge category={resource.category} />
          )}
        </div>
        {showSave && (
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

      <h3 className="mb-2 text-xl font-bold text-foreground">
        {resource.name}
      </h3>
      <p className="mb-0 text-base text-muted-foreground">
        {resource.description}
      </p>

      {(resource.city || resource.state || resource.phone || resource.website) && (
        <div className="mb-4 mt-4 space-y-2 border-t border-border pt-4 text-sm text-muted-foreground">
          {(resource.city || resource.state) && (
            <p className="flex items-center gap-2">
              <MapPin className="h-4 w-4 shrink-0 text-primary" aria-hidden="true" />
              {[resource.city, resource.state].filter(Boolean).join(", ")}
            </p>
          )}
          {resource.phone && (
            <p className="flex items-center gap-2">
              <Phone className="h-4 w-4 shrink-0 text-primary" aria-hidden="true" />
              {formatPhone(resource.phone)}
            </p>
          )}
          {resource.website && (
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
          "block w-full rounded-xl border-2 border-primary bg-transparent px-3 py-2 text-center text-sm font-semibold text-primary transition-colors",
          "hover:bg-secondary focus-visible:outline focus-visible:outline-3 focus-visible:outline-ring focus-visible:outline-offset-2"
        )}
      >
        {t("resources.viewDetails")}
      </Link>
    </Card>
  );
}
