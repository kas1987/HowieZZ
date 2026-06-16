# Claude Project Rules

## PDR-first execution

All Claude tasks must include:

```text
PDR_PATH: <exact file path in this repo>
```

Blocking behavior:
- If `PDR_PATH` is missing, stop and request it.
- If the path does not exist, stop and request correction.
- Do not infer implementation scope from old Command Center issues.

Primary baseline for recovery work:
- `docs/pdr/recovery-pack/HowieZZ_PDR_Recovery_Pack/docs/pdr/PDR-000-recovery-and-source-of-truth.md`
