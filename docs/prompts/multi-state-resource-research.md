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

**Geographic priority:** Many users are released from **county jails in smaller, rural counties**—not only state prisons near major cities. Research must produce **county-level local depth** (Phase 3b), not metro-only coverage with statewide backfill.

---

## Required output format

Produce a **CSV-ready dataset** saved as `data/{state-slug}-resources.csv` with exactly these columns (header row required). All states use this pattern—including Kentucky (`kentucky-resources.csv`, not `resources.csv`).

```text
id,name,category,region,description,description_es,address,city,phone,email,website,eligibility,eligibility_es,notes,notes_es,hours,tags,services,county,served_counties,coverage
```

Do **not** add an `intake_signals` column during research. After the CSV is saved, the enrichment script auto-tags each row (`accepts_criminal_record`, `referral_required`, `walk_in_ok`) from `eligibility`, `notes`, and description text. Write those fields clearly so tagging is accurate (e.g. “DOC referral required”, “walk-in clinic”, “justice-involved adults”).

Also produce a companion **`data/{state-slug}-research-log.csv`** with columns:

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


| Category                | Slug                      | Include                                                                    |
| ----------------------- | ------------------------- | -------------------------------------------------------------------------- |
| State Agency            | `state-agency`            | DOC/DCR, reentry division, statewide portals, official hotlines            |
| Housing                 | `housing`                 | Transitional, recovery, sober living, emergency shelter with reentry focus |
| Employment              | `employment`              | Job training, fair-chance hiring, workforce centers, ban-the-box programs  |
| Healthcare              | `healthcare`              | Medical, mental health, Medicaid navigation                                |
| Substance Use Treatment | `substance-use-treatment` | SUD treatment, MAT, recovery residences                                    |
| Legal Aid               | `legal-aid`               | Expungement, record sealing, civil legal aid                               |
| Food & Nutrition        | `food-nutrition`          | Food banks, SNAP application help                                          |
| ID & Documentation      | `id-documentation`        | ID clinics, birth certificate/vital records help                           |
| Financial Assistance    | `financial-assistance`    | Benefits enrollment, emergency funds, financial coaching                   |
| Transportation          | `transportation`          | Bus passes, rides to appointments/work                                     |
| Family & Children       | `family-children`         | Family reunification, children of incarcerated parents                     |
| Peer Support            | `peer-support`            | Certified peer specialists, recovery coaches, mentor programs              |
| Education               | `education`               | GED, HiSET, vocational training, college reentry programs                  |
| Veterans                | `veterans`                | Justice-involved veteran services                                          |
| Basic Needs             | `basic-needs`             | Clothing, hygiene kits, release bags                                       |
| Probation & Parole      | `probation-parole`        | Supervision offices, RSCs, community corrections contracted programs       |
| Reentry Organizations   | `reentry-organizations`   | Nonprofit coalitions, CBO reentry navigators, local reentry councils       |


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

- `**address`**: Street address of the **primary office or main intake location** only.
- `**city`**: City name.
- For **statewide phone/online-only** resources, leave both blank unless a headquarters address is clearly the public contact point.
- Do not put full service area in `address`.

### `phone`, `email`, `website`

- `**phone`**: Main public intake/referral line. Use consistent formatting; toll-free acceptable.
- `**email**`: Public contact email if published; otherwise blank.
- `**website**`: Canonical HTTPS URL for the **specific program page**, not a generic parent org homepage when a dedicated program URL exists.
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

- `**statewide`** — Serves all of {STATE} (hotlines, state agencies, online portals)
- `**multi**` — Serves a defined list of 2+ counties (`served_counties` required)
- `**single**` — Serves one county only (`county` required; `served_counties` optional)

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

### Phase 3b — Small-county depth (required)

**Many jails and release points are in smaller, rural counties—not just state capitals and top metros.** Metro-heavy research leaves users in those counties with only statewide hotlines. This phase is **mandatory** before marking a state complete.

**Goal:** Every county in `{STATE}` should have **actionable local coverage**—not inferred from a distant metro alone.

#### County coverage standard

After Phases 1–4, run a **gap-fill pass** against the official county list:

1. Build a checklist of all `{STATE}` counties.
2. For each county, mark it **covered** when at least one row meets **either**:
   - `coverage=single` with `county={CountyName}`, **or**
   - `coverage=multi` with the county listed in `served_counties`, **or**
   - A **direct-service** provider (housing, healthcare, employment, legal, food, probation/parole office, etc.) pinned to that county—not a referral-only coalition row alone.
3. **Statewide rows do not count** toward per-county coverage (they are baseline, not local depth).
4. **Target:** **≥90%** of counties covered; any uncovered county must be documented in `research_log` with reason (e.g. no published provider found after 211 + county JFS + sheriff search).

Compare against Kentucky (`data/kentucky-resources.csv`): mid-size states should touch **most counties**, with meaningful rows in rural/Appalachian counties—not only Jefferson/Fayette depth.

#### Per-county search (especially counties outside top 10 MSAs)

For each **uncovered** or **thin** county, search systematically:

- `{COUNTY} county jail reentry` / `{COUNTY} sheriff community corrections`
- `{COUNTY} county` probation parole field office
- `{COUNTY} county` DHS / Job and Family Services / benefits SNAP Medicaid
- `211 {COUNTY} county {STATE}` reentry housing employment
- `{COUNTY} county` food bank pantry
- `{COUNTY} county` community health center FQHC behavioral health
- `{COUNTY} county` American Job Center workforce
- `{COUNTY} county` transitional housing homeless shelter
- `{COUNTY} county` GED adult education HiSET
- `{COUNTY} county` legal aid expungement

Prioritize **county seats** and **jail-hosting counties** first, then remaining rural counties.

#### What to add for small counties

Prefer **program-level, county-pinned rows**:

- County probation/parole or community supervision office (when published)
- County human services / benefits intake office
- Nearest FQHC or CMHC that explicitly serves the county (use `multi` + full `served_counties` if regional)
- Regional food pantry or ministry with published county service area
- County adult education / HiSET site
- Local sheriff reentry or jail discharge navigator (when verifiable)

A single **multi-county** row with explicit `served_counties` covering several adjacent rural counties is acceptable when no standalone provider exists—but **name every county**; do not leave rural counties to “nearest metro” assumptions.

#### Anti-patterns (do not stop here)

- ❌ Assuming Nashville/Memphis/Louisville providers serve all surrounding rural counties without listing them
- ❌ Only adding a coalition row for a multi-county region with no direct-service pins for smaller member counties
- ❌ Marking a state complete when >10% of counties have zero local or multi-county coverage

#### Automated gap-fill (`scripts/phase3b_gapfill.py`)

After Phases 1–4, run a **coverage audit**, then register gap-fill rows in the build pipeline so small-county depth is reproducible (not a one-off CSV edit).

**1. Audit county coverage**

```bash
python3 scripts/check-county-coverage.py data/{state-slug}-resources.csv src/lib/{state-slug}/counties.ts
python3 scripts/check-county-coverage.py data/{state-slug}-resources.csv src/lib/{state-slug}/counties.ts --tier-a
python3 scripts/check-county-coverage.py data/{state-slug}-resources.csv src/lib/{state-slug}/counties.ts --report
```

Reports pinned %, uncovered counties, thin counties (0–1 pins), Tier A depth, category minimums, and a **COMPLETE | ANOTHER PASS NEEDED** verdict. Target **≥90%** pinned before marking complete.

**2. Add gap-fill rows for `{STATE}`**

In `scripts/phase3b_gapfill.py`, create:

```python
def register_phase3b_{state_slug}(add):
    """Small-county depth: uncovered and thin counties for {STATE}."""
    # add county JFS/DHS, probation field offices, AJCs, FQHCs, adult ed, etc.
    add(name="...", category="financial-assistance", county="Example", ...)
```

Use the existing `register_phase3b_indiana`, `register_phase3b_ohio`, and `register_phase3b_tennessee` functions as templates. Prefer **direct-service** rows:

- County benefits intake (JFS / DHS / DFR / equivalent)
- Probation/parole or community supervision field office
- American Job Center / workforce one-stop
- FQHC or community mental health center
- County adult education / HiSET site

Every `add()` row must include `_source`, `_source_type`, and `_confidence` for the research log. Write full publication-ready `description` / `description_es`—do not use `.replace()` word-swapping for Spanish.

**3. Wire into the state build script**

At the end of `scripts/build-{state-slug}-resources.py` (after Phases 1–4 entries):

```python
from phase3b_gapfill import register_phase3b_{state_slug}
register_phase3b_{state_slug}(add)
```

**4. Rebuild and verify**

```bash
npm run seed:resources:{state-slug}   # or python3 scripts/build-{state-slug}-resources.py + enrich
python3 scripts/check-county-coverage.py data/{state-slug}-resources.csv src/lib/{state-slug}/counties.ts
python3 scripts/enrich-resources.py --check-only data/{state-slug}-resources.csv
```

Re-run the gap-fill register function until coverage ≥90% and thin counties have 2+ direct-service pins where published providers exist. Document any remaining gaps in `{state-slug}-research-log.csv`.

#### County benefits sync (mandatory — all counties)

When a state has a **county-level benefits intake office in every county** (Ohio CDJFS, Tennessee TDHS, Indiana DFR, Kentucky DCBS), add CSV rows **mechanically**—do not log these as research GAPs.

1. **Sync official locator data**
   ```bash
   python3 scripts/sync-county-benefits-offices.py --state {state-slug}
   ```
   Writes `scripts/data/{state}-*-offices.json` (e.g. `ohio-cdjfs-offices.json`, `tn-tdhs-offices.json`). Phone/address only from primary source; leave blank + locator URL when unverified.

2. **Register in build pipeline** via `scripts/county_benefits_registry.py` (called from `register_phase3b_{state}`). Skips counties that already have a `financial-assistance` pin.

3. **Re-sync before major releases** when locators change (TDHS office moves, PCSAO directory updates).

#### Tier A anchors (after county benefits)

Add verified directory-backed rows that cover many counties with one network row:

- Probation/parole regions (ODRC APA, TDOC districts, KY DOC districts)
- FQHC / CMHC networks with explicit `served_counties`
- LWDB / American Job Center networks (Tennessee Jobs4TN)
- Regional food banks (explicit county lists)

See `scripts/tier_a_anchors.py`. Do **not** duplicate county JFS/TDHS rows here—those come from the county benefits registry.

#### BACKLOG vs GAP (`scripts/append-tier-a-research-gaps.py`)

| Outcome | When to use |
| --- | --- |
| **Mechanical CSV row** | Provider exists in every county (benefits office, AJC co-located with JFS)—use sync + registry, not research log GAP |
| **BACKLOG** | Verifiable provider exists but primary-source address/phone not yet in JSON—defer enrichment, not a coverage gap |
| **GAP** | No published local/regional direct-service provider after 211 + county benefits + sheriff/probation + state directory search |

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
- [ ] **County depth** — ≥90% of counties pinned; jail-hosting counties covered (Phase 3b)
- [ ] Description/eligibility/notes are not duplicated
- [ ] Spanish fields present or flagged
- [ ] **Publication-ready content** metrics met (see below)

---

## Post-research coverage report (required)

After Phases 1–5 and gap-fill rebuild, **before** marking `{STATE}` complete or generating seed SQL, run both audit commands and produce this report (copy the template below or use `--report`):

```bash
python3 scripts/check-county-coverage.py data/{state-slug}-resources.csv src/lib/{state-slug}/counties.ts
python3 scripts/check-county-coverage.py data/{state-slug}-resources.csv src/lib/{state-slug}/counties.ts --tier-a
python3 scripts/check-county-coverage.py data/{state-slug}-resources.csv src/lib/{state-slug}/counties.ts --report
python3 scripts/enrich-resources.py --check-only data/{state-slug}-resources.csv
```

### Report template

```text
Post-research coverage report — {STATE}
Date: YYYY-MM-DD
Row count: N

Pin coverage: X/Y counties (Z%) — PASS if ≥90%
Thin counties (1 pin): N — [list if any]

Tier A core (≥3 of 8): X/Y counties (Z%) — stretch ≥50%
Tier A weak sample: [optional 5–10 counties with missing core categories]

Data hygiene:
- Unknown county names: [none | list]
- Wrong-state counties in served_counties: [none | list]
- enrich-resources --check-only: PASS | FAIL (note failures)

Category minimums (17 slugs, program-level rows):
- [category]: count / minimum — OK | BELOW
- reentry-organizations share: N% (≤25% unless documented)

Verdict: COMPLETE | ANOTHER PASS NEEDED

COMPLETE only if ALL of:
- Pins ≥90%
- No mandatory jail-county gaps (or documented in research_log)
- Tier A ≥50% OR documented accepted gap in research_log
- enrich-resources --check-only passes
- No data hygiene blockers (unknown/wrong-state counties)
- Category minimums met; coalition balance OK

ANOTHER PASS NEEDED if ANY of:
- Pins <90%
- Tier A <50% without documented accepted gap
- >10 thin counties
- Data hygiene errors (unknown or wrong-state county names)
- Category minimums unmet or coalition-heavy without documentation
```

Document the report in `{state-slug}-research-log.csv` notes or paste into your handoff. If verdict is **ANOTHER PASS NEEDED**, add gap-fill rows in `scripts/phase3b_gapfill.py`, rebuild, and re-run until pins and hygiene pass (Tier A may remain below 50% only with an explicit accepted-gap note).

See also `docs/coverage-policy.md` for Tier A/B/C definitions.

---

## Publication-ready content standard (required on first pass)

**Do not ship thin CSV rows expecting a later enrichment pass.** Kentucky-quality entries are the default deliverable. Every row must be **publication-ready** when the CSV is first submitted.

### Description requirements (EN + ES)

Each `description` / `description_es` must be **2–5 sentences** and **300–500 characters** (median target ~400, matching `data/kentucky-resources.csv`).

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


| Metric                                                        | Target           |
| ------------------------------------------------------------- | ---------------- |
| Median `description` length                                   | ≥ 350 characters |
| Rows with generic eligibility                                 | 0                |
| Rows with “Contact program for current intake” in description | 0                |
| Rows missing `description_es`                                 | 0                |
| `services` with only generic placeholders                     | 0                |


If metrics fail, **expand weak rows in place** before marking the state complete. Optional `data/enrichments/{state}-*.json` files are for **targeted corrections only**, not bulk first-pass content.

### Kentucky reference

Compare random samples against `data/kentucky-resources.csv` and `data/enrichments/batch-*.json` for tone, depth, and field separation.

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
"{COUNTY} county" jail reentry discharge planning
"{COUNTY} county" sheriff community corrections
"{COUNTY} county" probation parole office
"{COUNTY} county" DHS SNAP Medicaid benefits
"{COUNTY} county" food pantry reentry
"{COUNTY} county" community health center
"{COUNTY} county" American Job Center workforce
"{COUNTY} county" GED HiSET adult education
"{COUNTY} county" legal aid expungement
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

Every state dataset should be **library-ready at depth**, not a thin coalition directory. Use **`data/kentucky-resources.csv`** as the density reference for mid-size states.

### Row-count targets


| State size                     | Target resources | Notes                                               |
| ------------------------------ | ---------------- | --------------------------------------------------- |
| Mid-size (e.g. KY, OH, IN, TN) | **150–200**      | Match Kentucky reference density (~190 rows)        |
| Large (CA, TX, FL)             | **250–400+**     | Scale metros and rural regions proportionally       |
| Small (e.g. DE, RI, VT)        | **75–120**       | Still require program-level depth in all categories |


**75 rows is a floor for discovery, not a completion target.** If category minimums below are unmet, keep researching.

### Category minimums (program-level rows)

Count only **direct-service or specialty program** rows toward these minimums. Reentry coalitions, councils, and referral-only portals **do not** count toward housing, healthcare, employment, education, veterans, or basic-needs minimums (they belong in `reentry-organizations`).


| Category slug             | Minimum rows | Examples                                                            |
| ------------------------- | ------------ | ------------------------------------------------------------------- |
| `housing`                 | 20           | Transitional housing, recovery residences, reentry shelter programs |
| `healthcare`              | 20           | FQHCs, mental health clinics, Medicaid navigators                   |
| `employment`              | 15           | Workforce centers, CEO, Goodwill reentry, fair-chance training      |
| `probation-parole`        | 10           | Field offices, RSCs, community corrections contractors              |
| `legal-aid`               | 12           | Regional legal aid + expungement clinics                            |
| `education`               | 12           | GED/HiSET sites, adult diploma, vocational reentry                  |
| `veterans`                | 10           | VJO specialists, VSOs, HCRV, veteran treatment courts               |
| `basic-needs`             | 10           | Clothing closets, release bags, hygiene programs                    |
| `substance-use-treatment` | 6            | MAT, residential SUD, ATR providers                                 |
| `financial-assistance`    | 6            | Benefits enrollment, emergency assistance                           |
| `food-nutrition`          | 4            | Regional food banks + SNAP help                                     |
| `id-documentation`        | 4            | ID clinics, vital records, BMV guidance                             |
| `peer-support`            | 4            | Certified peer specialists, mentor programs                         |
| `transportation`          | 3            | Reduced-fare transit, ride programs                                 |
| `family-children`         | 3            | Reunification, children of incarcerated parents                     |
| `state-agency`            | 4            | DOC, benefits portals, official hotlines                            |
| `reentry-organizations`   | 5–40         | Coalitions + CBO navigators (deduplicated)                          |


All **17 category slugs** must be represented. Compare your counts to Kentucky before marking complete.

### Balance check

Before marking `{STATE}` complete, confirm the dataset is **not coalition-heavy**:

- `reentry-organizations` should be **≤25%** of total rows unless the state has an unusually thin provider landscape (document in research log).
- At least **60%** of rows should be direct-service providers (housing, health, employment, legal, treatment, education, veterans, basic needs, probation/parole).

### County depth check (required)

Before marking `{STATE}` complete, confirm **small-county coverage** (Phase 3b):

- **≥90%** of official `{STATE}` counties have at least one **single** or **multi** row pinning them (statewide rows excluded from this count).
- Counties with jails or state/federal prisons are **never** left at zero local coverage without a documented gap in `research_log`.
- Rural counties outside the top 10 MSAs have more than coalition-only coverage—include probation offices, county JFS, FQHCs, food pantries, or adult ed where published.
- Compare county touch count to Kentucky (`data/kentucky-resources.csv`); mid-size states should be in the same ballpark for geographic spread.

---

## State onboarding / completion checklist

Use this sequence for every new state. Stop only when the post-research report verdict is **COMPLETE** (or document why **ANOTHER PASS NEEDED**).

| Step | Action | Pass criteria |
| --- | --- | --- |
| 1 | Phases 1–4 in `build-{state}-resources.py` | Category minimums, 150–200 rows (mid-size), publication-ready copy |
| 2 | **County benefits sync** | `python3 scripts/sync-county-benefits-offices.py --state {state}` → JSON in `scripts/data/` |
| 3 | **County benefits registry** | `register_county_benefits_{state}` wired in `phase3b_gapfill.py`; **100%** of counties have `financial-assistance` pin |
| 4 | **Tier A anchors** | Probation regions, FQHC networks, LWDB/AJC, food banks in `tier_a_anchors.py` where applicable |
| 5 | Rebuild CSV | `python3 scripts/build-{state}-resources.py` |
| 6 | Enrich + check | `python3 scripts/enrich-resources.py --check-only data/{state}-resources.csv` |
| 7 | Coverage report | `python3 scripts/check-county-coverage.py data/{state}-resources.csv src/lib/{state}/counties.ts --report` |
| 8 | Seed SQL | `npm run seed:resources:{state}` |

**COMPLETE** when: ≥90% county pins, **all counties** have county benefits FA pin (where state provides one), category minimums OK, enrich check PASS, Tier A stretch ≥50% (target higher after anchors).

**ANOTHER PASS NEEDED** when: uncovered counties, missing FA pins, thin jail counties, or Tier A weak counties with only 1–2 core categories and no BACKLOG/GAP documented.

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
- [ ] **County benefits:** 100% of counties have `financial-assistance` pin from sync + registry (where state has per-county intake)
- [ ] **County depth check** passed (≥90% counties pinned; jail counties covered; true gaps logged—not missing mechanical rows)
- [ ] **Post-research coverage report** produced (see below; `--report` flag or manual template)
- [ ] Every multi-county row has explicit `served_counties`
- [ ] No duplicate programs
- [ ] `research_log.csv` maps every `id` to ≥1 source URL
- [ ] CSV validates against column list (no extra columns, proper quoting)
- [ ] **Onboarding wired** (registry, counties, i18n—see batch workflow step 7)

---

## Batch workflow (for this codebase)

After research:

1. Save as `data/{state-slug}-resources.csv` with **publication-ready content** (see standard above—do not ship thin rows).
2. **County benefits + Phase 3b gap-fill:** sync locators → `county_benefits_registry.py` → `register_phase3b_{state-slug}` → wire into build script → rebuild (see Phase 3b and State onboarding checklist).
3. Quality gate: `python3 scripts/enrich-resources.py --check-only data/{state-slug}-resources.csv`
4. If the gate fails, expand weak rows in the CSV or run:
  `python3 scripts/enrich-resources.py data/{state-slug}-resources.csv --write-json data/enrichments/{state}-enriched.json`  
   This pass also fills `**intake_signals`** (`accepts_criminal_record`, `referral_required`, `walk_in_ok`) from the enriched eligibility/notes text.
5. Generate seed SQL:
  `RESOURCES_DEFAULT_STATE="{STATE}" RESOURCES_UUID_PREFIX=d3000001 RESOURCES_SEED_OUTPUT=supabase/seed-{state-slug}-resources.sql RESOURCES_INCLUDE_CATEGORIES=false npx tsx scripts/generate-resources-seed.ts data/{state-slug}-resources.csv`
6. Load seed in Supabase SQL Editor (or `npm run db:push:{state}` with service role key).
7. Admin review for category assignment, coverage, and Spanish quality before publish.
8. **Wire onboarding (required)** — the get-started wizard reads `ONBOARDING_STATE_REGISTRY` automatically; no wizard code changes needed when you follow this checklist:

   | Step | File / command | What to do |
   | ---- | -------------- | ------------ |
   | a | `src/lib/{state-slug}/counties.ts` | Export canonical county list (official names, sorted) as `{STATE}_COUNTIES` |
   | b | `src/lib/states/registry.ts` | Append `{ name: "{STATE}", slug: "{state-slug}", counties: {STATE}_COUNTIES }` |
   | c | `src/i18n/messages/en.ts` + `es.ts` | Add `onboarding.states.{state-slug}` and `pathways.firstWeek.introByState.{state-slug}` |
   | d | `scripts/lib/resource_enricher.py` | Add `{STATE}` to `STATE_PRESETS`; ensure `infer_state_from_csv_path` recognizes `{state-slug}` |
   | e | `package.json` | Add `seed:resources:{state-slug}`, `db:push:{state-slug}`, `enrich:{state-slug}`; include in `seed:resources:all` |
   | f | `scripts/push-{state-slug}-resources.ts` | Create push script (copy Indiana/Tennessee pattern); assign next `RESOURCES_UUID_PREFIX` (`d5000001` for the fifth state, etc.) |
   | g | `scripts/push-intake-signals.ts` | Include `data/{state-slug}-resources.csv` in intake signal source list |
   | h | Verify | `npm run build`; confirm `/get-started` shows `{STATE}` with full county dropdown |

   **UUID prefix convention:** Kentucky `d1000001`, Ohio `d2000001`, Indiana `d3000001`, Tennessee `d4000001` — increment for each new state.

**Ohio example:** `npm run seed:resources:ohio` rebuilds CSV, auto-enriches, and regenerates `supabase/seed-ohio-resources.sql`.

Use `data/enrichments/{state}-batch-XX.json` only for **targeted manual corrections** after the CSV is already publication-ready—not as a substitute for writing full descriptions during research.

See also:

- `data/kentucky-resources.csv` — Kentucky reference dataset
- `.cursor/rules/i18n.mdc` — field semantics for `description`, `eligibility`, `notes`, `served_counties`, `coverage`
- `scripts/phase3b_gapfill.py` — reproducible small-county gap-fill (add `register_phase3b_{state-slug}` per state)
- `scripts/check-county-coverage.py` — county pin % and Tier A audit; `--report` for structured verdict
- `scripts/generate-resources-seed.ts` — CSV column mapping and category aliases
- `scripts/apply-enrichments.ts` — enrichment merge workflow
- `src/lib/states/registry.ts` — onboarding state registry (wizard auto-wires from here)

---

## Start command

> **Begin research for `{STATE}`.**
>
> Phase 1: statewide backbone (target 15–25 rows).
> Phase 2: top 5 metros by population + counties with major correctional facilities (target 30–50 program-level rows).
> Phase 3: county reentry coalitions — deduplicated (target 25–40 rows).
> **Phase 3b: small-county depth — audit with `check-county-coverage.py`, gap-fill via `phase3b_gapfill.py`, rebuild until ≥90% counties pinned (jail counties mandatory).**
> Phase 4: program-level expansion until **150–200 total rows** and **category minimums** match `data/kentucky-resources.csv` (Kentucky reference).
> Phase 5: verification pass + **publication-ready content** self-check (descriptions enriched on first pass—no thin CSV).
>
> **Post-research coverage report (required):** Run both `check-county-coverage.py` audits plus `--report` and `enrich-resources.py --check-only`; output the structured report (template in **Post-research coverage report** section) with verdict **COMPLETE** or **ANOTHER PASS NEEDED** before seed/deploy.
>
> **Post-research pipeline (required before seed/deploy):**
>
> 1. Phase 3b gap-fill in `scripts/phase3b_gapfill.py` + rebuild CSV
> 2. `python3 scripts/check-county-coverage.py data/{state-slug}-resources.csv src/lib/{state-slug}/counties.ts` — must show ≥90%
> 2b. `python3 scripts/check-county-coverage.py ... --tier-a` and `... --report` — coverage report + verdict
> 3. `python3 scripts/enrich-resources.py --check-only data/{state-slug}-resources.csv` — quality gate
> 4. If needed: enrich JSON pass for weak rows + `intake_signals`
> 5. Generate seed SQL + `npm run db:push:{state-slug}` (or SQL Editor)
> 6. **Wire onboarding** — registry, counties file, i18n (EN/ES), enricher preset, package scripts, push script (see batch workflow step 8)
>
> Output: `data/{state-slug}-resources.csv` + `data/{state-slug}-research-log.csv`.
> Flag uncertain rows in the log; do not fabricate eligibility or hours.
> Compare final category counts and **county coverage %** to Kentucky before marking complete.
> **Deliver the Post-research coverage report** with your CSV handoff.

