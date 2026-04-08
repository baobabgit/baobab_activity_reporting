"""Règles d'éligibilité pour les sections fondées sur les tickets par canal."""

from __future__ import annotations

from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.domain.results.section_eligibility_codes import (
    SectionEligibilityCodes,
)
from baobab_activity_reporting.domain.results.section_eligibility_detail import (
    SectionEligibilityDetail,
)
from baobab_activity_reporting.reporting.kpi_value_assessor import KpiValueAssessor
from baobab_activity_reporting.reporting.report_context import ReportContext


class SectionTicketChannelEligibilityGate:
    """Contrôle qu'un volume ticket canal réellement positif est disponible."""

    def evaluate(
        self, context: ReportContext
    ) -> tuple[SectionStatus, str | None, SectionEligibilityDetail]:
        """Décide si la section tickets / canaux est pertinente.

        :param context: KPI disponibles.
        :type context: ReportContext
        :return: Statut, raison et détail.
        :rtype: tuple[SectionStatus, str | None, SectionEligibilityDetail]
        """
        has_channel = any(
            str(r.get("code", "")).startswith("tickets.channel.") for r in context.kpi_records
        )
        if not has_channel:
            detail = SectionEligibilityDetail(
                codes=frozenset({SectionEligibilityCodes.EXCLUDED_NO_TICKET_VOLUME}),
                notes=("aucun KPI tickets.channel.* présent.",),
            )
            return (
                SectionStatus.EXCLUDED,
                "aucun indicateur de tickets par canal",
                detail,
            )

        total, reliable = KpiValueAssessor.sum_channel_ticket_counts(context)
        if not reliable:
            detail = SectionEligibilityDetail(
                codes=frozenset({SectionEligibilityCodes.EXCLUDED_TICKET_VALUES_UNRELIABLE}),
                notes=("valeur de comptage canal invalide ou négative.",),
            )
            return (
                SectionStatus.EXCLUDED,
                "données tickets par canal non fiables",
                detail,
            )

        if total <= 0:
            detail = SectionEligibilityDetail(
                codes=frozenset({SectionEligibilityCodes.EXCLUDED_NO_TICKET_VOLUME}),
                notes=("somme des volumes canaux nulle.",),
            )
            return (
                SectionStatus.EXCLUDED,
                "aucun volume ticket exploitable sur les canaux",
                detail,
            )

        detail = SectionEligibilityDetail(
            codes=frozenset({SectionEligibilityCodes.MIN_DATA_SATISFIED}),
            notes=(f"volume total canaux={total}.",),
        )
        return SectionStatus.INCLUDED, None, detail
