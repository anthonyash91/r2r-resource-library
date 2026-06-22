/** Eastern Time — primary audience for this directory */
const ACTIVITY_TIMEZONE = "America/New_York";

function formatDateKey(date: Date): string {
  return new Intl.DateTimeFormat("en-CA", { timeZone: ACTIVITY_TIMEZONE }).format(date);
}

function formatDayLabel(date: Date): string {
  const weekday = new Intl.DateTimeFormat("en-US", {
    timeZone: ACTIVITY_TIMEZONE,
    weekday: "short",
  }).format(date);
  return weekday.slice(0, 3);
}

export function buildRecentActivityBuckets(): { dateKey: string; date: string }[] {
  const buckets: { dateKey: string; date: string }[] = [];
  const now = new Date();

  for (let offset = 6; offset >= 0; offset--) {
    const day = new Date(now.getTime() - offset * 24 * 60 * 60 * 1000);
    buckets.push({
      dateKey: formatDateKey(day),
      date: formatDayLabel(day),
    });
  }

  return buckets;
}

export function activityDateKey(iso: string): string {
  return formatDateKey(new Date(iso));
}

export function recentActivitySinceIso(): string {
  const since = new Date();
  since.setTime(since.getTime() - 7 * 24 * 60 * 60 * 1000);
  return since.toISOString();
}

export function aggregateRecentActivity(
  views: { viewed_at: string }[],
  saves: { created_at: string }[]
): { date: string; views: number; saves: number }[] {
  const buckets = buildRecentActivityBuckets();
  const viewCounts = new Map(buckets.map((bucket) => [bucket.dateKey, 0]));
  const saveCounts = new Map(buckets.map((bucket) => [bucket.dateKey, 0]));

  for (const row of views) {
    const key = activityDateKey(row.viewed_at);
    if (viewCounts.has(key)) {
      viewCounts.set(key, (viewCounts.get(key) ?? 0) + 1);
    }
  }

  for (const row of saves) {
    const key = activityDateKey(row.created_at);
    if (saveCounts.has(key)) {
      saveCounts.set(key, (saveCounts.get(key) ?? 0) + 1);
    }
  }

  return buckets.map((bucket) => ({
    date: bucket.date,
    views: viewCounts.get(bucket.dateKey) ?? 0,
    saves: saveCounts.get(bucket.dateKey) ?? 0,
  }));
}

export function emptyRecentActivity() {
  return buildRecentActivityBuckets().map((bucket) => ({
    date: bucket.date,
    views: 0,
    saves: 0,
  }));
}
