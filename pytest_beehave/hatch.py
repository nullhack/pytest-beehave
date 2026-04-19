"""Hatch command — generate bee-themed example features directory."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class HatchFile:
    """A single generated .feature file to be written.

    Attributes:
        relative_path: Path relative to the features root (e.g. backlog/forager.feature).
        content: The full Gherkin text to write.
    """

    relative_path: str
    content: str


def generate_hatch_files() -> list[HatchFile]: ...


def write_hatch(features_root: Path, files: list[HatchFile]) -> list[str]: ...


def run_hatch(features_root: Path, force: bool) -> list[str]: ...
