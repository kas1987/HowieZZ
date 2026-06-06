# Character story + profile schema (build contract)

Each story writer outputs a JSON object keyed by `character_id`, written to
`db/_stories_<series>.json` (lowercase series slug: k-series, inspiration, fusion, sle).
`scripts/build_characters.py` merges these into each character's `persona.story` and
`persona.profile`, then the front-end renders them.

## Exact output shape
```json
{
  "Inspiration-ZG170C-01": {
    "story": "120–180 word second-or-third-person narrative ...",
    "profile": {
      "personality": "3–5 adjectives or a short phrase",
      "ideal_setting": "where she belongs / the scene she evokes",
      "signature": "the one detail that makes her unmistakably hers",
      "for_you_if": "the buyer she's made for — finish the sentence 'For you if ...'"
    }
  },
  "...": { ... }
}
```

## Voice & grounding rules
- Voice = the ZELEX CEO Executive Brief: confident, editorial, premium, emotionally intelligent,
  never crude. Think a fashion house's character bible, not a product blurb. Read the brief first.
- GROUND every story in the character's real data — do not contradict it:
  - Use her actual `height_cm`, `cup`, and `body.family` / `silhouette`. Never call a 159cm body "tall";
    never call a B-cup "voluptuous". If `family` is null (Unclassified), lean on height/cup/series mood
    instead of inventing a silhouette.
  - Honor her `title` and `tagline` — the story should feel like the same person.
  - The 4 characters on one body share a silhouette but are DIFFERENT individuals (different head/face,
    name, title). Make each story distinct in personality and life — no copy-paste, no near-duplicates
    among siblings.
- Series flavor:
  - K-Series — Korean-creative flagship; refined, contemporary, artful.
  - Inspiration — Western naturalism; believable, warm, hip-led "muse" energy.
  - Fusion — movable-jaw realism; quiet luxury, understated.
  - SLE — widest spectrum; range from athletic minimalism to maximal fantasy/glamour. Match the body.
- Placeholder characters (status != "live"): write the story anyway (it's about the character, not the
  photo). Keep it aspirational; do not mention that a photoshoot is pending.
- Absolutely no torso references — every body here is a full standing figure.
- Keep each story 120–180 words. Keep profile fields tight (a phrase each, not paragraphs).
- Output STRICT valid JSON only in the file. No markdown, no comments, no trailing commas.
