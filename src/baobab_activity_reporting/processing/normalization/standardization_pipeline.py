"""Module contenant le pipeline de standardisation."""

import logging

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
from baobab_activity_reporting.processing.normalization.value_standardizer import (
    ValueStandardizer,
)

logger = logging.getLogger(__name__)


class StandardizationPipeline:
    """Pipeline orchestrant les étapes de standardisation.

    Enchaîne le mapping de colonnes, le nettoyage, la
    normalisation des types et l'uniformisation des valeurs
    dans un ordre déterministe.

    :param column_mapper: Mapper de colonnes (optionnel).
    :type column_mapper: ColumnMapper | None
    :param data_cleaner: Nettoyeur de données (optionnel).
    :type data_cleaner: DataCleaner | None
    :param type_normalizer: Normaliseur de types (optionnel).
    :type type_normalizer: DataTypeNormalizer | None
    :param value_standardizer: Standardiseur de valeurs (optionnel).
    :type value_standardizer: ValueStandardizer | None

    :Example:
        >>> pipeline = StandardizationPipeline(
        ...     column_mapper=ColumnMapper({"Date": "date"}),
        ...     data_cleaner=DataCleaner(),
        ... )
        >>> df_out = pipeline.run(df_in)
    """

    def __init__(
        self,
        column_mapper: ColumnMapper | None = None,
        data_cleaner: DataCleaner | None = None,
        type_normalizer: DataTypeNormalizer | None = None,
        value_standardizer: ValueStandardizer | None = None,
    ) -> None:
        """Initialise le pipeline de standardisation.

        :param column_mapper: Mapper de colonnes.
        :type column_mapper: ColumnMapper | None
        :param data_cleaner: Nettoyeur de données.
        :type data_cleaner: DataCleaner | None
        :param type_normalizer: Normaliseur de types.
        :type type_normalizer: DataTypeNormalizer | None
        :param value_standardizer: Standardiseur de valeurs.
        :type value_standardizer: ValueStandardizer | None
        """
        self.column_mapper: ColumnMapper | None = column_mapper
        self.data_cleaner: DataCleaner | None = data_cleaner
        self.type_normalizer: DataTypeNormalizer | None = type_normalizer
        self.value_standardizer: ValueStandardizer | None = value_standardizer

    def run(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Exécute le pipeline de standardisation complet.

        Les étapes sont exécutées dans l'ordre suivant :
        mapping → nettoyage → normalisation des types →
        uniformisation des valeurs.

        :param dataframe: DataFrame source.
        :type dataframe: pd.DataFrame
        :return: DataFrame standardisé.
        :rtype: pd.DataFrame
        """
        result = dataframe
        logger.info("Démarrage du pipeline de standardisation")

        if self.column_mapper is not None:
            result = self.column_mapper.apply(result)

        if self.data_cleaner is not None:
            result = self.data_cleaner.apply(result)

        if self.type_normalizer is not None:
            result = self.type_normalizer.apply(result)

        if self.value_standardizer is not None:
            result = self.value_standardizer.apply(result)

        logger.info("Pipeline de standardisation terminé")
        return result

    def __repr__(self) -> str:
        """Retourne une représentation technique du pipeline.

        :return: Représentation technique.
        :rtype: str
        """
        steps = []
        if self.column_mapper is not None:
            steps.append("column_mapper")
        if self.data_cleaner is not None:
            steps.append("data_cleaner")
        if self.type_normalizer is not None:
            steps.append("type_normalizer")
        if self.value_standardizer is not None:
            steps.append("value_standardizer")
        return f"StandardizationPipeline(steps={steps})"
