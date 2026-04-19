# Architecture: pytest-beehave

---

## 2026-04-18 — stub-creation: test file writing library

Decision: Use libcst for all test file writes.
Reason: Preserves formatting, comments, and existing function bodies; avoids string-template fragility.
Alternatives considered: `ast` module (cannot round-trip source with formatting preserved), string templates (fragile).
Feature: stub-creation

---

## 2026-04-18 — stub-creation: stub body

Decision: New stubs contain only `raise NotImplementedError` — no `# Given`, `# When`, `# Then` section comments.
Reason: Section comments are redundant given the docstring.
Alternatives considered: Adding section comments — rejected per AC Q1.
Feature: stub-creation

---

## 2026-04-18 — stub-creation: slug conventions

Decision: `FeatureSlug` replaces hyphens with underscores (for Python identifiers); `RuleSlug` uses underscores (for file names and Python identifiers).
Reason: Python function names cannot contain hyphens; file names can.
Alternatives considered: Both using underscores — rejected because file names with underscores diverge from the naming spec.
Feature: stub-creation

---

## 2026-04-18 — stub-creation: completed/ features excluded from stub sync

Decision: Stub creation is never invoked for features in `FeatureStage.COMPLETED`.
Reason: Matches AC `@id:38d864b9` and state machine.
Alternatives considered: Allowing stub creation for completed features — rejected per spec.
Feature: stub-creation

---

## 2026-04-18 — stub-updates: non-conforming handling creates conforming stub first

Decision: When a non-conforming stub is found, `sync_engine` first creates the conforming stub, then marks the original with `@pytest.mark.skip(reason="non-conforming: moved to <file>")`.
Reason: Ensures traceability is never lost — the conforming stub exists before the original is marked.
Alternatives considered: Delete the non-conforming stub — rejected because it loses the developer's implementation.
Feature: stub-updates

---

## 2026-04-18 — stub-updates: stub_reader uses libcst

Decision: `read_stubs_from_file` uses `libcst` to parse the test file and extract function names, decorators, and docstrings.
Reason: Consistent with stub_writer's use of libcst; avoids dual-library complexity.
Alternatives considered: `ast` module — rejected because it cannot extract decorator arguments reliably without round-trip capability.
Feature: stub-updates

---

## 2026-04-18 — stub-updates: stub-sync never touches @pytest.mark.slow

Decision: All stub_writer functions check the marker name before modifying; `slow` is never added or removed.
Reason: Matches marker ownership rules in discovery.md and AC `@id:c9a30d52`.
Alternatives considered: Allowing stub-sync to manage all markers — rejected per spec.
Feature: stub-updates

---

## 2026-04-18 — Cross-feature: remove class-based test structure

Decision: All test stubs are top-level functions. No `class Test<RuleSlug>` wrapping.
Reason: Class wrapping added indirection with no benefit; final implementation uses top-level functions throughout.
Alternatives considered: Keeping class-based layout for Rule blocks — rejected because it increases nesting without providing value.
Affected features: stub-creation, stub-updates
