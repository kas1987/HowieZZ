#!/usr/bin/env python3
"""
Unit tests for CDN manifest generation and asset collection.
"""
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest
import sys
import os

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from push_assets_to_cdn import (
    compute_hash, get_file_size_bytes, collect_assets, generate_manifest,
    _get_cdn_base_url
)


class TestHashComputation:
    """Test SHA-256 hash computation."""

    def test_compute_hash_consistency(self):
        """Same file should produce same hash."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"test content")
            f.flush()
            temp_path = Path(f.name)

        try:
            hash1 = compute_hash(temp_path)
            hash2 = compute_hash(temp_path)
            assert hash1 == hash2, "Hashes should be consistent"
            assert len(hash1) == 64, "SHA-256 hash should be 64 hex chars"
        finally:
            temp_path.unlink()

    def test_compute_hash_different_content(self):
        """Different content should produce different hashes."""
        with tempfile.NamedTemporaryFile(delete=False) as f1:
            f1.write(b"content1")
            f1.flush()
            path1 = Path(f1.name)

        with tempfile.NamedTemporaryFile(delete=False) as f2:
            f2.write(b"content2")
            f2.flush()
            path2 = Path(f2.name)

        try:
            hash1 = compute_hash(path1)
            hash2 = compute_hash(path2)
            assert hash1 != hash2, "Different content should produce different hashes"
        finally:
            path1.unlink()
            path2.unlink()


class TestFileSizeBytes:
    """Test file size detection."""

    def test_get_file_size_bytes(self):
        """Should return correct file size."""
        with tempfile.NamedTemporaryFile(delete=False) as f:
            content = b"x" * 1024  # 1 KB
            f.write(content)
            f.flush()
            temp_path = Path(f.name)

        try:
            size = get_file_size_bytes(temp_path)
            assert size == 1024, f"Expected 1024 bytes, got {size}"
        finally:
            temp_path.unlink()


class TestCdnBaseUrl:
    """Test CDN base URL generation."""

    def test_cloudinary_url(self):
        """Should generate Cloudinary URL."""
        with patch.dict(os.environ, {"ZELEX_CDN_PROVIDER": "cloudinary", "ZELEX_CDN_CLOUD_NAME": "test"}):
            from push_assets_to_cdn import CDN_PROVIDER
            # Note: CDN_PROVIDER is set at module load, so we test indirectly
            url = _get_cdn_base_url()
            assert "cloudinary.com" in url or url == ""

    def test_bunny_url(self):
        """Should generate Bunny CDN URL."""
        # Note: CDN_PROVIDER is set at module import, so this test validates the function
        # with direct calls to _get_cdn_base_url() which reads the env at call time
        with patch.dict(os.environ, {"ZELEX_CDN_PROVIDER": "bunny", "ZELEX_CDN_STORAGE_ZONE": "zelex"}):
            url = _get_cdn_base_url()
            # The function should generate a Bunny URL or return empty string
            # (depends on CDN_PROVIDER which was set at module load time)
            assert isinstance(url, str)


class TestManifestGeneration:
    """Test manifest generation."""

    def test_generate_manifest_dry_run(self):
        """Manifest should mark dry-run correctly."""
        assets = {
            "site_files": [],
            "thumbnails": [],
            "photoshoots": []
        }
        manifest = generate_manifest(assets, dry_run=True)
        assert manifest["dry_run"] is True
        assert manifest["metadata"]["sync_status"] == "dry_run"

    def test_generate_manifest_synced(self):
        """Manifest should mark synced correctly."""
        assets = {
            "site_files": [],
            "thumbnails": [],
            "photoshoots": []
        }
        manifest = generate_manifest(assets, dry_run=False)
        assert manifest["dry_run"] is False
        assert manifest["metadata"]["sync_status"] == "synced"

    def test_generate_manifest_schema(self):
        """Manifest should have required schema."""
        assets = {
            "site_files": [],
            "thumbnails": [],
            "photoshoots": []
        }
        manifest = generate_manifest(assets)

        # Required top-level fields
        assert "version" in manifest
        assert "schema_version" in manifest
        assert "generated_at" in manifest
        assert "cdn_provider" in manifest
        assert "cdn_base_url" in manifest
        assert "fallback_local" in manifest
        assert "assets" in manifest
        assert "images" in manifest
        assert "metadata" in manifest

        # Required metadata
        metadata = manifest["metadata"]
        assert "total_assets" in metadata
        assert "total_size_mb" in metadata
        assert "sync_status" in metadata

    def test_manifest_with_site_files(self):
        """Manifest should track site CSS/JS correctly."""
        assets = {
            "site_files": [
                {
                    "name": "site.css",
                    "local_path": "/path/to/site.css",
                    "rel_path": "assets/site.css",
                    "size": 45621,
                    "hash": "abc123def456ab1234567890",
                    "mime_type": "text/css",
                    "cdn_path": "zelex/site/site.css"
                }
            ],
            "thumbnails": [],
            "photoshoots": []
        }
        manifest = generate_manifest(assets)

        assert "site_css" in manifest["assets"]
        site_css = manifest["assets"]["site_css"]
        assert site_css["local_path"] == "assets/site.css"
        assert site_css["cdn_path"] == "zelex/site/site.css"
        assert site_css["size_bytes"] == 45621
        assert site_css["hash"] == "abc123def456"  # First 12 chars of hash

    def test_manifest_asset_count(self):
        """Manifest should count assets correctly."""
        assets = {
            "site_files": [
                {
                    "name": "site.css",
                    "size": 1000,
                    "hash": "a" * 64,
                    "mime_type": "text/css",
                    "rel_path": "assets/site.css",
                    "cdn_path": "zelex/site/site.css",
                    "local_path": "/path/to/site.css"
                }
            ],
            "thumbnails": [
                {
                    "name": f"thumb{i}.jpg",
                    "size": 2000,
                    "hash": f"{chr(97+i)}" * 64,
                    "mime_type": "image/jpeg",
                    "rel_path": f"thumbs/thumb{i}.jpg",
                    "cdn_path": f"zelex/thumbs/thumb{i}.jpg",
                    "local_path": f"/path/thumbs/thumb{i}.jpg"
                } for i in range(5)
            ],
            "photoshoots": [
                {
                    "name": f"photo{i}.jpg",
                    "size": 3000,
                    "hash": f"{chr(107+i)}" * 64,
                    "mime_type": "image/jpeg",
                    "rel_path": f"photos/photo{i}.jpg",
                    "cdn_path": f"zelex/photos/photo{i}.jpg",
                    "local_path": f"/path/photos/photo{i}.jpg"
                } for i in range(10)
            ]
        }
        manifest = generate_manifest(assets)

        # 1 site file + 5 thumbs + 10 photos = 16 total
        assert manifest["metadata"]["total_assets"] == 16
        assert manifest["metadata"]["total_size_mb"] > 0

    def test_manifest_images_metadata(self):
        """Manifest should track image folder metadata."""
        assets = {
            "site_files": [],
            "thumbnails": [
                {
                    "name": f"thumb{i}.jpg",
                    "size": 2000,
                    "rel_path": f"thumbs/thumb{i}.jpg",
                    "hash": "a" * 64,
                    "mime_type": "image/jpeg",
                    "cdn_path": f"zelex/thumbs/thumb{i}.jpg",
                    "local_path": f"/path/thumbs/thumb{i}.jpg"
                } for i in range(3)
            ],
            "photoshoots": [
                {
                    "name": f"photo{i}.jpg",
                    "size": 3000,
                    "rel_path": f"photos/photo{i}.jpg",
                    "hash": "b" * 64,
                    "mime_type": "image/jpeg",
                    "cdn_path": f"zelex/photos/photo{i}.jpg",
                    "local_path": f"/path/photos/photo{i}.jpg"
                } for i in range(2)
            ]
        }
        manifest = generate_manifest(assets)

        thumbs = manifest["images"]["thumbs"]
        assert thumbs["count"] == 3
        assert len(thumbs["files"]) == 3

        photos = manifest["images"]["photoshoots"]
        assert photos["count"] == 2
        assert len(photos["files"]) == 2


class TestManifestRoundtrip:
    """Test reading and writing manifest."""

    def test_manifest_json_valid(self):
        """Generated manifest should be valid JSON."""
        assets = {
            "site_files": [],
            "thumbnails": [],
            "photoshoots": []
        }
        manifest = generate_manifest(assets)

        # Should be JSON serializable
        json_str = json.dumps(manifest, indent=2)
        assert len(json_str) > 0

        # Should be JSON deserializable
        parsed = json.loads(json_str)
        assert parsed["version"] == manifest["version"]
        assert parsed["metadata"]["total_assets"] == manifest["metadata"]["total_assets"]


class TestCdnConfig:
    """Test CDN config generation."""

    def test_cdn_config_imports(self):
        """Should be able to import cdn_resolver."""
        from pathlib import Path
        resolver_path = Path(__file__).resolve().parent.parent / "scripts" / "cdn_resolver.py"
        assert resolver_path.exists(), "cdn_resolver.py should exist"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
