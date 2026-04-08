"""Rédaction narrative pour la section legacy « indicateurs par agent »."""

from __future__ import annotations

from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.reporting.agent_contribution_narrative_writer import (
    AgentContributionNarrativeWriter,
)
from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)


class AgentBreakdownNarrativeWriter:
    """Réutilise le rédacteur de contribution agent."""

    def write(self, ctx: SectionEditorialContext) -> list[str]:
        """Produit les paragraphes de ventilation agent.

        :param ctx: Contexte de section.
        :return: Paragraphes texte brut.
        """
        if ctx.status == SectionStatus.DEGRADED:
            return [
                "Les indicateurs par agent ne sont pas disponibles "
                "ou sont incomplets pour cette période.",
            ]
        return AgentContributionNarrativeWriter().write(ctx)
