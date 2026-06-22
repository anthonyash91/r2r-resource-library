export interface UserPreferences {
  state: string | null;
  county: string | null;
  priorityCategories: string[];
  completedAt: string | null;
  skipped: boolean;
}

export type UserPreferencesInput = {
  state: string;
  county: string;
  priorityCategories: string[];
  skipped?: boolean;
};
