# Security surfaces

Reentry Resource Library — areas to review when changing auth, APIs, or data access.

## Auth & sessions

- Supabase Auth via `@supabase/ssr`; facility tablets use PIN + password.
- Facility entry: `/api/facility/enter` (middleware); site IDs encrypted at rest (`FACILITY_CRYPTO_SECRET`).
- Local dev requires `FACILITY_CRYPTO_SECRET` or explicit `ALLOW_DEV_FACILITY_CRYPTO=1` (non-production only).
- `SUPABASE_SERVICE_ROLE_KEY` is server-only — never expose as `NEXT_PUBLIC_*`.

## APIs to review on change

- `src/app/api/facility/*` — signup, reset, enter, verify-login
- `src/app/api/auth/*`
- `src/app/api/admin/*` — admin CRUD, user password reset
- `src/app/api/saved-resources/email-pdf`

## Data access

- Row Level Security on all Supabase tables; admin access via `is_admin()`.
- User preferences: `reentry_prefs` cookie; sync to `profiles` on login.

## Do not

- Log or persist raw facility site IDs or inmate PINs.
- Use service role key in client components or `NEXT_PUBLIC_*` env vars.
- Bypass RLS in user-facing routes without explicit admin checks.
