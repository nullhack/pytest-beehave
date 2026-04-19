"""Tests for overwrite protection story."""

import pytest


class TestOverwriteProtection:
    @pytest.mark.skip(reason="not yet implemented")
    def test_example_hatch_5e6f7a8b() -> None:
        """
        Given: the configured features directory already contains at least one .feature file
        When: pytest is invoked with --beehave-hatch
        Then: the pytest run exits with a non-zero status code and an error naming the conflicting path
        """
        raise NotImplementedError

    @pytest.mark.skip(reason="not yet implemented")
    def test_example_hatch_6f7a8b9c() -> None:
        """
        Given: the configured features directory already contains at least one .feature file
        When: pytest is invoked with --beehave-hatch --beehave-hatch-force
        Then: the existing .feature files are replaced with the newly generated hatch content
        """
        raise NotImplementedError
