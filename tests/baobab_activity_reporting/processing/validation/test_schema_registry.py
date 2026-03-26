"""Tests unitaires pour SchemaRegistry et règles associées."""

import pandas as pd

from baobab_activity_reporting.processing.validation.schema_registry import (
    ColumnPresenceRule,
    NullRatioRule,
    SchemaRegistry,
)


class TestColumnPresenceRule:
    """Tests pour la règle ColumnPresenceRule."""

    def test_all_columns_present(self) -> None:
        """Vérifie le succès quand toutes les colonnes sont présentes."""
        df = pd.DataFrame({"date": [1], "agent": [2]})
        rule = ColumnPresenceRule(["date", "agent"])
        result = rule.evaluate(df)
        assert result.is_valid is True
        assert len(result.errors) == 0

    def test_missing_column(self) -> None:
        """Vérifie l'erreur quand une colonne manque."""
        df = pd.DataFrame({"date": [1]})
        rule = ColumnPresenceRule(["date", "agent"])
        result = rule.evaluate(df)
        assert result.is_valid is False
        assert len(result.errors) == 1
        assert "agent" in result.errors[0].text

    def test_multiple_missing_columns(self) -> None:
        """Vérifie les erreurs pour plusieurs colonnes manquantes."""
        df = pd.DataFrame({"other": [1]})
        rule = ColumnPresenceRule(["date", "agent", "site"])
        result = rule.evaluate(df)
        assert len(result.errors) == 3

    def test_empty_required(self) -> None:
        """Vérifie avec aucune colonne requise."""
        df = pd.DataFrame({"a": [1]})
        rule = ColumnPresenceRule([])
        result = rule.evaluate(df)
        assert result.is_valid is True


class TestNullRatioRule:
    """Tests pour la règle NullRatioRule."""

    def test_no_nulls(self) -> None:
        """Vérifie le succès sans valeurs nulles."""
        df = pd.DataFrame({"agent": ["A", "B", "C"]})
        rule = NullRatioRule(columns=["agent"], max_null_ratio=0.5)
        result = rule.evaluate(df)
        assert result.is_valid is True
        assert len(result.warning_list) == 0

    def test_nulls_above_threshold(self) -> None:
        """Vérifie le warning quand le taux dépasse le seuil."""
        df = pd.DataFrame({"agent": [None, None, "C"]})
        rule = NullRatioRule(columns=["agent"], max_null_ratio=0.5)
        result = rule.evaluate(df)
        assert len(result.warning_list) == 1
        assert "agent" in result.warning_list[0].text

    def test_nulls_at_threshold(self) -> None:
        """Vérifie à la limite exacte du seuil."""
        df = pd.DataFrame({"agent": [None, "B"]})
        rule = NullRatioRule(columns=["agent"], max_null_ratio=0.5)
        result = rule.evaluate(df)
        assert len(result.warning_list) == 0

    def test_empty_dataframe(self) -> None:
        """Vérifie sur un DataFrame vide."""
        df = pd.DataFrame({"agent": pd.Series([], dtype="object")})
        rule = NullRatioRule(columns=["agent"])
        result = rule.evaluate(df)
        assert result.is_valid is True

    def test_missing_column_ignored(self) -> None:
        """Vérifie que les colonnes absentes sont ignorées."""
        df = pd.DataFrame({"other": [1]})
        rule = NullRatioRule(columns=["missing"])
        result = rule.evaluate(df)
        assert result.is_valid is True


class TestSchemaRegistry:
    """Tests pour la classe SchemaRegistry."""

    def test_register_and_get(self) -> None:
        """Vérifie l'enregistrement et la récupération d'un schéma."""
        registry = SchemaRegistry()
        registry.register("appels_entrants", required_columns=["date", "agent"])
        rules = registry.get_rules("appels_entrants")
        assert len(rules) == 1

    def test_register_with_null_check(self) -> None:
        """Vérifie l'enregistrement avec vérification de nulls."""
        registry = SchemaRegistry()
        registry.register(
            "tickets",
            required_columns=["date"],
            null_check_columns=["agent"],
            max_null_ratio=0.3,
        )
        rules = registry.get_rules("tickets")
        assert len(rules) == 2

    def test_get_unknown_source(self) -> None:
        """Vérifie le retour vide pour une source inconnue."""
        registry = SchemaRegistry()
        rules = registry.get_rules("unknown")
        assert rules == []

    def test_registered_sources(self) -> None:
        """Vérifie la liste des sources enregistrées."""
        registry = SchemaRegistry()
        registry.register("a", required_columns=[])
        registry.register("b", required_columns=[])
        assert sorted(registry.registered_sources) == ["a", "b"]

    def test_repr(self) -> None:
        """Vérifie __repr__."""
        registry = SchemaRegistry()
        registry.register("test", required_columns=[])
        result = repr(registry)
        assert "SchemaRegistry(" in result
        assert "test" in result

    def test_rules_are_independent_copies(self) -> None:
        """Vérifie que get_rules retourne une copie."""
        registry = SchemaRegistry()
        registry.register("src", required_columns=["a"])
        rules1 = registry.get_rules("src")
        rules2 = registry.get_rules("src")
        assert rules1 is not rules2
