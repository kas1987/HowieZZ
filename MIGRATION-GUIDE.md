# Migration & Upgrade Guide

Instructions for common operational tasks: adding bodies, updating characters, deploying changes, and migrating data.

> See also: [ARCHITECTURE.md](ARCHITECTURE.md), [DATA-SCHEMA.md](DATA-SCHEMA.md), [DECISIONS.md](DECISIONS.md)

---

## Table of Contents

1. [Adding a New Body](#adding-a-new-body)
2. [Adding a New Character](#adding-a-new-character)
3. [Editing Existing Characters](#editing-existing-characters)
4. [Updating Body Measurements](#updating-body-measurements)
5. [Adding a New Series](#adding-a-new-series)
6. [Deploying Changes](#deploying-changes)
7. [Rolling Back](#rolling-back)
8. [Data Recovery](#data-recovery)
9. [Performance Tuning](#performance-tuning)
10. [Troubleshooting](#troubleshooting)

---

## Adding a New Body

### Step 1: Create Spec Card Image

1. Photograph the body with measurement annotations (bust, waist, hip lines).
2. Save as WebP: `assets/Measure/{BodyCode}_pc_3.0.webp`
   - Example: `assets/Measure/ZX175E_pc_3.0.webp`
3. Dimensions: ~800×1200px (fits on mobile + desktop).

### Step 2: Add Measurement Data

Edit `db/body_measurements.json`:

```json
{
  "bodies": [
    …,
    {
      "body_code": "ZX175E",
      "height_cm": 175,
      "cup": "E",
      "weight_kg": 42.0,
      "bust": 96.5,
      "waist": 70.0,
      "hip": 104.5,
      "bust_drop_cm": 26.5,
      "spec_card": "assets/Measure/ZX175E_pc_3.0.webp",
      "notes": "New 2026 body, Muse family"
    }
  ]
}
```

**Fields:**
- `body_code`: Unique identifier (follows pattern `Z[Series][Height][Cup]`)
- Measurements in **cm** (verified from physical product)
- `spec_card`: Path relative to repo root
- `notes`: Optional, for documentation

### Step 3: Verify Classification

Run the build:

```bash
python scripts/build_orchestrator.py
```

**Expected output:**
- Build completes successfully
- `db/body_profiles.json` includes your new body with computed WHR/BWR
- Family assigned automatically (or set to `null` if out-of-range)

**Check family assignment:**

```bash
python -c "
import json
with open('db/body_profiles.json') as f:
  profiles = json.load(f)
  for body in profiles['bodies']:
    if body['body_code'] == 'ZX175E':
      print(f\"WHR: {body['whr']:.3f}, BWR: {body['bwr']:.3f}, Family: {body['family']}\")
"
```

### Step 4: Override Family (if needed)

If auto-classification is wrong, edit `db/body_measurements.json`:

```json
{
  "body_code": "ZX175E",
  …,
  "family_override": "The Muse"
}
```

Re-run: `python scripts/build_orchestrator.py`

### Step 5: Link Photoshoots

Create product folders for each head+body combination:

```
assets/SLE-Series/ZXE225_1+ZX175E/
  ├─ ZXE225_1+ZX175E-101.jpg     (hero image)
  ├─ ZXE225_1+ZX175E-102.jpg
  ├─ ZXE225_1+ZX175E-103.jpg
  └─ …(40 more images)

assets/SLE-Series/ZXE226_2+ZX175E/
  └─ …(similar structure)
```

**File naming:** `{HeadCode}+{BodyCode}-{Sequence:03d}.jpg`

### Step 6: Generate Characters

Run build:

```bash
python scripts/build_orchestrator.py
```

**Expected:**
- `build_characters.py` finds photoshoots for this body
- Auto-generates 4 character records in `db/characters.json`
- Each character gets an auto-generated name + tagline (from family + series voice)

**Check:**

```bash
python -c "
import json
with open('db/characters.json') as f:
  chars = json.load(f)
  for c in chars:
    if 'ZX175E' in c.get('character_id', ''):
      print(c['character_id'], '-', c['persona']['name'])
"
```

### Step 7: Curate Personas (Optional)

If auto-generated names/stories need polish, edit `db/character_overlay.json`:

```json
{
  "overrides": {
    "SLE-ZX175E-01": {
      "persona": {
        "name": "Luna",
        "title": "The Ascendant",
        "tagline": "Reaching for the stars."
      }
    }
  }
}
```

Re-run: `python scripts/build_orchestrator.py`

### Step 8: Deploy

```bash
git add db/body_measurements.json db/character_overlay.json
git commit -m "feat: add ZX175E body + 4 SLE characters"
git push origin feature/add-zx175e
# Open PR, get approval, merge to main
```

---

## Adding a New Character

### Scenario: Extra Photoshoot on Existing Body

If a body has >4 photoshoots, the surplus are pooled in `additional_photoshoots[]`. To promote one to a full character:

### Step 1: Identify Surplus Photoshoot

Check `db/body_types.json`:

```json
{
  "body_code": "ZG170C",
  …,
  "photoshoot_count": 7,
  "additional_photoshoots": ["GE02_1", "GE03_2", "GE04_1"]
}
```

Choose one (e.g., `GE02_1`).

### Step 2: Create Slot 5 Character Record

Edit `db/character_overlay.json`:

```json
{
  "overrides": {
    "I-ZG170C-05": {
      "persona": {
        "name": "Nova",
        "title": "The Ascendant",
        "tagline": "Bold, brilliant, boundless.",
        "story": "120–180 word narrative…"
      },
      "photoshoot": {
        "product_code": "ZGE02_1+ZG170C",
        "folder": "assets/I-Series/ZGE02_1+ZG170C",
        "hero": "assets/I-Series/ZGE02_1+ZG170C/ZGE02_1+ZG170C-101.jpg"
      }
    }
  }
}
```

### Step 3: Update Body Structure (Optional)

If you want this to be a permanent 5th character (not just an overlay), edit `db/body_measurements.json` to add a note:

```json
{
  "body_code": "ZG170C",
  …,
  "notes": "Now has 5 live characters (2026-06)"
}
```

### Step 4: Re-run Build

```bash
python scripts/build_orchestrator.py
```

### Step 5: Deploy

```bash
git add db/character_overlay.json
git commit -m "feat: add I-ZG170C-05 (Nova) from surplus photoshoot"
git push
```

---

## Editing Existing Characters

### Use Case: Fix a Name or Story

Edit `db/character_overlay.json`:

```json
{
  "overrides": {
    "SLE-ZX160J-03": {
      "persona": {
        "name": "Vesper",  // New name
        "story": "New story text…"  // New story
      }
    }
  }
}
```

**Re-run build:**
```bash
python scripts/build_orchestrator.py
```

**Verify:**
```bash
python -c "
import json
with open('db/characters.json') as f:
  chars = json.load(f)
  c = [c for c in chars if c['character_id'] == 'SLE-ZX160J-03'][0]
  print(c['persona']['name'], '—', c['persona']['story'][:100])
"
```

### Use Case: Change Hero Image

In `db/character_overlay.json`:

```json
{
  "overrides": {
    "SLE-ZX160J-03": {
      "photoshoot": {
        "hero": "assets/SLE-Series/ZXE223_1+ZX160J/ZXE223_1+ZX160J-105.jpg"
      }
    }
  }
}
```

**File must exist** in the photoshoot folder.

### Use Case: Mark as Placeholder

In `db/character_overlay.json`:

```json
{
  "overrides": {
    "Fusion-ZF169C-04": {
      "status": "placeholder",
      "placeholder": {
        "reason": "Awaiting new head photoshoot",
        "art_direction": "Tan skin, studio light, ¾ view"
      }
    }
  }
}
```

---

## Updating Body Measurements

### Scenario: Corrected Spec Card

A body's measurements were slightly off. Update in `db/body_measurements.json`:

```json
{
  "body_code": "ZG170C",
  "height_cm": 170,
  "bust": 89.4,        // Updated from 89.0
  "waist": 65.8,
  "hip": 96.0,
  "spec_card": "assets/Measure/ZG170C_pc_3.1.webp"  // New version
}
```

**Re-run build:**
```bash
python scripts/build_orchestrator.py --reset
```

(Use `--reset` to recalculate WHR/BWR and potentially reclassify family.)

**Verify classification:**
```bash
python -c "
import json
with open('db/body_profiles.json') as f:
  profiles = json.load(f)
  body = [b for b in profiles['bodies'] if b['body_code'] == 'ZG170C'][0]
  print(f\"WHR: {body['whr']:.3f}, BWR: {body['bwr']:.3f}, Family: {body['family']}\")
"
```

---

## Adding a New Series

**Warning:** This is a major change. Requires:
- New asset folder structure
- New body types (minimum 2–4)
- 8–20 new characters
- New marketing narrative

### High-Level Steps

1. **Create asset folder:** `assets/{NewSeriesName}/`
2. **Add series metadata:** Edit `db/catalog.json` (manually or via script).
3. **Add bodies:** Edit `db/body_measurements.json` with new body codes.
4. **Add photoshoots:** Create `assets/{NewSeriesName}/{HeadCode}+{BodyCode}/` folders with images.
5. **Run build:**
   ```bash
   python scripts/build_orchestrator.py --reset
   ```
6. **Curate personas:** Edit `db/character_overlay.json` + `db/_stories_newseries.json`.
7. **Deploy:** PR + merge to main.

### Example: Adding "Classic Collection" Series

1. **`db/body_measurements.json`:**
   ```json
   {
     "body_code": "ZC160D",
     "height_cm": 160,
     …
   },
   {
     "body_code": "ZC165E",
     …
   }
   ```

2. **Create story file:** `db/_stories_classic.json`
   ```json
   {
     "Classic-ZC160D-01": {
       "story": "…",
       "profile": {…}
     }
   }
   ```

3. **Run build:** `python scripts/build_orchestrator.py --reset`

4. **Update site:** Add navigation link in `assets/site.js` (SERIES_ORDER).

---

## Deploying Changes

### Pre-Deployment Checklist

- [ ] **Config:** `assets/site.js` has correct `INQUIRY_EMAIL` + `FORM_ENDPOINT`
- [ ] **Analytics:** PDR thresholds are current (`docs/pdr/PDR-analytics-sanity-thresholds.json`)
- [ ] **Build:** `python scripts/build_orchestrator.py --reset` succeeds
- [ ] **Tests:** `pytest` + `npm test` both pass
- [ ] **Staging:** Deploy to staging branch; verify all pages load
- [ ] **CI/CD:** GitHub Actions pass (linter, tests, build)
- [ ] **Data:** No uncommitted changes to `db/*.json`

### Deployment Steps

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/add-zx175e-body
   ```

2. **Make changes:**
   ```bash
   # Edit db/body_measurements.json, db/character_overlay.json, etc.
   python scripts/build_orchestrator.py
   ```

3. **Commit:**
   ```bash
   git add db/ assets/
   git commit -m "feat: add ZX175E body + 4 SLE characters"
   ```

4. **Open PR:**
   ```bash
   git push origin feature/add-zx175e-body
   # Open PR on GitHub; request review
   ```

5. **Merge:**
   - Get approval
   - GitHub Actions tests pass
   - Merge to `main`

6. **Deploy to Netlify:**
   - Automatic (CI/CD triggers on `main` push)
   - Or manual: `netlify deploy --prod`

7. **Verify:**
   - Visit https://zelexdoll.com
   - Check browse.html, new characters visible
   - Test comparison tool, quiz

---

## Rolling Back

### Scenario: Deployed a Bug

1. **Identify the commit:**
   ```bash
   git log --oneline main | head -10
   ```

2. **Revert:**
   ```bash
   git revert {commit-hash}
   git push
   ```
   (Creates a new commit that undoes the bad one.)

3. **Or reset hard (destructive):**
   ```bash
   git reset --hard origin/main~1
   git push --force-with-lease
   ```
   (Use only if PR never went live.)

---

## Data Recovery

### Scenario: Accidentally Deleted Characters

1. **Check git history:**
   ```bash
   git log --oneline -p -- db/character_overlay.json | head -50
   ```

2. **Find the commit before deletion:**
   ```bash
   git show {commit-hash}:db/character_overlay.json > /tmp/recovery.json
   ```

3. **Restore:**
   ```bash
   cp /tmp/recovery.json db/character_overlay.json
   git add db/character_overlay.json
   git commit -m "fix: restore character overlay from commit {hash}"
   git push
   ```

### Scenario: Database Corruption

SQLite `db/catalog.db` is transient and rebuilt every run. To recover:

```bash
rm db/catalog.db
python scripts/build_orchestrator.py --reset
```

If the issue persists, check the source data (`db/*.json`, `db/body_measurements.json`).

---

## Performance Tuning

### Build Speed

**Current:** ~15 seconds (parallel execution)

To profile:

```bash
time python scripts/build_orchestrator.py
```

### Slowest Stages

1. **`thumbs`** (~5s) — Generating 100+ thumbnail images.
   - Mitigation: Run only on major image changes.
   - Command: `python scripts/build_orchestrator.py --stages=thumbs`

2. **`characters`** (~4s) — Processing 108 character records.
   - Mitigation: Use `--resume` if only one stage failed.

### Page Load Time

**Browser-side:**
- `db/catalog.json` (~30 KB) loads immediately
- Images lazy-loaded (`loading="lazy"`)
- No JS parsing overhead (single 35 KB file)

**CDN caching:**
- Set far-future expires on images (1 year)
- Invalidate on deploy (version hash in path, or Netlify purge)

---

## Troubleshooting

### Issue: Build fails with "Input hash mismatch"

**Cause:** Git doesn't track image folders; `db/catalog.db` can't find assets.

**Fix:**
```bash
python scripts/build_orchestrator.py --reset
```

---

### Issue: Character not appearing in browse.html

**Cause:** Character status is `"placeholder"` (hidden by default).

**Check:**
```bash
python -c "
import json
with open('db/characters.json') as f:
  chars = json.load(f)
  for c in chars:
    if c['character_id'] == 'SLE-ZX160J-03':
      print('Status:', c['status'])
"
```

**Fix:** Change `status` to `"live"` in `db/character_overlay.json`.

---

### Issue: WHR/BWR out of range; family is null

**Cause:** Body measurements fall outside all family ranges.

**Check:**
```bash
python -c "
import json
with open('db/body_profiles.json') as f:
  profiles = json.load(f)
  for b in profiles['bodies']:
    if b['body_code'] == 'ZX175E':
      print(f\"WHR: {b['whr']:.3f} (range), BWR: {b['bwr']:.3f}\")
      print(f\"Family: {b['family']}\")
"
```

**Fix:** Manually assign family via `family_override`:
```json
{
  "body_code": "ZX175E",
  "family_override": "The Empress"
}
```

---

### Issue: Images not loading in packaged build

**Cause:** Images were synced to local asset folders but not included in ZIP.

**Fix:**
```bash
# Ensure images exist locally
ls assets/SLE-Series/ZXE223_1+ZX160J/

# Re-run package builder
python scripts/build_package.py

# Re-upload ZIP
```

---

### Issue: Analytics events not tracking

**Cause:** `FORM_ENDPOINT` is empty; tracking falls back to debug mode.

**Check:** Open browser console:
```javascript
ZX.analyticsDebugEnabled()  // Should be false
ZX.getSessionId()           // Should return session ID
```

**Fix:** Ensure GA4 property ID is set in tracking config (see CLAUDE.md).

---

## References

- [ARCHITECTURE.md](ARCHITECTURE.md) — System design
- [DATA-SCHEMA.md](DATA-SCHEMA.md) — Schema reference
- [API.md](API.md) — Runtime API
- [GLOSSARY.md](GLOSSARY.md) — Terminology
- `scripts/build_orchestrator.py` — Build pipeline code
- `docs/BUILD-ORCHESTRATOR.md` — Detailed build docs
