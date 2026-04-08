"""Rédaction narrative de l'activité de traitement (tickets)."""

from __future__ import annotations

from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.reporting.narrative_kpi_accessor import (
    NarrativeKpiAccessor,
)
from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)


class TicketProcessingNarrativeWriter:
    """Met en perspective les volumes par canal sans lister mécaniquement chaque ligne."""

    def write(self, ctx: SectionEditorialContext) -> list[str]:
        """Produit un ou deux paragraphes.

        :param ctx: Contexte ; KPI filtrés sur les tickets.
        :return: Paragraphes texte brut.
        """
        if ctx.status == SectionStatus.DEGRADED:
            return [self._degraded(ctx)]

        pairs = NarrativeKpiAccessor.channel_volumes_sorted(ctx.kpi_rows)
        total = sum(v for _, v in pairs)
        if not pairs or total <= 0:
            return [
                "Aucun volume ticket par canal n'est documenté pour cette période : "
                "la section ne peut proposer de lecture quantitative."
            ]

        top_label, top_v = pairs[0]
        share = 100.0 * top_v / total
        if len(pairs) == 1:
            p1 = (
                f"Tout le flux ticket observé ({int(round(total))} unité(s)) transite par le "
                f"canal « {top_label} », ce qui simplifie la lecture mais concentre aussi le "
                f"risque opérationnel."
            )
        else:
            others = len(pairs) - 1
            p1 = (
                f"Sur {int(round(total))} ticket(s), le canal « {top_label} » concentre environ "
                f"{share:.0f} % du volume ; {others} autre(s) canal(aux) assure(nt) le reliquat."
            )

        if len(pairs) >= 2 and share >= 70:
            p2 = (
                "La répartition reste marquée par une forte polarisation : "
                "les tableaux détaillent les écarts entre canaux pour affiner le diagnostic."
            )
            return [p1, p2]
        if len(pairs) >= 3 and share < 50:
            p2 = (
                "La charge se répartit de façon relativement équilibrée entre plusieurs canaux, "
                "ce qui invite à analyser les segments plutôt que le seul total agrégé."
            )
            return [p1, p2]
        return [p1]

    @staticmethod
    def _degraded(ctx: SectionEditorialContext) -> str:
        """Texte dégradé."""
        base = ctx.section_objective or "Présenter l'activité tickets."
        return (
            f"{base} Les volumes par canal ne sont pas disponibles ou sont invalides "
            f"pour la période du {ctx.period_start} au {ctx.period_end}."
        )
