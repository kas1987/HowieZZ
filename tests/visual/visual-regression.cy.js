/**
 * Visual regression tests
 * Captures snapshots of key pages for visual regression detection
 * Can integrate with Percy CI or use local screenshot comparison
 */

describe('Visual Regression Tests', () => {
  const pages = [
    { name: 'homepage', file: 'index.html', viewport: [1280, 720] },
    { name: 'homepage-mobile', file: 'index.html', viewport: [375, 667] },
    { name: 'browse', file: 'browse.html', viewport: [1280, 1080] },
    { name: 'family', file: 'family.html?f=classic', viewport: [1280, 800] },
    { name: 'compare', file: 'compare.html', viewport: [1280, 900] },
    { name: 'quiz', file: 'quiz.html', viewport: [1280, 800] },
    { name: 'contact', file: 'contact.html', viewport: [1280, 800] },
  ];

  pages.forEach(({ name, file, viewport }) => {
    it(`visual snapshot: ${name}`, () => {
      cy.viewport(viewport[0], viewport[1]);
      cy.loadPage(file);
      // Wait for all images to load
      cy.get('img').each(($img) => {
        cy.wrap($img).should('have.css', 'display').and('not.equal', 'none');
      });
      cy.wait(500); // Wait for animations/fonts to settle
      // Take snapshot (integrates with Percy or local comparison)
      cy.percySnapshot(name) || cy.screenshot(name);
    });
  });

  it('hero section renders correctly', () => {
    cy.loadPage('index.html');
    cy.get('.hero').should('exist').and('be.visible');
    cy.percySnapshot('hero') || cy.screenshot('hero');
  });

  it('character grid renders consistently', () => {
    cy.loadPage('browse.html');
    cy.get('.grid, [role="grid"], .browse-grid').should('exist');
    cy.percySnapshot('character-grid') || cy.screenshot('character-grid');
  });

  it('responsive design: mobile view', () => {
    cy.viewport('iphone-x');
    cy.loadPage('index.html');
    cy.get('.hero').should('be.visible');
    cy.percySnapshot('mobile-homepage') || cy.screenshot('mobile-homepage');
  });

  it('responsive design: tablet view', () => {
    cy.viewport('ipad-2');
    cy.loadPage('browse.html');
    cy.percySnapshot('tablet-browse') || cy.screenshot('tablet-browse');
  });

  it('dark mode rendering (if supported)', () => {
    cy.loadPage('index.html');
    cy.window().then((win) => {
      if (win.matchMedia && win.matchMedia('(prefers-color-scheme: dark)').matches) {
        cy.percySnapshot('dark-mode-homepage') || cy.screenshot('dark-mode-homepage');
      }
    });
  });

  it('font rendering consistency', () => {
    cy.loadPage('index.html');
    cy.get('h1, h2, p').should('exist');
    cy.percySnapshot('typography') || cy.screenshot('typography');
  });
});
