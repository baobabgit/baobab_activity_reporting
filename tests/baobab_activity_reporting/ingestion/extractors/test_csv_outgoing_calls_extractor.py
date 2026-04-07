"""Tests unitaires pour CsvOutgoingCallsExtractor."""

from pathlib import Path

import pytest

from baobab_activity_reporting.exceptions.extraction_error import (
    ExtractionError,
)
from baobab_activity_reporting.ingestion.extractors.csv_extraction_configuration import (
    CsvExtractionConfiguration,
)
from baobab_activity_reporting.ingestion.extractors.csv_outgoing_calls_extractor import (
    CsvOutgoingCallsExtractor,
)


class TestCsvOutgoingCallsExtractor:
    """Tests pour la classe CsvOutgoingCallsExtractor."""

    def test_default_configuration(self) -> None:
        """Vérifie la configuration par défaut."""
        extractor = CsvOutgoingCallsExtractor()
        config = extractor.configuration
        assert config.separator == ";"
        assert config.encoding == "utf-8"
        assert config.source_label == "appels_sortants"
        assert "Début d'appel" in config.expected_columns
        assert "Valeurs de mesures" in config.expected_columns

    def test_custom_configuration(self) -> None:
        """Vérifie l'utilisation d'une configuration personnalisée."""
        custom = CsvExtractionConfiguration(
            separator=",",
            encoding="latin-1",
            source_label="custom_out",
        )
        extractor = CsvOutgoingCallsExtractor(configuration=custom)
        assert extractor.configuration.separator == ","
        assert extractor.configuration.source_label == "custom_out"

    def test_extract_nominal(self, fixtures_dir: Path) -> None:
        """Vérifie l'extraction nominale des appels sortants."""
        extractor = CsvOutgoingCallsExtractor()
        result = extractor.extract(str(fixtures_dir / "outgoing_calls.csv"))
        assert result.success is True
        assert result.row_count == 3
        assert result.source_name == "outgoing_calls.csv"
        assert result.warnings == []

    def test_extract_file_not_found(self, tmp_path: Path) -> None:
        """Vérifie l'exception si le fichier n'existe pas."""
        extractor = CsvOutgoingCallsExtractor()
        with pytest.raises(ExtractionError, match="introuvable"):
            extractor.extract(str(tmp_path / "nope.csv"))

    def test_extract_missing_columns(self, tmp_path: Path) -> None:
        """Vérifie les warnings pour colonnes manquantes."""
        csv_file = tmp_path / "partial.csv"
        csv_file.write_text(
            "Catégorie de qualification;Début d'appel;Fin d'appel\n;;01-01-26 08:00:00\n",
            encoding="utf-8",
        )
        extractor = CsvOutgoingCallsExtractor()
        result = extractor.extract(str(csv_file))
        assert result.success is True
        assert len(result.warnings) == 1
