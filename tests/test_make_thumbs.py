"""
Tests for scripts/make_thumbs.py — thumbnail generation and path handling.

Tests cover:
- thumb_rel() — path transformation logic (pure function)
- make() — thumbnail generation with caching and PIL integration
- main() — orchestration of body_profiles.json and characters.json processing
"""
import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
import make_thumbs


# ---------------------------------------------------------------------------
# thumb_rel() — pure function tests
# ---------------------------------------------------------------------------

class TestThumbRel:
    """Test path transformation logic for thumb_rel()."""

    def test_assets_prefix_stripped(self):
        """assets/images/foo.jpg → assets/thumbs/images/foo.jpg"""
        result = make_thumbs.thumb_rel("assets/images/foo.jpg")
        assert result == "assets/thumbs/images/foo.jpg"

    def test_nested_assets_path_stripped(self):
        """assets/a/b/c.jpg → assets/thumbs/a/b/c.jpg"""
        result = make_thumbs.thumb_rel("assets/a/b/c.jpg")
        assert result == "assets/thumbs/a/b/c.jpg"

    def test_no_assets_prefix_prepended(self):
        """Path without 'assets' prefix gets assets/thumbs/ prepended"""
        result = make_thumbs.thumb_rel("images/foo.jpg")
        assert result == "assets/thumbs/images/foo.jpg"

    def test_single_filename_no_directory(self):
        """foo.jpg → assets/thumbs/foo.jpg"""
        result = make_thumbs.thumb_rel("foo.jpg")
        assert result == "assets/thumbs/foo.jpg"

    def test_backslash_replaced_with_forward_slash(self):
        """Backslash paths (Windows) are normalized to forward slashes"""
        result = make_thumbs.thumb_rel("assets\\images\\foo.jpg")
        assert result == "assets/thumbs/images/foo.jpg"
        assert "\\" not in result

    def test_mixed_slashes_normalized(self):
        """Mixed slashes are normalized to forward slashes"""
        result = make_thumbs.thumb_rel("assets\\a/b\\c.jpg")
        assert "/" in result and "\\" not in result


# ---------------------------------------------------------------------------
# make() — cache and file handling
# ---------------------------------------------------------------------------

class TestMakeCache:
    """Test cache hit behavior."""

    def test_cache_hit_returns_cached_value(self, tmp_path):
        """If rel is in cache, return cache[rel] without any I/O."""
        with patch.object(make_thumbs, 'ROOT', tmp_path):
            cache = {"assets/images/foo.jpg": "assets/thumbs/images/foo.jpg"}
            result = make_thumbs.make("assets/images/foo.jpg", cache)
            assert result == "assets/thumbs/images/foo.jpg"

    def test_cache_hit_with_empty_string(self, tmp_path):
        """Cache hit with empty string value."""
        with patch.object(make_thumbs, 'ROOT', tmp_path):
            cache = {"foo.jpg": ""}
            result = make_thumbs.make("foo.jpg", cache)
            assert result == ""

    def test_cache_hit_unchanged_by_file_state(self, tmp_path):
        """Cache returns value even if source file doesn't exist."""
        with patch.object(make_thumbs, 'ROOT', tmp_path):
            cache = {"nonexistent.jpg": "cached/result.jpg"}
            result = make_thumbs.make("nonexistent.jpg", cache)
            assert result == "cached/result.jpg"

    def test_cache_hit_no_pil_call(self, tmp_path):
        """Cache hit does not trigger PIL or filesystem operations."""
        with patch.object(make_thumbs, 'ROOT', tmp_path):
            with patch('make_thumbs.Image') as mock_image:
                cache = {"test.jpg": "assets/thumbs/test.jpg"}
                make_thumbs.make("test.jpg", cache)
                mock_image.open.assert_not_called()

    def test_cache_hit_no_file_creation(self, tmp_path):
        """Cache hit does not create thumb files."""
        with patch.object(make_thumbs, 'ROOT', tmp_path):
            cache = {"test.jpg": "assets/thumbs/test.jpg"}
            make_thumbs.make("test.jpg", cache)
            assert not list(tmp_path.glob("**/*.jpg"))

    def test_multiple_cache_hits_return_correctly(self, tmp_path):
        """Multiple entries in cache are returned correctly."""
        with patch.object(make_thumbs, 'ROOT', tmp_path):
            cache = {
                "foo.jpg": "assets/thumbs/foo.jpg",
                "bar.jpg": "assets/thumbs/bar.jpg",
                "baz.jpg": "assets/thumbs/baz.jpg",
            }
            for rel, expected in cache.items():
                result = make_thumbs.make(rel, cache)
                assert result == expected


class TestMakeMissingSource:
    """Test behavior when source file doesn't exist."""

    def test_missing_source_returns_original_rel(self, tmp_path):
        """If source file doesn't exist, return rel unchanged."""
        with patch.object(make_thumbs, 'ROOT', tmp_path):
            cache = {}
            result = make_thumbs.make("assets/images/missing.jpg", cache)
            assert result == "assets/images/missing.jpg"

    def test_missing_source_stored_in_cache(self, tmp_path):
        """Missing source is stored in cache with original rel value."""
        with patch.object(make_thumbs, 'ROOT', tmp_path):
            cache = {}
            make_thumbs.make("assets/images/missing.jpg", cache)
            assert cache["assets/images/missing.jpg"] == "assets/images/missing.jpg"


class TestMakeThumbExists:
    """Test behavior when thumb file already exists."""

    def test_existing_thumb_not_regenerated(self, tmp_path):
        """If thumb exists, don't call PIL to regenerate it."""
        with patch.object(make_thumbs, 'ROOT', tmp_path):
            # Create source and thumb files
            src = tmp_path / "images" / "foo.jpg"
            src.parent.mkdir(parents=True)
            src.write_text("fake image")

            thumb = tmp_path / "assets" / "thumbs" / "images" / "foo.jpg"
            thumb.parent.mkdir(parents=True)
            thumb.write_text("fake thumb")

            cache = {}
            with patch('make_thumbs.Image') as mock_image:
                result = make_thumbs.make("images/foo.jpg", cache)
                # PIL should not be called
                mock_image.open.assert_not_called()
                assert result == "assets/thumbs/images/foo.jpg"

    def test_existing_thumb_returns_thumb_path(self, tmp_path):
        """Return thumb path even if PIL is not called."""
        with patch.object(make_thumbs, 'ROOT', tmp_path):
            src = tmp_path / "images" / "foo.jpg"
            src.parent.mkdir(parents=True)
            src.write_text("fake image")

            thumb = tmp_path / "assets" / "thumbs" / "images" / "foo.jpg"
            thumb.parent.mkdir(parents=True)
            thumb.write_text("fake thumb")

            cache = {}
            result = make_thumbs.make("images/foo.jpg", cache)
            assert result == "assets/thumbs/images/foo.jpg"


class TestMakePILCalled:
    """Test PIL is called when creating new thumbs."""

    def test_pil_called_for_new_thumb(self, tmp_path):
        """When thumb doesn't exist, PIL is used to create it."""
        with patch.object(make_thumbs, 'ROOT', tmp_path):
            src = tmp_path / "images" / "foo.jpg"
            src.parent.mkdir(parents=True)
            src.write_text("fake image")

            mock_image = MagicMock()
            mock_image.__enter__ = lambda s: mock_image
            mock_image.__exit__ = MagicMock(return_value=False)
            mock_image.size = (800, 600)
            mock_image.convert.return_value = mock_image

            with patch('make_thumbs.Image') as MockImage:
                MockImage.open.return_value = mock_image
                cache = {}
                result = make_thumbs.make("images/foo.jpg", cache)

                MockImage.open.assert_called_once()
                assert result == "assets/thumbs/images/foo.jpg"

    def test_pil_save_called_with_correct_params(self, tmp_path):
        """PIL save is called with JPEG format and quality 82."""
        with patch.object(make_thumbs, 'ROOT', tmp_path):
            src = tmp_path / "images" / "foo.jpg"
            src.parent.mkdir(parents=True)
            src.write_text("fake image")

            mock_image = MagicMock()
            mock_image.__enter__ = lambda s: mock_image
            mock_image.__exit__ = MagicMock(return_value=False)
            mock_image.size = (800, 600)
            mock_image.convert.return_value = mock_image

            with patch('make_thumbs.Image') as MockImage:
                MockImage.open.return_value = mock_image
                cache = {}
                make_thumbs.make("images/foo.jpg", cache)

                mock_image.save.assert_called_once()
                args = mock_image.save.call_args
                assert args[0][1] == "JPEG"
                assert args[1]["quality"] == 82


class TestMakePILException:
    """Test exception handling during PIL operations."""

    def test_pil_exception_returns_original_rel(self, tmp_path):
        """If PIL raises exception, return rel unchanged."""
        with patch.object(make_thumbs, 'ROOT', tmp_path):
            src = tmp_path / "images" / "corrupted.jpg"
            src.parent.mkdir(parents=True)
            src.write_text("corrupted data")

            with patch('make_thumbs.Image') as MockImage:
                MockImage.open.side_effect = Exception("Corrupted image")
                cache = {}
                result = make_thumbs.make("images/corrupted.jpg", cache)
                assert result == "images/corrupted.jpg"

    def test_pil_exception_stored_in_cache(self, tmp_path, capsys):
        """Exception case is stored in cache with original rel."""
        with patch.object(make_thumbs, 'ROOT', tmp_path):
            src = tmp_path / "images" / "corrupted.jpg"
            src.parent.mkdir(parents=True)
            src.write_text("corrupted")

            with patch('make_thumbs.Image') as MockImage:
                MockImage.open.side_effect = Exception("Corrupted")
                cache = {}
                make_thumbs.make("images/corrupted.jpg", cache)
                assert cache["images/corrupted.jpg"] == "images/corrupted.jpg"

    def test_pil_exception_prints_warning(self, tmp_path, capsys):
        """Warning is printed when PIL raises exception."""
        with patch.object(make_thumbs, 'ROOT', tmp_path):
            src = tmp_path / "images" / "bad.jpg"
            src.parent.mkdir(parents=True)
            src.write_text("bad")

            with patch('make_thumbs.Image') as MockImage:
                MockImage.open.side_effect = Exception("Bad image")
                cache = {}
                make_thumbs.make("images/bad.jpg", cache)
                captured = capsys.readouterr()
                assert "[warn]" in captured.out
                assert "bad.jpg" in captured.out


class TestMakeResizeLogic:
    """Test image resize conditional logic."""

    def test_width_under_520_skips_resize(self, tmp_path):
        """If image width <= 520, resize is not called."""
        with patch.object(make_thumbs, 'ROOT', tmp_path):
            src = tmp_path / "images" / "small.jpg"
            src.parent.mkdir(parents=True)
            src.write_text("small")

            mock_image = MagicMock()
            mock_image.__enter__ = lambda s: mock_image
            mock_image.__exit__ = MagicMock(return_value=False)
            mock_image.size = (400, 300)
            mock_image.convert.return_value = mock_image

            with patch('make_thumbs.Image') as MockImage:
                MockImage.open.return_value = mock_image
                cache = {}
                make_thumbs.make("images/small.jpg", cache)
                mock_image.resize.assert_not_called()

    def test_width_exactly_520_skips_resize(self, tmp_path):
        """If image width == 520, resize is not called."""
        with patch.object(make_thumbs, 'ROOT', tmp_path):
            src = tmp_path / "images" / "exact.jpg"
            src.parent.mkdir(parents=True)
            src.write_text("exact")

            mock_image = MagicMock()
            mock_image.__enter__ = lambda s: mock_image
            mock_image.__exit__ = MagicMock(return_value=False)
            mock_image.size = (520, 800)
            mock_image.convert.return_value = mock_image

            with patch('make_thumbs.Image') as MockImage:
                MockImage.open.return_value = mock_image
                cache = {}
                make_thumbs.make("images/exact.jpg", cache)
                mock_image.resize.assert_not_called()

    def test_width_over_520_triggers_resize(self, tmp_path):
        """If image width > 520, resize is called."""
        with patch.object(make_thumbs, 'ROOT', tmp_path):
            src = tmp_path / "images" / "large.jpg"
            src.parent.mkdir(parents=True)
            src.write_text("large")

            mock_image = MagicMock()
            mock_image.__enter__ = lambda s: mock_image
            mock_image.__exit__ = MagicMock(return_value=False)
            mock_image.size = (1000, 800)
            mock_image.convert.return_value = mock_image
            mock_image.resize.return_value = mock_image

            with patch('make_thumbs.Image') as MockImage:
                MockImage.open.return_value = mock_image
                MockImage.LANCZOS = 1
                cache = {}
                make_thumbs.make("images/large.jpg", cache)
                mock_image.resize.assert_called_once()

    def test_resize_maintains_aspect_ratio(self, tmp_path):
        """Resize maintains aspect ratio: new_height = h * (WIDTH / w)"""
        with patch.object(make_thumbs, 'ROOT', tmp_path):
            src = tmp_path / "images" / "wide.jpg"
            src.parent.mkdir(parents=True)
            src.write_text("wide")

            mock_image = MagicMock()
            mock_image.__enter__ = lambda s: mock_image
            mock_image.__exit__ = MagicMock(return_value=False)
            mock_image.size = (1000, 800)
            mock_image.convert.return_value = mock_image
            mock_image.resize.return_value = mock_image

            with patch('make_thumbs.Image') as MockImage:
                MockImage.open.return_value = mock_image
                MockImage.LANCZOS = 1
                cache = {}
                make_thumbs.make("images/wide.jpg", cache)

                # Expected: (520, 800 * 520 / 1000) = (520, 416)
                call_args = mock_image.resize.call_args
                assert call_args[0][0] == (520, 416)


class TestMakeCachePopulation:
    """Test that cache is populated after successful make()."""

    def test_cache_populated_on_new_thumb(self, tmp_path):
        """After successful make(), cache[rel] is set."""
        with patch.object(make_thumbs, 'ROOT', tmp_path):
            src = tmp_path / "images" / "foo.jpg"
            src.parent.mkdir(parents=True)
            src.write_text("foo")

            mock_image = MagicMock()
            mock_image.__enter__ = lambda s: mock_image
            mock_image.__exit__ = MagicMock(return_value=False)
            mock_image.size = (800, 600)
            mock_image.convert.return_value = mock_image

            with patch('make_thumbs.Image') as MockImage:
                MockImage.open.return_value = mock_image
                cache = {}
                make_thumbs.make("images/foo.jpg", cache)
                assert "images/foo.jpg" in cache
                assert cache["images/foo.jpg"] == "assets/thumbs/images/foo.jpg"


class TestMakeThumbDirCreated:
    """Test that thumb directory is created."""

    def test_thumb_dir_created_on_successful_make(self, tmp_path):
        """After successful make(), thumb parent directory exists."""
        with patch.object(make_thumbs, 'ROOT', tmp_path):
            src = tmp_path / "images" / "foo.jpg"
            src.parent.mkdir(parents=True)
            src.write_text("foo")

            mock_image = MagicMock()
            mock_image.__enter__ = lambda s: mock_image
            mock_image.__exit__ = MagicMock(return_value=False)
            mock_image.size = (800, 600)
            mock_image.convert.return_value = mock_image

            with patch('make_thumbs.Image') as MockImage:
                MockImage.open.return_value = mock_image
                cache = {}
                make_thumbs.make("images/foo.jpg", cache)

                thumb_dir = tmp_path / "assets" / "thumbs" / "images"
                assert thumb_dir.exists()


# ---------------------------------------------------------------------------
# main() — orchestration tests
# ---------------------------------------------------------------------------

class TestMainMissingFiles:
    """Test main() when JSON files don't exist."""

    def test_main_handles_missing_json_files(self, tmp_path):
        """main() runs without error if both JSON files are missing."""
        with patch.object(make_thumbs, 'ROOT', tmp_path):
            with patch.object(make_thumbs, 'BODY_PROFILES', tmp_path / "missing_profiles.json"):
                with patch.object(make_thumbs, 'CHARACTERS', tmp_path / "missing_characters.json"):
                    # Should not raise any exception
                    make_thumbs.main()


class TestMainCharactersJson:
    """Test main() processing of characters.json."""

    def test_main_adds_hero_thumb_to_character(self, tmp_path):
        """main() adds hero_thumb to photoshoot if hero exists."""
        with patch.object(make_thumbs, 'ROOT', tmp_path):
            # Create characters.json
            chars_file = tmp_path / "characters.json"
            data = {
                "characters": [
                    {
                        "id": "char1",
                        "photoshoot": {
                            "hero": "assets/images/char1.jpg"
                        }
                    }
                ]
            }
            chars_file.write_text(json.dumps(data), encoding="utf-8")

            # Create source image
            src = tmp_path / "assets" / "images" / "char1.jpg"
            src.parent.mkdir(parents=True)
            src.write_text("fake")

            with patch.object(make_thumbs, 'CHARACTERS', chars_file):
                mock_image = MagicMock()
                mock_image.__enter__ = lambda s: mock_image
                mock_image.__exit__ = MagicMock(return_value=False)
                mock_image.size = (800, 600)
                mock_image.convert.return_value = mock_image

                with patch('make_thumbs.Image') as MockImage:
                    MockImage.open.return_value = mock_image
                    make_thumbs.main()

            # Verify JSON was updated
            updated = json.loads(chars_file.read_text(encoding="utf-8"))
            assert "hero_thumb" in updated["characters"][0]["photoshoot"]

    def test_main_processes_empty_photoshoot(self, tmp_path):
        """main() handles character with empty/missing photoshoot."""
        with patch.object(make_thumbs, 'ROOT', tmp_path):
            chars_file = tmp_path / "characters.json"
            data = {
                "characters": [
                    {
                        "id": "char1",
                        "photoshoot": None
                    }
                ]
            }
            chars_file.write_text(json.dumps(data), encoding="utf-8")

            with patch.object(make_thumbs, 'CHARACTERS', chars_file):
                make_thumbs.main()

            # Should complete without error
            updated = json.loads(chars_file.read_text(encoding="utf-8"))
            assert updated["characters"][0]["photoshoot"] is None or isinstance(updated["characters"][0]["photoshoot"], dict)


class TestMainBodyProfilesJson:
    """Test main() processing of body_profiles.json."""

    def test_main_adds_hero_thumb_to_profile(self, tmp_path):
        """main() adds hero_thumb to profile if hero_image exists."""
        with patch.object(make_thumbs, 'ROOT', tmp_path):
            # Create body_profiles.json
            profiles_file = tmp_path / "body_profiles.json"
            data = {
                "profiles": [
                    {
                        "family": "The Classic",
                        "hero_image": "assets/images/classic.jpg"
                    }
                ]
            }
            profiles_file.write_text(json.dumps(data), encoding="utf-8")

            # Create source image
            src = tmp_path / "assets" / "images" / "classic.jpg"
            src.parent.mkdir(parents=True)
            src.write_text("fake")

            with patch.object(make_thumbs, 'BODY_PROFILES', profiles_file):
                mock_image = MagicMock()
                mock_image.__enter__ = lambda s: mock_image
                mock_image.__exit__ = MagicMock(return_value=False)
                mock_image.size = (800, 600)
                mock_image.convert.return_value = mock_image

                with patch('make_thumbs.Image') as MockImage:
                    MockImage.open.return_value = mock_image
                    make_thumbs.main()

            # Verify JSON was updated
            updated = json.loads(profiles_file.read_text(encoding="utf-8"))
            assert "hero_thumb" in updated["profiles"][0]
