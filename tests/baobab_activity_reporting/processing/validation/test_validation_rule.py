"""Tests unitaires pour ValidationRule."""

import pandas as pd
import pytest

from baobab_activity_reporting.domain.results.validation_result import (
    ValidationResult,
)
from baobab_activity_reporting.processing.validation.validation_rule import (
    ValidationRule,
)


class ConcreteRule(ValidationRule):
    """Implémentation concrète pour tester ValidationRule."""

    def evaluate(self, dataframe: pd.DataFrame) -> ValidationResult:
        """Retourne un résultat avec un message.

        :param dataframe: DataFrame à valider.
        :type dataframe: pd.DataFrame
        :return: Résultat de la validation.
        :rtype: ValidationResult
        """
        result = ValidationResult()
        if len(dataframe) == 0:
            result.add_error(self.code, "DataFrame vide")
        return result


class TestValidationRule:
    """Tests pour la classe ValidationRule."""

    def test_is_abstract(self) -> None:
        """Vérifie que ValidationRule ne peut pas être instanciée."""
        with pytest.raises(TypeError):
            ValidationRule(code="TEST", description="test")  # type: ignore[abstract]

    def test_concrete_can_be_instantiated(self) -> None:
        """Vérifie qu'une sous-classe concrète fonctionne."""
        rule = ConcreteRule(code="TEST", description="A test")
        assert rule.code == "TEST"
        assert rule.description == "A test"

    def test_evaluate_non_empty(self) -> None:
        """Vérifie l'évaluation sur un DataFrame non vide."""
        rule = ConcreteRule(code="TEST", description="test")
        df = pd.DataFrame({"a": [1]})
        result = rule.evaluate(df)
        assert result.is_valid is True

    def test_evaluate_empty(self) -> None:
        """Vérifie l'évaluation sur un DataFrame vide."""
        rule = ConcreteRule(code="TEST", description="test")
        df = pd.DataFrame()
        result = rule.evaluate(df)
        assert result.is_valid is False

    def test_repr(self) -> None:
        """Vérifie __repr__."""
        rule = ConcreteRule(code="T", description="d")
        result = repr(rule)
        assert "ValidationRule(" in result
        assert "code='T'" in result
