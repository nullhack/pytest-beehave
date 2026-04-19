"""Tests for explicit functions format story."""

from pathlib import Path

import pytest

from pytest_beehave.sync_engine import run_sync


@pytest.mark.skip(
    reason="non-conforming: should be in /home/user/Documents/projects/pytest-beehave/tests/features/example_hatch/configured_path_respect_test.py class TestConfiguredPathRespect"
)
@pytest.mark.skip(
    reason="non-conforming: should be in /home/user/Documents/projects/pytest-beehave/tests/features/example_hatch/configured_path_respect_test.py class TestConfiguredPathRespect"
)
def test_stub_format_config_c3d4e5f6(tmp_path: Path) -> None:
    """
    Given: a pyproject.toml with stub_format = "functions" under [tool.beehave]
    When: pytest generates a stub for a Rule-block Example
    Then: the stub is a top-level function def test_<feature_slug>_<@id> with no class wrapper
    """
    features_dir = tmp_path / "features"
    tests_dir = tmp_path / "tests"
    feature_dir = features_dir / "in-progress" / "my-feature"
    feature_dir.mkdir(parents=True)
    (feature_dir / "my-feature.feature").write_text(
        "Feature: My feature\n\n"
        "  Rule: My rule\n"
        "    @id:aabbccdd\n"
        "    Example: Something\n"
        "      Given a thing\n"
        "      When it runs\n"
        "      Then it works\n",
        encoding="utf-8",
    )
    run_sync(features_dir, tests_dir, stub_format="functions")
    test_file = tests_dir / "my_feature" / "my_rule_test.py"
    content = test_file.read_text(encoding="utf-8")
    assert "def test_my_feature_aabbccdd() -> None:" in content
    assert "class " not in content
