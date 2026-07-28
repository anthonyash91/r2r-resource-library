# Alabama Reentry Resource Discovery Prompt

State-specific research prompt for **Alabama** in the **Road to Reentry Library**. Based on [`multi-state-resource-research.md`](./multi-state-resource-research.md) — follow all field semantics, quality rules, and pipeline steps there unless overridden below.

**Replace in handoffs:** `{STATE}` = Alabama, `{state-slug}` = `alabama`, UUID prefix = `dc000001`.

---

## Alabama context

- **67 counties** (official list in `src/lib/alabama/counties.ts`; use **St. Clair** with period)
- **Major metros (Phase 2 priority):**
  - Birmingham / Jefferson (also Shelby, St. Clair)
  - Montgomery / Montgomery County
  - Mobile / Mobile County
  - Huntsville / Madison (also Limestone, Morgan)
  - Tuscaloosa / Tuscaloosa County
  - Dothan / Houston County (Wiregrass)
  - Florence / Lauderdale (Shoals)
- **Correctional hubs:** ADOC prisons (Donaldson, Holman, Staton, Tutwiler, Limestone, etc.), county jails in Jefferson, Mobile, Montgomery, Madison, and regional community corrections / probation offices statewide

---

## State-specific search terms & agencies

### Phase 1 — Statewide backbone

| Agency / program | Search terms | Primary URLs |
| --- | --- | --- |
| **ADOC Reentry** | `ADOC reentry`, `Alabama DOC reentry` | doc.alabama.gov/ReEntryInfo |
| **Bureau of Pardons and Paroles** | `Alabama parole probation`, `paroles.alabama.gov` | paroles.alabama.gov |
| **MyDHR** | `MyDHR Alabama SNAP Medicaid`, `Alabama DHR benefits` | mydhr.alabama.gov |
| **Alabama 211** | `211 Alabama reentry`, `uwca.org 211` | uwca.org/211 |
| **Legal Services Alabama** | `Legal Services Alabama expungement`, `alslegal.org` | alslegal.org |
| **Alabama Career Center / AIDT** | `Alabama Career Center`, `AIDT workforce training` | joblink.alabama.gov, aidt.edu |
| **ADRS** | `Alabama vocational rehabilitation reentry`, `rehab.alabama.gov` | rehab.alabama.gov |
| **ADMH** | `Alabama mental health substance abuse`, `mh.alabama.gov` | mh.alabama.gov |
| **Alabama Reentry Commission** | `Alabama reentry commission community partners` | doc.alabama.gov, governor's office |
| **DMV ID** | `Alabama DMV ID released from prison`, `alea.gov driver license` | alea.gov |
| **Veterans** | `Alabama Department of Veterans Affairs`, `va.alabama.gov` | va.alabama.gov |

### Phase 2 — Major metros

```text
"Birmingham" OR "Jefferson county" reentry programs formerly incarcerated
"Montgomery county" transitional housing reentry employment
"Mobile county" reentry housing legal aid
"Huntsville" OR "Madison county" reentry workforce
"Tuscaloosa" reentry programs justice involved
"Dothan" OR "Houston county" reentry housing employment
"Florence" OR "Lauderdale county" reentry programs
"Alabama" recovery housing "justice involved" parole probation
```

### Phase 3b — Small-county depth

For each uncovered county:

```text
"{COUNTY} county" Alabama DHR SNAP Medicaid
"{COUNTY} county" Alabama probation parole field office
"{COUNTY} county" Alabama Career Center
"{COUNTY} county" Alabama FQHC community health center
"{COUNTY} county" Alabama mental health center
"{COUNTY} county" food bank pantry Alabama
"{COUNTY} county" GED adult education Alabama
"211 {COUNTY} county Alabama" reentry
```

**County benefits sync (mandatory):**

```bash
python3 scripts/sync-county-benefits-offices.py --state alabama
```

Registers all 67 county DHR offices via `register_county_benefits_alabama` in `scripts/county_benefits_registry.py`.

---

## Row-count & coverage targets

| Metric | Target |
| --- | --- |
| Total rows | **150–200+** (67 counties — Kentucky-density reference) |
| County pin coverage | **≥90%** of 67 counties |
| County DHR FA pins | **100%** via sync + registry |
| Category minimums | All 17 slugs per multi-state prompt |

---

## Pipeline (Alabama)

```bash
npm run seed:resources:alabama
python3 scripts/check-county-coverage.py data/alabama-resources.csv src/lib/alabama/counties.ts --report
python3 scripts/enrich-resources.py --check-only data/alabama-resources.csv
npm run build
```

**Build script:** `scripts/build-alabama-resources.py`
**Phase 3b:** `register_phase3b_alabama()` in `scripts/phase3b_gapfill.py`
**Expansion:** `scripts/alabama_phase4_expansion.py`, `scripts/alabama_category_fill.py`, `scripts/alabama_thin_counties.py`

---

## Start command

> **Begin research for Alabama.**
>
> Phase 1: ADOC reentry, Bureau of Pardons and Paroles, MyDHR/DHR, 211, Legal Services Alabama, Career Center/AIDT, ADRS, ADMH, Reentry Commission, DMV, veterans (15–25 rows).
> Phase 2: Birmingham/Jefferson, Montgomery, Mobile, Huntsville/Madison, Tuscaloosa, Dothan/Houston, Florence/Lauderdale — housing, employment, legal, healthcare (30–50 program-level rows).
> Phase 3/4: Recovery housing, fair-chance employers, specialty gaps via `alabama_phase4_expansion.py`.
> Phase 3b: DHR sync + gap-fill until ≥90% county pins.
>
> Output: `data/alabama-resources.csv` + `data/alabama-research-log.csv`.
> Deliver post-research coverage report before seed/deploy.

See [`multi-state-resource-research.md`](./multi-state-resource-research.md) for full field definitions, category minimums, and completion checklist.
