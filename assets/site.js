/* ============================================================
   ZELEX site — shared runtime (global: ZX)
   Every page calls ZX.load() then uses the returned model + helpers.
   ============================================================ */
window.ZX = (function () {
  const SERIES_ORDER = ["K-Series", "Inspiration", "Fusion", "SLE"];
  const SERIES_SUB = {
    "K-Series": "The Korean-creative flagship. Curated heads, named personas, premium craft.",
    "Inspiration": "Western naturalism — believable, hip-led 'Muse' architectures.",
    "Fusion": "Movable-jaw realism hybrids; quiet-luxury proportions.",
    "SLE": "The SLE 3.0 range — the widest spectrum, athletic minimalism to maximal fantasy."
  };
  const FAMILIES = ["The Classic","The Icon","The Muse","The Siren","The Empress","The Sculpt"];
  const COMPARE_STORAGE_KEY = 'zx_compare_bodies';

  let _model = null;

  // One place to change where buyer inquiries go.
  const INQUIRY_EMAIL = 'inquiries@zelexdoll.com';
  // Optional form-backend endpoint (e.g. a Formspree/Getform URL). When empty, the
  // contact form falls back to composing a prefilled email via INQUIRY_EMAIL.
  const FORM_ENDPOINT = '';

  // Mark JS active so the reveal-hiding CSS only applies when JS can un-hide it
  // (no-JS / load-failure → content stays visible).
  try { document.documentElement.classList.add('js'); } catch (e) {}

  function famColor(f){ return f ? `var(--${String(f).replace('The ','')})` : 'var(--muted)'; }
  function famClass(f){
    if (!f) return 'fam--unclassified';
    const key = String(f).replace('The ', '').toLowerCase();
    if (key === 'classic') return 'fam--classic';
    if (key === 'icon') return 'fam--icon';
    if (key === 'muse') return 'fam--muse';
    if (key === 'siren') return 'fam--siren';
    if (key === 'empress') return 'fam--empress';
    if (key === 'sculpt') return 'fam--sculpt';
    return 'fam--unclassified';
  }
  function qs(name){ return new URLSearchParams(location.search).get(name); }
  function esc(s){ return String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }
  function img(c){ return (c.photoshoot && (c.photoshoot.hero_thumb || c.photoshoot.hero)) || ''; }

  const ANALYTICS_SCHEMA_VERSION = '2026-06-06';
  const ANALYTICS_SESSION_KEY = 'zx_analytics_session_id';
  const ANALYTICS_DEBUG_KEY = 'zx_analytics_debug';
  const EVENT_ALIASES = {
    compare_add_from_body: 'compare_add',
    compare_add_from_character: 'compare_add',
    compare_add_from_compare_page: 'compare_add',
    compare_to_contact_click: 'compare_handoff_click',
    compare_to_quiz_click: 'compare_handoff_click',
    compare_view_empty: 'compare_view'
  };

  function createSessionId() {
    const t = Date.now().toString(36);
    const r = Math.random().toString(36).slice(2, 10);
    return 'zx_' + t + '_' + r;
  }

  function getSessionId() {
    try {
      let sid = '';
      try { sid = sessionStorage.getItem(ANALYTICS_SESSION_KEY) || ''; } catch (e) {}
      if (!sid) {
        try { sid = localStorage.getItem(ANALYTICS_SESSION_KEY) || ''; } catch (e) {}
      }
      if (!sid) sid = createSessionId();
      try { sessionStorage.setItem(ANALYTICS_SESSION_KEY, sid); } catch (e) {}
      try { localStorage.setItem(ANALYTICS_SESSION_KEY, sid); } catch (e) {}
      return sid;
    } catch (e) {
      return createSessionId();
    }
  }

  function parseCodeList(raw) {
    if (!raw) return [];
    if (Array.isArray(raw)) {
      return raw.map(x => String(x || '').trim()).filter(x => x && /^[A-Za-z0-9_-]+$/.test(x));
    }
    return String(raw)
      .split(',')
      .map(x => (x || '').trim())
      .filter(x => x && /^[A-Za-z0-9_-]+$/.test(x));
  }

  function analyticsDebugEnabled() {
    try {
      const flag = String(qs('zx_analytics_debug') || '').toLowerCase();
      if (flag === '1' || flag === 'true' || flag === 'on') {
        try { localStorage.setItem(ANALYTICS_DEBUG_KEY, '1'); } catch (e) {}
        return true;
      }
      if (flag === '0' || flag === 'false' || flag === 'off') {
        try { localStorage.removeItem(ANALYTICS_DEBUG_KEY); } catch (e) {}
        return false;
      }
      return localStorage.getItem(ANALYTICS_DEBUG_KEY) === '1';
    } catch (e) {
      return false;
    }
  }

  function getCompareBodies() {
    try {
      const parsed = JSON.parse(localStorage.getItem(COMPARE_STORAGE_KEY) || '[]');
      if (!Array.isArray(parsed)) return [];
      return parsed.filter(Boolean).filter(x => x !== '.').slice(0, 4);
    } catch (e) {
      return [];
    }
  }

  function setCompareBodies(codes) {
    const clean = (Array.isArray(codes) ? codes : []).filter(Boolean).filter(x => x !== '.').slice(0, 4);
    try { localStorage.setItem(COMPARE_STORAGE_KEY, JSON.stringify(clean)); } catch (e) {}
    return clean;
  }

  function addCompareBody(bodyCode) {
    const code = String(bodyCode || '').trim();
    if (!code || code === '.') return { added: false, bodies: getCompareBodies() };
    const cur = getCompareBodies();
    if (cur.includes(code)) return { added: false, bodies: cur };
    const next = setCompareBodies(cur.concat(code));
    return { added: true, bodies: next };
  }

  function normalizeTrackPayload(eventName, payload) {
    const canonicalEvent = EVENT_ALIASES[eventName] || eventName;
    const clean = Object.assign({}, payload || {});
    const codes = parseCodeList(clean.body_codes || clean.compare_codes);

    if (codes.length) {
      clean.body_codes = codes.join(',');
      if (!(typeof clean.compare_count === 'number')) clean.compare_count = codes.length;
    }

    if (typeof clean.message === 'string') {
      clean.error_message = clean.message.trim().slice(0, 180);
      delete clean.message;
    }

    ['body_code','family','series','channel','context','cta','intent','timeline','source_page','view_state'].forEach(function(k) {
      if (clean[k] != null) clean[k] = String(clean[k]).trim();
    });

    return Object.assign({
      event: canonicalEvent,
      event_original: eventName,
      source: 'howiezz-web',
      schema_version: ANALYTICS_SCHEMA_VERSION,
      session_id: getSessionId(),
      ts: new Date().toISOString(),
      page: (location.pathname.split('/').pop() || 'index.html').toLowerCase(),
      path: location.pathname
    }, clean);
  }

  // Lightweight analytics hook. Emits to dataLayer when present and dispatches a
  // custom event for any local listeners. Safe no-op when analytics is absent.
  function track(eventName, payload){
    const eventPayload = normalizeTrackPayload(eventName, payload);
    try {
      if (Array.isArray(window.dataLayer)) window.dataLayer.push(eventPayload);
    } catch (e) {}
    try {
      window.dispatchEvent(new CustomEvent('zx:track', { detail: eventPayload }));
    } catch (e) {}
    if (analyticsDebugEnabled()) {
      try { console.debug('[ZX analytics]', eventPayload); } catch (e) {}
    }
  }

  function trackPageViewOnce() {
    if (window.__zxPageViewTracked) return;
    window.__zxPageViewTracked = true;
    const pageName = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
    track('page_view', {
      context: 'navigation',
      source_page: pageName.replace('.html', '')
    });
  }

  try {
    if (document.readyState === 'loading') {
      document.addEventListener('DOMContentLoaded', trackPageViewOnce, { once: true });
    } else {
      trackPageViewOnce();
    }
  } catch (e) {}

  // Link to the on-site contact form, prefilled for this character.
  function contactHref(c){ return `contact.html?id=${encodeURIComponent(c.character_id)}`; }

  // mailto: inquiry link prefilled with this character's identity + spec (fallback).
  function inquireHref(c){
    const b = c.body || {}, p = c.photoshoot || {};
    const subject = `ZELEX inquiry — ${c.persona.name} (${c.body_code})`;
    const lines = [
      `I'd like to inquire about this ZELEX character:`, ``,
      `Character : ${c.persona.name} — ${c.persona.title}`,
      `Series    : ${c.series}`,
      `Body      : ${c.body_code} · ${b.height_cm}cm · ${b.cup}-cup${b.family?' · '+b.family:''}`,
      p.product_code ? `Product   : ${p.product_code}` : ``,
      p.price ? `Listed    : $${p.price}` : ``, ``,
      `My questions:`, ``
    ].filter(x=>x!==undefined);
    return `mailto:${INQUIRY_EMAIL}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(lines.join('\n'))}`;
  }

  async function load(){
    if (_model) return _model;
    let chars, bodyTypes, profiles;
    try {
      [chars, bodyTypes, profiles] = await Promise.all([
        fetch('db/characters.json').then(r=>r.json()),
        fetch('db/body_types.json').then(r=>r.json()),
        fetch('db/body_profiles.json').then(r=>r.json()).catch(()=>({profiles:{}}))
      ]);
    } catch (e) {
      throw new Error('data-load');
    }
    const characters = chars.characters || [];
    const bts = (bodyTypes.body_types || bodyTypes || []);
    const byId = {}; characters.forEach(c => byId[c.character_id] = c);
    const byBody = {}; characters.forEach(c => (byBody[c.body_code] = byBody[c.body_code] || []).push(c));
    Object.values(byBody).forEach(a => a.sort((x,y)=>x.slot-y.slot));
    const btByCode = {}; bts.forEach(b => btByCode[b.body_code] = b);
    const bySeries = {}; characters.forEach(c => (bySeries[c.series] = bySeries[c.series] || []).push(c));

    _model = {
      characters, bodyTypes: bts, profiles: (profiles.profiles||profiles||{}),
      families: (profiles.families||{}),
      byId, byBody, btByCode, bySeries,
      series: SERIES_ORDER.filter(s => bySeries[s]),
      SERIES_SUB, SERIES_ORDER, FAMILIES
    };
    return _model;
  }

  /* ---- representative imagery + motion helpers ---- */
  // i-th live character (with image) from a list — for hero/title backdrops.
  function repImg(chars, idx){
    const a = (chars||[]).filter(c => c.status==='live' && img(c));
    const c = a[idx||0] || a[0];
    return c ? img(c) : '';
  }
  // Hero backdrop layer — drop as the FIRST child of a `.has-backdrop` hero. Slow
  // ken-burns drift + readability scrim are handled in CSS. Empty when no image.
  function heroBackdrop(src){
    return src ? `<div class="backdrop" style="background-image:url('${src}')"></div>` : '';
  }
  // Scroll reveal: fade `.reveal` elements up as they scroll into view. Idempotent —
  // call again after injecting new DOM. Uses a plain scroll-position check (not
  // IntersectionObserver) so its only failure mode is "show everything," never a
  // page of invisible content.
  function _revealSweep(){
    const vh = window.innerHeight || document.documentElement.clientHeight || 0;
    const els = document.querySelectorAll('.reveal:not(.in)');
    for (let i=0;i<els.length;i++){
      const r = els[i].getBoundingClientRect();
      if (r.top < vh * 0.94 && r.bottom > 0) els[i].classList.add('in');
    }
  }
  function revealInit(){
    _revealSweep();                       // reveal whatever is already on screen
    if (!revealInit._bound){
      revealInit._bound = true;
      let ticking = false;
      const onScroll = ()=>{ if(ticking) return; ticking = true;
        requestAnimationFrame(()=>{ ticking = false; _revealSweep(); }); };
      addEventListener('scroll', onScroll, {passive:true});
      addEventListener('resize', onScroll, {passive:true});
      // failsafe: in any environment where scroll, measurement, OR transitions
      // misbehave, never leave content hidden — hard-show anything still pending after
      // a few seconds, bypassing the transition (inline wins, transition:none = instant).
      setTimeout(()=>document.querySelectorAll('.reveal:not(.in)').forEach(e=>{
        e.classList.add('in'); e.style.transition='none'; e.style.opacity='1'; e.style.transform='none';
      }), 4000);
    }
  }

  /* ---- nav + footer injection ---- */
  function mountNav(active){
    const items = [
      ['index.html','Atlas'], ['browse.html','Browse'], ['family.html','Families'],
      ['compare.html','Compare'], ['options.html','Options'],
      ['community.html','Community'], ['quiz.html','Find Yours'], ['contact.html','Contact']
    ];
    const links = items.map(([h,l])=>`<a href="${h}" class="${active===h?'active':''}">${l}</a>`).join('');
    document.body.insertAdjacentHTML('afterbegin',
      `<nav class="nav"><a class="brand" href="index.html">ZEL<span class="x">E</span>X</a><div class="links">${links}</div></nav>`);
    // subtle nav elevation once the page scrolls past the hero lip
    const nav = document.querySelector('.nav');
    if (nav) addEventListener('scroll', ()=>nav.classList.toggle('up', (window.scrollY||0) > 40), {passive:true});
    revealInit(); // catch any static .reveal already in the markup (e.g. heroes)
  }
  function mountFooter(){
    document.body.insertAdjacentHTML('beforeend',
      `<footer><div class="fl"><a href="index.html">Atlas</a><a href="browse.html">Browse</a><a href="family.html">Families</a><a href="compare.html">Compare</a><a href="options.html">Options</a><a href="community.html">Community</a><a href="quiz.html">Find Yours</a><a href="craft.html">The Craft</a><a href="contact.html">Contact</a></div>
       THE CHARACTER ATLAS · generated from the live ZELEX catalog &amp; spec-card measurements · four series · full-body architectures · named characters</footer>`);
    revealInit(); // pages render asynchronously — sweep again once content + footer exist
  }
  function fail(){
    const m = document.getElementById('app') || document.body;
    m.innerHTML = '<div class="err">Could not load the catalog data. Serve this folder with <code>python serve.py</code> and open via <code>http://localhost</code>.</div>';
  }

  /* ---- shared render helpers ---- */
  // Metric icons (currentColor stroke). WHR = hourglass (waist↔hip); BWR = bust curve over
  // waist; DROP = caliper gap (bust − underbust = cup volume).
  const IC_WHR = '<svg viewBox="0 0 16 16" class="rsvg" aria-hidden="true"><path d="M4 2h8M4 14h8M4.5 2.4C4.5 6 11.5 6 11.5 2.4M4.5 13.6C4.5 10 11.5 10 11.5 13.6"/></svg>';
  const IC_BWR = '<svg viewBox="0 0 16 16" class="rsvg" aria-hidden="true"><path d="M1.5 8.5c2.6-4 10.4-4 13 0"/><path d="M4 13h8"/></svg>';
  const IC_DROP = '<svg viewBox="0 0 16 16" class="rsvg" aria-hidden="true"><path d="M2 4h12M2 12h12M8 4.6v6.8M5.6 7 8 4.6 10.4 7M5.6 9 8 11.4 10.4 9"/></svg>';
  const TIP_WHR = 'Waist-to-hip ratio — lower is more hourglass';
  const TIP_BWR = 'Bust-to-waist ratio — higher is more bust-forward';
  const TIP_DROP = 'Bust drop — bust minus underbust (cup volume)';
  function ratioStat(icon, val, tip){ return `<span class="rstat" title="${tip}">${icon}<span>${val}</span></span>`; }

  // A small shared legend explaining the body-metric icons. Pages drop it near a body grid.
  function metricsLegend(){
    return `<div class="metrics-legend">
      <span class="lg-title">Reading the signature</span>
      <span class="rstat" title="${TIP_WHR}">${IC_WHR}<span>Waist : hip</span></span>
      <span class="rstat" title="${TIP_BWR}">${IC_BWR}<span>Bust : waist</span></span>
      <span class="rstat" title="${TIP_DROP}">${IC_DROP}<span>Bust drop</span></span>
      <span class="lg-note">ratios shown as % · lower waist:hip = more hourglass, higher bust:waist = more bust-forward</span>
    </div>`;
  }

  function charStatusMeta(c){
    const isLive = c.status === 'live';
    const shootStatus = (c.photoshoot && c.photoshoot.status) || '';
    if (isLive && shootStatus === 'live') return { cls: 'stat stat-verified', label: 'Verified' };
    if (isLive) return { cls: 'stat stat-live', label: 'Live' };
    if (!isLive && img(c)) return { cls: 'stat stat-pending', label: 'Shoot Pending' };
    return { cls: 'stat stat-concept', label: 'Concept' };
  }

  function bodyStatusMeta(body){
    if (body && body.estimated) return { cls: 'stat stat-estimated', label: 'Estimated' };
    return { cls: 'stat stat-verified', label: 'Verified' };
  }

  function charCard(c){
    const ph = c.status !== 'live';
    const src = img(c);
    const fc = famColor(c.body.family);
    const status = charStatusMeta(c);
    // Graceful imagery: live → photo; placeholder with a borrowed sibling shoot → that
    // photo, softened, tagged "Concept"; placeholder with no image at all → a branded
    // monogram tile in the family color rather than an empty black box.
    const monogram = esc((c.persona.name||'?').trim().charAt(0).toUpperCase());
    const imgHtml = src
      ? `<img loading="lazy" src="${src}" alt="${esc(c.persona.name)}">`
      : `<div class="monotile" style="--fc:${fc}"><span>${monogram}</span></div>`;
    return `<a class="card ${ph?'ph':''}" href="character.html?id=${encodeURIComponent(c.character_id)}">
      <div class="imgwrap">
        ${imgHtml}
        ${ph?`<span class="repbadge">Concept${src?' · sister shoot':''}</span>`:''}
      </div>
      <div class="b">
        <div class="pname-row">
          <div class="pname">${esc(c.persona.name)}</div>
          <div class="card-meta-rail">
            <span class="cupchip" style="color:${fc};border-color:${fc}" title="Bust / cup size">${esc(c.body.cup)}-cup</span>
            <span class="${status.cls}">${status.label}</span>
          </div>
        </div>
        <div class="ptitle">${esc(c.persona.title)}</div>
        <div class="ptag">${esc(c.persona.tagline)}</div>
      </div></a>`;
  }
  function bodyCard(bc, m){
    const chars = m.byBody[bc] || [];
    const lead = chars.find(c=>c.status==='live') || chars[0];
    const bd = chars[0] ? chars[0].body : {};
    const meta = m.btByCode[bc] || {};
    const fc = famColor(bd.family);
    const src = lead ? img(lead) : '';
    const bodyStatus = bodyStatusMeta(bd);
    // Signature line: WHR/BWR as labelled-icon percentages + bust drop. (No character/shoot
    // counts — the character names below already convey that.)
    const pct = v => Math.round(v * 100) + '%';
    let sig;
    if (bd.WHR != null) {
      const drop = (bd.bust_drop_cm != null)
        ? ' · ' + ratioStat(IC_DROP, bd.bust_drop_cm + 'cm', TIP_DROP) : '';
      sig = ratioStat(IC_WHR, pct(bd.WHR), TIP_WHR)
          + ' · ' + ratioStat(IC_BWR, pct(bd.BWR), TIP_BWR)
          + drop;
      // estimated bodies: keep the line tight — no visible word, just a hover note.
      if (bd.estimated) sig = `<span title="Estimated — measurements interpolated; no published spec card">${sig}</span>`;
    } else {
      sig = 'spec card pending';
    }
    // Lead with the body's own identity (stature) so bodies in a single-family series
    // read as distinct. Family becomes a small chip (soft "spec card pending" when null).
    const famChip = bd.family
      ? `<span class="fam ${famClass(bd.family)}">${esc(bd.family)}</span>`
      : `<span class="fam fam--unclassified">Spec card pending</span>`;
    const names = chars.filter(c=>c.status==='live').slice(0,4).map(c=>esc(c.persona.name)).join(' · ');
    return `<a class="bodycard" href="body.html?b=${encodeURIComponent(bc)}">
      <div class="bw">${src?`<img loading="lazy" src="${src}" alt="${bc}">`:''}</div>
      <div class="bb">
        <h4>${bd.height_cm}cm · ${bd.cup}-cup</h4>
        <div class="m"><span class="bcode">${bc}</span> ${famChip} <span class="${bodyStatus.cls}">${bodyStatus.label}</span></div>
        ${names?`<div class="bnames">${names}</div>`:''}
        <div class="sig" style="color:${fc}">${sig}</div>
      </div></a>`;
  }

  return { load, famColor, famClass, qs, esc, img, inquireHref, contactHref, INQUIRY_EMAIL, FORM_ENDPOINT,
           getCompareBodies, setCompareBodies, addCompareBody,
           track,
           mountNav, mountFooter, fail, charCard, bodyCard, metricsLegend,
           repImg, heroBackdrop, revealInit,
           SERIES_ORDER, SERIES_SUB, FAMILIES };
})();
