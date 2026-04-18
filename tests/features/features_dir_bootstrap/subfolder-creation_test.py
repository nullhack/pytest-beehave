"""Tests for features dir bootstrap — subfolder creation rule."""

import pytest


class TestSubfolderCreation:
    """Tests for the Subfolder creation Rule."""

    @pytest.mark.skip(reason="not yet implemented")
    def test_features_dir_bootstrap_3a1f8c2e(self) -> None:
        """
        Given: the features directory exists with no backlog, in-progress, or completed subfolders
        When: pytest is invoked
        Then: the backlog, in-progress, and completed subfolders all exist inside the features directory
        """
        raise NotImplementedError

    @pytest.mark.skip(reason="not yet implemented")
    def test_features_dir_bootstrap_b7d4e091(self) -> None:
        """
        Given: the features directory exists with a backlog subfolder but no in-progress or completed subfolders
        When: pytest is invoked
        Then: the in-progress and completed subfolders are created and the backlog subfolder is unchanged
        """
        raise NotImplementedError

    @pytest.mark.skip(reason="not yet implemented")
    def test_features_dir_bootstrap_c2a53f7d(self) -> None:
        """
        Given: the features directory exists with no backlog, in-progress, or completed subfolders
        When: pytest is invoked
        Then: the terminal output names each subfolder that was created
        """
        raise NotImplementedError
