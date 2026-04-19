# Current Work

Feature: example-hatch
Step: 4 (Verify) — REJECTED
Source: docs/features/in-progress/example-hatch.feature

## Progress
- [x] `@id:1a2b3c4d`: Hatch creates the features directory tree when it does not exist
- [x] `@id:2b3c4d5e`: Hatch writes bee-themed .feature files into the correct subfolders
- [~] `@id:3c4d5e6f`: Hatch emits a terminal summary of files written — test tests return value, not terminal output (Finding 4)
- [x] `@id:4d5e6f7a`: pytest exits immediately after hatch without running tests
- [~] `@id:5e6f7a8b`: Hatch fails when the features directory already contains .feature files — INTERNALERROR crash + wrong abstraction level (Findings 1, 3)
- [x] `@id:6f7a8b9c`: Hatch overwrites existing content when --beehave-hatch-force is passed
- [x] `@id:7a8b9c0d`: Generated content includes an untagged Example to trigger auto-ID generation
- [x] `@id:8b9c0d1e`: Generated content includes a @deprecated-tagged Example
- [x] `@id:9c0d1e2f`: Generated content includes a multilingual feature file
- [x] `@id:0d1e2f3a`: Generated content includes a feature with a Background block
- [x] `@id:1e2f3a4b`: Generated content includes a Scenario Outline with an Examples table
- [x] `@id:a1f2e3d4`: Generated content includes a step with an attached data table
- [x] `@id:b2e3d4c5`: Generated content includes a feature placed in the completed subfolder
- [x] `@id:c3d4e5f6`: Hatch writes to the custom path when features_path is configured
- [x] `@id:d4e5f6a7`: Hatch produces a different Feature name on successive runs
- [x] `@id:e5f6a7b8`: Hatch completes without requiring any additional package installation

## Step 4 Rejection Fixes Required

1. `pytest_beehave/plugin.py:158` — catch SystemExit from run_hatch() and call pytest.exit(str(e), returncode=1) instead of letting it propagate as INTERNALERROR
2. `tests/unit/plugin_test.py` — mock_config.getoption() returns truthy MagicMock, triggering hatch branch and calling pytest.exit(), silently preventing 3 tests from running; fix by mocking getoption to return False for --beehave-hatch
3. `tests/features/example_hatch/overwrite_protection_test.py:test_example_hatch_5e6f7a8b` — rewrite to use pytest.main() and assert non-zero exit + error names conflicting path
4. `tests/features/example_hatch/hatch_invocation_test.py:test_example_hatch_3c4d5e6f` — rewrite to use pytest.main() with output capture and assert [beehave] HATCH <path> appears in output

## Notes
- lint: PASS
- static-check: PASS
- test-fast: PASS (95 passed, 4 skipped)
- test-coverage: FAIL at 95% — 44 lines missing in 5 pre-existing modules (pre-existing defect, not caused by this feature)
- hatch.py and plugin.py (new code): 100% covered

## Next
Run @software-engineer — apply the 4 fixes listed in Step 4 Rejection Fixes Required, re-run quality gate, update Self-Declaration, then signal Step 4 again
