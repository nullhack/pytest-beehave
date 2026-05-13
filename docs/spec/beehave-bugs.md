# beehave v0.3.1 Bug Report

Discovered during pytest-beehave end-to-end integration testing.

---

## Bug 1: Background steps excluded from ScenarioInfo.steps

**Severity**: High — causes incomplete step display in downstream tools

**File**: `beehave/gherkin.py:180,195`

**Symptom**: `ScenarioInfo.steps` only contains scenario-level steps. Feature-level and rule-level background steps are missing.

**Root cause**: In `_build_scenario()`, line 180 builds the scenario's own steps:
```python
steps = [_parse_step(s) for s in sc.get("steps", [])]
```

Line 181 correctly computes the merged list (background + scenario):
```python
merged = feature_bg + rule_bg + steps
```

But line 195 stores only the scenario steps, not the merged list:
```python
steps=tuple(steps),           # ← should be tuple(merged)
```

The `merged` list IS used for `placeholders` (line 196) and `literals` (line 197-198), so those fields are correct. Only `steps` is wrong.

**Evidence** (from e2e test):
```
Feature: Shopping cart
  Background:
    Given a user exists
    And the user has an empty cart
  Scenario: Add single item
    When the user adds "Widget" to the cart
    Then the cart contains 1 item
```

`test_Add_single_item` reports 2 steps (When, Then) instead of 4 (2 background + 2 scenario).

**Fix**: Change `gherkin.py:195` from `steps=tuple(steps)` to `steps=tuple(merged)`.

---

## Bug 2: check_all only scans top-level features directory

**Severity**: High — produces false-positive `unmapped-test` violations for all features in subdirectories

**File**: `beehave/check.py:233`

**Symptom**: `check_all()` reports every test function from a subdirectory feature as `"unmapped-test"` with message `"'test_X' has no matching scenario"`, even when the scenario and test are correctly linked.

**Root cause**: Line 233 uses `glob()` instead of `rglob()`:
```python
for feature_file in sorted(features_dir.glob("*.feature")):
```

`glob("*.feature")` only finds `.feature` files in the top-level `features_dir`. Any features organized in subdirectories (e.g., `docs/features/cart/shopping_cart.feature`, `docs/features/login/user_login.feature`) are never parsed, so their scenarios never enter `all_scenarios`. When the test discovery phase finds the corresponding test functions, they have no match → false-positive `unmapped-test` violations.

**Note**: `pytest-beehave` uses `rglob("*.feature")` in its own `_collect_scenarios_and_generate()` and correctly finds all features. Only `check_all` has this bug.

**Evidence** (from e2e test):
```
docs/features/
  smoke.feature                          ← found by glob
  cart/shopping_cart.feature             ← NOT found by glob
  login/user_login.feature              ← NOT found by glob
```

Result: 9 false-positive `unmapped-test` violations for all tests derived from subdirectory features. `test_Everything_is_fine` (top-level) is the only one correctly matched.

**Fix**: Change `check.py:233` from `features_dir.glob("*.feature")` to `features_dir.rglob("*.feature")`.

---

## Bug 3: generate_stubs creates directories without __init__.py

**Severity**: Medium — causes pytest collection failure when multiple features produce same-named test files

**File**: `beehave/generate.py:175`

**Symptom**: When multiple `.feature` files have no `Rule:` blocks, beehave generates `default_test.py` in different directories. Without `__init__.py`, pytest treats them as the same module name and fails:
```
import file mismatch:
imported module 'default_test' has this __file__ attribute:
  /tmp/e2e-test/tests/features/shopping_cart/default_test.py
which is not the same as the test file we want to collect:
  /tmp/e2e-test/tests/features/user_login/default_test.py
```

**Root cause**: `_write_file()` calls `test_file.parent.mkdir(parents=True, exist_ok=True)` (line 175) to create the directory, but never creates `__init__.py`. Python needs `__init__.py` (or namespace packages) to distinguish same-named modules in different directories.

**Fix**: After `mkdir`, touch `__init__.py` if it doesn't exist:
```python
test_file.parent.mkdir(parents=True, exist_ok=True)
init_file = test_file.parent / "__init__.py"
if not init_file.exists():
    init_file.touch()
```

---

## Bug 4: Function names preserve casing instead of lowercasing

**Severity**: Medium — inconsistent naming, potential duplicate-key collision goes undetected

**File**: `beehave/gherkin.py:40-53`

**Symptom**: Scenario titles produce function names that preserve the original casing:

| Scenario title | Function name | Expected |
|---------------|---------------|----------|
| `Add single item` | `test_Add_single_item` | `test_add_single_item` |
| `Everything is fine` | `test_Everything_is_fine` | `test_everything_is_fine` |

This is inconsistent with how beehave derives path slugs, which does lowercase (`_derive_path_slug` at line 40-41 calls `.lower()`).

**Root cause**: `_derive_function_name()` (line 44-53) collapses whitespace to underscores but never lowercases:

```python
def _derive_function_name(title: str) -> str:
    trimmed = title.strip()
    collapsed = re.sub(r"\s+", "_", trimmed)   # no .lower()
    name = f"test_{collapsed}"
    ...
    return name
```

Meanwhile `_derive_path_slug()` (line 40-41) does lowercase:

```python
def _derive_path_slug(title: str) -> str:
    return re.sub(r"\s+", "_", title.strip()).lower()
```

**Duplicate-key collision**: The collision check at line 172-178 uses exact string matching on the function name. Since case is preserved, these two scenarios in different features are NOT detected as duplicates:

```gherkin
# feature_a.feature
Scenario: Test
```

```gherkin
# feature_b.feature
Scenario: tEsT
```

These produce `test_Test` and `test_tEsT` — different function names, no collision error. But with lowercasing they would both produce `test_test` and correctly trigger the collision detection.

**Fix**: Add `.lower()` to `_derive_function_name`, matching `_derive_path_slug`:

```python
def _derive_function_name(title: str) -> str:
    trimmed = title.strip()
    collapsed = re.sub(r"\s+", "_", trimmed).lower()
    name = f"test_{collapsed}"
    ...
    return name
```
