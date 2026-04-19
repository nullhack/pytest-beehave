"""Tests for stdlib only randomisation story."""

import pytest


class TestStdlibOnlyRandomisation:
    @pytest.mark.skip(reason="not yet implemented")
    def test_example_hatch_d4e5f6a7() -> None:
        """
        Given: no features directory exists at the configured path
        When: pytest is invoked with --beehave-hatch on two separate occasions with the directory removed between runs
        Then: the Feature name in the generated .feature file differs between the two runs
        """
        raise NotImplementedError

    @pytest.mark.skip(reason="not yet implemented")
    def test_example_hatch_e5f6a7b8() -> None:
        """
        Given: a clean environment with only pytest-beehave installed and no other packages
        When: pytest is invoked with --beehave-hatch
        Then: the hatch completes successfully and no import error or missing-module error is raised
        """
        raise NotImplementedError
