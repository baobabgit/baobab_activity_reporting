"""Tests unitaires pour ValueStandardizer."""

import pandas as pd

from baobab_activity_reporting.processing.normalization.value_standardizer import (
    ValueStandardizer,
)


class TestValueStandardizer:
    """Tests pour la classe ValueStandardizer."""

    def test_collapse_whitespace(self) -> None:
        """Vérifie la réduction des espaces multiples."""
        df = pd.DataFrame({"agent": ["  Dupont   Marie  "]})
        std = ValueStandardizer(columns=["agent"])
        result = std.apply(df)
        assert result["agent"].iloc[0] == "Dupont Marie"

    def test_strip_accents(self) -> None:
        """Vérifie la suppression des accents."""
        df = pd.DataFrame({"site": ["Évreux-lès-Bains"]})
        std = ValueStandardizer(columns=["site"], strip_accents=True)
        result = std.apply(df)
        assert result["site"].iloc[0] == "Evreux-les-Bains"

    def test_to_upper(self) -> None:
        """Vérifie la conversion en majuscules."""
        df = pd.DataFrame({"agent": ["dupont marie"]})
        std = ValueStandardizer(columns=["agent"], to_upper=True)
        result = std.apply(df)
        assert result["agent"].iloc[0] == "DUPONT MARIE"

    def test_combined_options(self) -> None:
        """Vérifie les options combinées."""
        df = pd.DataFrame({"agent": ["  Éric  Dupont  "]})
        std = ValueStandardizer(
            columns=["agent"],
            strip_accents=True,
            to_upper=True,
        )
        result = std.apply(df)
        assert result["agent"].iloc[0] == "ERIC DUPONT"

    def test_missing_column_ignored(self) -> None:
        """Vérifie que les colonnes absentes sont ignorées."""
        df = pd.DataFrame({"other": ["test"]})
        std = ValueStandardizer(columns=["missing"])
        result = std.apply(df)
        assert list(result["other"]) == ["test"]

    def test_preserves_non_string(self) -> None:
        """Vérifie que les valeurs non-string sont préservées."""
        df = pd.DataFrame({"col": [42, None, "text"]})
        std = ValueStandardizer(columns=["col"], to_upper=True)
        result = std.apply(df)
        assert result["col"].iloc[0] == 42
        assert pd.isna(result["col"].iloc[1])
        assert result["col"].iloc[2] == "TEXT"

    def test_does_not_modify_original(self) -> None:
        """Vérifie que le DataFrame original n'est pas modifié."""
        df = pd.DataFrame({"agent": ["  test  "]})
        std = ValueStandardizer(columns=["agent"])
        std.apply(df)
        assert df["agent"].iloc[0] == "  test  "

    def test_empty_dataframe(self) -> None:
        """Vérifie sur un DataFrame vide."""
        df = pd.DataFrame({"agent": pd.Series([], dtype="object")})
        std = ValueStandardizer(columns=["agent"])
        result = std.apply(df)
        assert len(result) == 0

    def test_repr(self) -> None:
        """Vérifie __repr__."""
        std = ValueStandardizer(columns=["a"], strip_accents=True)
        result = repr(std)
        assert "ValueStandardizer(" in result
        assert "strip_accents=True" in result

    def test_remove_accents_static(self) -> None:
        """Vérifie la méthode statique de suppression d'accents."""
        assert ValueStandardizer._remove_accents("café") == "cafe"
        assert ValueStandardizer._remove_accents("naïve") == "naive"
