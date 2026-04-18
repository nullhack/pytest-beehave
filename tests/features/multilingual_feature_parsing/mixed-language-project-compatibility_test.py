"""Tests for multilingual feature parsing mixed-language project compatibility story."""

from pathlib import Path

import pytest

from pytest_beehave.feature_parser import ParsedFeature, parse_feature
from pytest_beehave.models import ExampleId


@pytest.mark.unit
def test_multilingual_feature_parsing_3c04262e(tmp_path: Path) -> None:
    """
    Given: a project containing a valid Spanish Gherkin feature file and a valid English feature file
    When: parse_feature is called on each file independently
    Then: both files are parsed successfully and return valid ParsedFeature objects
    """
    # Given
    spanish_dir = tmp_path / "mi-funcionalidad"
    spanish_dir.mkdir()
    spanish_file = spanish_dir / "historia.feature"
    spanish_file.write_text(
        "# language: es\n"
        "Característica: Mi funcionalidad\n\n"
        "  @id:a1b2c3d4\n"
        "  Escenario: Un escenario\n"
        "    Dado algo\n"
        "    Cuando algo ocurre\n"
        "    Entonces algo pasa\n",
        encoding="utf-8",
    )

    english_dir = tmp_path / "my-feature"
    english_dir.mkdir()
    english_file = english_dir / "story.feature"
    english_file.write_text(
        "Feature: My feature\n\n"
        "  @id:e1f2a3b4\n"
        "  Example: An example\n"
        "    Given something\n"
        "    When something happens\n"
        "    Then something passes\n",
        encoding="utf-8",
    )

    # When
    spanish_result = parse_feature(spanish_file, folder_name="mi-funcionalidad")
    english_result = parse_feature(english_file, folder_name="my-feature")

    # Then
    assert isinstance(spanish_result, ParsedFeature)
    assert isinstance(english_result, ParsedFeature)
    assert ExampleId("a1b2c3d4") in spanish_result.all_example_ids()
    assert ExampleId("e1f2a3b4") in english_result.all_example_ids()
