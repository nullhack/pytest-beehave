"""Tests for features dir bootstrap migration collision handling story."""

import pytest


@pytest.mark.skip(reason="not yet implemented")
def test_features_dir_bootstrap_7f2a0d51() -> None:
    """
    Given: the features directory contains root-level feature.feature and backlog/feature.feature already exists
    When: pytest is invoked
    Then: root-level feature.feature is not moved and backlog/feature.feature is unchanged
    """
    raise NotImplementedError


@pytest.mark.skip(reason="not yet implemented")
def test_features_dir_bootstrap_8c3b1e96() -> None:
    """
    Given: the features directory contains root-level feature.feature and backlog/feature.feature already exists
    When: pytest is invoked
    Then: the terminal output contains a warning naming the conflicting file and its location
    """
    raise NotImplementedError
