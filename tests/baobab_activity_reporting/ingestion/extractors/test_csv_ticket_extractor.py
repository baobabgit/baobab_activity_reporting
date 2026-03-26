"""Tests unitaires pour CsvTicketExtractor."""

from pathlib import Path

import pytest

from baobab_activity_reporting.exceptions.extraction_error import (
    ExtractionError,
)
from baobab_activity_reporting.ingestion.extractors.csv_extraction_configuration import (
    CsvExtractionConfiguration,
)
from baobab_activity_reporting.ingestion.extractors.csv_ticket_extractor import (
    CsvTicketExtractor,
)


class TestCsvTicketExtractor:
    """Tests pour la classe CsvTicketExtractor."""

    def test_default_configuration(self) -> None:
        """Vérifie la configuration par défaut."""
        extractor = CsvTicketExtractor()
        config = extractor.configuration
        assert config.separator == ";"
        assert config.encoding == "utf-8"
        assert config.source_label == "tickets"
        assert "Numéro" in config.expected_columns
        assert "Canal" in config.expected_columns
        assert "Catégorie" in config.expected_columns

    def test_custom_configuration(self) -> None:
        """Vérifie l'utilisation d'une configuration personnalisée."""
        custom = CsvExtractionConfiguration(
            separator=",",
            encoding="latin-1",
            source_label="custom_tickets",
        )
        extractor = CsvTicketExtractor(configuration=custom)
        assert extractor.configuration.separator == ","
        assert extractor.configuration.source_label == "custom_tickets"

    def test_extract_nominal(self, fixtures_dir: Path) -> None:
        """Vérifie l'extraction nominale des tickets."""
        extractor = CsvTicketExtractor()
        result = extractor.extract(str(fixtures_dir / "tickets.csv"))
        assert result.success is True
        assert result.row_count == 5
        assert result.source_name == "tickets.csv"
        assert result.warnings == []

    def test_extract_file_not_found(self, tmp_path: Path) -> None:
        """Vérifie l'exception si le fichier n'existe pas."""
        extractor = CsvTicketExtractor()
        with pytest.raises(ExtractionError, match="introuvable"):
            extractor.extract(str(tmp_path / "nope.csv"))

    def test_extract_missing_columns(self, tmp_path: Path) -> None:
        """Vérifie les warnings pour colonnes manquantes."""
        csv_file = tmp_path / "partial.csv"
        csv_file.write_text(
            "Numéro;Date\nT001;2026-01-01\n",
            encoding="utf-8",
        )
        extractor = CsvTicketExtractor()
        result = extractor.extract(str(csv_file))
        assert result.success is True
        assert len(result.warnings) == 1
