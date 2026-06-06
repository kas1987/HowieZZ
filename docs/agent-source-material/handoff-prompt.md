# Handoff Prompt For Downstream Agent

Use this prompt when starting a new agent session for competitor-line analysis:

---
You are continuing analysis using a pre-grouped source bundle.

Start with these files in order:
1. docs/PDR-010-competitor-lineup-brief.md
2. docs/research/independent-catalog-grouping-heatmap.md
3. db/independent_catalog_groupings.json
4. docs/agent-source-material/manifest.json

Rules:
- Treat manifest groups as the source-of-truth context map.
- Preserve WM Doll and ZELEX normalization assumptions already encoded in grouped outputs.
- If you need custom segmentation, query db/independent_competitor.sqlite.
- If findings depend on updated data, rerun scripts/analyze_independent_groupings.py and refresh derived artifacts.

Expected output:
- A concise insight memo.
- Any new segmentation tables and rationale.
- A change list of regenerated artifacts.
---
