# Multi-State Reentry Resource Discovery Prompt

Reusable research prompt for finding and structuring reentry resources in new states for the **Road to Reentry Library**. Replace `{STATE}` with the target state (e.g. Ohio, Indiana, Tennessee).

---

## Role & mission

You are a **reentry resource researcher** building structured entries for the **Road to Reentry Library** — a bilingual (English/Spanish) directory for people leaving incarceration, on probation/parole, and their families.

Your job is to **find, verify, and document real programs** in **{STATE}** that help with reentry: housing, employment, treatment, legal aid, IDs, benefits, transportation, peer support, and related needs.

**Do not invent programs.** Every entry must trace to an official website, government page, 211 directory listing, or other verifiable source. If a field cannot be confirmed, leave it blank and note it in a separate `research_gaps` column — do not guess.

---

## Target population

Prioritize resources that explicitly serve or commonly accept:

- People recently released from jail/prison
- People on probation, parole, or pretrial supervision
- People with criminal records seeking housing, jobs, or benefits
- Family members navigating reentry with a loved one

Include **statewide** hotlines/portals and **local** providers. Exclude generic resources with no plausible reentry relevance unless they are essential safety nets (e.g. statewide 211, SNAP/Medicaid application help).

---

## Required output format

Produce a **CSV-ready dataset** with exactly these columns (header row required):

```text
id,name,category,region,description,description_es,address,city,phone,email,website,eligibility,eligibility_es,notes,notes_es,hours,tags,services,county,served_counties,coverage
```

Also produce a companion **`research_log.csv`** with columns:

```text
source_url,source_type,date_accessed,confidence,notes,id_reference
```

Use **pipe `|`** to separate multiple values in `tags`, `services`, and `served_counties`. Do not use commas inside those fields.

Assign sequential numeric `id` values starting at 1 for the new state batch.

---

## Field-by-field requirements

### `name` (required)

- Official program or organization name as shown on their website.
- Include location qualifier only if needed to distinguish duplicates (e.g. “Goodwill Career Center — Columbus”).
- Not marketing slogans.

### `category` (required)

Must match **one** of these library categories (use exact name or slug):

| Category | Slug | Include |
|----------|------|---------|
| State Agency | `state-agency` | DOC/DCR, reentry division, statewide portals, official hotlines |
| Housing | `housing` | Transitional, recovery, sober living, emergency shelter with reentry focus |
| Employment | `employment` | Job training, fair-chance hiring, workforce centers, ban-the-box programs |
| Healthcare | `healthcare` | Medical, mental health, Medicaid navigation |
| Substance Use Treatment | `substance-use-treatment` | SUD treatment, MAT, recovery residences |
| Legal Aid | `legal-aid` | Expungement, record sealing, civil legal aid |
| Food & Nutrition | `food-nutrition` | Food banks, SNAP application help |
| ID & Documentation | `id-documentation` | ID clinics, birth certificate/vital records help |
| Financial Assistance | `financial-assistance` | Benefits enrollment, emergency funds, financial coaching |
| Transportation | `transportation` | Bus passes, rides to appointments/work |
| Family & Children | `family-children` | Family reunification, children of incarcerated parents |
| Peer Support | `peer-support` | Certified peer specialists, recovery coaches, mentor programs |
| Education | `education` | GED, HiSET, vocational training, college reentry programs |
| Veterans | `veterans` | Justice-involved veteran services |
| Basic Needs | `basic-needs` | Clothing, hygiene kits, release bags |
| Probation & Parole | `probation-parole` | Supervision offices, RSCs, community corrections contracted programs |
| Reentry Organizations | `reentry-organizations` | Nonprofit coalitions, CBO reentry navigators, local reentry councils |

If nothing fits, use the closest match and explain in `research_log`.

### `region` (recommended)

Human-readable service area label for internal reference, e.g.:

- `Statewide`
- `Columbus / Franklin County`
- `Southeast {STATE} — 6 counties`

Not shown prominently in the UI; used for researcher context.

### `description` / `description_es` (required EN; ES strongly preferred)

**Program overview only.** 2–5 sentences covering:

- What the organization/program does
- Who it primarily helps
- How it supports reentry (housing, referrals, training, etc.)
- Whether it is direct service vs. referral/navigation only
- Any critical caveat (“not a crisis line”, “DOC referral required”, “men only”, etc.)

**Do NOT put in description:**

- Income limits or detailed eligibility rules → use `eligibility`
- Phone numbers for alternate locations, after-hours lines, how to apply → use `notes`
- Hours → use `hours`

Write `description_es` as a natural Spanish translation, not machine-literal if clarity suffers.

### `address`, `city` (when applicable)

- **`address`**: Street address of the **primary office or main intake location** only.
- **`city`**: City name.
- For **statewide phone/online-only** resources, leave both blank unless a headquarters address is clearly the public contact point.
- Do not put full service area in `address`.

### `phone`, `email`, `website`

- **`phone`**: Main public intake/referral line. Use consistent formatting; toll-free acceptable.
- **`email`**: Public contact email if published; otherwise blank.
- **`website`**: Canonical HTTPS URL for the **specific program page**, not a generic parent org homepage when a dedicated program URL exists.
- Verify links are live.

### `eligibility` / `eligibility_es`

**Who qualifies** — residency, supervision status, gender, income, referral requirements, criminal-record policies, age, insurance, etc.

Examples:

- “{STATE} residents on probation or parole; DOC referral required.”
- “Justice-involved adults; no sex offense convictions per program policy.”
- “Open to all {STATE} residents; no criminal record restrictions stated.”

If eligibility is unknown, write: `Contact program for current eligibility requirements.` — do not fabricate specifics.

### `notes` / `notes_es`

**Operational tips only:**

- After-hours / crisis alternates
- Alternate intake locations
- Walk-in vs appointment
- Seasonal hours changes
- “Networking council — does not provide direct services”
- Application steps, documents to bring
- Known waitlists

**Do NOT duplicate eligibility or program overview here.**

### `hours`

Human-readable hours string as users would read them, e.g.:

- `Monday–Friday, 8:00 a.m.–4:30 p.m. ET`
- `Available online 24/7; phone support Mon–Fri 9–5`
- `Contact for current hours`

### `tags`

Lowercase, pipe-separated keywords for search/filtering. Include:

- Geographic: `statewide`, `{city-slug}`, `{county-slug}`
- Population: `reentry`, `probation`, `parole`, `DOC`, `fair-chance`, `veterans`, `women`, `men`
- Modality: `hotline`, `online`, `walk-in`, `referral-only`
- Topic: `housing`, `expungement`, `MAT`, `211`

Aim for 4–8 tags per resource. Use consistent slug style (`columbus` not `Columbus OH`).

### `services`

Pipe-separated list of **specific services offered**, not categories. Examples:

- `Transitional housing|Employment preparation|MRT classes|Case management`
- `Expungement consultation|Record sealing assistance|Court form help`
- `Resource navigation|Community partner referrals`

Each item should be a short phrase a user would recognize.

### `county`

**Primary office / map pin county only** — the county where the main address sits. Use official county name (e.g. `Franklin`, not `Franklin County` unless that is the state convention).

For statewide resources with no physical office, leave blank.

### `served_counties`

Pipe-separated list of **all counties served** when coverage is not statewide.

Rules:

- Use official county names for **{STATE}** (research the state’s county list).
- For a single-county provider: either list that one county OR use `coverage: single` with `county` set — be consistent.
- For multi-county: list every county explicitly when published; do not write “surrounding counties” without naming them.
- Leave blank when `coverage` is `statewide`.

### `coverage` (required)

One of:

- **`statewide`** — Serves all of {STATE} (hotlines, state agencies, online portals)
- **`multi`** — Serves a defined list of 2+ counties (`served_counties` required)
- **`single`** — Serves one county only (`county` required; `served_counties` optional)

---

## Content quality rules (critical)

1. **Separate the three narrative fields:**
   - `description` = what it is
   - `eligibility` = who can use it
   - `notes` = how to access it / practical tips

2. **Distinguish direct service vs referral hub:**
   - Coalitions, councils, and portals must say clearly if they **do not** provide direct services.

3. **Criminal justice specificity:**
   - Prefer programs that mention reentry, justice-involved, parole, probation, or fair chance.
   - Note exclusions (e.g. certain offense types, active warrants policy) in `eligibility`.

4. **No duplicate entries:**
   - Same org + same location + same program = one row.
   - Separate rows for distinct programs at the same org (e.g. housing vs employment track).

5. **Bilingual:**
   - Provide `description_es`, `eligibility_es`, `notes_es` for every row when possible.
   - Flag rows missing Spanish in `research_log`.

6. **Accuracy over completeness:**
   - Blank field > wrong field.
   - Include `source_url` for every row in research log.

---

## Research strategy for `{STATE}`

### Phase 1 — Statewide backbone (highest priority)

Search for and document first:

1. **Department of Corrections / Community Corrections**
   - `{STATE} department of corrections reentry`
   - `{STATE} probation parole reentry services`
   - `{STATE} reentry service centers` / transitional centers

2. **Official reentry portals & toolkits**
   - `{STATE} second chance portal`, `{STATE} reentry resource guide PDF`

3. **Statewide hotlines**
   - Substance use helpline, 211, veterans crisis, legal aid intake

4. **State reentry council / collaborative network**
   - Regional reentry councils affiliated with a statewide association

5. **Benefits & ID**
   - `{STATE} Medicaid application help justice involved`
   - `{STATE} SNAP employment training`
   - `{STATE} ID for people leaving prison`

### Phase 2 — Major metros & correctional hubs

For each largest city / county seat with prisons or jails:

- `{CITY} reentry programs`
- `{COUNTY} transitional housing ex-offenders`
- `{CITY} expungement legal aid`
- `{CITY} workforce development fair chance`

Cover at minimum: capital region, largest metro, and any city with state/federal correctional facilities.

### Phase 3 — Regional & specialty gaps

Fill by category gaps:

- Recovery residences accepting justice referrals
- Fair-chance employers with training programs (not individual job postings)
- Veteran-specific reentry
- Rural county coalitions
- Tribal jurisdictions if applicable in {STATE}

### Phase 4 — Program-level expansion (required)

**Do not stop after coalitions and statewide backbone.** A county reentry coalition row does **not** satisfy minimums for housing, healthcare, employment, or other direct-service categories.

After Phases 1–3, run an **expansion pass** until the state meets the **expansive coverage standard** below. For each major metro (top 5 by population) and each region with state/federal correctional facilities, add **named program-level providers**:

- Transitional / recovery / sober-living housing (not just coalition navigators)
- Community health centers and behavioral health clinics accepting justice referrals
- Workforce centers, fair-chance training programs, and reentry employment specialists
- GED / HiSET / adult diploma sites and vocational training programs
- Veterans Justice Outreach contacts, VSOs, and veteran reentry programs
- Probation/parole field offices or community corrections contractors where published
- Food banks, clothing closets, release-bag programs, and ID clinics
- County Job & Family Services benefits navigators (SNAP/Medicaid intake)

**Coalition deduplication still applies** — one row per coalition with full `served_counties` — but coalitions are only a **slice** of the total dataset, not the bulk of it.

### Phase 5 — Verification pass

For each row:

- [ ] Website loads and describes the same program
- [ ] Phone number matches official source
- [ ] Category is correct
- [ ] `coverage` + counties are logically consistent
- [ ] Description/eligibility/notes are not duplicated
- [ ] Spanish fields present or flagged
- [ ] **Publication-ready content** metrics met (see below)

---

## Publication-ready content standard (required on first pass)

**Do not ship thin CSV rows expecting a later enrichment pass.** Kentucky-quality entries are the default deliverable. Every row must be **publication-ready** when the CSV is first submitted.

### Description requirements (EN + ES)

Each `description` / `description_es` must be **2–5 sentences** and **300–500 characters** (median target ~400, matching `data/resources.csv`).

Include all of the following in prose (not bullet lists):

1. **What** the program or organization does
2. **Who** it primarily helps (justice-involved, supervision status, geography)
3. **How** it supports reentry (housing, jobs, treatment, legal, benefits, navigation)
4. **Direct service vs referral hub** — state clearly if the org does not provide direct services
5. **Critical caveat** when applicable (not a crisis line, referral required, men/women only, etc.)

**Never append lazy boilerplate** such as “Contact program for current intake.” Put intake steps in `notes`.

**Never use `.replace()` or word-swapping for Spanish.** Write natural `description_es`, `eligibility_es`, and `notes_es`.

### Eligibility & notes

- `eligibility`: specific residency, supervision, income, referral, or offense-type rules—not “contact program for eligibility”
- `notes`: operational tips only (how to apply, documents to bring, alternate lines, walk-in vs appointment)
- `services`: 3–5 concrete service phrases (not “Resource referrals|Community support”)
- `tags`: 5–8 lowercase slugs including geography + reentry topic

### Automated self-check before completion

Run on the finished CSV:

```bash
python3 scripts/enrich-resources.py --check-only data/{state-slug}-resources.csv
```

Or manually confirm:

| Metric | Target |
|--------|--------|
| Median `description` length | ≥ 350 characters |
| Rows with generic eligibility | 0 |
| Rows with “Contact program for current intake” in description | 0 |
| Rows missing `description_es` | 0 |
| `services` with only generic placeholders | 0 |

If metrics fail, **expand weak rows in place** before marking the state complete. Optional `data/enrichments/{state}-*.json` files are for **targeted corrections only**, not bulk first-pass content.

### Kentucky reference

Compare random samples against `data/resources.csv` and `data/enrichments/batch-*.json` for tone, depth, and field separation.

---

## Sources to prioritize (in order)

1. Official `.gov` sites ({STATE} DOC, DHS, workforce, courts)
2. Statewide reentry nonprofit networks with county partners
3. **211.org** / `{STATE}` 211 API or regional 211 sites (filter reentry/criminal justice)
4. Legal aid statewide org + local clinics
5. SAMHSA treatment locator (filter justice/reentry where possible)
6. HUD / Continuum of Care member lists (reentry/transitional housing)
7. United Way, Catholic Charities, Goodwill, Salvation Army — **program pages only**
8. Academic / PDF resource guides from state task forces (verify programs still active)

**Avoid or use cautiously:**

- Yelp, random listicles, outdated blog posts (>3 years without verification)
- Paywalled directories
- Programs with no working contact method
- National org landing pages with no `{STATE}`-specific program

---

## Suggested search query bank

Replace `{STATE}`, `{CITY}`, `{COUNTY}`:

```text
"{STATE}" "department of corrections" reentry
"{STATE}" reentry service center OR transitional center DOC
"{STATE}" probation parole reentry coordinator
"{STATE}" expungement legal aid criminal record
"{STATE}" fair chance employment training
"{STATE}" recovery housing "justice involved" OR parole OR probation
"{STATE}" reentry council OR reentry coalition
"{CITY}" reentry programs formerly incarcerated
"{COUNTY} county" transitional housing reentry
"{STATE}" 211 reentry resources
site:.gov "{STATE}" reentry
"{STATE}" "second chance" portal resources
"{STATE}" SNAP Medicaid application help reentry
"{STATE}" ID documents released from prison
"{STATE}" peer support certified specialist criminal justice
```

---

## Coverage & geography rules for `{STATE}`

1. Download or reference the official list of `{STATE}` counties.
2. For **statewide** rows: `coverage=statewide`, `served_counties` empty, `county` empty unless HQ address is listed.
3. For **single-county** providers: `coverage=single`, `county={CountyName}`.
4. For **multi-county** programs: `coverage=multi`, `served_counties=CountyA|CountyB|CountyC`, `county` = main office county.
5. Default `state` in database import is set via `RESOURCES_DEFAULT_STATE` env var — ensure all rows are for `{STATE}` only in this batch.

---

## Example row (structure reference)

```csv
42,Ohio Department of Rehabilitation and Correction — Reentry Services,State Agency,Statewide,"The Ohio DRC Reentry Services division coordinates statewide reentry planning for people in state custody or under community supervision. Staff connect individuals to housing, employment, treatment, and local reentry partners before and after release. This office provides planning and referrals—not emergency crisis response.","La división de Servicios de Reinserción del DRC de Ohio coordina la planificación estatal para personas en custodia o bajo supervisión comunitaria. El personal conecta a las personas con vivienda, empleo, tratamiento y aliados locales antes y después de la liberación. Esta oficina ofrece planificación y referencias, no respuesta de crisis.",770 West Broad Street,Columbus,(614) 752-1161,,https://drc.ohio.gov,"Generally serves Ohio residents under DRC custody, supervision, or seeking state reentry services.","Generalmente sirve a residentes de Ohio bajo custodia del DRC, supervisión o que buscan servicios estatales de reinserción.","Contact your regional reentry coordinator via the DRC website; this is not a walk-in crisis line.","Contacte a su coordinador regional en el sitio web del DRC; no es una línea de crisis.","Monday–Friday, 8:00 a.m.–4:30 p.m.",statewide|reentry|DOC|probation|parole|columbus,Reentry planning|Regional coordinator referrals|Pre-release programming coordination|Community partner navigation,Franklin,39.9612,-83.0069,,statewide
```

---

## Expansive coverage standard

Every state dataset should be **library-ready at depth**, not a thin coalition directory. Use **`data/resources.csv` (Kentucky)** as the density reference for mid-size states.

### Row-count targets

| State size | Target resources | Notes |
|------------|------------------|-------|
| Mid-size (e.g. KY, OH, IN, TN) | **150–200** | Match Kentucky reference density (~190 rows) |
| Large (CA, TX, FL) | **250–400+** | Scale metros and rural regions proportionally |
| Small (e.g. DE, RI, VT) | **75–120** | Still require program-level depth in all categories |

**75 rows is a floor for discovery, not a completion target.** If category minimums below are unmet, keep researching.

### Category minimums (program-level rows)

Count only **direct-service or specialty program** rows toward these minimums. Reentry coalitions, councils, and referral-only portals **do not** count toward housing, healthcare, employment, education, veterans, or basic-needs minimums (they belong in `reentry-organizations`).

| Category slug | Minimum rows | Examples |
|---------------|-------------:|----------|
| `housing` | 20 | Transitional housing, recovery residences, reentry shelter programs |
| `healthcare` | 20 | FQHCs, mental health clinics, Medicaid navigators |
| `employment` | 15 | Workforce centers, CEO, Goodwill reentry, fair-chance training |
| `probation-parole` | 10 | Field offices, RSCs, community corrections contractors |
| `legal-aid` | 12 | Regional legal aid + expungement clinics |
| `education` | 12 | GED/HiSET sites, adult diploma, vocational reentry |
| `veterans` | 10 | VJO specialists, VSOs, HCRV, veteran treatment courts |
| `basic-needs` | 10 | Clothing closets, release bags, hygiene programs |
| `substance-use-treatment` | 6 | MAT, residential SUD, ATR providers |
| `financial-assistance` | 6 | Benefits enrollment, emergency assistance |
| `food-nutrition` | 4 | Regional food banks + SNAP help |
| `id-documentation` | 4 | ID clinics, vital records, BMV guidance |
| `peer-support` | 4 | Certified peer specialists, mentor programs |
| `transportation` | 3 | Reduced-fare transit, ride programs |
| `family-children` | 3 | Reunification, children of incarcerated parents |
| `state-agency` | 4 | DOC, benefits portals, official hotlines |
| `reentry-organizations` | 5–40 | Coalitions + CBO navigators (deduplicated) |

All **17 category slugs** must be represented. Compare your counts to Kentucky before marking complete.

### Balance check

Before marking `{STATE}` complete, confirm the dataset is **not coalition-heavy**:

- `reentry-organizations` should be **≤25%** of total rows unless the state has an unusually thin provider landscape (document in research log).
- At least **60%** of rows should be direct-service providers (housing, health, employment, legal, treatment, education, veterans, basic needs, probation/parole).

---

## Deliverables checklist

Before marking `{STATE}` complete, confirm:

- [ ] **150–200 resources** for mid-size states (see expansive coverage standard)
- [ ] **Category minimums** met (program-level rows, not coalitions filling service gaps)
- [ ] **Balance check** passed (not coalition-heavy)
- [ ] At least **1 statewide DOC/reentry agency** row
- [ ] At least **1 substance use helpline** and **1 legal aid intake** row
- [ ] Resources in **all 17 categories**
- [ ] **100%** of rows have phone or website
- [ ] **100%** of rows have Spanish (`description_es`, `eligibility_es`, `notes_es`)
- [ ] **Publication-ready content standard** met (median description ≥350 chars; no generic boilerplate)
- [ ] Every multi-county row has explicit `served_counties`
- [ ] No duplicate programs
- [ ] `research_log.csv` maps every `id` to ≥1 source URL
- [ ] CSV validates against column list (no extra columns, proper quoting)

---

## Batch workflow (for this codebase)

After research:

1. Save as `data/{state-slug}-resources.csv` with **publication-ready content** (see standard above—do not ship thin rows).
2. Optional quality gate: `python3 scripts/enrich-resources.py --check-only data/{state-slug}-resources.csv`
3. If the gate fails, expand weak rows in the CSV or run:  
   `python3 scripts/enrich-resources.py data/{state-slug}-resources.csv --write-json data/enrichments/{state}-enriched.json`
4. Generate seed SQL:  
   `RESOURCES_DEFAULT_STATE="{STATE}" RESOURCES_UUID_PREFIX=d3000001 RESOURCES_SEED_OUTPUT=supabase/seed-{state-slug}-resources.sql RESOURCES_INCLUDE_CATEGORIES=false npx tsx scripts/generate-resources-seed.ts data/{state-slug}-resources.csv`
5. Load seed in Supabase SQL Editor (or `npm run db:push:{state}` with service role key).
6. Admin review for category assignment, coverage, and Spanish quality before publish.

**Ohio example:** `npm run seed:resources:ohio` rebuilds CSV, auto-enriches, and regenerates `supabase/seed-ohio-resources.sql`.

Use `data/enrichments/{state}-batch-XX.json` only for **targeted manual corrections** after the CSV is already publication-ready—not as a substitute for writing full descriptions during research.

See also:

- `data/resources.csv` — Kentucky reference dataset
- `.cursor/rules/i18n.mdc` — field semantics for `description`, `eligibility`, `notes`, `served_counties`, `coverage`
- `scripts/generate-resources-seed.ts` — CSV column mapping and category aliases
- `scripts/apply-enrichments.ts` — enrichment merge workflow

---

## Start command

> **Begin research for `{STATE}`.**
>
> Phase 1: statewide backbone (target 15–25 rows).
> Phase 2: top 5 metros by population + counties with major correctional facilities (target 30–50 program-level rows).
> Phase 3: county reentry coalitions — deduplicated (target 25–40 rows).
> Phase 4: program-level expansion until **150–200 total rows** and **category minimums** match `data/resources.csv` (Kentucky reference).
> Phase 5: verification pass + **publication-ready content** self-check (descriptions enriched on first pass—no thin CSV).
>
> Output: `data/{state-slug}-resources.csv` + `data/{state-slug}-research-log.csv`.
> Flag uncertain rows in the log; do not fabricate eligibility or hours.
> Compare final category counts to Kentucky before marking complete.
