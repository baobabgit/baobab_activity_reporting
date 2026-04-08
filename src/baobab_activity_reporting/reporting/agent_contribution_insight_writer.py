"""Insights sur la répartition de charge entre agents."""

from __future__ import annotations

from baobab_activity_reporting.reporting.narrative_kpi_accessor import (
    NarrativeKpiAccessor,
)
from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)


class AgentContributionInsightWriter:
    """Détecte concentration ou partage de l'effort."""

    def write(self, ctx: SectionEditorialContext) -> list[str]:
        """Produit au plus deux insights.

        :param ctx: Contexte avec KPI ``agent.``.
        :return: Phrases courtes.
        """
        totals = NarrativeKpiAccessor.dimension_totals(ctx.kpi_rows, "agent.")
        if len(totals) < 2:
            return []

        grand = sum(v for _, v in totals)
        if grand <= 0:
            return []

        top_name, top_v = totals[0]
        share = 100.0 * top_v / grand
        hhi = sum((v / grand) ** 2 for _, v in totals)

        insights: list[str] = []
        if share >= 50:
            insights.append(
                f"« {top_name} » concentre environ la moitié ou plus de l'agrégat observé "
                f"({share:.0f} %) : anticiper les absences ou la surcharge sur ce profil."
            )
        elif hhi <= 0.35:
            insights.append(
                "La charge paraît relativement partagée entre plusieurs agents, "
                "ce qui réduit la dépendance à une seule ressource."
            )
        else:
            insights.append(
                "La répartition présente un intermédiaire entre concentration et équilibre : "
                "le tableau détaillé permet d'identifier les leviers de rééquilibrage."
            )
        return insights[:2]
