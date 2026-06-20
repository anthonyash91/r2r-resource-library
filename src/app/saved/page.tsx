"use client";

import Link from "next/link";
import { Heart } from "lucide-react";
import { ResourceMasonry } from "@/components/resources/resource-masonry";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/lib/auth-context";
import { useSavedResources } from "@/lib/saved-context";
import { useTranslations } from "@/i18n/locale-context";

export default function SavedPage() {
  const { user, loading } = useAuth();
  const savedResources = useSavedResources();
  const { t } = useTranslations();

  if (loading) {
    return (
      <div className="flex min-h-[40vh] items-center justify-center">
        <p className="text-lg text-muted-foreground">{t("common.loading")}</p>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="px-4 py-16 text-center sm:px-6 lg:px-8">
        <div className="mx-auto max-w-lg">
          <Heart className="mx-auto mb-4 h-16 w-16 text-primary" aria-hidden="true" />
          <h1 className="mb-4 text-3xl font-bold">{t("saved.signInTitle")}</h1>
          <p className="mb-8 text-lg text-muted-foreground">{t("saved.signInDesc")}</p>
          <Link href="/login">
            <Button size="lg">{t("auth.signIn")}</Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="px-4 py-10 sm:px-6 lg:px-8">
      <div className="mx-auto max-w-7xl">
        <header className="mb-8">
          <h1 className="mb-2 text-3xl font-bold sm:text-4xl">{t("saved.title")}</h1>
          <p className="text-lg text-muted-foreground">{t("saved.subtitle")}</p>
        </header>

        {savedResources.length === 0 ? (
          <div className="rounded-2xl border border-border bg-card p-12 text-center">
            <Heart className="mx-auto mb-4 h-12 w-12 text-muted-foreground" aria-hidden="true" />
            <h2 className="mb-2 text-xl font-bold">{t("saved.emptyTitle")}</h2>
            <p className="mb-6 text-base text-muted-foreground">{t("saved.emptyDesc")}</p>
            <Link href="/resources">
              <Button size="lg">{t("saved.browseResources")}</Button>
            </Link>
          </div>
        ) : (
          <ResourceMasonry resources={savedResources} />
        )}
      </div>
    </div>
  );
}
