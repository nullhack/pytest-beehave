<div align="center">
  <img src="docs/images/banner.svg" alt="Beehave" width="860"/>

  <br><br>

  <p><strong>Bridge the gap between living docs and runnable tests. Beehave does it — every time you run pytest.</strong></p>

  [![Contributors][contributors-shield]][contributors-url]
  [![Forks][forks-shield]][forks-url]
  [![Stargazers][stars-shield]][stars-url]
  [![Issues][issues-shield]][issues-url]
  [![MIT License][license-shield]][license-url]
  [![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen?style=for-the-badge)](https://nullhack.github.io/pytest-beehave/coverage/)
  [![CI](https://img.shields.io/github/actions/workflow/status/nullhack/pytest-beehave/ci.yml?style=for-the-badge&label=CI)](https://github.com/nullhack/pytest-beehave/actions/workflows/ci.yml)
  [![Python](https://img.shields.io/badge/python-3.13-blue?style=for-the-badge)](https://www.python.org/downloads/)
</div>

---

## The problem

You write a Gherkin acceptance criterion. Then you write a test stub. Then you rename the feature. Now you have a stale stub, a broken docstring, and an orphaned test — and you only find out three sprints later.

Living documentation is supposed to keep specs and code in sync. In practice, the sync is always manual — and always falls behind.

**Beehave closes that gap.**

It is a pytest plugin that keeps your test suite in perfect sync with your `.feature` files — automatically, every time you invoke `pytest`. No scripts to remember. No CI step to add. No drift.

---

## Features

| Capability | Detail |
|---|---|
| **Auto stub generation** | New `@id`-tagged `Example:` → typed, skipped test stub written before collection runs |
| **Docstring sync** | Steps change in your `.feature`? Docstrings update. Test bodies are never touched. |
| **Auto ID assignment** | Missing `@id` on an `Example:`? Beehave generates one and writes it back in-place |
| **CI enforcement** | Read-only filesystem (CI)? Beehave fails loudly and names every untagged Example |
| **Orphan detection** | `@id` disappears from the feature file? The test is marked `skip(reason="orphan")` — not deleted, not silently run |
| **Non-conforming redirect** | Test in the wrong file or class? Beehave creates the canonical stub and marks the original as moved |
| **Deprecation sync** | `@deprecated` tag on an `Example:`, `Rule:`, or `Feature:`? The pytest marker propagates automatically |
| **Zero config** | Works out of the box. Optionally configure `features_path` in `pyproject.toml` |

---

## Installation

```bash
pip install pytest-beehave
```

The plugin registers itself via pytest's entry point system — no `conftest.py` changes needed.

---

## Quick start

**1. Write a feature file:**

```gherkin
# docs/features/backlog/checkout.feature
Feature: Checkout

  Rule: Tax calculation
    As a buyer
    I want the correct tax applied to my order
    So that I pay the right amount

    Example: VAT is applied at the correct rate
      Given a cart with items totalling £100
      When the buyer is in the UK
      Then the order total is £120
```

**2. Run pytest:**

```bash
pytest
```

**3. Beehave generates this before any test is collected:**

```python
# tests/features/checkout/tax-calculation_test.py

class TestTaxCalculation:
    @pytest.mark.skip(reason="not yet implemented")
    def test_checkout_a3f2b1c4(self) -> None:
        """
        Given: a cart with items totalling £100
        When: the buyer is in the UK
        Then: the order total is £120
        """
        raise NotImplementedError
```

The `@id` tag is also written back to your `.feature` file automatically.

**4. Implement the test body and ship.**

---

## How it works

Beehave hooks into `pytest_configure` — the earliest possible hook — so stubs exist before collection begins. The same `pytest` invocation that generates a stub also discovers and runs it.

```
pytest invoked
    └─ pytest_configure fires
         └─ Beehave reads docs/features/backlog/ + in-progress/
              ├─ assigns missing @id tags (or fails in CI)
              ├─ creates missing test stubs
              ├─ updates outdated docstrings
              ├─ marks orphans and non-conforming stubs
              └─ syncs @deprecated markers across all stages
    └─ Collection begins (stubs are already on disk)
    └─ Tests run
```

---

## Configuration

```toml
# pyproject.toml
[tool.beehave]
features_path = "docs/features"   # default — omit if this is your layout
```

If `features_path` is set but the directory does not exist, Beehave exits with a clear error message naming the missing path.

---

## Test file layout

```
tests/
  features/
    <feature-name>/
      <rule-slug>_test.py       ← one file per Rule: block
      examples_test.py          ← when the feature has no Rule: blocks
      conftest.py               ← autouse fixture from feature-level Background
```

Test function names encode the acceptance criterion ID:

```
test_<feature_slug>_<8char_hex>
```

Every test is traceable back to its exact `Example:` block by ID — not by fragile name matching.

---

## Marker semantics

Beehave manages four skip-based markers. User-owned markers (`slow`, `unit`, `integration`) are never touched.

| Marker | Set by | Meaning |
|---|---|---|
| `skip(reason="not yet implemented")` | Beehave | Stub exists, test body not written yet |
| `skip(reason="orphan: ...")` | Beehave | `@id` no longer in any `.feature` file |
| `skip(reason="non-conforming: moved to ...")` | Beehave | `@id` found but test is in the wrong location |
| `deprecated` | Beehave | Mirrors `@deprecated` Gherkin tag |
| `slow` | You | Opt-in for Hypothesis / long-running tests |

---

## Compatibility

| Requirement | Version |
|---|---|
| Python | ≥ 3.13 |
| pytest | ≥ 6.0 |

---

## Contributing

```bash
git clone https://github.com/nullhack/pytest-beehave
cd pytest-beehave
uv sync --all-extras
uv run task test && uv run task lint && uv run task static-check
```

Bug reports and pull requests are welcome on [GitHub](https://github.com/nullhack/pytest-beehave/issues).

---

## License

MIT — see [LICENSE](LICENSE).

**Author:** eol ([@nullhack](https://github.com/nullhack)) · [Documentation](https://nullhack.github.io/pytest-beehave)

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/nullhack/pytest-beehave.svg?style=for-the-badge
[contributors-url]: https://github.com/nullhack/pytest-beehave/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/nullhack/pytest-beehave.svg?style=for-the-badge
[forks-url]: https://github.com/nullhack/pytest-beehave/network/members
[stars-shield]: https://img.shields.io/github/stars/nullhack/pytest-beehave.svg?style=for-the-badge
[stars-url]: https://github.com/nullhack/pytest-beehave/stargazers
[issues-shield]: https://img.shields.io/github/issues/nullhack/pytest-beehave.svg?style=for-the-badge
[issues-url]: https://github.com/nullhack/pytest-beehave/issues
[license-shield]: https://img.shields.io/badge/license-MIT-green?style=for-the-badge
[license-url]: https://github.com/nullhack/pytest-beehave/blob/main/LICENSE
