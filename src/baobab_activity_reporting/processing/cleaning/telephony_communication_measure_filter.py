"""Filtre des lignes téléphonie sur la mesure « Durée de communication »."""

from __future__ import annotations

import logging

import pandas as pd

from baobab_activity_reporting.processing.kpi.consolidated_data_schema import (
    ConsolidatedDataSchema,
)

logger = logging.getLogger(__name__)


def filter_communication_duration_rows(
    dataframe: pd.DataFrame,
    *,
    measure_column: str = ConsolidatedDataSchema.COL_MEASURE_NAMES,
    measure_value: str = ConsolidatedDataSchema.MEASURE_COMMUNICATION_DURATION,
) -> tuple[pd.DataFrame, int]:
    """Ne conserve que les lignes dont la mesure est la durée de communication.

    Les exports téléphoniques combinent plusieurs types de mesures par appel
    (mise en garde, communication, etc.) : les indicateurs doivent s'appuyer
    sur une seule mesure pour éviter les doubles comptages.

    Si ``measure_column`` est absente, les données sont renvoyées telles quelles
    (compatibilité avec d'anciens gabarits CSV) et aucune ligne n'est exclue.

    :param dataframe: Données après standardisation (ou brutes équivalentes).
    :type dataframe: pd.DataFrame
    :param measure_column: Colonne des libellés de mesure.
    :type measure_column: str
    :param measure_value: Valeur à conserver (égalité stricte après strip).
    :type measure_value: str
    :return: ``(dataframe filtré, nombre de lignes exclues)``.
    :rtype: tuple[pd.DataFrame, int]
    """
    if len(dataframe) == 0:
        return dataframe.copy(), 0

    cols = set(dataframe.columns.astype(str))
    if measure_column not in cols:
        logger.warning(
            "Colonne '%s' absente : filtre mesure téléphonie non appliqué",
            measure_column,
        )
        return dataframe.copy(), 0

    series = dataframe[measure_column].astype("string").fillna("").str.strip()
    target = measure_value.strip()
    mask = series == target
    excluded = int((~mask).sum())
    result: pd.DataFrame = dataframe.loc[mask].copy()
    if excluded:
        logger.info(
            "Filtre téléphonie '%s'=%r : %d lignes conservées, %d exclues",
            measure_column,
            measure_value,
            len(result),
            excluded,
        )
    return result, excluded
