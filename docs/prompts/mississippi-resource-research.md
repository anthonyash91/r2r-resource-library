# Mississippi Reentry Resource Discovery Prompt

State-specific research prompt for **Mississippi** in the **Road to Reentry Library**. Based on [`multi-state-resource-research.md`](./multi-state-resource-research.md) — follow all field semantics, quality rules, and pipeline steps there unless overridden below.

**Replace in handoffs:** `{STATE}` = Mississippi, `{state-slug}` = `mississippi`, UUID prefix = `df000001`.

---

## Mississippi context

- **82 counties** (official list in `src/lib/mississippi/counties.ts`; use **DeSoto** and **Jefferson Davis** per state convention)
- **MDHS / ACCESS:** SNAP, TANF, and Medicaid referrals flow through **access.ms.gov** and county **MDHS Economic Assistance** offices
- **MDES:** **WIN Job Centers** and **Mississippi Works** (`msworks.ms.gov`) — verify regional center addresses; do not fabricate per-county job centers with fake domains
- **DMH:** **Community Mental Health Centers** (CMHCs) are the county/regional behavioral health backbone — not a single statewide clinic row per county
- **Major metros (Phase 2 priority):**
  - Jackson / Hinds (plus Madison, Rankin)
  - Gulfport–Biloxi / Harrison (plus Hancock, Jackson counties on the coast)
  - Hattiesburg / Forrest (Pine Belt)
  - Tupelo / Lee (northeast)
  - Meridian / Lauderdale (east-central)
  - Southaven / DeSoto (northwest Memphis metro)
- **Correctional hubs:** MDOC Parchman (Sunflower), regional prisons (South Mississippi, Central Mississippi, Marshall County), county jails (Hinds, Harrison, Forrest, Lee)

---

## State-specific search terms & agencies

### Phase 1 — Statewide backbone

| Agency / program | Search terms | Primary URLs |
| --- | --- | --- |
| **MDOC Reentry** | `Mississippi DOC reentry community corrections`, `mdoc.ms.gov reentry` | mdoc.ms.gov |
| **MDOC Probation & Parole** | `MDOC probation parole field offices` | mdoc.ms.gov/ProbationParole |
| **access.ms.gov** | `access.ms.gov SNAP TANF`, `MDHS benefits Mississippi` | access.ms.gov |
| **Division of Medicaid** | `Mississippi Medicaid enrollment`, `medicaid.ms.gov` | medicaid.ms.gov |
| **211 Mississippi** | `211 Mississippi United Way`, `ms211.org` | ms211.org |
| **Mississippi Center for Legal Services** | `MS legal services expungement`, `mslegalservices.org` | mslegalservices.org |
| **Mississippi Works / WIN** | `WIN Job Center Mississippi`, `msworks.ms.gov`, `mdes.ms.gov` | msworks.ms.gov, mdes.ms.gov |
| **MDRS VR** | `Mississippi vocational rehabilitation MDRS`, `mdrs.ms.gov` | mdrs.ms.gov |
| **Mississippi Veterans Affairs** | `MS county veterans service officer`, `msva.ms.gov` | msva.ms.gov |
| **DPS Driver Services** | `Mississippi driver license ID`, `dps.ms.gov driver services` | dps.ms.gov/driver-services |
| **MSDH Vital Records** | `Mississippi birth certificate`, `msdh.ms.gov vitalrecords` | msdh.ms.gov/vitalrecords |
| **DMH** | `Mississippi DMH community mental health center`, `dmh.ms.gov` | dmh.ms.gov |
| **Mississippi Reentry Council** | `MDOC reentry council Mississippi` | mdoc.ms.gov |
| **Crisis / SUD** | `988 Mississippi`, `SAMHSA`, `findtreatment.gov` | 988lifeline.org, samhsa.gov, findtreatment.gov |

### Phase 2 — Major metros

```text
"Jackson" "Hinds county" reentry housing Stewpot Gateway Catholic Charities
"Gulfport" "Harrison county" reentry Open Doors Coastal Family Health
"Hattiesburg" "Forrest county" reentry Pine Belt mental health
"Tupelo" "Lee county" reentry WIN Job Center Salvation Army
"Meridian" "Lauderdale county" reentry Weems CMHC employment
"Southaven" "DeSoto county" reentry Mississippi Center for Re-Entry
"Mississippi" recovery housing "justice involved" parole probation
```

### Phase 3b — County depth

For each uncovered or thin county:

```text
"{COUNTY} county" Mississippi MDHS SNAP access.ms.gov
"{COUNTY} county" MDOC probation parole field office
"{COUNTY} county" WIN Job Center MDES Mississippi Works
"{COUNTY} county" DMH community mental health center
"{COUNTY} county" Mississippi hospital FQHC primary care
"{COUNTY} county" food bank pantry community action agency
"{COUNTY} county" GED adult education Mississippi
```

**County benefits registry (mandatory):**

`scripts/data/mississippi-mdhs-offices.json` + `register_county_benefits_mississippi` in `scripts/county_benefits_registry.py`.

One **financial-assistance** row per county MDHS office. Use consortium/regional MDES WIN center addresses for employment rows in rural counties — label clearly in `name` and `notes` (e.g. “Greenville WIN Job Center (serves Issaquena County)”).

**Quality notes from production dataset:**

- **Do not invent** hospital domains, per-county WIN URLs, or placeholder reentry coalitions. Replace weak rows with verified regional providers (MDES WIN pages, Forrest Health, Ochsner, Delta Health Alliance, etc.).
- **Housing authority URLs** must match the actual PHA site (e.g. Columbus → `chauthority.org`, not stale domains).
- MDOC Community Corrections rows: prefer published field office addresses; upgrade `_confidence` to `high` only when sourced from mdoc.ms.gov.
- Reentry nonprofits verified in dataset: **Mississippi Center for Re-Entry** (Southaven), **RECH Foundation M.O.R.E.**, **MARC** (`marcreentry.org`), **WWISCAA** (Sharkey–Issaquena).

---

## Row-count & coverage targets

| Metric | Target |
| --- | --- |
| Total rows | **250–350+** (82 counties — rural depth is mandatory) |
| County pin coverage | **≥90%** of 82 counties |
| County MDHS FA pins | **100%** via registry |
| Tier A core (≥3 of 8 categories) | **≥50%** counties (stretch higher) |
| Category minimums | All 17 slugs per multi-state prompt |
| Low-confidence (`medium`) rows | **0** at deploy — verify phones/URLs or replace |

---

## Pipeline (Mississippi)

```bash
python3 scripts/sync-county-benefits-offices.py --state mississippi   # if sync wired; else verify mississippi-mdhs-offices.json
python3 scripts/build-mississippi-resources.py
python3 scripts/check-county-coverage.py data/mississippi-resources.csv src/lib/mississippi/counties.ts --tier-a --report
python3 scripts/enrich-resources.py --check-only data/mississippi-resources.csv
npm run db:push:mississippi
```

**Build script:** `scripts/build-mississippi-resources.py`  
**County benefits:** `register_county_benefits_mississippi` in `scripts/county_benefits_registry.py`  
**Expansion:** `scripts/mississippi_phase4_expansion.py`  
**Category fill:** `scripts/mississippi_category_fill.py`  
**Thin counties:** `scripts/mississippi_thin_counties.py`  
**Gap fill:** `scripts/mississippi_gap_fill.py` (+ `register_minimum_closure`, `register_mechanical_tier_a`, `register_tier_a_final` in gap_fill module)

---

## Start command

> **Begin research for Mississippi.**
>
> Phase 1: MDOC reentry/P&P, access.ms.gov, Division of Medicaid, 211, Mississippi Center for Legal Services, Mississippi Works/WIN, MDRS, MSVA, DPS, MSDH vital records, DMH, Mississippi Reentry Council, 988/SAMHSA/FindTreatment (18–25 rows).
> Phase 2: Jackson/Hinds, Gulf Coast/Harrison, Hattiesburg/Forrest, Tupelo/Lee, Meridian/Lauderdale, DeSoto — housing, employment, legal, healthcare (30–50 program-level rows).
> Phase 3/4: Recovery housing, CMHCs, fair-chance employers via `mississippi_phase4_expansion.py`.
> Phase 3b: MDHS county registry + `mississippi_thin_counties.py` + gap-fill until **≥90%** county pins, Tier A depth, and **0** medium-confidence rows.
>
> Output: `data/mississippi-resources.csv` + `data/mississippi-research-log.csv`.
> Deliver post-research coverage report before seed/deploy.

See [`multi-state-resource-research.md`](./multi-state-resource-research.md) for full field definitions, category minimums, and completion checklist.
