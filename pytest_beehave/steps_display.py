"""Terminal steps display — prints BDD steps under each test name."""

from __future__ import annotations

import pytest


class StepsReporter:
    """Prints BDD steps to the terminal when --beehave-verbose is active."""

    def __init__(self, config: pytest.Config) -> None:
        """Store pytest config for terminal writer access."""
        self._config = config

    def pytest_runtest_logreport(
        self,
        report: pytest.TestReport,
    ) -> None:
        """Print steps after each test call phase report."""
        if report.when != "call" and not (report.when == "setup" and report.skipped):
            return
        steps = getattr(report, "_beehave_steps", None)
        if not steps:
            return
        writer = self._config.get_terminal_writer()
        indented = "\n".join(f"  {line}" for line in steps.splitlines())
        writer.write(f"\n{indented}\n")
