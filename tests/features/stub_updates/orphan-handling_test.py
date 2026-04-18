"""Tests for stub updates — orphan handling rule."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

import pytest

from pytest_beehave.sync_engine import run_sync as sync_stubs


class TestOrphanHandling:
    """Tests for the Orphan handling Rule."""

    @pytest.mark.unit
    def test_stub_updates_9d7a0b34(
        self,
        tmp_path: Path,
        make_feature: Callable[..., None],
        make_test_file: Callable[..., Path],
    ) -> None:
        """
        Given: a test file containing a test function whose @id hex does not match any Example in any .feature file
        When: pytest is invoked
        Then: that test function has @pytest.mark.skip(reason="orphan: no matching @id in .feature files") applied
        """
        features_dir = tmp_path / "features"
        tests_dir = tmp_path / "tests"
        make_feature(
            features_dir,
            "in-progress",
            "my-feature",
            "my-story.feature",
            """\
Feature: My feature
  @id:11111111
  Example: Known example
    Given something
    When it runs
    Then it works
""",
        )
        make_test_file(
            tests_dir,
            "my_feature",
            "my_story",
            '''\
"""Tests for my story."""

import pytest


def test_my_feature_deadbeef() -> None:
    """
    Given: something stale
    When: it ran
    Then: it worked
    """
    raise NotImplementedError
''',
        )
        sync_stubs(features_dir, tests_dir)
        test_file = tests_dir / "my_feature" / "my_story_test.py"
        content = test_file.read_text(encoding="utf-8")
        assert (
            '@pytest.mark.skip(reason="orphan: no matching @id in .feature files")'
            in content
        )
        skip_idx = content.index(
            '@pytest.mark.skip(reason="orphan: no matching @id in .feature files")'
        )
        def_idx = content.index("def test_my_feature_deadbeef")
        assert skip_idx < def_idx

    @pytest.mark.unit
    def test_stub_updates_67192894(
        self,
        tmp_path: Path,
        make_feature: Callable[..., None],
        make_test_file: Callable[..., Path],
    ) -> None:
        """
        Given: a test function marked as orphan and a .feature file that now contains a matching @id Example
        When: pytest is invoked
        Then: the orphan skip marker is removed from that test function
        """
        features_dir = tmp_path / "features"
        tests_dir = tmp_path / "tests"
        make_feature(
            features_dir,
            "in-progress",
            "my-feature",
            "my-story.feature",
            """\
Feature: My feature
  @id:deadbeef
  Example: Now a real example
    Given something real
    When it runs
    Then it works
""",
        )
        make_test_file(
            tests_dir,
            "my_feature",
            "my_story",
            '''\
"""Tests for my story."""

import pytest


@pytest.mark.skip(reason="orphan: no matching @id in .feature files")
def test_my_feature_deadbeef() -> None:
    """
    Given: something real
    When: it runs
    Then: it works
    """
    raise NotImplementedError
''',
        )
        sync_stubs(features_dir, tests_dir)
        test_file = tests_dir / "my_feature" / "my_story_test.py"
        content = test_file.read_text(encoding="utf-8")
        assert (
            '@pytest.mark.skip(reason="orphan: no matching @id in .feature files")'
            not in content
        )
        assert "def test_my_feature_deadbeef() -> None:" in content

    @pytest.mark.skip(reason="not yet implemented")
    def test_stub_updates_8b2e4f17(self, tmp_path: Path) -> None:
        """
        Given: a completed feature test file containing a test function whose @id no longer exists in the feature file
        When: pytest is invoked
        Then: that test function receives @pytest.mark.skip(reason="orphan: no matching @id in .feature files")
        """
        raise NotImplementedError

    @pytest.mark.skip(reason="not yet implemented")
    def test_stub_updates_c9a30d52(self, tmp_path: Path) -> None:
        """
        Given: a test function with @pytest.mark.slow already applied by the software-engineer
        When: pytest is invoked and stub-sync processes the feature
        Then: @pytest.mark.slow is unchanged and no other software-engineer marker is added or removed
        """
        raise NotImplementedError
