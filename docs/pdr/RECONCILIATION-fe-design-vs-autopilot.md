# Reconciliation: `feat/howiezz-fe-design` (PR #34) vs Autopilot Design Work

**Date:** 2026-06-16
**Author:** Release-engineering read-only analysis (no code modified, no merges, no branch switches)
**Worktree:** `C:\Users\kas41\archived\HowieZZ-fe` on branch `feat/howiezz-fe-design`
**Repo:** `kas1987/HowieZZ`

---

## TL;DR

- **`feat/howiezz-fe-design` (PR #34) is the canonical frontend line.** It is a *linear descendant* of the
  `pdr-010` line (it branches off `df6cd89`, "HZZ-FE-002"). pdr-010 carries only **2 trailing chore commits**
  beyond fe-design's base.
- **The three `worktree-agent-*` branches at `782b510` are not competing work** — `782b510` is already an
  ancestor of fe-design, pdr-010, *and* `origin/main`. They are stale checkouts of already-merged code.
- **The only genuinely divergent design line is `feat/pdr-001-design-system-v2` (PR #27, tip `77f003e`).**
  It would textually conflict with fe-design in **6 HTML pages + 1 script**.
- **The stray uncommitted `index.html` in the main working dir is a regression**, not new work: it is an
  *older* homepage that is missing fe-design's mobile-responsive CTA fixes. It must be discarded.

---

## 1. Branch / PR Inventory

### Open design-relevant PRs (`gh pr list --state open`)

| PR | Title | Head branch | Tip | State |
|----|-------|-------------|-----|-------|
| **#34** | FE: Concierge Atlas frontend redesign (HZZ-FE-001..009 + premium intake) | `feat/howiezz-fe-design` | `f85bd43` | OPEN |
| #31 | PDR-010: compare funnel + analytics guardrails | `feat/pdr-010-ceo-roi-analysis` | `ae042a0` | OPEN |
| #27 | PDR-001/PDR-010: design system v2 + full competitor analysis package | `feat/pdr-001-design-system-v2` | `77f003e` | OPEN |
| #32 | PDR-011 declarative configurator (prototype) | `claude/zelex-config-ui-builder-rso32` | — | DRAFT |
| #30 | Test suite + pre-push hook | `claude/test-coverage-analysis-tnoRO` | — | DRAFT |
| #1 | dependabot setup-node 4→6 | dependabot | — | OPEN |

### Worktrees (`git worktree list`)

| Path | Branch | Tip |
|------|--------|-----|
| `C:/Users/kas41/archived/HowieZZ` (MAIN) | `feat/pdr-010-ceo-roi-analysis` | `ae042a0` (+ dirty `index.html`) |
| `C:/Users/kas41/archived/HowieZZ-fe` (THIS) | `feat/howiezz-fe-design` | `f85bd43` |
| `.claude/worktrees/agent-a0915cc58b842d46e` | `worktree-agent-a0915cc58b842d46e` | `782b510` |
| `.claude/worktrees/agent-a1386fba1f0b56967` | `worktree-agent-a1386fba1f0b56967` | `782b510` |
| `.claude/worktrees/agent-ae28a44091cbd6c97` | `worktree-agent-ae28a44091cbd6c97` | `782b510` |
| `…/Temp/howiezz-pr31-ci-check` | detached | `d093c5f` |

### Key commit hashes

| Ref | Hash |
|-----|------|
| `feat/howiezz-fe-design` (PR #34) | `f85bd43` |
| `feat/pdr-010-ceo-roi-analysis` (PR #31) | `ae042a0` |
| `origin/feat/pdr-001-design-system-v2` (PR #27) | `77f003e` |
| `worktree-agent-*` / autopilot tip | `782b510` ("PDR-001 luxury design system v2 (#25)") |
| `origin/main` | `01bb3a9` |
| fe-design's branch point off pdr line | `df6cd89` ("HZZ-FE-002: Refine luxury design system v2") |

---

## 2. Topology — who descends from whom

Verified with `git merge-base` and `git merge-base --is-ancestor`:

```
50ede02 (main base)
   └─ 782b510  ← already on origin/main, fe-design, AND pdr-010 (the "autopilot" worktrees sit here)
        └─ df6cd89 (HZZ-FE-002)  ← merge-base(fe-design, pdr-010)
             ├─ feat/howiezz-fe-design  f85bd43   (PR #34)
             └─ …d093c5f … ae042a0      feat/pdr-010-ceo-roi-analysis (PR #31)
                  (only 2 commits: ae042a0, d093c5f — both v2-HTML/community chores)

1853cf8 (PDR-001 v2 #26)  ← merge-base(fe-design, pdr-001) — SEPARATE line
   └─ … 541a0a1 … 822acca … 77f003e   feat/pdr-001-design-system-v2 (PR #27)
```

- `git merge-base --is-ancestor 782b510 feat/howiezz-fe-design` → **YES**
- `git merge-base --is-ancestor 782b510 feat/pdr-010-ceo-roi-analysis` → **YES**
- `git merge-base --is-ancestor 782b510 origin/main` → **YES**
- `git merge-base --is-ancestor 77f003e feat/howiezz-fe-design` → **NO** (pdr-001 is divergent)

**Consequence:** `782b510` and the three `worktree-agent-*` branches contribute **nothing** that is not
already merged. They are safe to ignore / delete.

---

## 3. File-Overlap Matrix

`merge-base(fe-design, pdr-010) = df6cd89`; `merge-base(fe-design, pdr-001) = 1853cf8`.

### A. fe-design vs `feat/pdr-010-ceo-roi-analysis` (base `df6cd89`)

pdr-010's only 2 unique commits beyond the shared base touch:
- `ae042a0` — `v2 HTML/*` regenerated package + `docs/handoffs/TASK-HZZ-P2-014-kickoff.md` (17 files)
- `d093c5f` — `db/community_channels.json`, `docs/handoffs/TASK-HZZ-P2-013-kickoff.md`

**No intersection with fe-design's design files** (`assets/site.css`, `assets/site.js`, `index.html`,
`contact.html`, page HTML). `git merge-tree --write-tree` → **clean, zero conflicts.**

### B. fe-design vs `feat/pdr-001-design-system-v2` (base `1853cf8`) — the real conflict

Files each side changed since `1853cf8`, and the intersection:

| File | fe-design touches | pdr-001 touches | merge-tree result |
|------|:---:|:---:|---|
| `assets/site.css` | ✅ (+197 vs pdr-010) | ✅ (+427 vs fe) | **Auto-merged (no conflict)** |
| `assets/site.js` | ✅ | ✗ | fe-only |
| `index.html` | ✅ | ✅ | **CONFLICT (content)** |
| `contact.html` | ✅ | ✅ | **CONFLICT (content)** |
| `browse.html` | ✅ | ✅ | **CONFLICT (content)** |
| `character.html` | ✅ | ✅ | **CONFLICT (content)** |
| `family.html` | ✅ | ✅ | **CONFLICT (content)** |
| `quiz.html` | ✅ | ✅ | **CONFLICT (content)** |
| `body.html` | ✅ | ✅ | Auto-merged (no conflict) |
| `craft.html` | ✗ | ✅ | pdr-001-only (auto) |
| `series.html` | ✗ | ✅ | pdr-001-only (auto) |
| `scripts/scrape_competitors.js` | ✗ (only on fe via inherited) | ✅ | **CONFLICT (content)** |
| `scripts/analyze_independent_groupings.py` etc. | ✗ | ✅ | pdr-001-only (auto) |
| `docs/PDR-005/006/007…`, `docs/agent-source-material/*` | ✗ | ✅ | pdr-001-only |

---

## 4. Files That Would TEXTUALLY CONFLICT on Merge

From `git merge-tree --write-tree --name-only feat/howiezz-fe-design origin/feat/pdr-001-design-system-v2`
(base `1853cf8`):

1. `index.html`
2. `contact.html`
3. `browse.html`
4. `character.html`
5. `family.html`
6. `quiz.html`
7. `scripts/scrape_competitors.js`

> `assets/site.css` and `body.html` **auto-merge cleanly** despite both sides editing them — git's 3-way
> merge reconciled the hunks. There are **zero conflicts** between fe-design and pdr-010.

---

## 5. Uniqueness Summary

**Only on `feat/howiezz-fe-design` (PR #34) — the FE redesign deliverables:**
- `configurator.html` — **NEW page**, absent from pdr-010 and pdr-001 (PDR-011 live configurator port).
- `contact.html` premium guided buyer-fit intake (HZZ-FE-006).
- `docs/design-packages/premium-intake/*` (Concierge Configurator/Intake reference package + `support.js`).
- `assets/site.css` FE-002 luxury system refinement (+197 lines vs pdr-010).
- `assets/site.js` redesign behaviors.
- Full `docs/pdr/PDR-FE-00x`, `docs/tickets/HZZ-FE-00x`, `docs/prompts/claude-design/*` source-of-truth set.
- Mobile-nav / CTA / overflow fixes (HZZ-FE-008, FE-010..013) — **these are the lines the stray index.html lacks.**

**Only on `feat/pdr-010-ceo-roi-analysis` (PR #31) — not in fe-design:**
- 2 trailing commits: regenerated `v2 HTML/*` snapshot bundle + manifest, and a
  `db/community_channels.json` provenance-ref fix. Both are **non-design packaging/data chores.**

**Only on `feat/pdr-001-design-system-v2` (PR #27) — divergent from fe-design:**
- `assets/site.css` design-system-v2 expansion (+427 lines; a *different* CSS evolution than FE-002).
- `craft.html`, `series.html` pages.
- Competitor-analysis pipeline: `scripts/scrape_competitors.js`, `analyze_independent_groupings.py`,
  `build_competitor_catalog_taxonomy.py`, `build_independent_db.py`, plus `docs/research/*`,
  `docs/agent-source-material/*`, `docs/PDR-005..007` briefs.
- `docs/pdr/PDR-001-luxury-design-system-v2.md`.

**Neither line touches the intake "port" / configurator except fe-design** — `configurator.html` exists
*only* on fe-design. No double-application risk for the configurator/intake work.

---

## 6. Stray Uncommitted `index.html` — Verdict: DISCARD (regression)

`git -C "C:/Users/kas41/archived/HowieZZ" status` on `feat/pdr-010-ceo-roi-analysis`:
```
 M index.html
?? .artifacts/
?? docs/howie-ceo-package/PDR-010-DISPATCH.md
```

Diffs:
- vs pdr-010 HEAD: `index.html | 85 +-` (**17 insertions, 68 deletions**) — a large rollback.
- vs `feat/howiezz-fe-design`: `index.html | 9 ---` (**0 insertions, 9 deletions**).

The 9-line delta vs fe-design shows the working copy is **missing** fe-design's mobile CTA media queries:
```
-  @media(max-width:560px){
-    .hero{padding:74px 20px 54px}
-    .hero .cta{flex-direction:column;align-items:stretch;gap:11px;margin-top:26px}
-    .hero .cta .btn{width:100%;text-align:center;padding:15px 22px}
-    .stats{gap:26px 34px;margin-top:30px}
-  }
…
-  @media(max-width:560px){.intent-card .btn{width:100%;text-align:center}}
```

**Verdict:** This is a *stale, less-complete* version of fe-design's FE-001 homepage — it does **not**
duplicate or advance fe-design's work; applying it would **delete the FE-008/FE-011 mobile responsiveness
fixes**. It is uncommitted scratch in the autopilot's working tree and should be **reverted/discarded**
(`git -C "…/HowieZZ" checkout -- index.html`). No content needs to be salvaged from it.

---

## 7. Recommended Merge Strategy

**Canonical line: `feat/howiezz-fe-design` (PR #34).** It supersedes the autopilot design work and already
contains everything `782b510` carries.

**Order of operations:**

1. **Discard the stray `index.html`** in `C:/Users/kas41/archived/HowieZZ` (regression, see §6).
   Also review the untracked `.artifacts/` and `docs/howie-ceo-package/PDR-010-DISPATCH.md` separately —
   they are unrelated to FE.

2. **Drop / delete the autopilot artifacts** — they contribute nothing:
   - `worktree-agent-a0915cc58b842d46e`, `…a1386fba…`, `…ae28a44…` (all at `782b510`, already merged everywhere).
   - The `…/Temp/howiezz-pr31-ci-check` detached worktree.
   Use `git worktree remove` for each after confirming clean.

3. **Land PR #34 (`feat/howiezz-fe-design`) first** as the frontend source of truth.

4. **Reconcile PR #31 (pdr-010) into the picture as a near-no-op.** Its only unique content (`ae042a0`,
   `d093c5f`) is the regenerated `v2 HTML/*` bundle + a community-data ref fix — **non-design chores** that
   merge cleanly with fe-design (zero conflicts). Either:
   - cherry-pick `ae042a0` + `d093c5f` onto the post-#34 main, **or**
   - regenerate the `v2 HTML/` snapshot from the merged HTML (preferred — the bundle is a build artifact and
     will be stale once #34 lands). Do **not** re-apply pdr-010's HTML/design state — it is older than #34.

5. **Treat PR #27 (pdr-001) as the only true merge decision.** It is genuinely divergent (base `1853cf8`)
   and conflicts in 6 pages + `scripts/scrape_competitors.js` (§4). Recommended split:
   - **Design (`assets/site.css`, all 6 HTML pages, `craft.html`, `series.html`): DROP in favor of #34.**
     fe-design's FE-001..009 + FE-002 CSS is the intended redesign; do not hand-merge the conflicting pages.
   - **Cherry-pick only the NON-overlapping, non-design value from #27:** the competitor-analysis pipeline
     and research artifacts that fe-design lacks — `scripts/analyze_independent_groupings.py`,
     `build_competitor_catalog_taxonomy.py`, `build_independent_db.py`, `inspect_scrape.py`,
     `print_report.py`, `docs/research/*`, `docs/agent-source-material/*`, `docs/PDR-005..007*`,
     `docs/pdr/PDR-001-luxury-design-system-v2.md`.
     For `scripts/scrape_competitors.js` (conflicting), take **pdr-001's version** (fe-design only inherited it).
   - This avoids double-applying the design system: #34's CSS wins; #27 contributes only data/analysis.

6. After #34 + the #27 data cherry-picks land, **close PRs #27 and #31** (their design content is now obsolete
   or absorbed), and regenerate `v2 HTML/` + `sitemap.xml` from the final merged tree.

**Net:** #34 is canonical. pdr-010 = trivial trailing chores (regenerate, don't merge). pdr-001 = drop its
design, salvage only its competitor-analysis data layer. The three `782b510` worktrees and the stray
`index.html` are dead weight — discard.
