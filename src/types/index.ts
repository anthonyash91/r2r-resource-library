export type UserRole = "user" | "case_manager" | "admin";
export type ResourceStatus = "active" | "inactive" | "archived";
export type ResourceCoverage = "single" | "multi" | "statewide";

export type IntakeSignal =
  | "accepts_criminal_record"
  | "referral_required"
  | "walk_in_ok";
export type CmsPageStatus = "draft" | "published" | "archived";
export type AnnouncementStatus = "draft" | "published" | "archived";

export interface Profile {
  id: string;
  email: string;
  full_name: string | null;
  role: UserRole;
  is_active: boolean;
  phone: string | null;
  state: string | null;
  county: string | null;
  city: string | null;
  facility_id?: string | null;
  signup_context?: "standard" | "facility" | null;
  contact_email?: string | null;
  priority_categories?: string[];
  onboarding_completed_at?: string | null;
  created_at: string;
  updated_at: string;
  saved_pdf_emails_sent?: number;
}

/** Profile row for admin user management (includes joined facility name). */
export interface AdminUserListItem extends Profile {
  facility_name: string | null;
}

export interface Category {
  id: string;
  name: string;
  slug: string;
  description: string | null;
  icon: string | null;
  sort_order: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Resource {
  id: string;
  name: string;
  description: string;
  description_es?: string | null;
  category_id: string;
  category?: Category;
  state: string | null;
  county: string | null;
  city: string | null;
  address: string | null;
  phone: string | null;
  website: string | null;
  email: string | null;
  hours: string | null;
  eligibility: string | null;
  eligibility_es?: string | null;
  notes?: string | null;
  notes_es?: string | null;
  served_counties?: string[];
  coverage?: ResourceCoverage;
  services: string[];
  tags: string[];
  intake_signals?: IntakeSignal[];
  is_featured: boolean;
  status: ResourceStatus;
  view_count: number;
  save_count: number;
  created_at: string;
  updated_at: string;
  created_by: string | null;
}

export interface SavedResource {
  id: string;
  user_id: string;
  resource_id: string;
  notes: string | null;
  created_at: string;
  resource?: Resource;
}

export interface ResourceView {
  id: string;
  user_id: string | null;
  resource_id: string;
  session_id: string | null;
  viewed_at: string;
  resource?: Resource;
}

export interface CmsPage {
  id: string;
  title: string;
  slug: string;
  content: string;
  meta_description: string | null;
  status: CmsPageStatus;
  sort_order: number;
  created_at: string;
  updated_at: string;
  published_at: string | null;
}

export interface Announcement {
  id: string;
  title: string;
  content: string;
  status: AnnouncementStatus;
  is_pinned: boolean;
  starts_at: string | null;
  ends_at: string | null;
  created_at: string;
  updated_at: string;
}

export interface Faq {
  id: string;
  question: string;
  answer: string;
  category: string | null;
  sort_order: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface HomepageContent {
  id: string;
  key: string;
  value: string;
  updated_at: string;
}

export interface ResourceFilters {
  query?: string;
  state?: string;
  county?: string;
  city?: string;
  category?: string;
  service?: string;
  tag?: string;
  coverage?: ResourceCoverage;
  eligibility?: string;
  intake?: IntakeSignal[];
  featured?: boolean;
  recentlyAdded?: boolean;
  status?: ResourceStatus;
}

export interface AnalyticsSummary {
  totalResources: number;
  activeResources: number;
  featuredResources: number;
  totalCategories: number;
  totalViews: number;
  totalSaves: number;
  resourcesByState: { state: string; count: number }[];
  resourcesByCategory: { category: string; count: number }[];
  mostViewed: Resource[];
  mostSaved: Resource[];
  recentActivity: { date: string; views: number; saves: number }[];
}
