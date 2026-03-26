"""Tests unitaires pour DataTypeNormalizer."""

import pandas as pd
import pytest

from baobab_activity_reporting.exceptions.standardization_error import (
    StandardizationError,
)
from baobab_activity_reporting.processing.normalization.data_type_normalizer import (
    DataTypeNormalizer,
)


class TestDataTypeNormalizer:
    """Tests pour la classe DataTypeNormalizer."""

    def test_convert_date_column(self) -> None:
        """Vérifie la conversion de colonnes date."""
        df = pd.DataFrame({"date": ["2026-01-01", "2026-01-02"]})
        normalizer = DataTypeNormalizer(date_columns=["date"])
        result = normalizer.apply(df)
        assert pd.api.types.is_datetime64_any_dtype(result["date"])

    def test_convert_date_with_format(self) -> None:
        """Vérifie la conversion avec format explicite."""
        df = pd.DataFrame({"date": ["01/03/2026", "15/03/2026"]})
        normalizer = DataTypeNormalizer(date_columns=["date"], date_format="%d/%m/%Y")
        result = normalizer.apply(df)
        assert result["date"].iloc[0].day == 1
        assert result["date"].iloc[0].month == 3

    def test_convert_int_column(self) -> None:
        """Vérifie la conversion de colonnes entières."""
        df = pd.DataFrame({"count": ["10", "20"]})
        normalizer = DataTypeNormalizer(int_columns=["count"])
        result = normalizer.apply(df)
        assert result["count"].dtype == int

    def test_convert_float_column(self) -> None:
        """Vérifie la conversion de colonnes flottantes."""
        df = pd.DataFrame({"ratio": ["1.5", "2.7"]})
        normalizer = DataTypeNormalizer(float_columns=["ratio"])
        result = normalizer.apply(df)
        assert result["ratio"].dtype == float

    def test_invalid_date_raises(self) -> None:
        """Vérifie l'exception sur une date invalide."""
        df = pd.DataFrame({"date": ["not-a-date"]})
        normalizer = DataTypeNormalizer(date_columns=["date"], date_format="%Y-%m-%d")
        with pytest.raises(StandardizationError, match="date"):
            normalizer.apply(df)

    def test_invalid_int_raises(self) -> None:
        """Vérifie l'exception sur un entier invalide."""
        df = pd.DataFrame({"count": ["abc"]})
        normalizer = DataTypeNormalizer(int_columns=["count"])
        with pytest.raises(StandardizationError, match="entier"):
            normalizer.apply(df)

    def test_invalid_float_raises(self) -> None:
        """Vérifie l'exception sur un flottant invalide."""
        df = pd.DataFrame({"ratio": ["xyz"]})
        normalizer = DataTypeNormalizer(float_columns=["ratio"])
        with pytest.raises(StandardizationError, match="flottant"):
            normalizer.apply(df)

    def test_missing_column_ignored(self) -> None:
        """Vérifie que les colonnes absentes sont ignorées."""
        df = pd.DataFrame({"other": [1]})
        normalizer = DataTypeNormalizer(
            date_columns=["date"],
            int_columns=["count"],
            float_columns=["ratio"],
        )
        result = normalizer.apply(df)
        assert list(result.columns) == ["other"]

    def test_does_not_modify_original(self) -> None:
        """Vérifie que le DataFrame original n'est pas modifié."""
        df = pd.DataFrame({"count": ["10"]})
        normalizer = DataTypeNormalizer(int_columns=["count"])
        normalizer.apply(df)
        assert df["count"].iloc[0] == "10"

    def test_default_no_columns(self) -> None:
        """Vérifie le fonctionnement avec aucune colonne définie."""
        df = pd.DataFrame({"a": [1]})
        normalizer = DataTypeNormalizer()
        result = normalizer.apply(df)
        assert list(result["a"]) == [1]

    def test_repr(self) -> None:
        """Vérifie __repr__."""
        normalizer = DataTypeNormalizer(date_columns=["d"])
        result = repr(normalizer)
        assert "DataTypeNormalizer(" in result
        assert "date_columns=['d']" in result
