# Reentry Resource Library

A modern, accessible web application helping incarcerated and formerly incarcerated individuals find local, state, and national reentry resources.

## Features

- **Resource Directory** — Searchable database with 16 categories, filtering by location, service type, and eligibility
- **Save Resources** — Personal saved list with dashboard
- **User Dashboard** — Saved resources, recently viewed, and recommendations
- **Admin Portal** — Resource, category, user, and CMS management with analytics
- **Accessibility** — WCAG-oriented design with large touch targets, keyboard navigation, skip links, and plain language

Requires a configured **Supabase** project for authentication and data.

## Tech Stack

- **Next.js 16** (App Router) + **TypeScript**
- **Tailwind CSS 4**
- **Supabase** (Auth, PostgreSQL, Row Level Security)
- **Lucide React** icons

## Quick Start

```bash
npm install
npm run dev
```

Open [http://localhost:8080](http://localhost:8080).

### Setup (Supabase required)

1. Create a [Supabase](https://supabase.com) project
2. Copy `.env.example` to `.env.local` and add your project URL and anon key
3. Run migrations in the Supabase SQL Editor:

   ```
   supabase/migrations/001_initial_schema.sql
   supabase/migrations/002_add_description_es.sql
   supabase/migrations/004_add_eligibility_es_and_notes.sql
   supabase/migrations/005_add_served_counties.sql
   supabase/migrations/003_fix_profile_signup_trigger.sql
   ```

4. Load resources:

   ```bash
   npm run seed:resources          # generates supabase/seed-resources.sql
   npm run seed:resources:ohio     # generates supabase/seed-ohio-resources.sql
   ```

   Run both SQL files in the Supabase SQL Editor (Kentucky first, then Ohio).

   Or add `SUPABASE_SERVICE_ROLE_KEY` to `.env.local` and run `npm run db:push:ohio`.

5. Create an admin user in Supabase Auth, then:

   ```sql
   UPDATE profiles SET role = 'admin' WHERE email = 'your-admin@email.com';
   ```

6. Build and deploy:

   ```bash
   npm run build
   npm start
   ```

### Email saved resources (PDF)

To let signed-in users email a PDF of their saved resources, configure [Resend](https://resend.com):

```bash
RESEND_API_KEY=re_xxxxxxxx
EMAIL_FROM="Reentry Resource Library <noreply@yourdomain.com>"
```

- `EMAIL_FROM` must use a domain verified in Resend.
- Without `RESEND_API_KEY` / `EMAIL_FROM`, the **Email PDF** button shows a not-configured message when clicked.

## Project Structure

```
src/
├── app/                    # Next.js App Router pages
│   ├── admin/              # Admin portal
│   ├── dashboard/          # User dashboard
│   ├── resources/          # Directory & detail pages
│   ├── saved/              # Saved resources
│   ├── login/ signup/      # Authentication
│   └── faq/ about/         # CMS-driven pages
├── components/
│   ├── admin/              # Admin UI
│   ├── layout/             # Header, footer
│   ├── resources/          # Resource cards, filters, search
│   └── ui/                 # Accessible UI primitives
├── lib/
│   ├── data.ts             # Data access layer (Supabase + mock fallback)
│   ├── mock-data.ts        # Demo data
│   └── supabase/           # Supabase clients
└── types/                  # TypeScript definitions
supabase/
├── migrations/             # Database schema
└── seed.sql                # Seed data
docs/
└── ARCHITECTURE.md         # Full architecture documentation
```

## Navigation

| Route | Description |
|-------|-------------|
| `/` | Homepage with search, categories, featured resources |
| `/resources` | Searchable resource directory |
| `/resources/[id]` | Resource detail page |
| `/saved` | Saved resources |
| `/dashboard` | User dashboard |
| `/admin` | Admin analytics dashboard |
| `/admin/resources` | Resource management |
| `/admin/categories` | Category management |
| `/admin/users` | User management |
| `/admin/cms` | Content pages |
| `/admin/announcements` | Announcements |
| `/admin/faqs` | FAQ management |
| `/admin/homepage` | Homepage content editor |

## Accessibility

- 18px base font size with high-contrast palette
- Minimum 44–48px touch targets
- Skip-to-content link
- Semantic HTML with ARIA labels
- Keyboard-navigable accordions and menus
- `prefers-reduced-motion` support

## Future Expansion

The database schema supports future features including:

- AI-powered recommendations (`latitude`/`longitude` for distance search)
- Case manager accounts (`case_manager` role)
- Facility-specific libraries (`facility_id` on profiles)
- Multilingual content
- Offline access and mobile apps

## License

Private — for reentry program use.
