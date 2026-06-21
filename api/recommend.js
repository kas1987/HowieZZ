/**
 * ZELEX Quiz Recommendation Engine — Edge Function
 *
 * Handles quiz completion → family scoring → character recommendations
 * Deterministic algorithm with WHR/BWR measurement validation
 * Production-ready for Vercel/Netlify edge runtime
 *
 * Usage:
 * POST /api/recommend
 * Body: { answers: [...], session_id?: string, ab_variant?: 'control'|'treatment' }
 * Response: { winner, source_family, matches: [...], reasoning, confidence }
 */

// Import character data — in production, this comes from a database or CDN
// For now, assume it's injected at build time or fetched at runtime
let CATALOG_CACHE = null;

/**
 * Core scoring algorithm
 * Maps quiz answers → family weights → normalized scores
 */
function scoreAnswers(answers, families) {
  const scores = {};
  families.forEach(f => { scores[f] = 0; });

  // Accumulate family weights from answers
  let whrLean = 0, bwrLean = 0, leanN = 0;

  answers.forEach(answer => {
    if (answer.weights) {
      Object.entries(answer.weights).forEach(([family, weight]) => {
        scores[family] = (scores[family] || 0) + weight;
      });
    }
    if (typeof answer.whr === 'number') { whrLean += answer.whr; leanN++; }
    if (typeof answer.bwr === 'number') { bwrLean += answer.bwr; }
  });

  const avgWhr = leanN ? whrLean / leanN : 0;
  const avgBwr = leanN ? bwrLean / leanN : 0;

  return { scores, avgWhr, avgBwr, leanN };
}

/**
 * Rank families by score and find the best-available match
 * Handles in-development families by fallback to nearest active family
 */
function rankFamiliesAndResolve(scores, families, catalog, expressed) {
  const ranked = families.slice().sort((a, b) => scores[b] - scores[a]);

  const liveByFam = (fam) => {
    return (catalog.characters || []).filter(c =>
      c.status === 'live' && c.body && c.body.family === fam
    );
  };

  const isInDev = (fam) => liveByFam(fam).length === 0;

  // Find the first live family in the ranking
  const sourceFam = ranked.find(f => liveByFam(f).length > 0) || ranked[0];

  // If expressed winner is in-dev, find nearest active family
  let fallbackFam = sourceFam;
  if (isInDev(expressed)) {
    const center = (fam) => {
      const famMeta = catalog.families.find(f => f.name === fam);
      return famMeta ? [(famMeta.whr[0] + famMeta.whr[1]) / 2, (famMeta.bwr[0] + famMeta.bwr[1]) / 2] : null;
    };

    const c0 = center(expressed);
    let bestDist = Infinity, bestFam = sourceFam;

    families.forEach(f => {
      if (isInDev(f)) return;
      const c1 = center(f);
      if (!c0 || !c1) return;
      const d = Math.abs(c0[0] - c1[0]) / 0.05 + Math.abs(c0[1] - c1[1]) / 0.10;
      if (d < bestDist) { bestDist = d; bestFam = f; }
    });

    fallbackFam = bestFam;
  }

  return {
    ranked,
    sourceFam: fallbackFam,
    expressed,
    liveByFam,
    isInDev: (f) => isInDev(f)
  };
}

/**
 * Select diverse matches from source family + runner-up families
 * Up to 4 characters, prioritized by body diversity
 */
function selectMatches(ranking, catalog, maxMatches = 4) {
  const pool = ranking.liveByFam(ranking.sourceFam);
  const matches = [];
  const seenBody = new Set();

  // First pass: diversify by body_code within source family
  for (const c of pool) {
    if (!seenBody.has(c.body_code)) {
      matches.push(c);
      seenBody.add(c.body_code);
    }
    if (matches.length === maxMatches) break;
  }

  // Second pass: fill remaining from source family
  for (const c of pool) {
    if (matches.length >= maxMatches) break;
    if (!matches.includes(c)) matches.push(c);
  }

  // Third pass: pull from runner-up families if we need more
  if (matches.length < maxMatches) {
    const runner = ranking.ranked.find(f =>
      f !== ranking.sourceFam && ranking.liveByFam(f).length > 0
    );
    if (runner) {
      const runnerPool = ranking.liveByFam(runner);
      for (const c of runnerPool) {
        if (matches.length >= maxMatches) break;
        if (!matches.includes(c)) matches.push(c);
      }
    }
  }

  // Final fallback: any live character
  if (matches.length < maxMatches) {
    for (const c of catalog.characters) {
      if (c.status !== 'live') continue;
      if (matches.length >= maxMatches) break;
      if (!matches.includes(c)) matches.push(c);
    }
  }

  return matches.slice(0, maxMatches);
}

/**
 * Build measurement-grounded reasoning text
 * Cites WHR/BWR ranges + user's directional leaning
 */
function buildReasoning(winner, familyMeta, avgWhr, avgBwr) {
  const fm = familyMeta.find(f => f.name === winner);

  const whrDir = avgWhr < -0.15
    ? 'a lower waist-to-hip ratio (more pronounced hourglass)'
    : avgWhr > 0.15
    ? 'a higher, more balanced waist-to-hip ratio'
    : 'a balanced waist-to-hip ratio';

  const bwrDir = avgBwr > 0.2
    ? 'a bust-forward bust-to-waist ratio'
    : avgBwr < -0.2
    ? 'a restrained, proportion-led bust-to-waist ratio'
    : 'a moderate bust-to-waist ratio';

  const ranges = fm
    ? `WHR ${fm.whr[0].toFixed(2)}–${fm.whr[1].toFixed(2)} and BWR ${fm.bwr[0].toFixed(2)}–${fm.bwr[1].toFixed(2)}`
    : 'published ranges';

  return {
    whrDir,
    bwrDir,
    ranges,
    confidence: 'near', // Quiz captures directional leaning, not exact body
    fm
  };
}

/**
 * A/B Test: Control vs. Treatment recommendation strategy
 *
 * Control: Traditional scoring (quiz answers only)
 * Treatment: Confidence-boosted scoring (emphasizes measurement alignment)
 */
function selectRecommendationVariant(abVariant, scores, ranking, avgWhr, avgBwr) {
  if (abVariant === 'treatment') {
    // Boost score for winner if measurement lean aligns with its ranges
    const winner = ranking.expressed;
    const fm = ranking.familyMeta?.find(f => f.name === winner);

    if (fm) {
      const whrCenter = (fm.whr[0] + fm.whr[1]) / 2;
      const bwrCenter = (fm.bwr[0] + fm.bwr[1]) / 2;
      const whrAlign = 1 - Math.abs(avgWhr - whrCenter) / 0.2;
      const bwrAlign = 1 - Math.abs(avgBwr - bwrCenter) / 0.2;

      const alignmentBoost = Math.max(0, (whrAlign + bwrAlign) / 2 * 3);
      scores[winner] = (scores[winner] || 0) + alignmentBoost;
    }
  }

  return scores;
}

/**
 * Main recommendation handler
 * Returns structured recommendation payload for frontend consumption
 */
async function recommend(answers, catalog, options = {}) {
  if (!catalog || !catalog.families || !catalog.characters) {
    throw new Error('Catalog data required');
  }

  if (!answers || !Array.isArray(answers)) {
    throw new Error('Answers array required');
  }

  const families = catalog.families.map(f => f.name);
  const { scores, avgWhr, avgBwr } = scoreAnswers(answers, families);

  const totalScore = Math.max(1, Object.values(scores).reduce((a, v) => a + (v > 0 ? v : 0), 0));
  const normalized = {};
  families.forEach(f => {
    normalized[f] = totalScore > 0 ? Math.round((scores[f] / totalScore) * 100) : 0;
  });

  // Determine expressed winner (highest score regardless of availability)
  const expressed = Object.keys(normalized).sort((a, b) => normalized[b] - normalized[a])[0];

  // Apply A/B variant if specified
  if (options.abVariant && options.abVariant !== 'control') {
    const ranking = rankFamiliesAndResolve(scores, families, catalog, expressed);
    ranking.familyMeta = catalog.families;
    selectRecommendationVariant(options.abVariant, scores, ranking, avgWhr, avgBwr);
  }

  // Resolve to available family
  const ranking = rankFamiliesAndResolve(scores, families, catalog, expressed);
  ranking.familyMeta = catalog.families;

  const matches = selectMatches(ranking, catalog, 4);
  const reasoning = buildReasoning(expressed, catalog.families, avgWhr, avgBwr);

  const top3 = ranking.ranked.slice(0, 3).map((fam, idx) => ({
    rank: idx + 1,
    family: fam,
    pct: normalized[fam],
    isLive: ranking.liveByFam(fam).length > 0,
    liveCount: ranking.liveByFam(fam).length
  }));

  return {
    // Recommendation result
    winner: expressed,
    sourceFam: ranking.sourceFam,
    inDevelopment: ranking.isInDev(expressed),

    // Measurement reasoning
    measurement: {
      whrLean: Math.round(avgWhr * 100) / 100,
      bwrLean: Math.round(avgBwr * 100) / 100,
      reasoning
    },

    // Character matches
    matches: matches.map(c => ({
      characterId: c.character_id,
      bodyCode: c.body_code,
      series: c.series,
      name: c.persona?.name || '',
      family: c.body?.family || '',
      whr: c.body?.WHR,
      bwr: c.body?.BWR,
      height: c.body?.height_cm,
      cup: c.body?.cup,
      image: (c.photoshoot?.hero_thumb || c.photoshoot?.hero) || null
    })),

    // Scoring transparency
    topFamilies: top3,
    variant: options.abVariant || 'control',
    timestamp: new Date().toISOString()
  };
}

/**
 * Vercel/Netlify Edge Function Handler
 */
export default async function handler(request) {
  // CORS headers
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': process.env.ALLOWED_ORIGINS || '*',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, X-Session-ID, X-AB-Variant'
  };

  // Preflight
  if (request.method === 'OPTIONS') {
    return new Response(null, { status: 204, headers });
  }

  if (request.method !== 'POST') {
    return new Response(
      JSON.stringify({ error: 'Method not allowed' }),
      { status: 405, headers }
    );
  }

  try {
    const body = await request.json();
    const { answers, session_id, ab_variant } = body;

    if (!answers) {
      return new Response(
        JSON.stringify({ error: 'Missing answers array' }),
        { status: 400, headers }
      );
    }

    // Load or cache catalog
    if (!CATALOG_CACHE) {
      const catalogUrl = process.env.CATALOG_URL || '/db/catalog.json';
      const charUrl = process.env.CHARACTERS_URL || '/db/characters.json';
      const profilesUrl = process.env.BODY_PROFILES_URL || '/db/body_profiles.json';

      const [catalogRes, charRes, profileRes] = await Promise.all([
        fetch(catalogUrl),
        fetch(charUrl),
        fetch(profilesUrl)
      ]);

      if (!catalogRes.ok || !charRes.ok || !profileRes.ok) {
        throw new Error('Failed to load catalog data');
      }

      const characters = await charRes.json();
      const profiles = await profileRes.json();

      CATALOG_CACHE = {
        families: profiles.families || [],
        characters: characters.characters || []
      };
    }

    const result = await recommend(answers, CATALOG_CACHE, {
      abVariant: ab_variant,
      sessionId: session_id
    });

    // Track conversion event (async, non-blocking)
    if (session_id) {
      fetch(process.env.ANALYTICS_URL || '/api/track', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          event: 'quiz_recommendation',
          session_id,
          winner: result.winner,
          variant: result.variant,
          timestamp: result.timestamp
        })
      }).catch(() => {}); // Silently fail analytics
    }

    return new Response(JSON.stringify(result), {
      status: 200,
      headers
    });

  } catch (error) {
    console.error('Recommendation error:', error);
    return new Response(
      JSON.stringify({
        error: error.message || 'Recommendation failed',
        timestamp: new Date().toISOString()
      }),
      { status: 500, headers }
    );
  }
}

// Export for server-side use (Node.js)
export { recommend, scoreAnswers, rankFamiliesAndResolve, buildReasoning };
