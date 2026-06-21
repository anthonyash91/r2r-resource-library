# Reentry Resource Library

A modern, accessible web application helping incarcerated and formerly incarcerated individuals find local, state, and national reentry resources.

## Features

- **Resource Directory** — Searchable database with 16 categories, filtering by location, service type, and eligibility
- **Save Resources** — Personal saved list with dashboard
- **User Dashboard** — Saved resources, recently viewed, and recommendations
- **Admin Portal** — Resource, category, user, and CMS management with analytics
- **Accessibility** — WCAG-oriented design with large touch targets, keyboard navigation, skip links, and plain language
- **Demo Mode** — Runs locally without Supabase using built-in sample data

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

### Demo Mode (no Supabase)

The app loads **20 verified Kentucky reentry resources** in demo mode. Edit `src/lib/kentucky/` and run `npx tsx scripts/generate-kentucky-seed.ts` to refresh `supabase/seed-kentucky.sql` for Supabase.

- **Sign in**: any email/password (include `admin` in email for admin access)
- **Admin portal**: `/admin`

To reset a Supabase database, run `supabase/reset-data.sql` in the SQL Editor. In demo mode, clear browser localStorage key `reentry_featured_resources` if you pinned featured items previously.

### Production Setup (Supabase)

1. Create a [Supabase](https://supabase.com) project
2. Copy `.env.example` to `.env.local` and add your keys
3. Run the migration in Supabase SQL Editor:

   ```
   supabase/migrations/001_initial_schema.sql
   ```

   Optional: run `supabase/seed.sql` (empty by default) or add content via `/admin`.

   To wipe content later: `supabase/reset-data.sql`

4. Create an admin user in Supabase Auth, then:

   ```sql
   UPDATE profiles SET role = 'admin' WHERE email = 'your-admin@email.com';
   ```

5. Build and deploy:

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
- Without these variables, the **Email PDF** button shows a not-configured message when clicked.
- In demo mode (no Supabase), email export is unavailable.

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
