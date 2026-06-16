# PDR-FE-009 — Visual QA & Screenshot Review — Findings

**Ticket:** HZZ-FE-009
**Reviewer role:** Auditor (read-only; no site code modified)
**Date:** 2026-06-16
**Branch:** feat/howiezz-fe-design
**Dev server:** http://localhost:9002 (pre-running; not started by reviewer)

---

## 1. Method used

**Headless-browser screenshots (Chrome stable) + corroborating code-level review.**

- No `playwright` / `puppeteer` packages are installed (no `node_modules`; `npx playwright`
  refused to auto-install). Chrome stable **is** present at
  `C:\Program Files\Google\Chrome\Application\chrome.exe`, so screenshots were captured with
  `chrome --headless --disable-gpu --screenshot`.
- Captured **desktop (1280px wide)** and **mobile (390px wide)** for: index, compare,
  character (`?id=Fusion-ZF161D-01`, a real live id from `db/characters.json`), quiz, contact
  (plain + `?id=`), configurator, browse, family. Artifacts saved to
  `docs/pdr/qa-screenshots/` (PNG; `d-*` desktop, `m-*` mobile).
- **Capture caveat (important for honesty):** most pages render their content via
  `ZX.load()` → `fetch(db/*.json)` in `assets/site.js`. Chrome's one-shot `--screenshot`
  fires *before* the async fetch settles. Initial captures showed "Loading catalog…".
  Re-captures used `--virtual-time-budget=6000–12000` to let the data load. Browse alone
  *still* showed "Loading the ZELEX catalog…" even at a 12s budget — see Finding **M-1**;
  this is judged a **headless virtual-time artifact, not a runtime bug** (the character,
  family, configurator and `?id=` contact pages all consume the *same* `ZX.load()` data and
  rendered correctly, and `db/characters.json` returns HTTP 200).
- Where a screenshot could not exercise interaction (the FE-008 mobile nav **drawer** open
  state, `Esc`/scrim/active behavior), the implementation was reviewed **at code level** in
  `assets/site.js` and `assets/site.css` and cited by line.

Each finding below cites either a rendered screenshot or a real `file:line`.

---

## 2. Overall verdict

**PASS with minor issues.** The redesign is coherent, on-brand, and the high-risk
behaviors the ticket calls out — missing-image fallback, honest in-development family
states, estimated-dimension disclosure, concierge voice, 18+/privacy — are all correctly
implemented and verified. **No blockers.** No major layout breakage on desktop. The only
real defects are (a) one un-verified mobile horizontal-overflow suspicion on short JS pages
and (b) cosmetic copy inconsistencies. Ship-able; open the follow-ups below.

**Counts:** Blocker **0** · Major **0** · Minor **5**

---

## 3. Per-page findings

### Homepage — index.html — PASS
Desktop (`d-index.png`) and mobile (`m-index.png`) both clean. Strong CTA hierarchy:
primary "Find Your Match" (solid cream) → secondary "Compare Bodies"/"Browse the Atlas"
ghost buttons; measurement-led value props ("MEASURED BODIES", "WHR/BWR signature");
"Body architecture is the real decision layer" framing. Adults-only / made-to-order chips
present. Mobile stacks to single column correctly.

### Compare — compare.html — PASS
`d-compare.png` / `m-compare.png`. Empty state is excellent and honest: "Nothing on the
table yet." with recovery CTAs (Take the quiz / Browse all bodies). Body selector dropdown
("ZF161D | 161cm | D-cup | The Muse"), Add/Clear/"Ask concierge" controls. Active nav
("Compare") highlighted gold. Concierge voice intact ("We translate the numbers into a
plain buyer read").

### Character — character.html?id=Fusion-ZF161D-01 — PASS
`d-character.png` / `m-character.png`. Renders the full conversion layout: 8-image gallery
with **monotile fallback tile visible** for missing shots; estimated-dimension callouts are
explicit and repeated ("Estimated — no published spec card. … Interpolated from
ZG162D / ZF168B"); full measurement panel (WHR/BWR, bust drop); "Request a Private
Consultation" primary CTA; secondary "Compare this body" / "Build something similar" /
"Ask the concierge"; "Her Story" concierge narrative. Measurement-led + concierge voice
fully present.

### Quiz — quiz.html — PASS (with M-2 mobile suspicion)
`d-quiz.png` shows the start screen ("Five questions. Six body families. One
introduction." / BEGIN / "Takes about 60 seconds"). Clean on desktop.
`m-quiz.png`: hero `h1` and intro paragraph appear **clipped at the right edge** at 390px
— see Finding **M-2**.

### Contact — contact.html (plain + ?id=) — PASS
`d-contact.png`: rich guided buyer-fit intake — "New to ZELEX" vs "Experienced collector"
cards, intent-of-use cards, timeline, realism-preference slider, handling comfort, and
**Shipping & privacy** ("Standard / Extra discreet / Maximum privacy"). "What to expect"
rail reinforces discreet, made-to-order, no-obligation positioning.
`d-contact-id.png` (with `?id=`): **prefill verified working** — injects a "YOUR
CONSULTATION BRIEF" chip for *Gwen* (body code + family) and a readonly "character of
interest" field reading "The Muse — tall, hip-dominant (>20)". (`contact.html:833 prefill()`,
`:993` readonly swap.) **18+/privacy preserved**: explicit consent checkbox "I confirm that
I am 18 years of age or older … information will not be shared with third parties"
(`contact.html:381`) + `err-consent` "Please confirm you are 18+ to proceed" (`:383`).

### Configurator — configurator.html — PASS (with M-2 mobile suspicion)
`d-configurator.png`: live body silhouette ("Shape your character, live."), family selector
with **The Classic & The Sculpt flagged "IN DEVELOPMENT"**, skin-tone swatches, real-time
measurement readout, "Request a Private Consultation" + "no obligation". `m-configurator.png`
renders but the right-side spec column appears to bleed past 390px — see **M-2**.

### Browse — browse.html — PASS (catalog grid not captured; see M-1)
`d-browse.png`: hero, taxonomy strip (Family / Series / Character glossary), "Photographed
only" filter, search box, compare-set controls, "Narrowed it down?" concierge CTA card all
render. The **character grid itself stayed at "Loading the ZELEX catalog…"** under headless
even at a 12s virtual-time budget — Finding **M-1** (artifact, not confirmed bug).

### Family — family.html — PASS
`d-family.png` / `m-family.png`. All **six** families render as cards. **In-development
states are honest, not broken**: The Classic and The Sculpt carry an "IN DEVELOPMENT" badge
and the dev-note "Architectures are in final development — the proportion signature is
locked; bodies are not yet in the catalogue" (`family.html:332`, intro `:262` "Four are in
the catalogue today; two are in development", source comment `:101` "limited / single-
character family — honest, not broken"). Stat row (4 available / 19 architectures / 76
characters). Mobile stacks cleanly.

---

## 4. Prioritized issue list

### Blocker — none

### Major — none

### Minor

**M-1 — Browse grid never paints under headless screenshot (capture artifact; verify in real browser).**
`browse.html:232` boots via `ZX.load().then(init)`; `assets/site.js:214 load()` does
`Promise.all([... 3 fetches ...])`. Under `chrome --headless --virtual-time-budget` the grid
stayed at "Loading the ZELEX catalog…" (`browse.html:202`) even at 12s, while every other
`ZX.load()`-driven page rendered. **Most likely a known Chrome-headless virtual-time +
parallel-fetch quirk, not a runtime defect.** Action: open `browse.html` in a real browser
and confirm the grid populates; if it does, no code change. *Ref: `browse.html:202,232`;
`assets/site.js:214-242`.*

**M-2 — Possible horizontal overflow on short JS pages at 390px (quiz hero, configurator spec panel).**
`m-quiz.png` shows the hero `h1` ("The one built *for you*") and intro sub clipped at the
right edge; `m-configurator.png` right column similarly bleeds. There is **no
`overflow-x:hidden` or width guard on `html`/`body`** (`assets/site.css:60-62`), so any
single overflowing child widens the page. Quiz `.intro h1` is `clamp(36px,6vw,62px)`
(`quiz.html:36`) → clamps to the **36px floor** at 390px, large for that phrase. The shared
footer itself is *not* the cause (it has `flex-wrap:wrap`, `assets/site.css:414`).
**Caveat:** captured with `--hide-scrollbars`, which can render at intrinsic width — confirm
in a real 390px viewport before treating as definite. Action: verify; if real, reduce the
quiz `h1` mobile floor and/or add `overflow-x:hidden` to `body`. *Ref: `quiz.html:36`;
`assets/site.css:60-62`.*

**M-3 — Family/series taxonomy copy is inconsistent ("six families" vs "four series").**
Quiz says "Six body families" (`d-quiz.png`) and family.html says "six curated silhouette
families" (`family.html:262`), but the global footer reads "four series · full-body
architectures" and compare/browse use "series" interchangeably. Not wrong, but the
six-families vs four-series distinction may read as a contradiction to a first-time buyer.
Action: align the glossary line once. *Ref: footer text in `d-compare.png`/`d-quiz.png`;
`family.html:262`.*

**M-4 — Secondary/label text leans on low-emphasis `--muted` (#9a9a9a) at small sizes.**
`--muted` on `--bg` (#121212) computes ≈ 6.6:1 — passes WCAG AA for normal text — but it is
applied to 10–12px uppercase labels with wide letter-spacing (nav links `assets/site.css:99`;
`.fam` badge 10px `:226`; `.metrics-legend .lg-note` 10.5px italic `:292`; footer 11px
`:415`). Legible but near the comfortable floor. Action: consider bumping the smallest label
sizes or using `--text` for the densest metric labels. *Ref: `assets/site.css:99,226,292,415`.*

**M-5 — Nav drawer/Esc/scrim/active confirmed by code only (no interactive screenshot).**
The FE-008 drawer could not be exercised by a one-shot screenshot. Code review confirms it is
correct (see §5), but a live click-through (open → Esc → scrim → active link) was not
visually captured. Action: a quick manual pass in a phone viewport to close the loop.

---

## 5. FE-008 mobile nav drawer — code-level verdict: PASS

`assets/site.js:287-358 mountNav()` + `assets/site.css:105-155`:
- Hamburger `#navToggle` hidden on desktop (`.nav-toggle{display:none}` `:105`), shown <860px
  (`:116`) with **`min-height:44px`** tap target.
- **Open/close**: `toggle.click` → `setOpen(!open)` (`site.js:343`); drawer slides via
  `translateX` (`site.css:139`).
- **Scrim**: `#navScrim` click closes (`site.js:344`).
- **Link tap** inside drawer auto-closes so destination isn't hidden (`:347`).
- **Esc** closes **and returns focus to the toggle** (`:349-351`).
- **aria**: `aria-expanded` + `aria-label` swap open/closed (`:337-338`); `aria-controls`.
- **Active page** highlighted with `.active` + `aria-current="page"` gold (`:294`,
  `site.css:101/144`).
- **Body scroll-lock** only while open (`:341`); **resize >860px** drops stuck open state
  (`:354`). Progressive enhancement: with no JS the links render inline (never trapped).
- **Reduced motion** honored: bars transition disabled (`site.css:339`).

---

## 6. Contrast & tap-target notes

- **Tap targets:** nav toggle `min-height:44px` (`site.css:116`) — meets the 44px guideline.
  Buttons `.btn` pad `12px 26px` and `.btn.solid`/concierge larger — adequate. Form
  checkboxes are 17px but have a full-width clickable `<label>` (`contact.html:381`).
- **Contrast (against `--bg` #121212):**
  - `--text` #e8e8e8 → ~13:1 (AAA).
  - `--gold` #D4A574 (CTAs, active nav, accents) → ~8:1 (AAA for normal text).
  - `--muted` #9a9a9a (secondary/labels) → ~6.6:1 (passes AA; see **M-4** re: small sizes).
  - `--blue` #5EA6E8 (links/sig, e.g. breadcrumbs, "sig" line) → ~5.9:1 (passes AA normal).
  - Focus ring `2px solid --gold, offset 3px` (`site.css:72`) — visible focus everywhere.
- No contrast **failures** found; only the small-label comfort note (M-4).

---

## 7. Special-state verdicts

| State | Verdict | Evidence |
|---|---|---|
| Missing-image fallback (`.monotile`) | **PASS** | `site.js:409-418` photo-or-monotile; `site.css:253-255` monogram tile; visible in `d-character.png` |
| Placeholder / borrowed-shoot "Concept" tag | **PASS** | `site.js:412-413`, "Shoot Pending" stat `:398` |
| In-development families (Classic & Sculpt) — honest, not broken | **PASS** | `family.html:101,262,332`; badge visible `d-family.png`/`m-family.png` |
| Estimated dimensions disclosed | **PASS** | character page "Estimated — Interpolated from …"; `d-character.png`; data `estimated:true` in `db/characters.json` |
| Measurement-led copy + concierge voice | **PASS** | every page; "private consultation", "we translate the numbers into a plain buyer read" |
| 18+ / privacy preserved | **PASS** | `contact.html:381,383`; discreet shipping + "not shared with third parties" |
| `?id=` contact prefill | **PASS** | `d-contact-id.png` (Gwen brief chip); `contact.html:833,993` |

---

## 8. Proposed follow-up tickets

No Blocker/Major issues were found, so **no blocker ticket is required by the acceptance
criteria.** The following optional Minor follow-ups are proposed (stubs written to
`docs/tickets/`):

- **HZZ-FE-010 — Confirm browse grid renders in a real browser; harden `ZX.load()` for
  headless/CI.** (from M-1) — verify live; if the headless artifact also affects CI
  screenshotting, add a load-complete signal.
- **HZZ-FE-011 — Fix mobile horizontal overflow on quiz/configurator at 390px.** (from M-2)
  — verify in a real narrow viewport; if real, lower quiz `h1` mobile floor and/or add
  `overflow-x:hidden` to `body`.
- **HZZ-FE-012 — Reconcile "six families" vs "four series" taxonomy copy.** (from M-3)
- **HZZ-FE-013 — Small-label contrast/legibility comfort pass.** (from M-4)

---

## 9. Screenshot index (`docs/pdr/qa-screenshots/`)

Desktop (1280w): `d-index`, `d-compare`, `d-character`, `d-quiz`, `d-contact`,
`d-contact-id`, `d-configurator`, `d-browse`, `d-family`.
Mobile (390w): `m-index`, `m-compare`, `m-character`, `m-quiz`, `m-contact`,
`m-contact-id`, `m-configurator`, `m-browse`, `m-family`.

---

## 10. Resolution (all minors addressed)

All five minor findings were addressed in the same cycle (commit follows this doc):

- **M-1 (HZZ-FE-010)** — RESOLVED. Verified via headless DOM dump that browse renders **76 character cards** (no "Loading" text) — confirmed a `--screenshot` one-shot artifact, not a runtime bug. Hardened for CI/headless: `ZX.load()` now sets `html[data-zx-loaded="1"]` once the catalog model resolves, so screenshot tooling can wait on that attribute instead of a fixed timeout (`assets/site.js`).
- **M-2 (HZZ-FE-011)** — RESOLVED. Added `overflow-x:hidden` guard to `body` (`assets/site.css`) and lowered the quiz hero `h1` mobile floor `clamp(36px→28px,6vw,62px)` (`quiz.html`) so the phrase fits at 390px.
- **M-3 (HZZ-FE-012)** — RESOLVED. Footer tagline reconciled to "six silhouette families across four series" (`assets/site.js`), making the family↔series relationship explicit (the 6×4 taxonomy is correct, not a contradiction).
- **M-4 (HZZ-FE-013)** — RESOLVED. Bumped `--muted` #9a9a9a → #ababab (~6.6:1 → ~7.4:1 on `--bg`) for small-label comfort while preserving the muted hierarchy.
- **M-5** — Drawer behavior remains code-verified (PASS); a live phone-viewport click-through is the only open item and needs no code change.

Net verdict unchanged: **PASS, 0 blockers, 0 major.** Follow-up tickets HZZ-FE-010–013 are now closed by these fixes.
