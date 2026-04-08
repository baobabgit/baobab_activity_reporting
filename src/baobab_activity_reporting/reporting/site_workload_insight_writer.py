"""Insights sur la répartition de charge entre sites."""

from __future__ import annotations

from baobab_activity_reporting.reporting.narrative_kpi_accessor import (
    NarrativeKpiAccessor,
)
from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)


class SiteWorkloadInsightWriter:
    """Détecte polarisation ou équilibre inter-sites."""

    def write(self, ctx: SectionEditorialContext) -> list[str]:
        """Produit au plus deux insights.

        :param ctx: Contexte avec KPI ``site.``.
        :return: Phrases courtes.
        """
        totals = NarrativeKpiAccessor.dimension_totals(ctx.kpi_rows, "site.")
        if len(totals) < 2:
            return []

        grand = sum(v for _, v in totals)
        if grand <= 0:
            return []

        top_name, top_v = totals[0]
        share = 100.0 * top_v / grand
        insights: list[str] = []

        if share >= 50:
            insights.append(
                f"Le site « {top_name} » porte environ {share:.0f} % de l'agrégat : "
                "la résilience opérationnelle dépend fortement de ce lieu."
            )
        else:
            insights.append(
                "Aucun site ne monopolise la moitié de l'activité agrégée : "
                "la charge semble mieux répartie géographiquement."
            )
        return insights[:2]
