"""Tests unitaires pour CsvIncomingCallsExtractor."""

from pathlib import Path

import pytest

from baobab_activity_reporting.exceptions.extraction_error import (
    ExtractionError,
)
from baobab_activity_reporting.ingestion.extractors.csv_extraction_configuration import (
    CsvExtractionConfiguration,
)
from baobab_activity_reporting.ingestion.extractors.csv_incoming_calls_extractor import (
    CsvIncomingCallsExtractor,
)


class TestCsvIncomingCallsExtractor:
    """Tests pour la classe CsvIncomingCallsExtractor."""

    def test_default_configuration(self) -> None:
        """Vérifie la configuration par défaut."""
        extractor = CsvIncomingCallsExtractor()
        config = extractor.configuration
        assert config.separator == ";"
        assert config.encoding == "utf-8"
        assert config.source_label == "appels_entrants"
        assert "Début d'appel" in config.expected_columns
        assert "Nom de l'agent" in config.expected_columns
        assert "Valeurs de mesures" in config.expected_columns

    def test_custom_configuration(self) -> None:
        """Vérifie l'utilisation d'une configuration personnalisée."""
        custom = CsvExtractionConfiguration(
            separator=",",
            encoding="latin-1",
            source_label="custom",
        )
        extractor = CsvIncomingCallsExtractor(configuration=custom)
        assert extractor.configuration.separator == ","
        assert extractor.configuration.source_label == "custom"

    def test_extract_nominal(self, fixtures_dir: Path) -> None:
        """Vérifie l'extraction nominale des appels entrants."""
        extractor = CsvIncomingCallsExtractor()
        result = extractor.extract(str(fixtures_dir / "incoming_calls.csv"))
        assert result.success is True
        assert result.row_count == 5
        assert result.source_name == "incoming_calls.csv"
        assert result.warnings == []

    def test_extract_missing_columns(self, fixtures_dir: Path) -> None:
        """Vérifie les warnings pour colonnes manquantes."""
        extractor = CsvIncomingCallsExtractor()
        result = extractor.extract(str(fixtures_dir / "incoming_calls_missing_cols.csv"))
        assert result.success is True
        assert len(result.warnings) == 1
        assert "Flux" in result.warnings[0] or "Service" in result.warnings[0]

    def test_extract_file_not_found(self, tmp_path: Path) -> None:
        """Vérifie l'exception si le fichier n'existe pas."""
        extractor = CsvIncomingCallsExtractor()
        with pytest.raises(ExtractionError, match="introuvable"):
            extractor.extract(str(tmp_path / "nope.csv"))

    def test_extract_empty_file(self, fixtures_dir: Path) -> None:
        """Vérifie l'extraction d'un fichier vide."""
        extractor = CsvIncomingCallsExtractor()
        result = extractor.extract(str(fixtures_dir / "empty.csv"))
        assert result.success is True
        assert result.row_count == 0
