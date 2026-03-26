"""Tests unitaires pour ColumnMapper."""

import pandas as pd
import pytest

from baobab_activity_reporting.exceptions.standardization_error import (
    StandardizationError,
)
from baobab_activity_reporting.processing.normalization.column_mapper import (
    ColumnMapper,
)


class TestColumnMapper:
    """Tests pour la classe ColumnMapper."""

    def test_apply_nominal(self) -> None:
        """Vérifie le renommage nominal des colonnes."""
        df = pd.DataFrame({"Date": [1], "Agent": [2]})
        mapper = ColumnMapper({"Date": "date", "Agent": "agent"})
        result = mapper.apply(df)
        assert list(result.columns) == ["date", "agent"]

    def test_apply_partial_mapping(self) -> None:
        """Vérifie le renommage partiel (colonne absente)."""
        df = pd.DataFrame({"Date": [1], "Agent": [2]})
        mapper = ColumnMapper({"Date": "date", "Missing": "miss"})
        result = mapper.apply(df)
        assert "date" in result.columns
        assert "Agent" in result.columns

    def test_apply_empty_mapping(self) -> None:
        """Vérifie un mapping vide."""
        df = pd.DataFrame({"A": [1]})
        mapper = ColumnMapper({})
        result = mapper.apply(df)
        assert list(result.columns) == ["A"]

    def test_apply_empty_dataframe_raises(self) -> None:
        """Vérifie l'exception sur un DataFrame complètement vide."""
        df = pd.DataFrame()
        mapper = ColumnMapper({"A": "a"})
        with pytest.raises(StandardizationError, match="vide"):
            mapper.apply(df)

    def test_columns_not_in_mapping_preserved(self) -> None:
        """Vérifie que les colonnes non mappées sont conservées."""
        df = pd.DataFrame({"A": [1], "B": [2], "C": [3]})
        mapper = ColumnMapper({"A": "alpha"})
        result = mapper.apply(df)
        assert "alpha" in result.columns
        assert "B" in result.columns
        assert "C" in result.columns

    def test_repr(self) -> None:
        """Vérifie __repr__."""
        mapper = ColumnMapper({"A": "a", "B": "b"})
        assert "mapping_count=2" in repr(mapper)

    def test_data_preserved(self) -> None:
        """Vérifie que les données sont préservées."""
        df = pd.DataFrame({"X": [10, 20], "Y": ["a", "b"]})
        mapper = ColumnMapper({"X": "x_new"})
        result = mapper.apply(df)
        assert list(result["x_new"]) == [10, 20]
        assert list(result["Y"]) == ["a", "b"]
