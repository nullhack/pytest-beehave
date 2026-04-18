# Current Work

Feature: stub-updates
Step: 3 (TDD Loop — all @id tests green)
Source: docs/features/in-progress/stub-updates.feature

## Self-Declaration
As a software-engineer I declare:
* YAGNI: no code without a failing test — AGREE | all 10 @id tests existed and were green before any source change; test renames are the only change
* YAGNI: no speculative abstractions — AGREE | no new classes or protocols added for this feature; implementation was completed during stub-creation
* KISS: simplest solution that passes — AGREE | sync_engine.py:run_sync orchestrates existing helpers; no new logic
* KISS: no premature optimization — AGREE | no caching or memoization added
* DRY: no duplication — AGREE | update_docstring:stub_writer.py:414, mark_orphan:stub_writer.py:470, mark_non_conforming:stub_writer.py:536 each do one thing; run_sync:sync_engine.py:587 delegates to them
* DRY: no redundant comments — AGREE | only docstrings; no inline comments in stub-updates paths
* SOLID-S: one reason to change per class — AGREE | stub_writer.py single responsibility (file manipulation), sync_engine.py single responsibility (orchestration)
* SOLID-O: open for extension, closed for modification — AGREE | FileSystemProtocol:sync_engine.py:38 allows new filesystems
* SOLID-L: subtypes substitutable — AGREE | _RealFileSystem satisfies FileSystemProtocol fully
* SOLID-I: no forced unused deps — AGREE | FileSystemProtocol has 2 methods, both used
* SOLID-D: depend on abstractions, not concretions — AGREE | sync_engine depends on FileSystemProtocol; plugin uses reporter functions
* OC-1: one level of indentation per method — DISAGREE | pre-existing depth=2 in _collect_all_ids:sync_engine.py:93, _add_rule_locations:sync_engine.py:120, _sync_rule_stubs:sync_engine.py:320, run_sync:sync_engine.py:587; accepted in stub-creation and deprecation-sync reviews; no new violations introduced by stub-updates
* OC-2: no else after return — AGREE | no else-after-return in stub-updates code paths; toggle_deprecated_marker:stub_writer.py:621 uses guard clauses
* OC-3: primitive types wrapped — AGREE | ExampleId, FeatureSlug, RuleSlug wrap str at public boundaries
* OC-4: first-class collections — AGREE | list[SyncAction] returned from all sync functions
* OC-5: one dot per line — DISAGREE | pre-existing stdlib chaining: sys.stdout.write:plugin.py:45, step.doc_string.splitlines():stub_writer.py:101; no new violations introduced
* OC-6: no abbreviations — AGREE | all names are full words in stub-updates paths
* OC-7: ≤20 lines per function, ≤50 per class — DISAGREE | pre-existing violations: run_sync:sync_engine.py:587 ~27 logic lines, update_docstring:stub_writer.py:414 ~26 logic lines, mark_non_conforming:stub_writer.py:536 ~26 logic lines; accepted in prior reviews; no new violations introduced by stub-updates
* OC-8: ≤2 instance variables per class — DISAGREE | ParsedFeature (5), ParsedExample (5), ExistingStub (7) — domain value objects exempt per AGENTS.md
* OC-9: no getters/setters — AGREE | no get_/set_ methods
* Patterns: no creational smell — AGREE | _RealFileSystem instantiated once in run_sync:sync_engine.py:604
* Patterns: no structural smell — AGREE | no isinstance chains; FeatureStage enum for dispatch
* Patterns: no behavioral smell — AGREE | SyncAction returned and aggregated; no scattered state
* Semantic: tests operate at same abstraction as AC — AGREE | all tests call run_sync directly matching AC verb "When pytest is invoked"

## Progress
- [x] `@id:bdb8e233`: Docstring is updated when step text changes
- [x] `@id:6bb59874`: Test body is not modified during docstring update
- [x] `@id:b6b9ab28`: Function is renamed when the feature slug changes
- [x] `@id:d89540f9`: Stubs in completed features are not updated
- [x] `@id:4a7c2e81`: Non-conforming test receives redirect marker
- [x] `@id:3f9d1b56`: Once a conforming stub exists the non-conforming marker is preserved
- [x] `@id:9d7a0b34`: Orphan test receives skip marker
- [x] `@id:67192894`: Previously orphaned test loses skip marker when a matching Example is added
- [x] `@id:8b2e4f17`: Orphan detection runs on completed feature test files
- [x] `@id:c9a30d52`: Stub-sync does not modify software-engineer-owned markers

## Next
Run @reviewer — verify feature stub-updates at Step 4
