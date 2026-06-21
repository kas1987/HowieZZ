"""
Unit tests for Shopify sync module.

Run: pytest tests/test_sync_shopify_feed.py -v
"""
import json
import pytest
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Import the sync module
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from sync_shopify_feed import (
    generate_sku,
    parse_sku,
    reconcile_products,
    ShopifyAPI,
)

# ─── SKU GENERATION TESTS ──────────────────────────────────────────────────────
class TestSKUGeneration:
    """Test SKU generation from internal product codes."""

    def test_complete_doll_sku(self):
        """Test ZELEX-{head}-{body} format."""
        sku = generate_sku("ZFE01_1+ZF161D", "complete")
        assert sku == "ZELEX-ZFE01_1-ZF161D"

    def test_body_only_sku(self):
        """Test ZX-BODY-{code} format."""
        sku = generate_sku("ZF161D", "body")
        assert sku == "ZX-BODY-ZF161D"

    def test_head_only_sku(self):
        """Test ZX-HEAD-{code} format."""
        sku = generate_sku("ZFE01_1", "head")
        assert sku == "ZX-HEAD-ZFE01_1"

    def test_generic_fallback_sku(self):
        """Test generic ZX-{code} fallback."""
        sku = generate_sku("UNKNOWN123", "generic")
        assert sku == "ZX-UNKNOWN123"

# ─── SKU PARSING TESTS ──────────────────────────────────────────────────────────
class TestSKUParsing:
    """Test parsing Shopify SKUs back to internal codes."""

    def test_parse_complete_doll(self):
        """Parse ZELEX-{head}-{body} SKU."""
        parsed = parse_sku("ZELEX-ZFE01_1-ZF161D")
        assert parsed is not None
        assert parsed["type"] == "complete"
        assert parsed["head_code"] == "ZFE01_1"
        assert parsed["body_code"] == "ZF161D"
        assert parsed["product_code"] == "ZFE01_1+ZF161D"

    def test_parse_body_only(self):
        """Parse ZX-BODY-{code} SKU."""
        parsed = parse_sku("ZX-BODY-ZF161D")
        assert parsed is not None
        assert parsed["type"] == "body"
        assert parsed["body_code"] == "ZF161D"
        assert parsed["product_code"] == "ZF161D"

    def test_parse_head_only(self):
        """Parse ZX-HEAD-{code} SKU."""
        parsed = parse_sku("ZX-HEAD-ZFE01_1")
        assert parsed is not None
        assert parsed["type"] == "head"
        assert parsed["head_code"] == "ZFE01_1"
        assert parsed["product_code"] == "ZFE01_1"

    def test_parse_invalid_sku(self):
        """Return None for unparseable SKU."""
        parsed = parse_sku("INVALID-SKU-123")
        assert parsed is None

    def test_parse_empty_sku(self):
        """Return None for empty SKU."""
        parsed = parse_sku("")
        assert parsed is None

    def test_round_trip_complete(self):
        """Generate SKU, parse it back — should match."""
        original_code = "ZFE01_1+ZF161D"
        sku = generate_sku(original_code, "complete")
        parsed = parse_sku(sku)
        assert parsed["product_code"] == original_code

# ─── RECONCILIATION TESTS ──────────────────────────────────────────────────────
class TestReconciliation:
    """Test product reconciliation logic."""

    def create_mock_catalog(self, codes):
        """Helper to create a mock catalog."""
        return {
            "products": [{"code": code} for code in codes],
            "series": []
        }

    def create_mock_shopify_product(self, sku, title="Test Product"):
        """Helper to create a mock Shopify product."""
        return {
            "sku": sku,
            "title": title,
            "status": "active",
            "variants": []
        }

    def test_in_sync_products(self):
        """Recognize products that are synced."""
        catalog = self.create_mock_catalog(["ZFE01_1+ZF161D", "ZFE02_1+ZF161D"])
        shopify_products = [
            self.create_mock_shopify_product("ZELEX-ZFE01_1-ZF161D", "Product 1"),
            self.create_mock_shopify_product("ZELEX-ZFE02_1-ZF161D", "Product 2"),
        ]

        result = reconcile_products(shopify_products, catalog)

        assert len(result["in_sync"]) == 2
        assert result["in_sync"][0]["sku"] == "ZELEX-ZFE01_1-ZF161D"
        assert result["in_sync"][1]["sku"] == "ZELEX-ZFE02_1-ZF161D"

    def test_new_shopify_products(self):
        """Detect products new to Shopify."""
        catalog = self.create_mock_catalog(["ZFE01_1+ZF161D"])
        shopify_products = [
            self.create_mock_shopify_product("ZELEX-ZFE01_1-ZF161D", "Known"),
            self.create_mock_shopify_product("ZELEX-ZFE99_9-ZF999D", "New Product"),
        ]

        result = reconcile_products(shopify_products, catalog)

        assert len(result["new_shopify"]) == 1
        assert result["new_shopify"][0]["sku"] == "ZELEX-ZFE99_9-ZF999D"

    def test_discontinued_products(self):
        """Detect products removed from Shopify."""
        catalog = self.create_mock_catalog(["ZFE01_1+ZF161D", "ZFE02_1+ZF161D"])
        shopify_products = [
            self.create_mock_shopify_product("ZELEX-ZFE01_1-ZF161D"),
        ]

        result = reconcile_products(shopify_products, catalog)

        assert len(result["discontinued"]) == 1
        assert result["discontinued"][0]["code"] == "ZFE02_1+ZF161D"

    def test_error_handling_unparseable_sku(self):
        """Capture unparseable SKUs in errors."""
        catalog = self.create_mock_catalog(["ZFE01_1+ZF161D"])
        shopify_products = [
            self.create_mock_shopify_product("INVALID-FORMAT-123"),
        ]

        result = reconcile_products(shopify_products, catalog)

        assert len(result["errors"]) == 1
        assert result["errors"][0]["reason"] == "unparseable_sku"

    def test_statistics(self):
        """Verify reconciliation stats."""
        catalog = self.create_mock_catalog(["A", "B", "C"])
        shopify_products = [
            self.create_mock_shopify_product("ZELEX-A-A"),
            self.create_mock_shopify_product("ZELEX-B-B"),
        ]

        result = reconcile_products(shopify_products, catalog)

        assert result["stats"]["shopify_total"] == 2
        assert result["stats"]["catalog_total"] == 3

# ─── SHOPIFY API CLIENT TESTS ──────────────────────────────────────────────────
class TestShopifyAPI:
    """Test Shopify REST API client."""

    def test_initialization(self):
        """Initialize API client."""
        api = ShopifyAPI("https://zelex.myshopify.com", "test-token")
        assert api.base_url == "https://zelex.myshopify.com"
        assert api.token == "test-token"
        assert api.call_count == 0
        assert api.error_count == 0

    def test_base_url_normalization(self):
        """Normalize base URL (strip trailing slash)."""
        api = ShopifyAPI("https://zelex.myshopify.com/", "token")
        assert api.base_url == "https://zelex.myshopify.com"

    @patch("sync_shopify_feed.requests.Session.request")
    def test_successful_request(self, mock_request):
        """Test successful HTTP request."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success"}
        mock_response.headers = {"X-Shopify-Shop-Api-Call-Limit": "1/40"}
        mock_request.return_value = mock_response

        api = ShopifyAPI("https://test.myshopify.com", "token")
        result = api._request("GET", "test.json")

        assert result == {"result": "success"}
        assert api.call_count == 1
        assert api.error_count == 0

    @patch("sync_shopify_feed.requests.Session.request")
    def test_auth_failure(self, mock_request):
        """Test 401 auth failure."""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_request.return_value = mock_response

        api = ShopifyAPI("https://test.myshopify.com", "bad-token")
        result = api._request("GET", "test.json")

        assert result is None
        assert api.error_count == 1

    @patch("sync_shopify_feed.requests.Session.request")
    @patch("sync_shopify_feed.time.sleep")
    def test_rate_limit_retry(self, mock_sleep, mock_request):
        """Test 429 rate limit handling."""
        # First call: 429, Second call: 200
        mock_response_429 = Mock()
        mock_response_429.status_code = 429
        mock_response_429.headers = {"Retry-After": "1"}

        mock_response_200 = Mock()
        mock_response_200.status_code = 200
        mock_response_200.json.return_value = {"result": "success"}
        mock_response_200.headers = {"X-Shopify-Shop-Api-Call-Limit": "1/40"}

        mock_request.side_effect = [mock_response_429, mock_response_200]

        api = ShopifyAPI("https://test.myshopify.com", "token")
        result = api._request("GET", "test.json", retries=2)

        # Rate limit retry should have slept
        mock_sleep.assert_called()
        assert result == {"result": "success"}

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
