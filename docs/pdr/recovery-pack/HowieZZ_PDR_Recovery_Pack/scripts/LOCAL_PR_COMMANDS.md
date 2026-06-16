# Local PR Commands for HowieZZ Recovery

```bash
git checkout main
git pull
git checkout -b pdr-000-recovery-source-of-truth

mkdir -p docs/pdr docs/handoffs docs/research command-center

# Copy this package's docs into the repo root, preserving paths.
# Example:
# cp -R HowieZZ_PDR_Recovery_Pack/docs/* docs/
# cp -R HowieZZ_PDR_Recovery_Pack/command-center/* command-center/

git add docs/pdr docs/handoffs docs/research command-center README.md
git commit -m "Recover HowieZZ PDR source of truth"

gh pr create \
  --title "PDR-000: Recover HowieZZ source-of-truth backlog" \
  --body "Adds the recovered PDR source files, dispatch board, handoff packets, research templates, and Command Center sync plan for the ZELEX Character Atlas rebuild."
```
