# Wisconsin Reentry Resource Discovery Prompt

State-specific research prompt for **Wisconsin** in the **Road to Reentry Library**. Based on [`multi-state-resource-research.md`](./multi-state-resource-research.md) — follow all field semantics, quality rules, and pipeline steps there unless overridden below.

**Replace in handoffs:** `{STATE}` = Wisconsin, `{state-slug}` = `wisconsin`, UUID prefix = `e0000001`.

---

## Wisconsin context

- **72 counties.** Use official names from `src/lib/wisconsin/counties.ts` (`Fond du Lac`, `La Crosse`, `St. Croix`).
- **Major metros (Phase 2 priority):**
  - Milwaukee metro — Milwaukee, Waukesha, Washington, Ozaukee
  - Madison / Dane County
  - Green Bay / Brown County, Fox Valley (Appleton, Oshkosh)
  - Kenosha / Racine corridor
  - La Crosse, Eau Claire (western Wisconsin)
- **Correctional hubs:** WDOC adult institutions statewide, regional probation/parole offices (Regions 1–8), county jails in major metros.

---

## State-specific search terms & agencies

### Phase 1 — Statewide backbone

| Agency / program | Search terms | Primary URLs |
| --- | --- | --- |
| **WDOC Reentry** | `WDOC reentry`, `Wisconsin DOC community corrections` | doc.wi.gov |
| **WDOC Probation & Parole** | `Wisconsin probation parole regional offices` | doc.wi.gov |
| **ACCESS Wisconsin** | `ACCESS Wisconsin FoodShare BadgerCare`, `access.wi.gov` | access.wi.gov |
| **ForwardHealth / BadgerCare Plus** | `BadgerCare Plus Medicaid Wisconsin` | dhs.wisconsin.gov/badgercareplus |
| **211 Wisconsin** | `211 Wisconsin reentry`, `211wisconsin.org` | 211wisconsin.org |
| **Legal aid network** | `Legal Action of Wisconsin`, `Wisconsin Judicare expungement` | legalaction.org, judicare.org |
| **Job Center of Wisconsin** | `Job Center of Wisconsin WIOA`, `wisconsinjobcenter.org` | wisconsinjobcenter.org |
| **DVR** | `Wisconsin DVR vocational rehabilitation reentry` | dwd.wisconsin.gov/dvr |
| **WDVA** | `Wisconsin Department of Veterans Affairs county VSO` | dva.wisconsin.gov |
| **DMV / vital records** | `Wisconsin DMV ID`, `Wisconsin vital records birth certificate` | wisdot.gov, dhs.wisconsin.gov/vitalrecords |
| **988 / CCS** | `988 Wisconsin`, `Wisconsin Comprehensive Community Services CCS` | 988lifeline.org, dhs.wisconsin.gov/ccs |
| **Reentry orgs** | `Wisconsin Community Services reentry`, `JustDane formerly incarcerated` | wiscs.org, justdane.org |

### Phase 2 — Major metros

```text
"Milwaukee" reentry programs formerly incarcerated Guest House Hope House
"Madison" OR "Dane County" reentry housing JustDane Porchlight
"Green Bay" OR "Brown County" homeless shelter reentry NEW Community Shelter
"Kenosha" OR "Racine" reentry employment housing HALO Hope Center
"Appleton" OR "Fox Valley" reentry housing employment
"La Crosse" OR "Eau Claire" reentry programs justice involved
"Wisconsin" recovery housing "justice involved" parole probation
```

### Phase 3b — County depth

For each uncovered county:

```text
"{COUNTY} county" Wisconsin DHS ACCESS FoodShare BadgerCare
"{COUNTY}" WDOC probation parole regional office
"{COUNTY}" Job Center of Wisconsin
"{COUNTY}" Wisconsin FQHC community health center
"{COUNTY}" Wisconsin CCS behavioral health
"{COUNTY}" food bank pantry Wisconsin
"{COUNTY}" GED adult education Wisconsin technical college
"211 {COUNTY} Wisconsin" reentry
```

**Locality benefits sync (mandatory):**

```bash
python3 scripts/sync-county-benefits-offices.py --state wisconsin
```

Registers all 72 county DHS Eligibility Management offices via `register_county_benefits_wisconsin` in `scripts/county_benefits_registry.py`.

---

## Row-count & coverage targets

| Phase | Target | Notes |
| --- | --- | --- |
| Phase 1 | ~18 | Statewide backbone |
| Phase 2 | ~12 | Major metro anchors |
| Phase 3b | 72 FA rows | One ACCESS Wisconsin row per county via sync |
| Phase 4 | ~25 | Program-level depth in major metros |
| Mechanical depth | 72+ | Per-county job center + healthcare anchors |

**Build command:**

```bash
python3 scripts/build-wisconsin-resources.py
```

**Confidence:** `high` unless DHS office missing street address (`medium`).

**Descriptions:** 300+ characters EN and ES for every row; eligibility in `eligibility`/`eligibility_es`, operational tips in `notes`/`notes_es`.
