"""Insights éditoriaux pour la synthèse hebdomadaire."""

from __future__ import annotations

from baobab_activity_reporting.reporting.narrative_kpi_accessor import (
    NarrativeKpiAccessor,
)
from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)


class WeeklySynthesisInsightWriter:
    """Constats de haut niveau sur la complétude des jeux de données."""

    def write(self, ctx: SectionEditorialContext) -> list[str]:
        """Produit au plus deux insights.

        :param ctx: Contexte avec ``full_kpi_rows``.
        :return: Phrases courtes sans code technique.
        """
        full = ctx.full_kpi_rows
        tel = NarrativeKpiAccessor.filter_global_telephony(full)
        inc, outg = NarrativeKpiAccessor.incoming_outgoing_counts(tel)
        channels = NarrativeKpiAccessor.channel_volumes_sorted(
            NarrativeKpiAccessor.filter_ticket_channels(full),
        )
        ticket_total = sum(v for _, v in channels)
        has_tel = inc is not None or outg is not None
        has_tickets = bool(channels) and ticket_total > 0

        out: list[str] = []
        if has_tel and has_tickets:
            out.append(
                "Les deux familles d'indicateurs (téléphonie et tickets) sont alimentées : "
                "la cohérence entre sections permet d'écarter une lecture unidimensionnelle."
            )
        elif has_tel:
            out.append(
                "Seule la téléphonie offre des agrégats stables sur cette fenêtre : "
                "toute analyse ticket devra s'appuyer sur d'autres exports si nécessaire."
            )
        elif has_tickets:
            out.append(
                "Les tickets sont documentés mais la téléphonie globale manque : "
                "le contact client n'est pas entièrement visible dans ce périmètre."
            )
        else:
            out.append(
                "Les agrégats de synthèse sont partiels : prioriser la validation des imports "
                "avant d'interpréter les sections détaillées."
            )
        if has_tel and inc is not None and outg is not None and inc > 0 and outg > 0:
            hi = max(inc, outg)
            lo = min(inc, outg)
            if lo > 0 and hi / lo >= 2.0:
                out.append(
                    "Le rapport entrants/sortants mérite un suivi : l'un des deux sens "
                    "porte nettement plus de volume que l'autre."
                )
        return out[:2]
