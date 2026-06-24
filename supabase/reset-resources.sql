-- Wipe all resources and categories (keeps FAQs, CMS pages, users, homepage settings)
-- Run in Supabase SQL Editor BEFORE loading supabase/seed-kentucky-resources.sql

TRUNCATE TABLE
  saved_resources,
  resource_views,
  resources,
  categories
RESTART IDENTITY CASCADE;
