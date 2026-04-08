"""Rédaction du paragraphe d'ouverture du rapport (hors rendu documentaire)."""

from __future__ import annotations

from baobab_activity_reporting.reporting.narrative_kpi_accessor import (
    NarrativeKpiAccessor,
)
from baobab_activity_reporting.reporting.report_context import ReportContext


class ReportLeadNarrativeWriter:
    """Produit une accroche contextualisée selon les données disponibles.

    Évite les formulations génériques du type « ce rapport couvre » lorsque
    des volumes exploitables permettent une lecture immédiate.
    """

    def write(  # pylint: disable=too-many-locals,too-many-return-statements
        self,
        context: ReportContext,
        report_title: str,
        report_type: str,
    ) -> str:
        """Rédige un seul paragraphe d'introduction.

        :param context: Période et KPI complets.
        :param report_title: Titre déjà formaté du rapport.
        :param report_type: Type logique du rapport.
        :return: Texte brut, une phrase ou deux reliées.
        """
        _ = report_title
        start, end = context.period_iso_bounds()
        period_clause = f"Sur la période du {start} au {end}"
        rows = context.kpi_records
        tel = NarrativeKpiAccessor.filter_global_telephony(rows)
        inc, outg = NarrativeKpiAccessor.incoming_outgoing_counts(tel)
        channels = NarrativeKpiAccessor.channel_volumes_sorted(
            NarrativeKpiAccessor.filter_ticket_channels(rows),
        )
        ticket_total = sum(v for _, v in channels)

        if report_type in ("weekly_activity_by_agent", "weekly_activity_by_site"):
            parts: list[str] = []
            if inc is not None or outg is not None:
                parts.append(self._telephony_clause(inc, outg))
            if channels and ticket_total > 0:
                parts.append(self._tickets_clause(channels, ticket_total))
            if parts:
                return f"{period_clause}, {self._join_clauses(parts)}."
            return (
                f"{period_clause}, les jeux de données disponibles restent partiels : "
                "la lecture s'appuie sur les sections suivantes pour préciser le périmètre couvert."
            )

        if report_type == "activity_telephony":
            parts2: list[str] = []
            if inc is not None or outg is not None:
                parts2.append(self._telephony_clause(inc, outg))
            if channels and ticket_total > 0:
                parts2.append(self._tickets_clause(channels, ticket_total))
            if parts2:
                return f"{period_clause}, {self._join_clauses(parts2)}."
            return (
                f"{period_clause}, aucun volume téléphonique ou ticket exploitable n'a été détecté."
            )

        agents = NarrativeKpiAccessor.dimension_totals(rows, "agent.")
        sites = NarrativeKpiAccessor.dimension_totals(rows, "site.")
        if report_type == "activity_by_agent" and agents:
            n = len(agents)
            return (
                f"{period_clause}, l'activité est ventilée sur {n} agent(s) ; "
                "les tableaux détaillent la contribution de chacun."
            )
        if report_type == "activity_by_site" and sites:
            n = len(sites)
            return (
                f"{period_clause}, la charge observée se répartit entre {n} site(s) "
                "analysés dans la suite du document."
            )

        return (
            f"{period_clause}, le rapport synthétise les indicateurs disponibles "
            "sans détailler ici chaque ligne de données."
        )

    @staticmethod
    def _telephony_clause(
        inc: float | None,
        outg: float | None,
    ) -> str:
        """Clause courte sur les volumes téléphoniques."""
        if inc is not None and outg is not None and (inc + outg) > 0:
            total = inc + outg
            pi = 100.0 * inc / total
            return (
                f"la téléphonie compte environ {int(round(inc))} appels entrants "
                f"et {int(round(outg))} sortants (les entrants représentent environ "
                f"{pi:.0f} % du volume)"
            )
        if inc is not None:
            return f"la téléphonie enregistre environ {int(round(inc))} appels entrants"
        if outg is not None:
            return f"la téléphonie enregistre environ {int(round(outg))} appels sortants"
        return "la téléphonie ne fournit pas de volumes agrégés exploitables"

    @staticmethod
    def _tickets_clause(
        channels: list[tuple[str, float]],
        ticket_total: float,
    ) -> str:
        """Clause courte sur les tickets."""
        if not channels or ticket_total <= 0:
            return "les tickets ne présentent pas de volumes canal exploitables"
        top_label, top_v = channels[0]
        pct = 100.0 * top_v / ticket_total
        if len(channels) == 1:
            return f"les tickets sont traités surtout via le canal « {top_label} »"
        return (
            f"le canal « {top_label} » concentre environ {pct:.0f} % "
            f"des tickets ({int(round(top_v))} sur {int(round(ticket_total))})"
        )

    @staticmethod
    def _join_clauses(parts: list[str]) -> str:
        """Relie deux propositions en français."""
        if len(parts) == 1:
            return parts[0]
        return f"{parts[0]}, tandis que {parts[1]}"
