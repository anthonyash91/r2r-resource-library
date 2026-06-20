import { getAnalytics } from "@/lib/data";
import { Card, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import Link from "next/link";
import { getServerTranslator } from "@/i18n/server";

export default async function AdminDashboardPage() {
  const { t } = await getServerTranslator();
  const analytics = await getAnalytics();

  return (
    <div>
      <header className="mb-8">
        <h1 className="mb-2 text-3xl font-bold">{t("admin.analyticsTitle")}</h1>
        <p className="text-lg text-muted-foreground">{t("admin.analyticsSubtitle")}</p>
      </header>

      <div className="mb-8 grid gap-4 sm:grid-cols-3">
        <Card>
          <CardTitle className="text-sm font-medium text-muted-foreground">
            {t("admin.totalResources")}
          </CardTitle>
          <p className="mt-2 text-4xl font-bold">{analytics.totalResources}</p>
        </Card>
        <Card>
          <CardTitle className="text-sm font-medium text-muted-foreground">
            {t("admin.totalUsers")}
          </CardTitle>
          <p className="mt-2 text-4xl font-bold">{analytics.totalUsers}</p>
        </Card>
        <Card>
          <CardTitle className="text-sm font-medium text-muted-foreground">
            {t("admin.totalSaves")}
          </CardTitle>
          <p className="mt-2 text-4xl font-bold">{analytics.totalSaves}</p>
        </Card>
      </div>

      <div className="mb-8 grid gap-6 lg:grid-cols-2">
        <Card>
          <CardTitle className="mb-4">{t("admin.resourcesByState")}</CardTitle>
          <ul className="space-y-2">
            {analytics.resourcesByState.map(({ state, count }) => (
              <li key={state} className="flex items-center justify-between text-base">
                <span>{state}</span>
                <Badge variant="primary">{count}</Badge>
              </li>
            ))}
          </ul>
        </Card>

        <Card>
          <CardTitle className="mb-4">{t("admin.resourcesByCategory")}</CardTitle>
          <ul className="space-y-2">
            {analytics.resourcesByCategory.map(({ category, count }) => (
              <li key={category} className="flex items-center justify-between text-base">
                <span>{category}</span>
                <Badge variant="secondary">{count}</Badge>
              </li>
            ))}
          </ul>
        </Card>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardTitle className="mb-4">{t("admin.mostViewed")}</CardTitle>
          <ul className="space-y-3">
            {analytics.mostViewed.map((r) => (
              <li key={r.id}>
                <Link
                  href={`/resources/${r.id}`}
                  className="flex items-center justify-between text-base hover:text-primary"
                >
                  <span className="font-medium">{r.name}</span>
                  <Badge>
                    {r.view_count} {t("admin.views")}
                  </Badge>
                </Link>
              </li>
            ))}
          </ul>
        </Card>

        <Card>
          <CardTitle className="mb-4">{t("admin.mostSaved")}</CardTitle>
          <ul className="space-y-3">
            {analytics.mostSaved.map((r) => (
              <li key={r.id}>
                <Link
                  href={`/resources/${r.id}`}
                  className="flex items-center justify-between text-base hover:text-primary"
                >
                  <span className="font-medium">{r.name}</span>
                  <Badge variant="success">
                    {r.save_count} {t("admin.saves")}
                  </Badge>
                </Link>
              </li>
            ))}
          </ul>
        </Card>
      </div>

      <Card className="mt-8">
        <CardTitle className="mb-4">{t("admin.weeklyActivity")}</CardTitle>
        <div className="flex items-end gap-2 h-40">
          {analytics.recentActivity.map(({ date, views, saves }) => (
            <div key={date} className="flex flex-1 flex-col items-center gap-1">
              <div className="flex w-full gap-1 items-end justify-center h-32">
                <div
                  className="w-1/2 rounded-t bg-primary/70"
                  style={{ height: `${Math.min(views * 1.5, 100)}%` }}
                  title={`${views} ${t("admin.views")}`}
                />
                <div
                  className="w-1/2 rounded-t bg-accent/70"
                  style={{ height: `${Math.min(saves * 4, 100)}%` }}
                  title={`${saves} ${t("admin.saves")}`}
                />
              </div>
              <span className="text-xs text-muted-foreground">{date}</span>
            </div>
          ))}
        </div>
        <div className="mt-4 flex gap-4 text-sm text-muted-foreground">
          <span className="flex items-center gap-2">
            <span className="h-3 w-3 rounded bg-primary/70" /> {t("admin.views")}
          </span>
          <span className="flex items-center gap-2">
            <span className="h-3 w-3 rounded bg-accent/70" /> {t("admin.saves")}
          </span>
        </div>
      </Card>
    </div>
  );
}
