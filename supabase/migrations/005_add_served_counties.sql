-- Service area: which counties a resource serves (for inmate home / release-county filtering).

ALTER TABLE resources
  ADD COLUMN IF NOT EXISTS served_counties TEXT[] NOT NULL DEFAULT '{}',
  ADD COLUMN IF NOT EXISTS coverage TEXT NOT NULL DEFAULT 'single'
    CHECK (coverage IN ('single', 'multi', 'statewide'));

CREATE INDEX IF NOT EXISTS idx_resources_served_counties
  ON resources USING GIN (served_counties);

CREATE INDEX IF NOT EXISTS idx_resources_coverage
  ON resources (coverage);
