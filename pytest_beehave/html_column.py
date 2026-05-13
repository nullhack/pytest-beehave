"""HTML column — adds a Scenario column to pytest-html reports."""

from __future__ import annotations

import html

import pytest

_SCENARIO_HEADER = (
    '<th class="sortable scenario" data-column-type="scenario">Scenario</th>'
)
_SCENARIO_CELL = (
    '<td class="col-scenario" style="white-space: pre-wrap;">{content}</td>'
)


class HtmlStepsPlugin:
    """Adds a Scenario column with BDD steps to pytest-html reports."""

    def pytest_html_results_table_header(
        self,
        cells: list[object],
    ) -> None:
        """Insert the Scenario column header after Test."""
        cells.insert(2, _SCENARIO_HEADER)

    def pytest_html_results_table_row(
        self,
        report: pytest.TestReport,
        cells: list[object],
    ) -> None:
        """Insert the Scenario cell for each test row."""
        steps = getattr(report, "_beehave_steps", None)
        content = html.escape(steps) if steps else ""
        cells.insert(2, _SCENARIO_CELL.format(content=content))
