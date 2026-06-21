/**
 * ZELEX Quiz Recommendation Engine — Frontend Integration
 *
 * Handles quiz completion flow:
 * 1. Collect answers
 * 2. Call edge function for recommendations
 * 3. Display results with measurement reasoning
 * 4. Track conversion via analytics
 *
 * A/B Testing:
 * - Control: Traditional scoring
 * - Treatment: Confidence-boosted measurement alignment
 */

const QuizEngine = (function () {
  // Configuration
  const API_ENDPOINT = '/api/recommend';
  const A_B_STORAGE_KEY = 'zx_ab_variant';
  const RESULTS_STORAGE_KEY = 'zx_quiz_result';
  const SESSION_STORAGE_KEY = 'zx_analytics_session_id';

  /**
   * Initialize A/B variant for this session
   * 50/50 control/treatment split
   */
  function initializeABVariant() {
    let variant = null;
    try {
      variant = sessionStorage.getItem(A_B_STORAGE_KEY);
    } catch (e) {}

    if (!variant) {
      // 50/50 split with pseudo-random assignment
      variant = Math.random() < 0.5 ? 'control' : 'treatment';
      try {
        sessionStorage.setItem(A_B_STORAGE_KEY, variant);
      } catch (e) {}
    }

    return variant;
  }

  /**
   * Get or create session ID for analytics tracking
   */
  function getSessionId() {
    let sessionId = null;
    try {
      sessionId = sessionStorage.getItem(SESSION_STORAGE_KEY);
    } catch (e) {}

    if (!sessionId) {
      const t = Date.now().toString(36);
      const r = Math.random().toString(36).slice(2, 10);
      sessionId = 'quiz_' + t + '_' + r;
      try {
        sessionStorage.setItem(SESSION_STORAGE_KEY, sessionId);
      } catch (e) {}
    }

    return sessionId;
  }

  /**
   * Transform quiz answer into recommendation engine format
   * Maps visual answers to weights and measurement leanings
   */
  function formatAnswersForEngine(quizAnswers) {
    // quizAnswers is an array of objects from quiz.html QUESTIONS
    // Each has: { b, s, w, whr, bwr }
    // Transform into engine-compatible format

    return quizAnswers.map(answer => ({
      weights: answer.w || {},
      whr: answer.whr !== undefined ? answer.whr : null,
      bwr: answer.bwr !== undefined ? answer.bwr : null,
      label: answer.b
    }));
  }

  /**
   * Call recommendation edge function with retry logic
   */
  async function callRecommendationEngine(answers, abVariant, sessionId) {
    const payload = {
      answers: formatAnswersForEngine(answers),
      session_id: sessionId,
      ab_variant: abVariant
    };

    let attempt = 0;
    const maxAttempts = 3;
    let lastError = null;

    while (attempt < maxAttempts) {
      try {
        const response = await fetch(API_ENDPOINT, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Session-ID': sessionId,
            'X-AB-Variant': abVariant
          },
          body: JSON.stringify(payload),
          signal: AbortSignal.timeout(10000) // 10s timeout
        });

        if (!response.ok) {
          throw new Error(`API error: ${response.status}`);
        }

        const result = await response.json();
        return result;

      } catch (error) {
        lastError = error;
        attempt++;

        // Exponential backoff
        if (attempt < maxAttempts) {
          await new Promise(r => setTimeout(r, Math.pow(2, attempt) * 1000));
        }
      }
    }

    throw new Error(`Recommendation failed after ${maxAttempts} attempts: ${lastError.message}`);
  }

  /**
   * Get confidence level description based on measurement alignment
   */
  function getConfidenceLevel(reasoning, scores, winner) {
    if (!reasoning) return 'standard';

    // High confidence: strong measurement alignment
    const whrScore = Math.abs(reasoning.measurement?.whrLean || 0);
    const bwrScore = Math.abs(reasoning.measurement?.bwrLean || 0);

    if (whrScore > 0.3 && bwrScore > 0.3) return 'high';
    if (whrScore > 0.1 && bwrScore > 0.1) return 'standard';
    return 'exploratory';
  }

  /**
   * Track recommendation conversion event
   */
  async function trackRecommendationEvent(result, sessionId) {
    const payload = {
      event: 'quiz_recommendation_shown',
      session_id: sessionId,
      winner: result.winner,
      source_family: result.sourceFam,
      in_development: result.inDevelopment,
      variant: result.variant,
      match_count: result.matches?.length || 0,
      top_scores: result.topFamilies?.map(f => `${f.family}:${f.pct}%`).join('|'),
      measurement_whr: result.measurement?.whrLean,
      measurement_bwr: result.measurement?.bwrLean,
      timestamp: result.timestamp
    };

    // Fire analytics event (async, non-blocking)
    if (window.ZX?.track) {
      window.ZX.track('quiz_complete', payload);
    }

    // Send to edge analytics (optional)
    fetch('/api/track', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }).catch(() => {});
  }

  /**
   * Build result display components
   */
  function buildResultDisplay(result) {
    const { winner, sourceFam, inDevelopment, measurement, matches, topFamilies } = result;

    const confidenceLevel = getConfidenceLevel(measurement, null, winner);
    const confidenceBadge = {
      high: { label: 'High Confidence', color: 'var(--gold)' },
      standard: { label: 'Strong Match', color: 'var(--cream)' },
      exploratory: { label: 'Exploratory', color: 'var(--muted)' }
    }[confidenceLevel] || { label: 'Match', color: 'var(--muted)' };

    return {
      winner,
      sourceFam,
      inDevelopment,
      confidenceLevel,
      confidenceBadge,
      measurement,
      matches,
      topFamilies
    };
  }

  /**
   * Store result in local storage for page navigation
   */
  function storeResult(result) {
    try {
      localStorage.setItem(RESULTS_STORAGE_KEY, JSON.stringify({
        ...result,
        stored_at: new Date().toISOString()
      }));
    } catch (e) {
      console.warn('Failed to store quiz result:', e);
    }
  }

  /**
   * Public API
   */
  return {
    /**
     * Execute full recommendation workflow
     * Called by quiz.html finish() function
     */
    async executeRecommendation(quizAnswers) {
      const abVariant = initializeABVariant();
      const sessionId = getSessionId();

      try {
        // Call edge function
        const result = await callRecommendationEngine(quizAnswers, abVariant, sessionId);

        // Track conversion
        await trackRecommendationEvent(result, sessionId);

        // Store for later access
        storeResult(result);

        // Build display payload
        const display = buildResultDisplay(result);

        return {
          success: true,
          result,
          display,
          variant: abVariant,
          sessionId
        };

      } catch (error) {
        console.error('Quiz recommendation error:', error);

        // Fallback to client-side algorithm if API fails
        return {
          success: false,
          error: error.message,
          fallback: true,
          variant: abVariant,
          sessionId
        };
      }
    },

    /**
     * Get current session's A/B variant
     */
    getVariant() {
      return initializeABVariant();
    },

    /**
     * Get stored result from a previous quiz session
     */
    getStoredResult() {
      try {
        return JSON.parse(localStorage.getItem(RESULTS_STORAGE_KEY));
      } catch (e) {
        return null;
      }
    },

    /**
     * Clear stored result
     */
    clearResult() {
      try {
        localStorage.removeItem(RESULTS_STORAGE_KEY);
      } catch (e) {}
    },

    /**
     * Debug: log current variant assignment
     */
    debug() {
      return {
        variant: initializeABVariant(),
        sessionId: getSessionId(),
        storedResult: this.getStoredResult()
      };
    }
  };
})();

// Export for use in quiz.html
if (typeof window !== 'undefined') {
  window.QuizEngine = QuizEngine;
}
