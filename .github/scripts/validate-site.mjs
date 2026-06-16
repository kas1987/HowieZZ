// CI validation for the ZELEX Atlas — no external deps, pure Node.
// 1) Every page's inline <script> block must parse as valid JS.
// 2) Every db/*.json must parse.
// 3) Each shipped page must reference the shared kit.
// 4) Each shipped page must carry baseline SEO/social metadata.
// 5) Discoverability + a11y support files must exist and parse.
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

  // baseline SEO / social metadata (kit pages only)
  if (KIT_PAGES.includes(f)) {
    const META_CHECKS = [
      [/<meta\s+name="description"\s+content="[^"]+"/i, 'meta description'],
      [/<link\s+rel="canonical"\s+href="https?:\/\/[^"]+"/i, 'canonical link'],
      [/<meta\s+property="og:title"\s+content="[^"]+"/i, 'og:title'],
      [/<meta\s+name="viewport"/i, 'viewport'],
      [/<link\s+rel="icon"/i, 'favicon link'],
    ];
    for (const [re, label] of META_CHECKS) {
      if (!re.test(html)) fail(`${f} is missing ${label}`);
    }
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

console.log('Validating discoverability + a11y support files…');
const SUPPORT_FILES = ['robots.txt', 'sitemap.xml', '404.html', 'assets/favicon.svg'];
for (const f of SUPPORT_FILES) {
  if (existsSync(f)) ok(`${f}`);
  else fail(`${f} is missing`);
}
// sitemap.xml must be well-formed enough to list at least the homepage
if (existsSync('sitemap.xml')) {
  const sm = readFileSync('sitemap.xml', 'utf8');
  if (!/<urlset[\s>]/.test(sm) || !/index\.html<\/loc>/.test(sm)) {
    fail('sitemap.xml is malformed or missing the homepage <loc>');
  }
}

if (failures) { console.error(`\n${failures} check(s) failed.`); process.exit(1); }
console.log('\nAll site checks passed.');
