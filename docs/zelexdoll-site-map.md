# Zelexdoll.com — Site Map & Data-Pull Reference

> Purpose: enough of the site's structure to (a) backfill gaps in our catalog DB and
> (b) rebuild the site for Howie. Zelexdoll runs on **Shopify**, so almost everything
> is available as structured JSON — no HTML scraping needed for data.

Store CDN base: `https://cdn.shopify.com/s/files/1/0661/6059/1091/files/`
(mirror: `https://www.zelexdoll.com/cdn/shop/files/`). The `?v=...` query is a
cache-buster and can be dropped when downloading.

---

## 1. Discovery — sitemaps (the full URL tree)

`https://www.zelexdoll.com/sitemap.xml` is an index pointing to:

| Sitemap | What it lists |
|---|---|
| `sitemap_products_1.xml?from=…&to=…` | every product URL (the master product list) |
| `sitemap_collections_1.xml?from=…&to=…` | every collection URL |
| `sitemap_pages_1.xml?from=…&to=…` | content/info pages |
| `sitemap_blogs_1.xml` | blog/magazine articles |
| `sitemap_agentic_discovery.xml` | LLM-oriented discovery feed |

Use the products sitemap to enumerate all product handles, then hit each
`/products/{handle}.json` for data.

---

## 2. Data API — Shopify JSON endpoints (no auth)

These are the workhorses. **All public, all JSON.**

| Endpoint | Returns |
|---|---|
| `/products/{handle}.json` | one product: title, tags, vendor, variants (SKU!), options, **all image src** |
| `/collections.json` | all collections (handle, title, id) — 30 total, no pagination |
| `/collections/{handle}/products.json?limit=250&page=N` | products in a collection, paginated |
| `/products.json?limit=250&page=N` | ALL products, paginated (~250/page max) |

Pagination: append `?limit=250&page=N`, increment `N` until an empty array.
(Note: a summarizing fetch tool will truncate these large arrays — do the actual
pull with a real HTTP client/script that reads the whole JSON body.)

Head-prefix observation: alongside our known head prefixes (`GE`=I-series,
`KE`=K-series, `ZFE`=Fusion), the **SLE lines use `ZXE` heads** paired with `ZX`
bodies — e.g. `SLE3.0-ZXE215_1`, `SLE2.0-ZXE216_4`. Worth modeling if we extend
the catalog to SLE products.

### Product JSON schema (the important fields)

```
product.title          e.g. "Ulrica ZG170C-170cm C Cup Fair Skin Sex Doll GE52_1_1"
product.handle         URL slug (can be outdated vs. the code — don't trust for codes)
product.vendor         "ZELEX" / "ZELEXDOLL"
product.tags           e.g. "162D, Fair, NEW"  or  "168B, NEW, ZK168B"  ← body code often here
product.options[]      {name, position, values[]}  — e.g. Skin Tone, Skeleton, Makeup
product.variants[]     {sku, title, price, compare_at_price, options...}
                       sku e.g. "GE52_1_1+ZG170C-Fair"  ← HEAD+BODY-TONE, the gap-filler
product.images[]       {position, alt, width, height, src, variant_ids}
                       src e.g. ".../files/GE52_1-108.jpg?v=…"
```

**Where the codes live (most reliable → least):**
1. `variant.sku` — `{HEAD}+{BODY}-{TONE}`, e.g. `GE149_1(GE74MJ)+ZG170D-Fair`. Most authoritative.
2. `product.title` — contains body code + height + cup spelled out (`ZG170C-170cm C Cup`).
3. `product.tags` — usually includes the body code (`ZK168B`) and a `{height}{cup}` tag (`162D`).
4. `product.images[].src` filename prefix — what our folder names are derived from
   (this is where legacy products LOSE the body code: image is `GE52_1-108.jpg`
   but the SKU is `GE52_1_1+ZG170C-Fair`).

This is exactly why 44 of our I-series folders have no body code: we built folder
names from image filenames. **The SKU/title always has it.** → see §6 backfill.

---

## 3. CDN asset URL structure

```
https://cdn.shopify.com/s/files/1/0661/6059/1091/files/{FILENAME}?v={version}
```
- `{FILENAME}` is exactly the `images[].src` basename in product JSON.
- Drop `?v=` to fetch full-res; Shopify also serves resized variants via `&width=N`.
- Product images: `{HEAD}_{BODY}-{NNN}.jpg` (I-series) / `{HEAD}_{BODY}-{NNN}.jpg` (K).
- Spec cards, option swatches, head shots are also CDN files referenced from pages.

---

## 4. Collections (the catalog taxonomy)

30 collections. The ones that map to our series / fill categorization:

| Handle | Title | Relevance |
|---|---|---|
| `silicone` | Inspiration Series | **our I-Series** (GE heads, ZG/ZGX bodies) |
| `k-series` | K Series | **our K-Series** (KE heads, ZK bodies) |
| `fusion` | Fusion Series | **our Fusion** (ZFE heads, ZF bodies) |
| `sle-doll-3-0` | SLE 3.0 | the **ZX** bodies (SLE 3.0 line) |
| `sle-series` / `in-stock-sle-series` | SLE Series / SLE 2.0 | older SLE |
| `sle-torso`, `sle-torso-with-hands`, `sle` | SLE torsos | torso-only products |
| `single-head-single-body` | Single Head & Single Body | head-only / body-only listings |
| `hair-plant` | Hair Implant | option/upgrade |
| Merch/marketing facets | `bestsellers`, `new-sex-dolls`, `bbw`, `curvy`, `milf`, `skinny`, `tall`, `blonde`, `sale`, `full-size-doll` | filtering only — products repeat across these |
| Regional stock | `eu-instock`, `eu-sle1-0`, `imperfection-dolls`, `eu-small-imperfections`, `eu-sle-torso-defective` | inventory/condition views |
| Ops | `payment-options`, `testsibling` | ignore |

For rebuilding the catalog, the **series collections** (`silicone`, `k-series`,
`fusion`, `sle-doll-3-0`) are the canonical product sources; the rest are facets.

---

## 5. Content pages (to rebuild the site for Howie)

From `sitemap_pages_1.xml` — the non-product content:

- **Brand/story:** `about-us`, `our-strength`, `first-to-zelex`, `first-to-sex-doll`, `vendors`
- **Buying guides:** `dolls-guide`, `tutorials`, `the-difference-between-standard-skeleton-and-upgraded-evo-skeleton`, `faq`
- **Policy/legal:** `shipping-return-policy`, `return-refund-policy`, `terms-of-service`, `track-your-order`, `contact-us`
- **Content/marketing:** `zelex-magazine`, `blogs`, `reviews`, `affiliates`, `influencer`
- **Stock status:** `normal-dolls-with-no-damage-in-stock`, `defective-dolls-in-stock`
- **Wishlist/search (app-driven):** `swym-wishlist`, `swym-share-wishlist`, `reviews`, `search-filter-help`, `search-results`

Blog/magazine content lives under `sitemap_blogs_1.xml` (`/blogs/{blog}/{article}`).

Each page's rendered content is fetchable as HTML; there is no page `.json` API
(pages are theme-rendered), so for page COPY we read the HTML, but for PRODUCT
data we always use `.json`.

---

## 6. How this fills our DB gaps

Our two known gaps and how the site closes them:

**Gap A — 44 I-series products missing a body code.**
Their image filenames (e.g. `GE52_1-108.jpg`) dropped the body, but the product
SKU (`GE52_1_1+ZG170C-Fair`) and title (`ZG170C-170cm C Cup`) carry it.
→ Match our product folder by head code to the live product (by SKU prefix or
title head code), read the body code, and backfill `products.body_code`.

**Gap B — options/variants not yet modeled per product.**
`product.options[]` + `product.variants[]` give the real configurable axes
(skin tone, skeleton, makeup version, etc.) and prices per product — richer than
our generic `options` table. → add a `product_variants` table keyed by SKU.

Recommended pull (one pass, no scraping):
```
for page in 1..N:
    GET /products.json?limit=250&page={page}
    for product in page:
        record handle, title, tags, vendor
        for variant in product.variants:  record sku, price, options
        derive body_code from sku/title  → backfill catalog
        (optionally) record image srcs to detect assets we're missing
```

Pricing, inventory, and "NEW" status also come free from this feed if we want
them in the rebuilt site.

**Implemented:** `scripts/fetch_catalog.py` does exactly this pull. It fetched
367 live products, matched all 77 of our folders by image-filename overlap (with a
head-code validity guard), and wrote `db/product_overrides.json` (code backfills +
price + live handle), `db/live_variants.json` (340 SKUs), and `db/asset_gaps.json`
(live images we're missing). `build_db.py` applies these fill-only on rebuild:
result is **77/77 products with a body code, all mapping to a full spec card**,
plus a `product_variants` table with pricing. Re-run `fetch_catalog.py` to refresh
from the live store, then `build_db.py --reset`.

---

## 7. Quick-reference recipes

- **Enumerate all products:** loop `/products.json?limit=250&page=N`.
- **One product, everything:** `/products/{handle}.json`.
- **Per-collection (series) products:** `/collections/silicone/products.json?limit=250&page=N`.
- **Asset download:** take `images[].src`, strip `?v=`, GET from CDN.
- **Codes:** trust `variant.sku` first, then `title`, then `tags`, never the handle.
