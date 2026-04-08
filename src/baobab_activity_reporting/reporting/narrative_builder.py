"""Orchestration de la rédaction narrative par section (hors rendu documentaire)."""

from __future__ import annotations

from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.domain.results.section_eligibility_detail import (
    SectionEligibilityDetail,
)
from baobab_activity_reporting.reporting.agent_breakdown_narrative_writer import (
    AgentBreakdownNarrativeWriter,
)
from baobab_activity_reporting.reporting.agent_contribution_narrative_writer import (
    AgentContributionNarrativeWriter,
)
from baobab_activity_reporting.reporting.attention_points_narrative_writer import (
    AttentionPointsNarrativeWriter,
)
from baobab_activity_reporting.reporting.conclusion_narrative_writer import (
    ConclusionNarrativeWriter,
)
from baobab_activity_reporting.reporting.editorial.editorial_section_definition import (
    EditorialSectionDefinition,
)
from baobab_activity_reporting.reporting.fallback_section_narrative_writer import (
    FallbackSectionNarrativeWriter,
)
from baobab_activity_reporting.reporting.report_context import ReportContext
from baobab_activity_reporting.reporting.report_lead_narrative_writer import (
    ReportLeadNarrativeWriter,
)
from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)
from baobab_activity_reporting.reporting.site_breakdown_narrative_writer import (
    SiteBreakdownNarrativeWriter,
)
from baobab_activity_reporting.reporting.site_workload_narrative_writer import (
    SiteWorkloadNarrativeWriter,
)
from baobab_activity_reporting.reporting.telephony_activity_narrative_writer import (
    TelephonyActivityNarrativeWriter,
)
from baobab_activity_reporting.reporting.telephony_overview_narrative_writer import (
    TelephonyOverviewNarrativeWriter,
)
from baobab_activity_reporting.reporting.ticket_channels_narrative_writer import (
    TicketChannelsNarrativeWriter,
)
from baobab_activity_reporting.reporting.ticket_processing_narrative_writer import (
    TicketProcessingNarrativeWriter,
)
from baobab_activity_reporting.reporting.weekly_synthesis_narrative_writer import (
    WeeklySynthesisNarrativeWriter,
)


class NarrativeBuilder:
    """Délègue la rédaction à des classes spécialisées par section.

    Chaque rédacteur produit au plus deux paragraphes analytiques, sans
    répétition mécanique des tableaux ni code KPI dans le texte.
    """

    def __init__(
        self,
        *,
        lead_writer: ReportLeadNarrativeWriter | None = None,
        section_writers: dict[str, object] | None = None,
        fallback_writer: FallbackSectionNarrativeWriter | None = None,
    ) -> None:
        """Initialise le registre des rédacteurs de section.

        :param lead_writer: Rédacteur d'accroche rapport (défaut : instance standard).
        :param section_writers: Map ``section_code`` → rédacteur avec méthode ``write(ctx)``.
        :param fallback_writer: Rédacteur si le code de section est inconnu.
        """
        self._lead: ReportLeadNarrativeWriter = (
            lead_writer if lead_writer is not None else ReportLeadNarrativeWriter()
        )
        self._fallback: FallbackSectionNarrativeWriter = (
            fallback_writer if fallback_writer is not None else FallbackSectionNarrativeWriter()
        )
        default_writers: dict[str, object] = {
            "weekly_synthesis": WeeklySynthesisNarrativeWriter(),
            "weekly_telephony": TelephonyActivityNarrativeWriter(),
            "weekly_ticket_processing": TicketProcessingNarrativeWriter(),
            "weekly_agent_contribution": AgentContributionNarrativeWriter(),
            "weekly_site_workload": SiteWorkloadNarrativeWriter(),
            "weekly_attention_points": AttentionPointsNarrativeWriter(),
            "weekly_conclusion": ConclusionNarrativeWriter(),
            "telephony_overview": TelephonyOverviewNarrativeWriter(),
            "ticket_channels": TicketChannelsNarrativeWriter(),
            "agent_breakdown": AgentBreakdownNarrativeWriter(),
            "site_breakdown": SiteBreakdownNarrativeWriter(),
        }
        self._writers: dict[str, object] = (
            dict(section_writers) if section_writers is not None else default_writers
        )

    def lead_paragraph(
        self,
        context: ReportContext,
        report_title: str,
        report_type: str,
    ) -> str:
        """Génère l'introduction du rapport selon le type et les données.

        :param context: Période et KPI complets.
        :param report_title: Titre formaté du rapport.
        :param report_type: Identifiant du type de rapport.
        :return: Un paragraphe texte brut.
        """
        return self._lead.write(context, report_title, report_type)

    def section_narrative_blocks(
        self,
        editorial: EditorialSectionDefinition,
        kpi_rows: list[dict[str, object]],
        status: SectionStatus,
        report_type: str,
        context: ReportContext,
        *,
        eligibility_detail: SectionEligibilityDetail | None = None,
    ) -> list[str]:
        """Produit les paragraphes narratifs d'une section.

        :param editorial: Définition éditoriale.
        :param kpi_rows: KPI filtrés pour la section.
        :param status: Statut d'inclusion.
        :param report_type: Type de rapport.
        :param context: Contexte complet (pour KPI globaux).
        :param eligibility_detail: Détail d'éligibilité optionnel.
        :return: Liste de paragraphes (souvent un ou deux éléments).
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
