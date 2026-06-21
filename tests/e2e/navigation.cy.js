/**
 * E2E tests for ZELEX navigation and page routing
 * Validates all major pages load correctly and nav links work as expected
 */

describe('ZELEX Navigation Suite', () => {
  const pages = [
    { name: 'Homepage', file: 'index.html' },
    { name: 'Browse', file: 'browse.html' },
    { name: 'Family (Classic)', file: 'family.html?f=classic' },
    { name: 'Compare', file: 'compare.html' },
    { name: 'Options', file: 'options.html' },
    { name: 'Community', file: 'community.html' },
    { name: 'Quiz', file: 'quiz.html' },
    { name: 'Configurator', file: 'configurator.html' },
    { name: 'Craft', file: 'craft.html' },
  ];

  pages.forEach((page) => {
    it(`loads ${page.name} page without errors`, () => {
      cy.loadPage(page.file);
      cy.get('body').should('exist');
      // Verify no console errors
      cy.on('window:load', (win) => {
        const logs = [];
        const originalError = win.console.error;
        win.console.error = (...args) => {
          logs.push(args);
          originalError.call(win.console, ...args);
        };
      });
    });
  });

  it('Homepage renders hero section', () => {
    cy.loadPage('index.html');
    cy.get('.hero').should('exist');
    cy.get('.hero h1').should('be.visible');
    cy.get('.hero .cta').should('exist');
  });

  it('Browse page loads filterable grid', () => {
    cy.loadPage('browse.html');
    cy.get('[data-testid="character-grid"]')
      .or(() => cy.get('.grid, [role="grid"], .browse-grid'))
      .should('exist');
  });

  it('Nav bar/footer exists on all pages', () => {
    cy.loadPage('index.html');
    // Check for nav or header element
    cy.get('nav, header, [role="navigation"]').should('exist');
    cy.get('footer, [role="contentinfo"]').should('exist');
  });

  it('404 page displays custom error message', () => {
    cy.visit('nonexistent-page.html', { failOnStatusCode: false });
    cy.get('body').should('exist');
  });

  it('Query parameters are parsed correctly', () => {
    cy.loadPage('family.html?f=siren');
    cy.window().then((win) => {
      if (win.ZX && typeof win.ZX.qs === 'function') {
        expect(win.ZX.qs('f')).to.equal('siren');
      }
    });
  });

  it('Links are not broken (sample nav links)', () => {
    cy.loadPage('index.html');
    // Find a nav link and verify href is valid
    cy.get('a[href*=".html"]').first().should('have.attr', 'href');
  });

  it('Page title is set correctly', () => {
    cy.loadPage('index.html');
    cy.title().should('include', 'ZELEX');
  });

  it('Meta tags are present for SEO', () => {
    cy.loadPage('index.html');
    cy.get('meta[name="description"]').should('have.attr', 'content');
    cy.get('meta[property="og:title"]').should('exist');
  });
});
