-- Allow admins to read all saved resources for dashboard analytics
CREATE POLICY "Admins read all saves"
  ON saved_resources
  FOR SELECT
  USING (is_admin());
