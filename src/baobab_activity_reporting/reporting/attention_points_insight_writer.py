"""Insights pour la section points d'attention."""

from __future__ import annotations

from baobab_activity_reporting.domain.results.section_eligibility_codes import (
    SectionEligibilityCodes,
)
from baobab_activity_reporting.reporting.narrative_kpi_accessor import (
    NarrativeKpiAccessor,
)
from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)


class AttentionPointsInsightWriter:
    """Transforme les signaux détectés en formulations éditoriales sans code KPI."""

    def write(  # pylint: disable=too-many-locals
        self,
        ctx: SectionEditorialContext,
    ) -> list[str]:
        """Produit des constats à partir du détail d'éligibilité et des KPI.

        :param ctx: Contexte ; ``eligibility_detail`` porte les codes machine.
        :return: Liste d'insights (peut être vide).
        """
        detail = ctx.eligibility_detail
        if detail is None:
            return []

        codes = detail.codes
        insights: list[str] = []

        if SectionEligibilityCodes.ATTENTION_IMBALANCE_TELEPHONY in codes:
            tel = NarrativeKpiAccessor.filter_global_telephony(ctx.kpi_rows)
            inc, outg = NarrativeKpiAccessor.incoming_outgoing_counts(tel)
            if inc is not None and outg is not None and inc > 0 and outg > 0:
                hi = max(inc, outg)
                lo = min(inc, outg)
                ratio = hi / lo if lo > 0 else 0.0
                dominant = "entrants" if inc > outg else "sortants"
                insights.append(
                    f"Écart marqué entre entrants et sortants (ratio ~{ratio:.1f}) : "
                    f"le sens « {dominant} » absorbe l'essentiel du volume téléphonique."
                )
            else:
                insights.append(
                    "Un signal de déséquilibre téléphonique a été relevé ; "
                    "les volumes détaillés doivent être vérifiés avant action."
                )

        if SectionEligibilityCodes.ATTENTION_TICKET_CHANNEL_DOMINANCE in codes:
            pairs = NarrativeKpiAccessor.channel_volumes_sorted(ctx.kpi_rows)
            total = sum(v for _, v in pairs)
            if pairs and total > 0:
                top_label, top_v = pairs[0]
                pct = 100.0 * top_v / total
                insights.append(
                    f"Un canal ticket concentre environ {pct:.0f} % du volume (« {top_label} ») : "
                    "surveiller la dépendance à ce mode de contact."
                )
            else:
                insights.append(
                    "Un canal ticket apparaît dominant dans les règles de détection ; "
                    "consolider les données canal avant de conclure."
                )

        return insights[:4]
