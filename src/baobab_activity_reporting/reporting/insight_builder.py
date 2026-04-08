"""Orchestration des insights éditoriaux par section (hors rendu documentaire)."""

from __future__ import annotations

from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.domain.results.section_eligibility_detail import (
    SectionEligibilityDetail,
)
from baobab_activity_reporting.reporting.agent_contribution_insight_writer import (
    AgentContributionInsightWriter,
)
from baobab_activity_reporting.reporting.attention_points_insight_writer import (
    AttentionPointsInsightWriter,
)
from baobab_activity_reporting.reporting.conclusion_insight_writer import (
    ConclusionInsightWriter,
)
from baobab_activity_reporting.reporting.dimensional_breakdown_insight_writer import (
    DimensionalBreakdownInsightWriter,
)
from baobab_activity_reporting.reporting.editorial.editorial_section_definition import (
    EditorialSectionDefinition,
)
from baobab_activity_reporting.reporting.fallback_section_insight_writer import (
    FallbackSectionInsightWriter,
)
from baobab_activity_reporting.reporting.report_context import ReportContext
from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)
from baobab_activity_reporting.reporting.site_workload_insight_writer import (
    SiteWorkloadInsightWriter,
)
from baobab_activity_reporting.reporting.telephony_activity_insight_writer import (
    TelephonyActivityInsightWriter,
)
from baobab_activity_reporting.reporting.telephony_overview_insight_writer import (
    TelephonyOverviewInsightWriter,
)
from baobab_activity_reporting.reporting.ticket_channels_insight_writer import (
    TicketChannelsInsightWriter,
)
from baobab_activity_reporting.reporting.ticket_processing_insight_writer import (
    TicketProcessingInsightWriter,
)
from baobab_activity_reporting.reporting.weekly_synthesis_insight_writer import (
    WeeklySynthesisInsightWriter,
)


class InsightBuilder:
    """Sélectionne un rédacteur d'insights selon le code de section.

    Les formulations visent des constats analytiques, pas une relecture ligne
    à ligne des tableaux ni l'exposition de codes KPI.
    """

    def __init__(
        self,
        *,
        section_writers: dict[str, object] | None = None,
        fallback_writer: FallbackSectionInsightWriter | None = None,
    ) -> None:
        """Initialise le registre des rédacteurs d'insights.

        :param section_writers: Map ``section_code`` → rédacteur avec ``write(ctx)``.
        :param fallback_writer: Rédacteur par défaut (liste vide par défaut).
        """
        self._fallback: FallbackSectionInsightWriter = (
            fallback_writer if fallback_writer is not None else FallbackSectionInsightWriter()
        )
        default_writers: dict[str, object] = {
            "weekly_synthesis": WeeklySynthesisInsightWriter(),
            "weekly_telephony": TelephonyActivityInsightWriter(),
            "weekly_ticket_processing": TicketProcessingInsightWriter(),
            "weekly_agent_contribution": AgentContributionInsightWriter(),
            "weekly_site_workload": SiteWorkloadInsightWriter(),
            "weekly_attention_points": AttentionPointsInsightWriter(),
            "weekly_conclusion": ConclusionInsightWriter(),
            "telephony_overview": TelephonyOverviewInsightWriter(),
            "ticket_channels": TicketChannelsInsightWriter(),
            "agent_breakdown": DimensionalBreakdownInsightWriter(),
            "site_breakdown": DimensionalBreakdownInsightWriter(),
        }
        self._writers: dict[str, object] = (
            dict(section_writers) if section_writers is not None else default_writers
        )

    def insights_for_section(
        self,
        editorial: EditorialSectionDefinition,
        kpi_rows: list[dict[str, object]],
        status: SectionStatus,
        report_type: str,
        context: ReportContext,
        *,
        eligibility_detail: SectionEligibilityDetail | None = None,
    ) -> list[str]:
        """Produit les insights pour une section donnée.

        :param editorial: Définition éditoriale (code, titre, objectif).
        :param kpi_rows: KPI filtrés pour la section.
        :param status: Statut d'éligibilité de la section.
        :param report_type: Type logique du rapport.
        :param context: Contexte rapport complet.
        :param eligibility_detail: Détail d'éligibilité (points d'attention).
        :return: Liste de phrases courtes.
        """
        period_start, period_end = context.period_iso_bounds()
        ctx = SectionEditorialContext.from_editorial(
            editorial,
            report_type,
            period_start,
            period_end,
            status,
            kpi_rows,
            context,
            eligibility_detail=eligibility_detail,
        )
        writer = self._writers.get(editorial.section_code, self._fallback)
        write_fn = getattr(writer, "write")
        return list(write_fn(ctx))
