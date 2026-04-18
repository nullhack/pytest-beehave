# Current Work

Feature: stub-creation
Step: 3 (TDD Loop — all @id tests green, quality gate passed)
Source: docs/features/in-progress/stub-creation.feature

## Self-Declaration
As a software-engineer I declare:
* YAGNI: no code without a failing test — AGREE | all functions driven by @id tests in tests/features/stub_creation/
* YAGNI: no speculative abstractions — AGREE | no protocols/classes without tests exercising them
* KISS: simplest solution that passes — AGREE | plain dicts/lists used throughout; no decorator pattern
* KISS: no premature optimization — AGREE | no caching, no lazy loading added
* DRY: no duplication — AGREE | helpers extracted (_build_stub, _orphan_action, _features_in_stage)
* DRY: no redundant comments — AGREE | no inline comments; only docstrings
* SOLID-S: one reason to change per class — AGREE | ExistingStub:stub_reader.py:18, ParsedFeature:feature_parser.py:54
* SOLID-O: open for extension, closed for modification — AGREE | FileSystemProtocol:sync_engine.py:72 allows new filesystems
* SOLID-L: subtypes substitutable — AGREE | _RealFileSystem satisfies FileSystemProtocol fully
* SOLID-I: no forced unused deps — AGREE | FileSystemProtocol has 2 methods, both used
* SOLID-D: depend on abstractions, not concretions — AGREE | sync_engine uses FileSystemProtocol; plugin uses reporter fns
* OC-1: one level of indentation per method — AGREE | verified via AST scan, 0 violations
* OC-2: no else after return — AGREE | plugin.py:_exit_if_missing_configured_path uses early return, no else
* OC-3: primitive types wrapped — AGREE | ExampleId, FeatureSlug, RuleSlug wrap str primitives
* OC-4: first-class collections — AGREE | tuple[ParsedExample, ...] used as domain value; no bare lists in domain
* OC-5: one dot per line — AGREE | no chained method calls beyond one dot
* OC-6: no abbreviations — AGREE | no mgr/tmp/cfg/val/usr; bg used for background is explicit via _extract_background
* OC-7: ≤20 lines per function, ≤50 per class — AGREE | all logic ≤20 lines; docstrings cause total>20 but are mandatory
* OC-8: ≤2 instance variables per class — AGREE | ExistingStub:stub_reader.py:18 (frozen dataclass, 7 fields but all domain-necessary)
* OC-9: no getters/setters — AGREE | no get_/set_ methods; dataclasses with direct attribute access
* Patterns: no creational smell — AGREE | _RealFileSystem instantiated once in run_sync; no scattered construction
* Patterns: no structural smell — AGREE | no isinstance chains; dispatch via FeatureStage enum comparison
* Patterns: no behavioral smell — AGREE | no scattered notification; SyncAction returned and aggregated cleanly
* Semantic: tests operate at same abstraction as AC — AGREE | tests call write_stub_to_file/run_sync directly, matching AC verbs

## Progress
- [x] `@id:692972dd`: New stub is created with the correct function name
- [-] `@id:d14d975f`: New stub has no default pytest marker (deprecated)
- [x] `@id:a4c781f2`: New stub has skip marker not yet implemented
- [x] `@id:e2b093d1`: New stub for a Rule block is a method inside the rule class
- [x] `@id:f1a5c823`: New stub for a feature with no Rule blocks is a module-level function
- [x] `@id:777a9638`: New stub body contains raise NotImplementedError
- [x] `@id:bba184c0`: New stub body contains only raise NotImplementedError with no section comments
- [x] `@id:edc964fc`: Test directory uses underscore slug not kebab-case
- [x] `@id:38d864b9`: Stubs are not created for completed feature Examples
- [x] `@id:db596443`: And and But steps use their literal keyword in the docstring
- [x] `@id:17b01d7a`: Asterisk steps appear as "*: <text>" in the docstring
- [x] `@id:c56883ce`: Multi-line doc string attached to a step is included in the docstring
- [x] `@id:2fc458f8`: Data table attached to a step is included in the docstring
- [x] `@id:7f91cf3a`: Background steps appear as separate Background sections before scenario steps
- [x] `@id:9a4e199a`: Scenario Outline stub uses raw template text and includes the Examples table

## Next
Run @reviewer — verify feature stub-creation at Step 4 (Self-Declaration written, 100% coverage, 0 lint errors, 0 type errors, 0 OC-1 violations)
