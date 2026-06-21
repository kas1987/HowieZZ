# Contributing

This is a private, proprietary project. Access is limited to the brand team.

## Branch & PR workflow

`main` is protected. **Do not commit directly to `main`.**

1. Branch off `main`: `git checkout -b feat/<short-topic>` (or `fix/…`, `chore/…`).
2. Make your change. Keep it scoped.
3. Push the branch and open a Pull Request.
4. CI (`.github/workflows/ci.yml`) must pass before merge.

## Branch naming

```text
feature/<short-description>
bugfix/<short-description>
hotfix/<short-description>
docs/<short-description>
chore/<short-description>
```

## Commit style

```text
type(scope): short description
```

Examples:

```text
feat(browse): add body-family filter rail
fix(character): handle missing hero image gracefully
docs(readme): update local setup instructions
chore(ci): bump actions/checkout to v4
```

## What belongs in this repo

- **Yes:** HTML pages, `assets/site.css` + `assets/site.js`, Python build scripts, `db/*.json` catalog data, `docs/`.
- **No:** images, video, the Shopify theme, build zips/PDFs, confidential business documents, local tooling state. These are excluded by `.gitignore` — do not force-add them.

If you need to add a genuinely new tracked file type, update `.gitignore` in the same PR and explain why.

## Component Storybook

A living, accessible component library is available at **[docs/component-storybook.html](docs/component-storybook.html)**. It documents all UI patterns used across the site:

- **Buttons** — default, solid, ghost, concierge styles
- **Status Chips** — live, verified, pending, estimated, concept
- **Family Tags** — all six body-family classifications
- **Cards** — character and body-architecture layouts
- **Panels** — content containers and accents
- **Form Elements** — inputs, textareas, selects, validation
- **Filters** — toggleable pills and choice groups
- **Grids** — responsive column systems
- **Modals** — dialogs and confirmations
- **Accessibility Features** — focus indicators, WCAG AA compliance, keyboard navigation, screen reader support

Use this as a reference when creating new components. All components meet WCAG AA accessibility standards.

## Phase 1: Foundation & Runbooks

Phase 1 (Weeks 1-6, 2026) establishes core infrastructure: design tokens, CDN, build pipeline, and analytics. Every developer must be familiar with these runbooks:

| Runbook | Purpose | Read First If You're |
|---------|---------|-----|
| [`docs/design-tokens-runbook.md`](docs/design-tokens-runbook.md) | How to add/modify CSS tokens (colors, spacing, type, shadows) | Editing styles |
| [`docs/cdn-runbook.md`](docs/cdn-runbook.md) | How to upload images to CDN, manage manifest, troubleshoot delivery | Adding images |
| [`docs/pipeline-runbook.md`](docs/pipeline-runbook.md) | How to run build orchestrator, resume after failure, parallelize stages | Running builds |
| [`docs/analytics-runbook.md`](docs/analytics-runbook.md) | How to wire GA4 events, test with GTM Preview, debug data quality | Working with analytics |
| [`docs/phase1-faq.md`](docs/phase1-faq.md) | Answers to 30+ common Phase 1 questions | Stuck on something |
| [`docs/PHASE1-KICKOFF.md`](docs/PHASE1-KICKOFF.md) | Training summary & team responsibilities | New to this project |

**Key Phase 1 Rules:**
1. **Design Tokens:** Never use hardcoded colors, spacing, or font sizes. Always use `var(--token-name)`.
2. **Images:** All images hosted on CDN. Run pipeline to auto-upload. Pre-push hook validates manifest freshness.
3. **Build Pipeline:** Use `build_orchestrator.py` (not individual scripts). It parallelizes, caches, and handles retries.
4. **Analytics:** Events fire via `ZX.analytics()` to dataLayer → GTM → GA4. Test with debug mode before merging.

## Building the catalog

Run the **Build Orchestrator** to generate all catalog data:

```bash
# Full pipeline with intelligent caching and parallel execution
python scripts/build_orchestrator.py --full

# Or use convenience wrappers
./scripts/build.sh              # macOS/Linux
scripts\build.bat               # Windows

# Resume from last failure (safer than full rebuild)
python scripts/build_orchestrator.py --resume

# Full rebuild (reset database)
python scripts/build_orchestrator.py --reset
```

See [`docs/pipeline-runbook.md`](docs/pipeline-runbook.md) for detailed pipeline docs, including troubleshooting and performance tuning.

## Conventions

- **Design Tokens (Phase 1):** All colors, spacing, type sizes, and shadows use CSS variables defined in `assets/site.css` `:root`. Never hardcode hex codes or pixel values in CSS. See [`docs/design-tokens-runbook.md`](docs/design-tokens-runbook.md).
  - ✓ `color: var(--color-primary);`
  - ✓ `padding: var(--sp4);`
  - ✗ `color: #d4a574;`
  - ✗ `padding: 16px;`
- Every page uses the shared kit (`ZX` global from `assets/site.js`). Prefer extending the kit over per-page one-offs so all pages stay consistent.
- Regenerate data with the orchestrator (see above); don't hand-edit generated `db/*.json` except the curated inputs (`character_overlay.json`, `body_measurements.json`).
- Match the surrounding code's style, naming, and comment density.
- All images must be uploaded via pipeline; see [`docs/cdn-runbook.md`](docs/cdn-runbook.md) for workflow.

## Tests

The project has two test suites that CI runs on every PR.

| Suite | Runner | What's covered |
|---|---|---|
| `tests/test_build_profiles.py` | pytest | `classify()`, `center()`, `in_range()` — the family classification engine |
| `tests/test_build_db.py` | pytest | All four folder-name parsers, `decode_body`, `parse_head_filename`, `parse_body_spec`, `canon_body`, and other helpers |
| `tests/test_build_characters.py` | pytest | `is_torso()`, `is_factory()`, `tagline()` |
| `tests/site.test.js` | vitest | `assets/site.js` runtime — `esc`, `famColor`, `charCard`, `bodyCard`, `load()`, and other `ZX` helpers |

Run the full suite locally:

```bash
python -m pytest --tb=short -q   # Python — ~0.2 s
npm test                          # JavaScript — ~1 s
```

Run just one file during development:

```bash
python -m pytest tests/test_build_profiles.py -v
npx vitest run tests/site.test.js
```

### Pre-push hook

The `hooks/pre-push` script runs both suites automatically before every push.
Install it once after cloning:

```bash
npm install          # installs vitest (needed for JS tests)
npm run install-hooks
```

That runs `git config core.hooksPath hooks`, which tells Git to look for hooks
in the committed `hooks/` directory rather than `.git/hooks/`. No extra tools
required. To bypass in an emergency: `git push --no-verify` (avoid unless you
understand why tests are failing).

## Local checks before pushing

With the hook installed, tests run automatically. You can also run the full
validation suite manually:

```bash
python -m py_compile scripts/*.py
python -m pytest --tb=short -q
npm test
node .github/scripts/validate-site.mjs      # validates inline JS + db JSON
```

## Security

Do not commit secrets. If you accidentally commit a secret, stop immediately — revoke it and report it so it can be purged from history.
