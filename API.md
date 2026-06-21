# Runtime API Reference

Complete specification of the `ZX` global object and browser runtime.

> See also: [ARCHITECTURE.md](ARCHITECTURE.md), [DATA-SCHEMA.md](DATA-SCHEMA.md)

**Location:** `assets/site.js` (single file, no npm dependencies)

---

## Table of Contents

1. [Initialization](#initialization)
2. [Core Methods](#core-methods)
3. [Data Access](#data-access)
4. [UI Components](#ui-components)
5. [Navigation & Routing](#navigation--routing)
6. [Analytics](#analytics)
7. [Comparison Tool](#comparison-tool)
8. [Quiz & Recommendation Engine](#quiz--recommendation-engine)
9. [Utility Helpers](#utility-helpers)
10. [Events & Hooks](#events--hooks)

---

## Initialization

### `ZX.load()`

Loads the entire catalog model asynchronously. Must be called before accessing any data.

**Signature:**
```javascript
ZX.load() → Promise<CatalogModel>
```

**Returns:**
```javascript
{
  catalog: {
    series: [ {id, name, folder, description, character_count, body_count}, … ],
    products: [ {code, head_code, body_code, series_id, …}, … ]
  },
  characters: [ {character_id, slot, series, status, persona, body, …}, … ],
  bodyProfiles: {
    families: [ {name, whr, bwr, silhouette, premium, target, color}, … ],
    bodies: [ {body_code, series_id, height_cm, cup, whr, bwr, family, …}, … ]
  },
  bodyTypes: [ {body_code, series, characters, …}, … ],
  characterStories: { "character_id": {story, profile}, … },
  families: [ "The Classic", "The Icon", "The Muse", "The Siren", "The Empress", "The Sculpt" ]
}
```

**Usage:**
```javascript
ZX.load().then(model => {
  console.log('Loaded', model.characters.length, 'characters');
  // Now safe to call other ZX methods
});
```

**Error Handling:**
- Rejects if any data file fails to load.
- Network timeouts produce a console warning; a fallback empty model is returned.
- Always check `model.characters.length > 0` before proceeding.

---

## Core Methods

### `ZX.getModel()`

Returns the cached catalog model (populated after `ZX.load()` completes).

**Signature:**
```javascript
ZX.getModel() → CatalogModel | null
```

**Returns:** Catalog model or `null` if not yet loaded.

**Usage:**
```javascript
const model = ZX.getModel();
if (!model) console.error('Catalog not loaded');
else console.log(model.characters.length);
```

---

## Data Access

### `ZX.getCharacter(characterId)`

Fetch a single character by ID.

**Signature:**
```javascript
ZX.getCharacter(id: string) → Character | null
```

**Example:**
```javascript
const vesper = ZX.getCharacter('SLE-ZX160J-03');
if (vesper) {
  console.log(vesper.persona.name);  // "Vesper"
  console.log(vesper.body.family);   // "The Siren"
}
```

---

### `ZX.getCharactersByBody(bodyCode)`

Fetch all 4 characters for a given body.

**Signature:**
```javascript
ZX.getCharactersByBody(bodyCode: string) → Character[]
```

**Example:**
```javascript
const bodyChars = ZX.getCharactersByBody('ZX160J');
console.log(bodyChars.length);  // 4
bodyChars.forEach(c => console.log(c.persona.name));
```

---

### `ZX.getCharactersBySeries(series)`

Fetch all characters in a series.

**Signature:**
```javascript
ZX.getCharactersBySeries(series: string) → Character[]
```

**Example:**
```javascript
const sle = ZX.getCharactersBySeries('SLE');
console.log(sle.length);  // 68
```

---

### `ZX.getCharactersByFamily(family)`

Fetch all characters in a body family.

**Signature:**
```javascript
ZX.getCharactersByFamily(family: string) → Character[]
```

**Example:**
```javascript
const sirens = ZX.getCharactersByFamily('The Siren');
console.log(sirens.length);  // ~20–30
```

---

### `ZX.getBody(bodyCode)`

Fetch body type details (architecture, measurements, family).

**Signature:**
```javascript
ZX.getBody(bodyCode: string) → BodyType | null
```

**Example:**
```javascript
const body = ZX.getBody('ZG170C');
if (body) {
  console.log(body.height_cm);  // 170
  console.log(body.family);     // "The Muse"
}
```

---

### `ZX.getFamilies()`

Get all 6 body families with full metadata.

**Signature:**
```javascript
ZX.getFamilies() → BodyFamily[]
```

**Returns:**
```javascript
[
  {
    name: "The Classic",
    whr: [0.68, 0.72],
    bwr: [1.4, 1.5],
    silhouette: "Timeless hourglass",
    premium: "+20%",
    target: "First-time premium buyer",
    color: "#FF6B9D"
  },
  // … 5 more …
]
```

---

### `ZX.getFamily(familyName)`

Get details for a single family.

**Signature:**
```javascript
ZX.getFamily(familyName: string) → BodyFamily | null
```

**Example:**
```javascript
const siren = ZX.getFamily('The Siren');
console.log(siren.whr);    // [0.55, 0.60]
console.log(siren.color);  // "#…"
```

---

## UI Components

### `ZX.mountNav()`

Render the top navigation bar.

**Signature:**
```javascript
ZX.mountNav() → void
```

**Renders:** Navigation links (all primary pages) into `<div id="nav">`.

**Example:**
```javascript
ZX.load().then(() => {
  ZX.mountNav();
});
```

**Expected HTML:**
```html
<div id="nav">…nav rendered here…</div>
```

---

### `ZX.mountFooter()`

Render the footer.

**Signature:**
```javascript
ZX.mountFooter() → void
```

**Renders:** Links, copyright, social → `<div id="footer">`.

---

### `ZX.renderCharacterCard(character, options)`

Generate HTML for a character card.

**Signature:**
```javascript
ZX.renderCharacterCard(
  character: Character,
  options?: {
    size?: 'small' | 'medium' | 'large',
    showStory?: boolean,
    href?: string
  }
) → string (HTML)
```

**Returns:** HTML string (does NOT insert into DOM).

**Example:**
```javascript
const html = ZX.renderCharacterCard(vesper, { size: 'medium', showStory: false });
document.querySelector('.gallery').innerHTML += html;
```

---

### `ZX.renderBodySpecCard(body)`

Generate HTML for a body spec card (measurements, family, silhouette).

**Signature:**
```javascript
ZX.renderBodySpecCard(body: BodyType) → string (HTML)
```

**Example:**
```javascript
const html = ZX.renderBodySpecCard(body);
document.querySelector('#body-detail').innerHTML = html;
```

---

### `ZX.renderComparison(bodyCodes)`

Generate HTML for a side-by-side body comparison.

**Signature:**
```javascript
ZX.renderComparison(bodyCodes: string[]) → string (HTML)
```

**Example:**
```javascript
const html = ZX.renderComparison(['ZG170C', 'ZX160J', 'ZF168B']);
document.querySelector('#compare-pane').innerHTML = html;
```

---

## Navigation & Routing

### `ZX.qs(paramName)`

Get a URL query parameter.

**Signature:**
```javascript
ZX.qs(paramName: string) → string | null
```

**Example:**
```javascript
const family = ZX.qs('f');      // from ?f=The+Siren
const bodyCode = ZX.qs('b');   // from ?b=ZX160J
```

---

### `ZX.ensureParams(paramMap)`

Validate and normalize URL parameters, redirecting if invalid.

**Signature:**
```javascript
ZX.ensureParams(paramMap: {[key]: string | string[]}) → boolean
```

**Example:**
```javascript
// Ensure 'f' is a valid family name
const valid = ZX.ensureParams({
  f: ZX.getFamilies().map(fam => fam.name)
});
if (!valid) window.location = '/family.html';  // Redirect if invalid
```

---

### `ZX.setParam(name, value)`

Update URL parameter (via history.replaceState; does NOT reload).

**Signature:**
```javascript
ZX.setParam(name: string, value: string) → void
```

**Example:**
```javascript
ZX.setParam('f', 'The Siren');
// URL changes from ?f=The+Muse to ?f=The+Siren (no reload)
```

---

### `ZX.navigate(path, params)`

Programmatic navigation.

**Signature:**
```javascript
ZX.navigate(path: string, params?: {[key]: string}) → void
```

**Example:**
```javascript
ZX.navigate('character.html', { id: 'SLE-ZX160J-03' });
// Navigates to character.html?id=SLE-ZX160J-03
```

---

## Analytics

### `ZX.track(eventName, payload)`

Fire an analytics event to GA4.

**Signature:**
```javascript
ZX.track(eventName: string, payload?: object) → void
```

**Example:**
```javascript
ZX.track('character_view', {
  character_id: 'SLE-ZX160J-03',
  family: 'The Siren',
  series: 'SLE'
});
```

**Event Aliases:**
Some events are canonicalized:
- `compare_add_from_body` → `compare_add`
- `compare_add_from_character` → `compare_add`
- `compare_to_contact_click` → `compare_handoff_click`

**Payload Normalization:**
- `body_codes` / `compare_codes` arrays are stringified as CSV.
- `message` field is renamed to `error_message` (for error events).
- Fields like `family`, `series`, `channel` are trimmed to strings.

---

### `ZX.getSessionId()`

Get or create a unique session ID.

**Signature:**
```javascript
ZX.getSessionId() → string
```

**Format:** `zx_{timestamp}_{random}` (e.g., `zx_1718980542_a1b2c3d4`)

**Persistence:** Stored in `sessionStorage` and `localStorage` with fallback.

**Example:**
```javascript
const sid = ZX.getSessionId();
ZX.track('page_view', { session_id: sid });
```

---

### `ZX.analyticsDebugEnabled()`

Check if analytics debug mode is enabled.

**Signature:**
```javascript
ZX.analyticsDebugEnabled() → boolean
```

**Toggle:** `?zx_analytics_debug=1` (URL param), persists to localStorage.

**Example:**
```javascript
if (ZX.analyticsDebugEnabled()) {
  console.log('Analytics events:', ZX.getDebugLog());
}
```

---

## Comparison Tool

### `ZX.getCompareBodies()`

Fetch the list of bodies currently in the comparison tool.

**Signature:**
```javascript
ZX.getCompareBodies() → string[]
```

**Returns:** Array of body codes (max 4 items).

**Storage:** `localStorage['zx_compare_bodies']`

---

### `ZX.addCompareBody(bodyCode)`

Add a body to the comparison list.

**Signature:**
```javascript
ZX.addCompareBody(bodyCode: string) → {added: boolean, bodies: string[]}
```

**Returns:**
```javascript
{
  added: true,  // or false if already in list or limit reached
  bodies: ['ZG170C', 'ZX160J', …]
}
```

**Limits:**
- Max 4 bodies.
- Duplicate body codes are rejected.
- Empty or invalid codes are filtered.

**Example:**
```javascript
const result = ZX.addCompareBody('ZX160J');
if (result.added) {
  console.log('Added. Now comparing:', result.bodies);
} else {
  console.log('Already in list or limit reached');
}
```

---

### `ZX.removeCompareBody(bodyCode)`

Remove a body from the comparison list.

**Signature:**
```javascript
ZX.removeCompareBody(bodyCode: string) → string[]
```

**Returns:** Updated array of body codes.

---

### `ZX.setCompareBodies(bodyCodes)`

Replace the entire comparison list.

**Signature:**
```javascript
ZX.setCompareBodies(bodyCodes: string[]) → string[]
```

**Example:**
```javascript
ZX.setCompareBodies(['ZG170C', 'ZX160J']);
// Clears previous list, sets to these 2
```

---

### `ZX.clearCompareBodies()`

Empty the comparison list.

**Signature:**
```javascript
ZX.clearCompareBodies() → void
```

---

## Quiz & Recommendation Engine

### `ZX.recommend(filters)`

Get character recommendations based on filters.

**Signature:**
```javascript
ZX.recommend(filters: {
  family?: string,
  series?: string,
  status?: 'live' | 'placeholder',
  limit?: number
}) → Character[]
```

**Example:**
```javascript
const recommendations = ZX.recommend({
  family: 'The Siren',
  series: 'SLE',
  limit: 10
});
console.log(recommendations.length);  // Up to 10 sirens in SLE
```

---

### `ZX.rankByFamily(characters, familyName)`

Sort characters by proximity to a family's WHR/BWR profile.

**Signature:**
```javascript
ZX.rankByFamily(characters: Character[], familyName: string) → Character[]
```

**Returns:** Same characters, sorted by morphometric similarity.

---

### `ZX.quizFlow(responses)`

Process quiz responses and return matching characters.

**Signature:**
```javascript
ZX.quizFlow(responses: {
  budget?: string,        // "budget" | "mid" | "luxury"
  style?: string,         // "natural" | "glamour" | "fantasy"
  height_pref?: string,   // "petite" | "tall" | "any"
  …more fields…
}) → Character[]
```

**Returns:** Ranked list of matching characters.

---

## Utility Helpers

### `ZX.escapeHtml(text)`

Escape HTML special characters (prevent XSS).

**Signature:**
```javascript
ZX.escapeHtml(text: string) → string
```

**Example:**
```javascript
const safe = ZX.escapeHtml('<script>alert("xss")</script>');
// Returns: &lt;script&gt;alert(&quot;xss&quot;)&lt;/script&gt;
```

---

### `ZX.familyColor(familyName)`

Get the CSS color variable for a family.

**Signature:**
```javascript
ZX.familyColor(familyName: string) → string
```

**Returns:** CSS variable name (e.g., `var(--Siren)`).

**Example:**
```javascript
const color = ZX.familyColor('The Siren');
element.style.borderColor = color;
```

---

### `ZX.familyClass(familyName)`

Get the CSS class name for a family.

**Signature:**
```javascript
ZX.familyClass(familyName: string) → string
```

**Returns:** Class name (e.g., `fam--siren`).

**Example:**
```javascript
const className = ZX.familyClass('The Siren');
element.classList.add(className);
```

---

### `ZX.heroImage(character)`

Get the best hero image for a character.

**Signature:**
```javascript
ZX.heroImage(character: Character) → string (URL)
```

**Logic:**
- If status = "live" → return `photoshoot.hero_thumb` or `photoshoot.hero`.
- If status = "placeholder" → return `placeholder.hero`.

---

### `ZX.formatPrice(price)`

Format a price string for display.

**Signature:**
```javascript
ZX.formatPrice(priceStr: string) → string
```

**Example:**
```javascript
ZX.formatPrice('2899.00')  // Returns: "$2,899.00"
```

---

### `ZX.pluralize(count, singular, plural)`

Pluralize text.

**Signature:**
```javascript
ZX.pluralize(count: number, singular: string, plural: string) → string
```

**Example:**
```javascript
ZX.pluralize(3, 'body', 'bodies')  // "3 bodies"
ZX.pluralize(1, 'body', 'bodies')  // "1 body"
```

---

## Events & Hooks

### Custom Events

Certain actions fire DOM events that other code can listen to:

```javascript
// When a character card is clicked
document.addEventListener('zx:character_selected', (e) => {
  console.log('Selected:', e.detail.character_id);
});

// When comparison list changes
document.addEventListener('zx:compare_changed', (e) => {
  console.log('New list:', e.detail.bodies);
});

// When quiz is completed
document.addEventListener('zx:quiz_complete', (e) => {
  console.log('Results:', e.detail.matches);
});
```

---

### Performance Hooks

**Lazy Loading:**
All images use the `loading="lazy"` attribute; no manual lazy-load library.

**Debouncing:**
Filter and sort operations are debounced to 300ms.

**Caching:**
- Catalog is cached in memory after first load.
- Recommendation results are cached per filter set.

---

## Error Handling

### Network Errors

If a data file fails to load:

```javascript
ZX.load().catch(err => {
  console.error('Failed to load catalog:', err);
  // Fallback UI
});
```

### Invalid Parameters

Navigation methods validate inputs:

```javascript
const valid = ZX.qs('family') in ['The Classic', 'The Icon', …];
if (!valid) {
  console.warn('Invalid family parameter');
  ZX.navigate('family.html');  // Reset to default
}
```

### Storage Limits

LocalStorage operations are wrapped in try-catch:

```javascript
try {
  localStorage.setItem('zx_compare_bodies', JSON.stringify(bodies));
} catch (e) {
  console.warn('localStorage unavailable; using session only');
}
```

---

## Configuration

### Edit These Values in `assets/site.js`

```javascript
const INQUIRY_EMAIL = 'inquiries@zelexdoll.com';  // Change before launch
const FORM_ENDPOINT = '';                         // Optional Formspree/Getform URL
const ANALYTICS_SCHEMA_VERSION = '2026-06-06';
const ANALYTICS_SESSION_KEY = 'zx_analytics_session_id';
const ANALYTICS_DEBUG_KEY = 'zx_analytics_debug';
```

---

## Examples

### Load and Display All Characters

```javascript
ZX.load().then(model => {
  const allCharacters = model.characters;
  const html = allCharacters
    .map(c => ZX.renderCharacterCard(c))
    .join('');
  document.querySelector('#gallery').innerHTML = html;
});
```

### Filter by Family and Track Event

```javascript
ZX.load().then(model => {
  const family = ZX.qs('f') || 'The Siren';
  const matches = ZX.getCharactersByFamily(family);
  
  ZX.track('family_view', {
    family: family,
    character_count: matches.length,
    session_id: ZX.getSessionId()
  });
  
  // Render matches
  matches.forEach(c => {
    // Render…
  });
});
```

### Compare Tool Flow

```javascript
function addToComparison(bodyCode) {
  const result = ZX.addCompareBody(bodyCode);
  if (result.added) {
    ZX.track('compare_add', {
      body_code: bodyCode,
      compare_count: result.bodies.length
    });
    updateComparisonUI();
  }
}

function updateComparisonUI() {
  const bodies = ZX.getCompareBodies();
  document.querySelector('#compare-pane').innerHTML = 
    ZX.renderComparison(bodies);
}
```

---

See [ARCHITECTURE.md](ARCHITECTURE.md) and [DATA-SCHEMA.md](DATA-SCHEMA.md) for context.
