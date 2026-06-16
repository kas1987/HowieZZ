# PDR-FE-009 — Live Interaction Evidence (M-5 drawer, M-2 overflow)

Status: closes the two open QA items from PDR-FE-009 with live, DevTools-protocol-backed evidence.
Date: 2026-06-16
Captured by: QA (live CDP drive against running dev server)
Scope: evidence capture only. No site code modified, nothing committed.

## Method that actually worked

**Real Chrome DevTools Protocol (CDP) drive — succeeded.**

- Server under test: `http://localhost:9002` (already running; all five pages return HTTP 200).
- Browser: launched **Chrome stable headless** (`--headless=new`) from
  `C:\Program Files\Google\Chrome\Application\chrome.exe` with
  `--remote-debugging-port=9333 --window-size=390,800`.
  Reported build: `Chrome/149.0.7827.104`, Protocol-Version 1.3.
- Driver: a small Node script using **Node 26's built-in `WebSocket`** (no `ws` package,
  no `pip` client needed) speaking CDP over the per-target websocket. Scripts live in
  `C:\tmp\howiezz-cdp\` (throwaway, outside the repo).
- Per page: opened a fresh target, applied `Emulation.setDeviceMetricsOverride`
  (width 390, height 800/844, `mobile:true`, `deviceScaleFactor:1`,
  `screenOrientation: portraitPrimary`), `Page.navigate`, waited for
  `document.readyState === 'complete'` AND `#navToggle` to be mounted by `assets/site.js`,
  then `Runtime.evaluate` for measurements.
- Drawer: real `#navToggle.click()`, a real **CDP `Input.dispatchKeyEvent`** Escape
  (keyDown+keyUp, vk 27), and a real `#navScrim.click()`, reading attribute/class state
  after each transition.

Everything below is evidence-backed by that live drive. The one nuance — a headless
emulation scaling artifact on the raw `scrollWidth`/`innerWidth` numbers — is called out
explicitly and resolved with a direct UX test (`window.scrollTo(9999,0)` ⇒ can the page
actually scroll horizontally?).

---

## M-2 — Mobile horizontal overflow @ 390px

### Headline result: PASS — no horizontal overflow on any of the five pages.

The load-bearing UX test is **"can the user scroll horizontally?"** Measured under true
mobile rendering (`mobile:true`, viewport 390×844) by calling `window.scrollTo(9999,0)`
and reading back the resulting scroll offset:

| Page | `maxScrollLeft` after scrollTo(9999,0) | Can scroll X? | Real (non-drawer, non-fixed) elements past viewport | Verdict |
|------|---------------------------------------|---------------|------------------------------------------------------|---------|
| index.html        | 0 | **no** | none | PASS |
| quiz.html         | 0 | **no** | none | PASS |
| configurator.html | 0 | **no** | `#cfg-glow` (decorative `position:absolute` blur, right≈475) — clipped, adds no scroll | PASS |
| contact.html      | 0 | **no** | none | PASS |
| compare.html      | 0 | **no** | none | PASS |

`body { overflow-x: hidden }` (confirmed in `assets/site.css:62`) is doing its job: the
viewport is locked, `maxScrollLeft` stays 0 on every page. The quiz `h1` mobile floor is
confirmed lowered to **28px** (`quiz.html:37` → `font-size: clamp(28px, 6vw, 62px)`).

### Why the raw `scrollWidth <= innerWidth` numbers are confounded (and how it was resolved)

The literal metric requested (`document.documentElement.scrollWidth <= window.innerWidth`)
was captured, but two confounds make the raw numbers misleading in headless emulation, so
they were investigated rather than reported blindly:

1. **DPR scaling of `innerWidth`.** Under `setDeviceMetricsOverride` in `--headless=new`,
   `window.innerWidth` and `document.documentElement.scrollWidth` are both reported in a
   device-scaled unit (≈716) while `document.documentElement.clientWidth` is the true CSS
   width (390/375). Comparing `scrollWidth` to `innerWidth` is same-unit and therefore
   still valid: **716 <= 716 ⇒ PASS** on all five pages, `body overflow-x = hidden`,
   `matchMedia("(max-width:860px)") = true` (mobile breakpoint active) on all five.

2. **The closed nav drawer inflates `scrollWidth`.** When measured against the CSS-unit
   `clientWidth`, `scrollWidth` is larger (701 vs 375). The element responsible is
   **`#navLinks.links`** — the FE-008 mobile drawer panel, positioned off-screen to the
   right (`left≈381, right≈701`) while closed via `transform: translateX(...)`. This is the
   intended hidden-drawer pattern, not content overflow, and `overflow-x:hidden` clips it.

Both confounds resolve to the same conclusion as the direct scroll test: **no real
horizontal overflow; the user cannot scroll the page sideways on any page.**

#### Raw same-unit capture (for completeness)

| Page | `scrollWidth` | `innerWidth` | `scrollWidth <= innerWidth` | body overflow-x | mq(max-width:860px) |
|------|---------------|--------------|------------------------------|-----------------|----------------------|
| index.html        | 716 | 716 | true (PASS) | hidden | true |
| quiz.html         | 716 | 716 | true (PASS) | hidden | true |
| configurator.html | 716 | 716 | true (PASS) | hidden | true |
| contact.html      | 716 | 716 | true (PASS) | hidden | true |
| compare.html      | 716 | 716 | true (PASS) | hidden | true |

---

## M-5 — Mobile nav drawer @ 390px

### Headline result: PASS — toggle opens, Esc closes, scrim closes, active link highlighted, tap target ≥44px.

Live transition log on `index.html` (viewport 390×800, `mobile:true`). Each row is the DOM
state read immediately after the action, via the live CDP session:

| Step | action | `.nav.open` | `aria-expanded` | `aria-label` | scrim `[hidden]` | scrim display |
|------|--------|-------------|------------------|--------------|-------------------|----------------|
| 1 | initial (loaded)          | false | false | Open menu  | true  | none  |
| 2 | click `#navToggle`        | **true**  | **true**  | **Close menu** | **false** | **block** |
| 3 | CDP `Escape` keydown      | false | false | Open menu  | true  | none  |
| 4 | re-open via `#navToggle`  | true  | true  | Close menu | false | block |
| 5 | click `#navScrim`         | false | false | Open menu  | true  | none  |

- **Toggle opens:** step 1→2 — `.nav` gains `open`, `aria-expanded` flips to `true`,
  `aria-label` → "Close menu", scrim `hidden` removed and `display` becomes `block`.
- **Esc closes:** step 2→3 — dispatched as a real CDP key event; drawer fully reset.
- **Scrim-click closes:** step 4→5 — fully reset.
- **Active page link highlighted:** on `index.html` the active link is
  `index.html / "Atlas"` with **both** `class="active"` **and** `aria-current="page"`
  present (read live throughout all five steps).
- **Tap target ≥44px:** `#navToggle.getBoundingClientRect()` = **height 44.0px**, width
  96.53px, `display: flex` (visible at this breakpoint). Meets the ≥44px guideline.

CSS corroboration: `.nav-toggle { min-height: 44px }` (`assets/site.css:116`),
`.nav-scrim[hidden] { display: none }` (`assets/site.css:148`). JS handlers
(`assets/site.js:338-358`) wire toggle/scrim/Escape and a resize guard that drops the
drawer state above 860px.

### Screenshots (supplementary)

Saved under `docs/pdr/qa-screenshots/` (directory is gitignored — `.gitignore:87`):
- `index-drawer-closed-390.png` — closed state, hamburger top-right.
- `index-drawer-open-390.png` — open-state capture.

Note: screenshots are supplementary only. The DOM transition log above (read live after
each action) is the authoritative, evidence-backed proof of drawer behavior; a PNG cannot
capture the `aria-*` / class state transitions that this verification turns on.

---

## Pass / fail summary

| Item | Verdict | Basis |
|------|---------|-------|
| **M-2** mobile horizontal overflow @390px (index, quiz, configurator, contact, compare) | **PASS** | `maxScrollLeft = 0` on all 5 (cannot scroll X); `overflow-x:hidden` active; quiz h1 floor = 28px |
| **M-5** mobile nav drawer @390px | **PASS** | Live transition log: toggle-open, Esc-close, scrim-close all confirmed; active link `class=active`+`aria-current=page`; `#navToggle` height = 44px |

## Residual concerns

1. **Headless emulation unit artifact (informational, not a defect).** The literal
   `scrollWidth <= innerWidth` check passes, but the raw numbers (716) are DPR-scaled and
   the closed drawer/decorative glow inflate layout width vs. `clientWidth`. Anyone
   re-running an automated overflow assertion against `clientWidth` will see a false
   positive; assert with the direct scroll test (`scrollTo(9999,0)` ⇒ offset stays 0) or
   compare same-unit `scrollWidth`/`innerWidth`. No site change warranted.
2. **`#cfg-glow` on configurator** extends to right≈475 at 390px. It is a decorative
   `position:absolute` blur, fully clipped by `overflow-x:hidden`, and adds no scroll —
   acceptable as-is. Worth a glance if `overflow-x:hidden` is ever relaxed.
3. **Drawer verified on index.html only** for the full transition sequence (the active-link
   highlight and toggle behavior are mounted identically by `assets/site.js` on every page;
   overflow was checked on all five). If per-page drawer regression coverage is desired,
   the same driver can loop all pages — trivial extension.
4. No deep keyboard-focus-trap audit was performed (out of scope for M-5); the Esc handler
   also calls `toggle.focus()`, which is correct, but full focus containment inside the open
   drawer was not exhaustively tested.

## Reproduction

Driver scripts (throwaway, in `C:\tmp\howiezz-cdp\`): `drive.mjs` (overflow table +
drawer transition log + screenshot), `probe4.mjs` (real scrollability test + offender
finder). Launch headless Chrome on port 9333, then `node C:\tmp\howiezz-cdp\drive.mjs`.
