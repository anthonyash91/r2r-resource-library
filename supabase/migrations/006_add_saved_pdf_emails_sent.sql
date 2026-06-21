-- Track how many saved-resources PDF emails each user has sent (limit enforced in app + RPC).

ALTER TABLE profiles
  ADD COLUMN IF NOT EXISTS saved_pdf_emails_sent INTEGER NOT NULL DEFAULT 0;

ALTER TABLE profiles
  DROP CONSTRAINT IF EXISTS profiles_saved_pdf_emails_sent_check;

ALTER TABLE profiles
  ADD CONSTRAINT profiles_saved_pdf_emails_sent_check
  CHECK (saved_pdf_emails_sent >= 0);

CREATE OR REPLACE FUNCTION increment_saved_pdf_email_send(p_limit INTEGER DEFAULT 3)
RETURNS INTEGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  new_count INTEGER;
BEGIN
  IF auth.uid() IS NULL THEN
    RETURN NULL;
  END IF;

  UPDATE profiles
  SET saved_pdf_emails_sent = saved_pdf_emails_sent + 1
  WHERE id = auth.uid()
    AND saved_pdf_emails_sent < p_limit
  RETURNING saved_pdf_emails_sent INTO new_count;

  RETURN new_count;
END;
$$;

CREATE OR REPLACE FUNCTION decrement_saved_pdf_email_send()
RETURNS INTEGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  new_count INTEGER;
BEGIN
  IF auth.uid() IS NULL THEN
    RETURN NULL;
  END IF;

  UPDATE profiles
  SET saved_pdf_emails_sent = GREATEST(saved_pdf_emails_sent - 1, 0)
  WHERE id = auth.uid()
  RETURNING saved_pdf_emails_sent INTO new_count;

  RETURN new_count;
END;
$$;

GRANT EXECUTE ON FUNCTION increment_saved_pdf_email_send(INTEGER) TO authenticated;
GRANT EXECUTE ON FUNCTION decrement_saved_pdf_email_send() TO authenticated;
