# Common Development Tasks

Quick recipes for everyday work on ZELEX.

---

## Running Servers

### Python dev server (default, fast)
```bash
./start-dev              # Starts on http://localhost:9000
```

### Caddy server (with caching headers)
```bash
./start-dev caddy        # Starts on http://localhost:2015
```

To access via `howiez.local`, add to your hosts file:
- **Windows:** `C:\Windows\System32\drivers\etc\hosts`
- **macOS/Linux:** `/etc/hosts`

```
127.0.0.1  howiez.local
```

---

## Running Tests

### All tests (Python + JavaScript)
```bash
./start-dev test
```

### Python tests only
```bash
./start-dev shell
python -m pytest --tb=short -q          # All tests, short output
python -m pytest tests/test_build_profiles.py -v  # Specific file, verbose
python -m pytest -k "classify" -v       # Tests matching keyword
```

### JavaScript tests only
```bash
./start-dev shell
npm test                                 # Run vitest
npx vitest run tests/site.test.js       # Specific file
```

### Tests run automatically before push

The pre-push hook (`hooks/pre-push`) runs all tests. To install the hook:
```bash
./start-dev shell
npm run install-hooks
```

Then every `git push` will run tests first. To bypass (not recommended):
```bash
git push --no-verify
```

---

## Building Data

### Full pipeline rebuild
```bash
./start-dev build
```

This runs (in order):
1. `build_db.py` — scan assets, populate database
2. `build_profiles.py` — classify bodies into 6 families
3. `build_characters.py` — generate character records
4. `merge_stories.py` — fold in story/profile data
5. `make_thumbs.py` — generate image thumbnails

### Resume from last failure
```bash
./start-dev shell
python scripts/build_orchestrator.py --resume
```

### Full rebuild (reset database)
```bash
./start-dev shell
python scripts/build_orchestrator.py --reset
```

### Run individual scripts
```bash
./start-dev shell
python scripts/build_db.py
python scripts/build_profiles.py
python scripts/build_characters.py
```

---

## Editing Code

### Frontend (HTML/CSS/JS)

1. Edit a file (e.g., `index.html`, `assets/site.css`)
2. Refresh browser
3. Changes are live

No rebuild needed. Design tokens and shared components use the global `ZX` object from `assets/site.js`.

**Important:** Never hardcode colors, spacing, or sizes. Use CSS tokens:
```css
/* Good */
color: var(--color-primary-gold);
padding: var(--spacing-4);

/* Bad */
color: #d4a574;
padding: 16px;
```

See `docs/design-tokens-runbook.md` for all available tokens.

### Backend (Python scripts)

1. Edit a script (e.g., `scripts/build_characters.py`)
2. Test locally (see "Running Tests" above)
3. Run pipeline to regenerate data:
   ```bash
   ./start-dev build
   ```
4. Refresh browser to see changes

---

## Adding Images

### Upload to CDN

All images must be on the CDN, not in git.

```bash
./start-dev shell
python scripts/download_assets.py       # Sync existing images
python scripts/extract_assets.py        # Extract from other sources
```

Then update the image manifest and commit:
```bash
git add db/cdn_manifest.json
git commit -m "chore(cdn): add new character photos"
```

See `docs/cdn-runbook.md` for detailed workflows.

### Reference images in HTML

```html
<img src="/assets/thumbs/character-GE52_1.webp" alt="Character">
```

The CDN manifest is auto-validated before push.

---

## Git Workflow

### Create a feature branch
```bash
git checkout -b feat/my-feature
```

Branch naming:
- `feat/…` — new feature
- `fix/…` — bug fix
- `docs/…` — documentation
- `chore/…` — maintenance

### Commit (follow style guide)
```bash
git commit -m "feat(browse): add body-family filter"
git commit -m "fix(character): handle missing images"
git commit -m "docs(readme): clarify setup steps"
```

Format: `type(scope): description`

### Push and open PR
```bash
git push origin feat/my-feature
```

Then open a PR on GitHub. CI will run automatically. All tests must pass before merge.

### Merge to main
Once PR is approved and CI passes, use GitHub's merge button (don't merge locally).

---

## Debugging

### Check what data exists

```bash
./start-dev shell
python scripts/check_db.py          # List catalog.db contents
cat db/catalog.json                 # View all catalog data
cat db/characters.json              # View all characters
```

### Debug a single character

```bash
./start-dev shell
python -c "
import json
chars = json.load(open('db/characters.json'))
print(json.dumps(chars['GE52_1'], indent=2))  # Replace with char ID
"
```

### View build logs

```bash
./start-dev shell
python scripts/build_orchestrator.py --full 2>&1 | tee build.log
```

### Inspect compiled HTML

Open DevTools in your browser (`F12`):
- **Elements tab** — inspect DOM
- **Console tab** — see JS errors
- **Network tab** — check asset loading
- **Application tab** → Cookies/Storage — view analytics data

---

## Performance & Profiling

### Lighthouse audit

```bash
./start-dev shell
npm run lighthouse              # Generates report
```

### Profile the build pipeline

```bash
./start-dev shell
python scripts/build_orchestrator.py --full --profile  # Shows timing per stage
```

### Check code quality

```bash
./start-dev shell
python -m py_compile scripts/*.py      # Syntax check all Python
node .github/scripts/validate-site.mjs  # Validate JS + JSON
```

---

## Project Structure Reference

```
├── index.html                  # Homepage
├── browse.html                 # Character grid
├── character.html              # Character detail (parameterized)
├── assets/
│   ├── site.css               # Global styles (design tokens)
│   ├── site.js                # Global JS (ZX object)
│   ├── thumbs/                # Character thumbnails (git-ignored)
│   └── data/                  # Source overrides
├── db/
│   ├── catalog.json           # All products/bodies (generated)
│   ├── characters.json        # All characters (generated)
│   ├── character_overlay.json # Hand-curated overrides
│   ├── body_measurements.json # Body dimensions (source of truth)
│   └── catalog.db             # SQLite database (generated)
├── scripts/
│   ├── build_orchestrator.py  # Master build script
│   ├── build_db.py
│   ├── build_profiles.py
│   ├── build_characters.py
│   └── *.py                   # Other utilities
├── tests/
│   ├── test_build_profiles.py # Python tests
│   ├── site.test.js           # JavaScript tests
│   └── conftest.py
├── docs/
│   ├── design-tokens-runbook.md
│   ├── pipeline-runbook.md
│   ├── analytics-runbook.md
│   └── component-storybook.html
└── hooks/
    └── pre-push               # Runs tests before git push
```

---

## Troubleshooting Common Issues

### Site won't load at localhost:9000

1. Check if container is running: `docker ps`
2. Check logs: `docker-compose logs zelex`
3. Try a different port: `./start-dev rebuild` then `docker-compose run -p 9001:9000 zelex python serve.py 9000`

### Tests fail with "module not found"

```bash
./start-dev shell
pip install -r requirements.txt  # Reinstall dependencies
npm install                      # Reinstall Node packages
```

### Character images not loading

```bash
./start-dev shell
python scripts/build_orchestrator.py --resume  # Regenerate thumbnails
```

### Build takes too long

The pipeline caches results. To skip cache:
```bash
./start-dev shell
python scripts/build_orchestrator.py --reset   # Full rebuild
```

### Git pre-push hook won't run

```bash
./start-dev shell
git config core.hooksPath hooks
chmod +x hooks/pre-push
```

---

## Useful Resources

- **[QUICKSTART.md](QUICKSTART.md)** — Get running in 5 minutes
- **[CONTRIBUTING.md](CONTRIBUTING.md)** — Branch/commit style, component library
- **[docs/pipeline-runbook.md](docs/pipeline-runbook.md)** — Detailed build pipeline
- **[docs/design-tokens-runbook.md](docs/design-tokens-runbook.md)** — CSS token system
- **[docs/analytics-runbook.md](docs/analytics-runbook.md)** — GA4 events & GTM
- **[docs/cdn-runbook.md](docs/cdn-runbook.md)** — CDN workflow
- **[docs/component-storybook.html](docs/component-storybook.html)** — UI component gallery

