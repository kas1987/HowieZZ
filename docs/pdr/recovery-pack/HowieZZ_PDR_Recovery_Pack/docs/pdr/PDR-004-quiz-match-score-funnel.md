# PDR-004: Quiz Match-Score Funnel

## Objective
Turn the quiz into an intelligent discovery funnel that returns ranked family scores, explanations, recommended characters, compare handoff, and contact prefill.

## Scope
- Show top 3 family scores and percentages.
- Explain why the winning family was selected.
- Recommend 3-4 characters with roles.
- Persist quiz result to localStorage.
- Add CTAs: Compare matches, Browse family, Ask concierge.
- Pass quiz result to contact flow.

## Acceptance criteria
- Result includes score ranking, not just a winner.
- Recommended characters include reasoning.
- Families with no live bodies can be marked in-development rather than broken.
- Contact handoff includes quiz summary.

## Dependencies
PDR-003 and PDR-006.

## Owner
Cartographer.
