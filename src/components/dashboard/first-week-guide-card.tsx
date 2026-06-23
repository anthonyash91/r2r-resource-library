import Link from "next/link";
import { ArrowRight, ListOrdered } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useTranslations } from "@/i18n/locale-context";

export function FirstWeekGuideCard() {
  const { t } = useTranslations();

  return (
    <Card className="mb-10 border-2 border-primary/25 bg-primary/5 p-5 sm:p-6">
      <div className="flex flex-col gap-5 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-start gap-4">
          <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-primary text-primary-foreground">
            <ListOrdered className="h-6 w-6" aria-hidden="true" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-foreground">
              {t("pathways.dashboardCardTitle")}
            </h2>
            <p className="mt-1 text-base leading-relaxed text-muted-foreground">
              {t("pathways.dashboardCardDesc")}
            </p>
          </div>
        </div>
        <Link href="/pathways/first-week" className="shrink-0">
          <Button size="lg" className="w-full gap-2 sm:w-auto">
            {t("pathways.dashboardCardCta")}
            <ArrowRight className="h-5 w-5" aria-hidden="true" />
          </Button>
        </Link>
      </div>
    </Card>
  );
}
