# Virginia Reentry Resource Discovery Prompt

State-specific research prompt for **Virginia** in the **Road to Reentry Library**. Based on [`multi-state-resource-research.md`](./multi-state-resource-research.md) — follow all field semantics, quality rules, and pipeline steps there unless overridden below.

**Replace in handoffs:** `{STATE}` = Virginia, `{state-slug}` = `virginia`, UUID prefix = `da000001`.

---

## Virginia context

- **133 localities: 95 counties + 38 independent cities.** Virginia's independent cities (Richmond, Norfolk, Virginia Beach, Roanoke, etc.) are **not** part of any county — treat each as its own locality in `county` / `served_counties` (official list in `src/lib/virginia/counties.ts`).
- **Major metros (Phase 2 priority):**
  - Hampton Roads — Virginia Beach, Norfolk, Chesapeake, Newport News, Hampton, Portsmouth, Suffolk
  - Richmond metro — Richmond city, Henrico, Chesterfield
  - Northern Virginia — Fairfax, Arlington, Alexandria, Prince William, Loudoun
  - Roanoke / Roanoke County / Salem
  - Lynchburg
  - Charlottesville / Albemarle
- **Correctional hubs:** VADOC prisons across the state (Greensville, Nottoway, Buckingham, Augusta, Red Onion, Fluvanna women's), regional jails (Hampton Roads, Riverside, Rappahannock, Blue Ridge, Middle River), and probation & parole district offices (~43 districts).

---

## State-specific search terms & agencies

### Phase 1 — Statewide backbone

| Agency / program | Search terms | Primary URLs |
| --- | --- | --- |
| **VADOC Reentry** | `VADOC reentry`, `Virginia DOC reentry and reintegration` | vadoc.virginia.gov |
| **VADOC Probation & Parole** | `Virginia probation parole district offices` | vadoc.virginia.gov |
| **CommonHelp / VDSS** | `CommonHelp Virginia SNAP Medicaid`, `VDSS benefits` | commonhelp.virginia.gov, dss.virginia.gov |
| **Virginia 211** | `211 Virginia reentry`, `211virginia.org` | 211virginia.org |
| **Legal aid network** | `Virginia legal aid expungement record sealing`, `valegalaid.org` | valegalaid.org, lsnv.org, cvlas.org |
| **Virginia Career Works** | `Virginia Career Works center`, `Virginia workforce reentry` | virginiacareerworks.com |
| **DARS** | `Virginia DARS vocational rehabilitation reentry` | vadars.org |
| **CSBs / 988** | `Virginia community services board directory`, `988 Virginia` | dbhds.virginia.gov, 988lifeline.org |
| **Virginia CARES** | `Virginia CARES reentry`, `vacares.org` | vacares.org |
| **OAR chapters** | `Offender Aid and Restoration Virginia` | oaronline.org (per-chapter) |
| **DMV ID** | `Virginia DMV ID released from prison`, `DMV Connect` | dmv.virginia.gov |
| **Veterans** | `Virginia Department of Veterans Services`, `Virginia Veteran and Family Support` | dvs.virginia.gov |

### Phase 2 — Major metros

```text
"Richmond" reentry programs formerly incarcerated
"Henrico" OR "Chesterfield" transitional housing reentry
"Norfolk" OR "Virginia Beach" reentry employment Hampton Roads
"Newport News" OR "Hampton" reentry housing
"Fairfax" OR "Arlington" OR "Alexandria" reentry expungement legal aid
"Roanoke" reentry programs justice involved
"Lynchburg" OR "Charlottesville" reentry housing employment
"Virginia" recovery housing "justice involved" parole probation
```

### Phase 3b — Small-locality depth

For each uncovered county or independent city:

```text
"{LOCALITY} county" Virginia DSS SNAP Medicaid
"{LOCALITY}" Virginia probation parole district office
"{LOCALITY}" Virginia Career Works center
"{LOCALITY}" Virginia FQHC community health center
"{LOCALITY}" community services board behavioral health
"{LOCALITY}" food bank pantry Virginia
"{LOCALITY}" GED adult education Virginia
"211 {LOCALITY} Virginia" reentry
```

**Locality benefits sync (mandatory):**

```bash
python3 scripts/sync-county-benefits-offices.py --state virginia
```

Registers all 120 local VDSS departments (some serve a combined city+county) via `register_county_benefits_virginia` in `scripts/county_benefits_registry.py`. Map each combined district office to **every locality it serves** in `served_counties`.

---

## Row-count & coverage targets

| Metric | Target |
| --- | --- |
| Total rows | **175–225+** (133 localities — above Kentucky density) |
| Locality pin coverage | **≥90%** of 133 localities |
| Locality DSS FA pins | **100%** via sync + registry |
| Category minimums | All 17 slugs per multi-state prompt |

---

## Pipeline (Virginia)

```bash
npm run seed:resources:virginia
python3 scripts/check-county-coverage.py data/virginia-resources.csv src/lib/virginia/counties.ts --report
python3 scripts/enrich-resources.py --check-only data/virginia-resources.csv
npm run build
```

**Build script:** `scripts/build-virginia-resources.py`
**Phase 3b:** `register_phase3b_virginia()` in `scripts/phase3b_gapfill.py`
**Expansion:** `scripts/virginia_phase4_expansion.py`

---

## Start command

> **Begin research for Virginia.**
>
> Phase 1: VADOC reentry/P&P districts, CommonHelp/VDSS, 211, legal aid network + record sealing, Virginia Career Works/DARS, CSBs/988, DMV Connect, veterans, Virginia CARES/OAR (15–25 rows).
> Phase 2: Hampton Roads, Richmond metro, Northern Virginia, Roanoke, Lynchburg, Charlottesville — housing, employment, legal, healthcare (30–50 program-level rows).
> Phase 3/4: Recovery housing, fair-chance employers, specialty gaps via `virginia_phase4_expansion.py`.
> Phase 3b: DSS sync + gap-fill until ≥90% locality pins (counties **and** independent cities).
>
> Output: `data/virginia-resources.csv` + `data/virginia-research-log.csv`.
> Deliver post-research coverage report before seed/deploy.

See [`multi-state-resource-research.md`](./multi-state-resource-research.md) for full field definitions, category minimums, and completion checklist.
