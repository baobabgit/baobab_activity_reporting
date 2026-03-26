"""Module contenant le validateur de jeu de données."""

import logging

import pandas as pd

from baobab_activity_reporting.domain.results.validation_result import (
    ValidationResult,
)
from baobab_activity_reporting.processing.validation.validation_rule import (
    ValidationRule,
)

logger = logging.getLogger(__name__)


class DatasetValidator:
    """Validateur de jeux de données par application de règles.

    Exécute séquentiellement une liste de
    :class:`ValidationRule` sur un DataFrame et agrège les
    résultats dans un unique :class:`ValidationResult`.

    :param rules: Liste des règles de validation.
    :type rules: list[ValidationRule]

    :Example:
        >>> validator = DatasetValidator(rules=[rule1, rule2])
        >>> result = validator.validate(df)
        >>> print(result.is_valid)
    """

    def __init__(self, rules: list[ValidationRule]) -> None:
        """Initialise le validateur avec ses règles.

        :param rules: Règles de validation à appliquer.
        :type rules: list[ValidationRule]
        """
        self.rules: list[ValidationRule] = list(rules)

    def validate(self, dataframe: pd.DataFrame) -> ValidationResult:
        """Valide un DataFrame en appliquant toutes les règles.

        :param dataframe: DataFrame à valider.
        :type dataframe: pd.DataFrame
        :return: Résultat agrégé de toutes les règles.
        :rtype: ValidationResult
        """
        aggregated = ValidationResult()
        logger.info(
            "Validation démarrée : %d règles à appliquer",
            len(self.rules),
        )

        for rule in self.rules:
            result = rule.evaluate(dataframe)
            aggregated.messages.extend(result.messages)
            logger.info(
                "Règle '%s' : %d messages",
                rule.code,
                len(result.messages),
            )

        logger.info(
            "Validation terminée : is_valid=%s, %d messages",
            aggregated.is_valid,
            len(aggregated.messages),
        )
        return aggregated

    def __repr__(self) -> str:
        """Retourne une représentation technique du validateur.

        :return: Représentation technique.
        :rtype: str
        """
        return f"DatasetValidator(rule_count={len(self.rules)})"
