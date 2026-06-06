# Contributing

This is a private, proprietary project. Access is limited to the brand team.

## Branch & PR workflow

`main` is protected. **Do not commit directly to `main`.**

1. Branch off `main`: `git checkout -b feat/<short-topic>` (or `fix/…`, `chore/…`).
2. Make your change. Keep it scoped.
3. Push the branch and open a Pull Request.
4. CI (`.github/workflows/ci.yml`) must pass before merge.

## What belongs in this repo

- **Yes:** HTML pages, `assets/site.css` + `assets/site.js`, Python build
  scripts, `db/*.json` catalog data, `docs/`.
- **No:** images, video, the Shopify theme, build zips/PDFs, confidential
  business documents, local tooling state. These are excluded by
  [`.gitignore`](.gitignore) — do not force-add them.

If you need to add a genuinely new tracked file type, update `.gitignore` in the
same PR and explain why.

## Conventions

- Every page uses the shared kit (`ZX` global from `assets/site.js`). Prefer
  extending the kit over per-page one-offs so all pages stay consistent.
- Regenerate data with the pipeline (see [README](README.md)); don't hand-edit
  generated `db/*.json` except the curated inputs (`character_overlay.json`,
  `body_measurements.json`).
- Match the surrounding code's style, naming, and comment density.

## Local checks before pushing

```bash
python -m py_compile scripts/*.py
node .github/scripts/validate-site.mjs      # validates inline JS + db JSON
```
