"""Tests for default format selection story."""

import pytest


@pytest.mark.skip(reason="not yet implemented")
def test_stub_format_config_a1b2c3d4() -> None:
    """
    Given: a pyproject.toml with no stub_format key under [tool.beehave]
    When: pytest generates a stub for a Rule-block Example
    Then: the stub is a top-level function def test_<feature_slug>_<@id> with no class wrapper
    """
    raise NotImplementedError


@pytest.mark.skip(reason="not yet implemented")
def test_stub_format_config_b2c3d4e5() -> None:
    """
    Given: a pyproject.toml with no stub_format key under [tool.beehave]
    When: pytest starts up
    Then: pytest starts without any stub_format-related error
    """
    raise NotImplementedError
