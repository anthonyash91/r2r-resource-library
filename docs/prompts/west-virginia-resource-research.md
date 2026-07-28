# West Virginia Reentry Resource Discovery Prompt

State-specific research prompt for **West Virginia** in the **Road to Reentry Library**. Based on [`multi-state-resource-research.md`](./multi-state-resource-research.md) — follow all field semantics, quality rules, and pipeline steps there unless overridden below.

**Replace in handoffs:** `{STATE}` = West Virginia, `{state-slug}` = `west-virginia`, UUID prefix = `d7000001`.

---

## West Virginia context

- **55 counties** (official list in `src/lib/west-virginia/counties.ts`)
- **Benefits offices:** DOHS county/local offices via `west-virginia-dohs-offices.json`
- **Major metros (Phase 2 priority):** Charleston/Kanawha, Huntington/Cabell-Wayne, Morgantown/Monongalia, Wheeling/Ohio, Beckley/Raleigh
- **Correctional hubs:** DIVR prisons, regional jails, probation & parole offices

---

## State-specific search terms & agencies

### Phase 1 — Statewide backbone

| Agency / program | Search terms | Primary URLs |
| --- | --- | --- |
| **DIVR Reentry** | `West Virginia corrections reentry`, `wv.gov corrections reentry` | wv.gov/corrections |
| **WV DHHR / PATH** | `West Virginia PATH SNAP Medicaid`, `DOHS county office` | dhhr.wv.gov |
| **WV 211** | `211 West Virginia reentry` | wv211.org |
| **Legal aid** | `Legal Aid of West Virginia expungement` | lawv.net |
| **WorkForce WV** | `WorkForce West Virginia career center reentry` | workforcewv.org |
| **WV Division of Rehabilitation Services** | `WV vocational rehabilitation reentry` | wvdrs.org |
| **LHD / CSB** | `West Virginia local health department`, `988 West Virginia` | dhhr.wv.gov |
| **WV DVS** | `West Virginia Department of Veterans Assistance` | veterans.wv.gov |

### Phase 2 — Major metros

```text
"West Virginia" reentry housing employment justice involved
"West Virginia" recovery housing parole probation
"Charleston/Kanawha" reentry programs
"Huntington/Cabell-Wayne" reentry programs
"Morgantown/Monongalia" reentry programs
"Wheeling/Ohio" reentry programs
```

### Phase 3b — County depth

For each uncovered county:

```text
"{COUNTY} county" West Virginia DOHS SNAP Medicaid
"{COUNTY} county" West Virginia probation parole
"{COUNTY} county" West Virginia workforce career center
"{COUNTY} county" West Virginia FQHC community health
"{COUNTY} county" West Virginia food bank pantry
"{COUNTY} county" GED adult education West Virginia
```

**Local benefits sync (mandatory):**

```bash
python3 scripts/sync-county-benefits-offices.py --state west-virginia
```

Registers all 55 county offices via `register_county_benefits_west_virginia` in `scripts/county_benefits_registry.py`.

---

## Row-count & coverage targets

| Metric | Target |
| --- | --- |
| Total rows | **220–300+** (55 counties) |
| County pin coverage | **≥90%** of 55 counties |
| County benefits pins | **100%** via registry |
| Tier A core depth | **≥50%** stretch (≥3 of 8 core categories per county) |
| Category minimums | All 17 slugs per multi-state prompt |

---

## Pipeline (West Virginia)

```bash
python3 scripts/sync-county-benefits-offices.py --state west-virginia
python3 scripts/build-west-virginia-resources.py
python3 scripts/check-county-coverage.py data/west-virginia-resources.csv src/lib/west-virginia/counties.ts --tier-a --report
python3 scripts/enrich-resources.py --check-only data/west-virginia-resources.csv
npm run db:push:west-virginia
```

**Build script:** `scripts/build-west-virginia-resources.py`  
**County benefits:** `scripts/data/west-virginia-dohs-offices.json`

---

## Start command

> **Begin research for West Virginia.**
>
> Phase 1: Statewide backbone agencies in table above (18–22 rows).
> Phase 2: Charleston, Huntington, Morgantown, Wheeling, Beckley — housing, employment, legal, healthcare (25–35 program-level rows).
> Phase 3/4: Recovery housing, fair-chance employers, specialty gaps via state expansion modules.
> Phase 3b: DOHS county registry + gap-fill until ≥90% county pins and Tier A stretch.
>
> Output: `data/west-virginia-resources.csv` + `data/west-virginia-research-log.csv`.
> Deliver post-research coverage report before seed/deploy.
