/* ============================================================
   GA4 Initialization & GTM Integration — ZELEX Character Atlas

   Loads GTM container and initializes GA4 event tracking.
   Insert this BEFORE any analytics-dependent code.

   GTM Container: REPLACE_WITH_CONTAINER_ID
   GA4 Measurement ID: REPLACE_WITH_GA4_MEASUREMENT_ID
   ============================================================ */

(function() {
  // GTM Container ID — replace with your actual container ID
  const GTM_CONTAINER_ID = 'REPLACE_WITH_CONTAINER_ID';
  const GA4_MEASUREMENT_ID = 'REPLACE_WITH_GA4_MEASUREMENT_ID';

  // Initialize dataLayer if not present
  window.dataLayer = window.dataLayer || [];

  // Push config event to GTM
  window.dataLayer.push({
    event: 'gtm.init',
    source: 'howiezz-web',
    schema_version: '2026-06-06',
    session_id: (function() {
      try {
        let sid = sessionStorage.getItem('zx_analytics_session_id');
        if (!sid) {
          const t = Date.now().toString(36);
          const r = Math.random().toString(36).slice(2, 10);
          sid = 'zx_' + t + '_' + r;
          sessionStorage.setItem('zx_analytics_session_id', sid);
        }
        return sid;
      } catch (e) {
        return 'zx_offline_' + Date.now();
      }
    })()
  });

  // Inject GTM script (if container ID is set)
  if (GTM_CONTAINER_ID && GTM_CONTAINER_ID !== 'REPLACE_WITH_CONTAINER_ID') {
    const scriptId = 'gtm-' + GTM_CONTAINER_ID;

    // Check if GTM already loaded
    if (!document.getElementById(scriptId)) {
      const gtmScript = document.createElement('script');
      gtmScript.id = scriptId;
      gtmScript.async = true;
      gtmScript.src = 'https://www.googletagmanager.com/gtm.js?id=' + GTM_CONTAINER_ID;
      document.head.appendChild(gtmScript);
    }
  }

  // Inject GTM noscript (for tracking without JS)
  if (GTM_CONTAINER_ID && GTM_CONTAINER_ID !== 'REPLACE_WITH_CONTAINER_ID') {
    const noscriptId = 'gtm-noscript-' + GTM_CONTAINER_ID;
    if (!document.getElementById(noscriptId)) {
      const noscript = document.createElement('noscript');
      noscript.id = noscriptId;
      noscript.innerHTML = '<iframe src="https://www.googletagmanager.com/ns.html?id=' + GTM_CONTAINER_ID + '" height="0" width="0" style="display:none;visibility:hidden"></iframe>';
      document.body.insertAdjacentElement('afterbegin', noscript);
    }
  }

  // GA4 native gtag setup (if using both GTM + GA4)
  if (GA4_MEASUREMENT_ID && GA4_MEASUREMENT_ID !== 'REPLACE_WITH_GA4_MEASUREMENT_ID') {
    // Note: If using GTM container, GA4 is configured within GTM.
    // This is a fallback / direct GA4 integration point.
    window.dataLayer.push({
      'gtag.config': {
        'config': {
          [GA4_MEASUREMENT_ID]: {
            'allow_google_signals': false,
            'allow_ad_personalization_signals': false
          }
        }
      }
    });
  }

  // Expose a utility to check GTM/GA4 status
  window.ZX = window.ZX || {};
  window.ZX.analyticsStatus = {
    gtmLoaded: !!(GTM_CONTAINER_ID && GTM_CONTAINER_ID !== 'REPLACE_WITH_CONTAINER_ID'),
    ga4Loaded: !!(GA4_MEASUREMENT_ID && GA4_MEASUREMENT_ID !== 'REPLACE_WITH_GA4_MEASUREMENT_ID'),
    gtmId: GTM_CONTAINER_ID,
    ga4Id: GA4_MEASUREMENT_ID,
    dataLayerReady: Array.isArray(window.dataLayer)
  };
})();
