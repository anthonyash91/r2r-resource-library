import { getActiveResourceMapStates } from "@/lib/resource-map-pins";
import type { Resource } from "@/types";

/** Grid placement for the homepage state-tile coverage map (from redesign). */
const COVERAGE_TILE_LAYOUT = [
  { abbr: "MN", col: 3, row: 1 },
  { abbr: "WI", col: 4, row: 1 },
  { abbr: "MI", col: 6, row: 1 },
  { abbr: "NY", col: 7, row: 1 },
  { abbr: "IA", col: 3, row: 2 },
  { abbr: "IL", col: 4, row: 2 },
  { abbr: "IN", col: 5, row: 2 },
  { abbr: "OH", col: 6, row: 2 },
  { abbr: "PA", col: 7, row: 2 },
  { abbr: "MO", col: 3, row: 3 },
  { abbr: "KY", col: 5, row: 3 },
  { abbr: "WV", col: 7, row: 3 },
  { abbr: "VA", col: 8, row: 3 },
  { abbr: "AZ", col: 2, row: 5 },
  { abbr: "AR", col: 3, row: 4 },
  { abbr: "TN", col: 5, row: 4 },
  { abbr: "NC", col: 7, row: 4 },
  { abbr: "MS", col: 4, row: 5 },
  { abbr: "AL", col: 5, row: 5 },
  { abbr: "GA", col: 6, row: 5 },
  { abbr: "SC", col: 7, row: 5 },
  { abbr: "LA", col: 4, row: 6 },
  { abbr: "FL", col: 6, row: 6 },
] as const;

const STATE_NAME_TO_ABBR: Record<string, string> = {
  Alabama: "AL",
  Arizona: "AZ",
  Arkansas: "AR",
  Florida: "FL",
  Georgia: "GA",
  Illinois: "IL",
  Indiana: "IN",
  Iowa: "IA",
  Kentucky: "KY",
  Louisiana: "LA",
  Michigan: "MI",
  Minnesota: "MN",
  Mississippi: "MS",
  Missouri: "MO",
  "New York": "NY",
  "North Carolina": "NC",
  Ohio: "OH",
  Pennsylvania: "PA",
  "South Carolina": "SC",
  Tennessee: "TN",
  Virginia: "VA",
  "West Virginia": "WV",
  Wisconsin: "WI",
};

export interface CoverageTile {
  abbr: string;
  col: number;
  row: number;
  active: boolean;
}

export function buildCoverageTiles(resources: Resource[]): CoverageTile[] {
  const activeAbbrs = new Set(
    [...getActiveResourceMapStates(resources)].map(
      (name) => STATE_NAME_TO_ABBR[name] ?? name.slice(0, 2).toUpperCase()
    )
  );

  const cols = COVERAGE_TILE_LAYOUT.map((tile) => tile.col);
  const minC = Math.min(...cols);
  const maxC = Math.max(...cols);
  const shift = Math.round((8 - (maxC - minC + 1)) / 2) - (minC - 1);

  return COVERAGE_TILE_LAYOUT.map((tile) => ({
    abbr: tile.abbr,
    col: tile.col + shift,
    row: tile.row,
    active: activeAbbrs.has(tile.abbr),
  }));
}

export function countActiveCoverageTiles(tiles: CoverageTile[]): number {
  return tiles.filter((tile) => tile.active).length;
}
