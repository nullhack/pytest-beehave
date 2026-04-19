# Current Work

Feature: stub-format-config
Step: 1 (SCOPE) — COMPLETE
Source: docs/features/backlog/stub-format-config.feature

## Progress
- [x] Stage 1 Discovery: stub-format-config scoped and baselined
- [x] Stage 2A Stories: 5 Rule blocks written and INVEST-gated
- [x] Stage 2B Criteria: 7 Examples written with @id tags
- [x] `@id:a1b2c3d4`: Stub is a top-level function when stub_format is absent
- [x] `@id:b2c3d4e5`: Absent stub_format does not raise an error
- [x] `@id:c3d4e5f6`: Stub is a top-level function when stub_format = "functions"
- [x] `@id:d4e5f6a7`: Stub is a class method when stub_format = "classes"
- [x] `@id:e5f6a7b8`: Class name is derived from the Rule title slug
- [x] `@id:f6a7b8c9`: Pytest fails at startup when stub_format has an unrecognised value
- [x] `@id:a7b8c9d0`: No-Rule feature produces module-level functions regardless of stub_format = "classes"

## Next
Run @software-engineer — load skill implementation and begin Step 2 (Architecture) for stub-format-config
