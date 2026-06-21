/**
 * axe-core accessibility audit configuration
 * Run: npx axe-core <url>
 * Or integrate with Cypress: cy.injectAxe(); cy.checkA11y();
 */

export const axeConfig = {
  standard: 'wcag2aa',
  rules: {
    'color-contrast': { enabled: true },
    'image-alt': { enabled: true },
    'label': { enabled: true },
    'button-name': { enabled: true },
    'link-name': { enabled: true },
    'heading-order': { enabled: true },
    'region': { enabled: true },
    'bypass': { enabled: true },
    'html-lang': { enabled: true },
    'meta-viewport': { enabled: true },
    'form-field-multiple-labels': { enabled: true },
    'duplicate-id': { enabled: true },
    'aria-valid-attr': { enabled: true },
    'aria-roles': { enabled: true },
  },
  checks: [
    'aria-required-attr',
    'aria-required-children',
    'aria-required-parent',
    'aria-valid-attr-value',
    'button-has-visible-text',
    'color-contrast',
    'definition-list',
    'duplicate-attr',
    'empty-heading',
    'heading-order',
    'image-alt',
    'label-title-only',
    'link-name',
  ],
};

export const reportConfig = {
  outputFormat: 'json',
  outputPath: '.artifacts/a11y-report.json',
  verbose: true,
};
