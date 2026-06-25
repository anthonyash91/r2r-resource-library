# Georgia Reentry Resource Discovery Prompt

State-specific research prompt for **Georgia** in the **Road to Reentry Library**. Based on [`multi-state-resource-research.md`](./multi-state-resource-research.md) — follow all field semantics, quality rules, and pipeline steps there unless overridden below.

**Replace in handoffs:** `{STATE}` = Georgia, `{state-slug}` = `georgia`, UUID prefix = `d8000001`.

---

## Georgia context

- **159 counties** (official list in `src/lib/georgia/counties.ts`)
- **Consolidated city-counties:** Athens-Clarke, Augusta-Richmond, Columbus-Muscogee, Macon-Bibb, Cusseta-Chattahoochee, Statenville-Echols, Georgetown-Quitman, Preston-Webster — use canonical county names (`Clarke`, `Richmond`, `Muscogee`, `Bibb`, etc.) in `county` / `served_counties`
- **Major metros (Phase 2 priority):**
  - Atlanta / Fulton (also DeKalb, Cobb, Gwinnett, Clayton)
  - Augusta / Richmond
  - Columbus / Muscogee
  - Macon / Bibb
  - Savannah / Chatham
- **Correctional hubs:** GDC facilities (Reidsville, Jackson, Baldwin, Rogers, Arrendale, etc.), county jails in Fulton, DeKalb, Chatham, Muscogee, Bibb, Richmond

---

## State-specific search terms & agencies

### Phase 1 — Statewide backbone

| Agency / program | Search terms | Primary URLs |
| --- | --- | --- |
| **GDC** (Georgia Dept. of Corrections) | `GDC reentry services`, `Georgia DOC pre-release` | gdc.georgia.gov |
| **DCS** (Dept. of Community Supervision) | `Georgia DCS reentry`, `parole probation Georgia` | dcs.georgia.gov |
| **Board of Pardons and Paroles** | `Georgia parole field office`, `pap.georgia.gov locations` | pap.georgia.gov |
| **DFCS / COMPASS GA** | `COMPASS Georgia SNAP Medicaid`, `DFCS county office locator` | compass.ga.gov, dfcs.georgia.gov/locations |
| **211 Georgia** | `211 Georgia reentry`, `georgia211.org` | georgia211.org |
| **Georgia Legal Services** | `GLSP record restriction`, `Georgia legal aid expungement` | glsp.org |
| **GDOL / WorkSource Georgia** | `WorkSource Georgia career center`, `Georgia fair chance employment` | dol.georgia.gov |
| **GVRA** | `Georgia Vocational Rehabilitation reentry` | gvra.georgia.gov |
| **GCAL / 988** | `Georgia Crisis Access Line`, `mygcal.com` | mygcal.com, 988 |
| **Reentry Partnership Housing (RPH)** | `Georgia RPH reentry housing DCA` | dca.georgia.gov RPH page |
| **Georgia CALLS** | `Georgia CALLS fair chance employers` | georgiacalls.org |
| **Georgia Justice Project** | `Georgia record restriction`, `GJP reentry legal` | gjp.org |
| **Veterans** | `Georgia Department of Veterans Service county office` | veterans.georgia.gov |

### Phase 2 — Major metros

```text
"Atlanta" reentry programs formerly incarcerated
"Fulton county" transitional housing reentry
"DeKalb county" expungement legal aid
"Augusta" "Richmond county" reentry housing
"Columbus" "Muscogee county" Valley Rescue Mission reentry
"Macon" "Bibb county" reentry employment
"Savannah" "Chatham county" Union Mission reentry
"Atlanta" fair chance employment training
"Georgia" recovery housing "justice involved" parole probation
```

### Phase 3b — Small-county depth

For each uncovered county:

```text
"{COUNTY} county" Georgia DFCS SNAP Medicaid
"{COUNTY} county" Georgia probation parole field office pap.georgia.gov
"{COUNTY} county" WorkSource Georgia career center
"{COUNTY} county" Georgia FQHC community health center
"{COUNTY} county" food bank pantry Georgia
"{COUNTY} county" GED adult education Georgia
"211 {COUNTY} county Georgia" reentry
```

**County benefits sync (mandatory):**

```bash
python3 scripts/sync-county-benefits-offices.py --state georgia
```

Registers all 159 DFCS county offices via `register_county_benefits_georgia` in `scripts/county_benefits_registry.py`.

---

## Row-count & coverage targets

| Metric | Target |
| --- | --- |
| Total rows | **150–200+** (159 counties — aim for Kentucky density) |
| County pin coverage | **≥90%** of 159 counties |
| County DFCS FA pins | **100%** via sync + registry |
| Category minimums | All 17 slugs per multi-state prompt |

---

## Pipeline (Georgia)

```bash
npm run seed:resources:georgia
python3 scripts/check-county-coverage.py data/georgia-resources.csv src/lib/georgia/counties.ts --report
python3 scripts/enrich-resources.py --check-only data/georgia-resources.csv
npm run build
```

**Build script:** `scripts/build-georgia-resources.py`  
**Phase 3b:** `register_phase3b_georgia()` in `scripts/phase3b_gapfill.py`  
**Expansion:** `scripts/georgia_phase4_expansion.py`, `scripts/georgia_rural_depth.py`

---

## Start command

> **Begin research for Georgia.**
>
> Phase 1: GDC, DCS, BPP, COMPASS/DFCS, 211 Georgia, GLSP, GDOL/GVRA, GCAL, veteran reentry, record restriction (15–25 rows).
> Phase 2: Atlanta, Augusta, Columbus, Macon, Savannah — housing, employment, legal, healthcare (30–50 program-level rows).
> Phase 3/4: Recovery housing, fair-chance employers, specialty gaps via `georgia_phase4_expansion.py`.
> Phase 3b: DFCS sync + gap-fill until ≥90% county pins.
>
> Output: `data/georgia-resources.csv` + `data/georgia-research-log.csv`.
> Deliver post-research coverage report before seed/deploy.

See [`multi-state-resource-research.md`](./multi-state-resource-research.md) for full field definitions, category minimums, and completion checklist.
