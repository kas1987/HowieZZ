import { beforeEach, describe, expect, test, vi } from 'vitest';

// site.js is an IIFE that assigns window.ZX as a side effect. Importing it (vs.
// eval) lets v8 attribute coverage back to the source file.
import '../../assets/site.js';

const ZX = window.ZX;

beforeEach(() => {
  localStorage.clear();
  sessionStorage.clear();
});

describe('family helpers', () => {
  test('famColor maps a family to a CSS var, else muted', () => {
    expect(ZX.famColor('The Siren')).toBe('var(--Siren)');
    expect(ZX.famColor('')).toBe('var(--muted)');
    expect(ZX.famColor(null)).toBe('var(--muted)');
  });

  test('famClass maps every known family', () => {
    expect(ZX.famClass('The Classic')).toBe('fam--classic');
    expect(ZX.famClass('The Icon')).toBe('fam--icon');
    expect(ZX.famClass('The Muse')).toBe('fam--muse');
    expect(ZX.famClass('The Siren')).toBe('fam--siren');
    expect(ZX.famClass('The Empress')).toBe('fam--empress');
    expect(ZX.famClass('The Sculpt')).toBe('fam--sculpt');
    expect(ZX.famClass('Mystery')).toBe('fam--unclassified');
    expect(ZX.famClass(null)).toBe('fam--unclassified');
  });
});

describe('esc (XSS-prevention)', () => {
  test('escapes HTML metacharacters', () => {
    expect(ZX.esc('<script>alert("x")&</script>'))
      .toBe('&lt;script&gt;alert(&quot;x&quot;)&amp;&lt;/script&gt;');
  });

  test('null/undefined become empty string', () => {
    expect(ZX.esc(null)).toBe('');
    expect(ZX.esc(undefined)).toBe('');
    expect(ZX.esc(42)).toBe('42');
  });
});

describe('qs (query string)', () => {
  test('reads a query param from location', () => {
    window.history.pushState({}, '', '/?id=K-ZK168B-01&empty=');
    expect(ZX.qs('id')).toBe('K-ZK168B-01');
    expect(ZX.qs('missing')).toBeNull();
    window.history.pushState({}, '', '/');
  });
});

describe('session id', () => {
  test('createSessionId has the zx_ prefix and entropy', () => {
    const a = ZX_internalCreate();
    expect(a).toMatch(/^zx_[a-z0-9]+_[a-z0-9]+$/);
  });

  test('getSessionId persists across calls', () => {
    // first call (track) generates + stores a session id
    ZX.track('page_view', {});
    const stored = sessionStorage.getItem('zx_analytics_session_id');
    expect(stored).toMatch(/^zx_/);
    expect(localStorage.getItem('zx_analytics_session_id')).toBe(stored);
  });
});

// createSessionId isn't exported; reach it indirectly through track()'s payload.
function ZX_internalCreate() {
  let detail;
  const handler = (e) => { detail = e.detail; };
  window.addEventListener('zx:track', handler, { once: true });
  ZX.track('page_view', {});
  window.removeEventListener('zx:track', handler);
  return detail.session_id;
}

describe('compare set storage', () => {
  test('addCompareBody adds unique, valid codes only', () => {
    expect(ZX.getCompareBodies()).toEqual([]);
    expect(ZX.addCompareBody('ZK168B')).toEqual({ added: true, bodies: ['ZK168B'] });
    // duplicate is rejected
    expect(ZX.addCompareBody('ZK168B')).toEqual({ added: false, bodies: ['ZK168B'] });
    // placeholder '.' and empty are rejected
    expect(ZX.addCompareBody('.').added).toBe(false);
    expect(ZX.addCompareBody('').added).toBe(false);
  });

  test('setCompareBodies caps at 4 and strips junk', () => {
    const out = ZX.setCompareBodies(['A', 'B', '.', 'C', 'D', 'E', null]);
    expect(out).toEqual(['A', 'B', 'C', 'D']);
    expect(ZX.getCompareBodies()).toEqual(['A', 'B', 'C', 'D']);
  });

  test('getCompareBodies tolerates corrupt storage', () => {
    localStorage.setItem('zx_compare_bodies', '{not json');
    expect(ZX.getCompareBodies()).toEqual([]);
    localStorage.setItem('zx_compare_bodies', '"a string"');
    expect(ZX.getCompareBodies()).toEqual([]);
  });
});

describe('track + normalizeTrackPayload', () => {
  function capture(eventName, payload) {
    let detail;
    const handler = (e) => { detail = e.detail; };
    window.addEventListener('zx:track', handler, { once: true });
    ZX.track(eventName, payload);
    window.removeEventListener('zx:track', handler);
    return detail;
  }

  test('aliases events and injects global fields', () => {
    const d = capture('compare_add_from_body', { body_code: 'ZK168B ' });
    expect(d.event).toBe('compare_add');           // alias applied
    expect(d.event_original).toBe('compare_add_from_body');
    expect(d.source).toBe('howiezz-web');
    expect(d.schema_version).toBeTruthy();
    expect(d.session_id).toMatch(/^zx_/);
    expect(d.body_code).toBe('ZK168B');            // trimmed
  });

  test('normalizes body code lists and compare_count', () => {
    const d = capture('compare_set_changed', { body_codes: ['ZK168B', 'ZG170D', 'bad code!'] });
    expect(d.body_codes).toBe('ZK168B,ZG170D');    // invalid token filtered
    expect(d.compare_count).toBe(2);
  });

  test('truncates a long message into error_message', () => {
    const d = capture('inquiry_submit_error', { message: '  ' + 'x'.repeat(300) });
    expect(d.message).toBeUndefined();
    expect(d.error_message.length).toBe(180);
  });

  test('pushes to dataLayer when present', () => {
    window.dataLayer = [];
    ZX.track('page_view', {});
    expect(window.dataLayer.length).toBe(1);
    expect(window.dataLayer[0].event).toBe('page_view');
    delete window.dataLayer;
  });
});

describe('inquiry + contact links', () => {
  const character = {
    character_id: 'K-ZK168B-01',
    series: 'K-Series',
    body_code: 'ZK168B',
    persona: { name: 'Mira', title: 'The Classic' },
    body: { height_cm: 168, cup: 'B', family: 'The Classic' },
    photoshoot: { product_code: 'KE03_1+ZK168B-1', price: '1999' },
  };

  test('contactHref points at the form prefilled by id', () => {
    expect(ZX.contactHref(character)).toBe('contact.html?id=K-ZK168B-01');
  });

  test('inquireHref builds a mailto with subject + body', () => {
    const href = ZX.inquireHref(character);
    expect(href.startsWith(`mailto:${ZX.INQUIRY_EMAIL}?subject=`)).toBe(true);
    expect(decodeURIComponent(href)).toContain('Mira');
    expect(decodeURIComponent(href)).toContain('ZK168B');
  });
});

describe('render helpers', () => {
  const liveChar = {
    character_id: 'K-ZK168B-01', status: 'live',
    persona: { name: 'Mira', title: 'The Classic', tagline: 'Timeless.' },
    body: { family: 'The Classic', cup: 'B' },
    photoshoot: { status: 'live', hero_thumb: 'assets/x.jpg' },
  };
  const conceptChar = {
    character_id: 'K-ZK168B-02', status: 'placeholder',
    persona: { name: 'Lian', title: 'The Sweetheart', tagline: 'New face.' },
    body: { family: 'The Classic', cup: 'B' },
    photoshoot: {},
  };

  test('charCard renders a live photo card', () => {
    const html = ZX.charCard(liveChar);
    expect(html).toContain('character.html?id=K-ZK168B-01');
    expect(html).toContain('Mira');
    expect(html).toContain('<img');
  });

  test('charCard renders a monogram tile when no image', () => {
    const html = ZX.charCard(conceptChar);
    expect(html).toContain('monotile');
    expect(html).toContain('>L<');     // monogram from "Lian"
    expect(html).toContain('Concept');
  });

  test('bodyCard renders signature ratios', () => {
    const model = {
      byBody: { ZK168B: [liveChar] },
      btByCode: { ZK168B: {} },
    };
    liveChar.body = { family: 'The Classic', cup: 'B', height_cm: 168, WHR: 0.7, BWR: 1.45, bust_drop_cm: 16 };
    const html = ZX.bodyCard('ZK168B', model);
    expect(html).toContain('body.html?b=ZK168B');
    expect(html).toContain('168cm');
    expect(html).toContain('70%');     // WHR rendered as a percentage
  });

  test('bodyCard handles a body with no measurements', () => {
    const bare = { ...liveChar, body: { family: null, cup: 'B', height_cm: 168 } };
    const model = { byBody: { ZK168B: [bare] }, btByCode: {} };
    const html = ZX.bodyCard('ZK168B', model);
    expect(html).toContain('spec card pending');
    expect(html).toContain('Spec card pending');
  });

  test('metricsLegend returns the legend block', () => {
    expect(ZX.metricsLegend()).toContain('Reading the signature');
  });

  test('repImg + heroBackdrop', () => {
    const chars = [{ status: 'live', photoshoot: { hero: 'a.jpg' } }];
    expect(ZX.repImg(chars, 0)).toBe('a.jpg');
    expect(ZX.repImg([], 0)).toBe('');
    expect(ZX.heroBackdrop('a.jpg')).toContain("url('a.jpg')");
    expect(ZX.heroBackdrop('')).toBe('');
  });
});

describe('DOM mounts', () => {
  beforeEach(() => {
    document.body.innerHTML = '<main></main>';
  });

  test('mountNav injects the primary nav', () => {
    ZX.mountNav('browse.html');
    const nav = document.querySelector('nav.nav');
    expect(nav).not.toBeNull();
    expect(document.querySelector('a[href="browse.html"].active')).not.toBeNull();
  });

  test('mountFooter injects a footer', () => {
    ZX.mountFooter();
    expect(document.querySelector('footer')).not.toBeNull();
  });

  test('fail renders an error message', () => {
    document.body.innerHTML = '<div id="app"></div>';
    ZX.fail();
    expect(document.getElementById('app').innerHTML).toContain('Could not load');
  });
});

describe('load (data model)', () => {
  test('fetches and indexes the catalog', async () => {
    const characters = [
      { character_id: 'K-ZK168B-01', body_code: 'ZK168B', series: 'K-Series', slot: 1 },
      { character_id: 'K-ZK168B-02', body_code: 'ZK168B', series: 'K-Series', slot: 2 },
    ];
    const fetchMock = vi.fn((url) => {
      const body = url.includes('characters') ? { characters }
        : url.includes('body_types') ? { body_types: [{ body_code: 'ZK168B' }] }
          : { profiles: {}, families: {} };
      return Promise.resolve({ json: () => Promise.resolve(body) });
    });
    global.fetch = fetchMock;

    const model = await ZX.load();
    expect(model.characters).toHaveLength(2);
    expect(model.byBody.ZK168B).toHaveLength(2);
    expect(model.byId['K-ZK168B-01']).toBeTruthy();
    expect(model.series).toContain('K-Series');
    // cached on second call (no extra fetches)
    const calls = fetchMock.mock.calls.length;
    await ZX.load();
    expect(fetchMock.mock.calls.length).toBe(calls);
  });
});
