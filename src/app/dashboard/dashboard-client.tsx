"use client";

import { useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { ArrowRight, Heart, Clock, Star, LayoutGrid, MapPin } from "lucide-react";
import { ResourceMasonry } from "@/components/resources/resource-masonry";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/lib/auth-context";
import { useSignInHref } from "@/hooks/use-sign-in-href";
import { useSaved, useSavedResources } from "@/lib/saved-context";
import type { Category, Resource } from "@/types";
import { useTranslations } from "@/i18n/locale-context";
import { EmailSavedResourcesButton } from "@/components/saved/email-saved-resources-button";
import {
  hasPersonalizedPreferences,
  needsOnboarding,
  type UserPreferences,
} from "@/lib/user-preferences";
import { buildResourcesPageHref } from "@/lib/resources-page";
import { pageSectionPadding, cn } from "@/lib/utils";
import { FacilityContactEmailSection } from "@/components/facility/facility-contact-email-section";
import { FirstWeekGuideCard } from "@/components/dashboard/first-week-guide-card";
import { PriorityCategoryBadge } from "@/components/resources/priority-category-badge";

interface DashboardClientProps {
  categories: Category[];
  recommended: Resource[];
  preferences: UserPreferences;
}

export function DashboardClient({
  categories,
  recommended,
  preferences,
}: DashboardClientProps) {
  const router = useRouter();
  const { user, loading, signingOut } = useAuth();
  const signInHref = useSignInHref();
  const { recentlyViewed } = useSaved();
  const savedResources = useSavedResources();
  const { t } = useTranslations();

  const personalized = hasPersonalizedPreferences(preferences);

  useEffect(() => {
    if (loading || !user) return;
    if (needsOnboarding(preferences)) {
      router.replace("/get-started");
    }
  }, [loading, user, preferences, router]);

  if (loading || signingOut) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center">
        <p className="text-lg text-muted-foreground">{t("dashboard.loading")}</p>
      </div>
    );
  }

  if (!user) {
    return (
      <div className={pageSectionPadding}>
        <div className="mx-auto max-w-lg">
          <h1 className="mb-4 text-3xl font-bold">{t("dashboard.signInRequired")}</h1>
          <p className="mb-8 text-lg text-muted-foreground">{t("dashboard.signInRequiredDesc")}</p>
          <div className="flex flex-col gap-3 sm:flex-row sm:justify-center">
            <Link href={signInHref}>
              <Button size="lg">{t("auth.signIn")}</Button>
            </Link>
            <Link href="/signup">
              <Button variant="outline" size="lg">{t("nav.createAccount")}</Button>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const firstName = user.full_name?.split(" ")[0];
  const countyBrowseHref =
    preferences.state && preferences.county
      ? buildResourcesPageHref(
          { state: preferences.state, county: preferences.county },
          "results"
        )
      : buildResourcesPageHref();

  return (
    <div className={pageSectionPadding}>
      <div className="mx-auto max-w-7xl">
        <header className="mb-10">
          <h1 className="mb-2 text-3xl font-bold sm:text-4xl">
            {firstName ? t("dashboard.welcomeNamed", { name: firstName }) : t("dashboard.welcome")}
          </h1>
          <p className="text-lg text-muted-foreground">{t("dashboard.description")}</p>

          {personalized && preferences.state && preferences.county ? (
            <div className="mt-6 flex flex-col gap-3 rounded-xl border border-border bg-card p-4 sm:flex-row sm:items-center sm:justify-between">
              <div className="flex items-start gap-3">
                <MapPin className="mt-0.5 h-5 w-5 shrink-0 text-primary" aria-hidden="true" />
                <div>
                  <p className="font-semibold">
                    {t("dashboard.resourcesFor", {
                      county: preferences.county,
                      state: preferences.state,
                    })}
                  </p>
                  {preferences.priorityCategories.length > 0 ? (
                    <div className="mt-3">
                      <p className="mb-2 text-sm text-muted-foreground">
                        {t("dashboard.yourPriorities")}
                      </p>
                      <ul
                        className="flex flex-wrap gap-2"
                        aria-label={t("dashboard.yourPriorities")}
                      >
                        {preferences.priorityCategories.map((slug) => (
                          <li key={slug}>
                            <PriorityCategoryBadge slug={slug} />
                          </li>
                        ))}
                      </ul>
                    </div>
                  ) : null}
                  <Link
                    href="/get-started?edit=1"
                    className="mt-3 inline-block text-sm font-semibold text-primary hover:underline"
                  >
                    {t("dashboard.changeLocation")}
                  </Link>
                </div>
              </div>
              <Link href={countyBrowseHref}>
                <Button variant="outline" size="sm">
                  {t("dashboard.browseMyCounty")}
                </Button>
              </Link>
            </div>
          ) : (
            <div className="mt-6 rounded-xl border border-border bg-card p-4">
              <p className="text-base text-muted-foreground">{t("dashboard.completeOnboardingReminder")}</p>
              <Link href="/get-started" className="mt-3 inline-block">
                <Button size="sm">{t("dashboard.completeOnboardingCta")}</Button>
              </Link>
            </div>
          )}
        </header>

        <FirstWeekGuideCard />

        <FacilityContactEmailSection />

        <div className="mb-10 grid gap-4 sm:grid-cols-3">
          <Card className="flex items-center gap-4">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary">
              <Heart className="h-6 w-6" aria-hidden="true" />
            </div>
            <div>
              <p className="text-2xl font-bold">{savedResources.length}</p>
              <p className="text-sm text-muted-foreground">{t("dashboard.savedCount")}</p>
            </div>
          </Card>
          <Card className="flex items-center gap-4">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary">
              <Clock className="h-6 w-6" aria-hidden="true" />
            </div>
            <div>
              <p className="text-2xl font-bold">{recentlyViewed.length}</p>
              <p className="text-sm text-muted-foreground">{t("dashboard.viewedCount")}</p>
            </div>
          </Card>
          <Card className="flex items-center gap-4">
            <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/10 text-primary">
              <LayoutGrid className="h-6 w-6" aria-hidden="true" />
            </div>
            <div>
              <p className="text-2xl font-bold">
                {personalized ? preferences.priorityCategories.length : categories.length}
              </p>
              <p className="text-sm text-muted-foreground">
                {personalized ? t("dashboard.priorityAreasCount") : t("dashboard.browseByCategory")}
              </p>
            </div>
          </Card>
        </div>

        {savedResources.length > 0 && (
          <section className="mb-10" aria-labelledby="saved-heading">
            <div className="mb-6 flex flex-wrap items-center justify-between gap-4">
              <h2 id="saved-heading" className="text-2xl font-bold">
                {t("dashboard.savedResources")}
              </h2>
              <div className="flex flex-wrap items-center gap-4">
                <EmailSavedResourcesButton resourceCount={savedResources.length} size="sm" />
                <Link href="/saved" className="text-base font-semibold text-primary hover:underline">
                  {t("home.viewAllResources")}
                </Link>
              </div>
            </div>
            <ResourceMasonry resources={savedResources.slice(0, 3)} contained />
          </section>
        )}

        {recommended.length > 0 ? (
          <section
            className={cn(recentlyViewed.length > 0 && "mb-10")}
            aria-labelledby="recommended-heading"
          >
            <div className="mb-6 flex flex-wrap items-center gap-2">
              <Star className="h-6 w-6 text-warning" aria-hidden="true" />
              <h2 id="recommended-heading" className="text-2xl font-bold">
                {personalized && preferences.county
                  ? t("dashboard.recommendedPersonalized", { county: preferences.county })
                  : t("dashboard.recommended")}
              </h2>
            </div>
            <ResourceMasonry resources={recommended} layout="masonry" contained />
            {preferences.state && preferences.county ? (
              <div className="mt-10 flex justify-center">
                <Link href={countyBrowseHref}>
                  <Button size="lg" variant="outline" className="gap-2">
                    {t("dashboard.browseMyCounty")}
                    <ArrowRight className="h-5 w-5" aria-hidden="true" />
                  </Button>
                </Link>
              </div>
            ) : null}
          </section>
        ) : null}

        {recentlyViewed.length > 0 && (
          <section aria-labelledby="recent-heading">
            <h2 id="recent-heading" className="mb-6 text-2xl font-bold">
              {t("dashboard.recentlyViewed")}
            </h2>
            <ResourceMasonry resources={recentlyViewed.slice(0, 3)} contained />
          </section>
        )}
      </div>
    </div>
  );
}
