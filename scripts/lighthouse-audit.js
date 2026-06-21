#!/usr/bin/env node

/**
 * Lighthouse CI audit runner
 * Generates performance, accessibility, and best practices reports
 * Run: node scripts/lighthouse-audit.js
 */

import lighthouse from 'lighthouse';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PROJECT_ROOT = path.resolve(__dirname, '..');
const ARTIFACTS_DIR = path.join(PROJECT_ROOT, '.artifacts');

const pages = [
  'http://localhost:8000/index.html',
  'http://localhost:8000/browse.html',
  'http://localhost:8000/family.html?f=classic',
  'http://localhost:8000/compare.html',
];

const lighthouseConfig = {
  logLevel: 'info',
  output: 'json',
  onlyCategories: ['performance', 'accessibility', 'best-practices', 'seo'],
  emulatedFormFactor: 'desktop',
};

async function runAudit(url) {
  console.log(`\n🔍 Auditing: ${url}`);
  try {
    const runnerResult = await lighthouse(url, lighthouseConfig);
    const categories = runnerResult.lhr.categories;

    const results = {
      url,
      timestamp: new Date().toISOString(),
      categories: {},
    };

    Object.entries(categories).forEach(([name, category]) => {
      results.categories[name] = {
        score: Math.round(category.score * 100),
        title: category.title,
      };
    });

    // Performance metrics
    if (runnerResult.lhr.audits) {
      const audits = runnerResult.lhr.audits;
      results.metrics = {
        first_contentful_paint: audits['first-contentful-paint']?.numericValue,
        largest_contentful_paint: audits['largest-contentful-paint']?.numericValue,
        cumulative_layout_shift: audits['cumulative-layout-shift']?.numericValue,
        total_blocking_time: audits['total-blocking-time']?.numericValue,
      };
    }

    return results;
  } catch (e) {
    console.error(`❌ Failed to audit ${url}:`, e.message);
    return null;
  }
}

async function main() {
  if (!fs.existsSync(ARTIFACTS_DIR)) {
    fs.mkdirSync(ARTIFACTS_DIR, { recursive: true });
  }

  console.log('🏃 Running Lighthouse audits...');
  console.log(`📍 Base URL: http://localhost:8000`);

  const allResults = {
    timestamp: new Date().toISOString(),
    pages: [],
    summary: {},
  };

  for (const page of pages) {
    const result = await runAudit(page);
    if (result) {
      allResults.pages.push(result);
    }
  }

  // Calculate summary
  if (allResults.pages.length > 0) {
    const categories = ['performance', 'accessibility', 'best-practices', 'seo'];
    const summary = {};

    categories.forEach((cat) => {
      const scores = allResults.pages
        .map((p) => p.categories[cat]?.score)
        .filter((s) => s !== undefined);
      if (scores.length > 0) {
        const avg = Math.round(scores.reduce((a, b) => a + b, 0) / scores.length);
        summary[cat] = {
          average: avg,
          min: Math.min(...scores),
          max: Math.max(...scores),
        };
      }
    });

    allResults.summary = summary;
  }

  // Write results
  const reportPath = path.join(ARTIFACTS_DIR, 'lighthouse-audit.json');
  fs.writeFileSync(reportPath, JSON.stringify(allResults, null, 2));

  // Output summary
  console.log('\n' + '═'.repeat(70));
  console.log('📊 LIGHTHOUSE AUDIT SUMMARY');
  console.log('═'.repeat(70));

  Object.entries(allResults.summary).forEach(([category, scores]) => {
    console.log(`\n${category.toUpperCase()}`);
    console.log(`  Average: ${scores.average}`);
    console.log(`  Range: ${scores.min} - ${scores.max}`);
  });

  console.log(`\n✅ Report saved to: ${reportPath}\n`);
}

main().catch(console.error);
