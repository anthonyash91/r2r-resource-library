# Road to Reentry — Feature Overview

**Document purpose:** Stakeholder summary of product capabilities  
**Product:** Road to Reentry (Reentry Resource Library)  
**Last updated:** July 2026  
**Audience:** Funders, partners, correctional stakeholders, program administrators, and community leaders

---

## Executive summary

Road to Reentry is a **free, bilingual (English / Spanish) web directory** that helps people coming home from incarceration—and the people who support them—find verified housing, jobs, healthcare, legal aid, benefits, and other reentry programs **filtered by where they live and what they need most**.

The platform is built for **clarity under stress**: plain language, large touch targets, mobile-first design, and accessibility patterns aligned with WCAG goals. It is a **directory and navigation tool**, not a benefits office or crisis line—users are always directed to real programs for services.

**Current scale:** 16 U.S. states live in the directory, **4,700+** curated program records, **17** service categories, county-level coverage with statewide backbone programs in every deployed state.

---

## Who the platform serves

| Audience | How they use Road to Reentry |
|----------|------------------------------|
| **People reentering the community** | Search and filter programs, complete a short personalization flow, save favorites, follow a first-week guide, email themselves a PDF resource list |
| **Family members and supporters** | Browse anonymously or create an account to build and share a resource list |
| **Reentry staff and case managers** | Point clients to vetted programs; dedicated case-management tools are on the product roadmap (see *Future capabilities*) |
| **Correctional facilities (tablets)** | Facility-scoped accounts via a bookmarked entry URL; one account per facility PIN; session timeouts for shared devices |
| **Program administrators** | Full admin portal to manage resources, categories, public content, facilities, users, and basic analytics—without redeploying code |

---

## Core capabilities

### 1. Program directory and search

- **Search by keyword** — Housing, jobs, healthcare, legal help, benefits, and more
- **Search by ZIP code** — Find programs in or near a ZIP, with results grouped for clarity
- **Filter by location** — State, county, and city
- **Filter by need** — 17 program categories (housing, employment, healthcare, legal aid, financial assistance, substance use treatment, probation/parole, food/nutrition, education, veterans, basic needs, ID/documentation, peer support, transportation, family/children, state agencies, reentry organizations)
- **Filter by coverage** — Local, multi-county/regional, or statewide programs
- **Practical intake filters** — e.g. programs that accept people with a criminal record, walk-in availability, referral requirements
- **Personalized results** — After a short onboarding flow, users see programs matched to their state, county, and top priorities

### 2. Program detail pages

Each listing includes:

- Program overview, who qualifies, and operational tips (hours, how to apply, what to bring)
- Full **English and Spanish** content where available
- Phone, email, website, and address with **directions**
- Counties served and coverage type
- Badges for category and intake signals (e.g. criminal-record friendly, walk-in OK)
- **Save** and **share** options
- Related programs and a clear disclaimer that Road to Reentry is a directory, not the service provider

### 3. Personalization (“Get started”)

A **3-step guided flow** (skippable):

1. Choose state  
2. Choose county  
3. Pick up to three priority needs  

Preferences drive **“Picked for you”** recommendations on the homepage and resource search. Signed-in users can update preferences anytime from the dashboard.

### 4. First-week reentry guide

A structured **first-week pathway** walks users through urgent steps after release—crisis support, ID, benefits, housing, treatment, employment—with matched programs for each step based on their location and priorities.

### 5. Accounts and dashboard

**Standard accounts** (email + password):

- **Saved resources** — Private list of programs to revisit
- **Dashboard** — Location and priority summary, saved programs, personalized recommendations, recently viewed programs
- **Email PDF** — Send a formatted PDF of saved programs to an email address (useful for court, parole, or family planning)

**Anonymous use** — Full search and browse without an account; preferences stored in the browser until the user signs up.

### 6. Facility / tablet mode

Designed for **jails and facilities** that issue shared tablets:

- Admin registers each facility with a unique site ID and PIN
- Tablets bookmark a facility entry URL; inmates create **one account per PIN**
- Password reset via security questions (no personal email required for core flows)
- **Inactivity timeout** and session reminders for shared-device safety
- Optional contact email for PDF delivery on facility accounts

### 7. Homepage and trust features

- Hero search and browse-by-category entry points
- **Interactive U.S. map** showing live vs. upcoming states
- Featured and personalized program highlights
- “How it works” and service category overview
- **Crisis bar** — Persistent links to **988** and Crisis Text Line
- **Library disclaimer** — Clear messaging that the site connects users to programs; it does not provide cash, housing placement, or legal representation directly
- Scheduled **announcements** for time-sensitive public messages

### 8. Public information pages

Editable content (no code deploy required):

- About Us  
- Contact (including inquiry form)  
- FAQ (searchable, grouped by topic)  
- Privacy Policy  
- Terms of Use  
- Accessibility Statement  

All public pages available in **English and Spanish**.

---

## Geography and data quality

### States currently in the directory

| State | State | State | State |
|-------|-------|-------|-------|
| Alabama | Georgia | North Carolina | Tennessee |
| Arizona | Illinois | Ohio | Virginia |
| Florida | Indiana | South Carolina | West Virginia |
| Kentucky | Michigan | Wisconsin | Mississippi |

### Data standards (behind the scenes)

Stakeholders should know that program data is maintained through a structured research and quality pipeline:

- County-level coverage targets (pin every county; depth across core need categories)
- Research logs with source URLs and confidence ratings for every record
- Bilingual fields for descriptions, eligibility, and operational notes
- County benefits offices synced from official government directories where applicable
- Admin review, archive, and featured-program controls

---

## Accessibility and inclusion

- **Bilingual** — Full UI and content localization (EN/ES)
- **Mobile-first** — Large text and touch targets for use on phones and tablets
- **Accessibility-oriented design** — Skip links, semantic structure, keyboard navigation, reduced-motion support
- **Plain language** — Written for people under stress, not for specialists
- **Dedicated accessibility statement** — Public, CMS-editable

---

## Administration (for program operators)

Authorized administrators access a secure portal to:

| Function | What admins can do |
|----------|-------------------|
| **Analytics** | View total programs, active/featured counts, most viewed and most saved resources |
| **Resources** | Add, edit, archive, and feature programs; manage English/Spanish copy, counties served, coverage, and intake signals |
| **Categories** | Manage the 17 service categories (icons, order) |
| **Facilities** | Register correctional facilities for tablet access; view signup activity |
| **Users** | View accounts, reset passwords, remove users, see saved-resource activity |
| **Content** | Edit homepage hero, About, Contact, legal pages, FAQs, and announcements |
| **Translation assist** | Optional auto-translate of English admin content to Spanish (when configured) |

---

## Technology summary (non-technical)

| Area | Approach |
|------|----------|
| **Platform** | Modern web application (works in any browser; no app store install) |
| **Hosting & data** | Cloud database with row-level security; user data isolated per account |
| **Email** | Transactional email for saved-resource PDFs |
| **Offline demo** | Can run in demonstration mode without live database for trainings |

---

## Future capabilities (roadmap signals)

These items are referenced in product planning but are **not fully productized today**:

- **Case manager workspace** — Caseload tracking, referral sending, and pre-release planning (schema and marketing placeholders exist; full workflow pending)
- **Additional states** — Registry and map support expansion; research pipeline is repeatable per state
- **Deeper facility integrations** — Potential ties to facility case management or discharge planning systems

---

## Feature checklist (at a glance)

| Capability | Available |
|------------|-----------|
| Multi-state program directory (16 states) | Yes |
| English / Spanish | Yes |
| Keyword and ZIP search | Yes |
| State / county / city filters | Yes |
| Category and intake-signal filters | Yes |
| Personalized recommendations | Yes |
| Onboarding wizard | Yes |
| First-week pathway guide | Yes |
| Program detail with directions & share | Yes |
| Save programs | Yes (account) |
| Email saved list as PDF | Yes (account) |
| User dashboard | Yes |
| Standard sign-up / sign-in | Yes |
| Facility tablet accounts | Yes |
| Facility password reset (security questions) | Yes |
| Crisis resources (988) in site chrome | Yes |
| Homepage U.S. coverage map | Yes |
| Featured programs | Yes |
| Public CMS pages (About, FAQ, legal, etc.) | Yes |
| Admin resource management | Yes |
| Admin analytics (views / saves) | Yes |
| Admin facility registry | Yes |
| Admin user management | Yes |
| Case manager caseload tools | Planned |
| Native mobile app | No (web only) |

---

## Suggested uses in stakeholder conversations

- **Legislators / funders** — Emphasize geographic coverage, bilingual access, facility tablet mode, and data quality pipeline  
- **Corrections partners** — Emphasize facility auth, inactivity guard, PIN-bound accounts, first-week guide, PDF export for discharge planning  
- **Community-based orgs** — Emphasize accurate listings, intake signals, “get listed” pathway via Contact, admin self-service updates  
- **Healthcare / workforce / legal networks** — Emphasize category depth, county coverage, and referral-friendly share/save flows  

---

## Contact and demo

- **Live demo:** Run locally or deployed instance (see project `README.md` for setup)  
- **List a program / partner inquiry:** Public Contact page (`/contact`)  
- **Technical documentation:** `README.md`, `docs/ARCHITECTURE.md` (maintainer-facing)

---

*Road to Reentry is a program directory. For emergencies, users are directed to 988 and local crisis lines. Program eligibility and availability are determined by each listed organization.*
