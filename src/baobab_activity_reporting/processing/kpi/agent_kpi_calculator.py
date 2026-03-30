"""Module de calcul des KPI agrégés par agent."""

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


class AgentKpiCalculator:
    """Produit des :class:`Kpi` par agent pour la téléphonie et les tickets.

    :param activity_aggregator: Agrégateur pour résoudre les colonnes.
    :type activity_aggregator: ActivityAggregator
    :param telephony_calculator: Conversion des durées en secondes.
    :type telephony_calculator: TelephonyKpiCalculator

    :Example:
        >>> import pandas as pd
        >>> from baobab_activity_reporting.processing.kpi.activity_aggregator import (
        ...     ActivityAggregator,
        ... )
        >>> from baobab_activity_reporting.processing.kpi.telephony_kpi_calculator import (
        ...     TelephonyKpiCalculator,
        ... )
        >>> from baobab_activity_reporting.processing.kpi.agent_kpi_calculator import (
        ...     AgentKpiCalculator,
        ... )
        >>> inc = pd.DataFrame(
        ...     {"Agent": ["A1"], "Durée": [5.0]},
        ... )
        >>> calc = AgentKpiCalculator(ActivityAggregator(), TelephonyKpiCalculator())
        >>> rows = calc.compute(inc, pd.DataFrame(), pd.DataFrame())
        >>> any("agent" in t[0].code for t in rows)
        True
    """

    def __init__(
        self,
        activity_aggregator: ActivityAggregator,
        telephony_calculator: TelephonyKpiCalculator,
    ) -> None:
        """Initialise le calculateur par agent.

        :param activity_aggregator: Agrégateur d'activité.
        :type activity_aggregator: ActivityAggregator
        :param telephony_calculator: Calculateur téléphonie.
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
        """Calcule des KPI par agent pour appels et tickets.

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
            agent_col = self.activity_aggregator.resolve_agent_column(incoming)
            dur_col = self.telephony_calculator.resolve_duration_column(incoming)
            sec = self.telephony_calculator.duration_series_to_seconds(incoming[dur_col])
            inc = incoming.assign(_sec=sec.fillna(0.0))
            grouped = inc.groupby(agent_col, dropna=False)["_sec"].agg(["count", "sum"])
            for agent_key, row in grouped.iterrows():
                agent_label = str(agent_key)
                count = float(row["count"])
                sum_sec = float(row["sum"])
                avg = sum_sec / count if count > 0 else 0.0
                base = f"agent.{agent_label}.telephony.incoming"
                results.append(
                    (
                        Kpi(
                            f"{base}.count",
                            f"Appels entrants — agent {agent_label}",
                            count,
                            "appels",
                        ),
                        None,
                        agent_label,
                        None,
                    )
                )
                results.append(
                    (
                        Kpi(
                            f"{base}.duration_seconds.sum",
                            f"Durée totale appels entrants — agent {agent_label}",
                            sum_sec,
                            "s",
                        ),
                        None,
                        agent_label,
                        None,
                    )
                )
                results.append(
                    (
                        Kpi(
                            f"{base}.duration_seconds.avg",
                            f"Durée moyenne appels entrants — agent {agent_label}",
                            float(avg),
                            "s",
                        ),
                        None,
                        agent_label,
                        None,
                    )
                )

        if len(outgoing) > 0:
            agent_col_o = self.activity_aggregator.resolve_agent_column(outgoing)
            dur_col_o = self.telephony_calculator.resolve_duration_column(outgoing)
            sec_o = self.telephony_calculator.duration_series_to_seconds(outgoing[dur_col_o])
            out = outgoing.assign(_sec=sec_o.fillna(0.0))
            grouped_o = out.groupby(agent_col_o, dropna=False)["_sec"].agg(["count", "sum"])
            for agent_key, row in grouped_o.iterrows():
                agent_label = str(agent_key)
                count = float(row["count"])
                sum_sec = float(row["sum"])
                avg = sum_sec / count if count > 0 else 0.0
                base = f"agent.{agent_label}.telephony.outgoing"
                results.append(
                    (
                        Kpi(
                            f"{base}.count",
                            f"Appels sortants — agent {agent_label}",
                            count,
                            "appels",
                        ),
                        None,
                        agent_label,
                        None,
                    )
                )
                results.append(
                    (
                        Kpi(
                            f"{base}.duration_seconds.sum",
                            f"Durée totale appels sortants — agent {agent_label}",
                            sum_sec,
                            "s",
                        ),
                        None,
                        agent_label,
                        None,
                    )
                )
                results.append(
                    (
                        Kpi(
                            f"{base}.duration_seconds.avg",
                            f"Durée moyenne appels sortants — agent {agent_label}",
                            float(avg),
                            "s",
                        ),
                        None,
                        agent_label,
                        None,
                    )
                )

        if len(tickets) > 0:
            agent_col_t = self.activity_aggregator.resolve_agent_column(tickets)
            counts = tickets.groupby(agent_col_t, dropna=False).size()
            for agent_key, count in counts.items():
                agent_label = str(agent_key)
                results.append(
                    (
                        Kpi(
                            f"agent.{agent_label}.tickets.count",
                            f"Nombre de tickets — agent {agent_label}",
                            float(count),
                            "tickets",
                        ),
                        None,
                        agent_label,
                        None,
                    )
                )

        logger.info("AgentKpiCalculator: %d KPI par agent générés", len(results))
        return results
