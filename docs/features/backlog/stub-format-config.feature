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
