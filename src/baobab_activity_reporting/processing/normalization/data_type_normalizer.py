"""Module contenant le composant de normalisation des types."""

import logging

import pandas as pd

from baobab_activity_reporting.exceptions.standardization_error import (
    StandardizationError,
)

logger = logging.getLogger(__name__)


class DataTypeNormalizer:
    """Normalise les types de colonnes d'un DataFrame.

    Convertit les colonnes vers les types cibles spécifiés :
    dates, entiers, flottants, chaînes.

    :param date_columns: Colonnes à convertir en ``datetime``.
    :type date_columns: list[str]
    :param int_columns: Colonnes à convertir en ``int``.
    :type int_columns: list[str]
    :param float_columns: Colonnes à convertir en ``float``.
    :type float_columns: list[str]
    :param date_format: Format de date pour le parsing.
    :type date_format: str | None

    :Example:
        >>> normalizer = DataTypeNormalizer(date_columns=["date"])
        >>> df_out = normalizer.apply(df_in)
    """

    def __init__(
        self,
        date_columns: list[str] | None = None,
        int_columns: list[str] | None = None,
        float_columns: list[str] | None = None,
        date_format: str | None = None,
    ) -> None:
        """Initialise le normaliseur de types.

        :param date_columns: Colonnes date.
        :type date_columns: list[str] | None
        :param int_columns: Colonnes entières.
        :type int_columns: list[str] | None
        :param float_columns: Colonnes flottantes.
        :type float_columns: list[str] | None
        :param date_format: Format de date explicite.
        :type date_format: str | None
        """
        self.date_columns: list[str] = list(date_columns) if date_columns else []
        self.int_columns: list[str] = list(int_columns) if int_columns else []
        self.float_columns: list[str] = list(float_columns) if float_columns else []
        self.date_format: str | None = date_format

    def apply(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Applique la normalisation des types sur le DataFrame.

        :param dataframe: DataFrame source.
        :type dataframe: pd.DataFrame
        :return: DataFrame avec les types normalisés.
        :rtype: pd.DataFrame
        :raises StandardizationError: Si une conversion échoue.
        """
        result: pd.DataFrame = dataframe.copy()
        cols = set(result.columns.astype(str))

        for col in self.date_columns:
            if col not in cols:
                continue
            try:
                result[col] = pd.to_datetime(result[col], format=self.date_format)
            except Exception as exc:
                raise StandardizationError(
                    "Conversion de date impossible",
                    column_name=col,
                    details=str(exc),
                ) from exc
            logger.info("Colonne '%s' convertie en datetime", col)

        for col in self.int_columns:
            if col not in cols:
                continue
            try:
                result[col] = pd.to_numeric(result[col], errors="raise").astype(int)
            except Exception as exc:
                raise StandardizationError(
                    "Conversion en entier impossible",
                    column_name=col,
                    details=str(exc),
                ) from exc
            logger.info("Colonne '%s' convertie en int", col)

        for col in self.float_columns:
            if col not in cols:
                continue
            try:
                result[col] = pd.to_numeric(result[col], errors="raise").astype(float)
            except Exception as exc:
                raise StandardizationError(
                    "Conversion en flottant impossible",
                    column_name=col,
                    details=str(exc),
                ) from exc
            logger.info("Colonne '%s' convertie en float", col)

        return result

    def __repr__(self) -> str:
        """Retourne une représentation technique du normaliseur.

        :return: Représentation technique.
        :rtype: str
        """
        return (
            f"DataTypeNormalizer("
            f"date_columns={self.date_columns!r}, "
            f"int_columns={self.int_columns!r}, "
            f"float_columns={self.float_columns!r})"
        )
