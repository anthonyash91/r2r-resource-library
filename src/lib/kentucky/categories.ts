import type { Category } from "@/types";

const now = new Date().toISOString();

/** Kentucky reentry directory categories (Reentry to Recovery) */
export const KENTUCKY_CATEGORIES: Category[] = [
  { id: "cat-ky-state-agency", name: "State Agency", slug: "state-agency", description: "Kentucky state government reentry resources and services", icon: "shield", sort_order: 1, is_active: true, created_at: now, updated_at: now },
  { id: "cat-ky-housing", name: "Housing", slug: "housing", description: "Transitional housing, recovery housing, and shelter for people leaving incarceration", icon: "home", sort_order: 2, is_active: true, created_at: now, updated_at: now },
  { id: "cat-ky-employment", name: "Employment", slug: "employment", description: "Job training, placement, and fair-chance employment for justice-involved Kentuckians", icon: "briefcase", sort_order: 3, is_active: true, created_at: now, updated_at: now },
  { id: "cat-ky-healthcare", name: "Healthcare", slug: "healthcare", description: "Medical care, mental health, and recovery navigation", icon: "heart-pulse", sort_order: 4, is_active: true, created_at: now, updated_at: now },
  { id: "cat-ky-substance-use", name: "Substance Use Treatment", slug: "substance-use-treatment", description: "Addiction treatment and recovery housing for justice-involved individuals", icon: "shield", sort_order: 5, is_active: true, created_at: now, updated_at: now },
  { id: "cat-ky-legal-aid", name: "Legal Aid", slug: "legal-aid", description: "Expungement, civil legal help, and record relief", icon: "scale", sort_order: 6, is_active: true, created_at: now, updated_at: now },
  { id: "cat-ky-food-nutrition", name: "Food & Nutrition", slug: "food-nutrition", description: "Food assistance and nutrition resources", icon: "utensils", sort_order: 7, is_active: true, created_at: now, updated_at: now },
  { id: "cat-ky-id-docs", name: "ID & Documentation", slug: "id-documentation", description: "Birth certificates, IDs, and vital records assistance", icon: "id-card", sort_order: 8, is_active: true, created_at: now, updated_at: now },
  { id: "cat-ky-financial", name: "Financial Assistance", slug: "financial-assistance", description: "Benefits, emergency funds, and financial coaching", icon: "dollar-sign", sort_order: 9, is_active: true, created_at: now, updated_at: now },
  { id: "cat-ky-transportation", name: "Transportation", slug: "transportation", description: "Transit passes and transportation to appointments and work", icon: "bus", sort_order: 10, is_active: true, created_at: now, updated_at: now },
  { id: "cat-ky-family", name: "Family & Children", slug: "family-children", description: "Family reunification and support for loved ones of incarcerated people", icon: "users", sort_order: 11, is_active: true, created_at: now, updated_at: now },
  { id: "cat-ky-peer-support", name: "Peer Support", slug: "peer-support", description: "Peer mentors and recovery community support", icon: "handshake", sort_order: 12, is_active: true, created_at: now, updated_at: now },
  { id: "cat-ky-education", name: "Education", slug: "education", description: "GED, job training, and credential resources during reentry", icon: "graduation-cap", sort_order: 13, is_active: true, created_at: now, updated_at: now },
  { id: "cat-ky-veterans", name: "Veterans", slug: "veterans", description: "Reentry services for justice-involved veterans", icon: "medal", sort_order: 14, is_active: true, created_at: now, updated_at: now },
  { id: "cat-ky-basic-needs", name: "Basic Needs", slug: "basic-needs", description: "Clothing, hygiene, and essential items at release", icon: "handshake", sort_order: 15, is_active: true, created_at: now, updated_at: now },
  { id: "cat-ky-probation-parole", name: "Probation & Parole", slug: "probation-parole", description: "Community supervision and DOC contracted reentry centers", icon: "scale", sort_order: 16, is_active: true, created_at: now, updated_at: now },
  { id: "cat-ky-reentry-orgs", name: "Reentry Organizations", slug: "reentry-organizations", description: "Nonprofit reentry coalitions and community-based reentry resources", icon: "handshake", sort_order: 17, is_active: true, created_at: now, updated_at: now },
];

export const KENTUCKY_CATEGORY_BY_ID = Object.fromEntries(
  KENTUCKY_CATEGORIES.map((category) => [category.id, category])
) as Record<string, Category>;
