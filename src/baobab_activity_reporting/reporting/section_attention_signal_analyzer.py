"""Détection de signaux méritant une section « points d'attention »."""

from __future__ import annotations

from baobab_activity_reporting.domain.results.section_attention_assessment import (
    SectionAttentionAssessment,
)
from baobab_activity_reporting.domain.results.section_eligibility_codes import (
    SectionEligibilityCodes,
)
from baobab_activity_reporting.reporting.kpi_value_assessor import KpiValueAssessor
from baobab_activity_reporting.reporting.report_context import ReportContext


class SectionAttentionSignalAnalyzer:
    """Analyse simples déséquilibres téléphonie et concentration canaux tickets.

    Seuils fixes et documentés ; aucune sortie formatée pour un document.
    """

    _IMBALANCE_RATIO: float = 5.0
    _CHANNEL_DOMINANCE: float = 0.85

    def analyze(self, context: ReportContext) -> SectionAttentionAssessment:
        """Produit une évaluation des anomalies visibles dans les KPI.

        :param context: KPI disponibles.
        :type context: ReportContext
        :return: Synthèse des signaux détectés.
        :rtype: SectionAttentionAssessment
        """
        notes: list[str] = []
        codes: set[str] = set()

        inc = KpiValueAssessor.numeric_for_code(context, "telephony.incoming.count")
        out = KpiValueAssessor.numeric_for_code(context, "telephony.outgoing.count")
        if inc is not None and out is not None and inc > 0 and out > 0:
            hi = max(inc, out)
            lo = min(inc, out)
            if lo > 0 and hi / lo >= self._IMBALANCE_RATIO:
                codes.add(SectionEligibilityCodes.ATTENTION_IMBALANCE_TELEPHONY)
                notes.append(
                    f"déséquilibre téléphonie entrants/sortants (ratio>={self._IMBALANCE_RATIO}).",
                )

        total, reliable = KpiValueAssessor.sum_channel_ticket_counts(context)
        if reliable and total > 0:
            for row in context.kpi_records:
                code = str(row.get("code", ""))
                if not code.startswith("tickets.channel.") or not code.endswith(".count"):
                    continue
                val = KpiValueAssessor.finite_number(row.get("value"))
                if val is None or val < 0:
                    continue
                if val / total >= self._CHANNEL_DOMINANCE:
                    codes.add(SectionEligibilityCodes.ATTENTION_TICKET_CHANNEL_DOMINANCE)
                    notes.append(
                        f"canal dominant {code} part={val / total:.2f}.",
                    )
                    break

        has_points = len(codes) > 0
        signal_codes = (
            frozenset(codes)
            if has_points
            else frozenset(
                {SectionEligibilityCodes.EXCLUDED_NO_ATTENTION_SIGNALS},
            )
        )

        return SectionAttentionAssessment(
            has_attention_points=has_points,
            signal_codes=signal_codes,
            notes=tuple(notes) if notes else ("aucun signal d'anomalie détecté.",),
        )
