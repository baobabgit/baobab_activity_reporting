"""Tests unitaires pour DatasetValidator."""

import pandas as pd

from baobab_activity_reporting.processing.validation.dataset_validator import (
    DatasetValidator,
)
from baobab_activity_reporting.processing.validation.schema_registry import (
    ColumnPresenceRule,
    NullRatioRule,
)


class TestDatasetValidator:
    """Tests pour la classe DatasetValidator."""

    def test_validate_all_pass(self) -> None:
        """Vérifie la validation quand toutes les règles passent."""
        df = pd.DataFrame({"date": ["2026-01-01"], "agent": ["A"]})
        validator = DatasetValidator(rules=[ColumnPresenceRule(["date", "agent"])])
        result = validator.validate(df)
        assert result.is_valid is True

    def test_validate_column_missing(self) -> None:
        """Vérifie l'échec quand une colonne manque."""
        df = pd.DataFrame({"date": ["2026-01-01"]})
        validator = DatasetValidator(rules=[ColumnPresenceRule(["date", "agent"])])
        result = validator.validate(df)
        assert result.is_valid is False

    def test_validate_multiple_rules(self) -> None:
        """Vérifie l'agrégation de plusieurs règles."""
        df = pd.DataFrame({"date": [None, None], "agent": ["A", "B"]})
        validator = DatasetValidator(
            rules=[
                ColumnPresenceRule(["date", "agent"]),
                NullRatioRule(columns=["date"], max_null_ratio=0.5),
            ]
        )
        result = validator.validate(df)
        assert len(result.warning_list) == 1
        assert result.is_valid is True

    def test_validate_no_rules(self) -> None:
        """Vérifie la validation sans règle."""
        df = pd.DataFrame({"a": [1]})
        validator = DatasetValidator(rules=[])
        result = validator.validate(df)
        assert result.is_valid is True
        assert len(result.messages) == 0

    def test_validate_empty_dataframe(self) -> None:
        """Vérifie la validation sur un DataFrame vide."""
        df = pd.DataFrame({"date": pd.Series([], dtype="object")})
        validator = DatasetValidator(rules=[ColumnPresenceRule(["date"])])
        result = validator.validate(df)
        assert result.is_valid is True

    def test_repr(self) -> None:
        """Vérifie __repr__."""
        validator = DatasetValidator(rules=[ColumnPresenceRule(["a"])])
        result = repr(validator)
        assert "DatasetValidator(" in result
        assert "rule_count=1" in result

    def test_messages_aggregated(self) -> None:
        """Vérifie que les messages de toutes les règles sont agrégés."""
        df = pd.DataFrame({"x": [1]})
        validator = DatasetValidator(
            rules=[
                ColumnPresenceRule(["a"]),
                ColumnPresenceRule(["b"]),
            ]
        )
        result = validator.validate(df)
        assert len(result.errors) == 2
