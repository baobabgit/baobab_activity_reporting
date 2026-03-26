"""Tests unitaires pour StandardizationPipeline."""

import pandas as pd

from baobab_activity_reporting.processing.cleaning.data_cleaner import (
    DataCleaner,
)
from baobab_activity_reporting.processing.normalization.column_mapper import (
    ColumnMapper,
)
from baobab_activity_reporting.processing.normalization.data_type_normalizer import (
    DataTypeNormalizer,
)
from baobab_activity_reporting.processing.normalization.standardization_pipeline import (
    StandardizationPipeline,
)
from baobab_activity_reporting.processing.normalization.value_standardizer import (
    ValueStandardizer,
)


class TestStandardizationPipeline:
    """Tests pour la classe StandardizationPipeline."""

    def test_run_all_steps(self) -> None:
        """Vérifie l'exécution de toutes les étapes."""
        df = pd.DataFrame(
            {
                "Date": ["2026-01-01"],
                "Agent": ["  Dupont  "],
            }
        )
        pipeline = StandardizationPipeline(
            column_mapper=ColumnMapper({"Date": "date", "Agent": "agent"}),
            data_cleaner=DataCleaner(strip_whitespace=True),
            type_normalizer=DataTypeNormalizer(date_columns=["date"]),
            value_standardizer=ValueStandardizer(columns=["agent"], to_upper=True),
        )
        result = pipeline.run(df)
        assert "date" in result.columns
        assert "agent" in result.columns
        assert pd.api.types.is_datetime64_any_dtype(result["date"])
        assert result["agent"].iloc[0] == "DUPONT"

    def test_run_no_steps(self) -> None:
        """Vérifie le pipeline sans aucune étape."""
        df = pd.DataFrame({"A": [1]})
        pipeline = StandardizationPipeline()
        result = pipeline.run(df)
        assert list(result["A"]) == [1]

    def test_run_mapper_only(self) -> None:
        """Vérifie avec le mapper seul."""
        df = pd.DataFrame({"X": [1]})
        pipeline = StandardizationPipeline(column_mapper=ColumnMapper({"X": "x"}))
        result = pipeline.run(df)
        assert "x" in result.columns

    def test_run_cleaner_only(self) -> None:
        """Vérifie avec le nettoyeur seul."""
        df = pd.DataFrame({"name": ["  test  "]})
        pipeline = StandardizationPipeline(data_cleaner=DataCleaner())
        result = pipeline.run(df)
        assert result["name"].iloc[0] == "test"

    def test_run_normalizer_only(self) -> None:
        """Vérifie avec le normaliseur seul."""
        df = pd.DataFrame({"count": ["10"]})
        pipeline = StandardizationPipeline(
            type_normalizer=DataTypeNormalizer(int_columns=["count"])
        )
        result = pipeline.run(df)
        assert result["count"].iloc[0] == 10

    def test_run_standardizer_only(self) -> None:
        """Vérifie avec le standardiseur seul."""
        df = pd.DataFrame({"agent": ["test"]})
        pipeline = StandardizationPipeline(
            value_standardizer=ValueStandardizer(columns=["agent"], to_upper=True)
        )
        result = pipeline.run(df)
        assert result["agent"].iloc[0] == "TEST"

    def test_repr_with_all_steps(self) -> None:
        """Vérifie __repr__ avec toutes les étapes."""
        pipeline = StandardizationPipeline(
            column_mapper=ColumnMapper({}),
            data_cleaner=DataCleaner(),
            type_normalizer=DataTypeNormalizer(),
            value_standardizer=ValueStandardizer(columns=[]),
        )
        result = repr(pipeline)
        assert "column_mapper" in result
        assert "data_cleaner" in result
        assert "type_normalizer" in result
        assert "value_standardizer" in result

    def test_repr_with_no_steps(self) -> None:
        """Vérifie __repr__ sans étape."""
        pipeline = StandardizationPipeline()
        assert "steps=[]" in repr(pipeline)

    def test_order_of_operations(self) -> None:
        """Vérifie l'ordre : mapper → cleaner → normalizer → standardizer."""
        df = pd.DataFrame({"Raw": ["  10  "]})
        pipeline = StandardizationPipeline(
            column_mapper=ColumnMapper({"Raw": "value"}),
            data_cleaner=DataCleaner(strip_whitespace=True),
            type_normalizer=DataTypeNormalizer(int_columns=["value"]),
        )
        result = pipeline.run(df)
        assert result["value"].iloc[0] == 10
