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

---

## Session: 2026-04-19 — Artifact normalization: per-feature Domain Models migrated from old-format .feature files

### Feature: features-path-config — Domain Model
| Type | Name | Candidate Class/Method | In Scope |
|------|------|----------------------|----------|
| Noun | features folder path | path to `docs/features/` directory | Yes |
| Noun | `pyproject.toml` | project configuration file | Yes |
| Noun | `[tool.beehave]` section | configuration section in `pyproject.toml` | Yes |
| Noun | default path | `docs/features/` relative to project root | Yes |
| Verb | read config | parse `[tool.beehave]` from `pyproject.toml` | Yes |
| Verb | resolve path | make the configured path absolute relative to project root | Yes |
| Verb | fall back to default | use `docs/features/` if no config present | Yes |

### Feature: plugin-hook — Domain Model
| Type | Name | Candidate Class/Method | In Scope |
|------|------|----------------------|----------|
| Noun | pytest plugin | `BeehavePlugin` | Yes |
| Noun | pytest session | pytest lifecycle | Yes |
| Noun | pytest config | `pytest_configure` hook | Yes |
| Noun | stub sync | full sync operation | Yes |
| Verb | register plugin | `pytest_configure` entry point | Yes |
| Verb | run before collection | `pytest_sessionstart` or `pytest_collection_start` | Yes |
| Verb | trigger stub sync | invoke sync logic before collection | Yes |

### Feature: deprecation-sync — Domain Model
| Type | Name | Candidate Class/Method | In Scope |
|------|------|----------------------|----------|
| Noun | `@deprecated` tag | Gherkin tag directly on an Example block | Yes |
| Noun | Gherkin tag inheritance | `@deprecated` on a `Rule:` or `Feature:` node applies to all child Examples | Yes |
| Noun | `@pytest.mark.deprecated` | pytest marker on a test function | Yes |
| Noun | backlog stage | `docs/features/backlog/` | Yes |
| Noun | in-progress stage | `docs/features/in-progress/` | Yes |
| Noun | completed stage | `docs/features/completed/` | Yes |
| Verb | detect deprecated | check Example tags for `@deprecated` (direct and inherited) | Yes |
| Verb | add marker | prepend `@pytest.mark.deprecated` to test function | Yes |
| Verb | remove marker | remove `@pytest.mark.deprecated` when tag is gone | Yes |

### Feature: auto-id-generation — Domain Model
| Type | Name | Candidate Class/Method | In Scope |
|------|------|----------------------|----------|
| Noun | Example block | Gherkin scenario | Yes |
| Noun | `@id` tag | `@id:<8-char-hex>` tag on Example | Yes |
| Noun | `.feature` file | Gherkin feature file on disk | Yes |
| Noun | hex ID | 8-character lowercase hex string | Yes |
| Noun | CI environment | read-only or automated environment | Yes |
| Verb | detect missing ID | scan Example tags for `@id` | Yes |
| Verb | generate ID | produce a unique 8-char hex string | Yes |
| Verb | write back | insert `@id` tag into `.feature` file in-place | Yes |
| Verb | fail run | abort pytest with a clear error message | Yes |

### Feature: multilingual-feature-parsing — Domain Model
| Type | Name | Candidate Class/Method | In Scope |
|------|------|----------------------|----------|
| Noun | `.feature` file | Gherkin feature file on disk | Yes |
| Noun | `# language: xx` comment | Language directive at top of feature file | Yes |
| Noun | non-English keyword | Gherkin keyword in a supported dialect | Yes |
| Noun | feature slug | Underscored folder name used in Python identifiers | Yes |
| Noun | docstring | Step-by-step docstring in generated test stub | Yes |
| Noun | pyproject.toml language config | Project-level default language setting | No |
| Noun | bad language code error handling | Custom error for unrecognised language codes | No |

### Feature: features-dir-bootstrap — Domain Model
| Type | Name                  | Candidate Class/Method                          | In Scope |
|------|-----------------------|-------------------------------------------------|----------|
| Noun | features directory    | root configured features path (e.g. docs/features/) | Yes  |
| Noun | backlog subfolder     | docs/features/backlog/                          | Yes      |
| Noun | in-progress subfolder | docs/features/in-progress/                      | Yes      |
| Noun | completed subfolder   | docs/features/completed/                        | Yes      |
| Noun | .feature file         | Gherkin file found directly in the root features dir | Yes |
| Noun | pytest plugin         | BeehavePlugin                                   | Yes      |
| Verb | bootstrap             | create missing canonical subfolders             | Yes      |
| Verb | migrate               | move root-level .feature files to backlog/      | Yes      |
| Verb | detect                | check whether the three-subfolder structure exists | Yes   |

### Feature: multilingual-feature-parsing — Session Syntheses

Session 1 Synthesis: pytest-beehave is transparent to Gherkin language. The gherkin-official library
auto-detects the `# language: xx` comment and switches keyword matching accordingly. Function names
and class names are always derived from the feature folder name (a filesystem path), so they are
valid Python identifiers regardless of the `.feature` file language. Docstrings preserve the original
non-English keywords. Mixed-language projects work because each file is parsed independently.

Session 3 Synthesis: pytest-beehave delegates all language handling to gherkin-official. When a
`.feature` file begins with `# language: es`, the parser switches to Spanish keywords
(Característica:, Dado:, Cuando:, Entonces:, etc.) automatically. When it begins with
`# language: zh-CN`, it switches to Chinese keywords (功能:, 假设:, 当:, 那么:, etc.). The plugin
never inspects the language directive itself. Generated test stubs use the feature folder name for
function/class names (always ASCII-safe slugs), and preserve the original keyword text verbatim in
docstrings. A project with mixed-language `.feature` files works because each file is parsed in
isolation.

### Feature: features-dir-bootstrap — Session Syntheses

Session 1 Synthesis: The bootstrap feature ensures the three-subfolder structure (backlog/,
in-progress/, completed/) exists inside the configured features directory. It runs as the first
action of every pytest invocation, before stub sync. If the root features directory exists but any
subfolder is missing, the plugin creates the missing subfolder(s) independently. Any `.feature`
files found directly in the root features directory are moved to backlog/; non-`.feature` files are
not touched. Name collisions during migration result in the root-level file being left in place with
a warning. If the structure is already correct and no root-level `.feature` files exist, the
bootstrap is a silent no-op. If the root features directory does not exist, the bootstrap is skipped
entirely.

Session 3 Synthesis: The features-dir-bootstrap feature ensures the Beehave plugin can always
operate on a well-structured features directory. When pytest is invoked, the plugin runs a bootstrap
step as its very first action (before stub sync). The bootstrap inspects the configured features
directory and, if it exists, ensures all three canonical subfolders (backlog/, in-progress/,
completed/) are present — creating any that are missing. It then scans for `.feature` files directly
in the root features directory (not inside any subfolder) and moves them to backlog/, making them
available for stub sync in the same pytest run. Non-`.feature` files in the root are left untouched.
If a name collision occurs (a root-level `.feature` file shares a name with an existing backlog/
file), the root-level file is left in place and a warning is emitted. If the structure is already
correct and no root-level `.feature` files exist, the bootstrap is a complete no-op with no terminal
output. If the root features directory does not exist, the bootstrap is skipped entirely.
