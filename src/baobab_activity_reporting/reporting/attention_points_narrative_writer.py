"""Rédaction de la section points d'attention."""

from __future__ import annotations

from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)


class AttentionPointsNarrativeWriter:
    """Cadre la section vigilance ; le détail factuel est porté par les insights."""

    def write(self, ctx: SectionEditorialContext) -> list[str]:
        """Produit un paragraphe d'encadrement (les constats sont dans les insights).

        :param ctx: Contexte de section.
        :return: Un paragraphe unique ou deux si dégradé.
        """
        if ctx.status == SectionStatus.DEGRADED:
            return [
                self._degraded(ctx),
            ]

        p1 = (
            "Cette section recense les écarts significatifs repérés dans les agrégats disponibles "
            f"sur la période du {ctx.period_start} au {ctx.period_end}. "
            "Les formulations ci-dessous restent descriptives et n'imputent pas de cause."
        )
        return [p1]

    @staticmethod
    def _degraded(ctx: SectionEditorialContext) -> str:
        """Texte lorsque la section est maintenue sans signaux exploitables."""
        base = ctx.section_objective or "Signaler les points d'attention."
        return (
            f"{base} Les données ne permettent pas d'identifier de signaux robustes "
            f"pour cette période ; les tableaux éventuels restent indicatifs."
        )
