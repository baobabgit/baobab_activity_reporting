"""Tests unitaires pour ExtractionResult."""

from baobab_activity_reporting.domain.results.extraction_result import (
    ExtractionResult,
)


class TestExtractionResult:
    """Tests pour la classe ExtractionResult."""

    def test_creation_nominal(self) -> None:
        """Vérifie la création avec des données valides."""
        result = ExtractionResult("appels.csv", 150, ["date", "agent"])
        assert result.source_name == "appels.csv"
        assert result.row_count == 150
        assert result.column_names == ["date", "agent"]
        assert result.errors == []
        assert result.warnings == []

    def test_creation_with_errors(self) -> None:
        """Vérifie la création avec des erreurs."""
        result = ExtractionResult("f.csv", 0, [], errors=["fichier vide"])
        assert result.errors == ["fichier vide"]

    def test_creation_with_warnings(self) -> None:
        """Vérifie la création avec des avertissements."""
        result = ExtractionResult("f.csv", 10, ["col"], warnings=["encodage détecté"])
        assert result.warnings == ["encodage détecté"]

    def test_success_true_when_no_errors(self) -> None:
        """Vérifie success=True sans erreurs."""
        result = ExtractionResult("f.csv", 10, ["col"])
        assert result.success is True

    def test_success_false_when_errors(self) -> None:
        """Vérifie success=False avec erreurs."""
        result = ExtractionResult("f.csv", 0, [], errors=["erreur"])
        assert result.success is False

    def test_success_true_with_warnings_only(self) -> None:
        """Vérifie success=True avec seulement des warnings."""
        result = ExtractionResult("f.csv", 5, ["c"], warnings=["warn"])
        assert result.success is True

    def test_column_names_is_copy(self) -> None:
        """Vérifie que la liste de colonnes est une copie."""
        cols = ["a", "b"]
        result = ExtractionResult("f.csv", 1, cols)
        cols.append("c")
        assert result.column_names == ["a", "b"]

    def test_errors_is_copy(self) -> None:
        """Vérifie que la liste d'erreurs est une copie."""
        errs = ["err1"]
        result = ExtractionResult("f.csv", 0, [], errors=errs)
        errs.append("err2")
        assert result.errors == ["err1"]

    def test_warnings_is_copy(self) -> None:
        """Vérifie que la liste de warnings est une copie."""
        warns = ["w1"]
        result = ExtractionResult("f.csv", 1, ["c"], warnings=warns)
        warns.append("w2")
        assert result.warnings == ["w1"]

    def test_repr(self) -> None:
        """Vérifie __repr__."""
        result = ExtractionResult("f.csv", 10, ["c"])
        text = repr(result)
        assert "ExtractionResult(" in text
        assert "source_name='f.csv'" in text
        assert "success=True" in text

    def test_zero_row_count(self) -> None:
        """Vérifie un résultat avec zéro ligne."""
        result = ExtractionResult("f.csv", 0, [])
        assert result.row_count == 0
        assert result.success is True
