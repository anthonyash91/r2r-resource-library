import { HomeSectionRule } from "@/components/home/home-section-divider";
import { HomePossibleStories } from "@/components/home/home-possible-stories";
import { StateTilesCoverageMap } from "@/components/home/state-tiles-coverage-map";
import { countActiveCoverageTiles, buildCoverageTiles } from "@/lib/home/coverage-tiles";
import type { Resource } from "@/types";

interface HomePossibleSectionProps {
  resources: Resource[];
  resourceStat: string;
}

export async function HomePossibleSection({
  resources,
  resourceStat,
}: HomePossibleSectionProps) {
  const activeStateCount = countActiveCoverageTiles(buildCoverageTiles(resources));

  return (
    <section className="app-dark-section text-white" aria-labelledby="home-possible-heading">
      <HomePossibleStories />

      <HomeSectionRule variant="dark" />

      <div className="px-4 pb-[71px] sm:px-9 sm:pb-[99px]">
        <div className="mx-auto max-w-[1180px]">
          <StateTilesCoverageMap
            resources={resources}
            resourceStat={resourceStat}
            activeStateCount={activeStateCount}
          />
        </div>
      </div>
    </section>
  );
}
