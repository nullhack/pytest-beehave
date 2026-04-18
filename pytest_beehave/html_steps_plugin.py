"""HTML Acceptance Criteria column plugin for pytest-beehave."""

from __future__ import annotations

from pathlib import Path

import pytest


class HtmlStepsPlugin:
    """Adds an Acceptance Criteria column to pytest-html reports."""

    def __init__(self, tests_root: Path) -> None: ...

    def pytest_html_results_table_header(self, cells: list[object]) -> None: ...

    def pytest_html_results_table_row(
        self, report: pytest.TestReport, cells: list[object]
    ) -> None: ...
