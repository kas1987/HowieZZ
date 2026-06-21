# Testing Quick Start

## Installation

```bash
npm install
npm install --save-dev cypress cypress-axe axe-core lighthouse
```

## Run Tests

### All Tests
```bash
npm run test:all
```

### By Category

```bash
# Unit tests (Vitest)
npm run test:unit
npm test:watch

# E2E tests (Cypress) — requires dev server running
npm run test:e2e
npm run test:e2e:watch  # Interactive UI

# Accessibility
npm run test:a11y

# Performance
npm run test:perf

# Visual regression
npm run test:visual
```

## Local Development Workflow

### Terminal 1: Start Dev Server
```bash
npm run dev
# or: python serve.py
# Serves on http://localhost:8000
```

### Terminal 2: Run Tests
```bash
# Watch mode for development
npm run test:e2e:watch

# Or run specific test file
npm run test:e2e -- tests/e2e/navigation.cy.js
```

## CI/CD

Tests run automatically on push to main via `.github/workflows/ci.yml`:

1. Python build + unit tests
2. JavaScript unit tests
3. E2E tests (Cypress)
4. Accessibility audit
5. Performance benchmarks
6. Site validation
7. Deploy to GitHub Pages (if all pass)

## File Structure

```
tests/
├── site.test.js                 # Unit tests
├── recommend.test.js            # API tests
├── coverage-report.js           # Coverage generator
├── axe-config.js                # A11y configuration
├── test-config.json             # Test metadata
├── e2e/
│   ├── support/
│   │   └── e2e.js               # Cypress helpers
│   ├── navigation.cy.js         # Page load tests
│   ├── data-loading.cy.js       # Model indexing tests
│   ├── interactions.cy.js       # User interaction tests
│   ├── accessibility.cy.js      # WCAG 2.1 AA
│   └── performance.cy.js        # Core Web Vitals
└── visual/
    └── visual-regression.cy.js  # Screenshot tests

docs/
└── TESTING.md                   # Full documentation

scripts/
└── lighthouse-audit.js          # Performance audits
```

## Test Coverage Target: 90%

| Area | Target | Status |
|------|--------|--------|
| Unit | 85% | ✅ |
| E2E | 92% | ✅ |
| Accessibility | 94% | ✅ |
| Performance | 88% | ✅ |
| **Overall** | **90%** | ✅ |

## Key Commands

```bash
# Development
npm run dev                 # Start local server
npm test:watch            # Unit tests in watch mode
npm run test:e2e:watch    # E2E tests in Cypress UI

# CI/CD
npm run test:ci           # Full CI suite (unit + lint + E2E)

# Analysis
node tests/coverage-report.js              # Generate coverage report
node scripts/lighthouse-audit.js           # Run Lighthouse audits
npm run lint              # ESLint
npm run format            # Prettier

# Testing specific areas
npm run test:a11y         # Accessibility only
npm run test:perf         # Performance only
npm run test:visual       # Visual regression
```

## Common Issues

### Dev server not found
```bash
# Make sure server is running
npm run dev
# Check it's on http://localhost:8000
```

### Cypress hangs
```bash
# Kill any existing Cypress processes
pkill -f cypress
# Try again
npm run test:e2e:watch
```

### Accessibility violations
```bash
# Check detailed report
cat .artifacts/a11y-report.json
```

## Next Steps

1. Run full test suite: `npm run test:ci`
2. Start dev server: `npm run dev`
3. Open test UI: `npm run test:e2e:watch`
4. Explore tests in Cypress Test Runner
5. Add tests for new features

See [docs/TESTING.md](docs/TESTING.md) for full documentation.
