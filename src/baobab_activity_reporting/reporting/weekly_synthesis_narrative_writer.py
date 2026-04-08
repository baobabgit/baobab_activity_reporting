"""Rédaction de la section synthèse hebdomadaire."""

from __future__ import annotations

from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.reporting.narrative_kpi_accessor import (
    NarrativeKpiAccessor,
)
from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)


class WeeklySynthesisNarrativeWriter:
    """Synthèse globale : téléphonie, tickets, ou données partielles."""

    def write(self, ctx: SectionEditorialContext) -> list[str]:
        """Produit au plus deux paragraphes analytiques.

        :param ctx: Contexte de section et KPI complets.
        :return: Liste de paragraphes (texte brut).
        """
        if ctx.status == SectionStatus.DEGRADED:
            return [self._degraded(ctx)]

        full = ctx.full_kpi_rows
        tel = NarrativeKpiAccessor.filter_global_telephony(full)
        inc, outg = NarrativeKpiAccessor.incoming_outgoing_counts(tel)
        channels = NarrativeKpiAccessor.channel_volumes_sorted(
            NarrativeKpiAccessor.filter_ticket_channels(full),
        )
        ticket_total = sum(v for _, v in channels)

        has_tel = inc is not None or outg is not None
        has_tickets = bool(channels) and ticket_total > 0

        p1 = self._paragraph_activity(inc, outg, channels, ticket_total, has_tel, has_tickets)
        p2 = self._paragraph_reading_guide(has_tel, has_tickets)
        return [p1, p2]

    @staticmethod
    def _paragraph_activity(
        inc: float | None,
        outg: float | None,
        channels: list[tuple[str, float]],
        ticket_total: float,
        has_tel: bool,
        has_tickets: bool,
    ) -> str:
        """Premier paragraphe : lecture des volumes principaux."""
        chunks: list[str] = []
        if has_tel and inc is not None and outg is not None and (inc + outg) > 0:
            total = inc + outg
            pi = 100.0 * inc / total
            chunks.append(
                f"Les flux téléphoniques s'établissent à environ {int(round(inc))} appels entrants "
                f"et {int(round(outg))} sortants, soit environ {pi:.0f} % d'appels entrants "
                f"dans le total."
            )
        elif has_tel:
            if inc is not None:
                chunks.append(
                    f"Le volume entrant domine la photographie téléphonique "
                    f"({int(round(inc))} appels) ; les sortants ne sont pas renseignés de "
                    f"façon comparable."
                )
            elif outg is not None:
                chunks.append(
                    f"L'activité sortante est documentée ({int(round(outg))} appels) "
                    f"tandis que le volet entrant manque ou est incomplet."
                )
        if has_tickets:
            top_label, top_v = channels[0]
            pct = 100.0 * top_v / ticket_total
            if len(channels) == 1:
                chunks.append(
                    f"Côté tickets, le flux passe entièrement par le canal « {top_label} » "
                    f"({int(round(ticket_total))} ticket(s) observé(s))."
                )
            else:
                chunks.append(
                    f"Le traitement ticket s'appuie sur plusieurs canaux : "
                    f"« {top_label} » porte environ {pct:.0f} % du volume ({int(round(top_v))} sur "
                    f"{int(round(ticket_total))})."
                )
        if not chunks:
            return (
                "Aucun agrégat téléphonique ou ticket n'est exploitable en tête de période : "
                "la synthèse se limite donc à cadrer la lecture des sections suivantes."
            )
        return " ".join(chunks)

    @staticmethod
    def _paragraph_reading_guide(
        has_tel: bool,
        has_tickets: bool,
    ) -> str:
        """Second paragraphe : guide de lecture et partialité."""
        if has_tel and has_tickets:
            return (
                "Les sections suivantes déclinent téléphonie et traitement sans recopier "
                "les tableaux : elles mettent l'accent sur les écarts et la répartition."
            )
        if has_tel and not has_tickets:
            return (
                "Faute de volumes tickets consolidés, l'analyse s'appuie surtout sur la "
                "téléphonie ; toute section tickets restera indicative ou vide selon les "
                "données réellement chargées."
            )
        if has_tickets and not has_tel:
            return (
                "Sans agrégats téléphoniques comparables, la lecture hebdomadaire repose "
                "prioritairement sur les canaux tickets et les ventilations disponibles plus bas."
            )
        return (
            "Les jeux partiels observés invitent à croiser chaque section avec son tableau "
            "associé plutôt qu'à inférer des totaux non publiés ici."
        )

    @staticmethod
    def _degraded(ctx: SectionEditorialContext) -> str:
        """Message pour section obligatoire sans indicateurs."""
        obj = ctx.section_objective
        if obj:
            return (
                f"{obj} Les indicateurs attendus ne sont pas présents ou sont insuffisants "
                f"pour la période du {ctx.period_start} au {ctx.period_end} ; "
                "les autres sections du rapport complètent la lecture lorsque des données existent."
            )
        return (
            f"La synthèse ne dispose pas d'indicateurs consolidés pour la période "
            f"du {ctx.period_start} au {ctx.period_end} ; le reste du rapport détaille "
            "les blocs pour lesquels des volumes sont disponibles."
        )
