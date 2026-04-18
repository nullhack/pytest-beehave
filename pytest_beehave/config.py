"""Configuration reader for pytest-beehave."""

import tomllib
from pathlib import Path

DEFAULT_FEATURES_PATH: str = "docs/features"


def _read_beehave_section(rootdir: Path) -> dict[str, object]:
    """Read the [tool.beehave] section from pyproject.toml.

    Args:
        rootdir: Absolute path to the project root.

    Returns:
        The [tool.beehave] dict, or empty dict if absent.
    """
    pyproject = rootdir / "pyproject.toml"
    if not pyproject.exists():
        return {}
    with pyproject.open("rb") as f:
        data = tomllib.load(f)
    return data.get("tool", {}).get("beehave", {})


def show_steps_in_terminal(rootdir: Path) -> bool:
    """Return True if show_steps_in_terminal is enabled (default: True).

    Args:
        rootdir: Absolute path to the project root.

    Returns:
        True unless explicitly set to false in [tool.beehave].
    """
    section = _read_beehave_section(rootdir)
    return bool(section.get("show_steps_in_terminal", True))


def show_steps_in_html(rootdir: Path) -> bool:
    """Return True if show_steps_in_html is enabled (default: True).

    Args:
        rootdir: Absolute path to the project root.

    Returns:
        True unless explicitly set to false in [tool.beehave].
    """
    section = _read_beehave_section(rootdir)
    return bool(section.get("show_steps_in_html", True))


def _read_configured_path(pyproject: Path) -> str | None:
    """Read features_path from [tool.beehave] in pyproject.toml.

    Args:
        pyproject: Path to the pyproject.toml file.

    Returns:
        The configured features_path string, or None if not set.
    """
    with pyproject.open("rb") as f:
        data = tomllib.load(f)
    tool_section = data.get("tool", {})
    beehave_section = tool_section.get("beehave", {})
    return beehave_section.get("features_path")


def is_explicitly_configured(rootdir: Path) -> bool:
    """Return True if features_path is explicitly set in [tool.beehave].

    Args:
        rootdir: Absolute path to the project root.

    Returns:
        True if [tool.beehave].features_path is present in pyproject.toml.
    """
    pyproject = rootdir / "pyproject.toml"
    if not pyproject.exists():
        return False
    return _read_configured_path(pyproject) is not None


def resolve_features_path(rootdir: Path) -> Path:
    """Resolve the features directory path from pyproject.toml or use the default.

    Reads [tool.beehave].features_path from pyproject.toml located at rootdir.
    Falls back to docs/features/ if pyproject.toml is absent or has no
    [tool.beehave] section. Does not validate existence.

    Args:
        rootdir: Absolute path to the project root (directory containing
            pyproject.toml).

    Returns:
        Resolved absolute Path to the features directory.
    """
    pyproject = rootdir / "pyproject.toml"
    if not pyproject.exists():
        return rootdir / DEFAULT_FEATURES_PATH
    configured = _read_configured_path(pyproject)
    if configured is None:
        return rootdir / DEFAULT_FEATURES_PATH
    return rootdir / configured
