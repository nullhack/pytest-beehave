# Discovery: pytest-beehave

---

## Session: 2026-04-18 — Initial Synthesis

### Scope
pytest-beehave is a pytest plugin for Python developers using the python-project-template workflow. It eliminates the manual `gen-tests` step by automatically syncing test stubs from Gherkin `.feature` files on every `pytest` invocation — before collection, so new stubs are collected in the same run. It generates IDs for untagged Examples (failing hard in CI), writes step docstrings, and applies deprecation markers. The plugin is always-on with a configurable features folder path. It never modifies test bodies and must not corrupt `.feature` files. Out of scope: new test runner, non-standard layouts, GUI, Gherkin parser changes.

Feature stages determine what the plugin does: backlog and in-progress features receive full stub creation and updates; completed features receive only orphan detection. Marker ownership is strictly split — stub-sync owns skip/deprecated markers; the developer owns slow.

Template §1: CONFIRMED

### Behavior Groups
- Configuration: custom features path via pyproject.toml; always-on behaviour
- ID generation: detect missing @id tags, write IDs back to .feature files, fail in CI if untagged
- Stub creation: create new stubs for backlog/in-progress; top-level functions; skip marker; all-steps docstring
- Stub updates: rename/update existing stubs; conformance enforcement; non-conforming redirect
- Deprecation sync: toggle @pytest.mark.deprecated; Gherkin tag inheritance from Rule/Feature nodes
- Lifecycle integration: pytest hook registration; run before collection

Template §2: CONFIRMED

### Feature List
- `features-path-config` — custom features folder path via pyproject.toml
- `plugin-hook` — pytest lifecycle integration (register plugin, run before collection)
- `auto-id-generation` — detect missing @id tags, generate IDs, write back or fail in CI
- `stub-creation` — create new test stubs for backlog/in-progress; top-level functions, skip marker, docstrings
- `stub-updates` — update/rename/orphan-mark existing stubs; conformance enforcement; non-conforming redirect
- `deprecation-sync` — toggle @pytest.mark.deprecated across all 3 feature stages; Gherkin tag inheritance

### Domain Model
| Type | Name | Description | In Scope |
|------|------|-------------|----------|
| Noun | test stub | top-level function `test_<feature_slug>_<@id>()` | Yes |
| Noun | test file | `<rule_slug>_test.py` or `examples_test.py` | Yes |
| Noun | feature slug | `.feature` file stem, hyphens → underscores, lowercase | Yes |
| Noun | rule slug | `Rule:` title slugified with hyphens, lowercase | Yes |
| Noun | docstring | verbatim step-by-step content in test stub | Yes |
| Noun | backlog stage | `docs/features/backlog/` | Yes |
| Noun | in-progress stage | `docs/features/in-progress/` | Yes |
| Noun | completed stage | `docs/features/completed/` — stub creation excluded | Yes |
| Noun | conforming test | test with correct file name AND correct function name | Yes |
| Noun | orphan test | test function with no matching `@id` in any `.feature` file | Yes |
| Verb | create stub | write new top-level test function for new Example | Yes |
| Verb | mark orphan | apply `@pytest.mark.skip(reason="orphan: ...")` | Yes |
| Verb | mark non-conforming | apply `@pytest.mark.skip(reason="non-conforming: moved to <file>")` | Yes |
| Verb | deprecate stub | apply `@pytest.mark.deprecated` when Gherkin `@deprecated` tag present | Yes |

Status: BASELINED (2026-04-18)
Template §3: CONFIRMED — stakeholder approved 2026-04-18

---

## Session: 2026-04-18 — Revision: remove class-based test structure

### Scope
All test stubs are top-level functions. The `class Test<RuleSlug>` wrapper described in Q15 of the initial discovery was never implemented. Conformance is now two-part: (1) correct file name and (2) correct function name. No class context check exists.

### Feature List
- `stub-creation` — updated: top-level functions only, not class methods
- `stub-updates` — updated: conformance is 2-part (file + function name), not 3-part

### Domain Model
| Type | Name | Description | Change |
|------|------|-------------|--------|
| Noun | conforming test | test with correct file name AND correct function name | Updated: was 3-part (file + class context + function name), now 2-part |

---

## Session: 2026-04-19 — Feature: report-steps

### Scope
`report-steps` surfaces BDD acceptance criteria in two independent output channels: the terminal (at `-v` or above) and pytest-html reports (when `pytest-html` is installed). Both channels are scoped exclusively to tests under `tests/features/` and are independently configurable via `pyproject.toml`. Steps are always rendered verbatim from the test docstring — no reformatting. Both channels are wired into the single existing `pytest_configure` entry point. `pytest-html` is an optional install extra (`pip install pytest-beehave[html]`); when it is absent the HTML channel is silently inactive with no error raised.

Feature stages and marker state do not affect rendering — steps are shown regardless of test outcome (pass, fail, skip, error).

Status: BASELINED (2026-04-18)

### Behavior Groups
- Terminal channel: print docstring verbatim below the test path line at `-v` or above; blank line separator; scoped to `tests/features/` only
- HTML channel: add an "Acceptance Criteria" column to the pytest-html report; populate with verbatim docstring for feature tests; blank for non-feature tests
- Configuration: `show_steps_in_terminal` (default `true`); `show_steps_in_html` (default `true`); both in `pyproject.toml`
- Optional dependency: `pytest-html` guarded at runtime — absent means HTML channel is silently skipped

### Feature List
- `report-steps` — terminal steps display and HTML acceptance criteria column for `tests/features/` tests

### Domain Model
| Type | Name | Description | In Scope |
|------|------|-------------|----------|
| Noun | terminal channel | verbatim docstring printed below test path at -v or above | Yes |
| Noun | HTML channel | "Acceptance Criteria" column in pytest-html report | Yes |
| Noun | feature test | any test residing under `tests/features/` | Yes |
| Noun | non-feature test | any test outside `tests/features/` (e.g. `tests/unit/`) | Yes — explicitly excluded from output |
| Noun | verbatim steps | docstring content rendered with no reformatting | Yes |
| Verb | render steps | print/inject docstring into the appropriate output channel | Yes |
| Verb | suppress steps | omit output when channel is disabled or test is out of scope | Yes |

### Out of Scope
- Reformatting or parsing of step text
- Rendering steps for tests outside `tests/features/`
- Any output channel other than terminal and pytest-html
- Making `pytest-html` a required dependency

Template §3: CONFIRMED — stakeholder approved 2026-04-18
