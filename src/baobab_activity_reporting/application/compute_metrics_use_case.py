"""Cas d'usage : calcul et persistance des KPI pour une période."""

from __future__ import annotations

import logging
from typing import Any

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.processing.kpi.kpi_computation_pipeline import (
    KpiComputationPipeline,
)
from baobab_activity_reporting.processing.kpi.period_aggregator import (
    PeriodAggregator,
)
from baobab_activity_reporting.storage.repositories.kpi_repository import (
    KpiRepository,
)
from baobab_activity_reporting.storage.repositories.prepared_data_repository import (
    PreparedDataRepository,
)

logger = logging.getLogger(__name__)


class ComputeMetricsUseCase:
    """Délègue au pipeline KPI : filtrage période, calculs, SQLite.

    :param prepared_data_repository: Données préparées ( trois sources ).
    :type prepared_data_repository: PreparedDataRepository
    :param kpi_repository: Cible de persistance des indicateurs.
    :type kpi_repository: KpiRepository
    """

    def __init__(
        self,
        prepared_data_repository: PreparedDataRepository,
        kpi_repository: KpiRepository,
    ) -> None:
        """Initialise le cas d'usage avec les repositories métier.

        :param prepared_data_repository: Repository des données préparées.
        :type prepared_data_repository: PreparedDataRepository
        :param kpi_repository: Repository des KPI.
        :type kpi_repository: KpiRepository
        """
        self._prepared: PreparedDataRepository = prepared_data_repository
        self._kpi: KpiRepository = kpi_repository

    def execute(
        self,
        reporting_period: ReportingPeriod,
        *,
        clear_existing_for_period: bool = False,
    ) -> dict[str, Any]:
        """Exécute le calcul KPI pour la période donnée.

        :param reporting_period: Période inclusive.
        :type reporting_period: ReportingPeriod
        :param clear_existing_for_period: Supprimer les KPI existants
            pour cette période avant insertion.
        :type clear_existing_for_period: bool
        :return: Résumé retourné par :meth:`KpiComputationPipeline.run`.
        :rtype: dict[str, Any]
        """
        pipeline = KpiComputationPipeline(
            self._prepared,
            self._kpi,
            reporting_period,
            clear_existing_for_period=clear_existing_for_period,
        )
        summary = pipeline.run()
        bounds = PeriodAggregator().period_to_iso_bounds(reporting_period)
        logger.info(
            "ComputeMetricsUseCase terminé : période %s → %s, %s KPI",
            bounds[0],
            bounds[1],
            summary.get("kpi_saved"),
        )
        return summary
