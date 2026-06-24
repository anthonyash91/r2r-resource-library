import type { Category, Resource } from "@/types";
import type { IntakeSignal } from "@/lib/intake-signals";
import {
  countResourcesByIntakeSignal,
  filterResourcesByIntakeSignals,
} from "@/lib/intake-signals";
import {
  countResourcesByCategoryId,
  countResourcesByService,
  isStatewideResource,
  resourceServesCounty,
  resourcesForLocationFacets,
} from "@/lib/resource-coverage";
import { normalizeService } from "@/lib/service-types";

export interface ResourceFilterFacetParams {
  state?: string;
  county?: string;
  city?: string;
  categorySlug?: string;
  categoryId?: string;
  service?: string;
  intake?: IntakeSignal[];
}

export type FacetDimension = "county" | "city" | "category" | "service" | "intake";

function filterByService(resources: Resource[], service: string): Resource[] {
  const normalized = normalizeService(service).toLowerCase();
  return resources.filter((resource) =>
    resource.services.some((svc) => normalizeService(svc).toLowerCase() === normalized)
  );
}

function filterByCity(resources: Resource[], city: string): Resource[] {
  return resources.filter((resource) => resource.city === city);
}

function filterByCategory(resources: Resource[], categoryId: string): Resource[] {
  return resources.filter((resource) => resource.category_id === categoryId);
}

export function applyResourceFacetFilters(
  resources: Resource[],
  params: ResourceFilterFacetParams,
  exclude: FacetDimension
): Resource[] {
  let result = resources;

  if (params.county?.trim() && exclude !== "county") {
    result = resourcesForLocationFacets(result, params.county);
  }

  if (params.city && exclude !== "city") {
    result = filterByCity(result, params.city);
  }

  if (params.categoryId && exclude !== "category") {
    result = filterByCategory(result, params.categoryId);
  }

  if (params.service && exclude !== "service") {
    result = filterByService(result, params.service);
  }

  if (params.intake?.length && exclude !== "intake") {
    result = filterResourcesByIntakeSignals(result, params.intake);
  }

  return result;
}

export function countResourcesByCounty(
  resources: Resource[],
  counties: string[]
): Record<string, number> {
  const counts = Object.fromEntries(counties.map((county) => [county, 0])) as Record<
    string,
    number
  >;

  for (const resource of resources) {
    if (isStatewideResource(resource)) continue;
    for (const county of counties) {
      if (resourceServesCounty(resource, county)) {
        counts[county] += 1;
      }
    }
  }

  return counts;
}

export interface BuiltResourceFilterOptions {
  cities: string[];
  counties: string[];
  countyCounts: Record<string, number>;
  services: string[];
  categories: Category[];
  categoryCounts: Record<string, number>;
  serviceCounts: Record<string, number>;
  intakeCounts: Record<IntakeSignal, number>;
}

export function buildResourceFilterOptions(
  resources: Resource[],
  allCategories: Category[],
  params: ResourceFilterFacetParams,
  stateCounties: string[] = []
): BuiltResourceFilterOptions {
  const forCategory = applyResourceFacetFilters(resources, params, "category");
  const categoryCountById = countResourcesByCategoryId(forCategory);
  const categories = allCategories.filter((category) => categoryCountById.has(category.id));
  const categoryCounts = Object.fromEntries(
    categories.map((category) => [category.slug, categoryCountById.get(category.id) ?? 0])
  );

  const forService = applyResourceFacetFilters(resources, params, "service");
  const serviceCountByName = countResourcesByService(forService);
  const services = [...serviceCountByName.keys()].sort((a, b) => a.localeCompare(b));
  const serviceCounts = Object.fromEntries(serviceCountByName.entries());

  const forIntake = applyResourceFacetFilters(resources, params, "intake");
  const intakeCounts = countResourcesByIntakeSignal(forIntake);

  let counties: string[] = [];
  let countyCounts: Record<string, number> = {};
  if (params.state && stateCounties.length > 0) {
    const forCounty = applyResourceFacetFilters(resources, params, "county");
    countyCounts = countResourcesByCounty(forCounty, stateCounties);
    counties = stateCounties
      .filter((county) => (countyCounts[county] ?? 0) > 0)
      .sort((a, b) => a.localeCompare(b));
  }

  let cities: string[] = [];
  if (params.state && params.county) {
    const forCity = applyResourceFacetFilters(resources, params, "city");
    const scoped = resourcesForLocationFacets(forCity, params.county);
    cities = [
      ...new Set(scoped.map((resource) => resource.city).filter(Boolean) as string[]),
    ].sort((a, b) => a.localeCompare(b));
  }

  return {
    cities,
    counties,
    countyCounts,
    services,
    categories,
    categoryCounts,
    serviceCounts,
    intakeCounts,
  };
}
