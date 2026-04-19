# Discovery Journal: pytest-beehave

---

## 2026-04-18 — Project: Session 1
Status: COMPLETE

| ID | Question | Answer | Status |
|----|----------|--------|--------|
| Q1 | Who are the users? | Python developers using the python-project-template workflow who run `pytest` and want their Gherkin acceptance criteria stubs kept in sync automatically | ANSWERED |
| Q2 | What does the product do at a high level? | A pytest plugin that automatically syncs test stubs from Gherkin `.feature` files when `pytest` is run — generating IDs for un-tagged Examples, writing generic step docstrings, and applying deprecation markers | ANSWERED |
| Q3 | Why does it exist — what problem does it solve? | Removes the manual step of running `uv run task gen-tests` before every test run; ensures stubs are always in sync with acceptance criteria without developer intervention | ANSWERED |
| Q4 | When and where is it used? | During local development and CI, whenever `pytest` is invoked; operates on the `docs/features/` directory structure of the python-project-template layout | ANSWERED |
| Q5 | Success — how do we know it works? | Running `pytest` automatically syncs stubs; new Examples get IDs written back to `.feature` files; deprecated Examples get `@pytest.mark.deprecated` applied; stubs for backlog/in-progress are created/updated; completed stubs are only touched for deprecation | ANSWERED |
| Q6 | Failure — what does failure look like? | Plugin modifies test bodies or parameters; plugin breaks `pytest` collection; plugin silently corrupts `.feature` files; plugin fails in CI without a graceful fallback | ANSWERED |
| Q7 | Out-of-scope — what are we explicitly not building? | A new test runner; changes to the Gherkin parser; support for non-standard feature folder layouts; GUI or web interface; any feature not related to stub sync and ID generation | ANSWERED |
| Q8 | Should the plugin support configuration options? | Yes — custom features folder path via `pyproject.toml`; always-on (no on/off switch) | ANSWERED |
| Q9 | Auto-ID write-back in CI / read-only environments? | Fail the pytest run with an error if untagged Examples are found; all Examples MUST have an ID | ANSWERED |
| Q10 | Empty feature folders behaviour? | Skip silently — no warning | ANSWERED |
| Q11 | pytest hook timing? | Sync BEFORE collection so newly generated stubs are collected in the same run | ANSWERED |
| Q12 | "All steps" in docstrings? | Every individual step line including And/But continuations | ANSWERED |
| Q13 | Plugin location? | This repository IS the plugin (`name = "pytest-beehave"` in pyproject.toml) | ANSWERED |
| Q14 | Default marker for new stubs? | `@pytest.mark.skip(reason="not yet implemented")` — stub-sync always adds this; software-engineer adds `@pytest.mark.slow` when the test is genuinely slow | ANSWERED |
| Q15 | Test structure: plain functions or class-based? | All tests are top-level functions — no classes. Rule blocks → `<rule_slug>_test.py`; no Rule blocks → `examples_test.py` | ANSWERED |
| Q16 | What owns stub-sync markers vs software-engineer markers? | Two non-overlapping domains: stub-sync owns `skip/not-yet-implemented`, `skip/orphan`, `skip/non-conforming`, `deprecated`; software-engineer owns `slow` — crossing is prohibited | ANSWERED |
| Q17 | How is test conformance defined? | Two-part: (1) correct file name (`<rule_slug>_test.py` or `examples_test.py`), (2) correct function name (`test_<feature_slug>_<@id>`) — both must match | ANSWERED |
| Q18 | How is `@deprecated` inherited from parent Gherkin nodes? | `@deprecated` on a `Rule:` or `Feature:` node is treated as present on all child Examples for marker sync purposes | ANSWERED |
| Q19 | What library for reading/writing test files? | `libcst` — preserves formatting and comments; needs to be added as dependency | ANSWERED |

---

## 2026-04-18 — Project: Session 2 — Behavior Groups
Status: COMPLETE

| ID | Group | Question | Answer | Status |
|----|-------|----------|--------|--------|
| Q20 | Lifecycle | How does the plugin handle the three feature stages (backlog, in-progress, completed) differently? | backlog + in-progress: full stub creation and updates; completed: orphan detection only — no new stubs, no updates | ANSWERED |
| Q21 | Conformance | What is the conformance model — what makes a test "correctly placed"? | Two-part: correct file name and correct function name — both must match | ANSWERED |
| Q22 | Marker ownership | How is marker ownership split between stub-sync and the developer? | Two non-overlapping domains: stub-sync owns skip markers and deprecated; developer owns slow — neither crosses into the other's territory | ANSWERED |
