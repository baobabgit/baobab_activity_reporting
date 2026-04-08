"""Insights sur les volumes tickets par canal."""

from __future__ import annotations

from baobab_activity_reporting.reporting.narrative_kpi_accessor import (
    NarrativeKpiAccessor,
)
from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)


class TicketProcessingInsightWriter:
    """Met en avant canal dominant ou équilibre sans énumération exhaustive."""

    def write(self, ctx: SectionEditorialContext) -> list[str]:
        """Produit au plus deux insights.

        :param ctx: Contexte avec KPI tickets.
        :return: Phrases courtes.
        """
        pairs = NarrativeKpiAccessor.channel_volumes_sorted(ctx.kpi_rows)
        total = sum(v for _, v in pairs)
        if not pairs or total <= 0:
            return []

        top_label, top_v = pairs[0]
        share = 100.0 * top_v / total
        insights: list[str] = []

        if share >= 75:
            insights.append(
                f"Le canal « {top_label} » structure l'essentiel du flux "
                f"({share:.0f} % des tickets) : toute défaillance sur ce canal "
                "impacterait fortement le service."
            )
        elif len(pairs) >= 2:
            second_label, second_v = pairs[1]
            s2 = 100.0 * second_v / total
            insights.append(
                f"Deux canaux portent la majorité du volume (« {top_label} » ~{share:.0f} %, "
                f"« {second_label} » ~{s2:.0f} %), ce qui laisse une marge sur les autres modes."
            )
        else:
            insights.append(
                f"L'activité ticket est portée par un canal unique (« {top_label} ») : "
                "la diversification des points de contact reste limitée sur cette période."
            )

        if len(pairs) >= 3 and share < 45:
            insights.append(
                "La multiplicité des canaux actifs suggère une organisation multi-points ; "
                "consolider les règles de routage peut aider à simplifier le pilotage."
            )

        return insights[:2]
