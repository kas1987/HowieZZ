import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    environment: 'jsdom',
    include: ['tests/js/**/*.test.js'],
    coverage: {
      provider: 'v8',
      include: ['assets/site.js'],
      reporter: ['text', 'text-summary'],
      thresholds: {
        lines: 50,
        functions: 50,
        statements: 50,
      },
    },
  },
});
