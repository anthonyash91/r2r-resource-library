-- Separate eligibility from operational notes; add Spanish eligibility column.

ALTER TABLE resources
  ADD COLUMN IF NOT EXISTS eligibility_es TEXT,
  ADD COLUMN IF NOT EXISTS notes TEXT,
  ADD COLUMN IF NOT EXISTS notes_es TEXT;

-- Backfill: existing eligibility column holds mixed content from the old CSV notes field.
-- Run scripts/migrate-eligibility-fields.ts before re-seeding to split content properly.
