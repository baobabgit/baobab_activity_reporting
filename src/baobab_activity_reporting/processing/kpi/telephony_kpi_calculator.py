"""Module de calcul des KPI d'activité téléphonique."""

import logging
import re
from datetime import timedelta

import pandas as pd

from baobab_activity_reporting.domain.models.kpi import Kpi
from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.exceptions.kpi_computation_error import (
    KpiComputationError,
)
from baobab_activity_reporting.processing.kpi.consolidated_data_schema import (
    ConsolidatedDataSchema,
)

logger = logging.getLogger(__name__)


def _duration_cell_to_seconds(  # pylint: disable=too-many-return-statements
    value: object,
) -> float:
    """Interprète une cellule de durée vers des secondes.

    :param value: Valeur brute (nombre, texte, durée HH:MM:SS, MM:SS).
    :type value: object
    :return: Secondes ou ``nan`` si non convertible.
    :rtype: float
    """
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return float("nan")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    text = str(value).strip()
    if not text:
        return float("nan")
    num_try = pd.to_numeric(text, errors="coerce")
    if pd.notna(num_try):
        return float(num_try)
    match = re.match(r"^(\d+):(\d{2}):(\d{2})$", text)
    if match:
        hours, minutes, seconds = (int(match.group(i)) for i in (1, 2, 3))
        delta = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        return float(delta.total_seconds())
    match2 = re.match(r"^(\d+):(\d{2})$", text)
    if match2:
        minutes, seconds = int(match2.group(1)), int(match2.group(2))
        delta = timedelta(minutes=minutes, seconds=seconds)
        return float(delta.total_seconds())
    return float("nan")


class TelephonyKpiCalculator:
    """Calcule les indicateurs globaux à partir des appels entrants et sortants.

    Les DataFrames fournis doivent déjà être filtrés sur la période voulue.
    Les durées peuvent être numériques (secondes) ou textuelles ``HH:MM:SS``.

    :param duration_column_candidates: Colonnes possibles pour la durée.
    :type duration_column_candidates: tuple[str, ...]

    :Example:
        >>> import pandas as pd
        >>> from datetime import date
        >>> from baobab_activity_reporting.domain.models.reporting_period import (
        ...     ReportingPeriod,
        ... )
        >>> from baobab_activity_reporting.processing.kpi.telephony_kpi_calculator import (
        ...     TelephonyKpiCalculator,
        ... )
        >>> inc = pd.DataFrame({"Durée": [60.0]})
        >>> out = pd.DataFrame()
        >>> p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        >>> rows = TelephonyKpiCalculator().compute(inc, out, p)
        >>> any(t[0].code == "telephony.incoming.count" for t in rows)
        True
    """

    def __init__(
        self,
        duration_column_candidates: tuple[str, ...] = (
            ConsolidatedDataSchema.COL_DURATION,
            "duree",
            "duration",
            "Valeurs de mesures",
        ),
    ) -> None:
        """Initialise le calculateur téléphonie.

        :param duration_column_candidates: Noms possibles pour la durée.
        :type duration_column_candidates: tuple[str, ...]
        """
        self.duration_column_candidates: tuple[str, ...] = duration_column_candidates

    @staticmethod
    def duration_series_to_seconds(series: pd.Series) -> pd.Series:
        """Convertit une série de durées hétérogènes en secondes (float).

        :param series: Valeurs brutes de durée.
        :type series: pd.Series
        :return: Secondes, ``NaN`` si valeur non interprétable.
        :rtype: pd.Series
        """
        numeric = pd.to_numeric(series, errors="coerce")
        if numeric.notna().any():
            return numeric.astype(float)
        return series.map(_duration_cell_to_seconds)

    def resolve_duration_column(self, dataframe: pd.DataFrame) -> str:
        """Retourne la colonne durée si elle existe.

        :param dataframe: Appels entrants ou sortants.
        :type dataframe: pd.DataFrame
        :return: Nom de colonne durée.
        :rtype: str
        :raises KpiComputationError: Si aucune colonne ne correspond.
        """
        cols = set(dataframe.columns.astype(str))
        for name in self.duration_column_candidates:
            if name in cols:
                return name
        raise KpiComputationError(
            "Colonne de durée introuvable pour les KPI téléphonie",
            details=f"candidats={list(self.duration_column_candidates)}",
        )

    def compute(  # pylint: disable=too-many-locals
        self,
        incoming: pd.DataFrame,
        outgoing: pd.DataFrame,
        period: ReportingPeriod,
    ) -> list[tuple[Kpi, str | None, str | None, str | None]]:
        """Calcule les KPI globaux de téléphonie pour la période donnée.

        :param incoming: Appels entrants filtrés.
        :type incoming: pd.DataFrame
        :param outgoing: Appels sortants filtrés.
        :type outgoing: pd.DataFrame
        :param period: Période (utilisée pour cohérence d'API ; réservé).
        :type period: ReportingPeriod
        :return: Liste de tuples ``(kpi, site, agent, canal)`` avec dimensions
            nulles au niveau global.
        :rtype: list[tuple[Kpi, str | None, str | None, str | None]]
        """
        _ = period
        results: list[tuple[Kpi, str | None, str | None, str | None]] = []

        inc_n = len(incoming)
        out_n = len(outgoing)

        def _trip(k: Kpi) -> tuple[Kpi, str | None, str | None, str | None]:
            return (k, None, None, None)

        results.append(
            _trip(
                Kpi(
                    "telephony.incoming.count",
                    "Nombre d'appels entrants",
                    float(inc_n),
                    "appels",
                )
            )
        )
        results.append(
            _trip(
                Kpi(
                    "telephony.outgoing.count",
                    "Nombre d'appels sortants",
                    float(out_n),
                    "appels",
                )
            )
        )

        inc_seconds = 0.0
        if inc_n > 0:
            dur_col = self.resolve_duration_column(incoming)
            sec = self.duration_series_to_seconds(incoming[dur_col])
            inc_seconds = float(sec.fillna(0.0).sum())

        out_seconds = 0.0
        if out_n > 0:
            dur_col_o = self.resolve_duration_column(outgoing)
            sec_o = self.duration_series_to_seconds(outgoing[dur_col_o])
            out_seconds = float(sec_o.fillna(0.0).sum())

        results.append(
            _trip(
                Kpi(
                    "telephony.incoming.duration_seconds.sum",
                    "Durée totale des appels entrants",
                    inc_seconds,
                    "s",
                )
            )
        )
        results.append(
            _trip(
                Kpi(
                    "telephony.outgoing.duration_seconds.sum",
                    "Durée totale des appels sortants",
                    out_seconds,
                    "s",
                )
            )
        )

        inc_avg = inc_seconds / inc_n if inc_n > 0 else 0.0
        out_avg = out_seconds / out_n if out_n > 0 else 0.0
        results.append(
            _trip(
                Kpi(
                    "telephony.incoming.duration_seconds.avg",
                    "Durée moyenne des appels entrants",
                    float(inc_avg),
                    "s",
                )
            )
        )
        results.append(
            _trip(
                Kpi(
                    "telephony.outgoing.duration_seconds.avg",
                    "Durée moyenne des appels sortants",
                    float(out_avg),
                    "s",
                )
            )
        )

        logger.info(
            "TelephonyKpiCalculator: %d KPI calculés (entrants=%d, sortants=%d)",
            len(results),
            inc_n,
            out_n,
        )
        return results
