import type { Resource } from "@/types";
import { ResourcesCoverageMap } from "@/components/home/resources-coverage-map";
import {
  buildResourceMapPins,
  buildResourceMapStateSummaries,
  getActiveResourceMapStates,
} from "@/lib/resource-map-pins";
import { cn, pageSectionHeadingClass, pageSectionPadding, pageSectionSubtitleClass, pageSectionBandClass, type PageSectionBand } from "@/lib/utils";
import { getServerTranslator } from "@/i18n/server";

interface ResourcesCoverageMapSectionProps {
  resources: Resource[];
  band?: PageSectionBand;
}

export async function ResourcesCoverageMapSection({
  resources,
  band = "muted",
}: ResourcesCoverageMapSectionProps) {
  const { t } = await getServerTranslator();
  const pins = buildResourceMapPins(resources);
  const stateSummaries = buildResourceMapStateSummaries(resources);
  const activeStates = [...getActiveResourceMapStates(resources)];

  if (stateSummaries.length === 0) return null;

  return (
    <section
      className={cn(pageSectionBandClass(band), pageSectionPadding)}
      aria-labelledby="coverage-map-heading"
    >
      <div className="mx-auto max-w-7xl">
        <header className="mb-10 text-center">
          <h2 id="coverage-map-heading" className={pageSectionHeadingClass}>
            {t("home.coverageMapTitle")}
          </h2>
          <p className={cn("mx-auto mt-2 max-w-3xl", pageSectionSubtitleClass)}>
            {t("home.coverageMapSubtitle", {
              states: String(stateSummaries.length),
              areas: String(pins.length),
            })}
          </p>
        </header>

        <ResourcesCoverageMap
          pins={pins}
          stateSummaries={stateSummaries}
          activeStates={activeStates}
        />
      </div>
    </section>
  );
}
