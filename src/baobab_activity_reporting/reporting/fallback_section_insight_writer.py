"""Insights de secours : pas de liste mécanique de KPI."""

from __future__ import annotations

from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)


class FallbackSectionInsightWriter:
    """Retourne une liste vide pour éviter la paraphrase des tableaux."""

    def write(self, ctx: SectionEditorialContext) -> list[str]:
        """Ne produit pas d'insights génériques.

        :param ctx: Contexte (non utilisé).
        :return: Liste vide.
        """
        _ = ctx
        return []
