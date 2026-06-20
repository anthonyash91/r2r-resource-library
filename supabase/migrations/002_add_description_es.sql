-- Add Spanish description field for bilingual resource content
ALTER TABLE resources ADD COLUMN IF NOT EXISTS description_es TEXT;
