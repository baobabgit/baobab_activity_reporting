"""Module contenant le composant d'uniformisation des valeurs."""

import logging
import unicodedata

import pandas as pd

logger = logging.getLogger(__name__)


class ValueStandardizer:
    """Uniformise les valeurs textuelles d'un DataFrame.

    Harmonise les libellés d'agents, de sites et d'autres
    champs en normalisant accents, casse et espaces.

    :param columns: Colonnes sur lesquelles appliquer la standardisation.
    :type columns: list[str]
    :param strip_accents: Supprime les accents.
    :type strip_accents: bool
    :param to_upper: Convertit en majuscules.
    :type to_upper: bool

    :Example:
        >>> std = ValueStandardizer(columns=["agent", "site"])
        >>> df_out = std.apply(df_in)
    """

    def __init__(
        self,
        columns: list[str],
        strip_accents: bool = False,
        to_upper: bool = False,
    ) -> None:
        """Initialise le standardiseur de valeurs.

        :param columns: Colonnes cibles.
        :type columns: list[str]
        :param strip_accents: Active la suppression d'accents.
        :type strip_accents: bool
        :param to_upper: Active la conversion en majuscules.
        :type to_upper: bool
        """
        self.columns: list[str] = list(columns)
        self.strip_accents: bool = strip_accents
        self.to_upper: bool = to_upper

    @staticmethod
    def _remove_accents(text: str) -> str:
        """Supprime les accents d'une chaîne.

        :param text: Texte source.
        :type text: str
        :return: Texte sans accents.
        :rtype: str
        """
        nfkd = unicodedata.normalize("NFKD", text)
        return "".join(c for c in nfkd if not unicodedata.combining(c))

    def _standardize_value(self, value: object) -> object:
        """Standardise une valeur individuelle.

        :param value: Valeur à standardiser.
        :type value: object
        :return: Valeur standardisée.
        :rtype: object
        """
        if not isinstance(value, str):
            return value
        result = " ".join(value.split())
        if self.strip_accents:
            result = self._remove_accents(result)
        if self.to_upper:
            result = result.upper()
        return result

    def apply(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Applique la standardisation sur les colonnes configurées.

        :param dataframe: DataFrame source.
        :type dataframe: pd.DataFrame
        :return: DataFrame standardisé.
        :rtype: pd.DataFrame
        """
        result: pd.DataFrame = dataframe.copy()
        cols = set(result.columns.astype(str))

        for col in self.columns:
            if col not in cols:
                logger.warning(
                    "Colonne '%s' absente, standardisation ignorée",
                    col,
                )
                continue
            result[col] = result[col].map(self._standardize_value)
            logger.info("Colonne '%s' standardisée", col)

        return result

    def __repr__(self) -> str:
        """Retourne une représentation technique du standardiseur.

        :return: Représentation technique.
        :rtype: str
        """
        return (
            f"ValueStandardizer("
            f"columns={self.columns!r}, "
            f"strip_accents={self.strip_accents!r}, "
            f"to_upper={self.to_upper!r})"
        )
