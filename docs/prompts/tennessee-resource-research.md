# Tennessee Reentry Resource Discovery Prompt

State-specific research prompt for **Tennessee** in the **Road to Reentry Library**. Based on [`multi-state-resource-research.md`](./multi-state-resource-research.md) — follow all field semantics, quality rules, and pipeline steps there unless overridden below.

**Replace in handoffs:** `{STATE}` = Tennessee, `{state-slug}` = `tennessee`, UUID prefix = `d4000001`.

---

## Tennessee context

- **95 counties** (official list in `src/lib/tennessee/counties.ts`)
- **Benefits offices:** TDHS county/local offices via `tn-tdhs-offices.json`
- **Major metros (Phase 2 priority):** Nashville/Davidson, Memphis/Shelby, Knoxville/Knox, Chattanooga/Hamilton, Tri-Cities
- **Correctional hubs:** TDOC prisons, county jails, probation & parole offices

---

## State-specific search terms & agencies

### Phase 1 — Statewide backbone

| Agency / program | Search terms | Primary URLs |
| --- | --- | --- |
| **TDOC Reentry** | `Tennessee corrections reentry`, `tn.gov corrections reentry` | tn.gov/correction |
| **TDHS / Family Assistance** | `Tennessee SNAP Medicaid office locator`, `TDHS benefits` | tn.gov/humanservices |
| **211 Tennessee** | `211 Tennessee reentry` | 211tn.org |
| **Legal aid** | `Tennessee legal aid expungement`, `laet.org` | laet.org, memphislegal.org |
| **American Job Centers** | `American Job Center Tennessee reentry` | jobs4tn.gov |
| **VR Tennessee** | `Tennessee vocational rehabilitation reentry` | tn.gov/humanservices/drs |
| **TDMHSAS / CSOs** | `Tennessee behavioral health`, `988 Tennessee` | tn.gov/behavioral-health |
| **Tennessee DVS** | `Tennessee Department of Veterans Services` | tn.gov/veterans |

### Phase 2 — Major metros

```text
"Tennessee" reentry housing employment justice involved
"Tennessee" recovery housing parole probation
"Nashville/Davidson" reentry programs
"Memphis/Shelby" reentry programs
"Knoxville/Knox" reentry programs
"Chattanooga/Hamilton" reentry programs
```

### Phase 3b — County depth

For each uncovered county:

```text
"{COUNTY} county" Tennessee TDHS SNAP Medicaid
"{COUNTY} county" Tennessee probation parole
"{COUNTY} county" Tennessee workforce career center
"{COUNTY} county" Tennessee FQHC community health
"{COUNTY} county" Tennessee food bank pantry
"{COUNTY} county" GED adult education Tennessee
```

**Local benefits sync (mandatory):**

```bash
python3 scripts/sync-county-benefits-offices.py --state tennessee
```

Registers all 95 county offices via `register_county_benefits_tennessee` in `scripts/county_benefits_registry.py`.

---

## Row-count & coverage targets

| Metric | Target |
| --- | --- |
| Total rows | **300–380+** (95 counties) |
| County pin coverage | **≥90%** of 95 counties |
| County benefits pins | **100%** via registry |
| Tier A core depth | **≥50%** stretch (≥3 of 8 core categories per county) |
| Category minimums | All 17 slugs per multi-state prompt |

---

## Pipeline (Tennessee)

```bash
python3 scripts/sync-county-benefits-offices.py --state tennessee
python3 scripts/build-tennessee-resources.py
python3 scripts/check-county-coverage.py data/tennessee-resources.csv src/lib/tennessee/counties.ts --tier-a --report
python3 scripts/enrich-resources.py --check-only data/tennessee-resources.csv
npm run db:push:tennessee
```

**Build script:** `scripts/build-tennessee-resources.py`  
**County benefits:** `scripts/data/tn-tdhs-offices.json`

---

## Start command

> **Begin research for Tennessee.**
>
> Phase 1: Statewide backbone agencies in table above (18–22 rows).
> Phase 2: Nashville, Memphis, Knoxville, Chattanooga — housing, employment, legal, healthcare (25–35 program-level rows).
> Phase 3/4: Recovery housing, fair-chance employers, specialty gaps via state expansion modules.
> Phase 3b: TDHS county registry + gap-fill until ≥90% county pins and Tier A stretch.
>
> Output: `data/tennessee-resources.csv` + `data/tennessee-research-log.csv`.
> Deliver post-research coverage report before seed/deploy.
