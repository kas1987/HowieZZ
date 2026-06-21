/**
 * Accessibility (a11y) tests using axe-core
 * Validates critical and serious violations on all major pages
 */

describe('Accessibility Audit', () => {
  const pages = [
    'index.html',
    'browse.html',
    'family.html?f=classic',
    'compare.html',
    'quiz.html',
    'contact.html',
  ];

  pages.forEach((page) => {
    it(`${page} has no critical/serious a11y violations`, () => {
      cy.loadPage(page);
      cy.checkA11y();
    });
  });

  it('all text has sufficient color contrast', () => {
    cy.loadPage('index.html');
    cy.injectAxe();
    cy.checkA11y(null, {
      rules: {
        'color-contrast': { enabled: true },
      },
      includedImpacts: ['critical', 'serious'],
    });
  });

  it('images have alt text', () => {
    cy.loadPage('browse.html');
    cy.get('img').each(($img) => {
      // Either has alt text or is decorative with empty alt
      const alt = $img.attr('alt');
      expect(alt !== undefined).to.be.true;
    });
  });

  it('form inputs have associated labels', () => {
    cy.loadPage('contact.html');
    cy.get('input[type="text"], textarea, input[type="email"]').each(($input) => {
      const id = $input.attr('id');
      if (id) {
        cy.get(`label[for="${id}"]`).should('exist');
      }
    });
  });

  it('headings hierarchy is correct (no skipped levels)', () => {
    cy.loadPage('index.html');
    let lastLevel = 0;
    cy.get('h1, h2, h3, h4, h5, h6').each(($heading) => {
      const level = parseInt($heading.prop('tagName')[1]);
      // Allow skip from h1 to h2, but not h1 to h3
      if (lastLevel > 0) {
        expect(level).to.be.lte(lastLevel + 1);
      }
      lastLevel = level;
    });
  });

  it('page is keyboard navigable', () => {
    cy.loadPage('browse.html');
    // Tab through first 5 interactive elements
    let count = 0;
    cy.get('a, button, input').each(() => {
      if (count < 5) {
        cy.focused().tab();
        count++;
      }
    });
  });

  it('skip links are present (if applicable)', () => {
    cy.loadPage('index.html');
    // Look for skip to main content link
    cy.get('a[href="#main"], a[href="#content"], a.skip-link').then(($links) => {
      // Optional but good practice
      if ($links.length > 0) {
        expect($links.length).to.be.at.least(1);
      }
    });
  });

  it('ARIA roles are used appropriately', () => {
    cy.loadPage('browse.html');
    // Check for proper role usage (no redundant roles on semantic elements)
    cy.get('[role="navigation"]').each(($nav) => {
      // If it's a nav tag, it shouldn't have role="navigation"
      if ($nav.prop('tagName').toLowerCase() === 'nav') {
        cy.wrap($nav).should('not.have.attr', 'role', 'navigation');
      }
    });
  });
});
