# K-Series Persona Analysis (APX-B Alignment)

This maps Appendix B personas to current K-Series asset folders so each persona can be pulled as a real character library.

## APX-B Source
- Sora -> Character: Suyeon -> Body: ZK159D
- Lian -> Character: Arin -> Body: ZK168B
- Mira -> Character: Suyeon -> Body: ZK168B
- Zhen -> Character: Somi -> Body: ZK168B

## Folder Alignment
Three underlying K-model character sets exist in assets:
- Arin: `assets/K-Series/KE01_1+ZK168B-1`
- Suyeon: `assets/K-Series/KE02_1+ZK159D-1` and `assets/K-Series/KE02_1+ZK168B-1`
- Somi: `assets/K-Series/KE03_1+ZK168B-1`

Persona mapping:
- Sora (Suyeon, ZK159D) -> `KE02_1+ZK159D-1`
- Lian (Arin, ZK168B) -> `KE01_1+ZK168B-1`
- Mira (Suyeon, ZK168B) -> `KE02_1+ZK168B-1`
- Zhen (Somi, ZK168B) -> `KE03_1+ZK168B-1`

## Why This Matches "3 K-Models"
APX-B has 4 persona names but 3 underlying characters because Suyeon appears twice (Sora and Mira) on two body variants.

## Pull Strategy
Use `assets/data/k-series-personas.json` as the canonical persona library index.
- `personas.*.library` provides curated glamour images for each persona.
- `modelCharacters` provides grouped pull paths by underlying character.
- Hero and card components should pull from persona library arrays, not raw folders.
