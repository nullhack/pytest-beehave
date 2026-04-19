# Current Work

Feature: stub-format-config
Step: 5 (Accept)
Source: docs/features/in-progress/stub-format-config.feature

## Progress
- [x] Stage 1 Discovery: stub-format-config scoped and baselined
- [x] Stage 2A Stories: 5 Rule blocks written and INVEST-gated
- [x] Stage 2B Criteria: 7 Examples written with @id tags
- [x] `@id:a1b2c3d4`: Stub is a top-level function when stub_format is absent
- [x] `@id:b2c3d4e5`: Absent stub_format does not raise an error
- [x] `@id:f1e2d3c4`: Stub is a top-level function when stub_format = "functions"
- [x] `@id:a2b3c4d5`: Stub is a class method when stub_format = "classes"
- [x] `@id:b3c4d5e6`: Class name is derived from the Rule title slug
- [x] `@id:f6a7b8c9`: Pytest fails at startup when stub_format has an unrecognised value
- [x] `@id:a7b8c9d0`: No-Rule feature produces module-level functions regardless of stub_format = "classes"
- [x] Step 4 Verify: APPROVED (reviewer)

## Next
Run @software-engineer — rename test functions in tests/features/stub_format_config/explicit_functions_format_test.py (c3d4e5f6 → f1e2d3c4) and tests/features/stub_format_config/classes_format_selection_test.py (d4e5f6a7 → a2b3c4d5, e5f6a7b8 → b3c4d5e6), remove the non-conforming skip reasons, then re-run the quality gate (uv run task test) before handing back to @product-owner for Step 5 acceptance
