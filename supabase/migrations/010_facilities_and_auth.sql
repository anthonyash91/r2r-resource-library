-- Facilities registry and inmate account fields

CREATE TABLE facilities (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  site_id_hash TEXT NOT NULL,
  site_id_encrypted TEXT NOT NULL,
  is_active BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  CONSTRAINT facilities_site_id_hash_unique UNIQUE (site_id_hash)
);

CREATE INDEX facilities_is_active_idx ON facilities (is_active) WHERE is_active = true;

ALTER TABLE profiles
  ADD COLUMN IF NOT EXISTS signup_context TEXT,
  ADD COLUMN IF NOT EXISTS inmate_pin_hash TEXT,
  ADD COLUMN IF NOT EXISTS recovery_question_1 TEXT,
  ADD COLUMN IF NOT EXISTS recovery_answer_1_hash TEXT,
  ADD COLUMN IF NOT EXISTS recovery_question_2 TEXT,
  ADD COLUMN IF NOT EXISTS recovery_answer_2_hash TEXT;

ALTER TABLE profiles
  DROP CONSTRAINT IF EXISTS profiles_signup_context_check;

ALTER TABLE profiles
  ADD CONSTRAINT profiles_signup_context_check
  CHECK (signup_context IS NULL OR signup_context IN ('standard', 'facility'));

DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM pg_constraint WHERE conname = 'profiles_facility_id_fkey'
  ) THEN
    ALTER TABLE profiles
      ADD CONSTRAINT profiles_facility_id_fkey
      FOREIGN KEY (facility_id) REFERENCES facilities(id) ON DELETE SET NULL;
  END IF;
END $$;

CREATE UNIQUE INDEX IF NOT EXISTS profiles_facility_pin_unique
  ON profiles (facility_id, inmate_pin_hash)
  WHERE facility_id IS NOT NULL AND inmate_pin_hash IS NOT NULL;

ALTER TABLE facilities ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Admins manage facilities" ON facilities
  FOR ALL
  USING (is_admin())
  WITH CHECK (is_admin());

CREATE OR REPLACE FUNCTION update_facilities_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER facilities_updated_at
  BEFORE UPDATE ON facilities
  FOR EACH ROW
  EXECUTE FUNCTION update_facilities_updated_at();
