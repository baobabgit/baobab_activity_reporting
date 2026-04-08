"""Insights analytiques sur l'activité téléphonique."""

from __future__ import annotations

from baobab_activity_reporting.reporting.narrative_kpi_accessor import (
    NarrativeKpiAccessor,
)
from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)


class TelephonyActivityInsightWriter:
    """Met en avant l'équilibre et l'intensité sans lister chaque compteur."""

    def write(self, ctx: SectionEditorialContext) -> list[str]:
        """Produit au plus deux insights.

        :param ctx: Contexte avec KPI téléphonie filtrés.
        :return: Phrases courtes.
        """
        rows = ctx.kpi_rows
        inc, outg = NarrativeKpiAccessor.incoming_outgoing_counts(rows)
        if inc is None and outg is None:
            return []

        insights: list[str] = []
        if inc is not None and outg is not None and (inc + outg) > 0:
            total = inc + outg
            in_pct = 100.0 * inc / total
            diff = abs(inc - outg) / total
            if diff < 0.15:
                insights.append(
                    f"Les flux entrants et sortants sont proches ({in_pct:.0f} % entrants) : "
                    "la charge est relativement équilibrée entre les deux sens."
                )
            elif inc > outg:
                insights.append(
                    f"Le poids des entrants ({in_pct:.0f} % du volume) domine : "
                    "vérifier la capacité de réponse côté prise d'appel."
                )
            else:
                insights.append(
                    f"Les sortants représentent environ {100.0 - in_pct:.0f} % du volume : "
                    "la prospection ou le rappel structure une part importante de l'activité."
                )
        elif inc is not None:
            insights.append(
                "Seul le volet entrant est renseigné de façon fiable ; "
                "toute comparaison avec les sortants reste impossible sur ce périmètre."
            )
        elif outg is not None:
            insights.append(
                "Seul le volet sortant est renseigné de façon fiable ; "
                "le besoin entrant n'est pas visible dans ces agrégats."
            )

        return insights[:2]
