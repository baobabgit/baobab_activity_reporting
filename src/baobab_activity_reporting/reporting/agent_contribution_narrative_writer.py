"""Rédaction de la répartition de l'activité par agent."""

from __future__ import annotations

from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.reporting.narrative_kpi_accessor import (
    NarrativeKpiAccessor,
)
from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)


class AgentContributionNarrativeWriter:
    """Analyse la concentration de charge entre agents."""

    def write(self, ctx: SectionEditorialContext) -> list[str]:
        """Produit au plus deux paragraphes.

        :param ctx: Contexte avec KPI préfixe ``agent.``.
        :return: Paragraphes texte brut.
        """
        if ctx.status == SectionStatus.DEGRADED:
            return [self._degraded(ctx)]

        totals = NarrativeKpiAccessor.dimension_totals(ctx.kpi_rows, "agent.")
        if not totals:
            return [
                "Aucune ventilation par agent n'est exploitable : "
                "les indicateurs attendus sont absents.",
            ]

        grand = sum(v for _, v in totals)
        top_name, top_v = totals[0]
        top_share = 100.0 * top_v / grand if grand > 0 else 0.0
        n = len(totals)

        p1 = (
            f"L'activité agrégée couvre {n} agent(s) ; « {top_name} » porte environ "
            f"{top_share:.0f} % de la somme des indicateurs présents dans cette section."
        )

        if n >= 2 and top_share >= 55:
            p2 = (
                "La charge paraît concentrée sur peu de contributeurs : "
                "le tableau ventilé permet de vérifier si cette concentration tient aux volumes "
                "téléphoniques, aux tickets, ou aux deux."
            )
            return [p1, p2]
        if n >= 3 and top_share < 40:
            p2 = (
                "La répartition semble plus diffuse : l'effort est partagé entre plusieurs "
                "profils, ce qui atténue le risque de goulot d'étranglement individuel."
            )
            return [p1, p2]
        return [p1]

    @staticmethod
    def _degraded(ctx: SectionEditorialContext) -> str:
        """Texte dégradé."""
        base = ctx.section_objective or "Analyser la contribution par agent."
        return (
            f"{base} Les ventilations agent ne sont pas disponibles ou sont insuffisantes "
            f"pour la période du {ctx.period_start} au {ctx.period_end}."
        )
