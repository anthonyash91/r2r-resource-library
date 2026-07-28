# Ohio Reentry Resource Discovery Prompt

State-specific research prompt for **Ohio** in the **Road to Reentry Library**. Based on [`multi-state-resource-research.md`](./multi-state-resource-research.md) — follow all field semantics, quality rules, and pipeline steps there unless overridden below.

**Replace in handoffs:** `{STATE}` = Ohio, `{state-slug}` = `ohio`, UUID prefix = `d2000001`.

---

## Ohio context

- **88 counties** (official list in `src/lib/ohio/counties.ts`)
- **Benefits offices:** CDJFS county/local offices via `ohio-cdjfs-offices.json`
- **Major metros (Phase 2 priority):** Columbus/Franklin, Cleveland/Cuyahoga, Cincinnati/Hamilton, Dayton/Montgomery, Akron/Summit, Toledo/Lucas
- **Correctional hubs:** DRC prisons, county jails, adult probation departments

---

## State-specific search terms & agencies

### Phase 1 — Statewide backbone

| Agency / program | Search terms | Primary URLs |
| --- | --- | --- |
| **DRC Reentry** | `Ohio DRC reentry`, `ohio.gov corrections reentry` | drc.ohio.gov |
| **ODJFS / Ohio Benefits** | `Ohio Benefits SNAP Medicaid`, `CDJFS county office` | benefits.ohio.gov |
| **Ohio 211** | `211 Ohio reentry` | 211.org |
| **Legal aid network** | `Ohio legal aid expungement sealing`, `ohiolegalhelp.org` | ohiolegalhelp.org, lasclev.org |
| **OhioMeansJobs** | `OhioMeansJobs center reentry`, `workforce Ohio reentry` | ohiomeansjobs.ohio.gov |
| **Opportunities for Ohioans with Disabilities** | `OOD vocational rehabilitation Ohio` | ood.ohio.gov |
| **OhioMHAS / ADAMHS boards** | `Ohio mental health board directory`, `988 Ohio` | mha.ohio.gov |
| **Ohio DVS** | `Ohio Department of Veterans Services` | dvs.ohio.gov |

### Phase 2 — Major metros

```text
"Ohio" reentry housing employment justice involved
"Ohio" recovery housing parole probation
"Columbus/Franklin" reentry programs
"Cleveland/Cuyahoga" reentry programs
"Cincinnati/Hamilton" reentry programs
"Dayton/Montgomery" reentry programs
```

### Phase 3b — County depth

For each uncovered county:

```text
"{COUNTY} county" Ohio CDJFS SNAP Medicaid
"{COUNTY} county" Ohio probation parole
"{COUNTY} county" Ohio workforce career center
"{COUNTY} county" Ohio FQHC community health
"{COUNTY} county" Ohio food bank pantry
"{COUNTY} county" GED adult education Ohio
```

**Local benefits sync (mandatory):**

```bash
python3 scripts/sync-county-benefits-offices.py --state ohio
```

Registers all 88 county offices via `register_county_benefits_ohio` in `scripts/county_benefits_registry.py`.

---

## Row-count & coverage targets

| Metric | Target |
| --- | --- |
| Total rows | **280–350+** (88 counties) |
| County pin coverage | **≥90%** of 88 counties |
| County benefits pins | **100%** via registry |
| Tier A core depth | **≥50%** stretch (≥3 of 8 core categories per county) |
| Category minimums | All 17 slugs per multi-state prompt |

---

## Pipeline (Ohio)

```bash
python3 scripts/sync-county-benefits-offices.py --state ohio
python3 scripts/build-ohio-resources.py
python3 scripts/check-county-coverage.py data/ohio-resources.csv src/lib/ohio/counties.ts --tier-a --report
python3 scripts/enrich-resources.py --check-only data/ohio-resources.csv
npm run db:push:ohio
```

**Build script:** `scripts/build-ohio-resources.py`  
**County benefits:** `scripts/data/ohio-cdjfs-offices.json`

---

## Start command

> **Begin research for Ohio.**
>
> Phase 1: Statewide backbone agencies in table above (18–22 rows).
> Phase 2: Columbus, Cleveland, Cincinnati, Dayton, Akron, Toledo — housing, employment, legal, healthcare (25–35 program-level rows).
> Phase 3/4: Recovery housing, fair-chance employers, specialty gaps via state expansion modules.
> Phase 3b: CDJFS county registry + gap-fill until ≥90% county pins and Tier A stretch.
>
> Output: `data/ohio-resources.csv` + `data/ohio-research-log.csv`.
> Deliver post-research coverage report before seed/deploy.
