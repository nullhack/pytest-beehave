Feature: Stub format configuration

  Controls the output format of generated test stubs via a `stub_format` key in
  `[tool.beehave]` in `pyproject.toml`. Two formats are supported: `"functions"`
  (default) generates top-level functions in `<rule_slug>_test.py` with no class
  wrapper; `"classes"` generates stubs as methods inside `class Test<RuleSlug>`.
  When the key is absent, `"functions"` is used. Existing projects that relied on
  the class-based output can opt back in by setting `stub_format = "classes"`.

  Status: BASELINED (2026-04-19)

  Rules (Business):
  - `stub_format` lives under `[tool.beehave]` in `pyproject.toml`
  - Valid values are exactly `"functions"` and `"classes"` (case-sensitive)
  - Default when key is absent: `"functions"`
  - Features with no `Rule:` blocks always produce module-level functions in `examples_test.py` regardless of `stub_format`
  - The format setting applies to ALL Rule-block features in the project uniformly

  Constraints:
  - Invalid `stub_format` values must produce a hard error at pytest startup (not silently ignored)
  - Changing `stub_format` does not retroactively reformat existing stubs — only new stubs are affected

  Rule: Default format selection
    As a developer
    I want stub generation to default to top-level functions when no stub_format is configured
    So that new projects and existing projects without explicit configuration get the preferred format automatically

  Rule: Explicit functions format
    As a developer
    I want to explicitly set stub_format = "functions" in pyproject.toml
    So that I can document my format choice and ensure top-level function stubs are generated

  Rule: Classes format selection
    As a developer
    I want to set stub_format = "classes" in pyproject.toml
    So that I can restore the class-wrapped stub output for projects that prefer that style

  Rule: Invalid format rejection
    As a developer
    I want pytest to fail immediately with a clear error when stub_format has an unrecognised value
    So that misconfiguration is caught at startup rather than silently producing wrong output

  Rule: No-Rule feature unaffected
    As a developer
    I want features with no Rule blocks to always produce module-level functions in examples_test.py
    So that the stub_format setting does not change the behavior of no-Rule features
