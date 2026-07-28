# Florida Reentry Resource Discovery Prompt

State-specific research prompt for **Florida** in the **Road to Reentry Library**. Based on [`multi-state-resource-research.md`](./multi-state-resource-research.md) — follow all field semantics, quality rules, and pipeline steps there unless overridden below.

**Replace in handoffs:** `{STATE}` = Florida, `{state-slug}` = `florida`, UUID prefix = `de000001`.

---

## Florida context

- **67 counties** (official list in `src/lib/florida/counties.ts`; use **Miami-Dade**, **DeSoto**, **St. Johns**, **St. Lucie** per state convention)
- **DCF / ACCESS:** Benefits (SNAP, TCA, Medicaid application) flow through **MyACCESS Florida** and county **DCF Family Resource Centers** — not a single statewide walk-in office per program
- **CareerSource:** 24 local workforce boards under the **CareerSource Florida** network (not one generic “state job center” row per county)
- **Major metros (Phase 2 priority):**
  - Miami / Miami-Dade
  - Tampa / Hillsborough
  - Orlando / Orange (plus Osceola, Seminole)
  - Jacksonville / Duval
  - Fort Lauderdale / Broward
  - West Palm Beach / Palm Beach
  - Pensacola / Escambia
  - Tallahassee / Leon
- **Correctional hubs:** FDC state prisons (e.g. Reception and Medical Center, Lowell, Tomoka, Everglades, Hamilton, Gulf, Apalachee), regional county jails (Miami-Dade, Broward, Hillsborough, Orange, Duval, Pinellas)

---

## State-specific search terms & agencies

### Phase 1 — Statewide backbone

| Agency / program | Search terms | Primary URLs |
| --- | --- | --- |
| **FDC Reentry** | `Florida DOC reentry transition`, `fdc.myflorida.com reentry` | fdc.myflorida.com/reentry |
| **FDC Probation & Parole** | `Florida probation parole circuit offices` | fdc.myflorida.com/probation |
| **MyACCESS Florida** | `MyACCESS SNAP TCA Medicaid`, `DCF benefits Florida` | myaccess.myflfamilies.com |
| **AHCA Medicaid** | `Florida Medicaid AHCA managed care` | ahca.myflorida.com |
| **211 Florida** | `211 Florida United Way`, `211.org Florida` | 211.org (Florida coverage) |
| **Florida Legal Services** | `Florida Legal Services intake`, `floridalegal.org` | floridalegal.org |
| **CareerSource Florida** | `CareerSource Florida career center`, `careersourceflorida.com` | careersourceflorida.com |
| **Florida VR** | `Florida Division of Vocational Rehabilitation`, `rehabworks.org` | rehabworks.org |
| **Florida DVS** | `Florida Department of Veterans Affairs`, `floridavets.org` | floridavets.org |
| **FLHSMV** | `Florida driver license ID released`, `flhsmv.gov` | flhsmv.gov |
| **Vital records** | `Florida birth certificate DOH`, `floridahealth.gov certificates` | floridahealth.gov/certificates |
| **Florida Housing** | `Florida Housing Finance Corporation SHIP`, `floridahousing.org` | floridahousing.org |
| **FRRC** | `Florida Rights Restoration Coalition`, `floridarrc.com` | floridarrc.com |
| **Crisis / SUD** | `988 Florida`, `SAMHSA`, `findtreatment.gov` | 988lifeline.org, samhsa.gov, findtreatment.gov |

### Phase 2 — Major metros

```text
"Miami" "Miami-Dade" reentry housing employment Camillus Carrfour
"Tampa" "Hillsborough" reentry Metropolitan Ministries CareerSource
"Orlando" "Orange county" reentry Coalition for the Homeless CLS
"Jacksonville" "Duval" reentry Operation New Hope
"Fort Lauderdale" "Broward" reentry housing employment
"West Palm Beach" "Palm Beach" reentry Lord's Place Adopt-a-Family
"Pensacola" "Escambia" reentry housing employment
"Tallahassee" "Leon" reentry Florida Supportive Housing Coalition
"Florida" recovery housing "justice involved" parole probation
```

### Phase 3b — County depth

For each uncovered county:

```text
"{COUNTY} county" Florida DCF MyACCESS SNAP Medicaid Family Resource Center
"{COUNTY} county" FDC probation parole circuit
"{COUNTY} county" CareerSource career center
"{COUNTY} county" Florida FQHC community health center
"{COUNTY} county" food bank Feeding Florida partner pantry
"{COUNTY} county" GED adult education Florida
"{COUNTY} county" Florida SHIP rental assistance
```

**County benefits registry (mandatory):**

`scripts/data/florida-dcf-offices.json` + `register_county_benefits_florida` in `scripts/county_benefits_registry.py`.

DCF office data is bootstrapped from published Family Resource Center / ACCESS locations (`scripts/_bootstrap_florida_pipeline.py`). Re-run bootstrap if DCF relocates offices; verify phone and address against myflfamilies.com before marking `high` confidence.

**Quality notes from production dataset:**

- Do **not** use placeholder coalition sites (e.g. unverified `floridareentry.org` GoDaddy pages). Prefer **Florida Rights Restoration Coalition** (FRRC) for statewide rights/reentry navigation.
- **Bridges of America** is FDC-contracted treatment/work-release — category `reentry-organizations` or `substance-use-treatment`, not generic housing.
- Deduplicate FRRC and other statewide orgs on `(name, county)` — prefer wider `served_counties` and fuller address.

---

## Row-count & coverage targets

| Metric | Target |
| --- | --- |
| Total rows | **250–350+** (67 counties — metro density + rural pins) |
| County pin coverage | **≥90%** of 67 counties |
| County DCF FA pins | **100%** via registry |
| Category minimums | All 17 slugs per multi-state prompt |
| Reentry-org share | **≤25%** unless documented in research log |

---

## Pipeline (Florida)

```bash
python3 scripts/sync-county-benefits-offices.py --state florida   # if sync wired; else verify florida-dcf-offices.json
python3 scripts/build-florida-resources.py
python3 scripts/check-county-coverage.py data/florida-resources.csv src/lib/florida/counties.ts --tier-a --report
python3 scripts/enrich-resources.py --check-only data/florida-resources.csv
npm run db:push:florida
```

**Build script:** `scripts/build-florida-resources.py`  
**County benefits:** `register_county_benefits_florida` in `scripts/county_benefits_registry.py`  
**Expansion:** `scripts/florida_phase4_expansion.py`  
**Category fill:** `scripts/florida_category_fill.py`  
**Thin counties:** `scripts/florida_thin_counties.py`  
**Gap fill:** `scripts/florida_gap_fill.py`

---

## Start command

> **Begin research for Florida.**
>
> Phase 1: FDC reentry/P&P, MyACCESS Florida, AHCA Medicaid, 211, Florida Legal Services, CareerSource Florida, VR, DVS, FLHSMV, vital records, Florida Housing, FRRC, 988/SAMHSA/FindTreatment (18–25 rows).
> Phase 2: Miami-Dade, Hillsborough, Orange/Osceola/Seminole, Duval, Broward, Palm Beach, Escambia, Leon — housing, employment, legal, healthcare (30–50 program-level rows).
> Phase 3/4: Recovery housing, fair-chance employers, specialty gaps via `florida_phase4_expansion.py`.
> Phase 3b: DCF county registry + `florida_thin_counties.py` + gap-fill until **≥90%** county pins and category minimums met.
>
> Output: `data/florida-resources.csv` + `data/florida-research-log.csv`.
> Deliver post-research coverage report before seed/deploy.

See [`multi-state-resource-research.md`](./multi-state-resource-research.md) for full field definitions, category minimums, and completion checklist.
