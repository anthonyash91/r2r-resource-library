"use client";

import { useEffect } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import {
  MapPin,
  Phone,
  Globe,
  Mail,
  Clock,
  Share2,
  ArrowLeft,
} from "lucide-react";
import { CategoryBadge } from "@/components/resources/category-badge";
import { StateBadge } from "@/components/resources/state-badge";
import { StatewideBadge } from "@/components/resources/statewide-badge";
import { RegionalBadge } from "@/components/resources/regional-badge";
import { Card, CardDescription, CardHeader } from "@/components/ui/card";
import { ResourceMasonry } from "@/components/resources/resource-masonry";
import { formatPhone, formatDate, formatWebsiteDisplay, shareResource, cn, pageSectionPadding, pageSectionSubheadingClass } from "@/lib/utils";
import { useSaved } from "@/lib/saved-context";
import { useAuth } from "@/lib/auth-context";
import { useSignInHref } from "@/hooks/use-sign-in-href";
import type { Resource } from "@/types";
import { useTranslations } from "@/i18n/locale-context";
import { formatOperatingHours } from "@/i18n/localize-content";
import { SaveResourceButton } from "@/components/resources/save-resource-button";
import { resourceBadgeClass } from "@/components/layout/site-branding-styles";
import { buildResourcesPageHref } from "@/lib/resources-page";
import { ServedCountiesLinks } from "@/components/resources/served-counties-links";
import { countyCoverageLabel, isRegionalResource, shouldShowCountiesServed } from "@/lib/resource-coverage";

interface ResourceDetailProps {
  resource: Resource;
  related: Resource[];
}

const sectionTitleClass = pageSectionSubheadingClass;

export function ResourceDetailView({ resource, related }: ResourceDetailProps) {
  const { isSaved, toggleSave, recordView } = useSaved();
  const { user, loading: authLoading } = useAuth();
  const signInHref = useSignInHref();
  const { t, locale } = useTranslations();
  const searchParams = useSearchParams();
  const selectedCounty = searchParams.get("county") ?? undefined;
  const saved = isSaved(resource.id);
  const showRegionalBadge = isRegionalResource(resource);
  const coverageLabel = countyCoverageLabel(resource, selectedCounty, t);
  const showCoverageLabel =
    coverageLabel &&
    !(showRegionalBadge && coverageLabel === t("resources.coverageRegional"));

  useEffect(() => {
    if (authLoading) return;
    recordView(resource);
  }, [resource.id, authLoading, user?.id, recordView]);

  const fullAddress = [resource.address, resource.city, resource.state]
    .filter(Boolean)
    .join(", ");

  const handleSave = () => {
    if (!user) {
      window.location.href = signInHref;
      return;
    }
    toggleSave(resource.id);
  };

  const handleShare = () => {
    shareResource(resource.name, window.location.href);
  };

  return (
    <div className={cn("bg-background", pageSectionPadding)}>
      <div className="mx-auto max-w-4xl">
        <Link
          href={buildResourcesPageHref()}
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
              {resource.state && <StateBadge state={resource.state} />}
              <RegionalBadge resource={resource} />
              <StatewideBadge resource={resource} />
            </div>
            <div className="flex items-center gap-2">
              <SaveResourceButton
                saved={saved}
                onClick={handleSave}
                showLabel
                ariaLabel={
                  saved
                    ? t("resources.removeSaveAria", { name: resource.name })
                    : t("resources.saveAria", { name: resource.name })
                }
              />
              <button
                type="button"
                onClick={handleShare}
                className={cn(
                  resourceBadgeClass,
                  "cursor-pointer focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
                )}
              >
                <Share2 aria-hidden="true" />
                {t("common.share")}
              </button>
            </div>
          </div>
        </header>

        <div className="grid gap-6 lg:grid-cols-3">
          <div className="space-y-6 lg:col-span-2">
            <Card>
              <h1 className="mb-4 text-xl font-bold">{resource.name}</h1>
              {showCoverageLabel && (
                <p className="mb-3 text-sm font-medium text-primary">{coverageLabel}</p>
              )}
              <p className="text-base text-muted-foreground">{resource.description}</p>
            </Card>

            {resource.services.length > 0 && (
              <Card>
                <CardHeader>
                  <h2 className={sectionTitleClass}>{t("resources.servicesOffered")}</h2>
                </CardHeader>
                <ul className="space-y-2">
                  {resource.services.map((service) => (
                    <li
                      key={service}
                      className="flex items-center gap-2 text-base app-check-list-item before:content-['✓'] before:font-bold"
                    >
                      {service}
                    </li>
                  ))}
                </ul>
              </Card>
            )}

            {resource.eligibility && (
              <Card className="app-eligibility-card">
                <CardHeader>
                  <h2 className={sectionTitleClass}>{t("resources.eligibilityRequirements")}</h2>
                </CardHeader>
                <CardDescription>{resource.eligibility}</CardDescription>
              </Card>
            )}

            {resource.notes && (
              <Card>
                <CardHeader>
                  <h2 className={sectionTitleClass}>{t("resources.additionalInfo")}</h2>
                </CardHeader>
                <CardDescription>{resource.notes}</CardDescription>
              </Card>
            )}
          </div>

          <aside className="min-w-0 space-y-6">
            <Card>
              <CardHeader>
                <h2 className={sectionTitleClass}>{t("resources.contactInfo")}</h2>
              </CardHeader>
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
                  <p className="flex min-w-0 items-center gap-2">
                    <Globe className="h-5 w-5 shrink-0 text-primary" aria-hidden="true" />
                    <a
                      href={resource.website}
                      target="_blank"
                      rel="noopener noreferrer"
                      title={formatWebsiteDisplay(resource.website)}
                      className="min-w-0 truncate text-base text-primary hover:underline"
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

            {shouldShowCountiesServed(resource) ? (
              <Card>
                <CardHeader>
                  <h2 className={sectionTitleClass}>{t("resources.countiesServed")}</h2>
                </CardHeader>
                <ServedCountiesLinks resource={resource} />
              </Card>
            ) : null}

            {resource.tags.length > 0 && (
              <Card>
                <CardHeader>
                  <h2 className={sectionTitleClass}>{t("resources.tags")}</h2>
                </CardHeader>
                <p className="text-base leading-relaxed text-muted-foreground">
                  {resource.tags.map((tag, index) => (
                    <span key={tag}>
                      {index > 0 && ", "}
                      <Link
                        href={buildResourcesPageHref({ tag }, "results")}
                        className="text-primary hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring rounded"
                      >
                        {tag}
                      </Link>
                    </span>
                  ))}
                </p>
              </Card>
            )}

            <p className="text-center text-sm text-muted-foreground">
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
