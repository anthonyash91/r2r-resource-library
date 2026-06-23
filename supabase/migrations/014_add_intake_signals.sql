-- Structured intake / eligibility signals for resource listings
ALTER TABLE resources
  ADD COLUMN IF NOT EXISTS intake_signals TEXT[] NOT NULL DEFAULT '{}';

CREATE INDEX IF NOT EXISTS idx_resources_intake_signals
  ON resources USING GIN (intake_signals);
