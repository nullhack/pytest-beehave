"""Tests for orphan marking story."""

from __future__ import annotations

from pathlib import Path
from typing import Callable

import pytest

from pytest_beehave.sync_engine import run_sync as sync_stubs


@pytest.mark.skip(reason="not yet implemented")
def test_stub_sync_4a7c2e81(tmp_path: Path) -> None:
    """
    Given: a test function whose @id matches a current Example but is in the wrong file or class
    When: pytest is invoked
    Then: stub-sync creates a conforming stub in the correct location and marks the original with @pytest.mark.skip(reason="non-conforming: moved to <file>::<Class>")
    """
    raise NotImplementedError


@pytest.mark.skip(reason="not yet implemented")
def test_stub_sync_3f9d1b56(tmp_path: Path) -> None:
    """
    Given: a non-conforming test already marked and a conforming stub already present in the correct location
    When: pytest is invoked
    Then: the non-conforming marker remains on the original test and the conforming stub is unchanged
    """
    raise NotImplementedError


@pytest.mark.skip(reason="not yet implemented")
def test_stub_sync_8b2e4f17(tmp_path: Path) -> None:
    """
    Given: a completed feature test file containing a test function whose @id no longer exists in the feature file
    When: pytest is invoked
    Then: that test function receives @pytest.mark.skip(reason="orphan: no matching @id in .feature files")
    """
    raise NotImplementedError


@pytest.mark.skip(reason="not yet implemented")
def test_stub_sync_c9a30d52(tmp_path: Path) -> None:
    """
    Given: a test function with @pytest.mark.slow already applied by the software-engineer
    When: pytest is invoked and stub-sync processes the feature
    Then: @pytest.mark.slow is unchanged and no other software-engineer marker is added or removed
    """
    raise NotImplementedError


@pytest.mark.unit
def test_stub_sync_9d7a0b34(
    tmp_path: Path,
    make_feature: Callable[..., None],
    make_test_file: Callable[..., Path],
) -> None:
    """
    Given: a test file containing a test function whose @id hex does not match any Example in any .feature file
    When: pytest is invoked
    Then: that test function has @pytest.mark.skip(reason="orphan: no matching @id in .feature files") applied
    """
    # Given
    features_dir = tmp_path / "features"
    tests_dir = tmp_path / "tests"
    # A feature file with a known ID (not the orphan's ID)
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
    # A test file with a function whose ID (deadbeef) is NOT in any .feature file
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
    # When
    sync_stubs(features_dir, tests_dir)
    # Then
    test_file = tests_dir / "my_feature" / "my_story_test.py"
    content = test_file.read_text(encoding="utf-8")
    assert (
        '@pytest.mark.skip(reason="orphan: no matching @id in .feature files")'
        in content
    )
    # The skip marker must appear before the def line
    skip_idx = content.index(
        '@pytest.mark.skip(reason="orphan: no matching @id in .feature files")'
    )
    def_idx = content.index("def test_my_feature_deadbeef")
    assert skip_idx < def_idx


@pytest.mark.unit
def test_stub_sync_67192894(
    tmp_path: Path,
    make_feature: Callable[..., None],
    make_test_file: Callable[..., Path],
) -> None:
    """
    Given: a test function marked as orphan and a .feature file that now contains a matching @id Example
    When: pytest is invoked
    Then: the orphan skip marker is removed from that test function
    """
    # Given
    features_dir = tmp_path / "features"
    tests_dir = tmp_path / "tests"
    # Feature file now contains the ID that was previously orphaned
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
    # Test file has the function already marked as orphan
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
    # When
    sync_stubs(features_dir, tests_dir)
    # Then
    test_file = tests_dir / "my_feature" / "my_story_test.py"
    content = test_file.read_text(encoding="utf-8")
    assert (
        '@pytest.mark.skip(reason="orphan: no matching @id in .feature files")'
        not in content
    )
    assert "def test_my_feature_deadbeef() -> None:" in content
