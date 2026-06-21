import type { AnalyticsSummary } from "@/types";

const DAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

export function emptyRecentActivity() {
  return DAY_LABELS.map((date) => ({ date, views: 0, saves: 0 }));
}

export function emptyAnalyticsSummary(): AnalyticsSummary {
  return {
    totalResources: 0,
    activeResources: 0,
    featuredResources: 0,
    totalCategories: 0,
    totalViews: 0,
    totalSaves: 0,
    resourcesByState: [],
    resourcesByCategory: [],
    mostViewed: [],
    mostSaved: [],
    recentActivity: emptyRecentActivity(),
  };
}
