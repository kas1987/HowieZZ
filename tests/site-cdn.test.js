/**
 * Unit tests for CDN functionality in site.js
 * Tests ZX.loadCdnConfig(), ZX.getCdnUrl(), ZX.loadImageWithFallback()
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { JSDOM } from 'jsdom';

describe('ZX CDN Module', () => {
  let dom;
  let window;
  let ZX;

  beforeEach(async () => {
    // Create fresh DOM for each test
    dom = new JSDOM('<!DOCTYPE html><html><body></body></html>', {
      url: 'http://localhost:8000',
    });
    window = dom.window;
    global.window = window;
    global.document = window.document;
    global.fetch = vi.fn();

    // Load site.js
    const fs = await import('fs');
    const path = await import('path');
    const siteJsPath = path.resolve('assets/site.js');
    const siteJsCode = fs.readFileSync(siteJsPath, 'utf8');

    // Execute site.js in the DOM context
    const script = window.document.createElement('script');
    script.textContent = siteJsCode;
    window.document.body.appendChild(script);

    ZX = window.ZX;
  });

  describe('loadCdnConfig', () => {
    it('should load CDN config from db/cdn_config.json', async () => {
      const mockConfig = {
        version: '1.0',
        cdn_enabled: true,
        cdn_provider: 'cloudinary',
        cdn_base_url: 'https://res.cloudinary.com/howiez/image/upload',
        fallback_local: true,
      };

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockConfig,
      });

      const config = await ZX.loadCdnConfig();
      expect(config.cdn_enabled).toBe(true);
      expect(config.cdn_provider).toBe('cloudinary');
      expect(global.fetch).toHaveBeenCalledWith('db/cdn_config.json', { cache: 'no-store' });
    });

    it('should cache config after first load', async () => {
      const mockConfig = { cdn_enabled: true, cdn_provider: 'cloudinary' };

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockConfig,
      });

      const config1 = await ZX.loadCdnConfig();
      const config2 = await ZX.loadCdnConfig();

      // fetch should only be called once
      expect(global.fetch).toHaveBeenCalledTimes(1);
      expect(config1).toEqual(config2);
    });

    it('should use fallback config when cdn_config.json is missing', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
      });

      const config = await ZX.loadCdnConfig();
      expect(config.cdn_enabled).toBe(false);
      expect(config.fallback_local).toBe(true);
    });

    it('should use fallback config on fetch error', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Network error'));

      const config = await ZX.loadCdnConfig();
      expect(config.cdn_enabled).toBe(false);
      expect(config.fallback_local).toBe(true);
    });
  });

  describe('getCdnUrl', () => {
    beforeEach(async () => {
      // Mock config for getCdnUrl tests
      const mockConfig = {
        cdn_enabled: true,
        cdn_base_url: 'https://res.cloudinary.com/howiez/image/upload',
        asset_mappings: {
          site_css: {
            cdn_url: 'https://res.cloudinary.com/howiez/image/upload/zelex/site/site.css',
          },
          site_js: {
            cdn_url: 'https://res.cloudinary.com/howiez/image/upload/zelex/site/site.js',
          },
        },
        image_folders: {
          thumbs: {
            cdn_url_template: 'https://res.cloudinary.com/howiez/image/upload/zelex/thumbs/',
          },
          photoshoots: {
            cdn_url_template: 'https://res.cloudinary.com/howiez/image/upload/zelex/photoshoots/',
          },
        },
      };

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockConfig,
      });

      await ZX.loadCdnConfig();
    });

    it('should return CDN URL for site.css', () => {
      const url = ZX.getCdnUrl('assets/site.css');
      expect(url).toContain('cloudinary.com');
      expect(url).toContain('site.css');
    });

    it('should return CDN URL for site.js', () => {
      const url = ZX.getCdnUrl('assets/site.js');
      expect(url).toContain('cloudinary.com');
      expect(url).toContain('site.js');
    });

    it('should return CDN URL for thumbnail', () => {
      const url = ZX.getCdnUrl('assets/thumbs/Fusion-Series/ZFE01_1+ZF161D/ZFE01_1_ZF161D-101.jpg');
      expect(url).toContain('cloudinary.com');
      expect(url).toContain('thumbs');
    });

    it('should return CDN URL for photoshoot image', () => {
      const url = ZX.getCdnUrl('assets/Fusion-Series/ZFE01_1+ZF161D/ZFE01_1_ZF161D-101.jpg');
      expect(url).toContain('cloudinary.com');
      expect(url).toContain('photoshoots');
    });

    it('should return local path when CDN is disabled', async () => {
      // Reset and load fallback config
      global.fetch.mockResolvedValueOnce({
        ok: false,
      });

      // Reset cache by creating new ZX context
      dom = new JSDOM('<!DOCTYPE html><html><body></body></html>');
      window = dom.window;
      global.window = window;
      global.document = window.document;

      // Re-execute site.js
      const fs = await import('fs');
      const path = await import('path');
      const siteJsPath = path.resolve('assets/site.js');
      const siteJsCode = fs.readFileSync(siteJsPath, 'utf8');

      const script = window.document.createElement('script');
      script.textContent = siteJsCode;
      window.document.body.appendChild(script);

      ZX = window.ZX;

      await ZX.loadCdnConfig();
      const url = ZX.getCdnUrl('assets/site.css');
      expect(url).toBe('assets/site.css');
    });
  });

  describe('loadImageWithFallback', () => {
    it('should successfully load image from CDN', async () => {
      const result = await ZX.loadImageWithFallback('https://res.cloudinary.com/howiez/image/upload/thumbs/test.jpg');
      // Note: In test environment, we can't actually load images, so this tests the structure
      expect(result).toHaveProperty('src');
      expect(result).toHaveProperty('loaded');
      expect(result).toHaveProperty('error');
    });

    it('should have correct retry configuration', async () => {
      const mockConfig = {
        cdn_enabled: true,
        retry_strategy: {
          max_attempts: 2,
          timeout_ms: 5000,
          fallback_delay_ms: 500,
        },
      };

      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockConfig,
      });

      await ZX.loadCdnConfig();
      const config = await ZX.loadCdnConfig();
      expect(config.retry_strategy.max_attempts).toBe(2);
      expect(config.retry_strategy.timeout_ms).toBe(5000);
    });
  });

  describe('CDN module initialization', () => {
    it('should export CDN functions on ZX object', () => {
      expect(typeof ZX.loadCdnConfig).toBe('function');
      expect(typeof ZX.getCdnUrl).toBe('function');
      expect(typeof ZX.loadImageWithFallback).toBe('function');
    });

    it('should not break existing ZX functionality', () => {
      // These are existing ZX methods that should still work
      expect(typeof ZX.load).toBe('function');
      expect(typeof ZX.track).toBe('function');
      expect(typeof ZX.qs).toBe('function');
      expect(typeof ZX.esc).toBe('function');
      expect(typeof ZX.famColor).toBe('function');
      expect(typeof ZX.famClass).toBe('function');
    });
  });

  describe('CDN config fallback', () => {
    it('should provide sensible defaults when config is missing', async () => {
      global.fetch.mockRejectedValueOnce(new Error('Not found'));

      const config = await ZX.loadCdnConfig();
      expect(config.fallback_local).toBe(true);
      expect(config.cdn_enabled).toBe(false);
      expect(config).toHaveProperty('retry_strategy');
    });
  });
});
