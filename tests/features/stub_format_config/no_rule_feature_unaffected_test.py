"""Tests for no-rule feature unaffected story."""

import pytest


@pytest.mark.skip(reason="not yet implemented")
def test_stub_format_config_a7b8c9d0() -> None:
    """
    Given: a pyproject.toml with stub_format = "classes" under [tool.beehave]
    And: a feature file with no Rule blocks
    When: pytest generates stubs for that feature
    Then: the stubs are module-level functions in examples_test.py with no class wrapper
    """
    raise NotImplementedError
