# Current Work

Feature: deprecation-sync
Step: 3 (TDD Loop — all @id tests green)
Source: docs/features/in-progress/deprecation-sync.feature

## Cycle State
Test: all @id complete
Phase: REFACTOR (complete)

## Self-Declaration
As a software-engineer I declare:
* YAGNI: no code without a failing test — AGREE | all sync functions driven by @id tests in tests/features/deprecation_sync/
* YAGNI: no speculative abstractions — AGREE | toggle_deprecated_marker:stub_writer.py:621 is directly called by sync_engine with no unused paths
* KISS: simplest solution that passes — AGREE | toggle_deprecated_marker reads existing decorators and rewrites them; no AST library needed
* KISS: no premature optimization — AGREE | no caching or lazy evaluation
* DRY: no duplication — AGREE | _apply_deprecated_toggle:stub_writer.py:592 used for both add and remove paths; _sync_top_level_stubs now calls _sync_deprecated_top_level instead of duplicating the loop
* DRY: no redundant comments — AGREE | only docstrings; no inline comments in deprecation sync functions
* SOLID-S: one reason to change per class — AGREE | ParsedExample:feature_parser.py:62 changes only if example model changes; toggle_deprecated_marker:stub_writer.py:621 changes only if deprecated marker format changes
* SOLID-O: open for extension, closed for modification — AGREE | FileSystemProtocol:sync_engine.py:38 allows new filesystem without modifying sync logic
* SOLID-L: subtypes substitutable — AGREE | _RealFileSystem satisfies FileSystemProtocol fully
* SOLID-I: no forced unused deps — AGREE | FileSystemProtocol has 2 methods, both used
* SOLID-D: depend on abstractions, not concretions — AGREE | sync_engine depends on FileSystemProtocol; no concrete I/O in domain
* OC-1: one level of indentation per method — AGREE | _sync_deprecated_in_rule:sync_engine.py:409 uses list comprehension (no nested for/if); _apply_deprecated_toggle:stub_writer.py:592 uses guard clauses; _sync_deprecated_rules:sync_engine.py added to avoid if+for nesting in _sync_completed_feature
* OC-2: no else after return — AGREE | toggle_deprecated_marker:stub_writer.py:621 uses early return, no else
* OC-3: primitive types wrapped — AGREE | ExampleId, FeatureSlug, RuleSlug wrap str primitives
* OC-4: first-class collections — AGREE | tuple[ParsedExample, ...] used as domain value
* OC-5: one dot per line — DISAGREE | sys.stdout.write (plugin.py:45), sys.stderr.write (plugin.py:58), self._impl.parse (feature_parser.py:41), step.doc_string.splitlines() (stub_writer.py:101) remain — all are stdlib/adapter boundary chaining, idiomatic Python
* OC-6: no abbreviations — AGREE | no mgr/tmp/cfg/val/usr abbreviations
* OC-7: ≤20 lines per function, ≤50 per class — AGREE | longest: toggle_deprecated_marker:stub_writer.py:621 ~18 logic lines
* OC-8: ≤2 instance variables per class — DISAGREE | ParsedFeature (5 fields), ParsedExample (5 fields), ExistingStub (7 fields) — domain value objects require all fields by domain necessity; splitting violates KISS
* OC-9: no getters/setters — AGREE | no get_/set_ methods; dataclasses with direct access
* Patterns: no creational smell — AGREE | _RealFileSystem instantiated once in run_sync:sync_engine.py
* Patterns: no structural smell — AGREE | no isinstance chains; FeatureStage enum used for dispatch
* Patterns: no behavioral smell — AGREE | SyncAction returned and aggregated; no scattered state
* Semantic: tests operate at same abstraction as AC — AGREE | tests call run_sync/toggle_deprecated_marker directly matching AC verbs "When pytest is invoked"

## Progress
- [x] `@id:f9b636df`: Deprecated Example in a backlog feature gets the deprecated marker
- [x] `@id:fc372f15`: Deprecated Example in a completed feature gets the deprecated marker
- [x] `@id:b3d7f942`: @deprecated on a Rule block propagates to all child Examples
- [x] `@id:a9e1c504`: @deprecated on the Feature node propagates to all Examples in the feature
- [x] `@id:d6f8b231`: Removing @deprecated from a Rule removes the marker from all child stubs
- [x] `@id:7fcee92a`: Deprecated marker is removed when @deprecated tag is removed

## Next
Run @reviewer — verify feature deprecation-sync at Step 4 (all 6 tests green, 100% coverage, 0 type errors)
