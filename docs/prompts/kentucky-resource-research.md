# Kentucky Reentry Resource Discovery Prompt

State-specific research prompt for **Kentucky** in the **Road to Reentry Library**. Based on [`multi-state-resource-research.md`](./multi-state-resource-research.md) — follow all field semantics, quality rules, and pipeline steps there unless overridden below.

**Replace in handoffs:** `{STATE}` = Kentucky, `{state-slug}` = `kentucky`, UUID prefix = `d1000001`.

---

## Kentucky context

- **120 counties** (official list in `src/lib/kentucky/counties.ts`)
- **Benefits offices:** DCBS county/local offices via `kentucky-dcbs-offices.json`
- **Major metros (Phase 2 priority):** Louisville/Jefferson, Lexington/Fayette, Northern Kentucky, Bowling Green, Owensboro, Eastern Kentucky coalfield
- **Correctional hubs:** KDOC institutions, county jails, probation & parole district offices

---

## State-specific search terms & agencies

### Phase 1 — Statewide backbone

| Agency / program | Search terms | Primary URLs |
| --- | --- | --- |
| **DRC Reentry** | `Kentucky corrections reentry`, `ky.gov corrections reentry` | corrections.ky.gov |
| **DCBS / kynect** | `kynect benefits SNAP Medicaid`, `DCBS local office Kentucky` | kynect.ky.gov, chfs.ky.gov |
| **211 Kentucky** | `211 Kentucky reentry` | 211.org |
| **Legal aid** | `Kentucky Legal Aid expungement`, `kyla.org` | kyla.org, lassd.org |
| **Kentucky Career Centers** | `Kentucky Career Center workforce reentry` | kcc.ky.gov |
| **OVRS** | `Kentucky vocational rehabilitation reentry` | vr.ky.gov |
| **CMHC / SUD** | `Kentucky community mental health`, `findhelp Kentucky SUD` | dbhdid.ky.gov |
| **KCVS** | `Kentucky Department of Veterans Affairs` | veterans.ky.gov |

### Phase 2 — Major metros

```text
"Kentucky" reentry housing employment justice involved
"Kentucky" recovery housing parole probation
"Louisville/Jefferson" reentry programs
"Lexington/Fayette" reentry programs
"Northern Kentucky" reentry programs
"Bowling Green" reentry programs
```

### Phase 3b — County depth

For each uncovered county:

```text
"{COUNTY} county" Kentucky DCBS SNAP Medicaid
"{COUNTY} county" Kentucky probation parole
"{COUNTY} county" Kentucky workforce career center
"{COUNTY} county" Kentucky FQHC community health
"{COUNTY} county" Kentucky food bank pantry
"{COUNTY} county" GED adult education Kentucky
```

**Local benefits sync (mandatory):**

```bash
python3 scripts/sync-county-benefits-offices.py --state kentucky
```

Registers all 120 county offices via `register_county_benefits_kentucky` in `scripts/county_benefits_registry.py`.

---

## Row-count & coverage targets

| Metric | Target |
| --- | --- |
| Total rows | **350–450+** (120 counties) |
| County pin coverage | **≥90%** of 120 counties |
| County benefits pins | **100%** via registry |
| Tier A core depth | **≥50%** stretch (≥3 of 8 core categories per county) |
| Category minimums | All 17 slugs per multi-state prompt |

---

## Pipeline (Kentucky)

```bash
python3 scripts/sync-county-benefits-offices.py --state kentucky
python3 scripts/build-kentucky-resources.py
python3 scripts/check-county-coverage.py data/kentucky-resources.csv src/lib/kentucky/counties.ts --tier-a --report
python3 scripts/enrich-resources.py --check-only data/kentucky-resources.csv
npm run db:push:kentucky
```

**Build script:** `scripts/build-kentucky-resources.py`  
**County benefits:** `scripts/data/kentucky-dcbs-offices.json`

---

## Start command

> **Begin research for Kentucky.**
>
> Phase 1: Statewide backbone agencies in table above (18–22 rows).
> Phase 2: Louisville, Lexington, Northern Kentucky, Bowling Green — housing, employment, legal, healthcare (25–35 program-level rows).
> Phase 3/4: Recovery housing, fair-chance employers, specialty gaps via state expansion modules.
> Phase 3b: DCBS county registry + gap-fill until ≥90% county pins and Tier A stretch.
>
> Output: `data/kentucky-resources.csv` + `data/kentucky-research-log.csv`.
> Deliver post-research coverage report before seed/deploy.
