import Link from "next/link";
import { Phone, AlertTriangle } from "lucide-react";
import { getServerTranslator } from "@/i18n/server";
import { cn } from "@/lib/utils";

export async function PathwayCrisisCallout() {
  const { t } = await getServerTranslator();

  return (
    <div
      className={cn(
        "rounded-xl border-2 border-destructive/30 bg-destructive/5 p-5",
        "flex flex-col gap-4 sm:flex-row sm:items-start sm:gap-5"
      )}
      role="note"
    >
      <AlertTriangle
        className="h-6 w-6 shrink-0 text-destructive"
        aria-hidden="true"
      />
      <div className="min-w-0 flex-1 space-y-3">
        <p className="text-base font-semibold text-foreground">
          {t("pathways.crisisTitle")}
        </p>
        <p className="text-base leading-relaxed text-muted-foreground">
          {t("pathways.crisisBody")}
        </p>
        <div className="flex flex-wrap gap-4 text-base font-semibold">
          <a
            href="tel:988"
            className="inline-flex items-center gap-2 text-primary hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
            aria-label={t("crisisBar.call988Aria")}
          >
            <Phone className="h-4 w-4 shrink-0" aria-hidden="true" />
            {t("crisisBar.call988")}
          </a>
          <a
            href="sms:741741?body=HOME"
            className="inline-flex items-center gap-2 text-primary hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
            aria-label={t("crisisBar.textLineAria")}
          >
            {t("crisisBar.textLine")}
          </a>
        </div>
      </div>
    </div>
  );
}
