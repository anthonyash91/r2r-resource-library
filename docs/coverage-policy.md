# Resource coverage policy

This document defines how we judge geographic and category completeness for the Resource Library. It matches how filters and search behave in the app.

## Three tiers (not one flat rule)

### State level — required

Every deployed state must have:

- All **17 category slugs** represented with **program-level rows** (not coalitions standing in for housing, health, etc.)
- **Category minimums** per `docs/prompts/multi-state-resource-research.md`
- A **statewide backbone** (211, benefits portal, legal help hub, crisis lines, DOC/reentry navigation)
- **≤25%** coalition/referral-only rows unless documented in the research log

### County level — required

Every official county should have **actionable local depth**:

- **≥90%** of counties pinned by at least one **single** or **multi** row (`statewide` rows do not count)
- **Jail counties** never at zero without a documented gap in `{state}-research-log.csv`
- **Thin counties** (only 1 pin) pushed toward **2+ direct-service pins** where verifiable providers exist
- **Multi-county rows** must list every served county explicitly in `served_counties`

**Good rural minimum** (local or regional, not statewide):

- Benefits intake (county JFS / DCBS / DHS) **or** regional benefits navigator
- Probation/parole or community corrections touchpoint
- At least one of: food pantry, FQHC/behavioral health, workforce/AJC, legal aid (regional OK if counties are named)

### Category × county — primary north-star (filter UX)

**Goal:** at least **one local or regional** resource per **Tier A** category per county
(so county-scoped category filters are never empty when statewide help exists elsewhere).

| Metric | Meaning | Current (run scorecard) |
| --- | --- | --- |
| **Tier A slot fill %** | Share of county×Tier A slots with ≥1 local/regional row | `python3 scripts/check-tier-a-county-coverage.py` |
| **Full Tier A counties** | Counties with all 8 Tier A categories locally | scorecard JSON |
| **Weak counties** | Counties with ≤3 Tier A categories locally | scorecard JSON |

**Targets**

| Horizon | Tier A slot fill | Full Tier A counties | Weak counties (≤3 Tier A) |
| --- | --- | --- | --- |
| Floor (no regression) | ≥50% | — | — |
| 90-day | **≥70%** | ≥40 | ≤60 |
| Stretch | ≥85% | — | — |

Regional/multi-county rows **count** toward every county listed in `served_counties`.
Do not invent per-county duplicates when one verified regional provider exists.

**Tier B** (education, veterans, basic-needs, id-documentation, transportation,
peer-support, family-children, reentry-organizations): add after Tier A depth; metro/regional
acceptable. See `data/research-backlog-phase2.csv`.

**Tier C** (`state-agency`): statewide acceptable; not part of slot-fill metric.

Legacy note: the older “≥3 of 8 Tier A core categories per county” rule remains a useful
pin-depth check (`check-county-coverage.py --tier-a`) but is **not** the primary goal.

## Product behavior

| View | Behavior |
| --- | --- |
| State only | Full category/service lists from all state resources |
| County selected — browse | Results include **local + regional + statewide** (county split UI) |
| County selected — filter dropdowns | **Local + regional only** (no statewide filler) |
| County + service search | Same pool as dropdowns (no “option but zero results”) |

When a county has no local/regional match for a service, the dropdown omits that service and copy explains statewide programs may still appear in results.

## Auditing

```bash
# Primary scorecard (Tier A county×category slot fill)
python3 scripts/check-tier-a-county-coverage.py
npm run audit:coverage          # scorecard + gap roadmap + research backlog

# Pin count (≥90% target)
python3 scripts/check-county-coverage.py data/{state}-resources.csv src/lib/{state}/counties.ts

# Tier A core depth (≥50% of counties with ≥3 core categories — legacy stretch)
python3 scripts/check-county-coverage.py data/{state}-resources.csv src/lib/{state}/counties.ts --tier-a

# Data quality (category slugs, statewide portals, served_counties)
python3 scripts/audit-data-quality.py
python3 scripts/audit-data-quality.py --fix-categories --fix-statewide-portals --fix-statewide-served-counties

# Featured suggestions for thin categories
python3 scripts/suggest-featured-resources.py
```

Outputs: `data/coverage-scorecard.json`, `docs/content-roadmap-category-gaps.md`,
`data/research-backlog-phase1.csv`, `data/research-backlog-phase2.csv`.

Gap-fill reproducibly via `scripts/phase3b_gapfill.py`, `scripts/county_benefits_registry.py`, and state build pipelines (`npm run seed:resources:{state}`).

**County benefits (mandatory before COMPLETE):** every official county must have a `financial-assistance` pin from the county intake office (JFS / TDHS / DFR / DCBS). Sync official locators into `scripts/data/{state}-*-offices.json` with `scripts/sync-county-benefits-offices.py`, then register rows mechanically in the build pipeline—do not log as a research GAP when the provider exists statewide per county.

**Ohio CDJFS:** sync uses the official ODJFS [County Directory PDF](https://dam.assets.ohio.gov/image/upload/jfs.ohio.gov/County/County_Directory.pdf) (requires `pip3 install -r scripts/requirements-data.txt`). After sync, run `python3 scripts/patch-ohio-cdjfs-from-json.py` to upgrade existing CSV stub rows.

After gap-fill, produce the **Post-research coverage report** defined in `docs/prompts/multi-state-resource-research.md` (or run `check-county-coverage.py --report` for an automated draft).

## When to stop researching

If no published provider exists after 211 + county benefits office + sheriff/probation + state directory search, **log the gap** — do not invent a listing.
