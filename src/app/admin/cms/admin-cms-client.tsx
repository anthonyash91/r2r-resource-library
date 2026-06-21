"use client";

import Link from "next/link";
import { ExternalLink, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { SITE_PAGE_DEFINITIONS, type SitePageKind } from "@/lib/site-pages";
import { useTranslations } from "@/i18n/locale-context";

function kindBadgeVariant(kind: SitePageKind): "primary" | "success" | "warning" | "default" {
  if (kind === "template") return "primary";
  if (kind === "dedicated") return "success";
  return "default";
}

function kindLabelKey(kind: SitePageKind): string {
  if (kind === "template") return "admin.pages.badgeTemplate";
  return "admin.pages.badgeDedicated";
}

export function AdminCmsClient() {
  const { t } = useTranslations();

  return (
    <div>
      <header className="mb-8">
        <h1 className="mb-2 text-3xl font-bold">{t("admin.sitePagesTitle")}</h1>
        <p className="text-lg text-muted-foreground">{t("admin.sitePagesDesc")}</p>
      </header>

      <div className="space-y-3">
        {SITE_PAGE_DEFINITIONS.map((page) => (
          <Card key={page.slug} className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
            <div className="min-w-0 flex-1">
              <div className="mb-2 flex flex-wrap items-center gap-2">
                <h2 className="text-lg font-bold">{t(page.labelKey)}</h2>
                <Badge variant={kindBadgeVariant(page.kind)}>{t(kindLabelKey(page.kind))}</Badge>
              </div>
              <p className="text-sm text-muted-foreground">{page.publicPath}</p>
              {page.noteKey ? (
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">{t(page.noteKey)}</p>
              ) : null}
            </div>
            <div className="flex shrink-0 flex-wrap gap-2">
              <Link href={page.publicPath}>
                <Button variant="ghost" size="sm">
                  <ExternalLink className="h-4 w-4" aria-hidden="true" />
                  {t("admin.viewPage")}
                </Button>
              </Link>
              {page.editHref ? (
                <Link href={page.editHref}>
                  <Button variant="outline" size="sm">
                    <ArrowRight className="h-4 w-4" aria-hidden="true" />
                    {t(page.editLabelKey ?? "common.edit")}
                  </Button>
                </Link>
              ) : null}
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
}
