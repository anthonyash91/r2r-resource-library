-- Seed data for Reentry Resource Library
-- Run after 001_initial_schema.sql

-- Categories
INSERT INTO categories (id, name, slug, description, icon, sort_order) VALUES
  ('11111111-1111-1111-1111-111111111101', 'Housing', 'housing', 'Shelter, transitional housing, and rental assistance', 'home', 1),
  ('11111111-1111-1111-1111-111111111102', 'Employment', 'employment', 'Job training, placement, and career services', 'briefcase', 2),
  ('11111111-1111-1111-1111-111111111103', 'Food Assistance', 'food-assistance', 'Food banks, SNAP enrollment, and meal programs', 'utensils', 3),
  ('11111111-1111-1111-1111-111111111104', 'Healthcare', 'healthcare', 'Medical care, clinics, and health insurance', 'heart-pulse', 4),
  ('11111111-1111-1111-1111-111111111105', 'Mental Health', 'mental-health', 'Counseling, therapy, and crisis support', 'brain', 5),
  ('11111111-1111-1111-1111-111111111106', 'Substance Abuse Recovery', 'substance-abuse-recovery', 'Treatment, support groups, and sober living', 'shield', 6),
  ('11111111-1111-1111-1111-111111111107', 'Transportation', 'transportation', 'Bus passes, rides, and vehicle assistance', 'bus', 7),
  ('11111111-1111-1111-1111-111111111108', 'Education', 'education', 'GED, college, vocational training', 'graduation-cap', 8),
  ('11111111-1111-1111-1111-111111111109', 'Financial Assistance', 'financial-assistance', 'Benefits, emergency funds, and budgeting help', 'dollar-sign', 9),
  ('11111111-1111-1111-1111-111111111110', 'Legal Aid', 'legal-aid', 'Free legal help and expungement services', 'scale', 10),
  ('11111111-1111-1111-1111-111111111111', 'Identification Documents', 'identification-documents', 'ID cards, birth certificates, and Social Security', 'id-card', 11),
  ('11111111-1111-1111-1111-111111111112', 'Family Services', 'family-services', 'Reunification, parenting, and child support', 'users', 12),
  ('11111111-1111-1111-1111-111111111113', 'Veterans Services', 'veterans-services', 'VA benefits and veteran-specific programs', 'medal', 13),
  ('11111111-1111-1111-1111-111111111114', 'Disability Services', 'disability-services', 'Accessibility support and disability benefits', 'accessibility', 14),
  ('11111111-1111-1111-1111-111111111115', 'Community Support Programs', 'community-support-programs', 'Peer support, mentoring, and community centers', 'handshake', 15),
  ('11111111-1111-1111-1111-111111111116', 'Emergency Assistance', 'emergency-assistance', 'Crisis help, hotlines, and immediate support', 'phone', 16)
ON CONFLICT (slug) DO NOTHING;

-- Homepage content
INSERT INTO homepage_content (key, value) VALUES
  ('hero_headline', 'Find the Resources You Need for a Successful Reentry'),
  ('hero_subheadline', 'Search local, state, and national programs that can help with housing, employment, healthcare, recovery, transportation, education, and more.')
ON CONFLICT (key) DO NOTHING;

-- Sample FAQs
INSERT INTO faqs (question, answer, category, sort_order) VALUES
  ('Who can use this resource library?', 'Anyone can search and view resources. Creating an account lets you save resources and track your personal list.', 'General', 1),
  ('Is this service free?', 'Yes. Searching resources and creating an account are completely free.', 'General', 2),
  ('How do I save a resource?', 'Click the Save button on any resource. You must be signed in.', 'Using the Site', 3)
ON CONFLICT DO NOTHING;

-- Note: Create admin user via Supabase Auth dashboard, then update profile:
-- UPDATE profiles SET role = 'admin' WHERE email = 'admin@yourorg.org';
