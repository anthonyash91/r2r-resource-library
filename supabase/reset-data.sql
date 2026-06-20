-- Reset all content data (keeps schema, auth users, and profiles)
-- Run in the Supabase SQL Editor when you want a clean slate.

TRUNCATE TABLE saved_resources CASCADE;
TRUNCATE TABLE resource_views CASCADE;
TRUNCATE TABLE resources CASCADE;
TRUNCATE TABLE categories CASCADE;
TRUNCATE TABLE cms_pages CASCADE;
TRUNCATE TABLE announcements CASCADE;
TRUNCATE TABLE faqs CASCADE;
TRUNCATE TABLE homepage_content CASCADE;
