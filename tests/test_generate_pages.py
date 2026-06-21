"""Tests for generate_pages.py — page inventory validation and manifest generation."""
import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

# Import generate_pages functions
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from generate_pages import (
    build_manifest,
    collect_declared_pages,
    compute_file_hash,
    find_undeclared_pages,
    load_config,
    validate_dependencies,
    validate_files,
)


class TestComputeFileHash:
    """Test file hashing logic."""

    def test_hash_small_file(self, tmp_path):
        """Hash small file (< 400KB)."""
        file_path = tmp_path / "small.txt"
        file_path.write_text("hello world")

        hash_val = compute_file_hash(file_path)
        assert hash_val
        assert len(hash_val) == 16  # sha256 hex, truncated

    def test_hash_nonexistent_file(self, tmp_path):
        """Hash non-existent file returns empty string."""
        file_path = tmp_path / "does_not_exist.txt"
        hash_val = compute_file_hash(file_path)
        assert hash_val == ""

    def test_hash_deterministic(self, tmp_path):
        """Same file content produces same hash."""
        file_path = tmp_path / "test.txt"
        file_path.write_text("content")

        hash1 = compute_file_hash(file_path)
        hash2 = compute_file_hash(file_path)
        assert hash1 == hash2

    def test_hash_different_content(self, tmp_path):
        """Different content produces different hash."""
        file1 = tmp_path / "f1.txt"
        file2 = tmp_path / "f2.txt"
        file1.write_text("content1")
        file2.write_text("content2")

        assert compute_file_hash(file1) != compute_file_hash(file2)


class TestCollectDeclaredPages:
    """Test page collection from config."""

    def test_collect_pages_basic(self):
        """Collect pages from valid config."""
        config = {
            "pages": {
                "primary_nav": {
                    "pages": [
                        {"id": "index", "file": "index.html", "title": "Home"},
                        {"id": "browse", "file": "browse.html", "title": "Browse"},
                    ]
                },
                "content_pages": {
                    "pages": [
                        {"id": "character", "file": "character.html", "title": "Character"},
                    ]
                },
            }
        }

        pages = collect_declared_pages(config)

        assert len(pages) == 3
        assert "index" in pages
        assert "browse" in pages
        assert "character" in pages
        assert pages["index"]["file"] == "index.html"

    def test_collect_pages_missing_id_or_file(self):
        """Skip entries missing id or file."""
        config = {
            "pages": {
                "test": {
                    "pages": [
                        {"id": "valid", "file": "valid.html"},
                        {"file": "no_id.html"},  # Missing id
                        {"id": "no_file"},  # Missing file
                    ]
                }
            }
        }

        pages = collect_declared_pages(config)
        assert len(pages) == 1
        assert "valid" in pages

    def test_collect_pages_empty_config(self):
        """Handle empty pages section."""
        config = {"pages": {}}
        pages = collect_declared_pages(config)
        assert len(pages) == 0

    def test_collect_pages_malformed(self):
        """Handle malformed category (not a dict)."""
        config = {
            "pages": {
                "bad_category": "not a dict"
            }
        }
        pages = collect_declared_pages(config)
        assert len(pages) == 0


class TestValidateFiles:
    """Test file validation logic."""

    def test_validate_all_exist(self, tmp_path):
        """Validate when all files exist."""
        f1 = tmp_path / "page1.html"
        f2 = tmp_path / "page2.html"
        f1.write_text("<html>page1</html>")
        f2.write_text("<html>page2</html>")

        declared = {
            "page1": {"id": "page1", "file": f1.name},
            "page2": {"id": "page2", "file": f2.name},
        }

        with patch("generate_pages.PAGES_DIR", tmp_path):
            metadata, problems = validate_files(declared)

        assert len(metadata) == 2
        assert len(problems) == 0
        assert metadata["page1"]["exists"] is True
        assert metadata["page2"]["exists"] is True

    def test_validate_missing_file(self, tmp_path):
        """Validate with missing file."""
        declared = {
            "missing": {"id": "missing", "file": "missing.html"}
        }

        with patch("generate_pages.PAGES_DIR", tmp_path):
            metadata, problems = validate_files(declared)

        assert len(metadata) == 0
        assert len(problems) == 1
        assert "MISSING" in problems[0]

    def test_validate_file_metadata(self, tmp_path):
        """Validate extracts correct file metadata."""
        file_path = tmp_path / "test.html"
        file_path.write_text("<html>test</html>")

        declared = {"test": {"id": "test", "file": "test.html"}}

        with patch("generate_pages.PAGES_DIR", tmp_path):
            metadata, problems = validate_files(declared)

        assert "test" in metadata
        assert metadata["test"]["exists"] is True
        assert metadata["test"]["size_bytes"] > 0
        assert metadata["test"]["mtime_unix"] > 0
        assert "content_hash" in metadata["test"]
        assert len(problems) == 0


class TestValidateDependencies:
    """Test dependency validation."""

    def test_validate_dependencies_exist(self, tmp_path):
        """Validate dependencies that exist."""
        catalog = tmp_path / "catalog.json"
        catalog.write_text('{"version": 1}')

        declared = {
            "index": {
                "id": "index",
                "file": "index.html",
                "dependencies": ["catalog.json"],
            }
        }

        with patch("generate_pages.DB", tmp_path):
            dep_meta, problems = validate_dependencies(
                {"metadata": {}},
                declared,
                {}
            )

        assert "catalog.json" in dep_meta
        assert dep_meta["catalog.json"]["exists"] is True
        assert len(problems) == 0

    def test_validate_dependencies_missing(self, tmp_path):
        """Report missing dependencies."""
        declared = {
            "index": {
                "id": "index",
                "file": "index.html",
                "dependencies": ["missing.json"],
            }
        }

        with patch("generate_pages.DB", tmp_path):
            dep_meta, problems = validate_dependencies(
                {"metadata": {}},
                declared,
                {}
            )

        assert len(problems) == 1
        assert "MISSING DEPENDENCY" in problems[0]
        assert "missing.json" in problems[0]

    def test_validate_no_dependencies(self):
        """Handle pages with no dependencies."""
        declared = {
            "404": {
                "id": "404",
                "file": "404.html",
                "dependencies": [],
            }
        }

        dep_meta, problems = validate_dependencies(
            {"metadata": {}},
            declared,
            {}
        )

        assert len(dep_meta) == 0
        assert len(problems) == 0


class TestBuildManifest:
    """Test manifest generation."""

    def test_build_manifest_no_problems(self):
        """Build manifest with all validations passing."""
        config = {"schema_version": "1.0", "metadata": {"cache_strategy": "per-page"}}
        declared = {"index": {"id": "index", "file": "index.html"}}
        files = {"index": {"file": "index.html", "size_bytes": 100}}
        deps = {"catalog.json": {"exists": True}}

        manifest = build_manifest(config, declared, files, deps, [])

        assert manifest["schema_version"] == "1.0"
        assert manifest["total_pages"] == 1
        assert manifest["validation"]["all_valid"] is True
        assert manifest["validation"]["problems_count"] == 0
        assert "generated_at" in manifest

    def test_build_manifest_with_problems(self):
        """Build manifest with validation problems."""
        config = {"schema_version": "1.0", "metadata": {}}
        declared = {"index": {"id": "index", "file": "index.html"}}
        files = {}
        deps = {}
        problems = ["MISSING: index.html", "UNDECLARED: contact-variant-b.html"]

        manifest = build_manifest(config, declared, files, deps, problems)

        assert manifest["validation"]["all_valid"] is False
        assert manifest["validation"]["problems_count"] == 2
        assert len(manifest["validation"]["problems"]) == 2

    def test_build_manifest_structure(self):
        """Verify manifest has all required fields."""
        manifest = build_manifest(
            {"schema_version": "1.0", "metadata": {"cache_strategy": "test"}},
            {},
            {},
            {},
            []
        )

        assert "schema_version" in manifest
        assert "generated_at" in manifest
        assert "config_version" in manifest
        assert "total_pages" in manifest
        assert "validation" in manifest
        assert "files" in manifest
        assert "dependencies" in manifest
        assert "cache_strategy" in manifest


class TestFindUndeclaredPages:
    """Test finding undeclared HTML files."""

    def test_find_undeclared_pages(self, tmp_path):
        """Find .html files not in EXPECTED_PAGES."""
        # Create some files
        (tmp_path / "index.html").write_text("<html>")
        (tmp_path / "browse.html").write_text("<html>")
        (tmp_path / "rogue.html").write_text("<html>")
        (tmp_path / "another.html").write_text("<html>")

        # Mock EXPECTED_PAGES to only contain first two
        with patch("generate_pages.PAGES_DIR", tmp_path):
            with patch("generate_pages.EXPECTED_PAGES", ["index.html", "browse.html"]):
                undeclared = find_undeclared_pages()

        assert len(undeclared) == 2
        assert "rogue.html" in undeclared
        assert "another.html" in undeclared

    def test_find_undeclared_pages_all_declared(self, tmp_path):
        """All files are declared."""
        (tmp_path / "index.html").write_text("<html>")
        (tmp_path / "browse.html").write_text("<html>")

        with patch("generate_pages.PAGES_DIR", tmp_path):
            with patch("generate_pages.EXPECTED_PAGES", ["index.html", "browse.html"]):
                undeclared = find_undeclared_pages()

        assert len(undeclared) == 0


class TestIntegration:
    """Integration tests for full pipeline."""

    def test_full_validation_pipeline(self, tmp_path):
        """Test full validation workflow."""
        # Create config
        config = {
            "schema_version": "1.0",
            "pages": {
                "primary_nav": {
                    "pages": [
                        {
                            "id": "index",
                            "file": "index.html",
                            "title": "Home",
                            "dependencies": ["catalog.json"],
                        }
                    ]
                }
            },
            "metadata": {"cache_strategy": "per-page TTL"},
        }

        # Create files
        (tmp_path / "index.html").write_text("<html>home</html>")
        (tmp_path / "catalog.json").write_text('{"version": 1}')

        # Mock paths
        with patch("generate_pages.CONFIG", tmp_path / "config.json"):
            with patch("generate_pages.PAGES_DIR", tmp_path):
                with patch("generate_pages.DB", tmp_path):
                    # Load and validate
                    declared = collect_declared_pages(config)
                    files, file_probs = validate_files(declared)
                    deps, dep_probs = validate_dependencies(config, declared, files)
                    manifest = build_manifest(config, declared, files, deps, file_probs + dep_probs)

        assert len(declared) == 1
        assert len(files) == 1
        assert len(deps) == 1
        assert manifest["validation"]["all_valid"] is True

    def test_validation_with_missing_dependency(self, tmp_path):
        """Test when dependency is missing."""
        config = {
            "schema_version": "1.0",
            "pages": {
                "test": {
                    "pages": [
                        {
                            "id": "browse",
                            "file": "browse.html",
                            "dependencies": ["characters.json"],
                        }
                    ]
                }
            },
            "metadata": {},
        }

        (tmp_path / "browse.html").write_text("<html>")
        # Note: characters.json is NOT created

        with patch("generate_pages.PAGES_DIR", tmp_path):
            with patch("generate_pages.DB", tmp_path):
                declared = collect_declared_pages(config)
                files, file_probs = validate_files(declared)
                deps, dep_probs = validate_dependencies(config, declared, files)

        assert len(dep_probs) > 0
        assert any("characters.json" in p for p in dep_probs)
