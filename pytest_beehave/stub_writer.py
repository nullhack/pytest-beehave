"""Test stub writer for pytest-beehave."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from pytest_beehave.feature_parser import (
    ParsedExample,
    ParsedFeature,
    ParsedRule,
    ParsedStep,
)
from pytest_beehave.models import ExampleId, FeatureSlug, RuleSlug

_SKIP_MARKER = 'pytest.mark.skip(reason="not yet implemented")'
_ORPHAN_MARKER = 'pytest.mark.skip(reason="orphan: no matching @id in .feature files")'
_DEPRECATED_MARKER = "pytest.mark.deprecated"


@dataclass(frozen=True, slots=True)
class SyncAction:
    """Description of a stub sync action taken.

    Attributes:
        action: The action type (CREATE, UPDATE, ORPHAN, DEPRECATED).
        path: Path to the affected test file.
        detail: Optional extra detail string.
    """

    action: str
    path: Path
    detail: str = ""

    def __str__(self) -> str:
        """Return a human-readable summary of the action."""
        if self.detail:
            return f"{self.action} {self.path} ({self.detail})"
        return f"{self.action} {self.path}"


@dataclass(frozen=True, slots=True)
class StubSpec:
    """Specification for a single test stub to write.

    Attributes:
        feature_slug: The feature slug (underscored).
        rule_slug: The rule slug (hyphenated), or None for top-level stubs.
        example: The parsed example.
        feature: The full parsed feature (for docstring context).
    """

    feature_slug: FeatureSlug
    rule_slug: RuleSlug | None
    example: ParsedExample
    feature: ParsedFeature


def build_function_name(feature_slug: FeatureSlug, example_id: ExampleId) -> str:
    """Build the test function name from slug and ID.

    Args:
        feature_slug: The feature slug.
        example_id: The example ID.

    Returns:
        String like 'test_my_feature_aabbccdd'.
    """
    return f"test_{feature_slug}_{example_id}"


def build_class_name(rule_slug: RuleSlug) -> str:
    """Build the test class name from a rule slug.

    Args:
        rule_slug: The rule slug (hyphen-separated).

    Returns:
        String like 'TestMyRule'.
    """
    parts = str(rule_slug).split("-")
    return "Test" + "".join(p.capitalize() for p in parts if p)


def _render_step(step: ParsedStep) -> str:
    """Render a single step for a docstring.

    Args:
        step: The step to render.

    Returns:
        Rendered step text with optional doc_string/data_table.
    """
    rendered = f"    {step.keyword}: {step.text}"
    if step.doc_string is not None:
        indented = "\n".join(f"      {line}" for line in step.doc_string.splitlines())
        rendered = f"{rendered}\n{indented}"
    if step.data_table is not None:
        indented = "\n".join(f"      {line}" for line in step.data_table.splitlines())
        rendered = f"{rendered}\n{indented}"
    return rendered


def build_docstring(
    feature: ParsedFeature,
    rule: ParsedRule | None,
    example: ParsedExample,
) -> str:
    """Build the docstring body for a test stub.

    Args:
        feature: The parsed feature (not used directly, kept for interface).
        rule: The parsed rule containing this example, or None.
        example: The parsed example.

    Returns:
        Docstring content (without surrounding triple-quotes).
    """
    lines: list[str] = []
    for bg_steps in example.background_sections:
        lines.append("    Background:")
        for step in bg_steps:
            lines.append(_render_step(step))
    for step in example.steps:
        lines.append(_render_step(step))
    if example.outline_examples is not None:
        lines.append(f"    {example.outline_examples}")
    return "\n".join(lines)


def _stub_function_source(
    function_name: str,
    docstring_body: str,
    is_deprecated: bool,
) -> str:
    """Build full source text for a single test stub function.

    Args:
        function_name: The test function name.
        docstring_body: The docstring body (without triple-quotes).
        is_deprecated: If True, add @pytest.mark.deprecated.

    Returns:
        Full function source as a string.
    """
    decorator = (
        '@pytest.mark.skip(reason="not yet implemented")\n'
        if not is_deprecated
        else "@pytest.mark.deprecated\n"
    )
    return (
        f"{decorator}"
        f"def {function_name}() -> None:\n"
        f'    """\n{docstring_body}\n    """\n'
        f"    raise NotImplementedError\n"
    )


def _build_file_header(story_slug: str) -> str:
    """Build the header for a new test stub file.

    Args:
        story_slug: The story file stem (underscore-separated).

    Returns:
        File header string including module docstring and imports.
    """
    title = story_slug.replace("_", " ")
    return f'"""Tests for {title} story."""\n\nimport pytest\n\n\n'


def _indent_stub(source: str, indent: str = "    ") -> str:
    """Indent all lines of a stub by the given prefix.

    Args:
        source: The stub source code.
        indent: Indentation prefix.

    Returns:
        Indented source.
    """
    return "\n".join(
        indent + line if line.strip() else line for line in source.splitlines()
    )


def _append_stub_to_file(path: Path, function_source: str) -> None:
    """Append a stub function to an existing file.

    Args:
        path: Path to the test file.
        function_source: The stub function source code.
    """
    existing = path.read_text(encoding="utf-8")
    updated = existing.rstrip("\n") + "\n\n\n" + function_source + "\n"
    path.write_text(updated, encoding="utf-8")


def write_stub_to_file(path: Path, spec: StubSpec) -> SyncAction:
    """Write a test stub for a single example to a test file.

    Creates the file if it doesn't exist, appends if it does.
    For Rule-based specs, wraps the stub in a Test<RuleSlug> class.

    Args:
        path: Path to the test file.
        spec: The stub specification.

    Returns:
        A SyncAction describing what was done.
    """
    function_name = build_function_name(spec.feature_slug, spec.example.example_id)
    rule = _find_rule(spec.feature, spec.rule_slug) if spec.rule_slug else None
    docstring_body = build_docstring(spec.feature, rule, spec.example)
    function_source = _stub_function_source(
        function_name, docstring_body, spec.example.is_deprecated
    )
    if spec.rule_slug is not None:
        return _write_class_based_stub(path, spec, function_name, function_source)
    if not path.exists():
        story_slug = path.stem.removesuffix("_test")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            _build_file_header(story_slug) + function_source + "\n",
            encoding="utf-8",
        )
        return SyncAction(action="CREATE", path=path)
    _append_stub_to_file(path, function_source)
    return SyncAction(action="UPDATE", path=path)


def _write_class_based_stub(
    path: Path,
    spec: StubSpec,
    function_name: str,
    function_source: str,
) -> SyncAction:
    """Write a class-method stub for a Rule-based spec.

    Args:
        path: Path to the test file.
        spec: The stub specification.
        function_name: The test function name.
        function_source: The function source code (module-level style).

    Returns:
        SyncAction describing the action taken.
    """
    if spec.rule_slug is None:
        raise ValueError("rule_slug must not be None for class-based stubs")
    class_name = build_class_name(spec.rule_slug)
    method_source = _indent_stub(function_source)
    if not path.exists():
        story_slug = path.stem.removesuffix("_test")
        path.parent.mkdir(parents=True, exist_ok=True)
        class_block = f"class {class_name}:\n{method_source}\n"
        path.write_text(
            _build_file_header(story_slug) + class_block + "\n",
            encoding="utf-8",
        )
        return SyncAction(action="CREATE", path=path)
    content = path.read_text(encoding="utf-8")
    if f"class {class_name}:" not in content:
        class_block = f"class {class_name}:\n{method_source}\n"
        updated = content.rstrip("\n") + "\n\n\n" + class_block + "\n"
        path.write_text(updated, encoding="utf-8")
    else:
        updated = content.rstrip("\n") + "\n\n" + method_source + "\n"
        path.write_text(updated, encoding="utf-8")
    return SyncAction(action="UPDATE", path=path)


def _find_rule(feature: ParsedFeature, rule_slug: RuleSlug) -> ParsedRule | None:
    """Find a rule in a feature by its slug.

    Args:
        feature: The parsed feature.
        rule_slug: The rule slug to find.

    Returns:
        The matching ParsedRule, or None.
    """
    for rule in feature.rules:
        if rule.rule_slug == rule_slug:
            return rule
    return None


def _update_docstring_in_content(
    content: str,
    function_name: str,
    new_docstring_body: str,
) -> str:
    """Replace the docstring of a named function in file content.

    Args:
        content: Full file content.
        function_name: The function name to find.
        new_docstring_body: New docstring body (without triple-quotes).

    Returns:
        Updated file content.
    """
    import re

    pattern = re.compile(
        rf'(def {re.escape(function_name)}\([^)]*\) -> None:\n    """).*?(""")',
        re.DOTALL,
    )

    def replacer(m: re.Match[str]) -> str:
        return f"{m.group(1)}\n{new_docstring_body}\n    {m.group(2)}"

    return pattern.sub(replacer, content, count=1)


def _rename_function_in_content(content: str, old_name: str, new_name: str) -> str:
    """Rename a test function in file content.

    Args:
        content: Full file content.
        old_name: Current function name.
        new_name: New function name.

    Returns:
        Updated file content.
    """
    import re

    pattern = re.compile(
        rf"^def {re.escape(old_name)}\(([^)]*)\) -> None:",
        re.MULTILINE,
    )
    return pattern.sub(
        lambda m: f"def {new_name}({m.group(1)}) -> None:",
        content,
        count=1,
    )


def update_docstring(
    path: Path,
    function_name: str,
    new_docstring_body: str,
    feature_slug: FeatureSlug,
    example_id: ExampleId,
) -> SyncAction | None:
    """Update the docstring and/or rename a function in a test file.

    Args:
        path: Path to the test file.
        function_name: Current function name.
        new_docstring_body: New docstring content.
        feature_slug: Current feature slug (for renaming).
        example_id: The example ID (for renaming).

    Returns:
        SyncAction if the file was changed, else None.
    """
    original = path.read_text(encoding="utf-8")
    content = original
    new_name = build_function_name(feature_slug, example_id)
    if function_name != new_name:
        content = _rename_function_in_content(content, function_name, new_name)
    content = _update_docstring_in_content(content, new_name, new_docstring_body)
    if content == original:
        return None
    path.write_text(content, encoding="utf-8")
    return SyncAction(action="UPDATE", path=path)


def mark_orphan(path: Path, function_name: str) -> SyncAction | None:
    """Add an orphan skip marker before a function if not already present.

    Args:
        path: Path to the test file.
        function_name: The function to mark as orphan.

    Returns:
        SyncAction if file was changed, else None.
    """
    import re

    content = path.read_text(encoding="utf-8")
    orphan_reason = "orphan: no matching @id in .feature files"
    marker_line = f'@pytest.mark.skip(reason="{orphan_reason}")\n'
    match = re.search(
        rf"^def {re.escape(function_name)}\([^)]*\) -> None:",
        content,
        re.MULTILINE,
    )
    if not match:
        return None
    if content[: match.start()].endswith(marker_line):
        return None
    updated = content[: match.start()] + marker_line + content[match.start() :]
    path.write_text(updated, encoding="utf-8")
    return SyncAction(action="ORPHAN", path=path)


def remove_orphan_marker(path: Path, function_name: str) -> SyncAction | None:
    """Remove orphan skip marker before a function if present.

    Args:
        path: Path to the test file.
        function_name: The function to un-orphan.

    Returns:
        SyncAction if file was changed, else None.
    """
    import re

    content = path.read_text(encoding="utf-8")
    escaped_marker = re.escape(
        '@pytest.mark.skip(reason="orphan: no matching @id in .feature files")'
    )
    escaped_name = re.escape(function_name)
    pattern = re.compile(
        rf"^{escaped_marker}\n(def {escaped_name}\([^)]*\) -> None:)",
        re.MULTILINE,
    )
    updated = pattern.sub(r"\1", content, count=1)
    if updated == content:
        return None
    path.write_text(updated, encoding="utf-8")
    return SyncAction(action="ORPHAN", path=path)


def mark_non_conforming(
    path: Path,
    function_name: str,
    correct_file: Path,
    correct_class: str | None,
) -> SyncAction | None:
    """Mark a non-conforming test function with a skip marker.

    A non-conforming stub is one in the wrong file, wrong class, or with a
    wrong function name.

    Args:
        path: Path to the test file.
        function_name: The function name to mark.
        correct_file: Where the stub should be.
        correct_class: The correct class name, if applicable.

    Returns:
        SyncAction if file was changed, else None.
    """
    import re

    detail = f"should be in {correct_file}"
    if correct_class:
        detail += f" class {correct_class}"
    marker_line = f'@pytest.mark.skip(reason="non-conforming: {detail}")\n'
    content = path.read_text(encoding="utf-8")
    match = re.search(
        rf"^def {re.escape(function_name)}\([^)]*\) -> None:",
        content,
        re.MULTILINE,
    )
    if not match:
        return None
    if content[: match.start()].endswith(marker_line):
        return None
    updated = content[: match.start()] + marker_line + content[match.start() :]
    path.write_text(updated, encoding="utf-8")
    return SyncAction(action="NON_CONFORMING", path=path)


def toggle_deprecated_marker(
    path: Path,
    function_name: str,
    *,
    should_be_deprecated: bool,
) -> SyncAction | None:
    """Add or remove @pytest.mark.deprecated before a function.

    Args:
        path: Path to the test file.
        function_name: The test function name.
        should_be_deprecated: If True, add the marker; if False, remove it.

    Returns:
        SyncAction if file was changed, else None.
    """
    import re

    if not path.exists():
        return None
    content = path.read_text(encoding="utf-8")
    decorator_pattern = re.compile(
        r"^( *)((?:@pytest\.mark\.\w+(?:\(.*?\))?\n\1)*)def test_\w+_([a-f0-9]{8})\b",
        re.MULTILINE,
    )
    for match in decorator_pattern.finditer(content):
        hex_suffix = match.group(3)
        if not function_name.endswith(f"_{hex_suffix}"):
            continue
        indent = match.group(1)
        decorators_block = match.group(2)
        # Region from match.start() to def_start is: indent + decorators_block
        def_start = match.start() + len(indent) + len(decorators_block)
        full_decorators = indent + decorators_block
        # Each decorator line is "{indent}@pytest.mark.xxx(...)\n"
        marker_line = f"{indent}@pytest.mark.deprecated\n"
        has_marker = marker_line in full_decorators
        if should_be_deprecated and not has_marker:
            new_decorators = marker_line + full_decorators
            updated = content[: match.start()] + new_decorators + content[def_start:]
            path.write_text(updated, encoding="utf-8")
            return SyncAction(action="DEPRECATED", path=path)
        if not should_be_deprecated and has_marker:
            new_decorators = full_decorators.replace(marker_line, "")
            updated = content[: match.start()] + new_decorators + content[def_start:]
            path.write_text(updated, encoding="utf-8")
            return SyncAction(action="DEPRECATED", path=path)
    return None
