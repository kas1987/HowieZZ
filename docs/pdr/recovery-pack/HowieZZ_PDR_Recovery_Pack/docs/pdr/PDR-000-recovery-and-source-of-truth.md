# PDR-000: Recovery and Source-of-Truth Alignment

## Objective
Reset the HowieZZ / ZZhowie HTML rebuild so all future implementation flows from PDR files inside `kas1987/HowieZZ`, not from scattered issues in Command Center, 3D_Meta, or chat history.

## Problem
Earlier PDR issues were generated through a GitHub connector that routed writes to the wrong repositories. This caused planning artifacts to exist outside the implementation repo and likely caused agents to work from incomplete or displaced instructions.

## Non-negotiable decision
`kas1987/HowieZZ` is the implementation source of truth.

## Scope
- Add all PDR files to `docs/pdr/`.
- Add handoff board to `docs/handoffs/`.
- Add research templates to `docs/research/`.
- Define repo routing rules.
- Define stop conditions for agents.

## Acceptance criteria
- All PDRs exist inside HowieZZ.
- Command Center references HowieZZ PDR paths, not duplicated bodies.
- No agent treats Command Center or 3D_Meta issues as implementation authority.
- Every task has owner, evidence, acceptance criteria, and stop condition.

## Owner roles
Archivist, Auditor, Cartographer, Chainbreaker.
