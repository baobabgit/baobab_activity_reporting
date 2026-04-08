"""Règles d'éligibilité métier pour les sections téléphonie globales."""

from __future__ import annotations

import math

from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.domain.results.section_eligibility_codes import (
    SectionEligibilityCodes,
)
from baobab_activity_reporting.domain.results.section_eligibility_detail import (
    SectionEligibilityDetail,
)
from baobab_activity_reporting.reporting.kpi_value_assessor import KpiValueAssessor
from baobab_activity_reporting.reporting.report_context import ReportContext


class SectionTelephonyEligibilityGate:
    """Vérifie la disponibilité d'indicateurs téléphoniques globaux exploitables.

    Exige des volumes globaux cohérents (entrants / sortants), pas seulement
    l'existence de codes KPI.
    """

    _INCOMING_COUNT = "telephony.incoming.count"
    _OUTGOING_COUNT = "telephony.outgoing.count"

    def evaluate(
        self, context: ReportContext
    ) -> tuple[SectionStatus, str | None, SectionEligibilityDetail]:
        """Décide du statut pour une section téléphonie globale.

        :param context: KPI disponibles.
        :type context: ReportContext
        :return: Statut, raison courte et détail diagnostic.
        :rtype: tuple[SectionStatus, str | None, SectionEligibilityDetail]
        """
        if not any(str(r.get("code", "")).startswith("telephony.") for r in context.kpi_records):
            detail = SectionEligibilityDetail(
                codes=frozenset({SectionEligibilityCodes.EXCLUDED_NO_TELEPHONY_METRICS}),
                notes=("aucun code KPI sous le préfixe telephony.",),
            )
            return (
                SectionStatus.EXCLUDED,
                "aucune donnée téléphonique globale",
                detail,
            )

        inc = KpiValueAssessor.numeric_for_code(context, self._INCOMING_COUNT)
        out = KpiValueAssessor.numeric_for_code(context, self._OUTGOING_COUNT)

        if inc is not None and (inc < 0 or not math.isfinite(inc)):
            return self._unreliable("valeur entrants invalide")
        if out is not None and (out < 0 or not math.isfinite(out)):
            return self._unreliable("valeur sortants invalide")

        inc_v = 0.0 if inc is None else inc
        out_v = 0.0 if out is None else out

        if inc_v == 0 and out_v == 0:
            detail = SectionEligibilityDetail(
                codes=frozenset({SectionEligibilityCodes.EXCLUDED_NO_TELEPHONY_METRICS}),
                notes=("volumes entrants et sortants nuls ou absents.",),
            )
            return (
                SectionStatus.EXCLUDED,
                "aucune activité téléphonique mesurable sur la période",
                detail,
            )

        if inc_v > 0 and out_v > 0:
            detail = SectionEligibilityDetail(
                codes=frozenset(
                    {
                        SectionEligibilityCodes.MIN_DATA_SATISFIED,
                        SectionEligibilityCodes.TELEPHONY_BALANCED,
                    },
                ),
                notes=("entrants et sortants strictement positifs.",),
            )
            return SectionStatus.INCLUDED, None, detail

        detail = SectionEligibilityDetail(
            codes=frozenset(
                {
                    SectionEligibilityCodes.TELEPHONY_PARTIAL_SINGLE_LEG,
                    SectionEligibilityCodes.MIN_DATA_SATISFIED,
                },
            ),
            notes=("une seule jambe téléphonique avec activité.",),
        )
        return (
            SectionStatus.DEGRADED,
            "données téléphoniques partielles (une jambe sans activité)",
            detail,
        )

    def _unreliable(self, note: str) -> tuple[SectionStatus, str | None, SectionEligibilityDetail]:
        """Construit une exclusion pour valeurs non fiables.

        :param note: Détail court.
        :type note: str
        :return: Triplet statut / raison / détail.
        :rtype: tuple[SectionStatus, str | None, SectionEligibilityDetail]
        """
        detail = SectionEligibilityDetail(
            codes=frozenset({SectionEligibilityCodes.EXCLUDED_TELEPHONY_VALUES_UNRELIABLE}),
            notes=(note,),
        )
        return (
            SectionStatus.EXCLUDED,
            "données téléphoniques non fiables",
            detail,
        )
