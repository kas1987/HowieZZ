// Support file for E2E tests
// Runs before each spec file

// Add custom commands here
Cypress.Commands.add('loadPage', (page = 'index.html') => {
  cy.visit(page);
  // Wait for ZX.load() to complete
  cy.window().then((win) => {
    if (win.ZX && typeof win.ZX.load === 'function') {
      return cy.wrap(win.ZX.load());
    }
  });
});

Cypress.Commands.add('checkA11y', () => {
  cy.injectAxe();
  cy.checkA11y(null, { includedImpacts: ['critical', 'serious'] });
});

Cypress.Commands.add('pageLoadTime', () => {
  return cy.window().then((win) => {
    if (win.performance && win.performance.timing) {
      const timing = win.performance.timing;
      const navigationStart = timing.navigationStart;
      const loadEventEnd = timing.loadEventEnd;
      return loadEventEnd - navigationStart;
    }
    return null;
  });
});
