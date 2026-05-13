"""pytest plugin entry point — orchestrates beehave during the pytest lifecycle."""

from __future__ import annotations

import importlib.util
import sys
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytest
from beehave.check import check_all
from beehave.config import Config, load_config
from beehave.generate import generate_stubs
from beehave.gherkin import parse_feature
from beehave.models import ScenarioInfo, Violation

_beehave_config_key: pytest.StashKey[Config] = pytest.StashKey()
_scenarios_key: pytest.StashKey[dict[str, ScenarioInfo]] = pytest.StashKey()
_error_violations_key: pytest.StashKey[list[Violation]] = pytest.StashKey()


class BeehaveViolationItem(pytest.Item):
    """Synthetic test item that fails, representing a beehave ERROR."""

    def __init__(  # noqa: D107
        self,
        *,
        violation: Violation,
        **kwargs: Any,  # noqa: ANN401
    ) -> None:
        safe_name = violation.error_type.replace("-", "_")
        super().__init__(name=f"beehave_{safe_name}", **kwargs)
        self.violation = violation

    def runtest(self) -> None:
        """Execute the test — always raises AssertionError."""
        raise AssertionError(f"[beehave] {self.violation}")

    def repr_failure(
        self,
        excinfo: pytest.ExceptionInfo[BaseException],
        style: str | None = None,
    ) -> str:
        """Return a string representation of the failure."""
        return str(excinfo.value)

    def reportinfo(self) -> tuple[str, int, str]:
        """Return location info for the test report."""
        return (
            str(self.violation.path),
            self.violation.line,
            f"[beehave] {self.violation.error_type}: {self.violation.message}",
        )


def _html_available() -> bool:
    return importlib.util.find_spec("pytest_html") is not None


def _format_scenario_steps(scenario: ScenarioInfo) -> str:
    lines = [f"{step.keyword} {step.text}" for step in scenario.steps]
    return "\n".join(lines)


def _write_line(config: pytest.Config, text: str) -> None:
    try:
        config.get_terminal_writer().line(text)
    except AssertionError, AttributeError:
        sys.stderr.write(text + "\n")
        sys.stderr.flush()


def _report_violation(config: pytest.Config, v: Violation) -> None:
    level = "WARNING" if v.is_warning else "ERROR"
    _write_line(config, f"[beehave] {level}: {v}")


_SKIP_MARKER = '@pytest.mark.skip(reason="not implemented")'


def _add_skip_markers(tests_dir: Path) -> None:
    """Add @pytest.mark.skip(reason='not implemented') to stub functions."""
    for test_file in tests_dir.rglob("*.py"):
        source = test_file.read_text(encoding="utf-8")
        if "..." not in source:
            continue

        lines = source.split("\n")
        changed = False
        new_lines: list[str] = []

        i = 0
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()

            if stripped == "..." and new_lines:
                prev = new_lines[-1]
                if prev.lstrip().startswith("def "):
                    def_indent = prev[: len(prev) - len(prev.lstrip())]
                    insert_idx = len(new_lines) - 1
                    while insert_idx > 0 and (
                        new_lines[insert_idx - 1].lstrip().startswith("@")
                    ):
                        insert_idx -= 1
                    already_marked = (
                        insert_idx < len(new_lines)
                        and "@pytest.mark.skip" in new_lines[insert_idx]
                    )
                    if not already_marked:
                        new_lines.insert(insert_idx, f"{def_indent}{_SKIP_MARKER}")
                        changed = True

            new_lines.append(line)
            i += 1

        if not changed:
            continue

        source = "\n".join(new_lines)
        if "import pytest" not in source:
            source = "import pytest\n\n" + source

        test_file.write_text(source, encoding="utf-8")


def _collect_scenarios_and_generate(
    features_dir: Path,
    config: Config,
    pytest_config: pytest.Config,
) -> dict[str, ScenarioInfo]:
    scenarios: dict[str, ScenarioInfo] = {}
    seen_names: dict[str, str] = {}

    for feature_file in sorted(features_dir.rglob("*.feature")):
        try:
            parsed = parse_feature(feature_file, config, seen_names)
        except Exception as exc:
            msg = f"[beehave] PARSE ERROR: {feature_file}: {exc}"
            _write_line(pytest_config, msg)
            continue
        scenarios.update(parsed)

        rel = feature_file.relative_to(features_dir)
        feature_path_str = str(rel.with_suffix(""))
        try:
            generate_stubs(feature_path_str, config)
        except Exception as exc:
            msg = f"[beehave] GENERATE ERROR: {feature_file}: {exc}"
            _write_line(pytest_config, msg)

    return scenarios


def pytest_configure(config: pytest.Config) -> None:
    """Parse features, generate stubs, check violations, register reporters."""
    rootdir = config.rootpath
    beehave_config = load_config(rootdir)
    config.stash[_beehave_config_key] = beehave_config

    features_dir = rootdir / beehave_config.features_dir
    if not features_dir.exists():
        return

    scenarios = _collect_scenarios_and_generate(
        features_dir,
        beehave_config,
        config,
    )
    config.stash[_scenarios_key] = scenarios

    _add_skip_markers(rootdir / beehave_config.tests_dir)

    violations = check_all(beehave_config)
    error_violations: list[Violation] = []
    for v in violations:
        _report_violation(config, v)
        if not v.is_warning:
            error_violations.append(v)
    config.stash[_error_violations_key] = error_violations

    if (config.getoption("verbose", default=0) or 0) >= 1:
        from pytest_beehave.steps_display import StepsReporter

        config.pluginmanager.register(
            StepsReporter(config),
            "beehave-steps-reporter",
        )

    if _html_available():
        from pytest_beehave.html_column import HtmlStepsPlugin

        config.pluginmanager.register(
            HtmlStepsPlugin(),
            "beehave-html-steps",
        )


def pytest_collection_modifyitems(
    session: pytest.Session,
    items: list[pytest.Item],
) -> None:
    """Inject synthetic failing tests for each ERROR violation."""
    error_violations = session.config.stash.get(_error_violations_key, [])
    for v in error_violations:
        item = BeehaveViolationItem.from_parent(
            parent=session,
            violation=v,
        )
        items.append(item)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(
    item: pytest.Item,
    call: pytest.CallInfo[None],
) -> Generator[None, None, None]:
    """Attach BDD steps to the test report for display plugins."""
    outcome: pytest.TestReport = yield  # type: ignore[assignment]
    report = outcome.get_result()
    stash = item.config.stash
    scenarios: dict[str, ScenarioInfo] | None = stash.get(
        _scenarios_key,
        None,
    )
    if scenarios is None:
        return
    func_name = getattr(item, "originalname", item.name)
    scenario = scenarios.get(func_name)
    if scenario is not None:
        report._beehave_steps = _format_scenario_steps(scenario)
