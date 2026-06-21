-- Reentry Resource Library - Initial Schema
-- Run in Supabase SQL Editor or via supabase db push

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Custom types
CREATE TYPE user_role AS ENUM ('user', 'case_manager', 'admin');
CREATE TYPE resource_status AS ENUM ('active', 'inactive', 'archived');
CREATE TYPE cms_page_status AS ENUM ('draft', 'published', 'archived');
CREATE TYPE announcement_status AS ENUM ('draft', 'published', 'archived');

-- Profiles (extends auth.users)
CREATE TABLE profiles (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT NOT NULL,
  full_name TEXT,
  role user_role NOT NULL DEFAULT 'user',
  is_active BOOLEAN NOT NULL DEFAULT true,
  phone TEXT,
  state TEXT,
  county TEXT,
  city TEXT,
  facility_id UUID, -- future: facility-specific libraries
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Categories
CREATE TABLE categories (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL UNIQUE,
  slug TEXT NOT NULL UNIQUE,
  description TEXT,
  icon TEXT,
  sort_order INT NOT NULL DEFAULT 0,
  is_active BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Resources
CREATE TABLE resources (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL,
  description TEXT NOT NULL,
  category_id UUID NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
  state TEXT,
  county TEXT,
  city TEXT,
  address TEXT,
  phone TEXT,
  website TEXT,
  email TEXT,
  hours TEXT,
  eligibility TEXT,
  services TEXT[] NOT NULL DEFAULT '{}',
  tags TEXT[] NOT NULL DEFAULT '{}',
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  is_featured BOOLEAN NOT NULL DEFAULT false,
  status resource_status NOT NULL DEFAULT 'active',
  view_count INT NOT NULL DEFAULT 0,
  save_count INT NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_by UUID REFERENCES profiles(id) ON DELETE SET NULL
);

-- Saved resources
CREATE TABLE saved_resources (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
  resource_id UUID NOT NULL REFERENCES resources(id) ON DELETE CASCADE,
  notes TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(user_id, resource_id)
);

-- Recently viewed resources
CREATE TABLE resource_views (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
  resource_id UUID NOT NULL REFERENCES resources(id) ON DELETE CASCADE,
  session_id TEXT,
  viewed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- CMS Pages
CREATE TABLE cms_pages (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  title TEXT NOT NULL,
  slug TEXT NOT NULL UNIQUE,
  content TEXT NOT NULL,
  meta_description TEXT,
  status cms_page_status NOT NULL DEFAULT 'draft',
  sort_order INT NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  published_at TIMESTAMPTZ,
  created_by UUID REFERENCES profiles(id) ON DELETE SET NULL
);

-- Announcements
CREATE TABLE announcements (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  status announcement_status NOT NULL DEFAULT 'draft',
  is_pinned BOOLEAN NOT NULL DEFAULT false,
  starts_at TIMESTAMPTZ,
  ends_at TIMESTAMPTZ,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  created_by UUID REFERENCES profiles(id) ON DELETE SET NULL
);

-- FAQs
CREATE TABLE faqs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  question TEXT NOT NULL,
  answer TEXT NOT NULL,
  category TEXT,
  sort_order INT NOT NULL DEFAULT 0,
  is_active BOOLEAN NOT NULL DEFAULT true,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Homepage content (key-value CMS)
CREATE TABLE homepage_content (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  key TEXT NOT NULL UNIQUE,
  value TEXT NOT NULL,
  updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  updated_by UUID REFERENCES profiles(id) ON DELETE SET NULL
);

-- Indexes for search performance
CREATE INDEX idx_resources_category ON resources(category_id);
CREATE INDEX idx_resources_state ON resources(state);
CREATE INDEX idx_resources_county ON resources(county);
CREATE INDEX idx_resources_city ON resources(city);
CREATE INDEX idx_resources_status ON resources(status);
CREATE INDEX idx_resources_featured ON resources(is_featured) WHERE is_featured = true;
CREATE INDEX idx_resources_services ON resources USING GIN(services);
CREATE INDEX idx_resources_tags ON resources USING GIN(tags);
CREATE INDEX idx_resources_search ON resources USING GIN(
  to_tsvector('english', coalesce(name, '') || ' ' || coalesce(description, '') || ' ' || coalesce(eligibility, ''))
);
CREATE INDEX idx_resources_name_trgm ON resources USING GIN(name gin_trgm_ops);
CREATE INDEX idx_saved_resources_user ON saved_resources(user_id);
CREATE INDEX idx_resource_views_user ON resource_views(user_id, viewed_at DESC);
CREATE INDEX idx_resource_views_resource ON resource_views(resource_id);

-- Updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER profiles_updated_at BEFORE UPDATE ON profiles FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER categories_updated_at BEFORE UPDATE ON categories FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER resources_updated_at BEFORE UPDATE ON resources FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER cms_pages_updated_at BEFORE UPDATE ON cms_pages FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER announcements_updated_at BEFORE UPDATE ON announcements FOR EACH ROW EXECUTE FUNCTION update_updated_at();
CREATE TRIGGER faqs_updated_at BEFORE UPDATE ON faqs FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- Auto-create profile on signup
CREATE OR REPLACE FUNCTION handle_new_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
  INSERT INTO public.profiles (id, email, full_name, role)
  VALUES (
    NEW.id,
    NEW.email,
    COALESCE(NEW.raw_user_meta_data->>'full_name', ''),
    'user'::user_role
  );
  RETURN NEW;
END;
$$;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE FUNCTION handle_new_user();

-- Increment view count
CREATE OR REPLACE FUNCTION increment_resource_view_count()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE resources SET view_count = view_count + 1 WHERE id = NEW.resource_id;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_resource_viewed
  AFTER INSERT ON resource_views
  FOR EACH ROW EXECUTE FUNCTION increment_resource_view_count();

-- Increment save count
CREATE OR REPLACE FUNCTION increment_resource_save_count()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE resources SET save_count = save_count + 1 WHERE id = NEW.resource_id;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_resource_saved
  AFTER INSERT ON saved_resources
  FOR EACH ROW EXECUTE FUNCTION increment_resource_save_count();

CREATE OR REPLACE FUNCTION decrement_resource_save_count()
RETURNS TRIGGER AS $$
BEGIN
  UPDATE resources SET save_count = GREATEST(save_count - 1, 0) WHERE id = OLD.resource_id;
  RETURN OLD;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_resource_unsaved
  AFTER DELETE ON saved_resources
  FOR EACH ROW EXECUTE FUNCTION decrement_resource_save_count();

-- Row Level Security
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE categories ENABLE ROW LEVEL SECURITY;
ALTER TABLE resources ENABLE ROW LEVEL SECURITY;
ALTER TABLE saved_resources ENABLE ROW LEVEL SECURITY;
ALTER TABLE resource_views ENABLE ROW LEVEL SECURITY;
ALTER TABLE cms_pages ENABLE ROW LEVEL SECURITY;
ALTER TABLE announcements ENABLE ROW LEVEL SECURITY;
ALTER TABLE faqs ENABLE ROW LEVEL SECURITY;
ALTER TABLE homepage_content ENABLE ROW LEVEL SECURITY;

-- Helper: check if user is admin
CREATE OR REPLACE FUNCTION is_admin()
RETURNS BOOLEAN AS $$
  SELECT EXISTS (
    SELECT 1 FROM profiles
    WHERE id = auth.uid() AND role = 'admin' AND is_active = true
  );
$$ LANGUAGE sql SECURITY DEFINER STABLE;

-- Profiles policies
CREATE POLICY "Users can view own profile" ON profiles FOR SELECT USING (auth.uid() = id OR is_admin());
CREATE POLICY "Users can update own profile" ON profiles FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Admins can manage profiles" ON profiles FOR ALL USING (is_admin());

-- Categories: public read, admin write
CREATE POLICY "Anyone can view active categories" ON categories FOR SELECT USING (is_active = true OR is_admin());
CREATE POLICY "Admins manage categories" ON categories FOR ALL USING (is_admin());

-- Resources: public read active, admin write
CREATE POLICY "Anyone can view active resources" ON resources FOR SELECT USING (status = 'active' OR is_admin());
CREATE POLICY "Admins manage resources" ON resources FOR ALL USING (is_admin());

-- Saved resources
CREATE POLICY "Users manage own saves" ON saved_resources FOR ALL USING (auth.uid() = user_id);

-- Resource views
CREATE POLICY "Anyone can log views" ON resource_views FOR INSERT WITH CHECK (true);
CREATE POLICY "Users view own history" ON resource_views FOR SELECT USING (auth.uid() = user_id OR is_admin());

-- CMS
CREATE POLICY "Public read published pages" ON cms_pages FOR SELECT USING (status = 'published' OR is_admin());
CREATE POLICY "Admins manage pages" ON cms_pages FOR ALL USING (is_admin());

CREATE POLICY "Public read published announcements" ON announcements FOR SELECT USING (status = 'published' OR is_admin());
CREATE POLICY "Admins manage announcements" ON announcements FOR ALL USING (is_admin());

CREATE POLICY "Public read active faqs" ON faqs FOR SELECT USING (is_active = true OR is_admin());
CREATE POLICY "Admins manage faqs" ON faqs FOR ALL USING (is_admin());

CREATE POLICY "Public read homepage content" ON homepage_content FOR SELECT USING (true);
CREATE POLICY "Admins manage homepage content" ON homepage_content FOR ALL USING (is_admin());
