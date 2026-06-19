# Changelog

All notable changes to the ZELEX Character Atlas are documented here.

Format: [Semantic Versioning](https://semver.org/) — `vMAJOR.MINOR.PATCH`

---

## [Unreleased]

### Added
- `docs/repo_operating_model.md` — branching, CI, release, and agent rules
- `CHANGELOG.md` — this file
- Caddy local dev server (`Caddyfile`, `start-caddy.bat`) serving `https://howiez.local`

### Changed
- `CLAUDE.md` — rewritten to reflect actual project stack; removed PDR-first gate
- `CONTRIBUTING.md` — removed PDR authority section; added conventional commit style guide
- `.github/workflows/ci.yml` — fixed action versions (`checkout@v4`, `setup-python@v5`); scoped `pages: write` / `id-token: write` to deploy job only; removed PDR_PATH guard step

### Fixed
- CI would have failed on every run due to non-existent `actions/checkout@v6` and `actions/setup-python@v6`

---

## [v1.0.0] — Initial Atlas Release

- Four series catalog: Inspiration · K-Series · SLE · Fusion
- Six Body Families: The Classic · The Icon · The Muse · The Siren · The Empress · The Sculpt
- Character detail, browse, quiz, compare, series, family, craft, and contact pages
- Python data pipeline: `build_db` → `build_profiles` → `build_characters` → `merge_stories` → `make_thumbs` → `build_package`
- GitHub Pages deployment via CI
