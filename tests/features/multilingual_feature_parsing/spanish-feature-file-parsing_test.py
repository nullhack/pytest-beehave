"""Tests for multilingual feature parsing Spanish feature file parsing story."""

from pathlib import Path

import pytest

from pytest_beehave.feature_parser import ParsedFeature, parse_feature
from pytest_beehave.models import ExampleId


@pytest.mark.unit
def test_multilingual_feature_parsing_e1081346(tmp_path: Path) -> None:
    """
    Given: a valid Spanish Gherkin feature file
    When: parse_feature is called on that file
    Then: a ParsedFeature is returned with the correct number of examples
    """
    # Given
    feature_dir = tmp_path / "mi-funcionalidad"
    feature_dir.mkdir()
    feature_file = feature_dir / "historia.feature"
    feature_file.write_text(
        "# language: es\n"
        "Característica: Mi funcionalidad\n\n"
        "  @id:a1b2c3d4\n"
        "  Ejemplo: Un ejemplo\n"
        "    Dado algo\n"
        "    Cuando algo ocurre\n"
        "    Entonces algo pasa\n",
        encoding="utf-8",
    )

    # When
    result = parse_feature(feature_file, folder_name="mi-funcionalidad")

    # Then
    assert isinstance(result, ParsedFeature)
    assert len(result.top_level_examples) == 1
    assert ExampleId("a1b2c3d4") in result.all_example_ids()
