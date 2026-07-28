# South Carolina Reentry Resource Discovery Prompt

State-specific research prompt for **South Carolina** in the **Road to Reentry Library**. Based on [`multi-state-resource-research.md`](./multi-state-resource-research.md) — follow all field semantics, quality rules, and pipeline steps there unless overridden below.

**Replace in handoffs:** `{STATE}` = South Carolina, `{state-slug}` = `south-carolina`, UUID prefix = `db000001`.

---

## South Carolina context

- **46 counties** (official list in `src/lib/south-carolina/counties.ts`)
- **4 DSS regions:** Lowcountry, Midlands, Pee Dee, Upstate (county DSS offices organized regionally)
- **Major metros (Phase 2 priority):**
  - Charleston / Tri-County (Berkeley, Charleston, Dorchester)
  - Columbia / Richland (also Lexington, Kershaw)
  - Greenville / Upstate (also Spartanburg, Anderson)
  - Florence / Pee Dee (also Darlington, Dillon)
  - Myrtle Beach / Horry (also Georgetown)
  - Rock Hill / York (also Lancaster, Chester)
- **Correctional hubs:** SCDC institutions (Broad River, Lee, McCormick, Tyger River, etc.), county detention centers in Richland, Charleston, Greenville, Horry, York

---

## State-specific search terms & agencies

### Phase 1 — Statewide backbone

| Agency / program | Search terms | Primary URLs |
| --- | --- | --- |
| **SCDC Reentry** | `SCDC reentry programs`, `doc.sc.gov programs` | doc.sc.gov/programs |
| **SCDPPPS** | `SC probation parole pardon`, `ppp.sc.gov field offices` | ppp.sc.gov |
| **SC Benefits Portal** | `benefitsportal.dss.sc.gov SNAP Medicaid`, `portal.dss.sc.gov` | benefitsportal.dss.sc.gov, portal.dss.sc.gov |
| **SC 211** | `SC 211 reentry`, `sc211.org` | sc211.org |
| **SCLS** | `South Carolina Legal Services expungement`, `sclegal.org` | sclegal.org |
| **SC Appleseed** | `SC Appleseed reentry`, `scjustice.org` | scjustice.org |
| **SC Bar PILS** | `SC Bar lawyer referral pro bono`, `scbar.org LawyerReferral` | scbar.org |
| **SC Works / DEW** | `SC Works career center`, `dew.sc.gov workforce reentry` | scworks.org, dew.sc.gov |
| **SCVRD** | `SC Vocational Rehabilitation reentry`, `scvrd.net` | scvrd.net |
| **SCDMH** | `SCDMH community mental health`, `scdmh.net` | scdmh.net |
| **SC CARES** | `SC CARES reentry`, `sccares.org` | sccares.org |
| **SC DMV** | `SCDMV online ID`, `scdmvonline.com` | scdmvonline.com |
| **Veterans** | `SC Department of Veterans Affairs`, `scdva.sc.gov` | scdva.sc.gov |
| **Crisis / SUD** | `988 South Carolina`, `SAMHSA`, `findtreatment.gov` | 988lifeline.org, samhsa.gov, findtreatment.gov |
| **Vital records** | `SC DHEC vital records birth certificate` | scdhec.gov/vital-records |

### Phase 2 — Major metros

```text
"Charleston" reentry programs formerly incarcerated
"Charleston county" transitional housing One80 Place Turning Leaf
"Columbia" "Richland county" reentry Oliver Gospel Mission New Directions
"Greenville" "Spartanburg" reentry United Housing Connections Miracle Hill ROAR
"Florence" "Pee Dee" reentry Hope Haven Keystone
"Myrtle Beach" "Horry county" reentry employment housing
"Rock Hill" "York county" reentry Catawba
"South Carolina" recovery housing "justice involved" parole probation
```

### Phase 3b — Small-county depth

For each uncovered county:

```text
"{COUNTY} county" South Carolina DSS SNAP Medicaid
"{COUNTY} county" SC probation parole SCDPPPS
"{COUNTY} county" SC Works career center
"{COUNTY} county" South Carolina FQHC community health center
"{COUNTY} county" food bank pantry South Carolina
"{COUNTY} county" GED adult education South Carolina
"211 {COUNTY} county South Carolina" reentry
```

**County benefits sync (mandatory):**

```bash
python3 scripts/sync-county-benefits-offices.py --state south-carolina
```

Registers all 46 county DSS offices via `register_county_benefits_south_carolina` in `scripts/county_benefits_registry.py`.

---

## Row-count & coverage targets

| Metric | Target |
| --- | --- |
| Total rows | **120–160+** (46 counties — aim for Kentucky/NC density) |
| County pin coverage | **≥90%** of 46 counties |
| County DSS FA pins | **100%** via sync + registry |
| Category minimums | All 17 slugs per multi-state prompt |

---

## Pipeline (South Carolina)

```bash
python3 scripts/build-south-carolina-resources.py
python3 scripts/check-county-coverage.py data/south-carolina-resources.csv src/lib/south-carolina/counties.ts --report
python3 scripts/enrich-resources.py --check-only data/south-carolina-resources.csv
npm run build
```

**Build script:** `scripts/build-south-carolina-resources.py`  
**Expansion:** `scripts/south_carolina_phase4_expansion.py`  
**Category fill:** `scripts/south_carolina_category_fill.py`  
**Thin counties:** `scripts/south_carolina_thin_counties.py`

---

## Start command

> **Begin research for South Carolina.**
>
> Phase 1: SCDC, SCDPPPS, benefits portal/DSS, 211, SCLS, SC Appleseed, SC Bar PILS, SC Works/DEW, SCVRD, SCDMH, SC CARES, DMV, veterans, 988/SAMHSA/FindTreatment, vital records (15–25 rows).
> Phase 2: Charleston, Columbia, Greenville, Spartanburg, Florence, Myrtle Beach, Rock Hill — housing, employment, legal, healthcare (30–50 program-level rows).
> Phase 3/4: Recovery housing, fair-chance employers, specialty gaps via `south_carolina_phase4_expansion.py`.
> Phase 3b: DSS sync + gap-fill until ≥90% county pins.
>
> Output: `data/south-carolina-resources.csv` + `data/south-carolina-research-log.csv`.
> Deliver post-research coverage report before seed/deploy.

See [`multi-state-resource-research.md`](./multi-state-resource-research.md) for full field definitions, category minimums, and completion checklist.
