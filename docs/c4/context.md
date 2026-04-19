# C4 Level 1 — System Context: pytest-beehave

```mermaid
C4Context
    title System Context — pytest-beehave

    Person(developer, "Developer", "Python developer using the Beehave workflow to write BDD-style acceptance tests")
    Person(ci, "CI Pipeline", "Automated environment (GitHub Actions, etc.) that runs pytest on every push")

    System(beehave, "pytest-beehave", "pytest plugin that syncs test stubs from Gherkin feature files before collection, assigns IDs, manages markers, and surfaces acceptance criteria in reports")

    System_Ext(pytest, "pytest", "Python test framework that discovers, runs, and reports on tests; provides the plugin hook lifecycle")
    System_Ext(gherkin, "gherkin-official", "Gherkin parser that reads .feature files and produces an AST; supports 70+ human languages")
    System_Ext(pytest_html, "pytest-html", "Optional pytest plugin that generates an HTML test report; beehave adds an Acceptance Criteria column when installed")

    Rel(developer, pytest, "Runs", "uv run pytest / uv run task test")
    Rel(ci, pytest, "Runs", "uv run pytest (read-only environment)")
    Rel(pytest, beehave, "Loads via pytest11 entry point", "pytest_configure hook")
    Rel(beehave, gherkin, "Parses .feature files via", "gherkin-official Python API")
    Rel(beehave, pytest_html, "Injects Acceptance Criteria column into", "pytest-html report hooks (optional)")
    Rel(beehave, developer, "Writes test stubs and @id tags to", "tests/features/ and docs/features/")
    Rel(beehave, ci, "Fails run with descriptive error when @id tags are missing in", "read-only CI environment")
```

## Notes

- **Developer** interacts with beehave indirectly: they write `.feature` files and run pytest; beehave auto-generates and maintains test stubs.
- **CI Pipeline** is a read-only environment: beehave detects this and fails fast (with a clear error) instead of writing `@id` tags back.
- **gherkin-official** handles all language parsing, including non-English feature files (`# language: es`, `# language: zh-CN`, etc.). beehave delegates fully.
- **pytest-html** is an optional install extra (`pip install pytest-beehave[html]`); its absence is silently ignored.
