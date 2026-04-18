# Current Work

Feature: stub-updates
Step: 3 (TDD Loop — all @id tests green)
Source: docs/features/in-progress/stub-updates.feature

## Self-Declaration
As a software-engineer I declare:
* YAGNI: no code without a failing test — AGREE | _FUNC_RE fix driven by @id:3f9d1b56 test assertion (assert correct_content == conforming_content); _extract_class_name and _CLASS_RE driven by test_read_stubs_from_file_reads_class_method_stubs unit test
* YAGNI: no speculative abstractions — AGREE | _extract_class_name:stub_reader.py:227 used only in _build_stub; _CLASS_RE used only in _extract_class_name
* KISS: simplest solution that passes — AGREE | _FUNC_RE extended with optional 4-space indent group; _extract_class_name finds last class match before func_start
* KISS: no premature optimization — AGREE | no caching or memoization added
* DRY: no duplication — AGREE | _extract_class_name shared by all _build_stub calls; update_docstring:stub_writer.py:414, mark_orphan:stub_writer.py:476, mark_non_conforming:stub_writer.py:536 each do one thing
* DRY: no redundant comments — AGREE | only docstrings; no inline comments in stub-updates paths
* SOLID-S: one reason to change per class — AGREE | stub_reader.py changes only if regex for stubs changes; stub_writer.py changes only if file manipulation changes
* SOLID-O: open for extension, closed for modification — AGREE | FileSystemProtocol:sync_engine.py:38 allows new filesystems
* SOLID-L: subtypes substitutable — AGREE | _RealFileSystem satisfies FileSystemProtocol fully
* SOLID-I: no forced unused deps — AGREE | FileSystemProtocol has 2 methods, both used
* SOLID-D: depend on abstractions, not concretions — AGREE | sync_engine depends on FileSystemProtocol; plugin uses reporter functions
* OC-1: one level of indentation per method — DISAGREE | pre-existing depth=2 in _collect_all_ids:sync_engine.py:93, _add_rule_locations:sync_engine.py:120, _sync_rule_stubs:sync_engine.py:320, run_sync:sync_engine.py:587; accepted in stub-creation/deprecation-sync; new functions _extract_class_name:stub_reader.py:227 depth=1 only
* OC-2: no else after return — AGREE | _extract_class_name:stub_reader.py:238 uses guard returns; no else-after-return
* OC-3: primitive types wrapped — AGREE | ExampleId, FeatureSlug, RuleSlug wrap str at public boundaries
* OC-4: first-class collections — AGREE | list[SyncAction] returned from sync functions; list[ExistingStub] returned from read_stubs_from_file
* OC-5: one dot per line — DISAGREE | pre-existing stdlib chaining: sys.stdout.write:plugin.py:45, step.doc_string.splitlines():stub_writer.py:101; new: class_matches[-1].group(1):stub_reader.py:244 — idiomatic Python list access + method call
* OC-6: no abbreviations — AGREE | all names are full words; func_start, func_name, indent are clear nouns
* OC-7: ≤20 lines per function, ≤50 per class — DISAGREE | pre-existing: run_sync ~27 logic lines, update_docstring ~26, mark_non_conforming ~26; new functions: _extract_class_name = 6 logic lines, _build_stub = 9 logic lines (both ≤20)
* OC-8: ≤2 instance variables per class — DISAGREE | ParsedFeature (5), ParsedExample (5), ExistingStub (7) — domain value objects exempt per AGENTS.md
* OC-9: no getters/setters — AGREE | no get_/set_ methods
* Patterns: no creational smell — AGREE | _RealFileSystem instantiated once in run_sync:sync_engine.py:604
* Patterns: no structural smell — AGREE | no isinstance chains; FeatureStage enum for dispatch
* Patterns: no behavioral smell — AGREE | SyncAction returned and aggregated; no scattered state
* Semantic: tests operate at same abstraction as AC — AGREE | @id:3f9d1b56 now asserts correct_content == conforming_content (byte-for-byte unchanged); all tests call run_sync directly

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
