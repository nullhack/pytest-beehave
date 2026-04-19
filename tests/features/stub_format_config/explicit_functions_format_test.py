"""Tests for explicit functions format story."""

import pytest


@pytest.mark.skip(reason="not yet implemented")
@pytest.mark.skip(reason="non-conforming: should be in /home/user/Documents/projects/pytest-beehave/tests/features/example_hatch/configured_path_respect_test.py class TestConfiguredPathRespect")
def test_stub_format_config_c3d4e5f6() -> None:
    """
    Given: a pyproject.toml with stub_format = "functions" under [tool.beehave]
    When: pytest generates a stub for a Rule-block Example
    Then: the stub is a top-level function def test_<feature_slug>_<@id> with no class wrapper
    """
    raise NotImplementedError
