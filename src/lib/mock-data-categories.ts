import type { Category } from "@/types";

const now = new Date().toISOString();

export const MOCK_CATEGORIES: Category[] = [
  { id: "cat-housing", name: "Housing", slug: "housing", description: "Shelter, transitional housing, and rental assistance", icon: "home", sort_order: 1, is_active: true, created_at: now, updated_at: now },
  { id: "cat-employment", name: "Employment", slug: "employment", description: "Job training, placement, and career services", icon: "briefcase", sort_order: 2, is_active: true, created_at: now, updated_at: now },
  { id: "cat-food", name: "Food Assistance", slug: "food-assistance", description: "Food banks, SNAP enrollment, and meal programs", icon: "utensils", sort_order: 3, is_active: true, created_at: now, updated_at: now },
  { id: "cat-healthcare", name: "Healthcare", slug: "healthcare", description: "Medical care, clinics, and health insurance", icon: "heart-pulse", sort_order: 4, is_active: true, created_at: now, updated_at: now },
  { id: "cat-mental-health", name: "Mental Health", slug: "mental-health", description: "Counseling, therapy, and crisis support", icon: "brain", sort_order: 5, is_active: true, created_at: now, updated_at: now },
  { id: "cat-recovery", name: "Substance Abuse Recovery", slug: "substance-abuse-recovery", description: "Treatment, support groups, and sober living", icon: "shield", sort_order: 6, is_active: true, created_at: now, updated_at: now },
  { id: "cat-transportation", name: "Transportation", slug: "transportation", description: "Bus passes, rides, and vehicle assistance", icon: "bus", sort_order: 7, is_active: true, created_at: now, updated_at: now },
  { id: "cat-education", name: "Education", slug: "education", description: "GED, college, vocational training", icon: "graduation-cap", sort_order: 8, is_active: true, created_at: now, updated_at: now },
  { id: "cat-financial", name: "Financial Assistance", slug: "financial-assistance", description: "Benefits, emergency funds, and budgeting help", icon: "dollar-sign", sort_order: 9, is_active: true, created_at: now, updated_at: now },
  { id: "cat-legal", name: "Legal Aid", slug: "legal-aid", description: "Free legal help and expungement services", icon: "scale", sort_order: 10, is_active: true, created_at: now, updated_at: now },
  { id: "cat-id", name: "Identification Documents", slug: "identification-documents", description: "ID cards, birth certificates, and Social Security", icon: "id-card", sort_order: 11, is_active: true, created_at: now, updated_at: now },
  { id: "cat-family", name: "Family Services", slug: "family-services", description: "Reunification, parenting, and child support", icon: "users", sort_order: 12, is_active: true, created_at: now, updated_at: now },
  { id: "cat-veterans", name: "Veterans Services", slug: "veterans-services", description: "VA benefits and veteran-specific programs", icon: "medal", sort_order: 13, is_active: true, created_at: now, updated_at: now },
  { id: "cat-disability", name: "Disability Services", slug: "disability-services", description: "Accessibility support and disability benefits", icon: "accessibility", sort_order: 14, is_active: true, created_at: now, updated_at: now },
  { id: "cat-community", name: "Community Support Programs", slug: "community-support-programs", description: "Peer support, mentoring, and community centers", icon: "handshake", sort_order: 15, is_active: true, created_at: now, updated_at: now },
  { id: "cat-emergency", name: "Emergency Assistance", slug: "emergency-assistance", description: "Crisis help, hotlines, and immediate support", icon: "phone", sort_order: 16, is_active: true, created_at: now, updated_at: now },
];
