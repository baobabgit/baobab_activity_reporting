"""Insights pour la conclusion (aucun constat additionnel)."""

from __future__ import annotations

from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)


class ConclusionInsightWriter:
    """La conclusion ne duplique pas d'insights : liste vide."""

    def write(self, ctx: SectionEditorialContext) -> list[str]:
        """Retourne toujours une liste vide.

        :param ctx: Contexte (non utilisé).
        :return: Liste vide.
        """
        _ = ctx
        return []
