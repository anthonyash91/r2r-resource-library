import { NextResponse } from "next/server";
import { getResourceFilterOptions } from "@/lib/data";
import { parseIntakeFilterParam } from "@/lib/intake-signals";

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const state = searchParams.get("state")?.trim() || undefined;
  const county = searchParams.get("county")?.trim() || undefined;
  const city = searchParams.get("city")?.trim() || undefined;
  const categorySlug = searchParams.get("category")?.trim() || undefined;
  const service = searchParams.get("service")?.trim() || undefined;
  const intake = parseIntakeFilterParam(searchParams.get("intake"));

  const options = await getResourceFilterOptions({
    state,
    county,
    city,
    categorySlug,
    service,
    intake,
  });

  return NextResponse.json({
    cities: options.cities,
    counties: options.counties,
    countyCounts: options.countyCounts,
    services: options.services,
    categories: options.categories.map((category) => ({
      id: category.id,
      slug: category.slug,
      name: category.name,
    })),
    categoryCounts: options.categoryCounts,
    serviceCounts: options.serviceCounts,
    intakeCounts: options.intakeCounts,
  });
}
