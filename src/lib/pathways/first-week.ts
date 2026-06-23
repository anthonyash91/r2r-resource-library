import type { PathwayDef } from "./types";

/** Fixed first-week checklist for people leaving custody — ordered for clarity under stress. */
export const FIRST_WEEK_PATHWAY: PathwayDef = {
  slug: "first-week",
  stepIds: [
    {
      id: "crisis-support",
      categorySlugs: ["healthcare", "mental-health"],
      tagSlugs: ["crisis", "988", "hotline", "emergency", "suicide"],
      includeStatewide: true,
      preferStatewide: true,
      maxResources: 4,
      browseCategorySlug: "healthcare",
    },
    {
      id: "id-documents",
      categorySlugs: ["id-documentation"],
      includeStatewide: true,
      maxResources: 4,
      browseCategorySlug: "id-documentation",
    },
    {
      id: "benefits",
      categorySlugs: ["financial-assistance", "food-nutrition"],
      tagSlugs: ["benefits", "medicaid", "snap", "ssi"],
      includeStatewide: true,
      maxResources: 4,
      browseCategorySlug: "financial-assistance",
    },
    {
      id: "housing",
      categorySlugs: ["housing"],
      includeStatewide: true,
      maxResources: 4,
      browseCategorySlug: "housing",
    },
    {
      id: "treatment",
      categorySlugs: ["substance-use-treatment", "healthcare"],
      includeStatewide: true,
      maxResources: 4,
      browseCategorySlug: "substance-use-treatment",
    },
    {
      id: "employment",
      categorySlugs: ["employment", "education"],
      includeStatewide: true,
      maxResources: 4,
      browseCategorySlug: "employment",
    },
    {
      id: "legal",
      categorySlugs: ["legal-aid"],
      includeStatewide: true,
      maxResources: 4,
      browseCategorySlug: "legal-aid",
    },
  ],
};
