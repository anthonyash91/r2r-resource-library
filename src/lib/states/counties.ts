import { KENTUCKY_COUNTIES } from "@/lib/kentucky/counties";
import { getOnboardingStateConfig } from "@/lib/states/registry";

/** Returns the canonical county list for a state, or Kentucky counties when unknown. */
export function getStateCounties(state?: string): readonly string[] {
  if (!state) return KENTUCKY_COUNTIES;
  return getOnboardingStateConfig(state)?.counties ?? [];
}
