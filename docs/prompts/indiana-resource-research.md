# Indiana Reentry Resource Discovery Prompt

State-specific research prompt for **Indiana** in the **Road to Reentry Library**. Based on [`multi-state-resource-research.md`](./multi-state-resource-research.md) — follow all field semantics, quality rules, and pipeline steps there unless overridden below.

**Replace in handoffs:** `{STATE}` = Indiana, `{state-slug}` = `indiana`, UUID prefix = `d3000001`.

---

## Indiana context

- **92 counties** (official list in `src/lib/indiana/counties.ts`)
- **Benefits offices:** DFR county/local offices via `indiana-dfr-offices.json`
- **Major metros (Phase 2 priority):** Indianapolis/Marion, Fort Wayne/Allen, Evansville/Vanderburgh, South Bend/St. Joseph, Gary/Lake
- **Correctional hubs:** IDOC facilities, county jails, probation departments

---

## State-specific search terms & agencies

### Phase 1 — Statewide backbone

| Agency / program | Search terms | Primary URLs |
| --- | --- | --- |
| **IDOC Reentry** | `Indiana DOC reentry`, `in.gov corrections reentry` | in.gov/idoc |
| **FSSA DFR / Indiana Benefits** | `Indiana Benefits SNAP Medicaid`, `DFR county office` | fssabenefits.in.gov |
| **211 Indiana** | `211 Indiana reentry` | in211.communityos.org |
| **Indiana Legal Services** | `Indiana Legal Services expungement` | indianalegalservices.org |
| **WorkOne** | `WorkOne career center Indiana reentry` | in.gov/dwd |
| **Vocational Rehabilitation** | `Indiana VR Bureau reentry` | in.gov/fssa/ddrs |
| **DMHA / SUD** | `Indiana community mental health`, `988 Indiana` | in.gov/fssa/dmha |
| **IDVA** | `Indiana Department of Veterans Affairs` | in.gov/dva |

### Phase 2 — Major metros

```text
"Indiana" reentry housing employment justice involved
"Indiana" recovery housing parole probation
"Indianapolis/Marion" reentry programs
"Fort Wayne/Allen" reentry programs
"Evansville/Vanderburgh" reentry programs
"South Bend/St. Joseph" reentry programs
```

### Phase 3b — County depth

For each uncovered county:

```text
"{COUNTY} county" Indiana DFR SNAP Medicaid
"{COUNTY} county" Indiana probation parole
"{COUNTY} county" Indiana workforce career center
"{COUNTY} county" Indiana FQHC community health
"{COUNTY} county" Indiana food bank pantry
"{COUNTY} county" GED adult education Indiana
```

**Local benefits sync (mandatory):**

```bash
python3 scripts/sync-county-benefits-offices.py --state indiana
```

Registers all 92 county offices via `register_county_benefits_indiana` in `scripts/county_benefits_registry.py`.

---

## Row-count & coverage targets

| Metric | Target |
| --- | --- |
| Total rows | **280–350+** (92 counties) |
| County pin coverage | **≥90%** of 92 counties |
| County benefits pins | **100%** via registry |
| Tier A core depth | **≥50%** stretch (≥3 of 8 core categories per county) |
| Category minimums | All 17 slugs per multi-state prompt |

---

## Pipeline (Indiana)

```bash
python3 scripts/sync-county-benefits-offices.py --state indiana
python3 scripts/build-indiana-resources.py
python3 scripts/check-county-coverage.py data/indiana-resources.csv src/lib/indiana/counties.ts --tier-a --report
python3 scripts/enrich-resources.py --check-only data/indiana-resources.csv
npm run db:push:indiana
```

**Build script:** `scripts/build-indiana-resources.py`  
**County benefits:** `scripts/data/indiana-dfr-offices.json`

---

## Start command

> **Begin research for Indiana.**
>
> Phase 1: Statewide backbone agencies in table above (18–22 rows).
> Phase 2: Indianapolis, Fort Wayne, Evansville, South Bend, Gary — housing, employment, legal, healthcare (25–35 program-level rows).
> Phase 3/4: Recovery housing, fair-chance employers, specialty gaps via state expansion modules.
> Phase 3b: DFR county registry + gap-fill until ≥90% county pins and Tier A stretch.
>
> Output: `data/indiana-resources.csv` + `data/indiana-research-log.csv`.
> Deliver post-research coverage report before seed/deploy.
