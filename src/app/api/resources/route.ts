import { NextResponse } from "next/server";
import { getResources } from "@/lib/data";
import { resourcesPageParamsFromSearchParams } from "@/lib/resources-page-filters";
import { resolveResourcesPageFilters } from "@/lib/resources-page-filters.server";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const params = resourcesPageParamsFromSearchParams(searchParams);
  const filters = await resolveResourcesPageFilters(params);
  const resources = await getResources(filters);

  return NextResponse.json({ resources });
}
