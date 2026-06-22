import type { AnalyticsSummary } from "@/types";
import { emptyRecentActivity } from "@/lib/analytics-recent-activity";

export { emptyRecentActivity } from "@/lib/analytics-recent-activity";

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
