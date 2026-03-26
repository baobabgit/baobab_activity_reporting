"""Module contenant la règle de validation abstraite."""

from abc import ABC, abstractmethod

import pandas as pd

from baobab_activity_reporting.domain.results.validation_result import (
    ValidationResult,
)


class ValidationRule(ABC):
    """Règle de validation abstraite applicable à un DataFrame.

    Chaque règle encapsule un contrôle unitaire (présence
    d'une colonne, type attendu, taux de valeurs manquantes,
    etc.) et produit un :class:`ValidationResult`.

    :param code: Code unique identifiant la règle.
    :type code: str
    :param description: Description lisible de la règle.
    :type description: str

    :Example:
        >>> class MyRule(ValidationRule):
        ...     def evaluate(self, df):
        ...         return ValidationResult()
    """

    def __init__(self, code: str, description: str) -> None:
        """Initialise la règle de validation.

        :param code: Code unique de la règle.
        :type code: str
        :param description: Description de la règle.
        :type description: str
        """
        self.code: str = code
        self.description: str = description

    @abstractmethod
    def evaluate(self, dataframe: pd.DataFrame) -> ValidationResult:
        """Évalue la règle sur un DataFrame.

        :param dataframe: DataFrame à valider.
        :type dataframe: pd.DataFrame
        :return: Résultat de la validation.
        :rtype: ValidationResult
        """

    def __repr__(self) -> str:
        """Retourne une représentation technique de la règle.

        :return: Représentation technique.
        :rtype: str
        """
        return f"ValidationRule(code={self.code!r}, " f"description={self.description!r})"
