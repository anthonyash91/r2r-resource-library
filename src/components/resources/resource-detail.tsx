"use client";

import { useEffect } from "react";
import Link from "next/link";
import {
  MapPin,
  Phone,
  Globe,
  Mail,
  Clock,
  Heart,
  Share2,
  ArrowLeft,
} from "lucide-react";
import { CategoryBadge } from "@/components/resources/category-badge";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { ResourceMasonry } from "@/components/resources/resource-masonry";
import { formatPhone, formatDate, formatWebsiteDisplay, shareResource, cn } from "@/lib/utils";
import { useSaved } from "@/lib/saved-context";
import { useAuth } from "@/lib/auth-context";
import type { Resource } from "@/types";
import { useTranslations } from "@/i18n/locale-context";
import { formatOperatingHours } from "@/i18n/localize-content";

interface ResourceDetailProps {
  resource: Resource;
  related: Resource[];
}

export function ResourceDetailView({ resource, related }: ResourceDetailProps) {
  const { isSaved, toggleSave, recordView } = useSaved();
  const { user } = useAuth();
  const { t, locale } = useTranslations();
  const saved = isSaved(resource.id);

  useEffect(() => {
    recordView(resource);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [resource.id]);

  const fullAddress = [resource.address, resource.city, resource.state]
    .filter(Boolean)
    .join(", ");

  const handleSave = () => {
    if (!user) {
      window.location.href = "/login";
      return;
    }
    toggleSave(resource.id);
  };

  const handleShare = () => {
    shareResource(resource.name, window.location.href);
  };

  return (
    <div className="px-4 py-10 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-4xl">
        <Link
          href="/resources"
          className="mb-6 inline-flex items-center gap-2 text-base font-medium text-primary hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring rounded"
        >
          <ArrowLeft className="h-5 w-5" aria-hidden="true" />
          {t("resources.backToResources")}
        </Link>

        <header className="mb-6">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="flex flex-wrap items-center gap-2">
              {resource.category && (
                <CategoryBadge category={resource.category} />
              )}
            </div>
            <div className="flex items-center gap-2">
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
                  "inline-flex cursor-pointer items-center gap-1.5 rounded-full px-3 py-1 text-sm font-medium transition-colors",
                  "focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring",
                  saved
                    ? "bg-primary text-primary-foreground hover:bg-primary-hover"
                    : "border border-primary bg-transparent text-primary hover:bg-primary/10"
                )}
              >
                <Heart className={cn("h-3.5 w-3.5", saved && "fill-current")} aria-hidden="true" />
                {saved ? t("common.saved") : t("common.save")}
              </button>
              <button
                type="button"
                onClick={handleShare}
                className={cn(
                  "inline-flex cursor-pointer items-center gap-1.5 rounded-full border border-primary bg-transparent px-3 py-1 text-sm font-medium text-primary transition-colors",
                  "hover:bg-primary/10 focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
                )}
              >
                <Share2 className="h-3.5 w-3.5" aria-hidden="true" />
                {t("common.share")}
              </button>
            </div>
          </div>
        </header>

        <div className="grid gap-6 lg:grid-cols-3">
          <div className="space-y-6 lg:col-span-2">
            <Card>
              <h1 className="mb-4 text-xl font-bold">{resource.name}</h1>
              <p className="text-base text-muted-foreground">{resource.description}</p>
            </Card>

            {resource.services.length > 0 && (
              <Card>
                <h2 className="mb-4 text-xl font-bold">{t("resources.servicesOffered")}</h2>
                <ul className="grid gap-2 sm:grid-cols-2">
                  {resource.services.map((service) => (
                    <li
                      key={service}
                      className="flex items-center gap-2 text-base before:content-['✓'] before:font-bold before:text-success"
                    >
                      {service}
                    </li>
                  ))}
                </ul>
              </Card>
            )}

            {resource.eligibility && (
              <Card>
                <h2 className="mb-4 text-xl font-bold">{t("resources.eligibilityRequirements")}</h2>
                <p className="text-base text-muted-foreground">{resource.eligibility}</p>
              </Card>
            )}
          </div>

          <aside className="space-y-4">
            <Card>
              <h2 className="mb-4 text-xl font-bold">{t("resources.contactInfo")}</h2>
              <div className="space-y-3">
                {fullAddress && (
                  <p className="flex items-start gap-2 text-base text-muted-foreground">
                    <MapPin className="mt-0.5 h-5 w-5 shrink-0 text-primary" aria-hidden="true" />
                    {fullAddress}
                  </p>
                )}
                {resource.phone && (
                  <p className="flex items-center gap-2">
                    <Phone className="h-5 w-5 shrink-0 text-primary" aria-hidden="true" />
                    <a
                      href={`tel:${resource.phone}`}
                      className="text-base text-primary hover:underline"
                    >
                      {formatPhone(resource.phone)}
                    </a>
                  </p>
                )}
                {resource.website && (
                  <p className="flex items-center gap-2">
                    <Globe className="h-5 w-5 shrink-0 text-primary" aria-hidden="true" />
                    <a
                      href={resource.website}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="break-all text-base text-primary hover:underline"
                    >
                      {formatWebsiteDisplay(resource.website)}
                    </a>
                  </p>
                )}
                {resource.email && (
                  <p className="flex items-center gap-2">
                    <Mail className="h-5 w-5 shrink-0 text-primary" aria-hidden="true" />
                    <a
                      href={`mailto:${resource.email}`}
                      className="break-all text-base text-primary hover:underline"
                    >
                      {resource.email}
                    </a>
                  </p>
                )}
                {resource.hours && (
                  <p className="flex items-start gap-2 text-base text-muted-foreground">
                    <Clock className="mt-0.5 h-5 w-5 shrink-0 text-primary" aria-hidden="true" />
                    {formatOperatingHours(resource.hours, locale)}
                  </p>
                )}
              </div>
            </Card>

            {resource.tags.length > 0 && (
              <Card>
                <h2 className="mb-4 text-xl font-bold">{t("resources.tags")}</h2>
                <div className="flex flex-wrap gap-2">
                  {resource.tags.map((tag) => (
                    <Link
                      key={tag}
                      href={`/resources?tag=${encodeURIComponent(tag)}`}
                      className="inline-flex rounded-full focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
                    >
                      <Badge variant="secondary" className="transition-colors hover:bg-muted">
                        {tag}
                      </Badge>
                    </Link>
                  ))}
                </div>
              </Card>
            )}

            <p className="text-sm text-muted-foreground">
              {t("resources.lastUpdated", {
                date: formatDate(resource.updated_at, locale),
              })}
            </p>
          </aside>
        </div>

        {related.length > 0 && (
          <section className="mt-12" aria-labelledby="related-heading">
            <h2 id="related-heading" className="mb-6 text-2xl font-bold">
              {t("resources.relatedResources")}
            </h2>
            <ResourceMasonry resources={related} columns={2} variant="compact" showSave={false} />
          </section>
        )}
      </div>
    </div>
  );
}
