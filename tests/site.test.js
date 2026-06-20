/**
 * Tests for assets/site.js — the shared browser runtime (window.ZX).
 *
 * site.js is a non-module IIFE that assigns to window.ZX.  We load it by
 * reading the source text and evaluating it with new Function() so it runs
 * in the jsdom global scope without any module-system friction.
 */
import { readFileSync } from 'node:fs'
import { resolve, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'
import { describe, it, expect, beforeAll, beforeEach, vi } from 'vitest'

const __dirname = dirname(fileURLToPath(import.meta.url))
const SITE_JS   = resolve(__dirname, '../assets/site.js')

/** Evaluate site.js in the jsdom global scope and return a fresh window.ZX. */
function loadZX() {
  // requestAnimationFrame is not in jsdom; shim it so revealInit doesn't throw
  if (!globalThis.requestAnimationFrame) {
    globalThis.requestAnimationFrame = (cb) => setTimeout(cb, 16)
  }
  const code = readFileSync(SITE_JS, 'utf-8')
  // new Function runs the code as a non-strict function with access to globals
  new Function(code)()
  return globalThis.ZX
}

// ---------------------------------------------------------------------------
// esc()
// ---------------------------------------------------------------------------

describe('esc', () => {
  let esc
  beforeAll(() => { esc = loadZX().esc })

  it('leaves plain text unchanged', () => expect(esc('hello')).toBe('hello'))
  it('escapes <', () => expect(esc('<')).toBe('&lt;'))
  it('escapes >', () => expect(esc('>')).toBe('&gt;'))
  it('escapes &', () => expect(esc('&')).toBe('&amp;'))
  it('escapes "', () => expect(esc('"')).toBe('&quot;'))
  it('escapes a mixed string', () =>
    expect(esc('<script>alert("xss")&done</script>')).toBe(
      '&lt;script&gt;alert(&quot;xss&quot;)&amp;done&lt;/script&gt;'
    ))
  it('handles null → empty string', () => expect(esc(null)).toBe(''))
  it('handles undefined → empty string', () => expect(esc(undefined)).toBe(''))
  it('coerces a number to string', () => expect(esc(0)).toBe('0'))
  it('handles empty string', () => expect(esc('')).toBe(''))
})

// ---------------------------------------------------------------------------
// famColor()
// ---------------------------------------------------------------------------

describe('famColor', () => {
  let famColor
  beforeAll(() => { famColor = loadZX().famColor })

  it('strips "The " prefix from family name', () =>
    expect(famColor('The Classic')).toBe('var(--Classic)'))

  it('works for all known families', () => {
    const families = ['The Classic', 'The Icon', 'The Muse', 'The Siren', 'The Empress', 'The Sculpt']
    for (const f of families) {
      expect(famColor(f)).toMatch(/^var\(--\w+\)$/)
    }
  })

  it('returns var(--muted) for null', () =>
    expect(famColor(null)).toBe('var(--muted)'))

  it('returns var(--muted) for undefined', () =>
    expect(famColor(undefined)).toBe('var(--muted)'))

  it('returns var(--muted) for empty string (falsy)', () =>
    expect(famColor('')).toBe('var(--muted)'))
})

// ---------------------------------------------------------------------------
// img()
// ---------------------------------------------------------------------------

describe('img', () => {
  let img
  beforeAll(() => { img = loadZX().img })

  it('prefers hero_thumb over hero', () =>
    expect(img({ photoshoot: { hero_thumb: 'thumb.jpg', hero: 'hero.jpg' } })).toBe('thumb.jpg'))

  it('falls back to hero when no thumb', () =>
    expect(img({ photoshoot: { hero: 'hero.jpg' } })).toBe('hero.jpg'))

  it('returns empty string when photoshoot is absent', () =>
    expect(img({})).toBe(''))

  it('returns empty string when photoshoot is null', () =>
    expect(img({ photoshoot: null })).toBe(''))

  it('returns empty string when both hero fields are absent', () =>
    expect(img({ photoshoot: {} })).toBe(''))
})

// ---------------------------------------------------------------------------
// contactHref()
// ---------------------------------------------------------------------------

describe('contactHref', () => {
  let contactHref
  beforeAll(() => { contactHref = loadZX().contactHref })

  it('builds a link with the character_id', () =>
    expect(contactHref({ character_id: 'K-ZK168B-01' }))
      .toBe('contact.html?id=K-ZK168B-01'))

  it('URI-encodes special characters in the id', () =>
    expect(contactHref({ character_id: 'a b/c' }))
      .toBe('contact.html?id=a%20b%2Fc'))
})

// ---------------------------------------------------------------------------
// inquireHref()
// ---------------------------------------------------------------------------

describe('inquireHref', () => {
  let inquireHref
  beforeAll(() => { inquireHref = loadZX().inquireHref })

  const baseChar = {
    body_code: 'ZK168B',
    series: 'K-Series',
    persona: { name: 'Sora', title: 'The Classic' },
    body: { height_cm: 168, cup: 'B', family: 'The Classic' },
    photoshoot: { product_code: 'KE03_1+ZK168B', price: 2500 },
  }

  it('returns a mailto: link', () =>
    expect(inquireHref(baseChar)).toMatch(/^mailto:/))

  it('encodes the character name in the subject', () => {
    const href = inquireHref(baseChar)
    expect(decodeURIComponent(href)).toContain('Sora')
  })

  it('encodes the body code in the subject', () => {
    expect(decodeURIComponent(inquireHref(baseChar))).toContain('ZK168B')
  })

  it('includes price when present', () =>
    expect(decodeURIComponent(inquireHref(baseChar))).toContain('2500'))

  it('omits price line when price is falsy', () => {
    const c = { ...baseChar, photoshoot: { product_code: 'KE03_1+ZK168B' } }
    expect(decodeURIComponent(inquireHref(c))).not.toContain('Listed')
  })

  it('omits product line when product_code is absent', () => {
    const c = { ...baseChar, photoshoot: {} }
    expect(decodeURIComponent(inquireHref(c))).not.toContain('Product')
  })

  it('handles missing body gracefully', () => {
    const c = { ...baseChar, body: undefined }
    expect(() => inquireHref(c)).not.toThrow()
  })
})

// ---------------------------------------------------------------------------
// repImg()
// ---------------------------------------------------------------------------

describe('repImg', () => {
  let repImg
  beforeAll(() => { repImg = loadZX().repImg })

  const live   = s => ({ status: 'live',        photoshoot: { hero_thumb: s } })
  const ph     = s => ({ status: 'placeholder', photoshoot: { hero_thumb: s } })

  it('returns empty string for empty array', () =>
    expect(repImg([], 0)).toBe(''))

  it('skips placeholder characters', () =>
    expect(repImg([ph('p.jpg')], 0)).toBe(''))

  it('returns the first live image when idx=0', () =>
    expect(repImg([live('a.jpg'), live('b.jpg')], 0)).toBe('a.jpg'))

  it('returns the second live image when idx=1', () =>
    expect(repImg([live('a.jpg'), live('b.jpg')], 1)).toBe('b.jpg'))

  it('falls back to idx=0 when idx is out of range', () =>
    expect(repImg([live('a.jpg')], 5)).toBe('a.jpg'))

  it('skips chars without images', () => {
    const noImg = { status: 'live', photoshoot: {} }
    expect(repImg([noImg, live('b.jpg')], 0)).toBe('b.jpg')
  })
})

// ---------------------------------------------------------------------------
// heroBackdrop()
// ---------------------------------------------------------------------------

describe('heroBackdrop', () => {
  let heroBackdrop
  beforeAll(() => { heroBackdrop = loadZX().heroBackdrop })

  it('returns empty string for falsy src', () => {
    expect(heroBackdrop('')).toBe('')
    expect(heroBackdrop(null)).toBe('')
    expect(heroBackdrop(undefined)).toBe('')
  })

  it('wraps a real src in a .backdrop div', () => {
    const html = heroBackdrop('hero.jpg')
    expect(html).toContain('class="backdrop"')
    expect(html).toContain("url('hero.jpg')")
  })
})

// ---------------------------------------------------------------------------
// charCard()
// ---------------------------------------------------------------------------

describe('charCard', () => {
  let charCard
  beforeAll(() => { charCard = loadZX().charCard })

  const liveChar = {
    status: 'live',
    character_id: 'K-ZK168B-01',
    persona: { name: 'Sora', title: 'The Classic', tagline: 'Timeless.' },
    body: { family: 'The Classic', cup: 'B' },
    photoshoot: { hero_thumb: 'assets/img.jpg' },
  }

  it('renders an anchor tag for the character', () =>
    expect(charCard(liveChar)).toContain('<a class="card '))

  it('includes the character_id in the href', () =>
    expect(charCard(liveChar)).toContain('K-ZK168B-01'))

  it('renders an <img> for a live character with an image', () =>
    expect(charCard(liveChar)).toContain('<img'))

  it('renders a monogram tile for a placeholder with no image', () => {
    const ph = {
      ...liveChar,
      status: 'placeholder',
      photoshoot: {},
    }
    const html = charCard(ph)
    expect(html).toContain('monotile')
    expect(html).toContain('S')  // first letter of 'Sora'
  })

  it('adds "ph" class for placeholder characters', () => {
    const ph = { ...liveChar, status: 'placeholder', photoshoot: {} }
    expect(charCard(ph)).toContain('class="card ph"')
  })

  it('does not add "ph" class for live characters', () =>
    expect(charCard(liveChar)).not.toContain('class="card ph"'))

  it('shows Concept badge for placeholder', () => {
    const ph = { ...liveChar, status: 'placeholder', photoshoot: {} }
    expect(charCard(ph)).toContain('Concept')
  })

  it('escapes HTML in persona name', () => {
    const c = { ...liveChar, persona: { ...liveChar.persona, name: '<Evil>' } }
    const html = charCard(c)
    expect(html).not.toContain('<Evil>')
    expect(html).toContain('&lt;Evil&gt;')
  })

  it('uses "?" as monogram when name is empty', () => {
    const c = {
      ...liveChar,
      status: 'placeholder',
      photoshoot: {},
      persona: { ...liveChar.persona, name: '' },
    }
    expect(charCard(c)).toContain('<span>?</span>')
  })
})

// ---------------------------------------------------------------------------
// bodyCard()
// ---------------------------------------------------------------------------

describe('bodyCard', () => {
  let bodyCard
  beforeAll(() => { bodyCard = loadZX().bodyCard })

  const makeModel = (chars) => ({
    byBody: { 'ZK168B': chars },
    btByCode: { 'ZK168B': {} },
  })

  const liveChar = {
    status: 'live',
    body: { family: 'The Classic', height_cm: 168, cup: 'B', WHR: 0.65, BWR: 1.42 },
    persona: { name: 'Sora' },
    photoshoot: { hero_thumb: 'img.jpg' },
  }

  it('renders an anchor tag linking to body.html', () =>
    expect(bodyCard('ZK168B', makeModel([liveChar]))).toContain('href="body.html?b=ZK168B"'))

  it('shows height and cup', () => {
    const html = bodyCard('ZK168B', makeModel([liveChar]))
    expect(html).toContain('168cm')
    expect(html).toContain('B-cup')
  })

  it('shows WHR/BWR signature when measurements are present', () => {
    const html = bodyCard('ZK168B', makeModel([liveChar]))
    expect(html).toContain('%')
  })

  it('shows "spec card pending" when WHR is null', () => {
    const c = { ...liveChar, body: { ...liveChar.body, WHR: null } }
    expect(bodyCard('ZK168B', makeModel([c]))).toContain('spec card pending')
  })

  it('handles unknown body code gracefully', () => {
    const model = makeModel([liveChar])
    // No entry in byBody for 'ZZUNKNOWN' — should not throw
    expect(() => bodyCard('ZZUNKNOWN', model)).not.toThrow()
  })

  it('shows live character names', () => {
    const html = bodyCard('ZK168B', makeModel([liveChar]))
    expect(html).toContain('Sora')
  })

  it('wraps estimated signature in a title-attribute span', () => {
    const c = { ...liveChar, body: { ...liveChar.body, estimated: true } }
    const html = bodyCard('ZK168B', makeModel([c]))
    expect(html).toContain('Estimated')
  })
})

// ---------------------------------------------------------------------------
// load()  — async, requires fetch mock
// ---------------------------------------------------------------------------

describe('load', () => {
  let zx

  function mockFetch(chars = [], bodyTypes = [], profiles = {}) {
    return vi.fn((url) => {
      let data
      if (url.includes('characters.json'))   data = { characters: chars }
      else if (url.includes('body_types'))   data = { body_types: bodyTypes }
      else                                    data = { profiles }
      return Promise.resolve({ json: () => Promise.resolve(data) })
    })
  }

  beforeEach(() => {
    // Fresh ZX instance so _model cache starts empty
    zx = loadZX()
    vi.stubGlobal('fetch', mockFetch())
  })

  afterEach(() => vi.unstubAllGlobals())

  it('returns a model with expected keys', async () => {
    const model = await zx.load()
    expect(model).toHaveProperty('characters')
    expect(model).toHaveProperty('byId')
    expect(model).toHaveProperty('byBody')
    expect(model).toHaveProperty('bySeries')
    expect(model).toHaveProperty('btByCode')
    expect(model).toHaveProperty('bodyTypes')
    expect(model).toHaveProperty('profiles')
    expect(model).toHaveProperty('series')
    expect(model).toHaveProperty('FAMILIES')
  })

  it('indexes characters by id', async () => {
    vi.stubGlobal('fetch', mockFetch([
      { character_id: 'abc', body_code: 'ZK168B', series: 'K-Series', slot: 1 }
    ]))
    const model = await zx.load()
    expect(model.byId['abc']).toBeDefined()
    expect(model.byId['abc'].character_id).toBe('abc')
  })

  it('groups characters by body code', async () => {
    vi.stubGlobal('fetch', mockFetch([
      { character_id: 'a1', body_code: 'ZK168B', series: 'K-Series', slot: 1 },
      { character_id: 'a2', body_code: 'ZK168B', series: 'K-Series', slot: 2 },
    ]))
    const model = await zx.load()
    expect(model.byBody['ZK168B']).toHaveLength(2)
  })

  it('sorts byBody entries by slot', async () => {
    vi.stubGlobal('fetch', mockFetch([
      { character_id: 'a2', body_code: 'ZK168B', series: 'K-Series', slot: 2 },
      { character_id: 'a1', body_code: 'ZK168B', series: 'K-Series', slot: 1 },
    ]))
    const model = await zx.load()
    const slots = model.byBody['ZK168B'].map(c => c.slot)
    expect(slots).toEqual([1, 2])
  })

  it('caches the model — fetch called only 3 times total', async () => {
    const fetchSpy = mockFetch()
    vi.stubGlobal('fetch', fetchSpy)
    await zx.load()
    await zx.load()
    expect(fetchSpy).toHaveBeenCalledTimes(3)  // 3 files on first call, 0 on second
  })

  it('throws a data-load error on network failure', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('Network error')))
    await expect(zx.load()).rejects.toThrow('data-load')
  })

  it('body_profiles.json failure is silently swallowed', async () => {
    // profiles fetch uses .catch(()=>({profiles:{}})) so it never rejects
    vi.stubGlobal('fetch', vi.fn((url) => {
      if (url.includes('body_profiles')) return Promise.reject(new Error('404'))
      return Promise.resolve({ json: () => Promise.resolve({ characters: [], body_types: [] }) })
    }))
    const model = await zx.load()
    expect(model).toBeDefined()
    expect(model.profiles).toEqual({})
  })

  it('only includes series present in the character data', async () => {
    vi.stubGlobal('fetch', mockFetch([
      { character_id: 'k1', body_code: 'ZK168B', series: 'K-Series', slot: 1 }
    ]))
    const model = await zx.load()
    expect(model.series).toContain('K-Series')
    expect(model.series).not.toContain('Fusion')
  })
})

// ---------------------------------------------------------------------------
// famClass()
// ---------------------------------------------------------------------------

describe('famClass', () => {
  let famClass
  beforeAll(() => { famClass = loadZX().famClass })

  it('converts "The Classic" to "fam--classic"', () =>
    expect(famClass('The Classic')).toBe('fam--classic'))

  it('converts "The Icon" to "fam--icon"', () =>
    expect(famClass('The Icon')).toBe('fam--icon'))

  it('converts "The Muse" to "fam--muse"', () =>
    expect(famClass('The Muse')).toBe('fam--muse'))

  it('converts "The Siren" to "fam--siren"', () =>
    expect(famClass('The Siren')).toBe('fam--siren'))

  it('converts "The Empress" to "fam--empress"', () =>
    expect(famClass('The Empress')).toBe('fam--empress'))

  it('converts "The Sculpt" to "fam--sculpt"', () =>
    expect(famClass('The Sculpt')).toBe('fam--sculpt'))

  it('returns "fam--unclassified" for null', () =>
    expect(famClass(null)).toBe('fam--unclassified'))

  it('returns "fam--unclassified" for undefined', () =>
    expect(famClass(undefined)).toBe('fam--unclassified'))

  it('returns "fam--unclassified" for empty string', () =>
    expect(famClass('')).toBe('fam--unclassified'))

  it('returns "fam--unclassified" for unknown family', () =>
    expect(famClass('The Athlete')).toBe('fam--unclassified'))
})

// ---------------------------------------------------------------------------
// qs()
// ---------------------------------------------------------------------------

describe('qs', () => {
  let qs
  let origLocation

  beforeAll(() => { qs = loadZX().qs })
  beforeEach(() => { origLocation = globalThis.location })
  afterEach(() => { globalThis.location = origLocation })

  function withSearch(search) {
    globalThis.location = { search }
  }

  it('extracts f parameter from ?f=siren', () => {
    withSearch('?f=siren')
    expect(qs('f')).toBe('siren')
  })

  it('extracts id parameter from ?id=K-ZK168B-01', () => {
    withSearch('?id=K-ZK168B-01')
    expect(qs('id')).toBe('K-ZK168B-01')
  })

  it('returns null for missing parameter in empty search', () => {
    withSearch('')
    expect(qs('f')).toBeNull()
  })

  it('returns null for missing parameter when others present', () => {
    withSearch('?a=1')
    expect(qs('b')).toBeNull()
  })

  it('extracts parameter from multiple parameters', () => {
    withSearch('?a=1&b=2')
    expect(qs('b')).toBe('2')
  })
})

// ---------------------------------------------------------------------------
// getCompareBodies() / setCompareBodies() / addCompareBody()
// ---------------------------------------------------------------------------

describe('compare bodies', () => {
  let getCompareBodies, setCompareBodies, addCompareBody

  beforeAll(() => {
    const zx = loadZX()
    getCompareBodies = zx.getCompareBodies
    setCompareBodies = zx.setCompareBodies
    addCompareBody   = zx.addCompareBody
  })
  beforeEach(() => { localStorage.clear() })

  // --- getCompareBodies tests ---

  it('returns empty array when localStorage is empty', () =>
    expect(getCompareBodies()).toEqual([]))

  it('parses stored array from localStorage', () => {
    localStorage.setItem('zx_compare_bodies', JSON.stringify(['ZK168B', 'ZK170D']))
    expect(getCompareBodies()).toEqual(['ZK168B', 'ZK170D'])
  })

  it('strips falsy values from stored array', () => {
    localStorage.setItem('zx_compare_bodies', JSON.stringify(['ZK168B', null, 'ZK170D', false]))
    expect(getCompareBodies()).toEqual(['ZK168B', 'ZK170D'])
  })

  it('strips "." values from stored array', () => {
    localStorage.setItem('zx_compare_bodies', JSON.stringify(['ZK168B', '.', 'ZK170D']))
    expect(getCompareBodies()).toEqual(['ZK168B', 'ZK170D'])
  })

  it('caps results at 4 entries even if more are stored', () => {
    localStorage.setItem('zx_compare_bodies', JSON.stringify(['A', 'B', 'C', 'D', 'E']))
    expect(getCompareBodies()).toEqual(['A', 'B', 'C', 'D'])
  })

  it('returns empty array when non-array is stored', () => {
    localStorage.setItem('zx_compare_bodies', JSON.stringify('not-an-array'))
    expect(getCompareBodies()).toEqual([])
  })

  // --- setCompareBodies tests ---

  it('stores array and returns it', () => {
    const result = setCompareBodies(['A', 'B'])
    expect(result).toEqual(['A', 'B'])
    expect(JSON.parse(localStorage.getItem('zx_compare_bodies'))).toEqual(['A', 'B'])
  })

  it('strips falsy values and "." when setting', () => {
    const result = setCompareBodies(['A', null, 'B', '.', 'C'])
    expect(result).toEqual(['A', 'B', 'C'])
  })

  it('caps at 4 entries when setting', () => {
    const result = setCompareBodies(['A', 'B', 'C', 'D', 'E'])
    expect(result).toEqual(['A', 'B', 'C', 'D'])
  })

  it('returns empty array for non-array input', () => {
    const result = setCompareBodies('not-an-array')
    expect(result).toEqual([])
  })

  // --- addCompareBody tests ---

  it('adds new code and returns { added: true }', () => {
    const result = addCompareBody('ZK168B')
    expect(result.added).toBe(true)
    expect(result.bodies).toContain('ZK168B')
  })

  it('returns { added: false } when adding duplicate code', () => {
    setCompareBodies(['ZK168B'])
    const result = addCompareBody('ZK168B')
    expect(result.added).toBe(false)
    expect(result.bodies).toEqual(['ZK168B'])
  })

  it('returns { added: false } for empty string', () => {
    const result = addCompareBody('')
    expect(result.added).toBe(false)
    expect(result.bodies).toEqual([])
  })

  it('returns { added: false } for "."', () => {
    const result = addCompareBody('.')
    expect(result.added).toBe(false)
    expect(result.bodies).toEqual([])
  })

  it('does not add 5th code when 4 already present', () => {
    setCompareBodies(['A', 'B', 'C', 'D'])
    const result = addCompareBody('E')
    expect(result.bodies).toHaveLength(4)
    expect(result.bodies).not.toContain('E')
  })
})
