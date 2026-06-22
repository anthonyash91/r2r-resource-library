-- User onboarding preferences for personalized recommendations

ALTER TABLE profiles
  ADD COLUMN IF NOT EXISTS priority_categories TEXT[] NOT NULL DEFAULT '{}',
  ADD COLUMN IF NOT EXISTS onboarding_completed_at TIMESTAMPTZ;
