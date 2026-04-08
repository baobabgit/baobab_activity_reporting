"""Rédaction de la conclusion de rapport."""

from __future__ import annotations

from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)


class ConclusionNarrativeWriter:
    """Clôture sobre du rapport, sans répéter les tableaux."""

    def write(self, ctx: SectionEditorialContext) -> list[str]:
        """Produit un paragraphe de clôture.

        :param ctx: Contexte (période, type de rapport).
        :return: Un paragraphe.
        """
        if ctx.report_type in ("weekly_activity_by_agent", "weekly_activity_by_site"):
            lens = "par agent" if ctx.report_type == "weekly_activity_by_agent" else "par site"
            return [
                f"La lecture hebdomadaire {lens} s'arrête sur les indicateurs disponibles "
                f"du {ctx.period_start} au {ctx.period_end}. Toute décision opérationnelle "
                "devra croiser ces agrégats avec les dossiers sources."
            ]
        return [
            f"Les indicateurs présentés couvrent la période du {ctx.period_start} "
            f"au {ctx.period_end}. Ils synthétisent les volumes observés sans se substituer "
            "aux outils métiers détaillés."
        ]
