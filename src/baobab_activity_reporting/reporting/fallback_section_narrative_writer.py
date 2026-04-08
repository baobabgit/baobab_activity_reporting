"""Rédacteur de secours pour les sections sans moteur dédié."""

from __future__ import annotations

from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)


class FallbackSectionNarrativeWriter:
    """Produit un texte sobre sans inventaire mécanique des KPI."""

    def write(self, ctx: SectionEditorialContext) -> list[str]:
        """Rédige au plus deux paragraphes génériques mais non vides de sens.

        :param ctx: Contexte de section.
        :return: Paragraphes texte brut.
        """
        title = ctx.section_title
        if ctx.status == SectionStatus.DEGRADED:
            return [
                f"La section « {title} » est conservée sans indicateurs exploitables "
                f"sur la période du {ctx.period_start} au {ctx.period_end}."
            ]
        n = len(ctx.kpi_rows)
        if ctx.section_objective:
            p1 = f"{ctx.section_objective} ({n} indicateur(s) lié(s) à cette section)."
        else:
            p1 = (
                f"La section « {title} » s'appuie sur {n} indicateur(s) ; le tableau résume "
                "les valeurs sans qu'une interprétation détaillée soit proposée ici."
            )
        return [p1]
