import Link from "next/link";
import { MapPin } from "lucide-react";
import { getServerTranslator } from "@/i18n/server";
import { cn } from "@/lib/utils";
import { PriorityCategoryBadge } from "@/components/resources/priority-category-badge";

interface RecommendedPreferencesSummaryProps {
  state: string | null;
  county: string | null;
  priorityCategories: string[];
  variant?: "home" | "resources";
}

export async function RecommendedPreferencesSummary({
  state,
  county,
  priorityCategories,
  variant = "home",
}: RecommendedPreferencesSummaryProps) {
  const { t } = await getServerTranslator();

  if (!state || !county) return null;

  const content = (
    <>
      <div className="flex min-w-0 items-start gap-3">
        <MapPin className="mt-0.5 h-5 w-5 shrink-0 text-primary" aria-hidden="true" />
        <div className="min-w-0">
          <p className="font-semibold text-foreground">
            {t("dashboard.resourcesFor", { county, state })}
          </p>
          {priorityCategories.length > 0 ? (
            <div className="mt-2">
              <p className="mb-2 text-sm text-muted-foreground">
                {t("dashboard.yourPriorities")}
              </p>
              <ul
                className="flex flex-wrap gap-2"
                aria-label={t("dashboard.yourPriorities")}
              >
                {priorityCategories.map((slug) => (
                  <li key={slug}>
                    <PriorityCategoryBadge slug={slug} />
                  </li>
                ))}
              </ul>
            </div>
          ) : null}
        </div>
      </div>
      <Link
        href="/get-started?edit=1"
        className="shrink-0 text-sm font-semibold text-primary hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
      >
        {t("dashboard.changeLocation")}
      </Link>
    </>
  );

  if (variant === "resources") {
    return (
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        {content}
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-3xl rounded-xl border border-border bg-card p-4 sm:p-5">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
        {content}
      </div>
    </div>
  );
}
