"""Tests for default format selection story."""

from pathlib import Path

import pytest


@pytest.mark.skip(reason="not yet implemented")
def test_stub_format_config_a1b2c3d4() -> None:
    """
    Given: a pyproject.toml with no stub_format key under [tool.beehave]
    When: pytest generates a stub for a Rule-block Example
    Then: the stub is a top-level function def test_<feature_slug>_<@id> with no class wrapper
    """
    raise NotImplementedError


@pytest.mark.slow
def test_stub_format_config_b2c3d4e5(tmp_path: Path) -> None:
    """
    Given: a pyproject.toml with no stub_format key under [tool.beehave]
    When: pytest starts up
    Then: pytest starts without any stub_format-related error
    """
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        '[tool.beehave]\nfeatures_path = "docs/features"\n', encoding="utf-8"
    )
    features_dir = tmp_path / "docs" / "features" / "backlog"
    features_dir.mkdir(parents=True)
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    conftest = tmp_path / "conftest.py"
    conftest.write_text("", encoding="utf-8")

    result = pytest.main(["--no-cov", "--co", "-q", str(tmp_path)], plugins=[])
    assert result in (0, 5)  # 0=ok, 5=no tests collected — both mean no error
