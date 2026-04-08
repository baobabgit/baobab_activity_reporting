"""Rédaction narrative pour la section legacy « synthèse téléphonique »."""

from __future__ import annotations

from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)
from baobab_activity_reporting.reporting.telephony_activity_narrative_writer import (
    TelephonyActivityNarrativeWriter,
)


class TelephonyOverviewNarrativeWriter:
    """Réutilise la logique du rédacteur téléphonie hebdomadaire (même famille de KPI)."""

    def write(self, ctx: SectionEditorialContext) -> list[str]:
        """Produit les paragraphes de synthèse téléphonique.

        :param ctx: Contexte de section.
        :return: Paragraphes texte brut.
        """
        if ctx.status == SectionStatus.DEGRADED:
            return [
                "La synthèse téléphonique ne dispose pas d'indicateurs fiables sur cette période.",
            ]
        return TelephonyActivityNarrativeWriter().write(ctx)
