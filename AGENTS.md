# Agent Execution Contract

This repository does not allow free-form implementation from stale issue history.

## Mandatory task header

Every task for Claude, Codex, or Cursor must start with these fields:

```text
TASK_ID: <short-id>
PDR_PATH: <exact repo path to one PDR file>
OBJECTIVE: <single-sentence deliverable>
```

`PDR_PATH` must point to a real file inside this repository.

Accepted examples:
- `docs/pdr/recovery-pack/HowieZZ_PDR_Recovery_Pack/docs/pdr/PDR-000-recovery-and-source-of-truth.md`
- `docs/pdr/recovery-pack/HowieZZ_PDR_Recovery_Pack/docs/pdr/PDR-003-body-compare-tool.md`
- `docs/pdr/PDR-010-competitor-family-coverage-roi-validation.md`

## Scope rule

Implement only what is in the cited `PDR_PATH` plus directly required dependencies.
Do not derive requirements from old external issues unless they are mirrored into a repo PDR file.
