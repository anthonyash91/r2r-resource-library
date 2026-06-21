-- Default About and Contact pages for Reentry Resource Library
-- Run after: supabase/migrations/001_initial_schema.sql
-- Safe to re-run: uses fixed IDs with ON CONFLICT DO UPDATE

INSERT INTO cms_pages (
  id, title, slug, content, meta_description, status, sort_order, published_at
) VALUES
  (
    'a1000001-0001-4000-8000-000000000001',
    'About Us',
    'about',
    'The Reentry Resource Library is a free platform designed to help individuals preparing for release or recently released from incarceration find the support they need to rebuild their lives.

We connect people with local, state, and national programs for housing, employment, healthcare, recovery, education, legal assistance, and more.

Our mission is simple: reduce barriers to reentry by making vital information easy to find, understand, and act on.

Who We Serve
• Individuals preparing for release
• Recently released individuals
• Reentry coordinators and case managers
• Probation and parole officers
• Community organizations',
    'Learn about the Reentry Resource Library and our mission.',
    'published',
    1,
    NOW()
  ),
  (
    'a1000001-0002-4000-8000-000000000001',
    'Contact Us',
    'contact',
    'We are here to help you find resources and improve this library.

Suggest a resource
Know a program that should be listed? Send us the organization name, location, and services offered.

Report outdated information
If a listing has wrong hours, a phone number, or eligibility details, let us know so we can review it.

General questions
For help using the site, creating an account, or accessing saved resources, visit our FAQ page or send us a message.

Email
[Your program email address]

Please include your city or county when asking about local resources so we can respond more helpfully.',
    'Get in touch with the Reentry Resource Library team.',
    'published',
    2,
    NOW()
  )
ON CONFLICT (slug) DO UPDATE SET
  title = EXCLUDED.title,
  content = EXCLUDED.content,
  meta_description = EXCLUDED.meta_description,
  status = EXCLUDED.status,
  sort_order = EXCLUDED.sort_order,
  published_at = EXCLUDED.published_at,
  updated_at = NOW();
