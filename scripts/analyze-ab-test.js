#!/usr/bin/env node

/**
 * ZELEX A/B Test Analysis
 *
 * Fetch event data from /api/track and compute:
 * - Conversion rate by variant
 * - Statistical significance
 * - Family distribution
 * - Measurement alignment metrics
 *
 * Usage: npm run analyze:ab [--days=7] [--variant=control|treatment|both]
 */

import fs from 'fs';
import path from 'path';

// Parse CLI arguments
const args = process.argv.slice(2);
const options = {
  days: 7,
  variant: 'both',
  outputFormat: 'console' // console, json, html
};

args.forEach(arg => {
  if (arg.startsWith('--days=')) {
    options.days = parseInt(arg.split('=')[1]);
  }
  if (arg.startsWith('--variant=')) {
    options.variant = arg.split('=')[1];
  }
  if (arg.startsWith('--format=')) {
    options.outputFormat = arg.split('=')[1];
  }
});

/**
 * Calculate statistical significance using chi-square test
 * H0: No difference in conversion rates between variants
 */
function chiSquareTest(control, treatment) {
  // contingency table
  const controlConversions = control.conversions || 0;
  const controlTotal = control.total || 1;
  const treatmentConversions = treatment.conversions || 0;
  const treatmentTotal = treatment.total || 1;

  const controlNonConversions = controlTotal - controlConversions;
  const treatmentNonConversions = treatmentTotal - treatmentConversions;

  const totalConversions = controlConversions + treatmentConversions;
  const totalNonConversions = controlNonConversions + treatmentNonConversions;
  const grandTotal = totalConversions + totalNonConversions;

  if (grandTotal === 0) return null;

  // Chi-square formula
  const expectedControlConv = (controlTotal * totalConversions) / grandTotal;
  const expectedTreatmentConv = (treatmentTotal * totalConversions) / grandTotal;
  const expectedControlNonConv = (controlTotal * totalNonConversions) / grandTotal;
  const expectedTreatmentNonConv = (treatmentTotal * totalNonConversions) / grandTotal;

  const chi2 =
    Math.pow(controlConversions - expectedControlConv, 2) / expectedControlConv +
    Math.pow(treatmentConversions - expectedTreatmentConv, 2) / expectedTreatmentConv +
    Math.pow(controlNonConversions - expectedControlNonConv, 2) / expectedControlNonConv +
    Math.pow(treatmentNonConversions - expectedTreatmentNonConv, 2) / expectedTreatmentNonConv;

  // Chi-square to p-value (1 df) — approximate
  // p < 0.05 = significant, p < 0.01 = highly significant
  const pValue = chiSquareToPValue(chi2);

  return {
    chi2: chi2.toFixed(4),
    pValue: pValue.toFixed(4),
    significant: pValue < 0.05,
    highlySignificant: pValue < 0.01
  };
}

/**
 * Approximate chi-square to p-value lookup (1 df)
 */
function chiSquareToPValue(chi2) {
  // Critical values for 1 degree of freedom
  if (chi2 < 1.074) return 0.3;
  if (chi2 < 2.706) return 0.1;
  if (chi2 < 3.841) return 0.05;
  if (chi2 < 6.635) return 0.01;
  if (chi2 < 10.828) return 0.001;
  return 0.0001;
}

/**
 * Generate summary report
 */
function generateReport(data) {
  const report = {
    timestamp: new Date().toISOString(),
    period: `Last ${options.days} days`,
    samples: data.samples,
    variants: data.variants
  };

  if (data.samples.control && data.samples.treatment) {
    const controlRate = (data.samples.control.conversions / data.samples.control.total * 100).toFixed(2);
    const treatmentRate = (data.samples.treatment.conversions / data.samples.treatment.total * 100).toFixed(2);
    const lift = (((treatmentRate - controlRate) / controlRate * 100)).toFixed(1);

    report.conversionRates = {
      control: `${controlRate}%`,
      treatment: `${treatmentRate}%`,
      lift: `${lift}%`
    };

    const stats = chiSquareTest(data.samples.control, data.samples.treatment);
    if (stats) {
      report.statisticalSignificance = stats;
    }
  }

  return report;
}

/**
 * Mock data for demonstration
 * In production, fetch from /api/track endpoint
 */
function getMockData() {
  return {
    samples: {
      control: {
        total: 598,
        conversions: 85,  // 14.2%
        events: [
          { event: 'quiz_recommendation_shown', count: 598 },
          { event: 'contact_form_submitted', count: 85 },
          { event: 'compare_set_from_quiz', count: 42 }
        ]
      },
      treatment: {
        total: 602,
        conversions: 112,  // 18.6%
        events: [
          { event: 'quiz_recommendation_shown', count: 602 },
          { event: 'contact_form_submitted', count: 112 },
          { event: 'compare_set_from_quiz', count: 58 }
        ]
      }
    },
    variants: {
      control: {
        topWinners: [
          { family: 'The Muse', count: 178, pct: 29.8 },
          { family: 'The Classic', count: 142, pct: 23.7 },
          { family: 'The Icon', count: 128, pct: 21.4 },
          { family: 'The Siren', count: 98, pct: 16.4 },
          { family: 'The Empress', count: 52, pct: 8.7 }
        ],
        measurementAlignment: {
          avgWhrLean: -0.12,
          avgBwrLean: 0.18,
          whrCaliber: 'moderate',
          bwrCaliber: 'moderate'
        }
      },
      treatment: {
        topWinners: [
          { family: 'The Muse', count: 186, pct: 30.9 },
          { family: 'The Classic', count: 138, pct: 22.9 },
          { family: 'The Icon', count: 122, pct: 20.3 },
          { family: 'The Siren', count: 108, pct: 17.9 },
          { family: 'The Empress', count: 48, pct: 8.0 }
        ],
        measurementAlignment: {
          avgWhrLean: -0.14,
          avgBwrLean: 0.22,
          whrCaliber: 'moderate',
          bwrCaliber: 'moderate'
        }
      }
    }
  };
}

/**
 * Format console output
 */
function formatConsoleOutput(report) {
  console.log('\n╔════════════════════════════════════════════════════════════╗');
  console.log('║        ZELEX Quiz Engine — A/B Test Analysis               ║');
  console.log('╚════════════════════════════════════════════════════════════╝\n');

  console.log(`📊 Analysis Period: ${report.period}`);
  console.log(`   Generated: ${report.timestamp}\n`);

  if (report.conversionRates) {
    console.log('📈 Conversion Rates:');
    console.log(`   Control:   ${report.conversionRates.control}`);
    console.log(`   Treatment: ${report.conversionRates.treatment}`);
    console.log(`   Lift:      ${report.conversionRates.lift}\n`);

    if (report.statisticalSignificance) {
      const sig = report.statisticalSignificance;
      const badge = sig.highlySignificant ? '✓✓ HIGHLY SIGNIFICANT' : (sig.significant ? '✓ SIGNIFICANT' : '○ NOT SIGNIFICANT');
      console.log(`📊 Statistical Test (Chi-Square):
   χ² = ${sig.chi2}, p = ${sig.pValue}
   Result: ${badge}\n`);
    }
  }

  console.log('Samples:');
  console.log(`   Control:   ${report.samples.control?.total || 0} completions`);
  console.log(`   Treatment: ${report.samples.treatment?.total || 0} completions\n`);

  console.log('═══════════════════════════════════════════════════════════\n');
}

/**
 * Format JSON output
 */
function formatJsonOutput(report) {
  console.log(JSON.stringify(report, null, 2));
}

/**
 * Format HTML report for dashboard embedding
 */
function formatHtmlOutput(report) {
  const html = `<!DOCTYPE html>
<html>
<head>
  <title>ZELEX A/B Test Analysis</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #1a1a1a; color: #ddd; padding: 40px; }
    .container { max-width: 1000px; margin: 0 auto; background: #242424; border-radius: 8px; padding: 32px; }
    h1 { color: #d4a574; margin-bottom: 24px; }
    .metric { display: inline-block; margin: 16px 20px 16px 0; padding: 16px 24px; background: #2a2a2a; border-radius: 6px; border-left: 3px solid #d4a574; }
    .metric-label { font-size: 12px; color: #999; text-transform: uppercase; letter-spacing: 1px; }
    .metric-value { font-size: 28px; font-weight: bold; color: #d4a574; margin-top: 8px; }
    .significant { border-left-color: #5fb878; }
    .significant .metric-value { color: #5fb878; }
    .not-significant { border-left-color: #e18b73; }
    .not-significant .metric-value { color: #e18b73; }
  </style>
</head>
<body>
  <div class="container">
    <h1>ZELEX Quiz Engine — A/B Test Results</h1>
    <p><em>Generated ${report.timestamp}</em></p>

    <div class="metric">
      <div class="metric-label">Control Conversion</div>
      <div class="metric-value">${report.conversionRates?.control || '—'}</div>
    </div>

    <div class="metric">
      <div class="metric-label">Treatment Conversion</div>
      <div class="metric-value">${report.conversionRates?.treatment || '—'}</div>
    </div>

    <div class="metric">
      <div class="metric-label">Lift (Treatment vs Control)</div>
      <div class="metric-value">${report.conversionRates?.lift || '—'}</div>
    </div>

    <div class="metric ${report.statisticalSignificance?.significant ? 'significant' : 'not-significant'}">
      <div class="metric-label">Statistical Significance</div>
      <div class="metric-value">${report.statisticalSignificance?.pValue || '—'}</div>
      <div style="font-size: 11px; margin-top: 8px; color: #999;">χ² = ${report.statisticalSignificance?.chi2 || '—'}</div>
    </div>
  </div>
</body>
</html>`;

  console.log(html);
}

/**
 * Main
 */
async function main() {
  try {
    // In production, fetch from API:
    // const response = await fetch('/api/track?action=query&days=' + options.days);
    // const data = await response.json();

    // For now, use mock data
    const data = getMockData();

    const report = generateReport(data);

    // Output in requested format
    switch (options.outputFormat) {
      case 'json':
        formatJsonOutput(report);
        break;
      case 'html':
        formatHtmlOutput(report);
        break;
      case 'console':
      default:
        formatConsoleOutput(report);
    }

  } catch (error) {
    console.error('Analysis failed:', error.message);
    process.exit(1);
  }
}

main();
