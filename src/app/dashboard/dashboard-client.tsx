"use client";

import Link from "next/link";
import { Heart, Clock, Star, LayoutGrid } from "lucide-react";
import { ResourceMasonry } from "@/components/resources/resource-masonry";
import { CategoryPills } from "@/components/resources/category-pills";
import { Card, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/lib/auth-context";
import { useSaved, useSavedResources } from "@/lib/saved-context";
import type { Category, Resource } from "@/types";
import { useTranslations } from "@/i18n/locale-context";

interface DashboardClientProps {
  categories: Category[];
  recommended: Resource[];
}

export function DashboardClient({ categories, recommended }: DashboardClientProps) {
  const { user, loading } = useAuth();
  const { recentlyViewed } = useSaved();
  const savedResources = useSavedResources();
  const { t } = useTranslations();

  if (loading) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center">
        <p className="text-lg text-muted-foreground">{t("dashboard.loading")}</p>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="px-4 py-16 text-center sm:px-6 lg:px-8">
        <div className="mx-auto max-w-lg">
          <h1 className="mb-4 text-3xl font-bold">{t("dashboard.signInRequired")}</h1>
          <p className="mb-8 text-lg text-muted-foreground">{t("dashboard.signInRequiredDesc")}</p>
          <div className="flex flex-col gap-3 sm:flex-row sm:justify-center">
            <Link href="/login">
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

  return (
    <div className="px-4 py-10 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        <header className="mb-10">
          <h1 className="mb-2 text-3xl font-bold sm:text-4xl">
            {firstName ? t("dashboard.welcomeNamed", { name: firstName }) : t("dashboard.welcome")}
          </h1>
          <p className="text-lg text-muted-foreground">{t("dashboard.description")}</p>
        </header>

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
              <p className="text-2xl font-bold">{categories.length}</p>
              <p className="text-sm text-muted-foreground">{t("dashboard.recommendedCount")}</p>
            </div>
          </Card>
        </div>

        {savedResources.length > 0 && (
          <section className="mb-12" aria-labelledby="saved-heading">
            <div className="mb-6 flex items-center justify-between">
              <h2 id="saved-heading" className="text-2xl font-bold">
                {t("dashboard.savedResources")}
              </h2>
              <Link href="/saved" className="text-base font-semibold text-primary hover:underline">
                {t("home.viewAllResources")}
              </Link>
            </div>
            <ResourceMasonry resources={savedResources.slice(0, 3)} />
          </section>
        )}

        {recentlyViewed.length > 0 && (
          <section className="mb-12" aria-labelledby="recent-heading">
            <h2 id="recent-heading" className="mb-6 text-2xl font-bold">
              {t("dashboard.recentlyViewed")}
            </h2>
            <ResourceMasonry resources={recentlyViewed.slice(0, 3)} />
          </section>
        )}

        <section className="mb-12" aria-labelledby="recommended-heading">
          <div className="mb-6 flex items-center gap-2">
            <Star className="h-6 w-6 text-warning" aria-hidden="true" />
            <h2 id="recommended-heading" className="text-2xl font-bold">
              {t("dashboard.recommended")}
            </h2>
          </div>
          <ResourceMasonry resources={recommended} />
        </section>

        <section aria-labelledby="categories-dash-heading">
          <CardTitle className="mb-3 text-lg" id="categories-dash-heading">
            {t("dashboard.browseByCategory")}
          </CardTitle>
          <CategoryPills categories={categories} compact />
        </section>
      </div>
    </div>
  );
}
