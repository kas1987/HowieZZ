# Build Pipeline Runbook

**Status:** Active (Phase 1)  
**Last Updated:** 2026-06-21  
**Owner:** Platform Engineering  
**Audience:** All developers, DevOps, data engineers

---

## Overview

This runbook explains the ZELEX build pipeline: how to run it, resume after failures, debug issues, and understand pipeline parallelization. The pipeline transforms raw assets + live feeds into a complete, deployable catalog site.

---

## Pipeline Architecture

```
Stage 1 (Scan)
├─ build_db.py            Scan assets + live product feed → catalog.db + catalog.json
│
Stage 2 (Classify)
├─ build_profiles.py      WHR/BWR analysis → classify into 6 Body Families
│
Stage 3 (Generate) [PARALLEL]
├─ build_characters.py    Series → Body → 4 characters → photoshoot|placeholder
├─ merge_stories.py       Fold story/profile inputs into characters.json
│
Stage 4 (Images) [PARALLEL]
├─ make_thumbs.py         Generate hero/gallery thumbnails
├─ push_assets_to_cdn.py  Upload images to CDN + manifest
│
Stage 5 (Package)
└─ build_package.py       Stage deliverable (code + images) + zip
```

**Total time (sequential):** ~2 minutes  
**Total time (parallelized):** <1 minute (50% improvement)

---

## Prerequisites

### Environment

- **Python 3.11+** with pip
- **SQLite3** (included in Python)
- **CDN credentials** (environment variables) for Stage 4
- **Live feed credentials** (API keys) for Stage 1

### Dependencies

```bash
pip install requests pillow tqdm pydantic
```

### Local Directory Structure

```
E:\HowieZZ\.claude\worktrees\amazing-tu-a4bd34\
├─ assets/                 # Local images (not tracked in git)
│  ├─ characters/          # Character photoshoots
│  ├─ series/              # Series imagery
│  └─ bodies/              # Body architecture images
├─ db/
│  ├─ catalog.db           # SQLite database (generated, not tracked)
│  ├─ catalog.json         # Catalog export (generated)
│  ├─ characters.json      # Final character data
│  ├─ assets_manifest.json # CDN manifest
│  ├─ character_overlay.json  # Hand-curated (tracked)
│  └─ body_measurements.json  # Hand-curated (tracked)
├─ scripts/
│  ├─ build_db.py
│  ├─ build_profiles.py
│  ├─ build_characters.py
│  ├─ merge_stories.py
│  ├─ make_thumbs.py
│  ├─ build_package.py
│  └─ build_orchestrator.py  # Master pipeline
└─ docs/
   └─ pipeline-guide.md
```

---

## Running the Full Pipeline

### Quick Start (One Command)

```bash
cd E:\HowieZZ\.claude\worktrees\amazing-tu-a4bd34

python scripts/build_orchestrator.py --full
```

**Output:**

```
Building ZELEX catalog...

[Stage 1] Scanning assets + feed... ✓ (12s)
  - Loaded 156 assets from local folders
  - Fetched 89 live products from feed
  - Database: db/catalog.db (2.1 MB)

[Stage 2] Classifying body families... ✓ (4s)
  - Analyzed WHR/BWR for 14 body types
  - Classified into 6 families
  - Output: db/profiles.json

[Stage 3] Generating characters (parallel)... ✓ (18s)
  ├─ build_characters.py... ✓ (10s)
  └─ merge_stories.py... ✓ (8s)
  - Generated 108 characters
  - Placeholder count: 12
  - Output: db/characters.json

[Stage 4] Processing images (parallel)... ✓ (22s)
  ├─ make_thumbs.py... ✓ (15s)
  └─ push_assets_to_cdn.py... ✓ (7s)
  - Thumbnail count: 268
  - CDN uploads: 4 new
  - Manifest: db/assets_manifest.json

[Stage 5] Packaging deliverable... ✓ (6s)
  - Code size: 1.8 MB
  - Images size: 258 MB
  - Output: build/zelex-site-2026-06-21.zip

Total time: 62 seconds ✓
Next step: Deploy build/zelex-site-*.zip to production
```

### Step-by-Step Execution

Run stages individually for debugging:

```bash
# Stage 1: Scan
python scripts/build_db.py
# Output: db/catalog.db, db/catalog.json

# Stage 2: Classify
python scripts/build_profiles.py
# Output: db/profiles.json

# Stage 3a: Generate characters
python scripts/build_characters.py
# Output: db/characters_raw.json

# Stage 3b: Merge stories
python scripts/merge_stories.py
# Output: db/characters.json (final)

# Stage 4a: Thumbnails
python scripts/make_thumbs.py
# Output: assets/*_thumb.jpg

# Stage 4b: Upload to CDN
python scripts/push_assets_to_cdn.py --incremental
# Output: db/assets_manifest.json

# Stage 5: Package
python scripts/build_package.py
# Output: build/zelex-site-*.zip
```

---

## Resuming After Failure

If a pipeline stage fails, resume from that stage without re-running earlier stages:

### Full Resume

```bash
python scripts/build_orchestrator.py --resume
```

**Output:**

```
Checking pipeline state...

Previously completed:
  ✓ [Stage 1] Scanning assets + feed
  ✓ [Stage 2] Classifying body families
  ✓ [Stage 3] Generating characters
  ✗ [Stage 4] Processing images (FAILED: CDN timeout)

Resuming from Stage 4...

[Stage 4] Processing images (parallel)... ✓ (22s)
  ├─ make_thumbs.py... ✓ (15s)
  └─ push_assets_to_cdn.py... ✓ (7s)

[Stage 5] Packaging deliverable... ✓ (6s)

Total time: 28 seconds ✓
```

### Resume from Specific Stage

```bash
# Skip to Stage 3
python scripts/build_orchestrator.py --resume --start-stage 3

# Skip to Stage 4
python scripts/build_orchestrator.py --resume --start-stage 4
```

### How Resume Works

The pipeline tracks state in `.build_state.json`:

```json
{
  "last_run": "2026-06-21T14:32:00Z",
  "stages_completed": [1, 2, 3],
  "stages_failed": [4],
  "retry_count": 1,
  "error": "CDN timeout on push_assets_to_cdn.py"
}
```

The `--resume` flag reads this file and skips completed stages.

---

## Retry Logic

The pipeline has exponential backoff retry logic:

```
Attempt 1: wait 1 second, retry
Attempt 2: wait 2 seconds, retry
Attempt 3: wait 4 seconds, retry
Attempt 4: wait 8 seconds, retry
(max 5 attempts, then fail)
```

### Manual Retry with Exponential Backoff

```bash
# Retry with aggressive retry policy (10 attempts)
python scripts/build_orchestrator.py --resume --max-retries 10

# Retry with gentle policy (2 attempts)
python scripts/build_orchestrator.py --resume --max-retries 2
```

### Skip Retry (Fail Fast)

```bash
python scripts/build_orchestrator.py --resume --no-retry
```

---

## Debugging Failures

### Issue: Stage 1 Fails (Asset Scan)

**Common causes:** Missing asset folder, corrupted image file, live feed API down

**Debug:**

```bash
# Check local folder structure
ls -R assets/

# Check for corrupt images
python scripts/debug_assets.py

# Check live feed connectivity
python -c "import requests; print(requests.get('https://api.product-feed.com/status').json())"
```

**Fix:**

```bash
# If images are missing: restore from backup or add new images
# If API is down: wait and retry, or skip live feed
python scripts/build_db.py --skip-live-feed

# Then resume
python scripts/build_orchestrator.py --resume --start-stage 2
```

### Issue: Stage 2 Fails (Classification)

**Common causes:** Invalid body measurements, missing WHR/BWR data

**Debug:**

```bash
# Check body measurements JSON
python -m json.tool db/body_measurements.json | head -50

# Validate profile calculation
python scripts/debug_profiles.py --body-code ZF161D
```

**Fix:**

```bash
# Update body_measurements.json with valid values
# (see docs/character-schema.md for schema)

# Then resume
python scripts/build_orchestrator.py --resume --start-stage 2
```

### Issue: Stage 3 Fails (Character Generation)

**Common causes:** Missing character names, invalid photoshoot structure

**Debug:**

```bash
# Check character data
python scripts/debug_characters.py --series Fusion

# Validate photoshoot structure
python scripts/debug_photoshoots.py
```

**Fix:**

```bash
# Update character_overlay.json with missing names/stories
# (see docs/character-profiles.md for schema)

# Then resume
python scripts/build_orchestrator.py --resume --start-stage 3
```

### Issue: Stage 4 Fails (Image Processing)

**Common causes:** CDN timeout, disk space, corrupted image file

**Debug:**

```bash
# Check disk space
du -sh assets/
df -h /   # or 'dir C:\' on Windows

# Check CDN connectivity
python scripts/test_cdn_connectivity.py

# Check for corrupt images
python scripts/find_corrupt_images.py
```

**Fix:**

```bash
# If CDN timeout: retry or use fallback provider
python scripts/build_orchestrator.py --resume --max-retries 10

# If disk full: delete old builds
rm -rf build/*

# If corrupt image: delete and regenerate thumbnails
rm assets/*_thumb.jpg
python scripts/make_thumbs.py
python scripts/build_orchestrator.py --resume --start-stage 4
```

### Issue: Stage 5 Fails (Packaging)

**Common causes:** Disk full, manifest missing, invalid zip structure

**Debug:**

```bash
# Check manifest exists
ls -lh db/assets_manifest.json

# Verify manifest integrity
python scripts/validate_manifest_freshness.py

# Check disk space
df -h /
```

**Fix:**

```bash
# If manifest missing: regenerate CDN manifest
python scripts/push_assets_to_cdn.py --refresh-manifest

# If disk full: clear build cache
rm -rf build/
python scripts/build_orchestrator.py --resume --start-stage 5
```

---

## Parallelization Details

### Stages That Run in Parallel

**Stage 3:** `build_characters.py` + `merge_stories.py`
```
Time: 18 seconds (parallel)
vs.  26 seconds (sequential) → 30% savings
```

**Stage 4:** `make_thumbs.py` + `push_assets_to_cdn.py`
```
Time: 22 seconds (parallel)
vs.  29 seconds (sequential) → 24% savings
```

### How Parallelization Works

```python
# In build_orchestrator.py
import concurrent.futures

with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    future_chars = executor.submit(build_characters.main)
    future_stories = executor.submit(merge_stories.main)
    
    # Wait for both to complete
    concurrent.futures.wait([future_chars, future_stories])
```

**Thread count:** 2 (configurable via `--workers`)

### Limitations

- **Thread-safe dependencies only:** Each stage must not conflict (no shared mutable state)
- **Stage order matters:** Stage 2 must complete before Stage 3 starts
- **I/O bottleneck:** Parallel stages may be I/O-bound (network, disk), not CPU-bound

---

## CI/CD Integration

### GitHub Actions Workflow

File: `.github/workflows/ci.yml`

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run build pipeline
        run: python scripts/build_orchestrator.py --full
        env:
          CDN_API_KEY: ${{ secrets.CDN_API_KEY }}
          CDN_API_SECRET: ${{ secrets.CDN_API_SECRET }}
      
      - name: Validate manifest freshness
        run: python scripts/validate_manifest_freshness.py
      
      - name: Upload build artifact
        uses: actions/upload-artifact@v3
        with:
          name: zelex-site-build
          path: build/
```

### Pre-Push Hook

File: `hooks/pre-push`

```bash
#!/bin/bash

echo "Running pre-push checks..."

# 1. Validate manifest freshness
python scripts/validate_manifest_freshness.py || exit 1

# 2. Run tests
npm test || exit 1
python -m pytest --tb=short -q || exit 1

# 3. Build pipeline sanity check (don't run full pipeline)
python scripts/build_orchestrator.py --validate-only || exit 1

echo "✓ All checks passed"
```

To skip pre-push checks (not recommended):

```bash
git push --no-verify
```

---

## Performance Tuning

### Build Time Breakdown

```
[Stage 1] 12s  - Network I/O (live feed API)
[Stage 2]  4s  - CPU (classification math)
[Stage 3] 18s  - I/O + CPU (character generation)
[Stage 4] 22s  - I/O (image upload, thumbnail generation)
[Stage 5]  6s  - I/O (zip creation)
Total:    62s
```

### Optimization Opportunities

1. **Cache live feed responses** (Stage 1)
   ```bash
   python scripts/build_db.py --cache-feed
   ```
   Reuses previous feed fetch if <24 hours old.

2. **Skip image upload** (Stage 4, for testing)
   ```bash
   python scripts/build_orchestrator.py --skip-cdn
   ```
   Builds locally but doesn't upload to CDN.

3. **Increase worker threads** (Stage 3-4)
   ```bash
   python scripts/build_orchestrator.py --full --workers 4
   ```
   Default is 2; increase if CPU available.

4. **Use SSD for temp files**
   ```bash
   TMPDIR=/fast-ssd python scripts/build_orchestrator.py --full
   ```

---

## Idempotence & Safety

All pipeline stages are **idempotent**—running twice gives the same result:

```bash
python scripts/build_orchestrator.py --full
# Output: build/zelex-site-2026-06-21-v1.zip

python scripts/build_orchestrator.py --full
# Output: build/zelex-site-2026-06-21-v2.zip (same content, new timestamp)
```

### Safe Operations

- ✓ Re-running any stage overwrites previous output
- ✓ Resuming after failure is safe (completed stages skipped)
- ✓ Parallel execution is thread-safe (no shared mutable state)

### Unsafe Operations

- ✗ Manually deleting `.build_state.json` (lose resume state)
- ✗ Running multiple pipelines simultaneously (race condition on db/catalog.db)
- ✗ Modifying db/ files during pipeline run (corruption)

---

## Cleanup & Maintenance

### Remove Old Builds

```bash
# Keep only last 5 builds
python scripts/cleanup_builds.py --keep 5

# Remove all builds older than 7 days
python scripts/cleanup_builds.py --older-than 7d
```

### Reset Pipeline State

```bash
# Clear build state (forces full re-run next time)
rm .build_state.json

# Clear all intermediate outputs
python scripts/cleanup_builds.py --full
```

### Archive Completed Builds

```bash
# Copy build to archive
cp build/zelex-site-*.zip archive/zelex-site-2026-06-21-final.zip
```

---

## FAQ

**Q: How do I skip a stage?**

A: Use `--start-stage`:
```bash
python scripts/build_orchestrator.py --full --start-stage 3
```

**Q: What if I want to run only Stage 1?**

A: Run the script directly:
```bash
python scripts/build_db.py
```

**Q: Can I run the pipeline without uploading to CDN?**

A: Yes:
```bash
python scripts/build_orchestrator.py --full --skip-cdn
```

**Q: What's the output deliverable?**

A: `build/zelex-site-2026-06-21.zip` (~260 MB) containing:
- All HTML pages
- assets/site.css + assets/site.js
- db/characters.json + db/assets_manifest.json
- All images (from CDN, fallback to git)

**Q: How do I deploy the build?**

A: See deployment guide (separate runbook).

---

## Support

For pipeline issues:
1. Check this runbook (search by keyword)
2. Run diagnostic scripts (see Debugging Failures)
3. Check log files in `.build_logs/`
4. Open issue: `chore(pipeline): [your issue]`

---

## References

- **Source PDR:** `docs/pdr/PDR-OPS-002-pipeline-parallelization.md`
- **Orchestrator:** `scripts/build_orchestrator.py`
- **Stage Scripts:** `scripts/build_*.py`, `scripts/merge_*.py`, `scripts/make_*.py`
- **CI Workflow:** `.github/workflows/ci.yml`
- **Data Schema:** `docs/character-schema.md`, `docs/character-profiles.md`
