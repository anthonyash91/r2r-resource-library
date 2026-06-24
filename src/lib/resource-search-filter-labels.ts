import { getCategoryLabel } from "@/i18n/category-label";
import { parseIntakeFilterParam } from "@/lib/intake-signals";
import { isValidCoverage } from "@/lib/resource-coverage";
import type { Category } from "@/types";

export interface ResourceSearchFilterParams {
  q?: string;
  state?: string;
  county?: string;
  city?: string;
  category?: string;
  service?: string;
  tag?: string;
  coverage?: string;
  intake?: string;
  filter?: string;
}

export interface BuildResourceSearchFilterLabelsOptions {
  /** Omit keyword when it already appears in the results heading. */
  excludeQuery?: boolean;
  /** Omit county when it already appears in a county-specific heading. */
  excludeCounty?: boolean;
}

type Translator = (key: string, params?: Record<string, string | number>) => string;

export function buildResourceSearchFilterLabels(
  params: ResourceSearchFilterParams,
  categories: Category[],
  t: Translator,
  options: BuildResourceSearchFilterLabelsOptions = {}
): string[] {
  const labels: string[] = [];

  const query = params.q?.trim();
  if (query && !options.excludeQuery) {
    labels.push(query);
  }

  const categorySlug = params.category?.trim();
  if (categorySlug) {
    const category = categories.find((item) => item.slug === categorySlug);
    labels.push(category ? getCategoryLabel(category, t) : categorySlug);
  }

  const state = params.state?.trim();
  if (state) labels.push(state);

  const county = params.county?.trim();
  if (county && !options.excludeCounty) labels.push(county);

  const city = params.city?.trim();
  if (city) labels.push(city);

  const service = params.service?.trim();
  if (service) labels.push(service);

  for (const signal of parseIntakeFilterParam(params.intake)) {
    labels.push(t(`resources.intakeSignals.${signal}`));
  }

  const coverage = params.coverage?.trim();
  if (coverage && isValidCoverage(coverage)) {
    if (coverage === "statewide") {
      labels.push(t("resources.coverageStatewide"));
    } else if (coverage === "multi") {
      labels.push(t("resources.coverageRegional"));
    } else {
      labels.push(t("resources.coverageInCounty"));
    }
  }

  const tag = params.tag?.trim();
  if (tag) labels.push(tag);

  if (params.filter?.trim() === "recent") {
    labels.push(t("resources.recentlyAdded"));
  }

  return labels;
}
