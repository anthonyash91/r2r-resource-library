-- Resources no longer store map coordinates.

ALTER TABLE resources
  DROP COLUMN IF EXISTS latitude,
  DROP COLUMN IF EXISTS longitude;
