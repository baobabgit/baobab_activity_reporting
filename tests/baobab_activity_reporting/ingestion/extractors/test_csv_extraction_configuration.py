"""Tests unitaires pour CsvExtractionConfiguration."""

from baobab_activity_reporting.ingestion.extractors.csv_extraction_configuration import (
    CsvExtractionConfiguration,
)


class TestCsvExtractionConfiguration:
    """Tests pour la classe CsvExtractionConfiguration."""

    def test_default_values(self) -> None:
        """Vérifie les valeurs par défaut."""
        config = CsvExtractionConfiguration()
        assert config.separator == ";"
        assert config.encoding == "utf-8"
        assert config.expected_columns == []
        assert config.skip_rows == 0
        assert config.source_label == "csv"

    def test_custom_separator(self) -> None:
        """Vérifie un séparateur personnalisé."""
        config = CsvExtractionConfiguration(separator=",")
        assert config.separator == ","

    def test_custom_encoding(self) -> None:
        """Vérifie un encodage personnalisé."""
        config = CsvExtractionConfiguration(encoding="latin-1")
        assert config.encoding == "latin-1"

    def test_expected_columns(self) -> None:
        """Vérifie les colonnes attendues."""
        cols = ["date", "agent"]
        config = CsvExtractionConfiguration(expected_columns=cols)
        assert config.expected_columns == ["date", "agent"]

    def test_expected_columns_is_copy(self) -> None:
        """Vérifie que la liste est une copie."""
        cols = ["date", "agent"]
        config = CsvExtractionConfiguration(expected_columns=cols)
        cols.append("extra")
        assert config.expected_columns == ["date", "agent"]

    def test_skip_rows(self) -> None:
        """Vérifie le nombre de lignes à ignorer."""
        config = CsvExtractionConfiguration(skip_rows=3)
        assert config.skip_rows == 3

    def test_source_label(self) -> None:
        """Vérifie le libellé de source."""
        config = CsvExtractionConfiguration(source_label="tickets")
        assert config.source_label == "tickets"

    def test_repr(self) -> None:
        """Vérifie __repr__."""
        config = CsvExtractionConfiguration(source_label="test")
        result = repr(config)
        assert "CsvExtractionConfiguration(" in result
        assert "source_label='test'" in result
        assert "separator=';'" in result
