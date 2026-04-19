"""Tests for configured path respect story."""

import pytest


class TestConfiguredPathRespect:
    @pytest.mark.skip(reason="not yet implemented")
    def test_example_hatch_c3d4e5f6() -> None:
        """
        Given: pyproject.toml contains [tool.beehave] with features_path set to a custom directory
        When: pytest is invoked with --beehave-hatch
        Then: the generated .feature files are written under the custom configured path and not under docs/features/
        """
        raise NotImplementedError

