"""Unit tests for id_generator module."""

from pathlib import Path

from pytest_beehave.id_generator import (
    _check_readonly_file,
    _count_preceding_id_tags,
    _id_tag_precedes,
)


def test_id_tag_precedes_returns_false_for_empty_lines() -> None:
    """_id_tag_precedes returns False when no preceding lines exist."""
    assert _id_tag_precedes([]) is False


def test_count_preceding_id_tags_skips_blank_lines() -> None:
    """_count_preceding_id_tags skips blank lines between tags and Example."""
    lines = ["  @id:aabbccdd\n", "\n", "  \n"]
    assert _count_preceding_id_tags(lines) == 1


def test_check_readonly_file_returns_error_for_duplicate_ids(
    tmp_path: Path,
) -> None:
    """_check_readonly_file returns an error when an Example has two @id tags."""
    feature_file = tmp_path / "my.feature"
    feature_file.write_text(
        "Feature: F\n"
        "  @id:aabbccdd\n"
        "  @id:11223344\n"
        "  Example: Duplicate IDs\n"
        "    Given x\n"
        "    When y\n"
        "    Then z\n"
    )
    feature_file.chmod(0o444)
    errors = _check_readonly_file(feature_file)
    assert len(errors) == 1
    assert "Duplicate IDs" in errors[0]


def test_check_readonly_file_no_errors_when_examples_already_tagged(
    tmp_path: Path,
) -> None:
    """_check_readonly_file returns no errors for an already-tagged read-only file."""
    feature_file = tmp_path / "my.feature"
    feature_file.write_text(
        "Feature: F\n"
        "  @id:aabbccdd\n"
        "  Example: Already tagged\n"
        "    Given x\n"
        "    When y\n"
        "    Then z\n"
    )
    feature_file.chmod(0o444)
    assert _check_readonly_file(feature_file) == []
