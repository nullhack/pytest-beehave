"""Smoke tests verifying pytest-beehave plugin loads correctly."""

import importlib

import pytest


def test_plugin_module_imports() -> None:
    """The pytest_beehave.plugin module can be imported without errors."""
    mod = importlib.import_module("pytest_beehave.plugin")
    assert hasattr(mod, "pytest_configure")


def test_version_is_set() -> None:
    """The package __version__ is a non-empty string."""
    from pytest_beehave import __version__

    assert isinstance(__version__, str)
    assert len(__version__) > 0


@pytest.mark.parametrize(
    "module_name",
    [
        "pytest_beehave.plugin",
        "pytest_beehave.steps_display",
        "pytest_beehave.html_column",
    ],
)
def test_all_modules_import(module_name: str) -> None:
    """Every module in the package imports cleanly."""
    mod = importlib.import_module(module_name)
    assert mod is not None
