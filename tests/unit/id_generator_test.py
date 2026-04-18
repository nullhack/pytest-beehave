"""Unit tests for id_generator module."""

from pytest_beehave.id_generator import _id_tag_precedes


def test_id_tag_precedes_returns_false_for_empty_lines() -> None:
    """_id_tag_precedes returns False when no preceding lines exist."""
    assert _id_tag_precedes([]) is False
