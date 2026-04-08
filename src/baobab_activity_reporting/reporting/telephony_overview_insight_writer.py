"""Insights pour la section legacy synthèse téléphonique."""

from __future__ import annotations

from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)
from baobab_activity_reporting.reporting.telephony_activity_insight_writer import (
    TelephonyActivityInsightWriter,
)


class TelephonyOverviewInsightWriter:
    """Délègue au rédacteur d'insights téléphonie hebdomadaire."""

    def write(self, ctx: SectionEditorialContext) -> list[str]:
        """Produit les insights téléphoniques.

        :param ctx: Contexte de section.
        :return: Phrases courtes.
        """
        return TelephonyActivityInsightWriter().write(ctx)
