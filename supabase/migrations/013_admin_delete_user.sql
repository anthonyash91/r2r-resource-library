-- Hard-delete auth user when GoTrue deleteUser fails (e.g. leftover auth rows).
-- Child public data should already be removed by the API; this is a fallback.

CREATE OR REPLACE FUNCTION admin_delete_user_account(target_user_id UUID)
RETURNS VOID
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public, auth
AS $$
BEGIN
  IF EXISTS (
    SELECT 1 FROM public.profiles WHERE id = target_user_id AND role = 'admin'
  ) THEN
    RAISE EXCEPTION 'cannot_delete_admin';
  END IF;

  DELETE FROM public.saved_resources WHERE user_id = target_user_id;
  DELETE FROM public.resource_views WHERE user_id = target_user_id;
  DELETE FROM public.profiles WHERE id = target_user_id;
  DELETE FROM auth.users WHERE id = target_user_id;
END;
$$;

REVOKE ALL ON FUNCTION admin_delete_user_account(UUID) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION admin_delete_user_account(UUID) TO service_role;
