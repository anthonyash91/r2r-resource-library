# Minimal Reentry Resource Directory — AI Build Prompt

Use this prompt when asking an AI to build a **stripped-down version** of **Road to Reentry**: a searchable program directory backed by a database. Copy everything below the line into your AI session and fill in the bracketed placeholders.

---

## Prompt (copy from here)

You are building **Road to Reentry — MVP**, a web app that helps people coming home from incarceration find local reentry programs (housing, jobs, healthcare, legal aid, benefits, etc.).

Build **only the basic features** described below. Do **not** implement accounts, saved lists, admin portals, facility tablet auth, PDF email, onboarding wizards, pathways, CMS editors, analytics, or multi-state research pipelines unless explicitly listed here.

---

### Product goal

A **fast, accessible, mobile-first directory** where a user can:

1. Land on a simple homepage with a search box  
2. Search and filter programs in a database  
3. Open a program detail page with contact info and eligibility  
4. Understand that the site is a **directory**, not a service provider  

Target users: justice-involved adults, families, and reentry staff who need to **look up verified programs by location and need**.

---

### Scope: IN vs OUT

**Build these (MVP):**

| Feature | Requirement |
|--------|-------------|
| Homepage | Hero with search input; optional short “How it works” (3 bullets); link to `/resources` |
| Resource search (`/resources`) | Keyword search + filters; paginated or “load more” results; result cards |
| Resource detail (`/resources/[id]`) | Full program info, contact block, map/directions link, disclaimer |
| Categories | Fixed list of ~10–17 categories (seed data); filter by category slug |
| Location filters | State, county, city dropdowns (cascading where practical) |
| Coverage display | Show whether program is single-county, multi-county, or statewide |
| Bilingual UI shell | English + Spanish for **all UI chrome** (labels, buttons, errors). Resource body fields may be English-only in MVP if `description_es` is empty |
| Crisis bar | Thin persistent bar: 988 + Crisis Text Line links |
| Footer disclaimer | “Directory only — contact programs directly” (EN/ES) |
| Static pages | Minimal: About (1 paragraph), Privacy, Accessibility (short statements) |
| Database | PostgreSQL (Supabase or equivalent) with `categories` + `resources` tables |
| Seed data | Script or SQL to load at least **50 sample resources** for one state (e.g. Kentucky) |
| Mock mode | App runs with in-memory or JSON mock data when DB env vars are missing |

**Do NOT build (defer):**

- User signup / login / dashboard / saved resources  
- Facility tablet auth  
- Onboarding wizard / personalized recommendations  
- First-week pathways  
- Admin CRUD UI (data loaded via seed scripts only)  
- Email PDF, announcements, FAQ CMS, homepage CMS  
- ZIP geolocation / “nearby” radius search (optional stretch; state/county/city is enough)  
- View counts, analytics, featured rotation logic  
- Intake signal filters (stretch only if time permits)  
- US coverage map, marketing sections, case-worker CTA  

---

### Tech stack (required)

Use this stack unless the user specifies otherwise:

- **Next.js** (App Router) + **TypeScript**  
- **Tailwind CSS** for styling  
- **Supabase** (PostgreSQL + optional later auth)  
- Server Components for initial data fetch; client components only for interactive filters/search form  
- **Zod** for API/query validation  

Project conventions:

- `src/app/` — routes  
- `src/components/` — UI  
- `src/lib/data.ts` — single data-access module  
- `src/types/` — shared types  
- `src/i18n/messages/en.ts` and `es.ts` — all user-facing strings (no hardcoded English in components)  

---

### Data model

#### `categories`

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | PK |
| name | text | e.g. "Housing" |
| slug | text | unique, e.g. `housing` |
| description | text | optional |
| sort_order | int | display order |
| is_active | boolean | default true |

Seed at least: housing, healthcare, employment, legal-aid, financial-assistance, substance-use-treatment, food-nutrition, education, id-documentation, veterans.

#### `resources`

| Column | Type | Notes |
|--------|------|-------|
| id | uuid | PK |
| name | text | required |
| description | text | required; program overview only |
| description_es | text | optional |
| category_id | uuid | FK → categories |
| state | text | e.g. "Kentucky" |
| county | text | primary office county |
| city | text | |
| address | text | |
| phone | text | |
| email | text | |
| website | text | |
| hours | text | |
| eligibility | text | who qualifies |
| eligibility_es | text | optional |
| notes | text | how to apply, tips — not eligibility |
| notes_es | text | optional |
| served_counties | text[] | county names served; empty + statewide coverage = whole state |
| coverage | enum | `single` \| `multi` \| `statewide` |
| services | text[] | e.g. `{"SNAP enrollment","Job search"}` |
| tags | text[] | lowercase slugs |
| status | enum | `active` \| `archived` — only show `active` publicly |
| created_at, updated_at | timestamptz | |

**RLS:** Public read on `active` resources and active categories. No write policies for anonymous users in MVP.

---

### Search & filter behavior

**Search page (`/resources`)**

Query params (all optional):

- `q` — keyword (searches `name`, `description`, `city`, `county`, `tags`)  
- `state` — exact state name  
- `county` — matches `county` OR `served_counties` contains county OR `coverage = statewide` for that state  
- `city` — exact or ilike match on `city`  
- `category` — category slug  
- `page` — pagination (default 24 per page)  

**Filter UX:**

- Collapsible filter panel (collapsed on mobile by default)  
- **Apply on button press** — changing filters does not auto-search until user clicks “Search” (reduces jank)  
- Show active filter chips above results with clear-all  
- Empty state: friendly message + suggestion to broaden filters  

**Sort:** Default alphabetical by `name`. Optional: `newest` by `created_at`.

**Result card shows:** name, category badge, city/county, 2-line description truncate, phone if present, coverage badge (Local / Regional / Statewide).

**Detail page shows:**

- Name, category, coverage, location line  
- Description  
- Eligibility (if set)  
- Notes (if set) — labeled “Good to know” / operational tips  
- Contact: phone (click-to-call), email, website, address + “Get directions” (Google Maps link)  
- Counties served (if multi)  
- Disclaimer bar at bottom  
- Back link to search preserving query string  

---

### Pages & routes

| Route | Purpose |
|-------|---------|
| `/` | Homepage + search |
| `/resources` | Search results |
| `/resources/[id]` | Detail |
| `/about` | Static copy from i18n |
| `/privacy` | Static copy from i18n |
| `/accessibility` | Static copy from i18n |
| `/api/resources` | GET JSON list (same filters as page) for client refresh optional |

No `/login`, `/admin`, `/dashboard`, `/saved`, `/get-started`, `/facility/*`.

---

### Internationalization

- Cookie `reentry_locale`: `en` \| `es` (default `en`)  
- Header language switcher  
- All UI strings in `src/i18n/messages/en.ts` and `es.ts` with matching keys  
- Resource content: use `description_es`, `eligibility_es`, `notes_es` when locale is `es` and field is non-empty; else fall back to English  

---

### Accessibility & design

- Mobile-first; **18px base font**  
- Minimum **44px** touch targets on buttons and links  
- Skip-to-main-content link  
- Semantic headings, form labels, focus states  
- High contrast text; avoid low-contrast gray-on-gray  
- `prefers-reduced-motion`: disable scroll animations  
- Color is not the only indicator for category badges (include text)  

Visual tone: calm, trustworthy, plain language — not corporate SaaS. Purple/blue accent acceptable; prioritize readability over decoration.

---

### Environment variables

```env
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

When Supabase vars are missing, load `data/mock-resources.json` (or similar) so `npm run dev` works out of the box.

---

### Seed data format

Accept CSV import with columns aligned to the full project format (minimum subset):

```text
name,category,description,address,city,phone,website,eligibility,notes,hours,county,served_counties,coverage,state
```

Provide:

1. `supabase/migrations/001_mvp_schema.sql`  
2. `supabase/seed-categories.sql`  
3. `scripts/import-resources-csv.ts` or Python script to load CSV → DB  
4. `data/sample-kentucky-resources.csv` with **≥50 rows** across **≥10 counties** and **≥8 categories**  

---

### Definition of done

The MVP is complete when:

- [ ] `npm install && npm run dev` starts without errors (mock mode OK)  
- [ ] Homepage search navigates to `/resources?q=…`  
- [ ] Filters combine correctly (state + county + category + keyword)  
- [ ] Detail pages render for every seeded resource  
- [ ] Language switcher toggles UI strings EN ↔ ES  
- [ ] Lighthouse accessibility score ≥ 90 on `/resources` (best effort)  
- [ ] README documents setup, env vars, and how to import CSV seed data  
- [ ] No scope creep: no auth, no admin UI, no saved resources  

---

### Implementation order

1. Schema + seed categories  
2. Data layer (`getResources`, `getResourceById`, `queryResources(filters)`)  
3. `/resources` list with filters  
4. `/resources/[id]` detail  
5. Homepage wire-up  
6. i18n + language switcher  
7. Static pages + crisis bar + footer  
8. CSV import script + sample data  
9. README  

---

### Reference (optional)

If you have access to the full **Road to Reentry** repo, use it only as a **reference** for field semantics and coverage logic — do not copy admin, facility, or onboarding code. Key reference files:

- `src/types/index.ts` — Resource shape  
- `src/lib/resource-coverage.ts` — county matching rules  
- `.cursor/rules/i18n.mdc` — i18n rules  

---

### User overrides (fill before sending)

- **Primary state for seed data:** [e.g. Kentucky]  
- **Hosting target:** [e.g. Vercel + Supabase]  
- **Brand name:** [Road to Reentry / other]  
- **Stretch goals if time permits:** [e.g. ZIP search, intake signal badges]  

Build the MVP now. Ask clarifying questions only if a requirement above is ambiguous; otherwise use sensible defaults and document assumptions in the README.

---

## End of prompt

---

## How to use this prompt

1. Copy from **“You are building Road to Reentry — MVP”** through **“Build the MVP now.”**  
2. Fill in **User overrides** at the bottom.  
3. Attach `data/kentucky-resources.csv` (or a 50-row sample) if you want real seed data on day one.  
4. For a greenfield build, paste into a new repo; for extending this repo, add: *“Create a new branch `mvp-basic-search` and implement only the IN scope; do not modify existing admin or facility routes.”*

## Related docs

- Full product feature list: `docs/stakeholder-feature-overview.md`  
- Full data research format: `docs/prompts/multi-state-resource-research.md`  
- Full app README: `README.md`
