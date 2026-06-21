/**
 * ZELEX Analytics Tracking — Edge Function
 *
 * Collects quiz recommendation events and form submission conversions
 * Aggregates for A/B testing analysis
 *
 * Events tracked:
 * - quiz_recommendation_shown (quiz completion)
 * - contact_form_submitted (conversion)
 * - compare_set_from_quiz (secondary action)
 */

import crypto from 'crypto';

// In-memory event buffer (replace with database for production)
let eventBuffer = [];
const BATCH_SIZE = 100;
const FLUSH_INTERVAL = 60000; // 1 minute

/**
 * Normalize and validate event payload
 */
function normalizeEvent(payload) {
  return {
    id: crypto.randomUUID?.() || `evt_${Date.now()}_${Math.random().toString(36).slice(2)}`,
    timestamp: new Date().toISOString(),
    session_id: String(payload.session_id || '').slice(0, 128),
    event: String(payload.event || 'unknown').slice(0, 64),
    variant: String(payload.variant || 'control').slice(0, 32),
    winner: String(payload.winner || '').slice(0, 64),
    source_family: String(payload.source_family || payload.sourceFam || '').slice(0, 64),
    in_development: Boolean(payload.in_development),
    match_count: parseInt(payload.match_count || 0),
    measurement_whr: payload.measurement_whr != null ? parseFloat(payload.measurement_whr) : null,
    measurement_bwr: payload.measurement_bwr != null ? parseFloat(payload.measurement_bwr) : null,
    top_scores: String(payload.top_scores || '').slice(0, 256),
    user_agent: String(payload.user_agent || '').slice(0, 512),
    referrer: String(payload.referrer || '').slice(0, 256),
    ip_country: String(payload.ip_country || '').slice(0, 2)
  };
}

/**
 * Buffer event and schedule flush
 */
function bufferEvent(event) {
  eventBuffer.push(event);

  if (eventBuffer.length >= BATCH_SIZE) {
    flushBuffer();
  }
}

/**
 * Send buffered events to analytics backend
 * In production, connect to Mixpanel, Amplitude, BigQuery, etc.
 */
async function flushBuffer() {
  if (eventBuffer.length === 0) return;

  const toFlush = eventBuffer.splice(0, BATCH_SIZE);

  // Log to console in development
  if (process.env.NODE_ENV === 'development') {
    console.log(`[Analytics Flush] ${toFlush.length} events`);
    toFlush.forEach(e => {
      if (e.event === 'quiz_recommendation_shown') {
        console.log(`  → Quiz: ${e.winner} (${e.variant}) - ${e.variant === 'treatment' ? '🔬' : '📊'}`);
      }
    });
  }

  // Send to external analytics (implement based on your backend)
  try {
    const endpoint = process.env.ANALYTICS_BACKEND_URL;
    if (endpoint) {
      await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ events: toFlush })
      });
    }
  } catch (error) {
    console.error('Analytics flush failed:', error);
    // Re-buffer events on failure
    eventBuffer.unshift(...toFlush);
  }
}

/**
 * Schedule periodic flush
 */
setInterval(() => {
  if (eventBuffer.length > 0) {
    flushBuffer();
  }
}, FLUSH_INTERVAL);

/**
 * Edge function handler
 */
export default async function handler(request) {
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': process.env.ALLOWED_ORIGINS || '*'
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

    // Normalize and validate event
    const event = normalizeEvent(body);

    // Add request context
    event.user_agent = request.headers.get('user-agent') || '';
    event.referrer = request.headers.get('referer') || '';
    event.ip_country = request.headers.get('cloudflare-country-code') || '';

    // Buffer event
    bufferEvent(event);

    return new Response(
      JSON.stringify({
        success: true,
        event_id: event.id,
        timestamp: event.timestamp
      }),
      { status: 202, headers }
    );

  } catch (error) {
    console.error('Tracking error:', error);
    return new Response(
      JSON.stringify({
        error: 'Tracking failed',
        message: error.message
      }),
      { status: 400, headers }
    );
  }
}

/**
 * Analytics Query API — retrieve A/B test results
 * POST /api/analytics?action=query
 */
export async function queryResults(options = {}) {
  const { variant, eventType = 'quiz_recommendation_shown', timeRange = '24h' } = options;

  // Filter buffered events
  const events = eventBuffer.filter(e => {
    if (eventType && e.event !== eventType) return false;
    if (variant && e.variant !== variant) return false;
    return true;
  });

  const totalCount = events.length;
  const byVariant = {
    control: events.filter(e => e.variant === 'control').length,
    treatment: events.filter(e => e.variant === 'treatment').length
  };

  const conversionRates = {
    control: calculateConversionRate(events, 'control'),
    treatment: calculateConversionRate(events, 'treatment')
  };

  return {
    summary: {
      total: totalCount,
      by_variant: byVariant,
      conversion_rates: conversionRates
    },
    events: events.slice(0, 100) // Sample
  };
}

/**
 * Calculate conversion rate for a variant
 * Placeholder — implement based on your funnel definition
 */
function calculateConversionRate(events, variant) {
  const variantEvents = events.filter(e => e.variant === variant);
  if (variantEvents.length === 0) return 0;

  // Simple: count form submissions / quiz completions
  const submissions = variantEvents.filter(e => e.event === 'contact_form_submitted').length;
  const completions = variantEvents.filter(e => e.event === 'quiz_recommendation_shown').length;

  return completions > 0 ? (submissions / completions) * 100 : 0;
}

/**
 * Export for testing/monitoring
 */
export { normalizeEvent, bufferEvent, queryResults };
