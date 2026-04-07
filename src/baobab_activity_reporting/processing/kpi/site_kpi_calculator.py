"""Module de calcul des KPI agrégés par site."""

import logging

import pandas as pd

from baobab_activity_reporting.domain.models.kpi import Kpi
from baobab_activity_reporting.processing.kpi.activity_aggregator import (
    ActivityAggregator,
)
from baobab_activity_reporting.processing.kpi.telephony_kpi_calculator import (
    TelephonyKpiCalculator,
)

logger = logging.getLogger(__name__)


class SiteKpiCalculator:
    """Produit des :class:`Kpi` par site pour appels et tickets.

    Attend des colonnes de site et, pour la téléphonie, une colonne de
    durée compatible avec :class:`TelephonyKpiCalculator`.

    :param activity_aggregator: Agrégateur utilisé pour les regroupements.
    :type activity_aggregator: ActivityAggregator
    :param telephony_calculator: Calculateur pour les durées par site.
    :type telephony_calculator: TelephonyKpiCalculator

    :Example:
        >>> import pandas as pd
        >>> from baobab_activity_reporting.processing.kpi.activity_aggregator import (
        ...     ActivityAggregator,
        ... )
        >>> from baobab_activity_reporting.processing.kpi.telephony_kpi_calculator import (
        ...     TelephonyKpiCalculator,
        ... )
        >>> from baobab_activity_reporting.processing.kpi.site_kpi_calculator import (
        ...     SiteKpiCalculator,
        ... )
        >>> inc = pd.DataFrame(
        ...     {"Site": ["S1"], "Durée": [10.0]},
        ... )
        >>> calc = SiteKpiCalculator(ActivityAggregator(), TelephonyKpiCalculator())
        >>> rows = calc.compute(inc, pd.DataFrame(), pd.DataFrame())
        >>> any("site" in t[0].code for t in rows)
        True
    """

    def __init__(
        self,
        activity_aggregator: ActivityAggregator,
        telephony_calculator: TelephonyKpiCalculator,
    ) -> None:
        """Initialise le calculateur par site.

        :param activity_aggregator: Agrégateur d'activité.
        :type activity_aggregator: ActivityAggregator
        :param telephony_calculator: Calculateur téléphonie (durées).
        :type telephony_calculator: TelephonyKpiCalculator
        """
        self.activity_aggregator: ActivityAggregator = activity_aggregator
        self.telephony_calculator: TelephonyKpiCalculator = telephony_calculator

    def compute(  # pylint: disable=too-many-locals
        self,
        incoming: pd.DataFrame,
        outgoing: pd.DataFrame,
        tickets: pd.DataFrame,
    ) -> list[tuple[Kpi, str | None, str | None, str | None]]:
        """Calcule des KPI par site pour les trois flux.

        :param incoming: Appels entrants filtrés.
        :type incoming: pd.DataFrame
        :param outgoing: Appels sortants filtrés.
        :type outgoing: pd.DataFrame
        :param tickets: Tickets filtrés.
        :type tickets: pd.DataFrame
        :return: Tuples ``(kpi, site, agent, canal)`` pour la persistance.
        :rtype: list[tuple[Kpi, str | None, str | None, str | None]]
        """
        results: list[tuple[Kpi, str | None, str | None, str | None]] = []

        if len(incoming) > 0:
            site_col = self.activity_aggregator.resolve_site_column(incoming)
            dur_col = self.telephony_calculator.resolve_duration_column(incoming)
            sec = self.telephony_calculator.duration_series_to_seconds(incoming[dur_col])
            inc = incoming.assign(_sec=sec.fillna(0.0))
            grouped = inc.groupby(site_col, dropna=False)["_sec"].agg(["count", "sum"])
            for site_key, row in grouped.iterrows():
                site_label = str(site_key)
                count = float(row["count"])
                sum_sec = float(row["sum"])
                avg = sum_sec / count if count > 0 else 0.0
                code_base = f"site.{site_label}.telephony.incoming"
                results.append(
                    (
                        Kpi(
                            f"{code_base}.count",
                            f"Appels entrants pour le site {site_label}",
                            count,
                            "appels",
                        ),
                        site_label,
                        None,
                        None,
                    )
                )
                results.append(
                    (
                        Kpi(
                            f"{code_base}.duration_seconds.sum",
                            f"Durée appels entrants — site {site_label}",
                            sum_sec,
                            "s",
                        ),
                        site_label,
                        None,
                        None,
                    )
                )
                results.append(
                    (
                        Kpi(
                            f"{code_base}.duration_seconds.avg",
                            f"Durée moyenne appels entrants — site {site_label}",
                            float(avg),
                            "s",
                        ),
                        site_label,
                        None,
                        None,
                    )
                )

        if len(outgoing) > 0:
            site_col_o = self.activity_aggregator.resolve_site_column_optional(outgoing)
            dur_col_o = self.telephony_calculator.resolve_duration_column(outgoing)
            sec_o = self.telephony_calculator.duration_series_to_seconds(outgoing[dur_col_o])
            if site_col_o is None:
                out = outgoing.assign(
                    _sec=sec_o.fillna(0.0),
                    _site_key="—",
                )
            else:
                out = outgoing.assign(
                    _sec=sec_o.fillna(0.0),
                    _site_key=outgoing[site_col_o].astype(str),
                )
            grouped_o = out.groupby("_site_key", dropna=False)["_sec"].agg(["count", "sum"])
            for site_key, row in grouped_o.iterrows():
                site_label = str(site_key)
                count = float(row["count"])
                sum_sec = float(row["sum"])
                avg = sum_sec / count if count > 0 else 0.0
                code_base = f"site.{site_label}.telephony.outgoing"
                results.append(
                    (
                        Kpi(
                            f"{code_base}.count",
                            f"Appels sortants pour le site {site_label}",
                            count,
                            "appels",
                        ),
                        site_label,
                        None,
                        None,
                    )
                )
                results.append(
                    (
                        Kpi(
                            f"{code_base}.duration_seconds.sum",
                            f"Durée appels sortants — site {site_label}",
                            sum_sec,
                            "s",
                        ),
                        site_label,
                        None,
                        None,
                    )
                )
                results.append(
                    (
                        Kpi(
                            f"{code_base}.duration_seconds.avg",
                            f"Durée moyenne appels sortants — site {site_label}",
                            float(avg),
                            "s",
                        ),
                        site_label,
                        None,
                        None,
                    )
                )

        if len(tickets) > 0:
            ch_col = self.activity_aggregator.resolve_channel_column(tickets)
            site_col_t = self.activity_aggregator.resolve_site_column(tickets)
            grouped_t = tickets.groupby([site_col_t, ch_col], dropna=False).size()
            frame_t = grouped_t.reset_index(name="_count")
            for _, row in frame_t.iterrows():
                site_label = str(row[site_col_t])
                channel_label = str(row[ch_col])
                count_val = float(row["_count"])
                results.append(
                    (
                        Kpi(
                            f"site.{site_label}.tickets.by_channel." f"{channel_label}.count",
                            f"Tickets canal {channel_label} — site {site_label}",
                            count_val,
                            "tickets",
                        ),
                        site_label,
                        None,
                        channel_label,
                    )
                )

        logger.info("SiteKpiCalculator: %d KPI par site générés", len(results))
        return results
