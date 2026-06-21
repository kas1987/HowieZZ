import { defineConfig } from 'cypress';

export default defineConfig({
  e2e: {
    baseUrl: 'http://localhost:8000',
    specPattern: 'tests/e2e/**/*.cy.js',
    supportFile: 'tests/e2e/support/e2e.js',
    video: true,
    videoUploadOnPasses: false,
    screenshotOnRunFailure: true,
    viewportWidth: 1280,
    viewportHeight: 720,
    defaultCommandTimeout: 8000,
    requestTimeout: 8000,
  },
  component: {
    devServer: {
      framework: 'webpack',
      bundler: 'webpack',
    },
    supportFile: 'tests/component/support/component.js',
    specPattern: 'tests/component/**/*.cy.js',
  },
});
