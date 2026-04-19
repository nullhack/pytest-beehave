"""Tests for overwrite protection story."""

from pathlib import Path

import pytest

from pytest_beehave.hatch import run_hatch


def test_example_hatch_5e6f7a8b(tmp_path: Path) -> None:
    """
    Given: the configured features directory already contains at least one .feature file
    When: pytest is invoked with --beehave-hatch
    Then: the pytest run exits with a non-zero status code and an error naming the conflicting path
    """
    features_root = tmp_path / "features"
    existing = features_root / "backlog" / "existing.feature"
    existing.parent.mkdir(parents=True)
    existing.write_text("Feature: existing\n", encoding="utf-8")

    with pytest.raises(SystemExit) as exc_info:
        run_hatch(features_root, force=False)

    assert str(existing) in str(exc_info.value)


def test_example_hatch_6f7a8b9c(tmp_path: Path) -> None:
    """
    Given: the configured features directory already contains at least one .feature file
    When: pytest is invoked with --beehave-hatch --beehave-hatch-force
    Then: the existing .feature files are replaced with the newly generated hatch content
    """
    features_root = tmp_path / "features"
    existing = features_root / "backlog" / "existing.feature"
    existing.parent.mkdir(parents=True)
    existing.write_text("Feature: existing\n", encoding="utf-8")

    run_hatch(features_root, force=True)

    assert not existing.exists()
    assert list(features_root.rglob("*.feature"))
