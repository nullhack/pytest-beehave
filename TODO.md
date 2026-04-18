# Current Work

Feature: stub-creation
Step: 2 (ARCH)
Source: docs/features/in-progress/stub-creation/stub-creation.feature

## Progress
- [ ] `@id:692972dd`: New stub is created with the correct function name
- [-] `@id:d14d975f`: New stub has no default pytest marker (deprecated)
- [ ] `@id:a4c781f2`: New stub has skip marker not yet implemented
- [ ] `@id:e2b093d1`: New stub for a Rule block is a method inside the rule class
- [ ] `@id:f1a5c823`: New stub for a feature with no Rule blocks is a module-level function
- [ ] `@id:777a9638`: New stub body contains raise NotImplementedError
- [ ] `@id:bba184c0`: New stub body contains only raise NotImplementedError with no section comments
- [ ] `@id:edc964fc`: Test directory uses underscore slug not kebab-case
- [ ] `@id:38d864b9`: Stubs are not created for completed feature Examples
- [ ] `@id:db596443`: And and But steps use their literal keyword in the docstring
- [ ] `@id:17b01d7a`: Asterisk steps appear as "*: <text>" in the docstring
- [ ] `@id:c56883ce`: Multi-line doc string attached to a step is included in the docstring
- [ ] `@id:2fc458f8`: Data table attached to a step is included in the docstring
- [ ] `@id:7f91cf3a`: Background steps appear as separate Background sections before scenario steps
- [ ] `@id:9a4e199a`: Scenario Outline stub uses raw template text and includes the Examples table

## Next
Run @reviewer — verify that all tests are now class-based and pass, then continue with stub-creation implementation
