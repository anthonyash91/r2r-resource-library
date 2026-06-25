import { NextResponse } from "next/server";
import {
  loadActiveResourcePool,
  queryResources,
  queryResourcesFromPool,
  resolveZipLocationFromFilters,
} from "@/lib/data";
import { resourcesPageParamsFromSearchParams } from "@/lib/resources-page-filters";
import { resolveResourcesPageFilters } from "@/lib/resources-page-filters.server";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const params = resourcesPageParamsFromSearchParams(searchParams);
  const filters = await resolveResourcesPageFilters(params);
  const zipSearch = resolveZipLocationFromFilters(filters);
  const poolState = filters.state?.trim() || zipSearch?.state;

  if (poolState) {
    const pool = await loadActiveResourcePool(poolState);
    const result = await queryResourcesFromPool(pool, filters);
    return NextResponse.json(result);
  }

  const { resources, zipSearch: resolvedZip } = await queryResources(filters);
  return NextResponse.json({ resources, zipSearch: resolvedZip });
}
