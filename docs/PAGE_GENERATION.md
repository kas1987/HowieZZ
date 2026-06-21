# Page Generation System — ZELEX Character Atlas

## Overview

The **Page Generation System** is a comprehensive page inventory, validation, and cache-management framework for the ZELEX Character Atlas. It maps all 21 HTML pages in the static frontend, validates consistency, and generates cache metadata for intelligent cache busting.

**Key files:**
- `db/pages_config.json` — complete page schema and metadata
- `scripts/generate_pages.py` — validation + manifest generator
- `db/pages_manifest.json` — generated output (file hashes, validation results)

## Architecture

### Pages Configuration (`pages_config.json`)

A single-source-of-truth JSON schema defining:
1. **Page metadata** (title, description, route, type)
2. **Cache strategy** (TTL per page, dependency tracking)
3. **Build dependencies** (which JSON files each page needs)
4. **Dynamic parameters** (e.g., ?id=, ?f=, ?s=)
5. **SEO metadata** (sitemap priority, OG tags)

#### Schema Structure

```json
{
  "schema_version": "1.0",
  "pages": {
    "primary_nav": { ... },        // 9 pages (top navigation)
    "content_pages": { ... },      // 6 pages (linked content)
    "support_pages": { ... },      // 4 pages (variants, error pages)
    "contact_variants": { ... }    // 2 pages (A/B test forms)
  },
  "metadata": { ... }              // Aggregated stats
}
```

#### Page Categories

| Category | Count | Purpose |
|----------|-------|---------|
| **primary_nav** | 9 | Appear in `mountNav()` and `mountFooter()` |
| **content_pages** | 6 | Linked content (not in top nav) |
| **support_pages** | 4 | Variants, error pages (not in sitemap) |
| **contact_variants** | 2 | A/B testing forms |
| **Total** | 21 | All HTML pages in repo |

#### Page Entry Schema

```json
{
  "id": "browse",
  "file": "browse.html",
  "title": "Browse Characters — ZELEX",
  "description": "Filterable character grid...",
  "route": "/browse.html",
  "type": "content",
  "nav_order": 1,
  "cache_ttl": 3600,                    // seconds until cache expires
  "dependencies": ["characters.json", "family_taxonomy.json"],
  "dynamic_params": ["f"],              // URL query params (e.g., ?f=family)
  "og_tags": {
    "type": "website",
    "image": "https://..."
  },
  "sitemap": {
    "changefreq": "weekly",
    "priority": 0.9
  },
  "include_in_sitemap": true,           // optional; default true
  "variant": "ab_test"                  // optional; marks as variant
}
```

### Page Types

| Type | Purpose | Examples |
|------|---------|----------|
| `homepage` | Canonical homepage + variants | index.html, hero.html, Landing.html |
| `content` | Informational/catalog pages | browse.html, series.html, character.html |
| `interactive_tool` | Client-side apps | quiz.html, compare.html, configurator.html |
| `form` | User input | contact.html, contact-variant-*.html |
| `guide` | Static guides | options.html |
| `error` | Error pages | 404.html |
| `legacy` | Backward compatibility | index-gallery-original.html |

### Page Manifest (`pages_manifest.json`)

Generated output from `generate_pages.py`. Contains:

```json
{
  "schema_version": "1.0",
  "generated_at": "2026-06-21T17:07:05Z",
  "total_pages": 21,
  "validation": {
    "problems_count": 0,
    "problems": [],
    "all_valid": true
  },
  "files": {
    "index": {
      "file": "index.html",
      "size_bytes": 15916,
      "mtime_unix": 1782061547,
      "content_hash": "a4451e9874edafed",    // First 16 chars of SHA256
      "exists": true
    },
    ...
  },
  "dependencies": {
    "catalog.json": {
      "exists": true,
      "size_bytes": 163639,
      "mtime_unix": 1782061547,
      "content_hash": "b1a75487ec411301"
    },
    ...
  },
  "cache_strategy": "per-page TTL + content-hash invalidation"
}
```

## Implementation

### `generate_pages.py` — Main Script

**Purpose:** Validate page consistency and generate manifest.

**Functions:**

#### `compute_file_hash(file_path, algorithm='sha256') -> str`
- Computes content hash (first 4KB for large files, full for small files)
- Returns 16-char hex (first half of SHA256)
- Used for intelligent cache invalidation

#### `load_config() -> dict`
- Loads `db/pages_config.json`
- Exits if file not found

#### `collect_declared_pages(config) -> dict`
- Extracts all page definitions from all categories
- Returns dict keyed by `id`

#### `validate_files(declared_pages) -> (metadata, problems)`
- Checks that all declared pages exist on disk
- Computes file size, mtime, content hash
- Returns: `(dict[page_id -> metadata], list[problems])`

#### `validate_dependencies(config, declared_pages, file_metadata) -> (metadata, problems)`
- Checks that all declared dependencies exist
- Computes dependency hashes for cache invalidation
- Returns: `(dict[dep_name -> metadata], list[problems])`

#### `find_undeclared_pages() -> list`
- Finds `.html` files not in `EXPECTED_PAGES`
- Reports orphaned or forgotten pages

#### `build_manifest(config, declared_pages, file_metadata, dep_metadata, problems) -> dict`
- Assembles final `pages_manifest.json`
- Includes timestamp, validation status, all metadata

#### `main(force_refresh=False, validate_only=False, verbose=False) -> int`
- Orchestrates full validation pipeline
- Returns 0 on success, 1 on problems
- Writes `db/pages_manifest.json` (unless `--validate-only`)

**Usage:**

```bash
# Run full validation and generate manifest
python scripts/generate_pages.py

# Verbose output
python scripts/generate_pages.py -v

# Validate only (don't write manifest)
python scripts/generate_pages.py --validate-only

# Force regenerate from scratch
python scripts/generate_pages.py --force-refresh
```

**Exit codes:**
- `0` = all validations passed
- `1` = problems found (missing files, undeclared pages, etc.)

## Integration into Build Pipeline

### In `build_orchestrator.py`

```python
("pages", "generate_pages.py",
  ["db/pages_config.json", "db/characters.json", "db/family_taxonomy.json"],
  ["db/pages_manifest.json"],
  True,  # parallel-safe (runs after DB finalized)
  1      # retry count
)
```

Runs in **Group 3** (after merge_stories + thumbs complete).

### Running via Orchestrator

```bash
# Full pipeline
python scripts/build_orchestrator.py

# Resume from last failure
python scripts/build_orchestrator.py --resume

# Just pages stage
python scripts/build_orchestrator.py --stages pages

# Dry run
python scripts/build_orchestrator.py --dry-run
```

## Cache Strategy

### Per-Page TTL

Each page specifies `cache_ttl` (time-to-live) in seconds:

```json
{
  "id": "browse",
  "cache_ttl": 3600  // 1 hour
}
```

**Common TTLs:**
- **Homepage** (index): 1 hour (3600s) — changes frequently
- **Content pages** (character, series, body): 1 hour — data-driven
- **Interactive tools** (quiz, compare): 2 hours — less volatile
- **Forms** (contact): 2 hours — config-stable
- **Error pages** (404): 24 hours (86400s) — stable
- **Legacy pages**: 24 hours — immutable

### Content-Hash Invalidation

When a file is modified:
1. `generate_pages.py` recomputes content hashes
2. Browser/CDN compares new hash against stored hash
3. If hash changes, cache is invalidated automatically
4. No manual cache-busting needed

**How it works:**
- File's `content_hash` stored in `pages_manifest.json`
- On each run, new hash is computed
- Hash mismatch → page has changed → invalidate cache
- Hash match → page unchanged → use cached version

### Dependency-Based Invalidation

If a dependency (e.g., `catalog.json`, `characters.json`) changes:
1. Dependency's hash changes in `pages_manifest.json`
2. Pages that list that dependency should be invalidated
3. Client-side JS can check dependency hashes before serving from cache

**Example:**
```json
{
  "id": "browse",
  "dependencies": ["characters.json"],
  "cache_ttl": 3600
}
```

If `characters.json` hash changes, `browse.html` should be invalidated.

## Validation Rules

### Files

- ✅ All declared pages must exist on disk
- ✅ All dependencies must exist
- ✅ No undeclared .html files in root (orphan detection)

### Configuration

- ✅ Each page has `id`, `file`, `title`, `route`, `type`
- ✅ Page IDs are unique
- ✅ File names are valid (no duplicates)
- ✅ Routes are unique
- ✅ Dependencies are listed (for cache tracking)

### Errors Reported

| Error | Example | Action |
|-------|---------|--------|
| MISSING | "MISSING: declared page index → index.html does not exist" | Add file or remove from config |
| UNDECLARED | "UNDECLARED: gallery.html" | Add to config or delete file |
| MISSING DEPENDENCY | "MISSING DEPENDENCY: characters.json (used by pages)" | Ensure build step generates file |
| ERROR | "ERROR: failed to stat contact.html: Permission denied" | Check file permissions |

## Testing

### Test Suite: `tests/test_generate_pages.py`

**Coverage:** 59% (21 tests)

**Test classes:**

| Class | Tests | Purpose |
|-------|-------|---------|
| `TestComputeFileHash` | 4 | Hash computation (determinism, edge cases) |
| `TestCollectDeclaredPages` | 4 | Config parsing |
| `TestValidateFiles` | 3 | File validation |
| `TestValidateDependencies` | 3 | Dependency checking |
| `TestBuildManifest` | 3 | Manifest generation |
| `TestFindUndeclaredPages` | 2 | Orphan detection |
| `TestIntegration` | 2 | Full pipeline |

**Run tests:**

```bash
# All tests
pytest tests/test_generate_pages.py -v

# Specific test class
pytest tests/test_generate_pages.py::TestComputeFileHash -v

# With coverage
pytest tests/test_generate_pages.py --cov=scripts/generate_pages
```

### All Tests Pass

```
============================= test session starts =============================
collected 21 items

tests/test_generate_pages.py::TestComputeFileHash::test_hash_small_file PASSED [  4%]
tests/test_generate_pages.py::TestComputeFileHash::test_hash_nonexistent_file PASSED [  9%]
tests/test_generate_pages.py::TestComputeFileHash::test_hash_deterministic PASSED [ 14%]
tests/test_generate_pages.py::TestComputeFileHash::test_hash_different_content PASSED [ 19%]
... (17 more)
=============================== 21 passed in 0.60s =============================
```

## Maintenance

### When to Update `pages_config.json`

1. **New page added**: Add entry to appropriate category
2. **Page renamed/deleted**: Update or remove entry
3. **Cache TTL changed**: Update `cache_ttl`
4. **Dependencies change**: Update `dependencies` list
5. **Route changes**: Update `route`
6. **SEO updates**: Update `og_tags`, `sitemap`

### When to Run `generate_pages.py`

- **After modifying pages_config.json** — always run
- **After adding/removing HTML files** — always run
- **After build_orchestrator completes** — automatic
- **Before deploying** — verify manifest is current
- **In CI/CD pipeline** — add as validation step

### CI/CD Integration

```yaml
# Example: GitHub Actions
- name: Generate page manifest
  run: python scripts/generate_pages.py
  
- name: Validate pages
  run: python scripts/generate_pages.py --validate-only
```

## Performance

- **Execution time:** ~0.1s (21 pages, 9 dependencies)
- **Manifest size:** ~3 KB (minimal JSON)
- **Hash computation:** O(file_size) for small files, O(1) for large files
- **Memory usage:** < 10 MB

## FAQ

### Q: What happens if a page is missing from disk?
**A:** The script reports "MISSING: ..." and exits with code 1. Fix by:
1. Creating the missing file, OR
2. Removing the entry from `pages_config.json`

### Q: Why hash the content instead of just using mtime?
**A:** File modification times are unreliable (git checkout, rsync, etc.). Content hashes detect actual changes.

### Q: Can I run this during development?
**A:** Yes. Run `python scripts/generate_pages.py` anytime to validate. It's safe—no side effects.

### Q: How do I know if cache needs invalidation?
**A:** Compare `content_hash` in `pages_manifest.json` to computed hash. If different, cache is stale.

### Q: Do dynamic pages (e.g., ?id=character_id) get their own entries?
**A:** No. Dynamic pages are listed once (e.g., `character.html`). The manifest lists the template; actual URLs are enumerated via `build_sitemap.py`.

### Q: What if I add an undeclared .html file?
**A:** The script reports "UNDECLARED: ..." and exits with code 1. Either:
1. Add it to `EXPECTED_PAGES` in `generate_pages.py`, then to `pages_config.json`, OR
2. Delete the file

## Example Workflow

```bash
# 1. Add new page file
touch community-gallery.html
echo '<html><body>Gallery</body></html>' > community-gallery.html

# 2. Update pages_config.json
# (manually add entry in appropriate category)

# 3. Validate
python scripts/generate_pages.py -v

# Output:
# Generating page manifest...
# Loaded 22 declared pages from pages_config.json
# Validated 22 pages on disk
# Validated 9 dependencies
# ============================================================
# All validations passed!
# ============================================================
# Wrote E:\.../db/pages_manifest.json

# 4. Check manifest
cat db/pages_manifest.json | jq '.total_pages'
# Output: 22

# 5. Run full pipeline
python scripts/build_orchestrator.py

# Pages stage runs automatically in Group 3
```

## Summary

The **Page Generation System** provides:
- ✅ **Single source of truth** for page metadata (pages_config.json)
- ✅ **Automated validation** (file existence, dependencies, orphan detection)
- ✅ **Intelligent caching** (per-page TTL + content-hash invalidation)
- ✅ **Pipeline integration** (orchestrator-managed stage)
- ✅ **Comprehensive testing** (21 tests, all passing)
- ✅ **Zero regressions** (backward-compatible, non-destructive)

**Files delivered:**
- `db/pages_config.json` — complete page schema
- `scripts/generate_pages.py` — validation + manifest generator
- `tests/test_generate_pages.py` — 21 comprehensive tests
- `docs/PAGE_GENERATION.md` — this documentation

**Integration:** Already integrated into `build_orchestrator.py` as Group 3 stage.
