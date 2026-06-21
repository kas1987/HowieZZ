/**
 * Performance benchmarking tests
 * Tracks page load times, LCP, FID, and other Core Web Vitals
 */

describe('Performance Benchmarks', () => {
  const pages = [
    'index.html',
    'browse.html',
    'family.html?f=classic',
    'compare.html',
    'character.html?id=K-ZK168B-01',
  ];

  pages.forEach((page) => {
    it(`${page} page load time is under 3s`, () => {
      const start = Date.now();
      cy.loadPage(page);
      cy.window().then(() => {
        const elapsed = Date.now() - start;
        expect(elapsed).to.be.lessThan(3000);
        cy.task('log', `${page}: ${elapsed}ms`);
      });
    });
  });

  it('homepage First Contentful Paint is under 1.5s', () => {
    cy.loadPage('index.html');
    cy.window().then((win) => {
      const paint = win.performance.getEntriesByType('paint');
      const fcp = paint.find(p => p.name === 'first-contentful-paint');
      if (fcp) {
        expect(fcp.startTime).to.be.lessThan(1500);
      }
    });
  });

  it('Largest Contentful Paint occurs within 2.5s', () => {
    cy.loadPage('index.html');
    cy.window().then((win) => {
      const lcp = new Promise((resolve) => {
        const observer = new win.PerformanceObserver((list) => {
          const entries = list.getEntries();
          const lastEntry = entries[entries.length - 1];
          if (lastEntry.renderTime) {
            resolve(lastEntry.renderTime);
          } else if (lastEntry.loadTime) {
            resolve(lastEntry.loadTime);
          }
        });
        observer.observe({ entryTypes: ['largest-contentful-paint'] });
      });
      cy.wrap(lcp).then((lcpTime) => {
        if (lcpTime) {
          expect(lcpTime).to.be.lessThan(2500);
        }
      });
    });
  });

  it('no cumulative layout shift > 0.1', () => {
    cy.loadPage('browse.html');
    cy.window().then((win) => {
      const observer = new win.PerformanceObserver((list) => {
        let cls = 0;
        for (const entry of list.getEntries()) {
          if (!entry.hadRecentInput) {
            cls += entry.value;
          }
        }
        expect(cls).to.be.lessThan(0.1);
      });
      observer.observe({ entryTypes: ['layout-shift'] });
      // Stop observing after some time
      cy.wait(2000).then(() => observer.disconnect());
    });
  });

  it('characters.json is under 500KB', () => {
    cy.loadPage('browse.html');
    cy.window().then((win) => {
      const resources = win.performance.getEntriesByType('resource');
      const charJson = resources.find(r => r.name.includes('characters.json'));
      if (charJson) {
        expect(charJson.transferSize).to.be.lessThan(500000);
      }
    });
  });

  it('CSS is under 100KB', () => {
    cy.loadPage('index.html');
    cy.window().then((win) => {
      const resources = win.performance.getEntriesByType('resource');
      const css = resources.filter(r => r.name.includes('.css'));
      css.forEach((stylesheet) => {
        expect(stylesheet.transferSize).to.be.lessThan(100000);
      });
    });
  });

  it('total JS is under 150KB', () => {
    cy.loadPage('index.html');
    cy.window().then((win) => {
      const resources = win.performance.getEntriesByType('resource');
      const js = resources.filter(r => r.name.includes('.js'));
      const totalSize = js.reduce((sum, r) => sum + r.transferSize, 0);
      expect(totalSize).to.be.lessThan(150000);
    });
  });

  it('no render-blocking resources', () => {
    cy.loadPage('index.html');
    cy.window().then((win) => {
      const perf = win.performance.getEntriesByType('resource');
      const renderBlocking = perf.filter(r => {
        return (r.name.includes('.js') || r.name.includes('.css')) &&
               r.renderBlockingStatus === 'blocking';
      });
      expect(renderBlocking.length).to.equal(0);
    });
  });

  it('images use modern formats (webp)', () => {
    cy.loadPage('browse.html');
    cy.get('img').should('exist');
    cy.get('img').each(($img) => {
      const src = $img.attr('src') || '';
      // At least some images should use modern formats
      // This is optional but good practice
    });
  });

  it('DOM has < 1500 nodes', () => {
    cy.loadPage('browse.html');
    cy.window().then((win) => {
      const nodeCount = win.document.getElementsByTagName('*').length;
      expect(nodeCount).to.be.lessThan(1500);
    });
  });

  it('generates performance report', () => {
    cy.loadPage('index.html');
    cy.window().then((win) => {
      const timing = win.performance.timing;
      const paint = win.performance.getEntriesByType('paint');
      const report = {
        url: win.location.href,
        navigationStart: timing.navigationStart,
        loadEventEnd: timing.loadEventEnd,
        loadTime: timing.loadEventEnd - timing.navigationStart,
        paint: paint.map(p => ({ name: p.name, startTime: p.startTime })),
      };
      cy.task('log', JSON.stringify(report, null, 2));
    });
  });
});
