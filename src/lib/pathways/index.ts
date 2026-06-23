import { FIRST_WEEK_PATHWAY } from "./first-week";
import type { PathwayDef } from "./types";

const PATHWAYS: Record<string, PathwayDef> = {
  [FIRST_WEEK_PATHWAY.slug]: FIRST_WEEK_PATHWAY,
};

export function getPathwayBySlug(slug: string): PathwayDef | null {
  return PATHWAYS[slug] ?? null;
}

export { FIRST_WEEK_PATHWAY };
export type { PathwayDef, PathwayStepDef, MatchedPathwayStep } from "./types";
export { matchPathwaySteps } from "./match-step-resources";
