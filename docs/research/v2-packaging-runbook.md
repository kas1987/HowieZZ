# v2 HTML Packaging Runbook

## Purpose
Keep [v2 HTML](v2%20HTML) as a deterministic snapshot of current root HTML pages.

## Script
- [scripts/refresh_v2_html.ps1](scripts/refresh_v2_html.ps1)

## Usage
- Default one pass:
  - `./scripts/refresh_v2_html.ps1`
- Explicit loop count:
  - `./scripts/refresh_v2_html.ps1 10`
- Placeholder-safe behavior:
  - If accidental `.` is passed, script falls back to loop count 1.

## Outputs
- [v2 HTML/manifest.json](v2%20HTML/manifest.json)
  - file list, sizes, hashes, generation timestamp, loop_count.
- [v2 HTML/manifest.sha256](v2%20HTML/manifest.sha256)
  - sha256 digest per HTML file.

## Best Practices
- Run script after any root `.html` change intended for packaged snapshots.
- Commit packaged HTML + manifest artifacts together for traceability.
- Use [ .github/scripts/validate-site.mjs ](.github/scripts/validate-site.mjs) before commit.
- Use [ .github/scripts/validate-pdr-path-task-files.mjs ](.github/scripts/validate-pdr-path-task-files.mjs) before commit.

## Notes
- Script prunes stale HTML files from [v2 HTML](v2%20HTML) before copying current root files.
- Non-HTML assets are intentionally not mirrored by this script.
