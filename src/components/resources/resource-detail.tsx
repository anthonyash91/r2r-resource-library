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
  Navigation,
  ArrowLeft,
} from "lucide-react";
import { CategoryBadge } from "@/components/resources/category-badge";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { ResourceMasonry } from "@/components/resources/resource-masonry";
import { formatPhone, formatDate, getDirectionsUrl, shareResource, cn } from "@/lib/utils";
import { useSaved } from "@/lib/saved-context";
import { useAuth } from "@/lib/auth-context";
import type { Resource } from "@/types";
import { useTranslations } from "@/i18n/locale-context";

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

        <header className="mb-8">
          <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
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
          <h1 className="mb-4 text-3xl font-bold sm:text-4xl">{resource.name}</h1>
          <p className="text-lg text-muted-foreground">{resource.description}</p>
        </header>

        <div className="grid gap-6 lg:grid-cols-3">
          <div className="space-y-6 lg:col-span-2">
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
                <h2 className="mb-4 text-xl font-bold">{t("resources.whoCanUse")}</h2>
                <p className="text-base text-muted-foreground">{resource.eligibility}</p>
              </Card>
            )}

            {resource.tags.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {resource.tags.map((tag) => (
                  <Badge key={tag} variant="secondary">
                    {tag}
                  </Badge>
                ))}
              </div>
            )}
          </div>

          <aside className="space-y-4">
            <Card>
              <h2 className="mb-4 text-xl font-bold">{t("resources.contactInfo")}</h2>
              <dl className="space-y-4">
                {fullAddress && (
                  <div>
                    <dt className="flex items-center gap-2 font-semibold">
                      <MapPin className="h-5 w-5 text-primary" aria-hidden="true" />
                      {t("resources.address")}
                    </dt>
                    <dd className="mt-1 pl-7 text-base text-muted-foreground">{fullAddress}</dd>
                    <a
                      href={getDirectionsUrl(fullAddress)}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="mt-2 inline-flex items-center gap-2 pl-7 text-base font-semibold text-primary hover:underline"
                    >
                      <Navigation className="h-4 w-4" aria-hidden="true" />
                      {t("resources.getDirections")}
                    </a>
                  </div>
                )}
                {resource.phone && (
                  <div>
                    <dt className="flex items-center gap-2 font-semibold">
                      <Phone className="h-5 w-5 text-primary" aria-hidden="true" />
                      {t("resources.phone")}
                    </dt>
                    <dd className="mt-1 pl-7">
                      <a
                        href={`tel:${resource.phone}`}
                        className="text-base text-primary hover:underline"
                      >
                        {formatPhone(resource.phone)}
                      </a>
                    </dd>
                  </div>
                )}
                {resource.website && (
                  <div>
                    <dt className="flex items-center gap-2 font-semibold">
                      <Globe className="h-5 w-5 text-primary" aria-hidden="true" />
                      {t("resources.website")}
                    </dt>
                    <dd className="mt-1 pl-7">
                      <a
                        href={resource.website}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-base text-primary hover:underline break-all"
                      >
                        {t("resources.visitWebsite")}
                      </a>
                    </dd>
                  </div>
                )}
                {resource.email && (
                  <div>
                    <dt className="flex items-center gap-2 font-semibold">
                      <Mail className="h-5 w-5 text-primary" aria-hidden="true" />
                      {t("admin.email")}
                    </dt>
                    <dd className="mt-1 pl-7">
                      <a
                        href={`mailto:${resource.email}`}
                        className="text-base text-primary hover:underline break-all"
                      >
                        {resource.email}
                      </a>
                    </dd>
                  </div>
                )}
                {resource.hours && (
                  <div>
                    <dt className="flex items-center gap-2 font-semibold">
                      <Clock className="h-5 w-5 text-primary" aria-hidden="true" />
                      {t("resources.hours")}
                    </dt>
                    <dd className="mt-1 pl-7 text-base text-muted-foreground">
                      {resource.hours}
                    </dd>
                  </div>
                )}
              </dl>
            </Card>

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
            <ResourceMasonry resources={related} columns={2} />
          </section>
        )}
      </div>
    </div>
  );
}
