Feature: Report Steps

  A pytest-beehave plugin capability that surfaces BDD acceptance criteria
  in two output channels: the terminal (when running with -v or above) and
  pytest-html reports (when pytest-html is installed). Both channels are
  independently configurable via pyproject.toml and are scoped exclusively
  to tests under tests/features/.

  Discovery:

  Status: BASELINED (2026-04-18)

  Entities:
  | Type | Name                        | Candidate Class/Method              | In Scope |
  |------|-----------------------------|-------------------------------------|----------|
  | Noun | Test docstring              | test.__doc__                        | Yes      |
  | Noun | pytest-html report          | HTML column hook                    | Yes      |
  | Noun | Terminal output             | pytest live output hook             | Yes      |
  | Noun | tests/features/ directory   | scope boundary                      | Yes      |
  | Noun | pyproject.toml config       | BeehaveConfig                       | Yes      |
  | Verb | Render steps in HTML        | pytest_html column hook             | Yes      |
  | Verb | Print steps to terminal     | pytest_runtest_logreport or similar | Yes      |
  | Verb | Detect verbosity            | config.option.verbose               | Yes      |
  | Verb | Scope to features dir       | path prefix check                   | Yes      |
  | Noun | pytest-html optional extra  | [html] install extra                | Yes      |
  | Noun | Unit tests (tests/unit/)    | non-feature tests                   | No       |
  | Noun | conftest.py (manual)        | replaced by this feature            | No       |

  Rules (Business):
  - Steps are always rendered verbatim from the test docstring — no reformatting
  - Both output channels are scoped exclusively to tests/features/
  - Steps are rendered regardless of test outcome (pass, fail, skip, error)
  - The HTML channel is silently absent when pytest-html is not installed

  Constraints:
  - show_steps_in_terminal defaults to true; active at -v or above
  - show_steps_in_html defaults to true; only active when pytest-html is installed
  - Both features are wired into the single existing pytest_configure entry point
  - pytest-html is an optional install extra: pip install pytest-beehave[html]

  Session 1 — Individual Entity Elicitation:
  | ID  | Question                                                                 | Answer                                                                                                      | Status   |
  |-----|--------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------|----------|
  | Q1  | Does terminal output trigger at -v or -vv?                               | -v or above                                                                                                 | ANSWERED |
  | Q2  | Terminal format: instead of, in addition to, or separate section?        | On the line below the test path, followed by one blank line                                                 | ANSWERED |
  | Q3  | Degrade gracefully if pytest-html not installed?                         | Yes — silently absent; also configurable via pyproject.toml with default=true                               | ANSWERED |
  | Q4  | Verbatim or reformatted docstring?                                       | Verbatim — no reformatting                                                                                  | ANSWERED |
  | Q5  | No docstring: skip, placeholder, or nothing?                             | Only render for tests/features/ — other folders show nothing                                                | ANSWERED |
  | Q6  | HTML column header name?                                                 | "Acceptance Criteria"                                                                                       | ANSWERED |
  | Q7  | pyproject.toml config key name for HTML?                                 | show_steps_in_html = true                                                                                   | ANSWERED |
  | Q8  | HTML and terminal: one toggle or independent?                            | Independent — two separate keys                                                                             | ANSWERED |
  | Q9  | Same plugin registration or separate concern?                            | Same plugin (single pytest_configure) — simpler, consistent with existing plugin                            | ANSWERED |
  | Q10 | CI terminal suppression?                                                 | No special CI suppression — follows show_steps_in_terminal in all environments                              | ANSWERED |
  | Q11 | Should steps print for skipped tests?                                    | Yes — print for all tests in tests/features/ regardless of outcome                                          | ANSWERED |
  | Q12 | show_steps_in_html pyproject.toml key still needed with optional extra?  | Yes — users may install [html] but opt out of the column                                                    | ANSWERED |
  Template §1: CONFIRMED
  Synthesis: The plugin gains two independent output capabilities scoped to tests/features/. Terminal
  output prints the verbatim docstring below the test path line (plus a blank line) at -v or above,
  controlled by show_steps_in_terminal (default true). HTML output adds an "Acceptance Criteria" column
  to pytest-html reports with the verbatim docstring, controlled by show_steps_in_html (default true),
  silently absent if pytest-html is not installed. Both are wired into the single pytest_configure entry
  point. Steps render for all test outcomes including skipped.

  Session 2 — Behavior Groups / Big Picture:
  | ID  | Question                                                    | Answer                                          | Status   |
  |-----|-------------------------------------------------------------|-------------------------------------------------|----------|
  | Q13 | Are the four behavior groups complete?                      | Yes — confirmed by stakeholder                  | ANSWERED |
  Template §2: CONFIRMED
  Behavior Groups:
  - Terminal steps rendering: verbatim docstring below test path + blank line, at -v or above, tests/features/ only, all outcomes
  - HTML column rendering: "Acceptance Criteria" column, verbatim docstring, tests/features/ only, blank elsewhere, silently absent without pytest-html
  - Configuration: two independent pyproject.toml keys (show_steps_in_html, show_steps_in_terminal), both default true
  - Plugin registration: both capabilities wired into single pytest_configure; [html] optional install extra

  Session 3 — Feature Synthesis:
  Synthesis: report-steps adds two independently-configurable output channels to pytest-beehave. The
  terminal channel prints verbatim BDD steps from the test docstring immediately below the test path
  line (followed by a blank line) whenever pytest runs with -v or higher verbosity, for any test under
  tests/features/, regardless of outcome. The HTML channel adds an "Acceptance Criteria" column to
  pytest-html reports showing the same verbatim docstring for tests/features/ tests and a blank cell
  for all others; it is silently absent when pytest-html is not installed. Both channels are controlled
  by independent pyproject.toml keys (show_steps_in_terminal, show_steps_in_html) that default to true.
  Both are registered within the single existing pytest_configure entry point. The optional install
  extra pip install pytest-beehave[html] pulls in pytest-html as a dependency.
  Template §3: CONFIRMED — stakeholder approved 2026-04-18

  Rule: Terminal Steps Display
    As a developer running pytest with verbosity
    I want BDD steps printed below each feature test result
    So that I can see what each test covers without opening the feature file

    @id:2ba9da81
    Example: Steps appear below test path at -v
      Given a test in tests/features/ with a docstring containing BDD steps
      When pytest runs with -v
      Then the docstring is printed verbatim on the line below the test path followed by a blank line

    @id:0869902b
    Example: Steps appear for skipped stubs at -v
      Given a test in tests/features/ marked skip with a docstring
      When pytest runs with -v
      Then the docstring is printed verbatim below the skipped test path followed by a blank line

    @id:99cbca75
    Example: No steps output for tests outside tests/features/
      Given a test in tests/unit/ with a docstring
      When pytest runs with -v
      Then no additional output is printed for that test

    @id:3c1b6d21
    Example: No steps output when show_steps_in_terminal is false
      Given show_steps_in_terminal = false in pyproject.toml
      And a test in tests/features/ with a docstring
      When pytest runs with -v
      Then no steps are printed for that test

    @id:3278cf4d
    Example: No steps output below -v verbosity
      Given show_steps_in_terminal = true in pyproject.toml
      And a test in tests/features/ with a docstring
      When pytest runs without any -v flag
      Then no steps are printed for that test

  Rule: HTML Acceptance Criteria Column
    As a developer reading a pytest-html report
    I want a dedicated column showing BDD steps for feature tests
    So that the report communicates what each test was verifying

    @id:88d58f5c
    Example: Acceptance Criteria column shows docstring for feature tests
      Given pytest-html is installed and show_steps_in_html = true
      And a test in tests/features/ with a docstring
      When the pytest-html report is generated
      Then the "Acceptance Criteria" column contains the verbatim docstring for that test

    @id:73c4a71a
    Example: Acceptance Criteria column is blank for non-feature tests
      Given pytest-html is installed and show_steps_in_html = true
      And a test outside tests/features/
      When the pytest-html report is generated
      Then the "Acceptance Criteria" column is blank for that test

    @id:6c592c81
    Example: HTML column absent when pytest-html not installed
      Given pytest-html is not installed
      When pytest runs and generates output
      Then no "Acceptance Criteria" column appears and no error is raised
