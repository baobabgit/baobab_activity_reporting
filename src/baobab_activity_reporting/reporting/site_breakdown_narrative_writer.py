"""Rédaction narrative pour la section legacy « indicateurs par site »."""

from __future__ import annotations

from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)
from baobab_activity_reporting.reporting.site_workload_narrative_writer import (
    SiteWorkloadNarrativeWriter,
)


class SiteBreakdownNarrativeWriter:
    """Réutilise le rédacteur de charge par site."""

    def write(self, ctx: SectionEditorialContext) -> list[str]:
        """Produit les paragraphes de ventilation site.

        :param ctx: Contexte de section.
        :return: Paragraphes texte brut.
        """
        if ctx.status == SectionStatus.DEGRADED:
            return [
                "Les indicateurs par site ne sont pas disponibles "
                "ou sont incomplets pour cette période.",
            ]
        return SiteWorkloadNarrativeWriter().write(ctx)
