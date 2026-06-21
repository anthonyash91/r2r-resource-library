import { KENTUCKY_COUNTIES } from "@/lib/kentucky/counties";
import { OHIO_COUNTIES } from "@/lib/ohio/counties";

/** Returns the canonical county list for a state, or an empty array if unknown. */
export function getStateCounties(state?: string): readonly string[] {
  if (!state || state === "Kentucky") return KENTUCKY_COUNTIES;
  if (state === "Ohio") return OHIO_COUNTIES;
  return [];
}
