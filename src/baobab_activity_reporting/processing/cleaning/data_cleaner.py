"""Module contenant le composant de nettoyage des données."""

import logging

import pandas as pd

logger = logging.getLogger(__name__)


class DataCleaner:
    """Nettoie les chaînes de caractères d'un DataFrame.

    Supprime les espaces parasites en début et fin de chaîne,
    normalise la casse et gère les valeurs manquantes sur
    les colonnes de type texte.

    :param strip_whitespace: Supprime les espaces en début/fin.
    :type strip_whitespace: bool
    :param normalize_case: Mode de normalisation de casse
        (``None``, ``"lower"``, ``"upper"``, ``"title"``).
    :type normalize_case: str | None

    :Example:
        >>> cleaner = DataCleaner(strip_whitespace=True)
        >>> df_out = cleaner.apply(df_in)
    """

    def __init__(
        self,
        strip_whitespace: bool = True,
        normalize_case: str | None = None,
    ) -> None:
        """Initialise le nettoyeur de données.

        :param strip_whitespace: Active le strip des espaces.
        :type strip_whitespace: bool
        :param normalize_case: Mode de casse à appliquer.
        :type normalize_case: str | None
        """
        self.strip_whitespace: bool = strip_whitespace
        self.normalize_case: str | None = normalize_case

    def apply(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Applique le nettoyage sur toutes les colonnes texte.

        :param dataframe: DataFrame source.
        :type dataframe: pd.DataFrame
        :return: DataFrame nettoyé.
        :rtype: pd.DataFrame
        """
        result: pd.DataFrame = dataframe.copy()
        str_cols = result.select_dtypes(include=["object"]).columns

        for col in str_cols:
            if self.strip_whitespace:
                result[col] = result[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
            if self.normalize_case == "lower":
                result[col] = result[col].apply(lambda x: x.lower() if isinstance(x, str) else x)
            elif self.normalize_case == "upper":
                result[col] = result[col].apply(lambda x: x.upper() if isinstance(x, str) else x)
            elif self.normalize_case == "title":
                result[col] = result[col].apply(lambda x: x.title() if isinstance(x, str) else x)

        logger.info(
            "Nettoyage appliqué sur %d colonnes texte",
            len(str_cols),
        )
        return result

    def __repr__(self) -> str:
        """Retourne une représentation technique du nettoyeur.

        :return: Représentation technique.
        :rtype: str
        """
        return (
            f"DataCleaner("
            f"strip_whitespace={self.strip_whitespace!r}, "
            f"normalize_case={self.normalize_case!r})"
        )
