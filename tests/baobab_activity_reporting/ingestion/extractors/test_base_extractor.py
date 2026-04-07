"""Tests unitaires pour BaseExtractor."""

from pathlib import Path

import pytest

from baobab_activity_reporting.domain.results.extraction_result import (
    ExtractionResult,
)
from baobab_activity_reporting.exceptions.extraction_error import (
    ExtractionError,
)
from baobab_activity_reporting.ingestion.extractors.base_extractor import (
    BaseExtractor,
)
from baobab_activity_reporting.ingestion.extractors.csv_extraction_configuration import (
    CsvExtractionConfiguration,
)


class ConcreteExtractor(BaseExtractor):
    """Implémentation concrète pour tester BaseExtractor."""

    def _build_configuration(self) -> CsvExtractionConfiguration:
        """Retourne une configuration par défaut.

        :return: Configuration par défaut.
        :rtype: CsvExtractionConfiguration
        """
        return CsvExtractionConfiguration()


class TestBaseExtractor:
    """Tests pour la classe BaseExtractor."""

    def test_is_abstract(self) -> None:
        """Vérifie que BaseExtractor ne peut pas être instancié."""
        with pytest.raises(TypeError):
            BaseExtractor(configuration=CsvExtractionConfiguration())  # type: ignore[abstract]

    def test_concrete_can_be_instantiated(self) -> None:
        """Vérifie qu'une sous-classe concrète peut être instanciée."""
        extractor = ConcreteExtractor(configuration=CsvExtractionConfiguration())
        assert extractor.configuration is not None

    def test_load_dataframe_matches_extract_metadata(self, fixtures_dir: Path) -> None:
        """Vérifie que load_dataframe + extraction_result_from_dataframe aligne extract."""
        extractor = ConcreteExtractor(
            configuration=CsvExtractionConfiguration(
                separator=";",
                encoding="utf-8",
                source_label="test",
            )
        )
        path = str(fixtures_dir / "incoming_calls.csv")
        frame = extractor.load_dataframe(path)
        meta = extractor.extraction_result_from_dataframe("incoming_calls.csv", frame)
        direct = extractor.extract(path)
        assert meta.row_count == direct.row_count == len(frame)
        assert meta.column_names == direct.column_names

    def test_extract_nominal(self, fixtures_dir: Path) -> None:
        """Vérifie l'extraction nominale d'un fichier CSV."""
        extractor = ConcreteExtractor(
            configuration=CsvExtractionConfiguration(
                separator=";",
                encoding="utf-8",
                source_label="test",
            )
        )
        result = extractor.extract(str(fixtures_dir / "incoming_calls.csv"))
        assert isinstance(result, ExtractionResult)
        assert result.success is True
        assert result.row_count == 5
        assert result.source_name == "incoming_calls.csv"
        assert "Début d'appel" in result.column_names
        assert "Nom de l'agent" in result.column_names

    def test_extract_file_not_found(self, tmp_path: Path) -> None:
        """Vérifie l'exception pour un fichier inexistant."""
        extractor = ConcreteExtractor(configuration=CsvExtractionConfiguration())
        with pytest.raises(ExtractionError, match="introuvable"):
            extractor.extract(str(tmp_path / "missing.csv"))

    def test_extract_path_is_directory(self, tmp_path: Path) -> None:
        """Vérifie l'exception si le chemin est un répertoire."""
        extractor = ConcreteExtractor(configuration=CsvExtractionConfiguration())
        with pytest.raises(ExtractionError, match="fichier"):
            extractor.extract(str(tmp_path))

    def test_extract_empty_file(self, fixtures_dir: Path) -> None:
        """Vérifie l'extraction d'un fichier vide (en-tête seul)."""
        extractor = ConcreteExtractor(configuration=CsvExtractionConfiguration(separator=";"))
        result = extractor.extract(str(fixtures_dir / "empty.csv"))
        assert result.success is True
        assert result.row_count == 0

    def test_extract_with_missing_expected_columns(self, fixtures_dir: Path) -> None:
        """Vérifie les warnings pour colonnes manquantes."""
        extractor = ConcreteExtractor(
            configuration=CsvExtractionConfiguration(
                separator=";",
                expected_columns=["Date", "Heure", "Agent", "INEXISTANT"],
            )
        )
        result = extractor.extract(str(fixtures_dir / "incoming_calls.csv"))
        assert result.success is True
        assert len(result.warnings) == 1
        assert "INEXISTANT" in result.warnings[0]

    def test_extract_with_all_expected_columns(self, fixtures_dir: Path) -> None:
        """Vérifie qu'aucun warning si toutes les colonnes sont présentes."""
        extractor = ConcreteExtractor(
            configuration=CsvExtractionConfiguration(
                separator=";",
                expected_columns=[
                    "Début d'appel",
                    "Nom de l'agent",
                    "Flux",
                ],
            )
        )
        result = extractor.extract(str(fixtures_dir / "incoming_calls.csv"))
        assert result.warnings == []

    def test_extract_bad_encoding(self, tmp_path: Path) -> None:
        """Vérifie l'exception sur un encodage invalide."""
        csv_file = tmp_path / "bad.csv"
        csv_file.write_bytes(b"\xff\xfe" + "col1;col2\n1;2\n".encode("utf-16-le"))
        extractor = ConcreteExtractor(
            configuration=CsvExtractionConfiguration(separator=";", encoding="ascii")
        )
        with pytest.raises(ExtractionError, match="lecture"):
            extractor.extract(str(csv_file))

    def test_extract_with_skip_rows(self, tmp_path: Path) -> None:
        """Vérifie l'option skip_rows."""
        csv_file = tmp_path / "skip.csv"
        csv_file.write_text(
            "# commentaire\ncol1;col2\nval1;val2\n",
            encoding="utf-8",
        )
        extractor = ConcreteExtractor(
            configuration=CsvExtractionConfiguration(separator=";", skip_rows=1)
        )
        result = extractor.extract(str(csv_file))
        assert result.row_count == 1
        assert "col1" in result.column_names

    def test_extract_comma_separator(self, tmp_path: Path) -> None:
        """Vérifie l'extraction avec virgule comme séparateur."""
        csv_file = tmp_path / "comma.csv"
        csv_file.write_text(
            "a,b,c\n1,2,3\n4,5,6\n",
            encoding="utf-8",
        )
        extractor = ConcreteExtractor(configuration=CsvExtractionConfiguration(separator=","))
        result = extractor.extract(str(csv_file))
        assert result.row_count == 2
        assert result.column_names == ["a", "b", "c"]
