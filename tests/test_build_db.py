"""
Tests for scripts/build_db.py — all pure parsing/helper functions.

No file I/O, no database, no network.  Module-level code in build_db.py reads
db/body_measurements.json once on import; that file is part of the repo so it
is always present in CI and local checkouts.
"""
import pytest
from build_db import (
    parse_i_folder, parse_k_folder, parse_fusion_folder, parse_sle_folder,
    decode_body, parse_head_filename, parse_body_spec, parse_option,
    seq, body_series, canon_body,
)


# ---------------------------------------------------------------------------
# parse_i_folder  →  (head, face, body, shoot)
# ---------------------------------------------------------------------------

class TestParseIFolder:

    def test_full_form_with_face_and_body(self):
        head, face, body, shoot = parse_i_folder("GE149_1_GE74MJ_ZG170D")
        assert head == "GE149_1"
        assert face == "GE74MJ"
        assert body == "ZG170D"
        assert shoot is None

    def test_head_only(self):
        head, face, body, shoot = parse_i_folder("GE52_1")
        assert head == "GE52_1"
        assert face is None
        assert body is None
        assert shoot is None

    def test_with_shoot_index(self):
        _, _, _, shoot = parse_i_folder("GE149_1_GE74MJ_ZG170D-2")
        assert shoot == 2

    def test_shoot_index_larger(self):
        _, _, _, shoot = parse_i_folder("GE52_1-10")
        assert shoot == 10

    def test_body_with_zgx_prefix(self):
        _, _, body, _ = parse_i_folder("GE52_1_GE30MJ_ZGX165F")
        assert body == "ZGX165F"

    def test_no_face_code(self):
        head, face, body, shoot = parse_i_folder("GE82_3_ZG162D")
        assert head == "GE82_3"
        assert face is None
        assert body == "ZG162D"

    def test_empty_string_returns_nones(self):
        head, face, body, shoot = parse_i_folder("")
        assert head is None
        assert face is None
        assert body is None
        assert shoot is None


# ---------------------------------------------------------------------------
# parse_k_folder  →  (head, face, body, shoot)
# ---------------------------------------------------------------------------

class TestParseKFolder:

    def test_standard_form(self):
        head, face, body, shoot = parse_k_folder("KE03_1+ZK168B-1")
        assert head == "KE03_1"
        assert face is None
        assert body == "ZK168B"
        assert shoot == 1

    def test_no_shoot_index(self):
        head, face, body, shoot = parse_k_folder("KE03_1+ZK168B")
        assert head == "KE03_1"
        assert body == "ZK168B"
        assert shoot is None

    def test_different_body_code(self):
        _, _, body, _ = parse_k_folder("KE12_3+ZK159D-2")
        assert body == "ZK159D"

    def test_face_always_none(self):
        _, face, _, _ = parse_k_folder("KE03_1+ZK168B-1")
        assert face is None

    def test_no_body_present(self):
        head, face, body, shoot = parse_k_folder("KE03_1")
        assert head == "KE03_1"
        assert body is None

    def test_empty_string_returns_nones(self):
        head, face, body, shoot = parse_k_folder("")
        assert all(x is None for x in (head, face, body, shoot))


# ---------------------------------------------------------------------------
# parse_fusion_folder  →  (head, face, body, shoot)
# ---------------------------------------------------------------------------

class TestParseFusionFolder:

    def test_standard_form(self):
        head, face, body, shoot = parse_fusion_folder("ZFE01_1+ZF168B")
        assert head == "ZFE01_1"
        assert face is None
        assert body == "ZF168B"
        assert shoot is None

    def test_with_shoot_index(self):
        _, _, _, shoot = parse_fusion_folder("ZFE01_1+ZF168B-3")
        assert shoot == 3

    def test_face_always_none(self):
        _, face, _, _ = parse_fusion_folder("ZFE01_1+ZF168B")
        assert face is None

    def test_different_body(self):
        _, _, body, _ = parse_fusion_folder("ZFE05_2+ZF165C")
        assert body == "ZF165C"

    def test_empty_string_returns_nones(self):
        head, face, body, shoot = parse_fusion_folder("")
        assert all(x is None for x in (head, face, body, shoot))


# ---------------------------------------------------------------------------
# parse_sle_folder  →  (head, face, body, shoot)
# ---------------------------------------------------------------------------

class TestParseSLEFolder:

    def test_standard_zxe_head(self):
        head, face, body, shoot = parse_sle_folder("ZXE200_1_ZX166K")
        assert head == "ZXE200_1"
        assert face is None
        assert body == "ZX166K"
        assert shoot is None

    def test_zx_head_variant(self):
        head, _, body, _ = parse_sle_folder("ZX201_2_ZX172E")
        assert head == "ZX201_2"
        assert body == "ZX172E"

    def test_letter_prefixed_version(self):
        head, _, body, _ = parse_sle_folder("ZXE200_W1_ZX171C")
        assert head == "ZXE200_W1"
        assert body == "ZX171C"

    def test_torso_body_short_code(self):
        _, _, body, _ = parse_sle_folder("ZXE201_1_ZX84J")
        assert body == "ZX84J"

    def test_plus_separator_with_skin_suffix(self):
        head, _, body, _ = parse_sle_folder("ZXE200_1+ZX165D-Tan-Sle3.0")
        assert head == "ZXE200_1"
        assert body == "ZX165D"

    def test_with_shoot_index(self):
        _, _, _, shoot = parse_sle_folder("ZXE200_1_ZX166K-2")
        assert shoot == 2

    def test_face_always_none(self):
        _, face, _, _ = parse_sle_folder("ZXE200_1_ZX166K")
        assert face is None

    def test_empty_string_returns_nones(self):
        head, face, body, shoot = parse_sle_folder("")
        assert all(x is None for x in (head, face, body, shoot))


# ---------------------------------------------------------------------------
# decode_body  →  (line, height, cup)
# ---------------------------------------------------------------------------

class TestDecodeBody:

    @pytest.mark.parametrize("code,line,height,cup", [
        ("ZK168B",  "ZK",  168, "B"),
        ("ZG149K",  "ZG",  149, "K"),
        ("ZGX165F", "ZGX", 165, "F"),
        ("ZF168B",  "ZF",  168, "B"),
        ("ZX160J",  "ZX",  160, "J"),
        ("ZX84J",   "ZX",   84, "J"),  # short 2-digit height
        ("ZK159D",  "ZK",  159, "D"),
    ])
    def test_valid_codes(self, code, line, height, cup):
        l, h, c = decode_body(code)
        assert l == line
        assert h == height
        assert c == cup

    def test_invalid_returns_none_triple(self):
        assert decode_body("INVALID") == (None, None, None)

    def test_empty_string_returns_none_triple(self):
        assert decode_body("") == (None, None, None)

    def test_height_is_int(self):
        _, height, _ = decode_body("ZK168B")
        assert isinstance(height, int)


# ---------------------------------------------------------------------------
# parse_head_filename  →  (head_code, face_code, tone, variant)
# ---------------------------------------------------------------------------

class TestParseHeadFilename:

    def test_full_form_with_face_and_variant(self):
        head, face, tone, variant = parse_head_filename("GE03_2 (GE70MJ)-Fair-2.png")
        assert head == "GE03_2"
        assert face == "GE70MJ"
        assert tone == "Fair"
        assert variant == 2

    def test_no_variant_defaults_to_1(self):
        _, _, _, variant = parse_head_filename("GE82_1(GE47MJ)-Fair.png")
        assert variant == 1

    def test_no_face_code(self):
        head, face, tone, variant = parse_head_filename("GE45_8-Fair.jpg")
        assert head == "GE45_8"
        assert face is None
        assert tone == "Fair"
        assert variant == 1

    def test_hyphen_variant_in_code(self):
        head, face, tone, _ = parse_head_filename("GE02-1(GE46MJ)-Tan.png")
        assert head == "GE02_1"
        assert face == "GE46MJ"
        assert tone == "Tan"

    def test_tan_skin_tone(self):
        _, _, tone, _ = parse_head_filename("GE45_8-Tan.jpg")
        assert tone == "Tan"

    def test_unrecognised_filename_returns_nones(self):
        assert parse_head_filename("random-file.txt") == (None, None, None, None)

    def test_tone_is_capitalised(self):
        _, _, tone, _ = parse_head_filename("GE45_8-fair.jpg")
        assert tone == "Fair"


# ---------------------------------------------------------------------------
# parse_body_spec  →  canonical body code (or None)
# ---------------------------------------------------------------------------

class TestParseBodySpec:

    def test_bare_code_webp(self):
        assert parse_body_spec("ZG162D.webp") == "ZG162D"

    def test_code_with_suffix(self):
        assert parse_body_spec("ZG170C-cm-pc.webp") == "ZG170C"

    def test_spec_prefix_lowercase(self):
        assert parse_body_spec("spec-zk159d.webp") == "ZK159D"

    def test_code_with_underscore_suffix(self):
        assert parse_body_spec("ZX160J_pc_3.0.webp") == "ZX160J"

    def test_unrecognised_returns_none(self):
        assert parse_body_spec("random-image.jpg") is None

    def test_zf_prefix(self):
        assert parse_body_spec("ZF168B.webp") == "ZF168B"


# ---------------------------------------------------------------------------
# parse_option  →  (key, label)
# ---------------------------------------------------------------------------

class TestParseOption:

    def test_standard_numbered_option(self):
        key, label = parse_option("1#-Hard Hand.jpg")
        assert key == "1#"
        assert label == "Hard Hand"

    def test_decimal_key(self):
        key, label = parse_option("2.0#-Soft Skin.jpg")
        assert key == "2.0#"
        assert label == "Soft Skin"

    def test_no_label(self):
        key, label = parse_option("3#-.jpg")
        assert key == "3#"
        assert label is None

    def test_fallback_to_stem_when_no_match(self):
        key, label = parse_option("some-option.jpg")
        assert key == "some-option"
        assert label is None


# ---------------------------------------------------------------------------
# seq()  →  sequence int from -NNN pattern
# ---------------------------------------------------------------------------

class TestSeq:

    def test_three_digit_sequence(self):
        assert seq("GE82_1-101.jpg") == 101

    def test_larger_sequence(self):
        assert seq("photo-205.jpg") == 205

    def test_no_pattern_returns_none(self):
        assert seq("nosequence.jpg") is None

    def test_two_digit_not_matched(self):
        # seq() requires exactly \d{3}
        assert seq("file-12.jpg") is None


# ---------------------------------------------------------------------------
# body_series()  →  series identifier string
# ---------------------------------------------------------------------------

class TestBodySeries:

    @pytest.mark.parametrize("code,expected", [
        ("ZK168B",  "K"),
        ("ZF168B",  "Fusion"),
        ("ZX160J",  "SLE"),
        ("ZG170D",  "I"),
        ("ZGX165F", "I"),   # ZGX is still I-series
    ])
    def test_all_series(self, code, expected):
        assert body_series(code) == expected


# ---------------------------------------------------------------------------
# canon_body()  →  typo-alias resolution
# ---------------------------------------------------------------------------

class TestCanonBody:

    def test_known_alias_resolved(self):
        # ZGE175E is a source-folder typo for ZG175E (from body_measurements.json)
        assert canon_body("ZGE175E") == "ZG175E"

    def test_canonical_code_unchanged(self):
        assert canon_body("ZK168B") == "ZK168B"

    def test_unknown_code_returned_as_is(self):
        assert canon_body("UNKNOWN99X") == "UNKNOWN99X"

    def test_none_input_returns_none(self):
        assert canon_body(None) is None

    def test_empty_string_returned_as_is(self):
        assert canon_body("") == ""
