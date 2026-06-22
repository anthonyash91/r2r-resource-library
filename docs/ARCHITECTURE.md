# Reentry Resource Library — Architecture

## Overview

The Reentry Resource Library is a full-stack Next.js application with Supabase as the backend. It follows a **mobile-first, accessibility-first** design philosophy with a clear separation between public-facing resource discovery and admin content management.

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client (Browser)                        │
│  Next.js App Router · React 19 · Tailwind CSS               │
└─────────────────────────┬───────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
   Server Components  Client Components  Middleware
   (data fetching)    (auth, saves, UI)  (session refresh)
          │               │
          └───────┬───────┘
                  ▼
         ┌─────────────────┐
         │  Data Layer     │
         │  lib/data.ts    │
         └────────┬────────┘
                  │
        ┌─────────┴─────────┐
        ▼                   ▼
   Supabase Client     Mock Data Fallback
   (production)        (demo/dev)
        │
        ▼
┌───────────────────────────────────┐
│           Supabase                │
│  Auth · PostgreSQL · RLS · Storage│
└───────────────────────────────────┘
```

## Database Schema

### Core Tables

| Table | Purpose |
|-------|---------|
| `profiles` | User profiles extending `auth.users` with roles |
| `categories` | Editable resource categories (16 defaults) |
| `resources` | Full resource directory with geo, tags, services |
| `saved_resources` | User favorites |
| `resource_views` | View tracking for analytics & recently viewed |
| `cms_pages` | Informational pages (About, Privacy, etc.) |
| `announcements` | Homepage announcements |
| `faqs` | FAQ content |
| `homepage_content` | Key-value homepage CMS |

### Roles

- `user` — Default; can save resources, view dashboard
- `case_manager` — Future: manage client resource lists
- `admin` — Full admin portal access

### Row Level Security

- Public read on active resources, categories, published CMS
- Users manage own saved resources and view history
- Admins have full CRUD via `is_admin()` helper function

## User Flows

### Resource Discovery Flow

1. User lands on homepage → searches or browses categories
2. Applies filters (state, county, city, category, service)
3. Views resource detail → saves or shares
4. Returns via dashboard to saved/recently viewed

### Authentication Flow

1. Sign up → Supabase Auth creates user → trigger creates profile
2. Sign in → session cookie via `@supabase/ssr`
3. Demo mode → localStorage-based mock auth

### Admin Flow

1. Admin signs in (role = `admin`)
2. Accesses `/admin` sidebar navigation
3. Manages resources, categories, users, CMS content
4. Views analytics dashboard

## API Architecture

The application uses **Next.js Server Components** for data fetching rather than a separate REST API. Server-side functions in `lib/data.ts` query Supabase directly.

Future API routes can be added at `src/app/api/` for:
- Bulk import/export webhooks
- Mobile app endpoints
- AI recommendation service

## Search & Filtering

### Current Implementation

- Full-text search via PostgreSQL `tsvector` (Supabase)
- Filter by: keyword, state, county, city, category, service, eligibility, featured, recently added
- Mock mode: client-side filtering in `filterMockResources()`

### Future: Distance Search

Not planned. Resources are located by county and address text; distance-based sorting would require geocoding at query time rather than stored coordinates.


## Component Architecture

```
components/
├── ui/           # Primitives (Button, Input, Card, Badge, Select)
├── layout/       # Header, Footer (global navigation)
├── resources/    # Domain components (cards, filters, search)
└── admin/        # Admin-specific (sidebar, forms)
```

### Design Tokens

- Primary: `#2d6a6a` (calming teal)
- Background: `#f8f6f3` (warm off-white)
- Base font: 18px Source Sans 3
- Min touch target: 48px

## Security Considerations

1. **RLS** on all Supabase tables
2. **Admin routes** protected client-side (add server-side check for production)
3. **Service role key** only on server, never exposed to client
4. **Auth middleware** refreshes sessions on every request

## Deployment Plan

### Recommended: Vercel + Supabase

1. Deploy Next.js to Vercel
2. Set environment variables
3. Configure Supabase Auth redirect URLs
4. Run database migrations
5. Create admin user

### Environment Variables

```
NEXT_PUBLIC_SUPABASE_URL
NEXT_PUBLIC_SUPABASE_ANON_KEY
SUPABASE_SERVICE_ROLE_KEY  (server only)
NEXT_PUBLIC_APP_URL
```

## Future Expansion Roadmap

| Feature | Schema Ready | Notes |
|---------|-------------|-------|
| AI recommendations | ✅ | `resource_views`, `saved_resources` for training data |
| Case manager accounts | ✅ | `case_manager` role, `facility_id` |
| Facility libraries | ✅ | `facility_id` on profiles |
| Multilingual | ⬜ | Add `locale` column to CMS tables |
| Mobile app | ✅ | Supabase REST/Realtime APIs |
| Offline access | ⬜ | Service worker + IndexedDB sync |
| Messaging | ⬜ | New `messages` table needed |
| Certificate programs | ⬜ | New `programs` table needed |

## Performance

- Server Components for initial data (no client JS for static content)
- Suspense boundaries on filter bar
- Database indexes on search columns
- GIN indexes for full-text and array searches
