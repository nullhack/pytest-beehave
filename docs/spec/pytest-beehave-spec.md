# pytest-beehave Specification

## Overview

pytest-beehave is a pytest plugin that integrates the `beehave` library into the pytest lifecycle. It generates missing test stubs from Gherkin `.feature` files, checks consistency between features and tests, and displays BDD steps in both terminal output and HTML reports.

## Identity

| Field | Value |
|-------|-------|
| Package name | `pytest-beehave` |
| Python support | >= 3.14 |
| Runtime dependency | `beehave>=0.4.0` |
| Optional extra | `pytest-beehave[html]` → `pytest-html>=4.1.1` |
| Entry point | `pytest11` → `pytest_beehave.plugin` |

## Architecture

The plugin is a thin orchestration layer over `beehave`. It does not implement its own Gherkin parser, stub generator, or consistency checker. All heavy lifting delegates to `beehave`:

```
beehave library          pytest-beehave plugin
─────────────────        ─────────────────────
config.load_config()  ←── reads [tool.beehave] from pyproject.toml
gherkin.parse_feature()  ←── parses .feature files into ScenarioInfo
generate.generate_stubs()  ←── writes Hypothesis test stubs to disk
check.check_all()  ←── returns Violation[] for drift/inconsistency
models.ScenarioInfo  ←── steps, placeholders, examples data for display
```

### Module structure

```
pytest_beehave/
  __init__.py         Package version
  plugin.py           pytest hooks: configure, makereport
  steps_display.py    Terminal verbose steps output
  html_column.py      pytest-html "Scenario" column
```

## Lifecycle

```
pytest_configure
  ├─ load_config(rootdir)               → beehave.Config
  ├─ features_dir exists?
  │   ├─ No → return silently
  │   └─ Yes → continue
  ├─ For each .feature file (sorted):
  │   ├─ parse_feature(path, config)    → {function_name: ScenarioInfo}
  │   └─ generate_stubs(rel_path, config) → writes stubs to tests/features/
  ├─ _add_skip_markers(tests_dir)         → adds @pytest.mark.skip to stubs
  ├─ check_all(config)                  → list[Violation]
  ├─ Report violations to terminal/stderr
  ├─ verbose >= 1 (-v)? → register StepsReporter
  └─ pytest-html available? → register HtmlStepsPlugin

pytest collection
  └─ Stubs already on disk; pytest collects normally

pytest_runtest_makereport  (hookwrapper)
  └─ Lookup item.originalname in ScenarioInfo map
     └─ Found → attach _beehave_steps to report

pytest_runtest_logreport  [StepsReporter, if --beehave-verbose]
  └─ Report has _beehave_steps? → print indented steps under test name

pytest_html_results_table_header/row  [HtmlStepsPlugin, if pytest-html installed]
  └─ Insert "Scenario" column at position 2
```

## Configuration

All configuration lives under `[tool.beehave]` in `pyproject.toml`, managed by `beehave.config.load_config()`:

```toml
[tool.beehave]
features_dir = "docs/features"      # default: docs/features
tests_dir = "tests/features"        # default: tests/features
default_strategy = "text"           # default: text (Hypothesis strategy for placeholders)
background_check_numeric = true     # default: true
background_check_string = true      # default: true
```

If `features_dir` does not exist, the plugin exits silently (no error, no stub generation).

## CLI Options

pytest-beehave has no custom CLI flags. It integrates with pytest's native flags:

| Flag | Effect |
|------|--------|
| `-v` / `-vv` | Enables terminal steps display (shows BDD steps under each test name) |
| `--html=<path>` | Enables HTML report with Scenario column (requires `pytest-html`) |

No `--beehave-verbose` flag exists. The plugin follows pytest's verbosity conventions.

## Feature 1: Stub Generation

### Hook: `pytest_configure`

For every `.feature` file found recursively under `features_dir`:

1. **Parse** via `beehave.gherkin.parse_feature(path, config, seen_names)` — returns `{function_name: ScenarioInfo}`
2. **Generate stubs** via `beehave.generate.generate_stubs(rel_path, config)` — creates Hypothesis-based test stubs under `tests_dir`
3. **Add skip markers** via `_add_skip_markers(tests_dir)` — adds `@pytest.mark.skip(reason="not implemented")` to newly generated stubs

The `seen_names` dict is passed across files to detect function-name collisions.

### Skip markers

After beehave generates stubs, pytest-beehave post-processes each test file under `tests_dir` to add `@pytest.mark.skip(reason="not implemented")` decorators to stub functions (functions whose body is only `...`).

**Behavior:**
- The skip marker is inserted **before all existing decorators** (e.g., `@example`, `@given`)
- `import pytest` is added at the top of the file if not already present
- Functions already marked with `@pytest.mark.skip` are left unchanged (idempotent)
- Functions whose body is not `...` (i.e., already implemented) are never touched
- Since beehave preserves existing functions across runs, re-running pytest does not re-add the marker to functions that were already present

**TDD workflow:**
1. `pytest --collect-only` → stubs generated with `@pytest.mark.skip` → all skipped
2. Developer removes `@pytest.mark.skip`, writes body → test runs and fails (red)
3. Developer fixes implementation → test passes (green)
4. New scenarios added to `.feature` files → only new stubs get the skip marker

### Error handling

- Parse errors: logged as `[beehave] PARSE ERROR: <path>: <message>`, processing continues to next file
- Generation errors: logged as `[beehave] GENERATE ERROR: <path>: <message>`, processing continues
- `beehave.generate.generate_stubs` calls `sys.exit(1)` on missing files — caught as `SystemExit` by the `Exception` handler

### Scenario-to-test mapping

beehave links scenarios to tests by **function name**:

```
Example: Simple passing test  →  def test_Simple_passing_test():
```

The function name is `test_` + title with spaces replaced by underscores. This is beehave's native convention — no `@id` tags, no step definitions, no glue code.

## Feature 2: Terminal Steps Display

### Activation

Automatic when pytest runs with `-v` or higher verbosity (`config.getoption("verbose") >= 1`).

### Implementation

`StepsReporter` is registered as a plugin during `pytest_configure` when verbosity is set.

### Hook: `pytest_runtest_logreport`

Triggers on:
- `report.when == "call"` (normal test execution)
- `report.when == "setup" and report.skipped` (skipped tests)

Looks up `report._beehave_steps` (set by `pytest_runtest_makereport`). If present, writes indented steps:

```
tests/features/foo/bar_test.py::test_Simple_passing_test PASSED
  Given a precondition exists
  When an action is taken
  Then the expected outcome occurs
```

Each step line is prefixed with two spaces. Steps come from `ScenarioInfo.steps` — formatted as `{keyword} {text}` (one per line).

### Non-feature tests

Tests whose `originalname` does not match any `ScenarioInfo.function_name` have no `_beehave_steps` attribute — they are silently skipped.

## Feature 3: HTML Scenario Column

### Activation

Automatic when `pytest-html` is importable (checked via `importlib.util.find_spec`). No CLI flag needed.

Installed via: `pip install pytest-beehave[html]`

### Column position

Inserted at index 2 (after "Test", before "Duration"):

| Result | Test | **Scenario** | Duration | Links |
|--------|------|-------------|----------|-------|

### Header cell

```html
<th class="sortable scenario" data-column-type="scenario">Scenario</th>
```

The `sortable` class and `data-column-type="scenario"` enable column sorting in the HTML report.

### Row cell

```html
<td class="col-scenario" style="white-space: pre-wrap;">{content}</td>
```

Content is HTML-escaped via `html.escape()` to prevent `<placeholder>` syntax from being interpreted as HTML tags.

For tests without matching scenarios, the cell is empty.

### Hooks

| Hook | Purpose |
|------|---------|
| `pytest_html_results_table_header(cells)` | Insert `<th>` at position 2 |
| `pytest_html_results_table_row(report, cells)` | Insert `<td>` at position 2 |

## Data Flow: Report Attachment

Steps flow from parsed features to display via the report object:

```
pytest_configure
  └─ scenarios: dict[str, ScenarioInfo]  →  config.stash[_scenarios_key]

pytest_runtest_makereport  (per test)
  └─ item.originalname → lookup in scenarios dict
     └─ found → report._beehave_steps = "Given ...\nWhen ...\nThen ..."

StepsReporter / HtmlStepsPlugin  (per test report)
  └─ getattr(report, "_beehave_steps", None)
     └─ present → display steps
```

The `item.originalname` attribute is used instead of `item.name` to handle parameterized/Hypothesis-generated test variants correctly (the base function name matches the ScenarioInfo key).

## Test-to-Scenario Matching

```
item.originalname  ←→  ScenarioInfo.function_name
```

Both use beehave's convention: `test_<snake_case_title>`. The match is exact string equality. No fuzzy matching, no ID lookup, no regex.

## File Layout Convention

beehave expects (and creates) this structure:

```
docs/features/              ← configured via features_dir
  **/*.feature              ← any subfolder structure is supported

tests/features/             ← configured via tests_dir
  <feature_slug>/           ← one directory per .feature file
    <rule_slug>_test.py     ← one file per Rule: block (or default_test.py)
```

## Stash Keys

| Key | Type | Set in | Read in |
|-----|------|--------|---------|
| `_beehave_config_key` | `beehave.config.Config` | `pytest_configure` | internal |
| `_scenarios_key` | `dict[str, ScenarioInfo]` | `pytest_configure` | `pytest_runtest_makereport` |

## Edge Cases

| Case | Behaviour |
|------|-----------|
| `features_dir` does not exist | Plugin returns silently; no errors, no stubs |
| `.feature` file has syntax errors | Logged as PARSE ERROR; next file processed |
| `generate_stubs` fails | Logged as GENERATE ERROR; next file processed |
| `-v` without matching scenarios | StepsReporter skips tests without `_beehave_steps` |
| Test has no matching scenario | No `_beehave_steps` attribute; display plugins skip it |
| `pytest-html` not installed | `HtmlStepsPlugin` not registered; no errors |
| `pytest-html` installed but no `--html` flag | `HtmlStepsPlugin` registered but hooks never fire (pytest-html only calls them during report generation) |
| Multiple `.feature` files with same scenario title | `seen_names` dict prevents collision; beehave raises `GherkinError` |
| Scenario Outline with Examples | beehave generates parameterized stubs with `@example()`; `originalname` still matches |
| Consistency violations found | Logged as `[beehave] ERROR` or `[beehave] WARNING`; run continues |
| Stub functions (body is `...`) | Excluded from placeholder/literal checks by `check_all`; marked with `@pytest.mark.skip` by plugin |
| Re-running pytest on existing stubs | Skip marker not re-added (beehave preserves existing functions, plugin only marks `...` bodies) |

## beehave API Dependencies

| beehave module | Function | Used for |
|----------------|----------|----------|
| `beehave.config` | `load_config(project_root)` | Reading `[tool.beehave]` from pyproject.toml |
| `beehave.gherkin` | `parse_feature(path, config, seen_names)` | Parsing .feature files into ScenarioInfo dicts |
| `beehave.generate` | `generate_stubs(feature_path, config)` | Writing Hypothesis test stubs to disk |
| `beehave.check` | `check_all(config)` | Detecting drift between features and tests |
| `beehave.models` | `ScenarioInfo`, `ParsedStep`, `Violation` | Data structures for steps display and violations |

## Feature 4: Consistency Checking

### Hook: `pytest_configure` (after stub generation)

After parsing features and generating stubs, the plugin runs `beehave.check.check_all(config)` to detect drift between feature files and test code.

### Violation types

| Type | Severity | Meaning |
|------|----------|---------|
| `unmapped-scenario` | ERROR | Scenario has no matching test function |
| `unmapped-test` | ERROR | Test function has no matching scenario |
| `misplaced-test` | WARNING | Test is in wrong rule file |
| `missing-placeholder` | ERROR | Test body missing a placeholder the scenario expects |
| `missing-literal` | ERROR | Test body missing a literal value from the scenario |
| `example-mismatch` | ERROR | Examples rows don't match `@example()` decorators |

### Reporting

Violations are logged to the terminal via `_write_line`:

```
[beehave] ERROR: tests/features/demo/default_test.py:5: unmapped-test: 'test_orphan' has no matching scenario
[beehave] WARNING: tests/features/rules/alpha_test.py:10: misplaced-test: 'test_beta' is in alpha_test.py but should be in beta_test.py
```

Stubs (functions containing only `...`) are excluded from placeholder and literal checks — they are expected to be incomplete.

### Resolution

Users fix violations by either:
- Implementing stub functions (replacing `...` with actual test logic)
- Removing orphan test functions
- Moving misplaced tests to the correct rule file
- Aligning Examples rows with `@example()` decorators
