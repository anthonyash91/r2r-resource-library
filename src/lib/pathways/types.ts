import type { Resource } from "@/types";

export interface PathwayStepDef {
  id: string;
  categorySlugs?: string[];
  tagSlugs?: string[];
  /** Include statewide resources when local matches are exhausted. */
  includeStatewide: boolean;
  /** Crisis and hotline steps surface statewide resources first. */
  preferStatewide?: boolean;
  maxResources: number;
  /** Primary category for "browse all" links. */
  browseCategorySlug?: string;
}

export interface PathwayDef {
  slug: string;
  stepIds: PathwayStepDef[];
}

export interface MatchedPathwayStep {
  step: PathwayStepDef;
  resources: Resource[];
  localResources: Resource[];
  statewideResources: Resource[];
  matchesUserPriority: boolean;
}
