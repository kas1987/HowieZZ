"""Tests for merge_stories.validate_and_merge function."""
import pytest
from merge_stories import validate_and_merge, PROFILE_FIELDS


class TestValidateAndMerge:
    """Test suite for validate_and_merge function."""

    def test_happy_path_single_character(self):
        """Valid data for one character ID with all fields."""
        parts_data = [
            ("stories.json", {
                "char_001": {
                    "story": "A compelling tale.",
                    "profile": {
                        "personality": "brave",
                        "ideal_setting": "adventure",
                        "signature": "fearless",
                        "for_you_if": "likes action"
                    }
                }
            })
        ]
        valid_ids = {"char_001"}

        merged, problems = validate_and_merge(parts_data, valid_ids)

        assert len(merged) == 1
        assert merged["char_001"]["story"] == "A compelling tale."
        assert merged["char_001"]["profile"]["personality"] == "brave"
        assert len(problems) == 0

    def test_happy_path_two_characters(self):
        """Valid data for two character IDs, no problems."""
        parts_data = [
            ("stories.json", {
                "char_001": {
                    "story": "Story one.",
                    "profile": {
                        "personality": "brave",
                        "ideal_setting": "adventure",
                        "signature": "fearless",
                        "for_you_if": "likes action"
                    }
                },
                "char_002": {
                    "story": "Story two.",
                    "profile": {
                        "personality": "kind",
                        "ideal_setting": "home",
                        "signature": "caring",
                        "for_you_if": "loves family"
                    }
                }
            })
        ]
        valid_ids = {"char_001", "char_002"}

        merged, problems = validate_and_merge(parts_data, valid_ids)

        assert len(merged) == 2
        assert "char_001" in merged
        assert "char_002" in merged
        assert len(problems) == 0

    def test_missing_file(self):
        """Missing file (None data) is handled gracefully."""
        parts_data = [
            ("missing.json", None)
        ]
        valid_ids = {"char_001"}

        merged, problems = validate_and_merge(parts_data, valid_ids)

        assert len(merged) == 0
        assert len(problems) == 1
        assert "MISSING OR INVALID FILE missing.json" in problems[0]

    def test_unknown_character_id(self):
        """Unknown character_id is recorded as problem, not merged."""
        parts_data = [
            ("stories.json", {
                "unknown_id": {
                    "story": "A story.",
                    "profile": {
                        "personality": "brave",
                        "ideal_setting": "adventure",
                        "signature": "fearless",
                        "for_you_if": "likes action"
                    }
                }
            })
        ]
        valid_ids = {"char_001"}

        merged, problems = validate_and_merge(parts_data, valid_ids)

        assert len(merged) == 0
        assert len(problems) == 1
        assert "unknown character_id unknown_id" in problems[0]

    def test_missing_story_field(self):
        """Missing or falsy story field is recorded as problem."""
        parts_data = [
            ("stories.json", {
                "char_001": {
                    "profile": {
                        "personality": "brave",
                        "ideal_setting": "adventure",
                        "signature": "fearless",
                        "for_you_if": "likes action"
                    }
                }
            })
        ]
        valid_ids = {"char_001"}

        merged, problems = validate_and_merge(parts_data, valid_ids)

        assert "char_001" in merged
        assert merged["char_001"]["story"] is None
        assert any("char_001: missing story" in p for p in problems)

    def test_empty_story_string(self):
        """Empty string story is treated as falsy."""
        parts_data = [
            ("stories.json", {
                "char_001": {
                    "story": "",
                    "profile": {
                        "personality": "brave",
                        "ideal_setting": "adventure",
                        "signature": "fearless",
                        "for_you_if": "likes action"
                    }
                }
            })
        ]
        valid_ids = {"char_001"}

        merged, problems = validate_and_merge(parts_data, valid_ids)

        assert "char_001: missing story" in problems

    def test_missing_profile_personality(self):
        """Missing personality field in profile."""
        parts_data = [
            ("stories.json", {
                "char_001": {
                    "story": "A story.",
                    "profile": {
                        "ideal_setting": "adventure",
                        "signature": "fearless",
                        "for_you_if": "likes action"
                    }
                }
            })
        ]
        valid_ids = {"char_001"}

        merged, problems = validate_and_merge(parts_data, valid_ids)

        assert "char_001: profile.personality missing" in problems

    def test_missing_profile_ideal_setting(self):
        """Missing ideal_setting field in profile."""
        parts_data = [
            ("stories.json", {
                "char_001": {
                    "story": "A story.",
                    "profile": {
                        "personality": "brave",
                        "signature": "fearless",
                        "for_you_if": "likes action"
                    }
                }
            })
        ]
        valid_ids = {"char_001"}

        merged, problems = validate_and_merge(parts_data, valid_ids)

        assert "char_001: profile.ideal_setting missing" in problems

    def test_missing_profile_signature(self):
        """Missing signature field in profile."""
        parts_data = [
            ("stories.json", {
                "char_001": {
                    "story": "A story.",
                    "profile": {
                        "personality": "brave",
                        "ideal_setting": "adventure",
                        "for_you_if": "likes action"
                    }
                }
            })
        ]
        valid_ids = {"char_001"}

        merged, problems = validate_and_merge(parts_data, valid_ids)

        assert "char_001: profile.signature missing" in problems

    def test_missing_profile_for_you_if(self):
        """Missing for_you_if field in profile."""
        parts_data = [
            ("stories.json", {
                "char_001": {
                    "story": "A story.",
                    "profile": {
                        "personality": "brave",
                        "ideal_setting": "adventure",
                        "signature": "fearless"
                    }
                }
            })
        ]
        valid_ids = {"char_001"}

        merged, problems = validate_and_merge(parts_data, valid_ids)

        assert "char_001: profile.for_you_if missing" in problems

    def test_all_profile_fields_present(self):
        """All 4 profile fields present means no profile-field problems."""
        parts_data = [
            ("stories.json", {
                "char_001": {
                    "story": "A story.",
                    "profile": {
                        "personality": "brave",
                        "ideal_setting": "adventure",
                        "signature": "fearless",
                        "for_you_if": "likes action"
                    }
                }
            })
        ]
        valid_ids = {"char_001"}

        merged, problems = validate_and_merge(parts_data, valid_ids)

        # Only check that no profile-field problems exist
        profile_problems = [p for p in problems if "profile." in p]
        assert len(profile_problems) == 0

    def test_profile_is_none(self):
        """profile: None is treated as empty dict, all 4 fields flagged."""
        parts_data = [
            ("stories.json", {
                "char_001": {
                    "story": "A story.",
                    "profile": None
                }
            })
        ]
        valid_ids = {"char_001"}

        merged, problems = validate_and_merge(parts_data, valid_ids)

        assert "char_001: profile.personality missing" in problems
        assert "char_001: profile.ideal_setting missing" in problems
        assert "char_001: profile.signature missing" in problems
        assert "char_001: profile.for_you_if missing" in problems

    def test_profile_absent(self):
        """profile key absent is treated as empty dict, all 4 fields flagged."""
        parts_data = [
            ("stories.json", {
                "char_001": {
                    "story": "A story."
                }
            })
        ]
        valid_ids = {"char_001"}

        merged, problems = validate_and_merge(parts_data, valid_ids)

        assert "char_001: profile.personality missing" in problems
        assert "char_001: profile.ideal_setting missing" in problems
        assert "char_001: profile.signature missing" in problems
        assert "char_001: profile.for_you_if missing" in problems

    def test_empty_parts_data(self):
        """Empty parts_data list returns empty merged and problems."""
        parts_data = []
        valid_ids = {"char_001"}

        merged, problems = validate_and_merge(parts_data, valid_ids)

        assert len(merged) == 0
        assert len(problems) == 0

    def test_empty_valid_ids(self):
        """Every character_id is unknown if valid_ids is empty."""
        parts_data = [
            ("stories.json", {
                "char_001": {
                    "story": "A story.",
                    "profile": {
                        "personality": "brave",
                        "ideal_setting": "adventure",
                        "signature": "fearless",
                        "for_you_if": "likes action"
                    }
                }
            })
        ]
        valid_ids = set()

        merged, problems = validate_and_merge(parts_data, valid_ids)

        assert len(merged) == 0
        assert "unknown character_id char_001" in problems[0]

    def test_multiple_files_merged(self):
        """Characters from two files are merged together."""
        parts_data = [
            ("stories1.json", {
                "char_001": {
                    "story": "Story one.",
                    "profile": {
                        "personality": "brave",
                        "ideal_setting": "adventure",
                        "signature": "fearless",
                        "for_you_if": "likes action"
                    }
                }
            }),
            ("stories2.json", {
                "char_002": {
                    "story": "Story two.",
                    "profile": {
                        "personality": "kind",
                        "ideal_setting": "home",
                        "signature": "caring",
                        "for_you_if": "loves family"
                    }
                }
            })
        ]
        valid_ids = {"char_001", "char_002"}

        merged, problems = validate_and_merge(parts_data, valid_ids)

        assert len(merged) == 2
        assert "char_001" in merged
        assert "char_002" in merged
        assert len(problems) == 0

    def test_duplicate_cid_across_files_last_wins(self):
        """Duplicate character_id across files: last write overwrites first."""
        parts_data = [
            ("stories1.json", {
                "char_001": {
                    "story": "First story.",
                    "profile": {
                        "personality": "brave",
                        "ideal_setting": "adventure",
                        "signature": "fearless",
                        "for_you_if": "likes action"
                    }
                }
            }),
            ("stories2.json", {
                "char_001": {
                    "story": "Second story.",
                    "profile": {
                        "personality": "kind",
                        "ideal_setting": "home",
                        "signature": "caring",
                        "for_you_if": "loves family"
                    }
                }
            })
        ]
        valid_ids = {"char_001"}

        merged, problems = validate_and_merge(parts_data, valid_ids)

        assert len(merged) == 1
        assert merged["char_001"]["story"] == "Second story."
        assert merged["char_001"]["profile"]["personality"] == "kind"

    def test_return_types(self):
        """Return types are dict for merged, list for problems."""
        parts_data = []
        valid_ids = set()

        merged, problems = validate_and_merge(parts_data, valid_ids)

        assert isinstance(merged, dict)
        assert isinstance(problems, list)

    def test_merged_value_shape(self):
        """Each merged value has 'story' and 'profile' keys."""
        parts_data = [
            ("stories.json", {
                "char_001": {
                    "story": "A story.",
                    "profile": {
                        "personality": "brave",
                        "ideal_setting": "adventure",
                        "signature": "fearless",
                        "for_you_if": "likes action"
                    }
                }
            })
        ]
        valid_ids = {"char_001"}

        merged, problems = validate_and_merge(parts_data, valid_ids)

        for cid, entry in merged.items():
            assert "story" in entry
            assert "profile" in entry
            assert isinstance(entry["profile"], dict)

    def test_multiple_problems_per_character(self):
        """A single character can have multiple problems recorded."""
        parts_data = [
            ("stories.json", {
                "char_001": {
                    "story": "",
                    "profile": {
                        "ideal_setting": "adventure"
                    }
                }
            })
        ]
        valid_ids = {"char_001"}

        merged, problems = validate_and_merge(parts_data, valid_ids)

        # Should have problems for: missing story, missing personality,
        # missing signature, missing for_you_if
        problems_for_char = [p for p in problems if "char_001" in p]
        assert len(problems_for_char) >= 4

    def test_story_with_value_is_preserved(self):
        """A non-empty story value is preserved exactly."""
        story_text = "This is a long and detailed story with many words."
        parts_data = [
            ("stories.json", {
                "char_001": {
                    "story": story_text,
                    "profile": {
                        "personality": "brave",
                        "ideal_setting": "adventure",
                        "signature": "fearless",
                        "for_you_if": "likes action"
                    }
                }
            })
        ]
        valid_ids = {"char_001"}

        merged, problems = validate_and_merge(parts_data, valid_ids)

        assert merged["char_001"]["story"] == story_text
