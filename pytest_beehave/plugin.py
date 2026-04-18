"""pytest plugin entry point for pytest-beehave."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from pytest_beehave.bootstrap import bootstrap_features_directory
from pytest_beehave.config import is_explicitly_configured, resolve_features_path
from pytest_beehave.id_generator import assign_ids
from pytest_beehave.reporter import (
    report_bootstrap,
    report_id_write_back,
    report_sync_actions,
)
from pytest_beehave.sync_engine import run_sync

features_path_key: pytest.StashKey[Path] = pytest.StashKey()


class _PytestTerminalWriter:
    """Adapter wrapping pytest's terminal writer to match TerminalWriterProtocol."""

    def __init__(self, config: pytest.Config) -> None:
        """Initialise the adapter.

        Args:
            config: The pytest Config object.
        """
        self._config = config

    def line(self, s: str = "") -> None:
        """Write a line to the terminal.

        Args:
            s: The line to write.
        """
        try:
            writer = self._config.get_terminal_writer()
            writer.line(s)
        except (AssertionError, AttributeError):
            sys.stdout.write(s + "\n")
            sys.stdout.flush()


def pytest_configure(config: pytest.Config) -> None:
    """Read beehave configuration, bootstrap directory, sync stubs.

    Resolves the features directory from pyproject.toml. Bootstraps the
    canonical subfolder structure. Assigns IDs to untagged Examples. Syncs
    test stubs. Exits pytest with a hard error only when features_path is
    explicitly configured AND the path does not exist.

    Args:
        config: The pytest Config object (provides rootdir and stash).
    """
    rootdir = config.rootpath
    path = resolve_features_path(rootdir)
    if not path.exists() and is_explicitly_configured(rootdir):
        msg = f"[beehave] features_path not found: {path}"
        sys.stderr.write(msg + "\n")
        sys.stderr.flush()
        pytest.exit(msg, returncode=1)
    config.stash[features_path_key] = path
    if not path.exists():
        return
    writer = _PytestTerminalWriter(config)
    bootstrap_result = bootstrap_features_directory(path)
    report_bootstrap(writer, bootstrap_result)
    errors = assign_ids(path)
    report_id_write_back(writer, errors)
    if errors:
        pytest.exit("[beehave] untagged Examples in read-only files", returncode=1)
    tests_dir = rootdir / "tests" / "features"
    actions = run_sync(path, tests_dir)
    report_sync_actions(writer, actions)
