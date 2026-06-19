"""
Tests for scripts/build_profiles.py — the body-family classification engine.

These are pure-function unit tests; no file I/O or DB required.
"""
import pytest
from build_profiles import center, in_range, classify, FAMILIES


# ---------------------------------------------------------------------------
# center()
# ---------------------------------------------------------------------------

class TestCenter:
    def test_symmetric_range(self):
        assert center((0.0, 1.0)) == pytest.approx(0.5)

    def test_real_whr_range(self):
        assert center((0.68, 0.72)) == pytest.approx(0.70)

    def test_real_bwr_range(self):
        assert center((1.40, 1.50)) == pytest.approx(1.45)

    def test_single_point(self):
        assert center((0.5, 0.5)) == pytest.approx(0.5)

    def test_asymmetric(self):
        assert center((1.60, 1.75)) == pytest.approx(1.675)


# ---------------------------------------------------------------------------
# in_range()
# ---------------------------------------------------------------------------

class TestInRange:
    def test_midpoint_in_range(self):
        assert in_range(0.70, (0.68, 0.72)) is True

    def test_lower_boundary_inclusive(self):
        assert in_range(0.68, (0.68, 0.72)) is True

    def test_upper_boundary_inclusive(self):
        assert in_range(0.72, (0.68, 0.72)) is True

    def test_just_below_lower(self):
        assert in_range(0.6799, (0.68, 0.72)) is False

    def test_just_above_upper(self):
        assert in_range(0.7201, (0.68, 0.72)) is False

    def test_far_below(self):
        assert in_range(0.50, (0.68, 0.72)) is False

    def test_far_above(self):
        assert in_range(0.99, (0.68, 0.72)) is False

    def test_bwr_range(self):
        assert in_range(1.55, (1.50, 1.60)) is True

    def test_zero_width_range_on_boundary(self):
        assert in_range(0.5, (0.5, 0.5)) is True

    def test_zero_width_range_off(self):
        assert in_range(0.51, (0.5, 0.5)) is False


# ---------------------------------------------------------------------------
# classify()
#
# Family ranges (from build_profiles.FAMILIES):
#   The Classic:  WHR (0.68–0.72), BWR (1.40–1.50)
#   The Icon:     WHR (0.60–0.65), BWR (1.50–1.60)
#   The Muse:     WHR (0.65–0.70), BWR (1.30–1.40)
#   The Siren:    WHR (0.55–0.60), BWR (1.60–1.75)
#   The Empress:  WHR (0.58–0.64), BWR (1.55–1.65)
#   The Sculpt:   WHR (0.65–0.68), BWR (1.45–1.55)
# ---------------------------------------------------------------------------

class TestClassify:

    # -- exact match: one family contains both axes ---------------------------

    @pytest.mark.parametrize("family,whr,bwr", [
        # Points chosen to lie inside exactly ONE family's box
        ("The Classic", 0.70, 1.42),    # Classic only (Muse excluded: BWR 1.42 > 1.40)
        ("The Icon",    0.62, 1.52),    # Icon only   (Empress excluded: BWR 1.52 < 1.55)
        ("The Muse",    0.675, 1.35),   # Muse only   (Sculpt excluded: BWR 1.35 < 1.45)
        ("The Siren",   0.575, 1.675),  # Siren only  (Empress excluded: WHR 0.575 < 0.58)
        ("The Empress", 0.585, 1.58),   # Empress only (Siren excluded: BWR 1.58 < 1.60)
        ("The Sculpt",  0.665, 1.50),   # Sculpt only  (Muse excluded: BWR 1.50 > 1.40)
    ])
    def test_exact_match_all_families(self, family, whr, bwr):
        name, conf, meta = classify(whr, bwr)
        assert name == family
        assert conf == "exact"

    def test_meta_is_complete_tuple(self):
        _, _, meta = classify(0.70, 1.42)
        assert meta[0] == "The Classic"
        assert len(meta) == 6  # (name, whr_range, bwr_range, silhouette, premium, target)

    def test_meta_ranges_match_families_constant(self):
        name, _, meta = classify(0.70, 1.42)
        expected = next(f for f in FAMILIES if f[0] == name)
        assert meta == expected

    # -- exact-tie: two families contain the same point ----------------------

    def test_exact_tie_classic_sculpt_overlap(self):
        # WHR=0.68 lies in both Classic (0.68–0.72) and Sculpt (0.65–0.68)
        # BWR=1.47 lies in both Classic (1.40–1.50) and Sculpt (1.45–1.55)
        name, conf, _ = classify(0.68, 1.47)
        assert conf == "exact-tie"
        assert name in ("The Classic", "The Sculpt")

    def test_exact_tie_returns_nearest_center(self):
        # At (0.68, 1.47), distances to each family centre:
        #   Classic centre (0.70, 1.45): |0.02|/0.05 + |0.02|/0.10 = 0.40 + 0.20 = 0.60
        #   Sculpt  centre (0.665, 1.50): |0.015|/0.05 + |0.03|/0.10 = 0.30 + 0.30 = 0.60
        # Tied — min() returns the first in iteration order (The Classic).
        name, conf, _ = classify(0.68, 1.47)
        assert conf == "exact-tie"
        # Python min is stable: Classic appears first in FAMILIES list
        assert name == "The Classic"

    # -- near match: no exact range but one axis is in the best family --------

    def test_near_match_whr_in_range_bwr_outside(self):
        # WHR=0.70 is inside Classic's WHR range; BWR=2.00 is outside everything
        name, conf, _ = classify(0.70, 2.00)
        assert conf == "near"

    def test_near_match_bwr_in_range_whr_outside(self):
        # BWR=1.45 in Classic range; WHR=0.90 is outside all ranges
        name, conf, _ = classify(0.90, 1.45)
        assert conf == "near"

    # -- loose match: both axes outside every family --------------------------

    def test_loose_match_both_axes_outside(self):
        # WHR=0.90, BWR=2.00 is outside every single family box
        _, conf, _ = classify(0.90, 2.00)
        assert conf == "loose"

    def test_loose_match_very_low_whr_bwr(self):
        _, conf, _ = classify(0.20, 0.50)
        assert conf == "loose"

    # -- return structure consistency ----------------------------------------

    def test_returns_three_tuple(self):
        result = classify(0.70, 1.45)
        assert len(result) == 3

    def test_name_is_string(self):
        name, _, _ = classify(0.65, 1.40)
        assert isinstance(name, str)
        assert name.startswith("The ")

    def test_confidence_valid_values(self):
        valid = {"exact", "exact-tie", "near", "loose"}
        for whr, bwr in [(0.70, 1.45), (0.68, 1.47), (0.70, 2.00), (0.90, 2.00)]:
            _, conf, _ = classify(whr, bwr)
            assert conf in valid
