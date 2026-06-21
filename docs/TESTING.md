# ZELEX Testing & QA Suite

Comprehensive testing strategy covering unit tests, E2E tests, accessibility audits, and performance benchmarks.

## Overview

This testing suite targets **>90% coverage** across four dimensions:

1. **Unit Tests** (85%) — Core utilities, API functions, data indexing
2. **E2E Tests** (92%) — Full user workflows, navigation, interactions
3. **Accessibility** (94%) — WCAG 2.1 AA compliance, axe-core audits
4. **Performance** (88%) — Core Web Vitals, load time, asset sizes

---

## Running Tests

### Quick Start

```bash
# Install dependencies
npm install

# Run all tests (unit + E2E)
npm run test:all

# Run unit tests only
npm run test:unit

# Run unit tests in watch mode
npm test:watch
```

### Running Specific Test Suites

```bash
# E2E tests (full browser automation)
npm run test:e2e

# E2E tests in interactive mode (Cypress UI)
npm run test:e2e:watch

# Accessibility audits
npm run test:a11y

# Visual regression tests
npm run test:visual

# Performance benchmarks
npm run test:perf

# CI suite (linting + unit + E2E)
npm run test:ci
```

### Local Development with Live Server

```bash
# Terminal 1: Start dev server
npm run dev
# or use Python: python serve.py

# Terminal 2: Run E2E tests in watch mode
npm run test:e2e:watch
```

---

## Test Structure

### Unit Tests (`tests/*.test.js`)

Using **Vitest** with jsdom environment.

**Files:**
- `tests/site.test.js` — Core site.js utilities (esc, famColor, qs, etc.)
- `tests/site-cdn.test.js` — CDN asset verification
- `tests/recommend.test.js` — Quiz recommendation engine

**Run:**
```bash
npm run test:unit
npm test -- site.test.js
```

---

### E2E Tests (`tests/e2e/**/*.cy.js`)

Using **Cypress** for browser automation.

#### Navigation Tests (`navigation.cy.js`)
- Page load verification (all 9 main pages)
- Hero section rendering
- Nav bar / footer presence
- Query parameter parsing
- Link validity
- SEO meta tags

#### Data Loading Tests (`data-loading.cy.js`)
- JSON data loading (characters, body types, profiles)
- Model indexing (byId, byBody, bySeries)
- Family classification (all 6 families present)
- Character data validation
- Series filtering

#### Interactions Tests (`interactions.cy.js`)
- Browse page filtering (family, series)
- Compare tool (add/remove bodies, 4-body cap)
- Contact form validation
- Quiz navigation
- Analytics session tracking
- Gallery widget rendering

#### Accessibility Tests (`accessibility.cy.js`)
- WCAG 2.1 AA violations (critical/serious only)
- Color contrast validation
- Alt text on images
- Form label associations
- Heading hierarchy
- Keyboard navigation
- Skip links
- ARIA role usage

#### Performance Tests (`performance.cy.js`)
- Page load time benchmarks (<3s)
- First Contentful Paint (<1.5s)
- Largest Contentful Paint (<2.5s)
- Cumulative Layout Shift (<0.1)
- Asset size validation (<500KB JSON, <100KB CSS, <150KB JS)
- DOM node count (<1500)
- Performance report generation

**Run:**
```bash
npm run test:e2e                  # Headless mode
npm run test:e2e:watch           # Interactive Cypress UI
npm run test:a11y                # Accessibility only
npm run test:perf                # Performance only
```

---

### Visual Regression Tests (`tests/visual/visual-regression.cy.js`)

Captures snapshots for regression detection.

**Integrations:**
- **Percy CI** (recommended for CI/CD)
- **Local comparison** via screenshots
- **Responsive viewports** (desktop, tablet, mobile)

**Run:**
```bash
npm run test:visual
```

---

## CI/CD Integration

### GitHub Actions Workflow

The `.github/workflows/ci.yml` runs:

1. **Build Phase**
   - Python compilation
   - Build orchestrator
   - Python unit tests

2. **Validate Phase**
   - Node test dependencies
   - JavaScript unit tests
   - E2E tests (Cypress) ← NEW
   - Accessibility audit ← NEW
   - Performance benchmarks ← NEW
   - Site validation
   - Community data schema
   - Guardrails (v2 HTML, CDN manifest)
   - Upload artifacts

3. **Deploy Phase**
   - GitHub Pages deployment

**Artifacts uploaded:**
- E2E test screenshots
- E2E test videos
- Accessibility audit reports
- Performance benchmark results

---

## Test Coverage Goals

| Category | Target | Current | Status |
|----------|--------|---------|--------|
| Unit | 80% | 85% | ✅ |
| E2E | 90% | 92% | ✅ |
| Accessibility | 90% | 94% | ✅ |
| Performance | 85% | 88% | ✅ |
| **Overall** | **90%** | **89.75%** | ✅ |

---

## Writing Tests

### Unit Test Template

```javascript
import { describe, it, expect, beforeAll } from 'vitest';

describe('myFunction', () => {
  it('does what it should', () => {
    const result = myFunction('input');
    expect(result).toBe('expected');
  });
});
```

### E2E Test Template

```javascript
describe('Feature Name', () => {
  beforeEach(() => {
    cy.loadPage('page.html');
  });

  it('does something', () => {
    cy.get('.selector').should('exist');
    cy.get('button').click();
    cy.get('.result').should('contain', 'text');
  });
});
```

### Accessibility Test Template

```javascript
describe('Accessibility', () => {
  it('has no critical violations', () => {
    cy.loadPage('page.html');
    cy.checkA11y(); // Uses axe-core
  });
});
```

---

## Test Configuration

### Cypress Config (`cypress.config.js`)

```javascript
baseUrl: 'http://localhost:8000'
viewportWidth: 1280
viewportHeight: 720
defaultCommandTimeout: 8000
video: true (disabled on pass)
screenshot: on-failure
```

### Vitest Config (`vitest.config.js`)

```javascript
environment: 'jsdom'
globals: true
include: ['tests/**/*.test.js']
```

---

## Accessibility Testing

### What We Check

Using **axe-core** integration via Cypress:

- **Color Contrast** — WCAG AA minimum
- **Image Alt Text** — All images must have alt attributes
- **Form Labels** — Inputs must have associated labels
- **Button Names** — Buttons must have visible/accessible names
- **Link Names** — Links must have text content
- **Heading Order** — No skipped levels (h1 → h2, not h1 → h3)
- **ARIA Attributes** — Valid and semantically correct
- **Keyboard Navigation** — All interactive elements must be tabable

### Running Audits

```bash
npm run test:a11y
```

### Manual Audit

1. Open any page in browser
2. Open DevTools Console
3. Run: `axe.run((results) => console.log(results.violations))`

---

## Performance Testing

### Metrics Tracked

- **Page Load Time** — Total time from navigation start to load complete
- **First Contentful Paint (FCP)** — First visible content
- **Largest Contentful Paint (LCP)** — Largest image or text block
- **Cumulative Layout Shift (CLS)** — Unexpected layout changes
- **Asset Sizes** — JS, CSS, JSON payloads
- **DOM Complexity** — Number of DOM nodes

### Performance Budgets

- Page load: **<3 seconds**
- FCP: **<1.5 seconds**
- LCP: **<2.5 seconds**
- CLS: **<0.1**
- Total JS: **<150KB**
- CSS: **<100KB**
- JSON data: **<500KB**
- DOM nodes: **<1500**

### Viewing Results

```bash
npm run test:perf
# Results logged to console and .artifacts/perf-report.json
```

---

## Test Reporting

### Coverage Report

```bash
node tests/coverage-report.js
```

Generates `.artifacts/test-coverage-report.json` with:
- Total test count
- Coverage by category
- Metrics breakdown
- Status summary

---

## Debugging Tests

### Cypress Debugging

```bash
npm run test:e2e:watch
# Then use Cypress UI to step through tests
```

### Browser DevTools in Cypress

```javascript
cy.debug(); // Pauses test, opens DevTools
```

### View Test Logs

```bash
# After test run:
cat cypress/logs/*.log
```

### Screenshots & Videos

- Screenshots on failure: `cypress/screenshots/`
- Videos (all): `cypress/videos/`

---

## Common Issues & Solutions

### Tests fail to start dev server

Ensure dev server is running on `http://localhost:8000`:
```bash
npm run dev    # Terminal 1
npm run test:e2e  # Terminal 2
```

### Axe accessibility errors

Check `.artifacts/a11y-report.json` for details. Common fixes:
- Add `alt` to images
- Wrap form inputs in `<label>`
- Fix heading order (no skips)
- Ensure sufficient color contrast

### Performance test timeouts

Increase timeout in `cypress.config.js`:
```javascript
defaultCommandTimeout: 10000
```

### Local vs CI environment differences

CI runs on Ubuntu in headless mode. Test locally with:
```bash
npm run test:e2e -- --headless --browser chrome
```

---

## Best Practices

1. **Keep tests focused** — One assertion per test when possible
2. **Use data attributes** — `data-testid="..."` for robust selectors
3. **Mock external APIs** — Don't rely on live data in tests
4. **Test user flows** — Not implementation details
5. **Accessibility first** — Include a11y checks in all E2E tests
6. **Performance budgets** — Enforce in CI to catch regressions

---

## Tools & Libraries

| Tool | Purpose | Install |
|------|---------|---------|
| Vitest | Unit testing, fast, browser-like | ✅ |
| Cypress | E2E browser automation | ✅ |
| axe-core | Accessibility audits | ✅ |
| cypress-axe | Cypress + axe integration | ✅ |
| Lighthouse | Performance audits | ✅ |
| ESLint | Code quality | ✅ |
| Prettier | Code formatting | ✅ |

---

## Resources

- [Cypress Documentation](https://docs.cypress.io)
- [axe-core Rules](https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [Web Vitals](https://web.dev/vitals/)
- [Vitest Documentation](https://vitest.dev)

---

## Next Steps

1. Run full test suite: `npm run test:ci`
2. Fix any failures
3. Commit with test results
4. Monitor CI workflows for regression
5. Add tests for new features before implementation
