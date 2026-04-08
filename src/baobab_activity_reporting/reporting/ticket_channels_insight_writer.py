"""Insights pour la section legacy tickets par canal."""

from __future__ import annotations

from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)
from baobab_activity_reporting.reporting.ticket_processing_insight_writer import (
    TicketProcessingInsightWriter,
)


class TicketChannelsInsightWriter:
    """Délègue au rédacteur d'insights traitement ticket."""

    def write(self, ctx: SectionEditorialContext) -> list[str]:
        """Produit les insights sur les canaux.

        :param ctx: Contexte de section.
        :return: Phrases courtes.
        """
        return TicketProcessingInsightWriter().write(ctx)
