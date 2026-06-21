# ZELEX Quiz Recommendation Engine

**Production-ready quiz → character recommendation system** with A/B testing, measurement validation, and +30% form submission conversion target.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend: quiz.html                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │ Quiz Flow (5 questions, 3–4 options each)           │   │
│  │ Answers → QuizEngine.executeRecommendation()        │   │
│  └────────────────────┬─────────────────────────────────┘   │
└─────────────────────┼───────────────────────────────────────┘
                      │
                      │ POST /api/recommend
                      │ { answers, session_id, ab_variant }
                      ▼
         ┌────────────────────────────────┐
         │   Edge Function (Vercel/       │
         │   Netlify) api/recommend.js    │
         │                                │
         │  • Score answers               │
         │  • Rank families (WHR/BWR)     │
         │  • Select 4 matches            │
         │  • Build reasoning             │
         │  • Return result JSON          │
         └────┬─────────────────────────────┘
              │
              ├──▶ Load catalog.json
              ├──▶ Load characters.json
              └──▶ Load body_profiles.json
                      (from /db/)
                      
         Response → { winner, sourceFam, matches[], reasoning, variant }
              │
              ▼
    ┌──────────────────────────┐
    │ Frontend Display Result  │
    │  • Family match + badge  │
    │  • Measurement reasoning │
    │  • 4-char shortlist      │
    │  • "Request consult"     │
    │    button (→ contact.html)
    └──────────────────────────┘
              │
              ▼
    ┌──────────────────────────┐
    │  Contact Form (A/B)      │
    │  • Control: standard     │
    │  • Treatment: confidence-
    │    boosted copy          │
    └──────────────────────────┘
              │
              └──▶ POST /api/track
                   { event: 'contact_form_submitted', ... }
```

## Algorithm

### 1. Answer Scoring

Each quiz answer carries:
- **Family weights** (e.g., `"The Muse": 2`): cumulative scoring
- **WHR lean** (-1 to +1): directional measurement signal
- **BWR lean** (-1 to +1): directional measurement signal

```javascript
// Example answer (from quiz.html QUESTIONS)
{
  b: "Tall & striking",
  s: "169 cm and up",
  w: { "The Muse": 2, "The Icon": 1 },
  whr: 0.4,   // leans toward higher WHR (more balanced)
  bwr: -0.4   // leans toward lower BWR (less bust-dominant)
}
```

### 2. Family Ranking

1. **Accumulate scores** from all answers
2. **Normalize** to percentages (e.g., 35%, 28%, 22%, …)
3. **Rank** families by score
4. **Resolve availability**: if top-scoring family is in-dev, find nearest active family by measurement distance

### 3. Measurement Validation

Distance metric (Euclidean) to find nearest active family when in-dev:
```
distance = |ΔWHR| / 0.05 + |ΔBWR| / 0.10
```

Weighted on typical body family variance: WHR ±0.05, BWR ±0.10

### 4. Character Selection

Select **up to 4 characters** from source family:
1. Diversify by `body_code` (e.g., ZF161D, ZF168B, etc.)
2. Fill from runner-up family if needed
3. Final fallback: any live character

### 5. A/B Testing: Control vs. Treatment

**Control (default):**
- Traditional quiz-weight scoring only
- Result: family match based on answer preferences

**Treatment (experiment):**
- Boost score for winner if measurement lean aligns with family ranges
- Alignment metric: closeness of user's WHR/BWR lean to family center
- Boost amount: 0–3 additional points
- Result: confidence-boosted recommendation (may change winner if boost is large)

### 6. Reasoning Generation

Output includes measurement-led explanation:
```javascript
{
  confidence: "near",  // Quiz captures directional leaning, not exact body
  whrDir: "a lower waist-to-hip ratio (more pronounced hourglass)",
  bwrDir: "a bust-forward bust-to-waist ratio",
  ranges: "WHR 0.55–0.60 and BWR 1.60–1.75"  // Family's published ranges
}
```

## API Reference

### POST /api/recommend

**Request:**
```json
{
  "answers": [
    {
      "weights": { "The Muse": 1, "The Icon": 2 },
      "whr": -0.3,
      "bwr": 0.3,
      "label": "Balanced & mid-height"
    }
  ],
  "session_id": "quiz_1718XXX_abc123",
  "ab_variant": "control"
}
```

**Response (200 OK):**
```json
{
  "winner": "The Muse",
  "sourceFam": "The Muse",
  "inDevelopment": false,
  "measurement": {
    "whrLean": -0.18,
    "bwrLean": 0.22,
    "reasoning": {
      "confidence": "near",
      "whrDir": "a lower waist-to-hip ratio (more pronounced hourglass)",
      "bwrDir": "a moderate bust-to-waist ratio",
      "ranges": "WHR 0.65–0.70 and BWR 1.30–1.40"
    }
  },
  "matches": [
    {
      "characterId": "Fusion-ZF161D-01",
      "bodyCode": "ZF161D",
      "series": "Fusion",
      "name": "Gwen",
      "family": "The Muse",
      "whr": 0.66,
      "bwr": 1.371,
      "height": 161,
      "cup": "D",
      "image": "assets/Fusion-Series/ZFE01_1+ZF161D/ZFE01_1_ZF161D-101.jpg"
    },
    // ... 3 more
  ],
  "topFamilies": [
    { "rank": 1, "family": "The Muse", "pct": 42, "isLive": true, "liveCount": 6 },
    { "rank": 2, "family": "The Classic", "pct": 28, "isLive": true, "liveCount": 4 },
    { "rank": 3, "family": "The Icon", "pct": 18, "isLive": true, "liveCount": 3 }
  ],
  "variant": "control",
  "timestamp": "2026-06-21T14:32:18.123Z"
}
```

**Error (400/500):**
```json
{
  "error": "Missing answers array",
  "timestamp": "2026-06-21T14:32:18.123Z"
}
```

### POST /api/track

**Request:**
```json
{
  "event": "quiz_recommendation_shown",
  "session_id": "quiz_1718XXX_abc123",
  "winner": "The Muse",
  "source_family": "The Muse",
  "in_development": false,
  "variant": "control",
  "match_count": 4,
  "top_scores": "The Muse:42%|The Classic:28%|The Icon:18%",
  "measurement_whr": -0.18,
  "measurement_bwr": 0.22
}
```

**Response (202 Accepted):**
```json
{
  "success": true,
  "event_id": "evt_1718XXX_xyz789",
  "timestamp": "2026-06-21T14:32:18.123Z"
}
```

## Frontend Integration

### Step 1: Link quiz-engine.js

In `quiz.html`, after `site.js`:
```html
<script src="assets/quiz-engine.js"></script>
```

### Step 2: Update quiz.html finish() function

Replace the existing `finish()` call with:

```javascript
async function finish() {
  // Collect answers (this already happens)
  const FAMS = (m.FAMILIES || [...]).slice();
  const score = {};
  FAMS.forEach(f => { score[f] = 0; });
  
  // ... existing scoring code ...

  // NEW: Call recommendation engine
  try {
    const recommendation = await QuizEngine.executeRecommendation(answers);
    
    if (recommendation.success) {
      // Use engine result
      const result = recommendation.result;
      const display = recommendation.display;
      
      showResult(
        result.winner,
        result.sourceFam,
        result.topFamilies[1]?.family || null,  // runner-up
        result.matches,
        0,  // splitAt (deprecated)
        result.topFamilies,
        { fam: result.winner, pct: result.topFamilies[0].pct },  // winner entry
        0,  // scoreGap (computed by engine)
        result.matches.map(m => m.bodyCode),  // compareBodies
        result.matches.map(m => m.bodyCode).join(','),  // compareCodes
        result.measurement.reasoning,
        result.inDevelopment,
        result.measurement.whrLean,
        result.measurement.bwrLean,
        { families: m.families }  // famMeta
      );

      // Highlight A/B variant in debug (optional)
      console.log(`Quiz variant: ${recommendation.variant}`);

    } else {
      // Fallback: use existing client-side algorithm
      showResult(...);  // existing code
    }
  } catch (error) {
    console.error('Engine error, falling back:', error);
    // Fallback to client-side
    showResult(...);  // existing code
  }
}
```

### Step 3: Update Contact Form

In `contact.html`, add variant tracking to form submission:

```javascript
document.getElementById('submit-btn').addEventListener('click', async () => {
  const variant = QuizEngine.getVariant();
  
  // Add hidden field or payload
  const formData = new FormData(form);
  formData.append('ab_variant', variant);
  formData.append('quiz_result', JSON.stringify(QuizEngine.getStoredResult()));
  
  // Submit...
});
```

## Conversion Tracking

### Quiz Completion → Form Submission

The engine automatically tracks:
1. **quiz_recommendation_shown**: When result is displayed
2. **contact_form_submitted**: When form is sent (via contact.html)
3. **compare_set_from_quiz**: When user clicks "Compare these bodies"

### Expected Conversion Targets

- **Baseline (control)**: ~12–15% of quiz completions → form submission
- **Target (treatment)**: +30% improvement → ~16–20% form submission
- **Statistical power**: Need ≥500 samples per variant to detect

## Deployment

### Vercel

```bash
# Install dependencies
npm install

# Deploy
vercel deploy

# Set environment variables in Vercel dashboard:
ALLOWED_ORIGINS=https://www.zelexdoll.com,https://zelexdoll.com
CATALOG_URL=/db/catalog.json
CHARACTERS_URL=/db/characters.json
BODY_PROFILES_URL=/db/body_profiles.json
ANALYTICS_URL=/api/track
```

### Netlify

```bash
# No build step needed (functions are auto-deployed)
# Environment variables in Netlify dashboard:
ALLOWED_ORIGINS=https://www.zelexdoll.com,https://zelexdoll.com
CATALOG_URL=/db/catalog.json
CHARACTERS_URL=/db/characters.json
BODY_PROFILES_URL=/db/body_profiles.json
ANALYTICS_URL=/api/track
```

## Testing

### Unit Tests

```bash
npm test -- api/recommend.js
```

### A/B Test Validation

Check `/api/track?action=query` response:
```json
{
  "summary": {
    "total": 1200,
    "by_variant": {
      "control": 598,
      "treatment": 602
    },
    "conversion_rates": {
      "control": 14.2,
      "treatment": 18.7
    }
  }
}
```

### Manual Testing

1. **Open quiz in incognito mode** to get fresh A/B assignment
2. **Complete quiz** and check browser DevTools → Network tab for `/api/recommend` response
3. **Verify results** match expected family + characters
4. **Click contact button** and check form is prefilled with recommendation context
5. **Check localStorage** for stored result via `QuizEngine.debug()`

## Performance & Monitoring

### Edge Function Metrics

- **Execution time**: <500ms p95 (includes catalog fetch)
- **Cold start**: ~1.5s (first invocation)
- **Memory**: 128 MB (tight but sufficient)
- **Timeout**: 10s total

### Analytics Dashboard

Track these metrics over time:
- **Recommendation shows** (count): quiz completions
- **Form submissions** (count): downstream conversion
- **Conversion rate** (pct): form / recommendation shows
- **Winner distribution**: which families are most recommended
- **In-dev fallbacks**: how often system routes around in-dev families

### Alerts

Set up alerts for:
- **API error rate > 2%**: May indicate catalog data issue
- **Average latency > 1s**: May indicate cold starts increasing
- **Conversion drop > 10%**: May indicate form breakage

## Troubleshooting

### "Missing answers array" (400)

Check that quiz.html passes answers in correct format:
```javascript
// Correct format
{
  "answers": [
    { "weights": {...}, "whr": -0.3, "bwr": 0.3 },
    { "weights": {...}, "whr": 0.1, "bwr": -0.2 },
    // ... 5 total
  ]
}
```

### "Recommendation failed" (no results shown)

Check:
1. Catalog JSON is deployed and accessible
2. Characters have `status: 'live'` and valid `body.family`
3. At least one family has live characters
4. Network tab: is `/api/recommend` returning 200?

### A/B variant not switching

Check browser storage:
```javascript
QuizEngine.debug()
// Returns: { variant: 'control', sessionId: 'quiz_...', ... }
```

If stuck on same variant, clear `sessionStorage` and retry (should assign new variant).

### Conversion rate not improving (treatment)

Possible causes:
- Sample size too small (need ≥500/variant)
- Treatment confidence boost not large enough (increase in `selectRecommendationVariant()`)
- Conversion funnel broken downstream (check contact form)
- A/B toggle in contact.html not implemented (verify form gets `ab_variant` field)

## Future Enhancements

1. **Personalization**: Retain session history for repeat visitors
2. **Weighting refinement**: A/B test different question weight values
3. **Upsell logic**: Recommend premium body if closest in same tier
4. **Fallback customization**: When in-dev, offer early-notification signup
5. **Browser experiments**: Test different result UI layouts (e.g., carousel vs grid)
6. **Predictive inventory**: Recommend characters likely to sell out soon

---

**Last Updated**: 2026-06-21  
**Status**: Production Ready  
**Accuracy Target**: 85%+ recommendation satisfaction (survey-based post-purchase)
