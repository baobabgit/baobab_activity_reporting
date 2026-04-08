"""Rédaction de la répartition de l'activité par site."""

from __future__ import annotations

from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.reporting.narrative_kpi_accessor import (
    NarrativeKpiAccessor,
)
from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)


class SiteWorkloadNarrativeWriter:
    """Analyse la répartition de charge entre sites."""

    def write(self, ctx: SectionEditorialContext) -> list[str]:
        """Produit au plus deux paragraphes.

        :param ctx: Contexte avec KPI préfixe ``site.``.
        :return: Paragraphes texte brut.
        """
        if ctx.status == SectionStatus.DEGRADED:
            return [self._degraded(ctx)]

        totals = NarrativeKpiAccessor.dimension_totals(ctx.kpi_rows, "site.")
        if not totals:
            return [
                "Aucune ventilation par site n'est exploitable : "
                "les indicateurs attendus sont absents.",
            ]

        grand = sum(v for _, v in totals)
        top_name, top_v = totals[0]
        top_share = 100.0 * top_v / grand if grand > 0 else 0.0
        n = len(totals)

        p1 = (
            f"La charge observée s'étend sur {n} site(s) ; « {top_name} » représente "
            f"environ {top_share:.0f} % de l'agrégat des volumes présents dans cette section."
        )

        if n >= 2 and top_share >= 55:
            p2 = (
                "Un site domine nettement l'activité : les écarts méritent d'être "
                "rapprochés des objectifs de répartition ou des contraintes locales."
            )
            return [p1, p2]
        if n >= 3 and top_share < 40:
            p2 = (
                "Les sites partagent la charge de façon relativement homogène, "
                "ce qui limite la dépendance à un seul lieu."
            )
            return [p1, p2]
        return [p1]

    @staticmethod
    def _degraded(ctx: SectionEditorialContext) -> str:
        """Texte dégradé."""
        base = ctx.section_objective or "Analyser la charge par site."
        return (
            f"{base} Les ventilations site ne sont pas disponibles ou sont insuffisantes "
            f"pour la période du {ctx.period_start} au {ctx.period_end}."
        )
