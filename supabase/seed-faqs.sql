-- Default Help & FAQ content for Reentry Resource Library
-- Run after: supabase/migrations/001_initial_schema.sql
-- Safe to re-run: uses fixed IDs with ON CONFLICT DO UPDATE

INSERT INTO faqs (id, question, answer, category, sort_order, is_active) VALUES
  (
    'f1000001-0001-4000-8000-000000000001',
    'What is the Reentry Resource Library?',
    'A free online directory that helps people returning from incarceration—and their families and supporters—find programs for housing, employment, healthcare, legal help, treatment, and other reentry needs.',
    'General',
    1,
    true
  ),
  (
    'f1000001-0002-4000-8000-000000000001',
    'Who is this website for?',
    'Anyone can search resources. The site is built for people in reentry, family members, case managers, parole/probation staff, and community organizations looking for verified local programs.',
    'General',
    2,
    true
  ),
  (
    'f1000001-0003-4000-8000-000000000001',
    'Is this service free?',
    'Yes. Searching and browsing are free. Creating an account is also free. Individual programs may have their own fees or eligibility rules.',
    'General',
    3,
    true
  ),
  (
    'f1000001-0004-4000-8000-000000000001',
    'Does this site provide legal, medical, or emergency help?',
    'No. This library lists community programs and contact information. It does not replace lawyers, doctors, or crisis services. If you are in crisis, call or text 988, or text HOME to 741741.',
    'General',
    4,
    true
  ),
  (
    'f1000001-0005-4000-8000-000000000001',
    'What areas does the library cover?',
    'The library is designed to grow over time. Programs are organized by state, county, and city so you can find help near you. Check the resources page for what is currently listed in your area.',
    'General',
    5,
    true
  ),
  (
    'f1000001-0006-4000-8000-000000000001',
    'How do I know if a program is right for me?',
    'Each listing includes eligibility information when available. Contact the organization directly to confirm you qualify, that space is available, and that hours or services have not changed.',
    'General',
    6,
    true
  ),
  (
    'f1000001-0007-4000-8000-000000000001',
    'Can family members or case managers use this site?',
    'Yes. Anyone may search. Case managers and family members often use the site to research options and share listings with someone in reentry.',
    'General',
    7,
    true
  ),
  (
    'f1000001-0008-4000-8000-000000000001',
    'Can I suggest a resource or report incorrect information?',
    'Yes. If a program is missing, outdated, or incorrect, contact us through the About page or ask your case manager to submit an update for review.',
    'General',
    8,
    true
  ),
  (
    'f1000001-0009-4000-8000-000000000001',
    'How do I search for resources?',
    'Use the search bar on the homepage or resources page. You can search by keyword (such as housing or jobs) or by location (city, county, or state). Open Location & advanced filters to narrow results by category, service type, and more.',
    'Using the Site',
    9,
    true
  ),
  (
    'f1000001-0010-4000-8000-000000000001',
    'How do I filter by location?',
    'On the resources page, open Location & advanced filters. Choose a state first, then county and city if available. You can also type a city or county name in the main search bar.',
    'Using the Site',
    10,
    true
  ),
  (
    'f1000001-0011-4000-8000-000000000001',
    'What do the categories mean?',
    'Categories group programs by type of help—such as housing, employment, healthcare, legal aid, and recovery services. Select a category in the filters or browse from the homepage to see related programs.',
    'Using the Site',
    11,
    true
  ),
  (
    'f1000001-0012-4000-8000-000000000001',
    'Do I need an account to use the site?',
    'No. You can search and view resources without signing in. An account is only needed to save favorites and use your personal dashboard.',
    'Using the Site',
    12,
    true
  ),
  (
    'f1000001-0013-4000-8000-000000000001',
    'How do I save a resource?',
    'Sign in, then click Save on a resource card or detail page. Saved items appear on your Saved page and in your dashboard.',
    'Using the Site',
    13,
    true
  ),
  (
    'f1000001-0014-4000-8000-000000000001',
    'What is the dashboard?',
    'The dashboard is your personal page when signed in. It helps you return to saved resources and resources you have viewed recently.',
    'Using the Site',
    14,
    true
  ),
  (
    'f1000001-0015-4000-8000-000000000001',
    'Is the site available in Spanish?',
    'Yes. Use the language switcher (EN / ES) in the top navigation to view the site in English or Spanish.',
    'Using the Site',
    15,
    true
  ),
  (
    'f1000001-0016-4000-8000-000000000001',
    'How often is information updated?',
    'We review listings regularly and show a last updated date when available. Programs can change without notice, so always confirm details with the organization before relying on them.',
    'Using the Site',
    16,
    true
  ),
  (
    'f1000001-0017-4000-8000-000000000001',
    'Why don''t I see any results?',
    'Try clearing filters, searching a broader area (such as your county or state instead of a city), or using a general term like housing or employment. Some areas may have fewer listed programs while the library is still growing.',
    'Using the Site',
    17,
    true
  ),
  (
    'f1000001-0018-4000-8000-000000000001',
    'What information do I need to create an account?',
    'Typically your name, email address, and a password. Some profile fields are optional and help personalize your experience.',
    'Accounts & Privacy',
    18,
    true
  ),
  (
    'f1000001-0019-4000-8000-000000000001',
    'Is my saved list private?',
    'Yes. Saved resources are tied to your account and are not visible to other users.',
    'Accounts & Privacy',
    19,
    true
  ),
  (
    'f1000001-0020-4000-8000-000000000001',
    'How do I sign out or delete my account?',
    'Use Sign out in the top navigation. To delete an account, contact us through the About page and we will help you.',
    'Accounts & Privacy',
    20,
    true
  )
ON CONFLICT (id) DO UPDATE SET
  question = EXCLUDED.question,
  answer = EXCLUDED.answer,
  category = EXCLUDED.category,
  sort_order = EXCLUDED.sort_order,
  is_active = EXCLUDED.is_active,
  updated_at = NOW();
