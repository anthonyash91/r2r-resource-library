import { US_MAP_VIEWBOX } from "@/lib/us-map/state-paths.generated";

const LON_MIN = -125.0;
const LON_MAX = -66.5;
const LAT_MIN = 24.0;
const LAT_MAX = 49.5;

export function projectLatLonToMap(lon: number, lat: number): { x: number; y: number } {
  const x = ((lon - LON_MIN) / (LON_MAX - LON_MIN)) * US_MAP_VIEWBOX.width;
  const y = ((LAT_MAX - lat) / (LAT_MAX - LAT_MIN)) * US_MAP_VIEWBOX.height;
  return { x, y };
}
