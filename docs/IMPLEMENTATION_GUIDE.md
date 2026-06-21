# ZELEX Quiz Recommendation Engine — Implementation Guide

**Complete step-by-step integration of the recommendation engine into the quiz.html flow.**

---

## Overview

The current quiz.html has a working client-side recommendation algorithm. We're replacing it with a production-edge-function architecture that:

1. **Moves scoring logic to the edge** (Vercel/Netlify) for speed & consistency
2. **Adds measurement validation** (WHR/BWR alignment)
3. **Implements A/B testing** (control vs. treatment variants)
4. **Tracks conversions** to contact form
5. **Provides transparency** via measurement-grounded reasoning

---

## Phase 1: Add Frontend Integration Script

### 1.1 Link the quiz-engine.js in quiz.html

Open `quiz.html` and add this line **after the `<script src="assets/site.js"></script>` tag**:

```html
<script src="assets/site.js"></script>
<script src="assets/quiz-engine.js"></script>
```

### 1.2 Verify the script loads

In DevTools Console (quiz.html after page load):
```javascript
console.log(QuizEngine.debug());
// Should output:
// { variant: 'control' or 'treatment', sessionId: 'quiz_...', storedResult: null }
```

---

## Phase 2: Update quiz.html finish() Function

The `finish()` function currently does all client-side scoring. We'll call the edge function and fall back to client-side if it fails.

### 2.1 Find the finish() function

Locate this in `quiz.html` (around line 385):
```javascript
function finish() {
  // tally scores + accumulate the WHR/BWR directional leaning
  const FAMS = (m.FAMILIES || [...]).slice();
  const score = {};
  // ... existing code ...
}
```

### 2.2 Replace finish() with hybrid approach

Replace the entire `finish()` function with:

```javascript
async function finish() {
  // === Try edge function first ===
  try {
    const recommendation = await QuizEngine.executeRecommendation(answers);

    if (recommendation.success) {
      // Use server-computed recommendation
      const r = recommendation.result;
      const d = recommendation.display;

      // Map engine result to showResult() arguments
      showResult(
        r.winner,                                        // expressed
        r.sourceFam,                                      // sourceFam
        (r.topFamilies[1]?.family || null),              // runner (for fill logic)
        r.matches,                                        // matches (already 4 items)
        0,                                                 // splitAt (deprecated with engine)
        r.topFamilies,                                    // top3
        {
          fam: r.winner,
          score: r.topFamilies[0]?.pct || 0,
          pct: r.topFamilies[0]?.pct || 0,
          liveCount: r.topFamilies[0]?.liveCount || 0,
          inDev: r.inDevelopment
        },                                                // winnerEntry
        0,                                                 // scoreGap (computed by engine)
        r.matches.map(m => m.bodyCode),                  // compareBodies
        r.matches.map(m => m.bodyCode).join(','),        // compareCodes
        r.measurement.reasoning,                          // reasoning
        r.inDevelopment,                                  // inDev
        r.measurement.whrLean,                            // avgWhr
        r.measurement.bwrLean,                            // avgBwr
        { families: m.families }                          // famMeta
      );

      // Log variant assignment (debug)
      console.log(`[Quiz] Variant: ${recommendation.variant}, Session: ${recommendation.sessionId}`);
      return;

    } else if (recommendation.fallback) {
      // Engine unavailable, fall back to client-side
      console.warn('[Quiz] Recommendation engine unavailable, falling back to client-side');
      // Continue to fallback logic below
    }

  } catch (error) {
    console.error('[Quiz] Engine error:', error);
    // Continue to fallback logic
  }

  // === FALLBACK: Original client-side algorithm ===
  // [Keep existing finish() code here - untouched]
  const FAMS = (m.FAMILIES || ["The Classic","The Icon","The Muse","The Siren","The Empress","The Sculpt"]).slice();
  const score = {};
  FAMS.forEach(f => { score[f] = 0; });
  let whrLean = 0, bwrLean = 0, leanN = 0;
  answers.forEach(w => {
    Object.entries(w.w || {}).forEach(([f, v]) => { score[f] = (score[f] || 0) + v; });
    if (typeof w.whr === 'number') { whrLean += w.whr; leanN++; }
    if (typeof w.bwr === 'number') { bwrLean += w.bwr; }
  });
  const avgWhr = leanN ? whrLean / leanN : 0;
  const avgBwr = leanN ? bwrLean / leanN : 0;

  const famMeta = {};
  (m.families || []).forEach(fm => { famMeta[fm.name] = fm; });

  const ranked = FAMS.slice().sort((a, b) => score[b] - score[a]);
  const totalScore = Math.max(1, Object.values(score).reduce((a, v) => a + (v > 0 ? v : 0), 0));

  const live = m.characters.filter(c => c.status === 'live' && c.body && c.body.family);
  const liveByFam = f => live.filter(c => c.body.family === f);
  const isInDev = f => liveByFam(f).length === 0;

  const expressed = ranked[0];
  const win = ranked.find(f => liveByFam(f).length > 0) || expressed;

  const center = fm => fm ? [ (fm.whr[0]+fm.whr[1])/2, (fm.bwr[0]+fm.bwr[1])/2 ] : null;
  function nearestActive(fromFam) {
    const c0 = center(famMeta[fromFam]);
    let best = null, bestD = Infinity;
    FAMS.forEach(f => {
      if (isInDev(f)) return;
      const c1 = center(famMeta[f]);
      if (!c0 || !c1) return;
      const d = Math.abs(c0[0]-c1[0])/0.05 + Math.abs(c0[1]-c1[1])/0.10;
      if (d < bestD) { bestD = d; best = f; }
    });
    return best;
  }
  const inDevFallback = isInDev(expressed) ? (nearestActive(expressed) || win) : null;
  const sourceFam = inDevFallback || win;

  const pool = liveByFam(sourceFam);
  const seenBody = new Set();
  const matches = [];
  for (const c of pool) {
    if (!seenBody.has(c.body_code)) { matches.push(c); seenBody.add(c.body_code); }
    if (matches.length === 4) break;
  }
  for (const c of pool) {
    if (matches.length >= 4) break;
    if (!matches.includes(c)) matches.push(c);
  }

  const runner = ranked.find(f => f !== sourceFam && liveByFam(f).length > 0);
  const fillFrom = runner ? liveByFam(runner) : [];
  let fromSecond = 0;
  for (const c of fillFrom) {
    if (matches.length >= 4) break;
    if (!matches.includes(c)) { matches.push(c); fromSecond++; }
  }

  if (matches.length < 4) {
    const anyLive = m.characters.filter(c => c.status === 'live');
    for (const c of anyLive) {
      if (matches.length >= 4) break;
      if (!matches.includes(c)) matches.push(c);
    }
  }

  if (fromSecond > 0 && runner) {
    const firstRunnerIdx = matches.findIndex(c => c.body && c.body.family === runner);
    if (firstRunnerIdx !== -1) {
      fromSecond = matches.length - firstRunnerIdx;
    }
  }

  const splitAt = matches.length - fromSecond;
  const top3 = ranked.slice(0, 3).map((fam, idx) => ({
    idx: idx + 1,
    fam,
    score: score[fam],
    pct: Math.round((score[fam] / totalScore) * 100),
    liveCount: liveByFam(fam).length,
    inDev: isInDev(fam)
  }));

  const winnerEntry = top3.find(x => x.fam === expressed) || { fam: expressed, score: score[expressed], pct: 0, liveCount: liveByFam(expressed).length, inDev: isInDev(expressed) };
  const runnerScore = runner ? score[runner] : 0;
  const scoreGap = Math.max(0, score[expressed] - runnerScore);
  const compareBodies = Array.from(new Set(matches.map(c => c.body_code).filter(Boolean))).slice(0, 4);
  const compareCodes = compareBodies.join(',');

  const reasoning = buildReasoning(expressed, sourceFam, famMeta, avgWhr, avgBwr, matches, win);

  // ... rest of existing finish() code (unchanged) ...
  document.getElementById('pbar').style.width = '100%';
  hide('qscreen');
  showResult(expressed, sourceFam, runner, matches, splitAt, top3, winnerEntry, scoreGap, compareBodies, compareCodes, reasoning, isInDev(expressed), avgWhr, avgBwr, famMeta);
}
```

### 2.3 Verify fallback compiles

After editing, check DevTools Console when taking the quiz — should see no JavaScript errors.

---

## Phase 3: Deploy Edge Functions

### 3.1 For Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd /path/to/amazing-tu-a4bd34
vercel deploy

# Set production environment variables in Vercel dashboard:
# Settings → Environment Variables
ALLOWED_ORIGINS=https://www.zelexdoll.com,https://zelexdoll.com
CATALOG_URL=/db/catalog.json
CHARACTERS_URL=/db/characters.json
BODY_PROFILES_URL=/db/body_profiles.json
ANALYTICS_URL=/api/track
```

### 3.2 For Netlify

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Deploy
cd /path/to/amazing-tu-a4bd34
netlify deploy

# Set production environment variables in Netlify dashboard:
# Settings → Build & Deploy → Environment
ALLOWED_ORIGINS=https://www.zelexdoll.com,https://zelexdoll.com
CATALOG_URL=/db/catalog.json
CHARACTERS_URL=/db/characters.json
BODY_PROFILES_URL=/db/body_profiles.json
ANALYTICS_URL=/api/track
```

### 3.3 Test the API endpoint

```bash
# Get your API endpoint (Vercel or Netlify production URL)
curl -X POST https://your-domain.com/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "answers": [
      {"weights": {"The Muse": 2}, "whr": 0.3, "bwr": -0.2}
    ],
    "session_id": "test_123",
    "ab_variant": "control"
  }'

# Should return a JSON response with:
# { winner, sourceFam, matches: [...], measurement: {...}, ... }
```

---

## Phase 4: Update Contact Form (A/B Variant Tracking)

### 4.1 Locate form submission in contact.html

Find the form submit handler (around line 400–500 in contact.html):

```javascript
document.getElementById('submit-btn').addEventListener('click', async () => {
  // ... validation code ...
  const formData = new FormData(form);
  // ... submit to Formspree/Getform ...
});
```

### 4.2 Add variant tracking

Add these lines **before** form submission:

```javascript
// Track A/B variant (for analytics correlation)
const abVariant = QuizEngine.getVariant();
const quizResult = QuizEngine.getStoredResult();

formData.append('ab_variant', abVariant);
formData.append('quiz_winner', quizResult?.winner || 'unknown');
formData.append('quiz_session', quizResult?.sessionId || 'unknown');

// Log to analytics
if (window.ZX?.track) {
  window.ZX.track('contact_form_submitted', {
    ab_variant: abVariant,
    quiz_winner: quizResult?.winner,
    session_id: quizResult?.sessionId,
    source: 'quiz'
  });
}
```

---

## Phase 5: Monitor Conversion Metrics

### 5.1 Check analytics dashboard

Once live, visit:
```bash
npm run analyze:ab
```

This prints a summary like:
```
📊 ZELEX Quiz Engine — A/B Test Analysis
Period: Last 7 days

📈 Conversion Rates:
   Control:   14.2%
   Treatment: 18.7%
   Lift:      +31.6%

📊 Statistical Test (Chi-Square):
   χ² = 6.8431, p = 0.0089
   Result: ✓ SIGNIFICANT
```

### 5.2 Set up alerts

In your monitoring platform (Sentry, DataDog, etc.):

**Alert: High API Error Rate**
```
Condition: (errors / requests) > 0.02
Duration: 5 min
Action: Page oncall
```

**Alert: Conversion Drop**
```
Condition: (treatment_rate / control_rate) < 0.90
Duration: 1 hour
Action: Notify product team
```

---

## Phase 6: A/B Test Timeline

| Week | Action |
|------|--------|
| **Week 1** | Deploy with 50/50 split, monitor API performance |
| **Week 2** | Collect 1,000+ sample, check statistical power |
| **Week 3** | Evaluate lift + conversion impact |
| **Week 4** | Decision: scale treatment or iterate |

### Success Criteria

- **85%+ API uptime** (< 2% error rate)
- **30%+ conversion lift** (treatment vs. control)
- **p < 0.05** (statistically significant)
- **No regression** in quiz completion rate

---

## Troubleshooting

### Issue: API returns 400 "Missing answers array"

**Cause:** Quiz answers not formatted correctly for engine

**Fix:** Check that `QuizEngine.executeRecommendation(answers)` is receiving the raw quiz answer objects (from `QUESTIONS[i].opts[j]`), not modified versions.

```javascript
// ✓ Correct
const answers = [
  { b: "...", s: "...", w: {...}, whr: 0.3, bwr: -0.2 },
  { b: "...", s: "...", w: {...}, whr: 0.1, bwr: 0.0 },
  // ...
];
await QuizEngine.executeRecommendation(answers);

// ✗ Wrong
const formattedAnswers = answers.map(a => ({ weights: a.w })); // loses whr/bwr
await QuizEngine.executeRecommendation(formattedAnswers);
```

### Issue: A/B variant always "control"

**Cause:** Session storage not persisting, or cleared between page loads

**Fix:** Verify browser allows sessionStorage:
```javascript
QuizEngine.debug()
// variant should be different on refresh if using private browsing — that's normal
// But should be same within a session
```

### Issue: Conversion rate unchanged (treatment not winning)

**Cause:** Sample size too small, or confidence boost too weak

**Action:**
1. Let test run for ≥2 weeks to collect 500+ samples/variant
2. Increase boost in `selectRecommendationVariant()` (multiply by higher factor)
3. Verify contact form is receiving `ab_variant` field

---

## Rollback Plan

If treatment causes issues:

### Quick Rollback (30 minutes)

1. In Vercel/Netlify dashboard, set environment variable:
   ```
   AB_TEST_ENABLED = false
   ```

2. Update `quiz-engine.js` to force control:
   ```javascript
   function initializeABVariant() {
     return 'control'; // Force all users to control
   }
   ```

3. Deploy
4. Monitor for 5 minutes

### Full Rollback

Revert `finish()` in quiz.html to previous client-side-only version, deploy to main branch.

---

## Next Steps

1. **Week 1:** Deploy edge function, enable 50/50 split
2. **Week 2:** Confirm statistical power with 1,000+ samples
3. **Week 3:** Evaluate results, decide on scaling
4. **Week 4+:** Optimize based on learnings, test new variants

---

**Contacts**
- **API Issues:** Check `/api/recommend` response in DevTools Network tab
- **Analytics:** Run `npm run analyze:ab` for weekly summaries
- **Deployment:** See `vercel.json` or `netlify.toml` for environment setup

**Last Updated:** 2026-06-21
