"""Tests for features dir bootstrap — feature file migration rule."""

import pytest


class TestFeatureFileMigration:
    """Tests for the Feature file migration Rule."""

    @pytest.mark.skip(reason="not yet implemented")
    def test_features_dir_bootstrap_e8b61d04(self) -> None:
        """
        Given: the features directory contains a .feature file directly (not inside any subfolder)
        When: pytest is invoked
        Then: that .feature file exists in the backlog subfolder and no longer exists in the root features directory
        """
        raise NotImplementedError

    @pytest.mark.skip(reason="not yet implemented")
    def test_features_dir_bootstrap_f3c97a52(self) -> None:
        """
        Given: the features directory contains a non-.feature file (e.g. discovery.md) directly in the root
        When: pytest is invoked
        Then: that file remains in the root features directory and is not moved to backlog
        """
        raise NotImplementedError

    @pytest.mark.skip(reason="not yet implemented")
    def test_features_dir_bootstrap_a9d02b6e(self) -> None:
        """
        Given: the features directory contains a .feature file inside the in-progress subfolder
        When: pytest is invoked
        Then: that file remains in the in-progress subfolder and is not moved to backlog
        """
        raise NotImplementedError

    @pytest.mark.skip(reason="not yet implemented")
    def test_features_dir_bootstrap_d1e74c83(self) -> None:
        """
        Given: the features directory contains a .feature file directly in the root
        When: pytest is invoked
        Then: the terminal output names the file that was moved to backlog
        """
        raise NotImplementedError
