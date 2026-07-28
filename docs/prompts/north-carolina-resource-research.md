# North Carolina Reentry Resource Discovery Prompt

State-specific research prompt for **North Carolina** in the **Road to Reentry Library**. Based on [`multi-state-resource-research.md`](./multi-state-resource-research.md) — follow all field semantics, quality rules, and pipeline steps there unless overridden below.

**Replace in handoffs:** `{STATE}` = North Carolina, `{state-slug}` = `north-carolina`, UUID prefix = `d9000001`.

---

## North Carolina context

- **100 counties** (official list in `src/lib/north-carolina/counties.ts`, NC Gen. Stat. § 153A-10)
- **Major metros (Phase 2 priority):**
  - Charlotte / Mecklenburg (also Union, Gaston, Cabarrus)
  - Raleigh / Wake (also Durham, Johnston)
  - Greensboro / Guilford (also Forsyth, Randolph)
  - Durham
  - Winston-Salem / Forsyth
  - Fayetteville / Cumberland (Fort Bragg area)
  - Wilmington / New Hanover
- **Correctional hubs:** NC DPS prisons (Raleigh Central, Maury, Tabor, Lanesboro, etc.), county jails in Mecklenburg, Wake, Guilford, Cumberland, Forsyth

---

## State-specific search terms & agencies

### Phase 1 — Statewide backbone

| Agency / program | Search terms | Primary URLs |
| --- | --- | --- |
| **NC DPS / DAC** | `NC DPS reentry`, `Division of Adult Correction reentry` | ncdps.gov |
| **NC Community Corrections** | `NC probation parole community corrections`, `NC DPS field services` | ncdps.gov |
| **ePASS / NC FAST** | `ePASS SNAP Medicaid North Carolina`, `NC FAST benefits` | epass.nc.gov, ncdhhs.gov |
| **NC 211** | `NC 211 reentry`, `nc211.org` | nc211.org |
| **Legal Aid of NC** | `Legal Aid NC expungement`, `legalaidnc.org` | legalaidnc.org |
| **NC Works** | `NC Works career center`, `NC Commerce workforce reentry` | ncworks.gov |
| **NC DVRS** | `NC Vocational Rehabilitation reentry`, `ncdhhs.gov/dvrs` | ncdhhs.gov/dvrs |
| **NC Crisis Solutions / 988** | `NC Crisis Solutions`, `988 North Carolina` | ncdhhs.gov, 988lifeline.org |
| **NC Second Chance** | `NC Second Chance Alliance`, `second chance employment NC` | ncsecondchance.org |
| **NC Justice Center** | `NC Justice Center reentry`, `ncjustice.org` | ncjustice.org |
| **NC CJC** | `NC Community Corrections reentry coalition` | nccjc.org |
| **Veterans** | `NC Department of Military and Veterans Affairs`, `ncdva.nc.gov` | ncdva.nc.gov |

### Phase 2 — Major metros

```text
"Charlotte" reentry programs formerly incarcerated
"Mecklenburg county" transitional housing reentry
"Raleigh" "Wake county" reentry employment
"Greensboro" "Guilford county" expungement legal aid
"Durham" reentry housing TROSA
"Fayetteville" "Cumberland county" Fort Bragg reentry
"Wilmington" "New Hanover" reentry programs
"North Carolina" recovery housing "justice involved" parole probation
```

### Phase 3b — Small-county depth

For each uncovered county:

```text
"{COUNTY} county" North Carolina DSS SNAP Medicaid
"{COUNTY} county" NC probation parole community corrections
"{COUNTY} county" NC Works career center
"{COUNTY} county" North Carolina FQHC community health center
"{COUNTY} county" food bank pantry North Carolina
"{COUNTY} county" GED adult education North Carolina
"211 {COUNTY} county North Carolina" reentry
```

**County benefits sync (mandatory):**

```bash
python3 scripts/sync-county-benefits-offices.py --state north-carolina
```

Registers all 100 county DSS offices via `register_county_benefits_north_carolina` in `scripts/county_benefits_registry.py`.

---

## Row-count & coverage targets

| Metric | Target |
| --- | --- |
| Total rows | **150–200+** (100 counties — aim for Kentucky density) |
| County pin coverage | **≥90%** of 100 counties |
| County DSS FA pins | **100%** via sync + registry |
| Category minimums | All 17 slugs per multi-state prompt |

---

## Pipeline (North Carolina)

```bash
npm run seed:resources:north-carolina
python3 scripts/check-county-coverage.py data/north-carolina-resources.csv src/lib/north-carolina/counties.ts --report
python3 scripts/enrich-resources.py --check-only data/north-carolina-resources.csv
npm run build
```

**Build script:** `scripts/build-north-carolina-resources.py`  
**Phase 3b:** `register_phase3b_north_carolina()` in `scripts/phase3b_gapfill.py`  
**Expansion:** `scripts/north_carolina_phase4_expansion.py`

---

## Start command

> **Begin research for North Carolina.**
>
> Phase 1: NC DPS/DAC, Community Corrections, ePASS/NC FAST, 211, Legal Aid NC, NC Works/DVRS, Crisis Solutions/988, veteran reentry, Second Chance (15–25 rows).
> Phase 2: Charlotte, Raleigh, Greensboro, Durham, Winston-Salem, Fayetteville, Wilmington — housing, employment, legal, healthcare (30–50 program-level rows).
> Phase 3/4: Recovery housing, fair-chance employers, specialty gaps via `north_carolina_phase4_expansion.py`.
> Phase 3b: DSS sync + gap-fill until ≥90% county pins.
>
> Output: `data/north-carolina-resources.csv` + `data/north-carolina-research-log.csv`.
> Deliver post-research coverage report before seed/deploy.

See [`multi-state-resource-research.md`](./multi-state-resource-research.md) for full field definitions, category minimums, and completion checklist.
