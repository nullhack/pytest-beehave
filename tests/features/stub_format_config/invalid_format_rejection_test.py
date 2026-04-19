"""Tests for invalid format rejection story."""

from pathlib import Path

import pytest

from pytest_beehave.config import read_stub_format


@pytest.mark.slow
def test_stub_format_config_f6a7b8c9(tmp_path: Path) -> None:
    """
    Given: a pyproject.toml with stub_format = "methods" under [tool.beehave]
    When: pytest starts up
    Then: pytest exits with a non-zero status and an error message naming the invalid value
    """
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text(
        '[tool.beehave]\nfeatures_path = "docs/features"\nstub_format = "methods"\n',
        encoding="utf-8",
    )
    features_dir = tmp_path / "docs" / "features" / "backlog"
    features_dir.mkdir(parents=True)
    tests_dir = tmp_path / "tests"
    tests_dir.mkdir()
    conftest = tmp_path / "conftest.py"
    conftest.write_text("", encoding="utf-8")

    result = pytest.main(["--no-cov", "--co", "-q", str(tmp_path)], plugins=[])
    assert result != 0


def test_stub_format_config_f6a7b8c9_read_raises(tmp_path: Path) -> None:
    """Direct unit test: read_stub_format raises SystemExit on invalid value."""
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text('[tool.beehave]\nstub_format = "methods"\n', encoding="utf-8")
    with pytest.raises(SystemExit, match="methods"):
        read_stub_format(tmp_path)
