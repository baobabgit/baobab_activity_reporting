"""Rédaction narrative pour la section legacy « tickets par canal »."""

from __future__ import annotations

from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)
from baobab_activity_reporting.reporting.ticket_processing_narrative_writer import (
    TicketProcessingNarrativeWriter,
)


class TicketChannelsNarrativeWriter:
    """Réutilise le rédacteur d'activité de traitement ticket."""

    def write(self, ctx: SectionEditorialContext) -> list[str]:
        """Produit les paragraphes sur la répartition par canal.

        :param ctx: Contexte de section.
        :return: Paragraphes texte brut.
        """
        if ctx.status == SectionStatus.DEGRADED:
            return [
                "La répartition des tickets par canal ne peut être commentée : "
                "données absentes ou invalides.",
            ]
        return TicketProcessingNarrativeWriter().write(ctx)
