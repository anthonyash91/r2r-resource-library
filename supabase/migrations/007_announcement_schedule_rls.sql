-- Hide expired or not-yet-started announcements from public reads.

DROP POLICY IF EXISTS "Public read published announcements" ON announcements;

CREATE POLICY "Public read published announcements" ON announcements
FOR SELECT USING (
  is_admin()
  OR (
    status = 'published'
    AND (starts_at IS NULL OR starts_at <= NOW())
    AND (ends_at IS NULL OR ends_at > NOW())
  )
);
