# Michigan Reentry Resource Discovery Prompt

State-specific research prompt for **Michigan** in the **Road to Reentry Library**. Based on [`multi-state-resource-research.md`](./multi-state-resource-research.md) — follow all field semantics, quality rules, and pipeline steps there unless overridden below.

**Replace in handoffs:** `{STATE}` = Michigan, `{state-slug}` = `michigan`, UUID prefix = `d5000001`.

---

## Michigan context

- **83 counties** (official list in `src/lib/michigan/counties.ts`)
- **Benefits offices:** MDHHS county/local offices via `michigan-mdhhs-offices.json`
- **Major metros (Phase 2 priority):** Detroit/Wayne, Grand Rapids/Kent, Lansing/Ingham, Flint/Genesee, Ann Arbor/Washtenaw
- **Correctional hubs:** MDOC facilities, county jails, probation & parole

---

## State-specific search terms & agencies

### Phase 1 — Statewide backbone

| Agency / program | Search terms | Primary URLs |
| --- | --- | --- |
| **MDOC Reentry** | `Michigan corrections reentry`, `michigan.gov corrections reentry` | michigan.gov/corrections |
| **MDHHS / MI Bridges** | `MI Bridges SNAP Medicaid`, `MDHHS county office` | mibridges.michigan.gov |
| **211 Michigan** | `211 Michigan reentry` | mi211.org |
| **Legal aid** | `Michigan legal help expungement`, `michiganlegalhelp.org` | michiganlegalhelp.org, lakeshorelegalaid.org |
| **Michigan Works!** | `Michigan Works career center reentry` | michiganworks.org |
| **MRS VR** | `Michigan Rehabilitation Services reentry` | michigan.gov/leo/bureaus-agencies/mrs |
| **CMHSP / SUD** | `Michigan community mental health`, `988 Michigan` | michigan.gov/mdhhs |
| **Michigan DVS** | `Michigan Veterans Affairs Agency` | michigan.gov/dmva |

### Phase 2 — Major metros

```text
"Michigan" reentry housing employment justice involved
"Michigan" recovery housing parole probation
"Detroit/Wayne" reentry programs
"Grand Rapids/Kent" reentry programs
"Lansing/Ingham" reentry programs
"Flint/Genesee" reentry programs
```

### Phase 3b — County depth

For each uncovered county:

```text
"{COUNTY} county" Michigan MDHHS SNAP Medicaid
"{COUNTY} county" Michigan probation parole
"{COUNTY} county" Michigan workforce career center
"{COUNTY} county" Michigan FQHC community health
"{COUNTY} county" Michigan food bank pantry
"{COUNTY} county" GED adult education Michigan
```

**Local benefits sync (mandatory):**

```bash
python3 scripts/sync-county-benefits-offices.py --state michigan
```

Registers all 83 county offices via `register_county_benefits_michigan` in `scripts/county_benefits_registry.py`.

---

## Row-count & coverage targets

| Metric | Target |
| --- | --- |
| Total rows | **280–350+** (83 counties) |
| County pin coverage | **≥90%** of 83 counties |
| County benefits pins | **100%** via registry |
| Tier A core depth | **≥50%** stretch (≥3 of 8 core categories per county) |
| Category minimums | All 17 slugs per multi-state prompt |

---

## Pipeline (Michigan)

```bash
python3 scripts/sync-county-benefits-offices.py --state michigan
python3 scripts/build-michigan-resources.py
python3 scripts/check-county-coverage.py data/michigan-resources.csv src/lib/michigan/counties.ts --tier-a --report
python3 scripts/enrich-resources.py --check-only data/michigan-resources.csv
npm run db:push:michigan
```

**Build script:** `scripts/build-michigan-resources.py`  
**County benefits:** `scripts/data/michigan-mdhhs-offices.json`

---

## Start command

> **Begin research for Michigan.**
>
> Phase 1: Statewide backbone agencies in table above (18–22 rows).
> Phase 2: Detroit, Grand Rapids, Lansing, Flint, Ann Arbor — housing, employment, legal, healthcare (25–35 program-level rows).
> Phase 3/4: Recovery housing, fair-chance employers, specialty gaps via state expansion modules.
> Phase 3b: MDHHS county registry + gap-fill until ≥90% county pins and Tier A stretch.
>
> Output: `data/michigan-resources.csv` + `data/michigan-research-log.csv`.
> Deliver post-research coverage report before seed/deploy.
