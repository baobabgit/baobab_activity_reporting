"""Module du pipeline rejouable de calcul et persistance des KPI."""

import logging
from typing import Any

import pandas as pd

from baobab_activity_reporting.domain.models.kpi import Kpi
from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.processing.kpi.activity_aggregator import (
    ActivityAggregator,
)
from baobab_activity_reporting.processing.kpi.agent_kpi_calculator import (
    AgentKpiCalculator,
)
from baobab_activity_reporting.processing.kpi.consolidated_data_schema import (
    ConsolidatedDataSchema,
)
from baobab_activity_reporting.processing.kpi.period_aggregator import (
    PeriodAggregator,
)
from baobab_activity_reporting.processing.kpi.site_kpi_calculator import (
    SiteKpiCalculator,
)
from baobab_activity_reporting.processing.kpi.telephony_kpi_calculator import (
    TelephonyKpiCalculator,
)
from baobab_activity_reporting.storage.repositories.kpi_repository import (
    KpiRepository,
)
from baobab_activity_reporting.storage.repositories.prepared_data_repository import (
    PreparedDataRepository,
)

logger = logging.getLogger(__name__)


class KpiComputationPipeline:  # pylint: disable=too-many-instance-attributes
    """Orchestre chargement, filtrage, calculs KPI et persistance SQLite.

    Charge les trois sources préparées (appels entrants, sortants, tickets),
    applique le filtre de :class:`ReportingPeriod`, enchaîne les
    calculateurs puis enregistre chaque indicateur via :class:`KpiRepository`.

    :param prepared_data_repository: Accès aux données consolidées.
    :type prepared_data_repository: PreparedDataRepository
    :param kpi_repository: Persistance des métriques.
    :type kpi_repository: KpiRepository
    :param reporting_period: Période inclusive sur laquelle calculer.
    :type reporting_period: ReportingPeriod
    :param period_aggregator: Filtre temporel (injectable pour les tests).
    :type period_aggregator: PeriodAggregator | None
    :param activity_aggregator: Regroupements site / agent / canal.
    :type activity_aggregator: ActivityAggregator | None
    :param telephony_calculator: KPI téléphonie globaux.
    :type telephony_calculator: TelephonyKpiCalculator | None
    :param site_calculator: KPI par site.
    :type site_calculator: SiteKpiCalculator | None
    :param agent_calculator: KPI par agent.
    :type agent_calculator: AgentKpiCalculator | None
    :param clear_existing_for_period: Si ``True``, supprime les KPI de la
        même période avant insertion (rejouabilité).
    :type clear_existing_for_period: bool

    :Example:
        >>> from datetime import date
        >>> import pandas as pd
        >>> from baobab_activity_reporting.domain.models.reporting_period import (
        ...     ReportingPeriod,
        ... )
        >>> from baobab_activity_reporting.storage.sqlite.database_session_manager import (
        ...     DatabaseSessionManager,
        ... )
        >>> from baobab_activity_reporting.storage.repositories.prepared_data_repository import (
        ...     PreparedDataRepository,
        ... )
        >>> from baobab_activity_reporting.storage.repositories.kpi_repository import (
        ...     KpiRepository,
        ... )
        >>> from baobab_activity_reporting.processing.kpi.consolidated_data_schema import (
        ...     ConsolidatedDataSchema as S,
        ... )
        >>> mgr = DatabaseSessionManager(":memory:")
        >>> prep = PreparedDataRepository(mgr)
        >>> kpi = KpiRepository(mgr)
        >>> df = pd.DataFrame(
        ...     {"Date": ["2026-01-10"], "Durée": [1.0], "Site": ["X"], "Agent": ["A"]},
        ... )
        >>> prep.save(df, S.SOURCE_INCOMING_CALLS)
        >>> period = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        >>> pipe = KpiComputationPipeline(prep, kpi, period)
        >>> summary = pipe.run()
        >>> int(summary["kpi_saved"]) > 0
        True
    """

    def __init__(  # pylint: disable=too-many-arguments
        self,
        prepared_data_repository: PreparedDataRepository,
        kpi_repository: KpiRepository,
        reporting_period: ReportingPeriod,
        *,
        period_aggregator: PeriodAggregator | None = None,
        activity_aggregator: ActivityAggregator | None = None,
        telephony_calculator: TelephonyKpiCalculator | None = None,
        site_calculator: SiteKpiCalculator | None = None,
        agent_calculator: AgentKpiCalculator | None = None,
        clear_existing_for_period: bool = False,
    ) -> None:
        """Initialise le pipeline avec repositories et période.

        :param prepared_data_repository: Données préparées.
        :type prepared_data_repository: PreparedDataRepository
        :param kpi_repository: Cible de persistance des KPI.
        :type kpi_repository: KpiRepository
        :param reporting_period: Période de calcul.
        :type reporting_period: ReportingPeriod
        :param period_aggregator: Agrégateur de période.
        :type period_aggregator: PeriodAggregator | None
        :param activity_aggregator: Agrégateur site / agent / canal.
        :type activity_aggregator: ActivityAggregator | None
        :param telephony_calculator: Calculateur téléphonie.
        :type telephony_calculator: TelephonyKpiCalculator | None
        :param site_calculator: Calculateur par site.
        :type site_calculator: SiteKpiCalculator | None
        :param agent_calculator: Calculateur par agent.
        :type agent_calculator: AgentKpiCalculator | None
        :param clear_existing_for_period: Effacer la période avant insertion.
        :type clear_existing_for_period: bool
        """
        self._prepared_data_repository: PreparedDataRepository = prepared_data_repository
        self._kpi_repository: KpiRepository = kpi_repository
        self._reporting_period: ReportingPeriod = reporting_period
        self._period_aggregator: PeriodAggregator = (
            period_aggregator if period_aggregator is not None else PeriodAggregator()
        )
        self._activity_aggregator: ActivityAggregator = (
            activity_aggregator if activity_aggregator is not None else ActivityAggregator()
        )
        self._telephony_calculator: TelephonyKpiCalculator = (
            telephony_calculator if telephony_calculator is not None else TelephonyKpiCalculator()
        )
        self._site_calculator: SiteKpiCalculator = (
            site_calculator
            if site_calculator is not None
            else SiteKpiCalculator(
                self._activity_aggregator,
                self._telephony_calculator,
            )
        )
        self._agent_calculator: AgentKpiCalculator = (
            agent_calculator
            if agent_calculator is not None
            else AgentKpiCalculator(
                self._activity_aggregator,
                self._telephony_calculator,
            )
        )
        self._clear_existing_for_period: bool = clear_existing_for_period

    def run(self) -> dict[str, Any]:  # pylint: disable=too-many-locals
        """Exécute le calcul complet et persiste les KPI.

        :return: Résumé avec effectifs et bornes de période.
        :rtype: dict[str, Any]
        """
        schema = ConsolidatedDataSchema
        incoming_raw = self._prepared_data_repository.load(
            schema.SOURCE_INCOMING_CALLS,
        )
        outgoing_raw = self._prepared_data_repository.load(
            schema.SOURCE_OUTGOING_CALLS,
        )
        tickets_raw = self._prepared_data_repository.load(schema.SOURCE_TICKETS)

        incoming = self._period_aggregator.filter_for_period(
            incoming_raw,
            self._reporting_period,
        )
        outgoing = self._period_aggregator.filter_for_period(
            outgoing_raw,
            self._reporting_period,
        )
        tickets = self._period_aggregator.filter_for_period(
            tickets_raw,
            self._reporting_period,
        )

        period_start, period_end = self._period_aggregator.period_to_iso_bounds(
            self._reporting_period,
        )

        if self._clear_existing_for_period:
            self._kpi_repository.delete_for_period(period_start, period_end)

        rows: list[tuple[Kpi, str | None, str | None, str | None]] = []
        rows.extend(
            self._telephony_calculator.compute(
                incoming,
                outgoing,
                self._reporting_period,
            )
        )
        rows.extend(
            self._site_calculator.compute(incoming, outgoing, tickets),
        )
        rows.extend(
            self._agent_calculator.compute(incoming, outgoing, tickets),
        )
        rows.extend(self._period_level_channel_kpis(tickets))

        for kpi, site, agent, channel in rows:
            self._kpi_repository.save_kpi(
                kpi.code,
                kpi.label,
                kpi.value,
                kpi.unit,
                period_start,
                period_end,
                site=site,
                agent=agent,
                channel=channel,
            )

        summary: dict[str, Any] = {
            "period_start": period_start,
            "period_end": period_end,
            "kpi_saved": len(rows),
            "rows_incoming": len(incoming),
            "rows_outgoing": len(outgoing),
            "rows_tickets": len(tickets),
        }
        logger.info(
            "KpiComputationPipeline terminé : %s KPI enregistrés",
            summary["kpi_saved"],
        )
        return summary

    def _period_level_channel_kpis(
        self,
        tickets: pd.DataFrame,
    ) -> list[tuple[Kpi, str | None, str | None, str | None]]:
        """Compte les tickets par canal sur la période (ex. EFI, EDI).

        :param tickets: Tickets déjà filtrés sur la période.
        :type tickets: pd.DataFrame
        :return: KPI globaux avec canal renseigné.
        :rtype: list[tuple[Kpi, str | None, str | None, str | None]]
        """
        if len(tickets) == 0:
            return []
        counts = self._activity_aggregator.count_by_channel(tickets)
        results: list[tuple[Kpi, str | None, str | None, str | None]] = []
        for channel_key, count in counts.items():
            label = str(channel_key)
            results.append(
                (
                    Kpi(
                        f"tickets.channel.{label}.count",
                        f"Nombre de tickets par canal ({label})",
                        float(count),
                        "tickets",
                    ),
                    None,
                    None,
                    label,
                )
            )
        logger.info(
            "Canaux de tickets à la période : %d indicateurs",
            len(results),
        )
        return results
