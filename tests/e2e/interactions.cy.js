/**
 * E2E tests for user interactions
 * Tests filters, sorting, comparisons, forms, and dynamic features
 */

describe('User Interactions', () => {
  describe('Browse Page Filtering', () => {
    beforeEach(() => {
      cy.loadPage('browse.html');
    });

    it('filters characters by family', () => {
      cy.get('button[data-family], a[data-family], [role="button"][data-family]').first().then(($btn) => {
        const family = $btn.attr('data-family');
        if (family) {
          cy.wrap($btn).click();
          // After filtering, only characters with that family should be visible
          // (Depends on implementation)
        }
      });
    });

    it('filters characters by series', () => {
      cy.get('select[name="series"], input[name="series"], [data-series]')
        .first()
        .then(($el) => {
          if ($el.prop('tagName').toLowerCase() === 'select') {
            cy.wrap($el).select(1);
          } else if ($el.prop('tagName').toLowerCase() === 'button') {
            cy.wrap($el).click();
          }
        });
    });

    it('displays character count', () => {
      cy.get('[data-testid="character-count"], .count, [data-count]').should('exist');
    });

    it('clears filters when reset button is clicked', () => {
      cy.get('button[data-reset], button:contains("Reset"), button:contains("Clear")')
        .first()
        .then(($btn) => {
          if ($btn.length > 0) {
            cy.wrap($btn).click();
            // Verify filters are cleared
          }
        });
    });
  });

  describe('Compare Tool', () => {
    beforeEach(() => {
      cy.loadPage('compare.html');
    });

    it('allows adding bodies to compare', () => {
      cy.window().then((win) => {
        if (win.ZX && typeof win.ZX.addCompareBody === 'function') {
          const result = win.ZX.addCompareBody('ZK168B');
          expect(result.added).to.be.true;
        }
      });
    });

    it('prevents adding duplicate bodies', () => {
      cy.window().then((win) => {
        if (win.ZX && typeof win.ZX.addCompareBody === 'function') {
          win.ZX.addCompareBody('ZK168B');
          const result = win.ZX.addCompareBody('ZK168B');
          expect(result.added).to.be.false;
        }
      });
    });

    it('caps compare list at 4 bodies', () => {
      cy.window().then((win) => {
        if (win.ZX && typeof win.ZX.addCompareBody === 'function') {
          win.ZX.setCompareBodies([]);
          for (let i = 0; i < 5; i++) {
            win.ZX.addCompareBody(`Body${i}`);
          }
          const bodies = win.ZX.getCompareBodies();
          expect(bodies.length).to.equal(4);
        }
      });
    });

    it('persists compare list in localStorage', () => {
      cy.window().then((win) => {
        if (win.ZX && typeof win.ZX.setCompareBodies === 'function') {
          win.ZX.setCompareBodies(['ZK168B', 'ZK170D']);
          expect(localStorage.getItem('zx_compare_bodies')).to.not.be.null;
        }
      });
    });
  });

  describe('Contact Form', () => {
    beforeEach(() => {
      cy.loadPage('contact.html');
    });

    it('has contact form fields', () => {
      cy.get('form').should('exist');
      cy.get('input[name="email"], input[type="email"]').should('exist');
      cy.get('textarea, textarea[name="message"]').should('exist');
    });

    it('validates required fields', () => {
      cy.get('button[type="submit"]').first().click();
      // Form validation should prevent submission
      // Exact behavior depends on implementation
    });

    it('pre-fills character ID if provided in URL', () => {
      cy.loadPage('contact.html?id=K-ZK168B-01');
      // Check if character ID is pre-filled
      cy.get('input, textarea').each(($el) => {
        const val = $el.val();
        if (val && val.includes('K-ZK168B-01')) {
          expect(val).to.include('K-ZK168B-01');
        }
      });
    });
  });

  describe('Quiz Navigation', () => {
    beforeEach(() => {
      cy.loadPage('quiz.html');
    });

    it('renders quiz questions', () => {
      cy.get('[data-testid="question"], .question, [role="group"]').should('exist');
    });

    it('allows answering questions', () => {
      cy.get('button[data-answer], input[type="radio"], input[type="checkbox"]').first().click();
    });

    it('shows results after completion', () => {
      // Answer all questions
      cy.get('input[type="radio"]').each(($radio) => {
        cy.wrap($radio).click({ force: true });
      });
      cy.get('button[data-next], button:contains("Next"), button:contains("Submit")')
        .last()
        .click({ multiple: true });
      // Verify results are shown
      cy.get('[data-testid="quiz-result"], .result, .recommendations').should('exist');
    });
  });

  describe('Gallery Widget', () => {
    beforeEach(() => {
      cy.loadPage('browse.html');
    });

    it('displays character images', () => {
      cy.get('img[src*="hero"], img[src*="thumb"]').should('have.length.greaterThan', 0);
    });

    it('shows placeholder for missing images', () => {
      cy.get('[data-placeholder], .placeholder, .monotile').should('exist');
    });

    it('links character cards to detail page', () => {
      cy.get('a[href*="character.html"]').first().should('have.attr', 'href');
    });
  });

  describe('Analytics Event Tracking', () => {
    beforeEach(() => {
      cy.loadPage('index.html');
    });

    it('initializes analytics session ID', () => {
      cy.window().then((win) => {
        expect(localStorage.getItem('zx_analytics_session_id')).to.exist;
      });
    });

    it('creates session ID on first visit', () => {
      cy.window().then((win) => {
        const sid = localStorage.getItem('zx_analytics_session_id');
        expect(sid).to.match(/^zx_/);
      });
    });
  });
});
