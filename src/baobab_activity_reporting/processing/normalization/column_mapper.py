"""Module contenant le composant de mapping de colonnes."""

import logging

import pandas as pd

from baobab_activity_reporting.exceptions.standardization_error import (
    StandardizationError,
)

logger = logging.getLogger(__name__)


class ColumnMapper:
    """Renomme les colonnes d'un DataFrame selon un dictionnaire de mapping.

    Permet d'harmoniser les noms de colonnes provenant de
    fichiers sources hétérogènes vers un schéma cible uniforme.

    :param mapping: Dictionnaire ``{ancien_nom: nouveau_nom}``.
    :type mapping: dict[str, str]

    :Example:
        >>> mapper = ColumnMapper({"Date": "date", "Agent": "agent"})
        >>> df_out = mapper.apply(df_in)
    """

    def __init__(self, mapping: dict[str, str]) -> None:
        """Initialise le mapper avec le dictionnaire de correspondance.

        :param mapping: Dictionnaire ``{ancien_nom: nouveau_nom}``.
        :type mapping: dict[str, str]
        """
        self.mapping: dict[str, str] = dict(mapping)

    def apply(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        """Applique le mapping de colonnes sur le DataFrame.

        Les colonnes absentes du DataFrame sont ignorées avec
        un avertissement. Les colonnes non présentes dans le
        mapping sont conservées telles quelles.

        :param dataframe: DataFrame source.
        :type dataframe: pd.DataFrame
        :return: DataFrame avec les colonnes renommées.
        :rtype: pd.DataFrame
        :raises StandardizationError: Si le DataFrame est vide.
        """
        if dataframe.columns.empty and len(dataframe) == 0:
            raise StandardizationError("DataFrame vide, mapping impossible")

        current_cols = set(dataframe.columns.astype(str))
        effective: dict[str, str] = {}
        for old_name, new_name in self.mapping.items():
            if old_name in current_cols:
                effective[old_name] = new_name
            else:
                logger.warning(
                    "Colonne '%s' absente, mapping ignoré",
                    old_name,
                )

        result: pd.DataFrame = dataframe.rename(columns=effective)
        logger.info(
            "Mapping appliqué : %d colonnes renommées",
            len(effective),
        )
        return result

    def __repr__(self) -> str:
        """Retourne une représentation technique du mapper.

        :return: Représentation technique.
        :rtype: str
        """
        return f"ColumnMapper(mapping_count={len(self.mapping)})"
