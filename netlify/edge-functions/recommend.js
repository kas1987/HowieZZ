/**
 * ZELEX Quiz Recommendation Engine — Netlify Edge Function
 * Deployed as /recommend edge function (runs on Deno)
 *
 * Context: https://docs.netlify.com/edge-functions/overview/
 */

import { recommend } from '../../api/recommend.js';

/**
 * Netlify Edge Function Handler
 * Automatically deployed to edge locations globally
 */
export default async (request, context) => {
  // Preflight CORS
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      status: 204,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, X-Session-ID, X-AB-Variant'
      }
    });
  }

  if (request.method !== 'POST') {
    return new Response(
      JSON.stringify({ error: 'Method not allowed' }),
      { status: 405, headers: { 'Content-Type': 'application/json' } }
    );
  }

  try {
    const body = await request.json();
    const { answers, session_id, ab_variant } = body;

    if (!answers) {
      return new Response(
        JSON.stringify({ error: 'Missing answers array' }),
        { status: 400, headers: { 'Content-Type': 'application/json' } }
      );
    }

    // Load catalog from deployed static assets
    const catalogUrl = Deno.env.get('CATALOG_URL') || '/db/catalog.json';
    const charUrl = Deno.env.get('CHARACTERS_URL') || '/db/characters.json';
    const profilesUrl = Deno.env.get('BODY_PROFILES_URL') || '/db/body_profiles.json';

    const [catalogRes, charRes, profileRes] = await Promise.all([
      fetch(new URL(catalogUrl, request.url)),
      fetch(new URL(charUrl, request.url)),
      fetch(new URL(profilesUrl, request.url))
    ]);

    if (!catalogRes.ok || !charRes.ok || !profileRes.ok) {
      throw new Error('Failed to load catalog');
    }

    const characters = await charRes.json();
    const profiles = await profileRes.json();

    const catalog = {
      families: profiles.families || [],
      characters: characters.characters || []
    };

    const result = await recommend(answers, catalog, {
      abVariant: ab_variant,
      sessionId: session_id
    });

    return new Response(JSON.stringify(result), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'private, no-cache'
      }
    });

  } catch (error) {
    console.error('Recommendation error:', error);
    return new Response(
      JSON.stringify({
        error: error.message || 'Recommendation failed',
        timestamp: new Date().toISOString()
      }),
      {
        status: 500,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
};

export const config = {
  path: '/recommend'
};
