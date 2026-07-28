# Texas Reentry Resource Discovery Prompt

State-specific research prompt for **Texas** in the **Road to Reentry Library**. Based on [`multi-state-resource-research.md`](./multi-state-resource-research.md) — follow all field semantics, quality rules, and pipeline steps there unless overridden below.

**Replace in handoffs:** `{STATE}` = Texas, `{state-slug}` = `texas`, UUID prefix = `e1000001`.

---

## Texas context

- **254 counties.** Use official names from `src/lib/texas/counties.ts` (`DeWitt`, `La Salle`, `McLennan`, `Deaf Smith`).
- **Major metros (Phase 2 priority):**
  - Houston metro — Harris, Fort Bend, Montgomery, Brazoria, Galveston
  - Dallas–Fort Worth — Dallas, Tarrant, Collin, Denton
  - San Antonio — Bexar, Comal, Guadalupe
  - Austin — Travis, Williamson, Hays
  - El Paso, Rio Grande Valley, Corpus Christi, Lubbock
- **Correctional hubs:** TDCJ units statewide, regional parole offices, county jails in major metros.

---

## State-specific search terms & agencies

### Phase 1 — Statewide backbone

| Agency / program | Search terms | Primary URLs |
| --- | --- | --- |
| **TDCJ Reentry** | `TDCJ reentry`, `Texas DOC release planning` | tdcj.texas.gov/divisions/rrd |
| **TDCJ Parole** | `Texas parole division`, `TDCJ mandatory supervision` | tdcj.texas.gov/divisions/pd |
| **Your Texas Benefits** | `Your Texas Benefits SNAP Medicaid`, `yourtexasbenefits.com` | yourtexasbenefits.com |
| **Texas Medicaid** | `Texas Medicaid CHIP HHSC` | hhs.texas.gov/services/health/medicaid-chip |
| **211 Texas** | `211 Texas reentry`, `211texas.org` | 211texas.org |
| **Legal aid network** | `Lone Star Legal Aid`, `Texas RioGrande Legal Aid`, `Texas Law Help` | lonestarlegal.org, trla.org, texaslawhelp.org |
| **Workforce Solutions** | `Workforce Solutions Texas WIOA`, `twc.texas.gov find work` | twc.texas.gov |
| **Texas Veterans Commission** | `Texas Veterans Commission county VSO` | tvc.texas.gov |
| **DPS / vital records** | `Texas DPS ID`, `Texas vital records birth certificate` | dps.texas.gov, dshs.texas.gov/vital-statistics |
| **988 / SAMHSA** | `988 Texas`, `FindTreatment.gov Texas` | 988lifeline.org, findtreatment.gov |
| **Reentry orgs** | `Unlocking DOORS Dallas`, `Career and Recovery Resources Houston`, `Texas CJC` | unlockingdoors.org, crrhouston.org, texascjc.org |

### Phase 2 — Major metros

```text
"Houston" OR "Harris County" reentry programs formerly incarcerated SEARCH The Way Home
"Dallas" OR "Dallas County" reentry housing Unlocking DOORS Exodus Ministries
"San Antonio" OR "Bexar County" reentry employment Workforce Solutions Alamo
"Austin" OR "Travis County" reentry housing Foundation Communities Texas CJC
"Fort Worth" OR "Tarrant County" reentry coalition probation parole
"El Paso" reentry programs justice involved Project Vida
"Texas" recovery housing "justice involved" parole probation
```

### Phase 3b — County depth

For each uncovered county:

```text
"{COUNTY} county" Texas Your Texas Benefits SNAP Medicaid HHSC
"{COUNTY}" TDCJ parole office Texas
"{COUNTY}" Workforce Solutions Texas WIOA
"{COUNTY}" Texas FQHC community health center
"{COUNTY}" Texas local health entity DSHS
"{COUNTY}" food bank pantry Texas
"{COUNTY}" GED adult education Texas community college
"211 {COUNTY} Texas" reentry
```

**Locality benefits sync (mandatory):**

```bash
python3 scripts/sync-county-benefits-offices.py --state texas
```

Registers all 254 county HHSC benefits offices via `register_county_benefits_texas` in `scripts/county_benefits_registry.py`.

---

## Row-count & coverage targets

| Phase | Target | Notes |
| --- | --- | --- |
| Phase 1 backbone | ~18 | Statewide agencies, hotlines, legal/employment anchors |
| Phase 2 metros | ~40–80 | Houston, DFW, San Antonio, Austin, El Paso depth |
| Phase 3b mechanical | ~508 | Workforce Solutions + local health entity per county |
| County benefits | 254 | One HHSC/Your Texas Benefits row per county |
| **Total stretch** | **800+** | Tier A depth in all 254 counties |

---

## Build commands

```bash
python3 scripts/bootstrap_texas_state.py   # regenerate scaffold (if needed)
python3 scripts/sync-county-benefits-offices.py --state texas
python3 scripts/build-texas-resources.py
python3 scripts/enrich-resources.py data/texas-resources.csv --write-json data/enrichments/texas-enriched.json
python3 scripts/check-county-coverage.py --state Texas --tier-a --report
```
