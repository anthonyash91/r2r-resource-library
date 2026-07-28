# Arizona Reentry Resource Discovery Prompt

State-specific research prompt for **Arizona** in the **Road to Reentry Library**. Based on [`multi-state-resource-research.md`](./multi-state-resource-research.md) — follow all field semantics, quality rules, and pipeline steps there unless overridden below.

**Replace in handoffs:** `{STATE}` = Arizona, `{state-slug}` = `arizona`, UUID prefix = `dd000001`.

---

## Arizona context

- **15 counties** (official list in `src/lib/arizona/counties.ts`)
- **DES regions:** Benefits and workforce services organized through county DES local offices
- **Major metros (Phase 2 priority):**
  - Phoenix / Maricopa (Valley)
  - Tucson / Pima
  - Flagstaff / Coconino
  - Yuma / Yuma & La Paz
  - Prescott / Yavapai
  - Kingman / Mohave
- **Correctional hubs:** ADCRR complexes (Florence, Perryville, Tucson, Yuma, Douglas), Maricopa and Pima county jails

---

## State-specific search terms & agencies

### Phase 1 — Statewide backbone

| Agency / program | Search terms | Primary URLs |
| --- | --- | --- |
| **ADCRR Reentry** | `Arizona corrections reentry`, `corrections.az.gov reentry` | corrections.az.gov/adcr/reentry |
| **ADCRR Community Corrections** | `Arizona parole probation community corrections` | corrections.az.gov/adcr/community-corrections |
| **Health-e-Arizona Plus** | `healthearizonaplus SNAP Medicaid`, `DES benefits Arizona` | healthearizonaplus.gov |
| **AHCCCS** | `Arizona Medicaid AHCCCS`, `azahcccs.gov` | azahcccs.gov |
| **211 Arizona** | `211 Arizona reentry`, `211arizona.org` | 211arizona.org |
| **CLS** | `Community Legal Services Arizona`, `clsaz.org` | clsaz.org |
| **DNA People's Legal** | `DNA People's Legal Services northern Arizona`, `dnaazlaw.org` | dnaazlaw.org |
| **ARIZONA@WORK** | `Arizona at Work career center`, `arizonaatwork.com` | arizonaatwork.com, des.az.gov |
| **RSA VR** | `Arizona vocational rehabilitation DES`, `des.az.gov rsa` | des.az.gov/rsa |
| **RBHA / SUD** | `Arizona behavioral health RBHA`, `AHCCCS crisis` | azahcccs.gov |
| **Arizona DVS** | `Arizona Department of Veterans Services`, `dvs.az.gov` | dvs.az.gov |
| **Arizona MVD** | `azmvdnow.gov ID`, `ServiceArizona` | azmvdnow.gov |
| **Vital records** | `Arizona vital records birth certificate` | azdhs.gov |
| **Crisis / SUD** | `988 Arizona`, `SAMHSA`, `findtreatment.gov` | 988lifeline.org, samhsa.gov, findtreatment.gov |

### Phase 2 — Major metros

```text
"Phoenix" "Maricopa county" reentry housing employment
"Tucson" "Pima county" reentry Primavera Our Family Services
"Flagstaff" "Coconino" reentry North Country HealthCare
"Yuma" reentry Crossroads Mission
"Prescott" "Yavapai" reentry housing employment
"Arizona" recovery housing "justice involved" parole probation
```

### Phase 3b — County depth

For each uncovered county:

```text
"{COUNTY} county" Arizona DES SNAP Medicaid
"{COUNTY} county" ADCRR probation parole
"{COUNTY} county" ARIZONA@WORK career center
"{COUNTY} county" Arizona FQHC community health
"{COUNTY} county" food bank Arizona
"{COUNTY} county" GED adult education Arizona
```

**County benefits registry:**

`scripts/data/arizona-des-offices.json` + `register_county_benefits_arizona` in `scripts/county_benefits_registry.py`.

---

## Row-count & coverage targets

| Metric | Target |
| --- | --- |
| Total rows | **120–180+** (15 counties — metro density + rural pins) |
| County pin coverage | **≥90%** of 15 counties |
| County DES pins | **100%** via registry |
| Category minimums | All 17 slugs per multi-state prompt |

---

## Pipeline (Arizona)

```bash
python3 scripts/build-arizona-resources.py
python3 scripts/check-county-coverage.py data/arizona-resources.csv src/lib/arizona/counties.ts --tier-a --report
python3 scripts/enrich-resources.py --check-only data/arizona-resources.csv
npm run db:push:arizona
```

**Build script:** `scripts/build-arizona-resources.py`  
**Expansion:** `scripts/arizona_phase4_expansion.py`  
**Category fill:** `scripts/arizona_category_fill.py`  
**Thin counties:** `scripts/arizona_thin_counties.py`  
**Gap fill:** `scripts/arizona_gap_fill.py`

---

## Start command

> **Begin research for Arizona.**
>
> Phase 1: ADCRR, Health-e-Arizona Plus, AHCCCS, 211, CLS, DNA People's Legal, ARIZONA@WORK, RSA VR, RBHA, DVS, MVD, vital records, 988/SAMHSA/FindTreatment (18–22 rows).
> Phase 2: Phoenix, Tucson, Flagstaff, Yuma, Prescott, Mohave — housing, employment, legal, healthcare (25–35 program-level rows).
> Phase 3/4: Recovery housing, fair-chance employers, specialty gaps via `arizona_phase4_expansion.py`.
> Phase 3b: DES county registry + gap-fill until ≥90% county pins.
>
> Output: `data/arizona-resources.csv` + `data/arizona-research-log.csv`.
> Deliver post-research coverage report before seed/deploy.
