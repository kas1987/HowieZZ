# Agent Source Material Bundle

This folder groups the current competitor-analysis artifacts into a handoff package for other agents.

## Primary Entry Points

- Human overview: `docs/PDR-010-competitor-lineup-brief.md`
- Narrative matrix: `docs/research/independent-catalog-grouping-heatmap.md`
- Machine payload: `db/independent_catalog_groupings.json`
- Bundle manifest: `docs/agent-source-material/manifest.json`

## Grouping Model

The manifest groups artifacts into six buckets:

1. Executive Context
2. Independent Competitor Groupings
3. Competitor Family Coverage
4. Visual Assets
5. Source Catalog Datasets
6. Generation Pipeline

## Recommended Consumption Order

1. Read executive context for current findings and ranking logic.
2. Load machine payload and CSV for structured downstream analysis.
3. Use SQLite databases for custom SQL slices.
4. Consult source datasets only when lineage validation is needed.
5. Re-run pipeline scripts to refresh grouped outputs when data updates.

## Notes

- WM Doll depth and ZELEX normalization are already reflected in grouped artifacts.
- PNG heatmaps are included for presentation and quick inspection workflows.
- Keep this bundle updated whenever new grouped outputs are generated.
