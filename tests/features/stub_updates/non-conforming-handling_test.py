"""Tests for stub updates — non-conforming handling rule."""

from __future__ import annotations

from pathlib import Path

import pytest


class TestNonConformingHandling:
    """Tests for the Non-conforming handling Rule."""

    @pytest.mark.skip(reason="not yet implemented")
    def test_stub_updates_4a7c2e81(self, tmp_path: Path) -> None:
        """
        Given: a test function whose @id matches a current Example but is in the wrong file or class
        When: pytest is invoked
        Then: stub-sync creates a conforming stub in the correct location and marks the original with @pytest.mark.skip(reason="non-conforming: moved to <file>::<Class>")
        """
        raise NotImplementedError

    @pytest.mark.skip(reason="not yet implemented")
    def test_stub_updates_3f9d1b56(self, tmp_path: Path) -> None:
        """
        Given: a non-conforming test already marked and a conforming stub already present in the correct location
        When: pytest is invoked
        Then: the non-conforming marker remains on the original test and the conforming stub is unchanged
        """
        raise NotImplementedError
