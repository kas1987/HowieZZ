"""
Tests for scripts/build_characters.py — torso detection, factory-image
filtering, and tagline generation.

No DB or file I/O required.
"""
import pytest
from build_characters import is_torso, is_factory, tagline, TORSO_CODES


# ---------------------------------------------------------------------------
# is_torso()
# ---------------------------------------------------------------------------

class TestIsTorso:

    # -- known torso codes ----------------------------------------------------

    @pytest.mark.parametrize("code", list(TORSO_CODES))
    def test_known_torso_codes_are_torso(self, code):
        assert is_torso(code, 999) is True  # height irrelevant for known list

    # -- height threshold -----------------------------------------------------

    def test_height_below_150_is_torso(self):
        assert is_torso("ZX999Z", 149) is True

    def test_height_exactly_150_is_not_torso(self):
        # threshold is < 150 (strict)
        assert is_torso("ZX999Z", 150) is False

    def test_height_above_150_is_not_torso(self):
        assert is_torso("ZX999Z", 165) is False

    def test_height_none_is_not_torso(self):
        # None height: is_torso can't determine by height alone → not torso
        assert is_torso("ZX999Z", None) is False

    # -- normal bodies --------------------------------------------------------

    def test_regular_i_series_body_not_torso(self):
        assert is_torso("ZG170D", 170) is False

    def test_regular_k_series_body_not_torso(self):
        assert is_torso("ZK168B", 168) is False


# ---------------------------------------------------------------------------
# is_factory()
# ---------------------------------------------------------------------------

class TestIsFactory:

    # -- paths that are definitely factory / catalog images ------------------

    def test_heads_path_is_factory(self):
        # Use a -101-indexed filename so the path check is the gating condition,
        # not the PHOTO_RE fallback (which would also return True for non-indexed names).
        assert is_factory("GE03_1-Fair-101.jpg", "Heads/Hard/GE03_1-Fair-101.jpg") is True

    def test_specs_path_is_factory(self):
        assert is_factory("ZG162D-101.webp", "I-Series/specs/ZG162D-101.webp") is True

    def test_measure_path_is_factory(self):
        assert is_factory("ZK168B-101.webp", "Measure/ZK168B-101.webp") is True

    def test_uppercase_paths_detected(self):
        assert is_factory("foo.jpg", "I-Series/SPECS/bar.jpg") is True

    def test_windows_backslash_path_detected(self):
        assert is_factory("foo.jpg", "Heads\\Hard\\foo.jpg") is True

    # -- files without a photo-index (-NNN) are factory ----------------------

    def test_plain_filename_without_index_is_factory(self):
        assert is_factory("GE149_1_GE74MJ_ZG170D.jpg", None) is True

    def test_none_filename_is_factory(self):
        assert is_factory(None, None) is True

    # -- real photoshoot frames have -NNN index ------------------------------

    def test_photoshoot_frame_101(self):
        assert is_factory("GE149_1_GE74MJ_ZG170D-101.jpg", "I-Series/GE149_1_GE74MJ_ZG170D/GE149_1_GE74MJ_ZG170D-101.jpg") is False

    def test_photoshoot_frame_205(self):
        assert is_factory("shoot-205.jpg", "K-Series/KE03_1+ZK168B/shoot-205.jpg") is False

    def test_photoshoot_frame_two_digit_is_enough(self):
        # PHOTO_RE requires 2–4 digits; 2-digit index IS accepted as a photoshoot frame
        assert is_factory("shoot-10.jpg", "I-Series/shoot/shoot-10.jpg") is False

    def test_photoshoot_with_none_path(self):
        # path is None but filename has -NNN → photoshoot, not factory
        assert is_factory("shot-101.jpg", None) is False


# ---------------------------------------------------------------------------
# tagline()
# ---------------------------------------------------------------------------

class TestTagline:

    # -- template substitution -----------------------------------------------

    def test_height_interpolated(self):
        result = tagline("The Muse", "B", 170, 1)
        assert "170" in result

    def test_cup_interpolated(self):
        result = tagline("The Siren", "K", 165, 2)
        assert "K" in result

    def test_empress_slot_3_cup_appears(self):
        result = tagline("The Empress", "J", 160, 3)
        assert "J" in result

    # -- slot cycling ---------------------------------------------------------

    def test_slot_1_and_5_same_for_four_entry_pool(self):
        # Classic has 4 taglines; slot 5 wraps to slot 1
        t1 = tagline("The Classic", "B", 165, 1)
        t5 = tagline("The Classic", "B", 165, 5)
        assert t1 == t5

    def test_slot_2_and_6_same_for_four_entry_pool(self):
        t2 = tagline("The Classic", "B", 165, 2)
        t6 = tagline("The Classic", "B", 165, 6)
        assert t2 == t6

    def test_different_slots_have_different_taglines(self):
        tags = [tagline("The Classic", "B", 165, s) for s in range(1, 5)]
        assert len(set(tags)) == 4  # all four are distinct

    # -- unknown family falls back to default pool ---------------------------

    def test_unknown_family_returns_string(self):
        result = tagline(None, "B", 165, 1)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_unknown_family_slots_cycle(self):
        t1 = tagline("Nonexistent", "B", 165, 1)
        t5 = tagline("Nonexistent", "B", 165, 5)
        assert t1 == t5

    # -- all families produce non-empty strings ------------------------------

    @pytest.mark.parametrize("family", [
        "The Classic", "The Icon", "The Muse", "The Siren",
        "The Athlete", "The Empress", "The Sculpt",
    ])
    def test_all_families_return_nonempty_string(self, family):
        for slot in range(1, 5):
            result = tagline(family, "D", 165, slot)
            assert isinstance(result, str) and len(result) > 0
