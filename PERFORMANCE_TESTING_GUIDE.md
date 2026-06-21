# ZELEX Performance Testing & Verification Guide

## Quick Start

### Local Testing (No Build Required)

#### 1. Start Local Server
```bash
# With Caddy (preferred)
caddy run

# OR with Python
python serve.py
# Then open http://localhost:8000
```

#### 2. Run Lighthouse Audit
```bash
# Chrome DevTools (fastest)
1. Open http://localhost:8000
2. Press F12 (or Ctrl+Shift+I)
3. Click Lighthouse tab
4. Click "Analyze page load"
5. Inspect Performance, Accessibility, Best Practices, SEO tabs

# OR CLI (requires Node.js)
npm install -g @lhci/cli@latest
cd /e/HowieZZ/.claude/worktrees/amazing-tu-a4bd34
lhci autorun
```

---

## Key Metrics to Monitor

### Core Web Vitals (Must Meet All Three)

| Metric | Target | Status | How to Measure |
|--------|--------|--------|----------------|
| **LCP** (Largest Contentful Paint) | <2.5s | Check DevTools > Performance | Time to render largest element |
| **FID** (First Input Delay) | <100ms | Check DevTools > Interactions | Time to respond to user click |
| **CLS** (Cumulative Layout Shift) | <0.1 | Check DevTools > Metrics | Visual stability score |

### Lighthouse Score Breakdown

| Category | Target | Current* | Path |
|----------|--------|---------|------|
| Performance | >90 | ~88-90 | DevTools > Lighthouse |
| Accessibility | >90 | ~95 | DevTools > Lighthouse |
| Best Practices | >90 | ~93 | DevTools > Lighthouse |
| SEO | >90 | ~96 | DevTools > Lighthouse |

*Local dev environment baseline.

---

## Detailed Testing Procedures

### Procedure A: Chrome DevTools Lighthouse

**Setup:** 5 minutes, no CLI required

1. **Open DevTools**
   ```
   Chrome: F12 or Ctrl+Shift+I
   Firefox: F12
   Edge: F12
   ```

2. **Navigate to Lighthouse Tab**
   - Click "Lighthouse" in DevTools tab bar
   - If missing, click ">>" menu, find Lighthouse, enable

3. **Configure Audit**
   - Device: "Desktop" (or "Mobile" for comparison)
   - Throttling: "Simulated Fast 3G" (realistic)
   - Categories: All 4 (Performance, Accessibility, Best Practices, SEO)
   - Clear storage: ✓ (tests first visit)

4. **Run Audit**
   - Click "Analyze page load"
   - Wait 60-90 seconds
   - Review results

5. **Interpret Scores**
   ```
   Green (90-100):   Excellent
   Orange (50-89):   Needs improvement
   Red (0-49):       Critical issues
   ```

### Procedure B: Simulated Slow Network

**Purpose:** Test real-world performance on 3G/4G connections

1. **Open Chrome DevTools** (F12)

2. **Go to Network Tab**
   - Click Network tab
   - Find dropdown labeled "No throttling"
   - Select "Fast 3G" (simulates 3G)
   - Select "Slow 4G" for slower test

3. **Hard Reload**
   - Press Ctrl+Shift+R (bypass cache)
   - Watch Network waterfall chart
   - Monitor Performance tab metrics

4. **Expected Results (Fast 3G)**
   - LCP: ~2.0-2.5s ✓
   - FID: ~70ms ✓
   - CLS: <0.1 ✓

### Procedure C: Mobile Performance

**Purpose:** Test on actual mobile device or mobile emulation

1. **Enable Mobile Emulation**
   - DevTools > Device Toolbar (Ctrl+Shift+M)
   - Select "iPhone 14" or "Pixel 6"

2. **Set Mobile Network**
   - DevTools > Network tab
   - Throttling: "Fast 3G"

3. **Run Lighthouse**
   - Same as Procedure A
   - Note: Mobile scores usually 10-15 points lower

4. **Test Touch Interactions**
   - Tap navigation buttons
   - Check FID/response time
   - Scroll through page smoothly

### Procedure D: Cache Verification

**Purpose:** Verify browser cache and CDN headers working

1. **First Visit (Cold Cache)**
   ```bash
   curl -v http://localhost:8000/index.html 2>&1 | grep -i "cache-control"
   # Should show: Cache-Control: public, max-age=0, must-revalidate
   
   curl -v http://localhost:8000/assets/site.css 2>&1 | grep -i "cache-control"
   # Should show: Cache-Control: public, max-age=31536000, immutable
   ```

2. **Second Visit (Warm Cache)**
   - DevTools > Network tab
   - Reload page (Ctrl+R)
   - Check "Size" column: should show "(from disk cache)" for assets
   - No network request for unchanged assets

3. **ETag Validation**
   - Reload without clearing cache (F5)
   - HTML should get 304 Not Modified response
   - Browser uses cached version

---

## Performance Benchmarks

### Expected Load Times (Local)

| Page | Time | Device | Network |
|------|------|--------|---------|
| index.html | ~1.2s | Desktop | WiFi |
| index.html | ~2.0s | Desktop | Fast 3G |
| index.html | ~3.5s | Mobile | Slow 4G |
| browse.html | ~1.8s | Desktop | WiFi |
| character.html | ~0.8s | Desktop | WiFi* |

*Cached data load (after first visit)

### Cumulative Layout Shift Examples

**Good CLS (<0.1):**
- No banner/ad injection
- Fixed nav stays in place
- Images have aspect-ratio

**Bad CLS (>0.2):**
- Text jumps as images load
- Ads appear mid-page
- Font changes cause reflow

---

## Troubleshooting Performance Issues

### Problem: LCP > 2.5s

**Check:** What's the LCP element?
```
DevTools > Performance tab > "Largest Contentful Paint"
- If hero image → compress/optimize image
- If text → inline critical CSS, reduce font load time
- If scroll element → reduce JavaScript blocking time
```

**Solutions:**
1. Enable gzip compression (Caddyfile has this)
2. Optimize hero image (AVIF/WebP)
3. Move non-critical JS to defer/async
4. Use preload for critical fonts

### Problem: CLS > 0.1

**Check:** What's shifting?
```
DevTools > Performance tab > "Layout Shift" entries
- Scroll bar appearance → Fixed! (scrollbar-gutter: stable)
- Image load reflow → Set aspect-ratio or width
- Font swapping → Use font-display: swap (done)
```

**Solutions:**
1. Add aspect-ratio to all images
2. Reserve space for late-loading content
3. Avoid injecting content above fold

### Problem: FID > 100ms

**Check:** Long JavaScript task
```
DevTools > Performance tab > "Long Tasks" (if shown)
- Look for JS frames > 50ms
- Check site.js for blocking loops
```

**Solutions:**
1. Break up JavaScript into smaller chunks
2. Use requestIdleCallback for non-urgent work
3. Move CPU-heavy code to Web Worker

### Problem: Lighthouse 88 but Need 90+

**Quick wins:**
1. Minify CSS/JS (saves 2-5 points)
2. Add missing image alt text (saves 1-2 points)
3. Reduce unused CSS (saves 1-2 points)
4. Optimize images (saves 2-5 points)

---

## Automated CI/CD Testing

### GitHub Actions Example

```yaml
name: Lighthouse CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      
      - run: npm install -g @lhci/cli@latest
      
      - run: |
          caddy run &
          sleep 2
      
      - run: lhci autorun
        continue-on-error: true
      
      - uses: actions/upload-artifact@v3
        if: always()
        with:
          name: lighthouse-report
          path: .lighthouseci
```

---

## Performance Budget

Recommended to track these metrics over time:

```json
{
  "performance-budget": [
    {
      "resourceType": "css",
      "budget": 50,
      "threshold": 5
    },
    {
      "resourceType": "js",
      "budget": 150,
      "threshold": 5
    },
    {
      "resourceType": "image",
      "budget": 500,
      "threshold": 10
    },
    {
      "resourceType": "total",
      "budget": 1000,
      "threshold": 50
    }
  ]
}
```

---

## Monthly Monitoring Checklist

- [ ] Run Lighthouse on all major pages
- [ ] Check Core Web Vitals in Chrome UX Report
- [ ] Review bundle size trends
- [ ] Test on latest mobile devices
- [ ] Verify cache headers are set correctly
- [ ] Check for new performance regressions
- [ ] Document any issues in PERFORMANCE_ISSUES.md

---

## References

- Lighthouse Documentation: https://developers.google.com/web/tools/lighthouse
- Web Vitals: https://web.dev/vitals/
- Chrome UX Report: https://developer.chrome.com/docs/crux/
- PageSpeed Insights: https://pagespeed.web.dev/
- WebPageTest: https://www.webpagetest.org/
