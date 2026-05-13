<div align="center">
  <img src="docs/images/banner.svg" alt="pytest-beehave" width="860"/>

  <br><br>

  <p><strong>Generates test stubs from Gherkin <code>.feature</code> files, keeps them in sync, and displays BDD steps in pytest output — automatically, every time pytest runs.</strong></p>

  [![Contributors][contributors-shield]][contributors-url]
  [![Forks][forks-shield]][forks-url]
  [![Stargazers][stars-shield]][stars-url]
  [![Issues][issues-shield]][issues-url]
  [![MIT License][license-shield]][license-url]
  [![CI](https://img.shields.io/github/actions/workflow/status/nullhack/pytest-beehave/ci.yml?style=for-the-badge&label=CI)](https://github.com/nullhack/pytest-beehave/actions/workflows/ci.yml)
  [![Python](https://img.shields.io/badge/python-3.14-blue?style=for-the-badge)](https://www.python.org/downloads/)
</div>

---

## What it does

pytest-beehave is a pytest plugin powered by the [beehave](https://pypi.org/project/beehave/) library. Every time you run `pytest`, it reads your Gherkin `.feature` files and keeps your test stubs in sync:

- **New scenario?** It generates a typed, Hypothesis-compatible test stub — already marked `@pytest.mark.skip(reason="not implemented")` so it doesn't pollute your results.
- **Scenario Outline?** It generates `@example()` and `@given()` decorators with the right parameters.
- **Test drift?** `check_all()` detects orphan tests, misplaced tests, missing placeholders, and example mismatches — and reports them as real test failures.
- **Want to see your steps?** Run with `-v` and BDD steps appear under each test name. Install `pytest-html` and a "Scenario" column appears in the report.

All of this happens in `pytest_configure` — before pytest collects a single test.

---

## Why pytest-beehave?

BDD frameworks sold a compelling promise: human-readable specifications that live alongside your tests, kept honest by the test suite itself. The promise is real. The implementation is the problem. Every scenario explodes into a constellation of `@given`, `@when`, and `@then` step functions scattered across multiple files, wired together by fragile string matching. Refactor one step and you're hunting across the codebase. The ceremony grows with every feature, and the spec drifts from reality anyway.

pytest-beehave is the middle ground. Write your acceptance criteria in plain Gherkin — business-readable, version-controlled, owned by the team. The plugin generates test stubs with the right names and structure, marks unimplemented ones as skipped, and flags drift before it silently rots. You implement the test body however you like, in plain pytest, with no step files and no glue code.

---

## Installation

```bash
pip install pytest-beehave
```

No `conftest.py` changes required. The plugin registers itself via pytest's entry-point system.

Optional: install `pytest-beehave[html]` for a "Scenario" column in pytest-html reports.

```bash
pip install "pytest-beehave[html]"
```

---

## Quick start

**1. Write a feature file:**

```gherkin
# docs/features/checkout/shopping_cart.feature
Feature: Shopping cart

  Background:
    Given an empty cart

  Rule: Tax calculation

    Scenario: VAT is applied at the correct rate
      Given a cart with items totalling $100
      When the buyer is in the UK
      Then the order total is $120
```

**2. Run pytest:**

```bash
pytest --collect-only
```

**3. A test stub was created at `tests/features/shopping_cart/tax_calculation_test.py`:**

```python
import pytest

@pytest.mark.skip(reason="not implemented")
def test_VAT_is_applied_at_the_correct_rate():
    ...
```

**4. Run pytest again:**

```bash
pytest -v
```

```
tests/features/shopping_cart/tax_calculation_test.py::test_VAT_is_applied_at_the_correct_rate SKIPPED
  Given an empty cart
  Given a cart with items totalling $100
  When the buyer is in the UK
  Then the order total is $120
```

**5. Implement the test and ship.**

Remove the `@pytest.mark.skip` decorator, replace `...` with your test logic, and run `pytest` again. The steps display stays in sync with your feature file.

---

## How it works

pytest-beehave hooks into `pytest_configure`, the earliest possible entry point. Every stub exists on disk before pytest begins collection.

```
pytest invoked
  └─ pytest_configure fires
       ├─ load_config()                  → read [tool.beehave] from pyproject.toml
       ├─ parse_feature()                → parse .feature files into ScenarioInfo
       ├─ generate_stubs()               → write Hypothesis test stubs to disk
       ├─ _add_skip_markers()            → mark unimplemented stubs with @pytest.mark.skip
       ├─ check_all()                    → detect drift between features and tests
       └─ register display plugins       → StepsReporter (-v) and/or HtmlStepsPlugin
  └─ pytest_collection_modifyitems       → inject synthetic failing tests for ERROR violations
  └─ Collection begins — every stub is already present
  └─ Tests run
```

---

## File layout

```
docs/features/              ← configured via features_dir
  **/*.feature              ← any subfolder structure is supported

tests/features/             ← configured via tests_dir
  <feature_slug>/           ← one directory per feature (derived from Feature title)
    <rule_slug>_test.py     ← one file per Rule: block (or default_test.py)
```

Each test function name follows the convention `test_<scenario_title_with_underscores>`. The mapping is exact string equality — no `@id` tags, no step definitions, no glue code.

---

## Consistency checking

After stub generation, the plugin runs `check_all()` to detect drift between feature files and test code. Violations produce real test failures:

| Type | Severity | Meaning |
|------|----------|---------|
| `unmapped-scenario` | ERROR (fails run) | Scenario has no matching test function |
| `unmapped-test` | ERROR (fails run) | Test function has no matching scenario |
| `misplaced-test` | WARNING | Test is in the wrong rule file |
| `missing-placeholder` | ERROR (fails run) | Test body missing a placeholder |
| `missing-literal` | ERROR (fails run) | Test body missing a literal value |
| `example-mismatch` | ERROR (fails run) | Examples rows don't match `@example()` decorators |

```
$ pytest
[beehave] ERROR: tests/features/demo/default_test.py:5: unmapped-test: 'test_orphan' has no matching scenario
========================= 1 failed, 3 passed, 2 skipped =========================
```

Stub functions (body is `...`) are excluded from placeholder and literal checks — they are expected to be incomplete.

---

## TDD workflow

1. `pytest --collect-only` → stubs generated with `@pytest.mark.skip` → all skipped
2. Remove `@pytest.mark.skip`, write the test body → test runs and fails (red)
3. Fix the implementation → test passes (green)
4. Add new scenarios to `.feature` files → only new stubs get the skip marker

---

## Configuration

All configuration lives under `[tool.beehave]` in `pyproject.toml`:

```toml
[tool.beehave]
features_dir = "docs/features"      # default: docs/features
tests_dir = "tests/features"        # default: tests/features
default_strategy = "text"           # default: text (Hypothesis strategy for placeholders)
background_check_numeric = true     # default: true
background_check_string = true      # default: true
```

If `features_dir` does not exist, the plugin exits silently (no error, no stub generation).

---

## Requirements

| | Version |
|---|---|
| Python | >= 3.14 |
| pytest | >= 6.0 |
| beehave | >= 0.4.0 |

---

## Contributing

```bash
git clone https://github.com/nullhack/pytest-beehave
cd pytest-beehave
uv sync --all-extras
uv run task test && uv run task lint && uv run task static-check
```

Bug reports and pull requests are welcome on [GitHub](https://github.com/nullhack/pytest-beehave/issues).

---

## License

MIT — see [LICENSE](LICENSE).

**Author:** eol ([@nullhack](https://github.com/nullhack)) · [Documentation](https://nullhack.github.io/pytest-beehave)

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/nullhack/pytest-beehave.svg?style=for-the-badge
[contributors-url]: https://github.com/nullhack/pytest-beehave/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/nullhack/pytest-beehave.svg?style=for-the-badge
[forks-url]: https://github.com/nullhack/pytest-beehave/network/members
[stars-shield]: https://img.shields.io/github/stars/nullhack/pytest-beehave.svg?style=for-the-badge
[stars-url]: https://github.com/nullhack/pytest-beehave/stargazers
[issues-shield]: https://img.shields.io/github/issues/nullhack/pytest-beehave.svg?style=for-the-badge
[issues-url]: https://github.com/nullhack/pytest-beehave/issues
[license-shield]: https://img.shields.io/badge/license-MIT-green?style=for-the-badge
[license-url]: https://github.com/nullhack/pytest-beehave/blob/main/LICENSE
