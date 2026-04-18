# Discovery: multilingual-feature-parsing

## State
Status: BASELINED (2026-04-18)

## Entities
| Type | Name | Candidate Class/Method | In Scope |
|------|------|----------------------|----------|
| Noun | `.feature` file | Gherkin feature file on disk | Yes |
| Noun | `# language: xx` comment | Language directive at top of feature file | Yes |
| Noun | non-English keyword | Gherkin keyword in a supported dialect (e.g. `Fonctionnalité:`, `Dado:`, `功能:`) | Yes |
| Noun | feature slug | Underscored folder name used in Python function/class names | Yes |
| Noun | rule slug | Slugified `Rule:` title used in test file names | Yes |
| Noun | docstring | Step-by-step docstring in generated test stub | Yes |
| Noun | function name | `test_<feature_slug>_<8hex>` — always derived from folder name, never from Gherkin keywords | Yes |
| Noun | class name | `class Test<RuleSlug>` — always derived from folder name, never from Gherkin keywords | Yes |
| Verb | parse feature | `parse_feature(path)` — delegates to `gherkin-official` | Yes |
| Verb | detect language | `gherkin-official` `TokenMatcher` auto-detects `# language: xx` mid-parse | Yes |
| Verb | preserve keyword | Docstring uses the keyword exactly as it appears in the `.feature` file | Yes |
| Noun | pyproject.toml language config | Project-level default language setting | **No** |
| Noun | bad language code error handling | Custom error for unrecognised `# language:` values | **No** |

## Rules (Business)
- `pytest-beehave` is transparent to language: the `# language: xx` comment is the sole mechanism for non-English parsing; no beehave configuration is required or supported.
- `gherkin-official` auto-detects the `# language: xx` comment and switches keyword matching accordingly; `pytest-beehave` does not need to pass a language parameter.
- Function names (`test_<feature_slug>_<8hex>`) and class names (`class Test<RuleSlug>`) are derived from the **feature folder name** (a filesystem path), never from Gherkin keywords — they are always valid Python identifiers regardless of the `.feature` file language.
- Docstrings in generated stubs preserve the original keyword exactly as it appears in the `.feature` file (e.g., `Dado:`, `当:`, `Given:`).
- A project may contain `.feature` files in different languages; each file is parsed independently and transparently.

## Constraints
- No `pyproject.toml` language configuration — out of scope.
- No custom error handling for unrecognised language codes — out of scope; let `gherkin-official` raise its own exception.
- No keyword normalisation to English in docstrings — preserve original.
- No changes to `feature_parser.py` implementation are expected; this feature is about adding tests that prove existing behaviour.

## Questions
| ID | Question | Answer | Status |
|----|----------|--------|--------|
| Q1 | Should beehave support a project-level default language in pyproject.toml? | No — transparent; `# language: xx` comment is the only mechanism | ANSWERED |
| Q2 | Which languages need verification? | Spanish (`es`) and Chinese Simplified (`zh-CN`) — small focused tests, do not overdo | ANSWERED |
| Q3 | Should beehave add custom error handling for bad language codes? | No — out of scope; let gherkin-official raise | ANSWERED |
| Q4 | Should mixed-language projects (Spanish + English) work transparently? | Yes — each file parsed independently | ANSWERED |
| Q5 | Should docstrings normalise non-English keywords to English? | No — preserve original keyword as-is | ANSWERED |
| Q6 | Scope of this feature? | Tests only — verify existing behaviour works; no implementation changes expected | ANSWERED |

All questions answered. Discovery frozen.
