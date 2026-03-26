"""Module contenant le registre de schémas attendus par source."""

import logging

import pandas as pd

from baobab_activity_reporting.domain.results.validation_result import (
    ValidationResult,
)
from baobab_activity_reporting.processing.validation.validation_rule import (
    ValidationRule,
)

logger = logging.getLogger(__name__)


class ColumnPresenceRule(ValidationRule):
    """Règle vérifiant la présence de colonnes obligatoires.

    :param required_columns: Liste des colonnes requises.
    :type required_columns: list[str]
    """

    def __init__(self, required_columns: list[str]) -> None:
        """Initialise la règle de présence de colonnes.

        :param required_columns: Colonnes obligatoires.
        :type required_columns: list[str]
        """
        super().__init__(
            code="COL_PRESENCE",
            description="Vérifie la présence des colonnes obligatoires",
        )
        self.required_columns: list[str] = list(required_columns)

    def evaluate(self, dataframe: pd.DataFrame) -> ValidationResult:
        """Évalue la présence des colonnes.

        :param dataframe: DataFrame à valider.
        :type dataframe: pd.DataFrame
        :return: Résultat de la validation.
        :rtype: ValidationResult
        """
        result = ValidationResult()
        current = set(dataframe.columns.astype(str))
        for col in self.required_columns:
            if col not in current:
                result.add_error(
                    self.code,
                    f"Colonne obligatoire manquante : {col}",
                )
        return result


class NullRatioRule(ValidationRule):
    """Règle vérifiant le taux de valeurs nulles.

    :param columns: Colonnes à vérifier.
    :type columns: list[str]
    :param max_null_ratio: Taux maximal de nulls autorisé (0.0 à 1.0).
    :type max_null_ratio: float
    """

    def __init__(
        self,
        columns: list[str],
        max_null_ratio: float = 0.5,
    ) -> None:
        """Initialise la règle de taux de nulls.

        :param columns: Colonnes à contrôler.
        :type columns: list[str]
        :param max_null_ratio: Seuil maximal.
        :type max_null_ratio: float
        """
        super().__init__(
            code="NULL_RATIO",
            description="Vérifie le taux de valeurs nulles",
        )
        self.columns: list[str] = list(columns)
        self.max_null_ratio: float = max_null_ratio

    def evaluate(self, dataframe: pd.DataFrame) -> ValidationResult:
        """Évalue le taux de nulls sur les colonnes.

        :param dataframe: DataFrame à valider.
        :type dataframe: pd.DataFrame
        :return: Résultat de la validation.
        :rtype: ValidationResult
        """
        result = ValidationResult()
        if len(dataframe) == 0:
            return result
        current = set(dataframe.columns.astype(str))
        for col in self.columns:
            if col not in current:
                continue
            ratio = float(dataframe[col].isna().sum() / len(dataframe))
            if ratio > self.max_null_ratio:
                result.add_warning(
                    self.code,
                    f"Colonne '{col}' : {ratio:.1%} de nulls "
                    f"(seuil : {self.max_null_ratio:.1%})",
                )
        return result


class SchemaRegistry:
    """Registre de schémas attendus par type de source.

    Permet d'enregistrer, pour chaque type de source, la
    liste des colonnes obligatoires et les règles de qualité
    associées.

    :Example:
        >>> registry = SchemaRegistry()
        >>> registry.register(
        ...     "appels_entrants",
        ...     required_columns=["date", "agent"],
        ... )
        >>> rules = registry.get_rules("appels_entrants")
    """

    def __init__(self) -> None:
        """Initialise le registre de schémas."""
        self._schemas: dict[str, list[ValidationRule]] = {}

    def register(
        self,
        source_type: str,
        required_columns: list[str],
        null_check_columns: list[str] | None = None,
        max_null_ratio: float = 0.5,
    ) -> None:
        """Enregistre un schéma pour un type de source.

        :param source_type: Identifiant du type de source.
        :type source_type: str
        :param required_columns: Colonnes obligatoires.
        :type required_columns: list[str]
        :param null_check_columns: Colonnes à vérifier pour les nulls.
        :type null_check_columns: list[str] | None
        :param max_null_ratio: Seuil maximal de nulls.
        :type max_null_ratio: float
        """
        rules: list[ValidationRule] = [ColumnPresenceRule(required_columns)]
        if null_check_columns:
            rules.append(NullRatioRule(null_check_columns, max_null_ratio))
        self._schemas[source_type] = rules
        logger.info(
            "Schéma enregistré pour '%s' : %d règles",
            source_type,
            len(rules),
        )

    def get_rules(self, source_type: str) -> list[ValidationRule]:
        """Retourne les règles associées à un type de source.

        :param source_type: Identifiant du type de source.
        :type source_type: str
        :return: Liste des règles de validation.
        :rtype: list[ValidationRule]
        """
        return list(self._schemas.get(source_type, []))

    @property
    def registered_sources(self) -> list[str]:
        """Retourne la liste des sources enregistrées.

        :return: Liste des identifiants de source.
        :rtype: list[str]
        """
        return list(self._schemas.keys())

    def __repr__(self) -> str:
        """Retourne une représentation technique du registre.

        :return: Représentation technique.
        :rtype: str
        """
        return f"SchemaRegistry(" f"sources={self.registered_sources})"
