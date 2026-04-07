"""Module d'agrégation et filtrage par période de reporting."""

import logging

import pandas as pd

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.exceptions.kpi_computation_error import (
    KpiComputationError,
)

logger = logging.getLogger(__name__)


class PeriodAggregator:
    """Filtre les données consolidées sur une :class:`ReportingPeriod`.

    Résout la colonne de date parmi des candidats connus, convertit en
    dates calendaires et applique un masque borné par la période.

    :param date_column_candidates: Ordre de préférence pour la colonne date.
    :type date_column_candidates: tuple[str, ...]

    :Example:
        >>> from datetime import date
        >>> from baobab_activity_reporting.domain.models.reporting_period import (
        ...     ReportingPeriod,
        ... )
        >>> agg = PeriodAggregator()
        >>> period = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        >>> df = pd.DataFrame({"Date": ["2026-01-15"], "x": [1]})
        >>> out = agg.filter_for_period(df, period)
        >>> len(out)
        1
    """

    def __init__(
        self,
        date_column_candidates: tuple[str, ...] = (
            "Date",
            "date",
            "Début d'appel",
            "Date-Heure Depot Formulaire",
        ),
    ) -> None:
        """Initialise l'agrégateur de période.

        :param date_column_candidates: Colonnes date essayées dans l'ordre.
        :type date_column_candidates: tuple[str, ...]
        """
        self.date_column_candidates: tuple[str, ...] = date_column_candidates

    def resolve_date_column(self, dataframe: pd.DataFrame) -> str:
        """Retourne le nom de la colonne date présente dans le DataFrame.

        :param dataframe: Données consolidées.
        :type dataframe: pd.DataFrame
        :return: Nom de colonne retenu.
        :rtype: str
        :raises KpiComputationError: Si aucune colonne candidate n'existe.
        """
        cols = set(dataframe.columns.astype(str))
        for candidate in self.date_column_candidates:
            if candidate in cols:
                return candidate
        raise KpiComputationError(
            "Colonne de date introuvable pour le filtrage par période",
            details=f"candidats={list(self.date_column_candidates)}",
        )

    def filter_for_period(
        self,
        dataframe: pd.DataFrame,
        period: ReportingPeriod,
        date_column: str | None = None,
    ) -> pd.DataFrame:
        """Restreint les lignes à la période ``[start_date, end_date]``.

        :param dataframe: Données à filtrer.
        :type dataframe: pd.DataFrame
        :param period: Période de reporting inclusive.
        :type period: ReportingPeriod
        :param date_column: Colonne date explicite, sinon résolution auto.
        :type date_column: str | None
        :return: Copie filtrée (vide si aucune ligne dans la période).
        :rtype: pd.DataFrame
        """
        if len(dataframe) == 0:
            logger.info("PeriodAggregator: DataFrame vide, rien à filtrer")
            empty_frame: pd.DataFrame = dataframe.copy()
            return empty_frame

        col = date_column if date_column is not None else self.resolve_date_column(dataframe)
        parsed = pd.to_datetime(dataframe[col], errors="coerce")
        start = period.start_date
        end = period.end_date
        dates_only = parsed.dt.date
        mask = (dates_only >= start) & (dates_only <= end) & parsed.notna()
        result: pd.DataFrame = dataframe.loc[mask].copy()
        logger.info(
            "PeriodAggregator: %d lignes sur %d conservées pour la période",
            len(result),
            len(dataframe),
        )
        return result

    @staticmethod
    def period_to_iso_bounds(period: ReportingPeriod) -> tuple[str, str]:
        """Convertit une période en bornes ISO 8601 (date seule).

        :param period: Période de reporting.
        :type period: ReportingPeriod
        :return: ``(period_start, period_end)`` au format ``YYYY-MM-DD``.
        :rtype: tuple[str, str]
        """
        return period.start_date.isoformat(), period.end_date.isoformat()
