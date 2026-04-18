"""HTML Acceptance Criteria column plugin for pytest-beehave."""

from __future__ import annotations

from pathlib import Path

import pytest


class HtmlStepsPlugin:
    """Adds an Acceptance Criteria column to pytest-html reports."""

    def __init__(self, tests_root: Path) -> None:
        """Initialise the plugin.

        Args:
            tests_root: Absolute path to the tests/ directory.
        """
        self._tests_root = tests_root

    def pytest_html_results_table_header(self, cells: list[object]) -> None:
        """Insert the Acceptance Criteria column header.

        Args:
            cells: The list of header cells to modify.
        """
        cells.insert(2, "<th>Acceptance Criteria</th>")

    def pytest_html_results_table_row(
        self, report: pytest.TestReport, cells: list[object]
    ) -> None:
        """Insert the Acceptance Criteria column value for each row.

        Args:
            report: The test report for this row.
            cells: The list of row cells to modify.
        """
        nodeid = report.nodeid
        features_prefix = str(self._tests_root / "features")
        if "tests/features/" in nodeid or nodeid.startswith(features_prefix):
            docstring = getattr(report, "_beehave_docstring", "") or ""
        else:
            docstring = ""
        cells.insert(2, f"<td style='white-space: pre-wrap;'>{docstring}</td>")
