# Illinois Reentry Resource Discovery Prompt

State-specific research prompt for **Illinois** in the **Road to Reentry Library**. Based on [`multi-state-resource-research.md`](./multi-state-resource-research.md) — follow all field semantics, quality rules, and pipeline steps there unless overridden below.

**Replace in handoffs:** `{STATE}` = Illinois, `{state-slug}` = `illinois`, UUID prefix = `d6000001`.

---

## Illinois context

- **102 counties** (official list in `src/lib/illinois/counties.ts`)
- **Benefits offices:** IDHS FCRC county/local offices via `illinois-idhs-offices.json`
- **Major metros (Phase 2 priority):** Chicago/Cook, Aurora/DuPage-Kane, Rockford/Winnebago, Peoria, Springfield/Sangamon, Metro East
- **Correctional hubs:** IDOC facilities, Cook County Jail, probation departments

---

## State-specific search terms & agencies

### Phase 1 — Statewide backbone

| Agency / program | Search terms | Primary URLs |
| --- | --- | --- |
| **IDOC Reentry** | `Illinois DOC reentry`, `illinois.gov idoc reentry` | idoc.illinois.gov |
| **IDHS / ABE** | `Illinois ABE SNAP Medicaid`, `IDHS FCRC office locator` | abe.illinois.gov |
| **211 Illinois** | `211 Illinois reentry` | 211illinois.org |
| **Legal aid** | `Illinois Legal Aid expungement`, `illinoislegalaid.org` | illinoislegalaid.org, lafchicago.org |
| **Illinois workNet** | `Illinois workNet career center reentry` | illinoisworknet.com |
| **IDVR** | `Illinois vocational rehabilitation reentry` | drs.illinois.gov |
| **DMH / SUD** | `Illinois community mental health`, `988 Illinois` | dhs.state.il.us |
| **IDVA** | `Illinois Department of Veterans Affairs` | illinois.gov/veterans |

### Phase 2 — Major metros

```text
"Illinois" reentry housing employment justice involved
"Illinois" recovery housing parole probation
"Chicago/Cook" reentry programs
"Aurora/DuPage-Kane" reentry programs
"Rockford/Winnebago" reentry programs
"Peoria" reentry programs
```

### Phase 3b — County depth

For each uncovered county:

```text
"{COUNTY} county" Illinois IDHS FCRC SNAP Medicaid
"{COUNTY} county" Illinois probation parole
"{COUNTY} county" Illinois workforce career center
"{COUNTY} county" Illinois FQHC community health
"{COUNTY} county" Illinois food bank pantry
"{COUNTY} county" GED adult education Illinois
```

**Local benefits sync (mandatory):**

```bash
python3 scripts/sync-county-benefits-offices.py --state illinois
```

Registers all 102 county offices via `register_county_benefits_illinois` in `scripts/county_benefits_registry.py`.

---

## Row-count & coverage targets

| Metric | Target |
| --- | --- |
| Total rows | **320–400+** (102 counties) |
| County pin coverage | **≥90%** of 102 counties |
| County benefits pins | **100%** via registry |
| Tier A core depth | **≥50%** stretch (≥3 of 8 core categories per county) |
| Category minimums | All 17 slugs per multi-state prompt |

---

## Pipeline (Illinois)

```bash
python3 scripts/sync-county-benefits-offices.py --state illinois
python3 scripts/build-illinois-resources.py
python3 scripts/check-county-coverage.py data/illinois-resources.csv src/lib/illinois/counties.ts --tier-a --report
python3 scripts/enrich-resources.py --check-only data/illinois-resources.csv
npm run db:push:illinois
```

**Build script:** `scripts/build-illinois-resources.py`  
**County benefits:** `scripts/data/illinois-idhs-offices.json`

---

## Start command

> **Begin research for Illinois.**
>
> Phase 1: Statewide backbone agencies in table above (18–22 rows).
> Phase 2: Chicago, Aurora, Rockford, Peoria, Springfield — housing, employment, legal, healthcare (25–35 program-level rows).
> Phase 3/4: Recovery housing, fair-chance employers, specialty gaps via state expansion modules.
> Phase 3b: IDHS FCRC county registry + gap-fill until ≥90% county pins and Tier A stretch.
>
> Output: `data/illinois-resources.csv` + `data/illinois-research-log.csv`.
> Deliver post-research coverage report before seed/deploy.
