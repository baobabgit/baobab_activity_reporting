"""Tests unitaires pour DataCleaner."""

import pandas as pd

from baobab_activity_reporting.processing.cleaning.data_cleaner import (
    DataCleaner,
)


class TestDataCleaner:
    """Tests pour la classe DataCleaner."""

    def test_strip_whitespace(self) -> None:
        """Vérifie la suppression des espaces en début/fin."""
        df = pd.DataFrame({"name": ["  Alice  ", " Bob "]})
        cleaner = DataCleaner(strip_whitespace=True)
        result = cleaner.apply(df)
        assert list(result["name"]) == ["Alice", "Bob"]

    def test_no_strip(self) -> None:
        """Vérifie sans strip."""
        df = pd.DataFrame({"name": ["  Alice  "]})
        cleaner = DataCleaner(strip_whitespace=False)
        result = cleaner.apply(df)
        assert list(result["name"]) == ["  Alice  "]

    def test_normalize_case_lower(self) -> None:
        """Vérifie la normalisation en minuscules."""
        df = pd.DataFrame({"name": ["ALICE", "Bob"]})
        cleaner = DataCleaner(normalize_case="lower")
        result = cleaner.apply(df)
        assert list(result["name"]) == ["alice", "bob"]

    def test_normalize_case_upper(self) -> None:
        """Vérifie la normalisation en majuscules."""
        df = pd.DataFrame({"name": ["alice", "Bob"]})
        cleaner = DataCleaner(normalize_case="upper")
        result = cleaner.apply(df)
        assert list(result["name"]) == ["ALICE", "BOB"]

    def test_normalize_case_title(self) -> None:
        """Vérifie la normalisation en titre."""
        df = pd.DataFrame({"name": ["alice dupont", "BOB MARTIN"]})
        cleaner = DataCleaner(normalize_case="title")
        result = cleaner.apply(df)
        assert list(result["name"]) == ["Alice Dupont", "Bob Martin"]

    def test_no_normalize_case(self) -> None:
        """Vérifie sans normalisation de casse."""
        df = pd.DataFrame({"name": ["Alice"]})
        cleaner = DataCleaner(normalize_case=None)
        result = cleaner.apply(df)
        assert list(result["name"]) == ["Alice"]

    def test_preserves_non_string_columns(self) -> None:
        """Vérifie que les colonnes non-texte sont préservées."""
        df = pd.DataFrame({"val": [1, 2], "name": ["a", "b"]})
        cleaner = DataCleaner(normalize_case="upper")
        result = cleaner.apply(df)
        assert list(result["val"]) == [1, 2]
        assert list(result["name"]) == ["A", "B"]

    def test_handles_nan_values(self) -> None:
        """Vérifie la gestion des valeurs NaN."""
        df = pd.DataFrame({"name": ["Alice", None, "Bob"]})
        cleaner = DataCleaner(strip_whitespace=True)
        result = cleaner.apply(df)
        assert result["name"].iloc[0] == "Alice"
        assert pd.isna(result["name"].iloc[1])

    def test_empty_dataframe(self) -> None:
        """Vérifie sur un DataFrame vide."""
        df = pd.DataFrame({"name": pd.Series([], dtype="object")})
        cleaner = DataCleaner()
        result = cleaner.apply(df)
        assert len(result) == 0

    def test_does_not_modify_original(self) -> None:
        """Vérifie que le DataFrame original n'est pas modifié."""
        df = pd.DataFrame({"name": ["  test  "]})
        cleaner = DataCleaner()
        cleaner.apply(df)
        assert df["name"].iloc[0] == "  test  "

    def test_repr(self) -> None:
        """Vérifie __repr__."""
        cleaner = DataCleaner(normalize_case="lower")
        result = repr(cleaner)
        assert "DataCleaner(" in result
        assert "normalize_case='lower'" in result
