"""Insights pour les ventilations legacy par agent ou par site."""

from __future__ import annotations

from baobab_activity_reporting.reporting.agent_contribution_insight_writer import (
    AgentContributionInsightWriter,
)
from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)
from baobab_activity_reporting.reporting.site_workload_insight_writer import (
    SiteWorkloadInsightWriter,
)


class DimensionalBreakdownInsightWriter:
    """Route vers agent ou site selon le code de section."""

    def write(self, ctx: SectionEditorialContext) -> list[str]:
        """Produit les insights de concentration dimensionnelle.

        :param ctx: Contexte ; ``section_code`` vaut ``agent_breakdown`` ou ``site_breakdown``.
        :return: Phrases courtes.
        """
        if ctx.section_code == "agent_breakdown":
            return AgentContributionInsightWriter().write(ctx)
        if ctx.section_code == "site_breakdown":
            return SiteWorkloadInsightWriter().write(ctx)
        return []
