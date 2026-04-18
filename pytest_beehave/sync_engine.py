"""Sync engine for pytest-beehave — orchestrates stub creation and updates."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from pytest_beehave.feature_parser import (
    ParsedExample,
    ParsedFeature,
    ParsedRule,
    parse_feature,
)
from pytest_beehave.models import ExampleId, FeatureStage
from pytest_beehave.stub_reader import ExistingStub, read_stubs_from_file
from pytest_beehave.stub_writer import (
    StubSpec,
    SyncAction,
    build_docstring,
    build_function_name,
    mark_orphan,
    remove_orphan_marker,
    toggle_deprecated_marker,
    update_docstring,
    write_stub_to_file,
)

_FEATURE_STAGES = (
    FeatureStage.BACKLOG,
    FeatureStage.IN_PROGRESS,
    FeatureStage.COMPLETED,
)


class FileSystemProtocol(Protocol):
    """Protocol for filesystem operations needed by the sync engine."""

    def list_feature_files(self, stage_dir: Path) -> list[Path]:  # pragma: no cover
        """List all .feature files recursively under stage_dir."""
        ...

    def list_test_files(self, tests_dir: Path) -> list[Path]:  # pragma: no cover
        """List all *_test.py files recursively under tests_dir."""
        ...


@dataclass(frozen=True, slots=True)
class _RealFileSystem:
    """Concrete filesystem adapter using pathlib."""

    def list_feature_files(self, stage_dir: Path) -> list[Path]:
        """List all .feature files recursively under stage_dir.

        Args:
            stage_dir: Root directory to search.

        Returns:
            Sorted list of .feature file paths.
        """
        return sorted(stage_dir.rglob("*.feature"))

    def list_test_files(self, tests_dir: Path) -> list[Path]:
        """List all *_test.py files recursively under tests_dir.

        Args:
            tests_dir: Root directory to search.

        Returns:
            Sorted list of test file paths.
        """
        return sorted(tests_dir.rglob("*_test.py"))


@dataclass(frozen=True, slots=True)
class SyncResult:
    """Result of a sync operation.

    Attributes:
        actions: Tuple of SyncAction objects describing what was done.
    """

    actions: tuple[SyncAction, ...]

    @property
    def is_noop(self) -> bool:
        """Return True if no actions were taken."""
        return len(self.actions) == 0


def _collect_all_ids(
    features_dir: Path,
    filesystem: FileSystemProtocol,
) -> frozenset[ExampleId]:
    """Collect all example IDs from all .feature files.

    Args:
        features_dir: Root of the features directory.
        filesystem: Filesystem adapter.

    Returns:
        Frozenset of ExampleId objects.
    """
    import re

    id_re = re.compile(r"@id:([a-f0-9]{8})")
    ids: set[ExampleId] = set()
    for stage in _FEATURE_STAGES:
        stage_dir = features_dir / stage.value
        if not stage_dir.exists():
            continue
        for path in filesystem.list_feature_files(stage_dir):
            text = path.read_text(encoding="utf-8")
            ids.update(ExampleId(match.group(1)) for match in id_re.finditer(text))
    return frozenset(ids)


def _sync_orphans(
    tests_dir: Path,
    all_ids: frozenset[ExampleId],
    filesystem: FileSystemProtocol,
) -> list[SyncAction]:
    """Add or remove orphan markers for test functions without matching @id.

    Args:
        tests_dir: Root of the tests/features/ directory.
        all_ids: All known example IDs.
        filesystem: Filesystem adapter.

    Returns:
        List of SyncAction objects.
    """
    actions: list[SyncAction] = []
    for test_file in filesystem.list_test_files(tests_dir):
        stubs = read_stubs_from_file(test_file)
        for stub in stubs:
            if stub.example_id not in all_ids:
                action = mark_orphan(test_file, stub.function_name)
            else:
                action = remove_orphan_marker(test_file, stub.function_name)
            if action is not None:
                actions.append(action)
    return actions


def _sync_active_feature(
    feature: ParsedFeature,
    tests_dir: Path,
) -> list[SyncAction]:
    """Sync stubs for an active (backlog/in-progress) feature.

    Args:
        feature: The parsed feature.
        tests_dir: Root of the tests/features/ directory.

    Returns:
        List of SyncAction objects.
    """
    actions: list[SyncAction] = []
    feature_test_dir = tests_dir / str(feature.feature_slug)

    if feature.rules:
        for rule in feature.rules:
            actions.extend(_sync_rule_stubs(feature, rule, feature_test_dir))
    elif feature.top_level_examples:
        actions.extend(_sync_top_level_stubs(feature, feature_test_dir))

    return actions


def _sync_rule_stubs(
    feature: ParsedFeature,
    rule: ParsedRule,
    feature_test_dir: Path,
) -> list[SyncAction]:
    """Sync stubs for a single rule block.

    Args:
        feature: The parsed feature.
        rule: The parsed rule.
        feature_test_dir: Directory for this feature's tests.

    Returns:
        List of SyncAction objects.
    """
    if not rule.examples:
        return []
    test_file = feature_test_dir / f"{rule.rule_slug}_test.py"
    existing = {s.example_id: s for s in read_stubs_from_file(test_file)}
    actions: list[SyncAction] = []
    for example in rule.examples:
        action = _sync_one_example(feature, rule, example, test_file, existing)
        if action is not None:
            actions.append(action)
    actions.extend(_sync_deprecated_in_rule(feature, rule, test_file))
    return actions


def _sync_one_example(
    feature: ParsedFeature,
    rule: ParsedRule | None,
    example: ParsedExample,
    test_file: Path,
    existing: dict[ExampleId, ExistingStub],
) -> SyncAction | None:
    """Sync a single example stub — create or update.

    Args:
        feature: The parsed feature.
        rule: The parsed rule (or None for top-level).
        example: The parsed example.
        test_file: Path to the test file.
        existing: Map of existing stubs by example ID.

    Returns:
        SyncAction or None.
    """
    if example.example_id in existing:
        stub = existing[example.example_id]
        new_docstring = build_docstring(feature, rule, example)
        return update_docstring(
            test_file,
            stub.function_name,
            new_docstring,
            feature.feature_slug,
            example.example_id,
        )
    spec = StubSpec(
        feature_slug=feature.feature_slug,
        rule_slug=rule.rule_slug if rule else None,
        example=example,
        feature=feature,
    )
    return write_stub_to_file(test_file, spec)


def _sync_deprecated_in_rule(
    feature: ParsedFeature,
    rule: ParsedRule,
    test_file: Path,
) -> list[SyncAction]:
    """Sync deprecated markers for all examples in a rule.

    Args:
        feature: The parsed feature.
        rule: The parsed rule.
        test_file: Path to the test file.

    Returns:
        List of SyncAction objects.
    """
    actions: list[SyncAction] = []
    for example in rule.examples:
        func_name = build_function_name(feature.feature_slug, example.example_id)
        action = toggle_deprecated_marker(
            test_file, func_name, should_be_deprecated=example.is_deprecated
        )
        if action is not None:
            actions.append(action)
    return actions


def _sync_top_level_stubs(
    feature: ParsedFeature,
    feature_test_dir: Path,
) -> list[SyncAction]:
    """Sync stubs for top-level examples (no Rule blocks).

    Args:
        feature: The parsed feature.
        feature_test_dir: Directory for this feature's tests.

    Returns:
        List of SyncAction objects.
    """
    test_file = feature_test_dir / "examples_test.py"
    existing = {s.example_id: s for s in read_stubs_from_file(test_file)}
    actions: list[SyncAction] = []
    for example in feature.top_level_examples:
        action = _sync_one_example(feature, None, example, test_file, existing)
        if action is not None:
            actions.append(action)
    for example in feature.top_level_examples:
        func_name = build_function_name(feature.feature_slug, example.example_id)
        action = toggle_deprecated_marker(
            test_file, func_name, should_be_deprecated=example.is_deprecated
        )
        if action is not None:
            actions.append(action)
    return actions


def _sync_completed_feature(
    feature: ParsedFeature,
    tests_dir: Path,
) -> list[SyncAction]:
    """Sync deprecated markers only for a completed feature.

    Args:
        feature: The parsed feature.
        tests_dir: Root of the tests/features/ directory.

    Returns:
        List of SyncAction objects.
    """
    feature_test_dir = tests_dir / str(feature.feature_slug)
    actions: list[SyncAction] = []
    if feature.rules:
        for rule in feature.rules:
            test_file = feature_test_dir / f"{rule.rule_slug}_test.py"
            actions.extend(_sync_deprecated_in_rule(feature, rule, test_file))
    else:
        test_file = feature_test_dir / "examples_test.py"
        for example in feature.top_level_examples:
            func_name = build_function_name(feature.feature_slug, example.example_id)
            action = toggle_deprecated_marker(
                test_file, func_name, should_be_deprecated=example.is_deprecated
            )
            if action is not None:
                actions.append(action)
    return actions


def discover_feature_locations(
    features_dir: Path,
    filesystem: FileSystemProtocol,
) -> list[tuple[ParsedFeature, FeatureStage]]:
    """Discover all feature files and their stages.

    Args:
        features_dir: Root of the features directory.
        filesystem: Filesystem adapter.

    Returns:
        List of (ParsedFeature, FeatureStage) tuples.
    """
    results: list[tuple[ParsedFeature, FeatureStage]] = []
    for stage in _FEATURE_STAGES:
        stage_dir = features_dir / stage.value
        if not stage_dir.exists():
            continue
        for feature_path in filesystem.list_feature_files(stage_dir):
            if feature_path.parent == stage_dir:
                folder_name = feature_path.stem
            else:
                folder_name = feature_path.parent.name
            feature = parse_feature(feature_path, folder_name)
            results.append((feature, stage))
    return results


def run_sync(
    features_root: Path,
    tests_root: Path,
    filesystem: FileSystemProtocol | None = None,
) -> list[str]:
    """Sync test stubs from .feature files to the tests directory.

    Args:
        features_root: Root of the features directory (contains backlog/,
            in-progress/, completed/).
        tests_root: Root of the tests/features/ directory.
        filesystem: Optional filesystem adapter. Defaults to _RealFileSystem.

    Returns:
        List of action description strings.
    """
    if filesystem is None:
        filesystem = _RealFileSystem()
    actions: list[SyncAction] = []
    feature_stage_pairs = discover_feature_locations(features_root, filesystem)
    for feature, stage in feature_stage_pairs:
        if stage == FeatureStage.COMPLETED:
            actions.extend(_sync_completed_feature(feature, tests_root))
        else:
            actions.extend(_sync_active_feature(feature, tests_root))
    all_ids = _collect_all_ids(features_root, filesystem)
    actions.extend(_sync_orphans(tests_root, all_ids, filesystem))
    return [str(a) for a in actions]
