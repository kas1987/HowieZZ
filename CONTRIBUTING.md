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

## Building the catalog

Run the **Build Orchestrator** to generate all catalog data:

```bash
# Full pipeline with intelligent caching and parallel execution
python scripts/build_orchestrator.py

# Or use convenience wrappers
./scripts/build.sh              # macOS/Linux
scripts\build.bat               # Windows

# Resume from last failure
python scripts/build_orchestrator.py --resume

# Full rebuild (reset database)
python scripts/build_orchestrator.py --reset
```

See [`docs/BUILD-ORCHESTRATOR.md`](docs/BUILD-ORCHESTRATOR.md) for full docs.

## Conventions

- Every page uses the shared kit (`ZX` global from `assets/site.js`). Prefer extending the kit over per-page one-offs so all pages stay consistent.
- Regenerate data with the orchestrator (see above); don't hand-edit generated `db/*.json` except the curated inputs (`character_overlay.json`, `body_measurements.json`).
- Match the surrounding code's style, naming, and comment density.

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
