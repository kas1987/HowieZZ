/**
 * Competitor catalog scraper — targeted pass
 * Sites: SiliconWives, BestRealDoll, FantasyWives
 * Priority brands: Doll Forever, Sanhui, Starpery (+ all others found)
 * Strategy:
 *   1. Shopify /products.json (all pages) for catalog + pricing
 *   2. Sample product pages for full measurement depth (B/W/H, height, weight)
 * Output: db/competitor_web_scrape.json
 */

const { chromium } = require('playwright');
const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

const OUT_PATH = path.join(__dirname, '..', 'db', 'competitor_web_scrape.json');

const TARGETS = [
  { name: 'SiliconWives',  url: 'https://www.siliconwives.com',  type: 'retailer' },
  { name: 'BestRealDoll',  url: 'https://www.bestsexylovedoll.com', type: 'retailer' },
  { name: 'FantasyWives',  url: 'https://www.fantasywives.com',   type: 'retailer' },
];

// Brands we care about most for gap analysis
const PRIORITY_BRANDS = ['doll forever', 'dollfuture', 'sanhui', 'starpery', 'star perry', 'zelex', 'gynoid', 'irontech', 'game lady', 'gamelady', 'jiusheng', 'tayu', 'fanreal', 'jk doll', 'wm doll', 'se doll', 'ds doll'];

const UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36';

// ── HTTP fetch (JSON) ─────────────────────────────────────────────────────────
function fetchJson(url) {
  return new Promise((resolve, reject) => {
    const lib = url.startsWith('https') ? https : http;
    const req = lib.get(url, {
      headers: { 'User-Agent': UA, 'Accept': 'application/json' },
    }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        const loc = res.headers.location.startsWith('http') ? res.headers.location : new URL(res.headers.location, url).href;
        return fetchJson(loc).then(resolve).catch(reject);
      }
      if (res.statusCode !== 200) return reject(new Error(`HTTP ${res.statusCode}`));
      let body = '';
      res.on('data', d => body += d);
      res.on('end', () => { try { resolve(JSON.parse(body)); } catch (e) { reject(e); } });
    });
    req.on('error', reject);
    req.setTimeout(20000, () => { req.destroy(); reject(new Error('timeout')); });
  });
}

// Extract measurements from HTML/text
function parseMeasurements(text) {
  const clean = text.replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ');
  const height = clean.match(/(?:height|tall)[:\s]*(\d{2,3})\s*cm/i)?.[1]
               || clean.match(/(\d{2,3})\s*cm\s*(?:tall|height)/i)?.[1]
               || clean.match(/\b(14\d|15\d|16\d|17\d|18\d)\s*cm\b/)?.[1];
  const weight = clean.match(/(?:weight)[:\s]*([\d.]+)\s*kg/i)?.[1]
               || clean.match(/([\d.]+)\s*kg/i)?.[1];
  const bust   = clean.match(/(?:bust|chest)[:\s]*([\d.]+)\s*cm/i)?.[1];
  const waist  = clean.match(/(?:waist)[:\s]*([\d.]+)\s*cm/i)?.[1];
  const hip    = clean.match(/(?:hip|hips)[:\s]*([\d.]+)\s*cm/i)?.[1];
  const cup    = clean.match(/([A-K])-?cup/i)?.[1]?.toUpperCase();
  return {
    height_cm:  height ? parseInt(height)    : null,
    weight_kg:  weight ? parseFloat(weight)  : null,
    bust_cm:    bust   ? parseFloat(bust)    : null,
    waist_cm:   waist  ? parseFloat(waist)   : null,
    hip_cm:     hip    ? parseFloat(hip)     : null,
    cup_size:   cup    || null,
  };
}

// ── Shopify catalog fetch (all pages) ─────────────────────────────────────────
async function fetchShopifyCatalog(baseUrl) {
  const all = [];
  let page = 1;
  while (true) {
    const url = `${baseUrl}/products.json?limit=250&page=${page}`;
    const data = await fetchJson(url);
    const products = data.products || [];
    if (!products.length) break;
    for (const p of products) {
      const variant = p.variants?.[0] || {};
      const price = variant.price ? parseFloat(variant.price) : null;
      const bodyText = (p.body_html || '').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
      const meas = parseMeasurements(p.body_html || '');
      all.push({
        method: 'shopify_api',
        brand: (p.vendor || '').trim(),
        title: p.title,
        handle: p.handle,
        product_type: p.product_type,
        price_usd: price,
        price_raw: variant.price,
        available: variant.available,
        tags: Array.isArray(p.tags) ? p.tags : (p.tags || '').split(',').map(t => t.trim()).filter(Boolean),
        created_at: p.created_at,
        ...meas,
        specs_snippet: bodyText.substring(0, 500),
      });
    }
    console.log(`  page ${page}: ${products.length} products`);
    if (products.length < 250) break;
    page++;
    if (page > 20) break;
  }
  return all;
}

// ── Playwright: product page deep-dive for measurements ──────────────────────
async function deepMeasurements(page, productUrl, baseUrl) {
  try {
    await page.goto(productUrl.startsWith('http') ? productUrl : baseUrl + productUrl, {
      waitUntil: 'domcontentloaded', timeout: 20000,
    });
    await page.waitForTimeout(1500);
    const bodyHtml = await page.evaluate(() => document.body.innerHTML);
    return parseMeasurements(bodyHtml);
  } catch {
    return {};
  }
}

// ── Playwright: full catalog scrape fallback ──────────────────────────────────
async function playwrightCatalog(browser, target) {
  const ctx = await browser.newContext({ userAgent: UA, locale: 'en-US' });
  const page = await ctx.newPage();
  const results = [];

  const tryPaths = ['/collections/all', '/collections/silicone-sex-dolls', '/collections/silicone', '/products', '/shop', '/'];
  let landed = false;

  for (const p of tryPaths) {
    try {
      const res = await page.goto(target.url + p, { waitUntil: 'domcontentloaded', timeout: 20000 });
      if (res?.ok()) { landed = true; console.log(`  landed on ${target.url + p}`); break; }
    } catch (_) {}
  }

  if (!landed) { await ctx.close(); return results; }
  await page.waitForTimeout(3000);

  const cards = await page.evaluate(() => {
    const selectors = ['.product-card', '.product-item', '.grid__item', 'li.grid-item', '.product', '[class*="product-card"]', 'article.product'];
    for (const sel of selectors) {
      const els = document.querySelectorAll(sel);
      if (els.length > 3) {
        return Array.from(els).slice(0, 300).map(el => ({
          title:  el.querySelector('[class*="title"],[class*="name"],h2,h3,h4')?.textContent?.trim() || '',
          price:  el.querySelector('[class*="price"],.price,.amount')?.textContent?.trim() || '',
          link:   el.querySelector('a')?.getAttribute('href') || '',
        }));
      }
    }
    return [];
  });

  for (const card of cards) {
    if (!card.title || card.title.length < 2) continue;
    const priceMatch = card.price.match(/\$?([\d,]+\.?\d*)/);
    results.push({
      method: 'playwright_dom',
      brand: target.name,
      title: card.title,
      handle: card.link,
      product_type: null,
      price_usd: priceMatch ? parseFloat(priceMatch[1].replace(',', '')) : null,
      price_raw: card.price,
      available: null,
      tags: [],
      created_at: null,
      height_cm: null, weight_kg: null, bust_cm: null, waist_cm: null, hip_cm: null, cup_size: null,
      specs_snippet: null,
    });
  }

  console.log(`  [playwright] ${results.length} products`);
  await ctx.close();
  return results;
}

// ── Measurement depth pass (sample product pages for missing measurements) ────
async function enrichMeasurements(browser, baseUrl, products, sampleSize = 20) {
  // Focus on priority brands first, then fill to sample size
  const needsMeasurements = products.filter(p =>
    p.height_cm == null || p.bust_cm == null
  );
  const priority = needsMeasurements.filter(p =>
    PRIORITY_BRANDS.some(b => (p.brand || p.title || '').toLowerCase().includes(b))
  );
  const rest = needsMeasurements.filter(p => !priority.includes(p));
  const toSample = [...priority, ...rest].slice(0, sampleSize);

  if (toSample.length === 0) return;

  const ctx = await browser.newContext({ userAgent: UA, locale: 'en-US' });
  const page = await ctx.newPage();
  let enriched = 0;

  for (const product of toSample) {
    const handle = product.handle;
    if (!handle) continue;
    const productUrl = handle.startsWith('http') ? handle : `${baseUrl}/products/${handle}`;
    try {
      await page.goto(productUrl, { waitUntil: 'domcontentloaded', timeout: 20000 });
      await page.waitForTimeout(1000);
      const html = await page.evaluate(() => document.body.innerHTML);
      const meas = parseMeasurements(html);
      if (meas.height_cm || meas.bust_cm) {
        Object.assign(product, meas);
        enriched++;
      }
    } catch (_) {}
  }

  await ctx.close();
  console.log(`  enriched ${enriched}/${toSample.length} products with page-level measurements`);
}

// ── Main ──────────────────────────────────────────────────────────────────────
async function main() {
  const output = { scraped_at: new Date().toISOString(), summary: [], total_products: 0, products: [] };
  const browser = await chromium.launch({ headless: true });

  for (const target of TARGETS) {
    console.log(`\n══ ${target.name} (${target.url}) ══`);
    let products = [];
    let method = 'shopify_api';

    try {
      products = await fetchShopifyCatalog(target.url);
      console.log(`  Shopify API: ${products.length} total products`);
    } catch (err) {
      console.log(`  Shopify failed (${err.message}), trying Playwright...`);
      products = await playwrightCatalog(browser, target);
      method = 'playwright_dom';
    }

    // Enrich with product-page measurements (especially for priority brands)
    if (products.length > 0) {
      console.log(`  Running measurement depth pass...`);
      await enrichMeasurements(browser, target.url, products, 30);
    }

    // Tag source
    for (const p of products) {
      p.source = target.name;
      p.source_url = target.url;
      p.is_priority = PRIORITY_BRANDS.some(b => (p.brand || p.title || '').toLowerCase().includes(b));
    }

    const brands = [...new Set(products.map(p => p.brand).filter(Boolean))].sort();
    const priced = products.filter(p => p.price_usd != null).length;
    const measured = products.filter(p => p.height_cm != null).length;
    const priorityHits = products.filter(p => p.is_priority);

    output.summary.push({
      source: target.name,
      type: target.type,
      method,
      product_count: products.length,
      priced_count: priced,
      measured_count: measured,
      brands_found: brands,
      priority_brands_found: [...new Set(priorityHits.map(p => p.brand))],
      priority_products: priorityHits.length,
    });

    output.products.push(...products);
    console.log(`  Brands: ${brands.slice(0, 10).join(', ')}${brands.length > 10 ? ` +${brands.length - 10} more` : ''}`);
    console.log(`  Priority brands: ${[...new Set(priorityHits.map(p => p.brand))].join(', ') || 'none found'}`);
    console.log(`  Priced: ${priced}/${products.length}  Measured: ${measured}/${products.length}`);
  }

  await browser.close();

  output.total_products = output.products.length;
  fs.writeFileSync(OUT_PATH, JSON.stringify(output, null, 2));

  console.log('\n\n══════════════════════════════════════════');
  console.log(`DONE — ${output.total_products} total products → ${OUT_PATH}`);
  console.log('══════════════════════════════════════════');
  console.log('\nSummary:');
  for (const s of output.summary) {
    console.log(`  ${s.source.padEnd(14)} ${String(s.product_count).padStart(4)} products  ${String(s.priced_count).padStart(4)} priced  ${String(s.measured_count).padStart(4)} measured  [${s.method}]`);
    if (s.priority_brands_found.length) console.log(`    Priority: ${s.priority_brands_found.join(', ')}`);
  }
}

main().catch(err => { console.error(err); process.exit(1); });
