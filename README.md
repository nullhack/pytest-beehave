<div align="center">

<img src="docs/assets/banner.svg" alt="pytest-beehave" width="100%"/>

[![Python](https://img.shields.io/badge/python-%E2%89%A53.14-blue?style=for-the-badge)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/pytest-beehave?style=for-the-badge)](https://pypi.org/project/pytest-beehave/)
[![CI](https://img.shields.io/github/actions/workflow/status/nullhack/pytest-beehave/ci.yml?style=for-the-badge&label=CI)](https://github.com/nullhack/pytest-beehave/actions/workflows/ci.yml)

**Generates pytest test stubs from Gherkin `.feature` files, checks consistency, and displays BDD steps — automatically, every time pytest runs.**

</div>

---

**pytest-beehave** is a pytest plugin powered by [beehave](https://pypi.org/project/beehave/). It reads your Gherkin `.feature` files and generates [Hypothesis](https://hypothesis.readthedocs.io/)-compatible test stubs with the right names, decorators, and parameters — then verifies that your test code stays consistent with your spec. New scenarios get `@pytest.mark.skip`; drift becomes a real test failure.

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

### 1. Write a feature file

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

### 2. Run pytest

```bash
pytest --collect-only
```

### 3. A test stub is created

```
tests/features/shopping_cart/
├── tax_calculation_test.py
```

```python
# tests/features/shopping_cart/tax_calculation_test.py
import pytest

@pytest.mark.skip(reason="not implemented")
def test_VAT_is_applied_at_the_correct_rate():
    ...
```

### 4. See BDD steps

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

### 5. Implement and ship

Remove `@pytest.mark.skip`, write the test body, run `pytest` again. The steps display stays in sync with your feature file.

---

## How it works

The plugin hooks into `pytest_configure` — every stub exists on disk before collection begins.

```
pytest invoked
  └─ pytest_configure fires
       ├─ load_config()                  → read [tool.beehave] from pyproject.toml
       ├─ parse_feature()                → parse .feature files into ScenarioInfo
       ├─ generate_stubs()               → write Hypothesis test stubs to disk
       ├─ _add_skip_markers()            → mark unimplemented stubs with @pytest.mark.skip
       ├─ check_all()                    → detect drift between features and tests
       └─ register display plugins       → StepsReporter (-v) and/or HtmlStepsPlugin
  └─ pytest_collection_modifyitems       → inject failing tests for ERROR violations
  └─ Collection begins — every stub is already present
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

Each test function name follows `test_<scenario_title_with_underscores>`. The mapping is exact string equality — no `@id` tags, no step definitions, no glue code.

---

## What `check_all` enforces

After stub generation, the plugin runs `check_all()` to detect drift between feature files and test code. ERROR violations produce real test failures via synthetic test items:

| Type | Severity | What it catches |
|------|----------|-----------------|
| `unmapped-scenario` | ERROR | Scenario has no matching test function |
| `unmapped-test` | ERROR | Test function has no matching scenario |
| `misplaced-test` | WARNING | Function is in the wrong rule file |
| `missing-placeholder` | ERROR | Test body missing a `<placeholder>` |
| `missing-literal` | ERROR | Test body missing a `"string"` or numeric literal |
| `example-mismatch` | ERROR | Examples rows don't match `@example()` decorators |

```
$ pytest
[beehave] ERROR: tests/features/demo/default_test.py:5: unmapped-test: 'test_orphan' has no matching scenario
========================= 1 failed, 3 passed, 2 skipped =========================
```

Stub functions (body is `...`) are excluded from placeholder and literal checks.

---

## How it maps

- **Scenario title → function name:** `VAT Is Applied At The Correct Rate` → `test_VAT_is_applied_at_the_correct_rate`. Lowercased. Globally unique.
- **Rule → test file:** Top-level scenarios go to `default_test.py`. Scenarios inside a Rule go to `<rule>_test.py`.
- **Feature title → directory:** `Shopping Cart` → `tests/features/shopping_cart/`.
- **Scenario Outline → decorators:** `<placeholder>` columns become `@given()` parameters with inferred Hypothesis strategies. Example rows become `@example()` decorators.

---

## TDD workflow

1. `pytest --collect-only` → stubs generated with `@pytest.mark.skip`
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

If `features_dir` does not exist, the plugin exits silently.

---

## Requirements

| | Version |
|---|---|
| Python | >= 3.14 |
| pytest | >= 6.0 |
| beehave | >= 1.0.0 |

---

## Contributing

```bash
git clone https://github.com/nullhack/pytest-beehave
cd pytest-beehave
uv sync --all-extras
uv run task test && uv run task lint && uv run task static-check
```

Bug reports and pull requests welcome on [GitHub](https://github.com/nullhack/pytest-beehave/issues).

---

## License

MIT — see [LICENSE](LICENSE).
