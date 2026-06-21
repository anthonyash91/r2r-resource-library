-- Reset all content data (keeps schema, auth users, and profiles)
-- Run in the Supabase SQL Editor when you want a clean slate for everything.
--
-- To reset ONLY resources and categories (keeps FAQs, CMS, etc.), use:
--   supabase/reset-resources.sql

TRUNCATE TABLE
  saved_resources,
  resource_views,
  resources,
  categories,
  cms_pages,
  announcements,
  faqs,
  homepage_content
RESTART IDENTITY CASCADE;
