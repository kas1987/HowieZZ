// CI validation for the ZELEX Atlas — no external deps, pure Node.
// 1) Every page's inline <script> block must parse as valid JS.
// 2) Every db/*.json must parse.
// 3) Each shipped page must reference the shared kit.
// Exits non-zero on the first failure so CI fails loudly.

import { readFileSync, readdirSync, existsSync } from 'node:fs';

let failures = 0;
const fail = (msg) => { console.error('  ✗ ' + msg); failures++; };
const ok   = (msg) => console.log('  ✓ ' + msg);

// Standalone legacy page(s) intentionally not on the shared runtime.
const STANDALONE_PAGES = new Set(['index-gallery-original.html']);

// Auto-discover root HTML pages so new pages are always validated.
const PAGES = readdirSync('.')
  .filter((n) => n.endsWith('.html'))
  .sort();

console.log('Validating pages…');
for (const f of PAGES) {
  if (!existsSync(f)) { fail(`${f} is missing`); continue; }
  const html = readFileSync(f, 'utf8');

  // shared-kit reference (all non-legacy pages)
  if (!STANDALONE_PAGES.has(f) && !html.includes('assets/site.js')) {
    fail(`${f} does not reference assets/site.js`);
  }

  // inline script(s) must parse
  const blocks = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]);
  let parsedAll = true;
  for (const code of blocks) {
    if (!code.trim()) continue;
    try { new Function(code); }
    catch (e) { fail(`${f} inline <script> parse error: ${e.message}`); parsedAll = false; }
  }
  if (parsedAll) ok(`${f}`);
}

console.log('Validating db/*.json…');
if (existsSync('db')) {
  for (const f of readdirSync('db').filter(n => n.endsWith('.json'))) {
    try { JSON.parse(readFileSync('db/' + f, 'utf8')); ok(`db/${f}`); }
    catch (e) { fail(`db/${f} invalid JSON: ${e.message}`); }
  }
} else {
  fail('db/ directory is missing');
}

if (failures) { console.error(`\n${failures} check(s) failed.`); process.exit(1); }
console.log('\nAll site checks passed.');
