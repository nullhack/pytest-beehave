# Current Work

Feature: stub-creation
Step: 3 (TDD Loop — all @id tests green)
Source: docs/features/in-progress/stub-creation.feature

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
Run @reviewer — verify feature stub-creation at Step 4 (all tests green, 100% coverage, 0 type errors)
