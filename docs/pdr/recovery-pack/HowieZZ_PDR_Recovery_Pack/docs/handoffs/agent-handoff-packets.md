# Agent Handoff Packets

## Cartographer — Homepage + Compare
- task_id: HZZ-P1-001 / HZZ-P1-002
- mission: finish the first visible buyer-decision flow.
- source_files: `index.html`, `assets/site.css`, `assets/site.js`, `compare.html`
- allowed_actions: add static HTML/CSS/JS, use existing `ZX.load()` model, preserve static hosting.
- blocked_actions: do not rewrite stack, do not require React/Next, do not move images into git.
- acceptance_criteria: homepage routes to quiz/compare/contact; compare page compares 2-4 bodies; mobile stable.
- stop_condition: data shape mismatch or missing HowieZZ write target.

## Archivist — PDR + Taxonomy
- task_id: HZZ-P0-001 / HZZ-P2-003
- mission: make HowieZZ PDRs the source of truth.
- source_files: `docs/pdr/*`, `docs/taxonomy/*`, `db/*.json`
- acceptance_criteria: all PDRs exist; taxonomy is documented; Command Center references not duplicates.

## Auditor — Governance + PII
- task_id: HZZ-P1-003
- mission: validate evidence, no PII leakage, acceptance gates.
- source_files: `contact.html`, `assets/site.js`, `docs/pdr/*`
- acceptance_criteria: event payloads exclude PII; estimated specs marked honestly; launch blockers recorded.

## Financier — Competitor ROI
- task_id: HZZ-P2-004
- mission: prove whether the six-family system creates ROI.
- source_files: `docs/research/*`, competitor source URLs.
- acceptance_criteria: 80+ body profiles or blocker; ROI score by family; CEO-facing recommendation.

## Sentinel — SEO/CI/Quality
- task_id: HZZ-P3-001
- mission: add metadata generation and keep CI safe.
- source_files: `scripts/*`, `assets/*`, `*.html`
- acceptance_criteria: static server works; sitemap/metadata generated; no broken no-JS states.
