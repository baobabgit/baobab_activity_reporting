"""Cas d'usage : construction du ReportModel et export documentaire optionnel."""

from __future__ import annotations

import logging

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.processing.kpi.period_aggregator import (
    PeriodAggregator,
)
from baobab_activity_reporting.reporting.report_builder import ReportBuilder
from baobab_activity_reporting.reporting.report_context import ReportContext
from baobab_activity_reporting.reporting.report_definition import ReportDefinition
from baobab_activity_reporting.reporting.report_model import ReportModel
from baobab_activity_reporting.reporting.writers.docx_writer import DocxWriter
from baobab_activity_reporting.reporting.writers.markdown_writer import (
    MarkdownWriter,
)
from baobab_activity_reporting.storage.repositories.kpi_repository import (
    KpiRepository,
)

logger = logging.getLogger(__name__)


class GenerateReportUseCase:
    """Charge les KPI de période, construit le modèle et écrit les fichiers demandés.

    :param kpi_repository: Source des enregistrements KPI.
    :type kpi_repository: KpiRepository
    :param report_builder: Orchestrateur de :class:`ReportModel` (injectable).
    :type report_builder: ReportBuilder | None
    """

    def __init__(
        self,
        kpi_repository: KpiRepository,
        report_builder: ReportBuilder | None = None,
    ) -> None:
        """Initialise le cas d'usage.

        :param kpi_repository: Repository des KPI.
        :type kpi_repository: KpiRepository
        :param report_builder: Builder de rapport, défaut si ``None``.
        :type report_builder: ReportBuilder | None
        """
        self._kpi: KpiRepository = kpi_repository
        self._builder: ReportBuilder = (
            report_builder if report_builder is not None else ReportBuilder()
        )

    def execute(
        self,
        reporting_period: ReportingPeriod,
        definition: ReportDefinition,
        *,
        markdown_path: str | None = None,
        docx_path: str | None = None,
    ) -> ReportModel:
        """Construit le rapport et exporte éventuellement en MD / DOCX.

        :param reporting_period: Période du rapport.
        :type reporting_period: ReportingPeriod
        :param definition: Gabarit et sections.
        :type definition: ReportDefinition
        :param markdown_path: Fichier Markdown de sortie (optionnel).
        :type markdown_path: str | None
        :param docx_path: Fichier Word de sortie (optionnel).
        :type docx_path: str | None
        :return: Modèle documentaire produit.
        :rtype: ReportModel
        """
        period_agg = PeriodAggregator()
        start_iso, end_iso = period_agg.period_to_iso_bounds(reporting_period)
        records = self._kpi.load_for_period(start_iso, end_iso)
        context = ReportContext(reporting_period, records)
        model = self._builder.build(definition, context)
        if markdown_path is not None:
            MarkdownWriter().write(model, markdown_path)
        if docx_path is not None:
            DocxWriter().write(model, docx_path)
        logger.info(
            "GenerateReportUseCase terminé : type=%s, md=%s, docx=%s",
            definition.report_type,
            markdown_path,
            docx_path,
        )
        return model
