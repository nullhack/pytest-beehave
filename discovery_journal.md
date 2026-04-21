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

---

## 2026-04-18 — Feature: features-path-config — Session 1
Status: COMPLETE

| ID | Question | Answer | Status |
|----|----------|--------|--------|
| Q1 | What is the exact config key name? | `features_path` under `[tool.beehave]` | ANSWERED |
| Q2 | Should an invalid/missing configured path be a hard error or a warning? | Hard error — if the user explicitly configured a path that doesn't exist, fail loudly | ANSWERED |

---

## 2026-04-18 — Feature: plugin-hook — Session 1
Status: COMPLETE

| ID | Question | Answer | Status |
|----|----------|--------|--------|
| Q1 | Which pytest hook runs before collection? | `pytest_configure` runs at startup before collection; `pytest_sessionstart` runs after collection starts — use `pytest_configure` or a custom `pytest_collection_start` hook | ANSWERED |
| Q2 | Should the plugin emit any output to the pytest terminal during sync? | Yes — brief summary of actions taken (same style as current script) | ANSWERED |

---

## 2026-04-18 — Feature: deprecation-sync — Session 1
Status: COMPLETE

| ID | Question | Answer | Status |
|----|----------|--------|--------|
| Q1 | Should deprecation sync run even if stub sync is skipped for completed features? | Yes — deprecation sync always runs on all 3 stages regardless | ANSWERED |

---

## 2026-04-18 — Feature: auto-id-generation — Session 1
Status: COMPLETE

| ID | Question | Answer | Status |
|----|----------|--------|--------|
| Q1 | Should ID uniqueness be guaranteed globally (across all feature files) or just within a single file? | Within-file only — scan the current `.feature` file for existing `@id` values before generating new ones for that file; 8-char hex collision probability across files is negligible | ANSWERED (REVISED) |
| Q2 | How is "CI / read-only" detected — by checking file writability or by checking a `CI` env var? | Check file writability — more reliable across different CI systems | ANSWERED |

---

## 2026-04-18 — Feature: multilingual-feature-parsing — Session 1
Status: COMPLETE

| ID | Question | Answer | Status |
|----|----------|--------|--------|
| Q1 | Should beehave support a project-level default language? | No — transparent; `# language: xx` is the only mechanism | ANSWERED |
| Q2 | Which languages need verification? | Spanish (es) and Chinese Simplified (zh-CN) | ANSWERED |
| Q3 | Custom error handling for bad language codes? | No — out of scope | ANSWERED |
| Q4 | Mixed-language projects work transparently? | Yes — each file parsed independently | ANSWERED |
| Q5 | Docstrings normalise non-English keywords to English? | No — preserve original keyword | ANSWERED |
| Q6 | Scope? | Tests only — verify existing behaviour | ANSWERED |

---

## 2026-04-18 — Feature: features-dir-bootstrap — Session 1
Status: COMPLETE

| ID | Question | Answer | Status |
|----|----------|--------|--------|
| Q1 | What triggers the bootstrap — always on every run, or only when structure is missing? | Always run on every pytest invocation; it is a no-op when structure is already correct | ANSWERED |
| Q2 | What constitutes "missing structure" — all three subfolders absent, or any one? | Any missing subfolder triggers creation of that subfolder; all three must exist | ANSWERED |
| Q3 | What if only some subfolders exist? | Create only the missing ones; existing subfolders are not touched | ANSWERED |
| Q4 | Are only .feature files migrated, or all files? | Only .feature files directly in the root features folder; other files are left in place | ANSWERED |
| Q5 | What if a root-level .feature file has the same name as one already in backlog/? | Leave the root-level file in place and emit a warning; do not overwrite | ANSWERED |
| Q6 | Should bootstrap emit terminal output? | Yes — report each action (subfolder created, file moved, collision warning); no output if no-op | ANSWERED |
| Q7 | What if the root features directory does not exist at all? | Bootstrap is skipped; existing graceful handling in plugin-hook covers this case | ANSWERED |
| Q8 | Does bootstrap run before or after stub sync? | Bootstrap runs first so migrated files are available for stub sync in the same run | ANSWERED |
| Q9 | Are non-.feature files in the root features folder migrated? | No — only .feature files are migrated; discovery.md and other files stay in place | ANSWERED |

---

## 2026-04-18 — Feature: features-dir-bootstrap — Session 2
Status: COMPLETE

| ID | Question | Answer | Status |
|----|----------|--------|--------|
| Q10 | Are nested non-canonical subdirectories in the root features folder left alone? | Yes — only the three canonical subfolders are managed; any other subdirectory is ignored | ANSWERED |
| Q11 | Is the bootstrap idempotent — safe to run multiple times? | Yes — creating an already-existing subfolder is a no-op; migration only moves files not already in a subfolder | ANSWERED |

---

## 2026-04-19 — Session 3
Status: IN-PROGRESS

### Feature: example-hatch

| ID | Question | Answer | Status |
|----|----------|--------|--------|
| Q1 | What interface is used to invoke the hatch? | `pytest --beehave-hatch` (bee-related wordplay — bees hatch from cells, generating a new colony of examples) — a pytest CLI flag | ANSWERED |
| Q2 | What content should be generated? | `docs/features/` (or the configured path) with pre-defined Gherkin showcasing ALL plugin capabilities; Feature names, scenarios, and step text should use bee/hive metaphors | ANSWERED |
| Q3 | Should randomization use external libraries (e.g. Hypothesis)? | No external dependencies — use Python stdlib only (e.g. `random`, `uuid`) to vary generated content so it is not boring | ANSWERED |
| Q4 | What does success look like? | Run the flag → `docs/features/` is generated → run `pytest` → stubs are properly generated with no errors | ANSWERED |
| Q5 | Where does the generated folder land? | Respects the configured features path (`features_path` in `[tool.beehave]`); defaults to `docs/features/` | ANSWERED |
| Q6 | What happens if the target features directory already contains content? | Fail loudly with a descriptive error; provide a `--beehave-hatch-force` flag to overwrite (PO-resolved by convention — consistent with project hard-error philosophy) | RESOLVED-BY-PO |

Status: COMPLETE

---

## 2026-04-19 — Feature: stub-format-config — Session 1
Status: IN-PROGRESS

### Feature: stub-format-config

| ID | Question | Answer | Status |
|----|----------|--------|--------|
| Q1 | What config key name and section? | `stub_format` under `[tool.beehave]` in `pyproject.toml` | ANSWERED |
| Q2 | What are the valid values? | `"functions"` (default, top-level functions, no class wrapper) and `"classes"` (class Test<RuleSlug> wrapping) — case-sensitive | ANSWERED |
| Q3 | What is the default when the key is absent? | `"functions"` — existing projects that never set this key get top-level functions | ANSWERED |
| Q4 | Does this affect features with no Rule blocks? | No — no-Rule features always produce module-level functions in `examples_test.py` regardless of `stub_format` | ANSWERED |
| Q5 | What happens with an invalid value (e.g. `stub_format = "methods"`)? | Hard error at pytest startup with a descriptive message — consistent with the project's hard-error philosophy | ANSWERED |
| Q6 | Does changing `stub_format` reformat existing stubs? | No — only new stubs are affected; existing stubs are not touched | ANSWERED |
| Q7 | Is the setting per-feature or project-wide? | Project-wide — applies uniformly to all Rule-block features | ANSWERED |
| Q8 | What happens to existing projects using the plugin (no `stub_format` key)? | They get `"functions"` (the new default) — top-level functions, which is the desired behavior going forward | ANSWERED |
| Q9 | What happens if a project was relying on class-based output? | They set `stub_format = "classes"` in `[tool.beehave]` to restore the old behavior | ANSWERED |
| Q10 | Is the `"classes"` format identical to the old class-based stub output? | Yes — `class Test<RuleSlug>:` wrapper with methods inside, same as what `stub_writer.py` currently produces | ANSWERED |

Status: COMPLETE
