"""Terminal steps reporter for pytest-beehave."""

from __future__ import annotations

from pathlib import Path

import pytest


def is_feature_test(nodeid: str, tests_root: Path) -> bool: ...


def get_steps_docstring(item: pytest.Item) -> str: ...


class StepsReporter:
    """Prints BDD step docstrings to the terminal for tests/features/ tests."""

    def __init__(self, config: pytest.Config) -> None: ...

    def pytest_runtest_logreport(self, report: pytest.TestReport) -> None: ...
