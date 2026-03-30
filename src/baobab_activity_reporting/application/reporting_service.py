"""Façade applicative exposant import, calcul KPI et génération de rapport."""

from __future__ import annotations

import logging
from typing import Any

from baobab_activity_reporting.application.compute_metrics_use_case import (
    ComputeMetricsUseCase,
)
from baobab_activity_reporting.application.generate_report_use_case import (
    GenerateReportUseCase,
)
from baobab_activity_reporting.application.import_sources_use_case import (
    ImportSourcesUseCase,
)
from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.processing.normalization.standardization_pipeline import (
    StandardizationPipeline,
)
from baobab_activity_reporting.reporting.report_definition import ReportDefinition
from baobab_activity_reporting.reporting.report_model import ReportModel
from baobab_activity_reporting.storage.repositories.kpi_repository import (
    KpiRepository,
)
from baobab_activity_reporting.storage.repositories.prepared_data_repository import (
    PreparedDataRepository,
)
from baobab_activity_reporting.storage.repositories.raw_data_repository import (
    RawDataRepository,
)
from baobab_activity_reporting.storage.sqlite.database_session_manager import (
    DatabaseSessionManager,
)

logger = logging.getLogger(__name__)


class ReportingService:
    """Point d'entrée unique pour enchaîner les cas d'usage sur une base SQLite.

    :param database_path: Chemin fichier SQLite ou ``:memory:``.
    :type database_path: str
    :param standardization_pipeline: Pipeline appliqué à l'import (injectable).
    :type standardization_pipeline: StandardizationPipeline | None
    """

    def __init__(
        self,
        database_path: str,
        *,
        standardization_pipeline: StandardizationPipeline | None = None,
    ) -> None:
        """Ouvre la session SQLite et compose les cas d'usage.

        :param database_path: Cible SQLite.
        :type database_path: str
        :param standardization_pipeline: Standardisation à l'import, défaut si ``None``.
        :type standardization_pipeline: StandardizationPipeline | None
        """
        self._session: DatabaseSessionManager = DatabaseSessionManager(database_path)
        self._raw: RawDataRepository = RawDataRepository(self._session)
        self._prepared: PreparedDataRepository = PreparedDataRepository(self._session)
        self._kpi: KpiRepository = KpiRepository(self._session)
        std = (
            standardization_pipeline
            if standardization_pipeline is not None
            else StandardizationPipeline()
        )
        self._import_uc = ImportSourcesUseCase(
            self._raw,
            self._prepared,
            std,
        )
        self._compute_uc = ComputeMetricsUseCase(self._prepared, self._kpi)
        self._generate_uc = GenerateReportUseCase(self._kpi)

    def close(self) -> None:
        """Ferme proprement la connexion SQLite.

        :rtype: None
        """
        self._session.close()

    def import_sources(
        self,
        incoming_csv_path: str,
        outgoing_csv_path: str,
        tickets_csv_path: str,
    ) -> dict[str, Any]:
        """Voir :meth:`ImportSourcesUseCase.execute`.

        :param incoming_csv_path: CSV appels entrants.
        :type incoming_csv_path: str
        :param outgoing_csv_path: CSV appels sortants.
        :type outgoing_csv_path: str
        :param tickets_csv_path: CSV tickets.
        :type tickets_csv_path: str
        :return: Résumé d'import.
        :rtype: dict[str, Any]
        """
        logger.info("ReportingService.import_sources")
        return self._import_uc.execute(
            incoming_csv_path,
            outgoing_csv_path,
            tickets_csv_path,
        )

    def compute_metrics(
        self,
        reporting_period: ReportingPeriod,
        *,
        clear_existing_for_period: bool = False,
    ) -> dict[str, Any]:
        """Voir :meth:`ComputeMetricsUseCase.execute`.

        :param reporting_period: Période de calcul.
        :type reporting_period: ReportingPeriod
        :param clear_existing_for_period: Effacer les KPI de cette période avant calcul.
        :type clear_existing_for_period: bool
        :return: Résumé du pipeline KPI.
        :rtype: dict[str, Any]
        """
        logger.info("ReportingService.compute_metrics")
        return self._compute_uc.execute(
            reporting_period,
            clear_existing_for_period=clear_existing_for_period,
        )

    def generate_report(
        self,
        reporting_period: ReportingPeriod,
        definition: ReportDefinition,
        *,
        markdown_path: str | None = None,
        docx_path: str | None = None,
    ) -> ReportModel:
        """Voir :meth:`GenerateReportUseCase.execute`.

        :param reporting_period: Période du rapport.
        :type reporting_period: ReportingPeriod
        :param definition: Type et sections du rapport.
        :type definition: ReportDefinition
        :param markdown_path: Sortie Markdown optionnelle.
        :type markdown_path: str | None
        :param docx_path: Sortie DOCX optionnelle.
        :type docx_path: str | None
        :return: Modèle produit.
        :rtype: ReportModel
        """
        logger.info("ReportingService.generate_report")
        return self._generate_uc.execute(
            reporting_period,
            definition,
            markdown_path=markdown_path,
            docx_path=docx_path,
        )

    @property
    def session_manager(self) -> DatabaseSessionManager:
        """Exposition du gestionnaire de session pour les tests avancés.

        :return: Session SQLite sous-jacente.
        :rtype: DatabaseSessionManager
        """
        return self._session
