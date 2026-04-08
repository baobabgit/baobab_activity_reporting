"""Module d'évaluation de l'éligibilité des sections."""

from __future__ import annotations

import logging

from baobab_activity_reporting.domain.results.section_decision import (
    SectionDecision,
    SectionStatus,
)
from baobab_activity_reporting.domain.results.section_eligibility_codes import (
    SectionEligibilityCodes,
)
from baobab_activity_reporting.domain.results.section_eligibility_detail import (
    SectionEligibilityDetail,
)
from baobab_activity_reporting.reporting.editorial.editorial_section_definition import (
    EditorialSectionDefinition,
)
from baobab_activity_reporting.reporting.report_context import ReportContext
from baobab_activity_reporting.reporting.section_attention_signal_analyzer import (
    SectionAttentionSignalAnalyzer,
)
from baobab_activity_reporting.reporting.section_dimensional_breakdown_eligibility_gate import (
    SectionDimensionalBreakdownEligibilityGate,
)
from baobab_activity_reporting.reporting.section_telephony_eligibility_gate import (
    SectionTelephonyEligibilityGate,
)
from baobab_activity_reporting.reporting.section_ticket_channel_eligibility_gate import (
    SectionTicketChannelEligibilityGate,
)

logger = logging.getLogger(__name__)


class SectionEligibilityEvaluator:
    """Décide si une section est pertinente au regard des données disponibles.

    Ne produit aucun rendu : agrège des garde-fous métier (seuils, volumes,
    cohérence) en plus des préfixes KPI historiques pour les gabarits génériques.
    """

    def __init__(self) -> None:
        """Construit les garde-fous internes réutilisables."""
        self._telephony_gate = SectionTelephonyEligibilityGate()
        self._ticket_channel_gate = SectionTicketChannelEligibilityGate()
        self._agent_breakdown_gate = SectionDimensionalBreakdownEligibilityGate("agent")
        self._site_breakdown_gate = SectionDimensionalBreakdownEligibilityGate("site")
        self._attention_analyzer = SectionAttentionSignalAnalyzer()

    def evaluate(
        self,
        section_code: str,
        required_kpi_prefixes: frozenset[str],
        context: ReportContext,
    ) -> SectionDecision:
        """Évalue l'éligibilité d'une section (API historique par préfixes).

        :param section_code: Identifiant de section dans la définition.
        :type section_code: str
        :param required_kpi_prefixes: Préfixes historiques ; vide = toujours incluse.
        :type required_kpi_prefixes: frozenset[str]
        :param context: Contexte courant.
        :type context: ReportContext
        :return: Décision structurée.
        :rtype: SectionDecision
        """
        if not required_kpi_prefixes:
            detail = SectionEligibilityDetail(
                codes=frozenset({SectionEligibilityCodes.ALWAYS_VISIBLE}),
                notes=("aucun prérequis KPI.",),
            )
            logger.info(
                "Section %s : aucun prérequis KPI, inclusion systématique",
                section_code,
            )
            return SectionDecision(
                section_code,
                SectionStatus.INCLUDED,
                reason="aucun prérequis KPI",
                detail=detail,
            )

        routed = self._route_legacy_prefixes(section_code, required_kpi_prefixes, context)
        if routed is not None:
            status, reason, detail = routed
            return SectionDecision(section_code, status, reason, detail=detail)

        codes = context.kpi_codes()
        matched = any(
            any(code.startswith(prefix) for prefix in required_kpi_prefixes) for code in codes
        )
        if matched:
            detail = SectionEligibilityDetail(
                codes=frozenset({SectionEligibilityCodes.PREFIX_GATE_PASSED}),
                notes=("au moins un code correspond aux préfixes.",),
            )
            logger.info("Section %s : incluse (au moins un KPI correspond)", section_code)
            return SectionDecision(
                section_code,
                SectionStatus.INCLUDED,
                detail=detail,
            )

        prefix_list = ", ".join(sorted(required_kpi_prefixes))
        detail = SectionEligibilityDetail(
            codes=frozenset({SectionEligibilityCodes.PREFIX_GATE_FAILED}),
            notes=(f"préfixes: {prefix_list}",),
        )
        logger.info(
            "Section %s : exclue (préfixes requis non satisfaits)",
            section_code,
        )
        return SectionDecision(
            section_code,
            SectionStatus.EXCLUDED,
            reason=f"aucun KPI pour les préfixes requis: {prefix_list}",
            detail=detail,
        )

    def evaluate_editorial_section(
        self,
        section: EditorialSectionDefinition,
        context: ReportContext,
        *,
        peer_exploitable_included: frozenset[str] | None = None,
    ) -> SectionDecision:
        """Évalue une section à partir de sa définition éditoriale.

        :param section: Définition éditoriale complète.
        :type section: EditorialSectionDefinition
        :param context: Contexte KPI.
        :type context: ReportContext
        :param peer_exploitable_included: Sections à contenu déjà retenues
            (requis pour ``weekly_conclusion``).
        :type peer_exploitable_included: frozenset[str] | None
        :return: Décision d'inclusion, exclusion ou mode dégradé.
        :rtype: SectionDecision
        """
        code = section.section_code
        if code == "weekly_synthesis":
            return self._synthesis_decision(code)
        if code == "weekly_conclusion":
            return self._conclusion_decision(code, peer_exploitable_included)
        routed = self._route_named_editorial_section(code, context)
        if routed is not None:
            return routed
        return self._evaluate_by_prefix_gate(section, context)

    def _route_named_editorial_section(
        self,
        section_code: str,
        context: ReportContext,
    ) -> SectionDecision | None:
        """Applique les garde-fous nommés hors porte générique par préfixes.

        :param section_code: Code de section.
        :type section_code: str
        :param context: Contexte KPI.
        :type context: ReportContext
        :return: Décision si routée, sinon ``None``.
        :rtype: SectionDecision | None
        """
        if section_code in ("weekly_telephony", "telephony_overview"):
            return self._apply_telephony(section_code, context)
        if section_code in ("weekly_ticket_processing", "ticket_channels"):
            return self._apply_ticket_channel(section_code, context)
        if section_code in ("weekly_agent_contribution", "agent_breakdown"):
            return self._apply_agent_breakdown(section_code, context)
        if section_code in ("weekly_site_workload", "site_breakdown"):
            return self._apply_site_breakdown(section_code, context)
        if section_code == "weekly_attention_points":
            return self._attention_section_decision(section_code, context)
        return None

    def _synthesis_decision(self, section_code: str) -> SectionDecision:
        """Synthèse toujours visible.

        :param section_code: Code section.
        :type section_code: str
        :return: Décision incluse.
        :rtype: SectionDecision
        """
        detail = SectionEligibilityDetail(
            codes=frozenset({SectionEligibilityCodes.ALWAYS_VISIBLE}),
            notes=("synthèse obligatoire du plan hebdomadaire.",),
        )
        return SectionDecision(
            section_code,
            SectionStatus.INCLUDED,
            reason="section de synthèse toujours affichée",
            detail=detail,
        )

    def _conclusion_decision(
        self,
        section_code: str,
        peer_exploitable_included: frozenset[str] | None,
    ) -> SectionDecision:
        """Conclusion conditionnée par la matière rédactionnelle disponible.

        :param section_code: Code section.
        :type section_code: str
        :param peer_exploitable_included: Sections exploitables déjà incluses.
        :type peer_exploitable_included: frozenset[str] | None
        :return: Décision.
        :rtype: SectionDecision
        """
        if peer_exploitable_included is None:
            detail = SectionEligibilityDetail(
                codes=frozenset({SectionEligibilityCodes.EXCLUDED_NO_EXPLOITABLE_PEER_SECTIONS}),
                notes=("peer_exploitable_included non fourni — exclusion par défaut.",),
            )
            return SectionDecision(
                section_code,
                SectionStatus.EXCLUDED,
                reason="évaluation de conclusion sans jeux de sections pairs",
                detail=detail,
            )
        if not peer_exploitable_included:
            detail = SectionEligibilityDetail(
                codes=frozenset({SectionEligibilityCodes.EXCLUDED_NO_EXPLOITABLE_PEER_SECTIONS}),
                notes=("aucune section à contenu exploitable dans le plan.",),
            )
            return SectionDecision(
                section_code,
                SectionStatus.EXCLUDED,
                reason="aucune matière exploitable hors synthèse",
                detail=detail,
            )
        detail = SectionEligibilityDetail(
            codes=frozenset(
                {
                    SectionEligibilityCodes.CONCLUSION_ALLOWED,
                    SectionEligibilityCodes.MIN_DATA_SATISFIED,
                },
            ),
            notes=(f"sections_pairs={sorted(peer_exploitable_included)}",),
        )
        return SectionDecision(
            section_code,
            SectionStatus.INCLUDED,
            reason="matière exploitable présente ailleurs dans le rapport",
            detail=detail,
        )

    def _apply_telephony(self, section_code: str, context: ReportContext) -> SectionDecision:
        """Applique la porte téléphonie.

        :param section_code: Code section.
        :type section_code: str
        :param context: Contexte KPI.
        :type context: ReportContext
        :return: Décision.
        :rtype: SectionDecision
        """
        status, reason, detail = self._telephony_gate.evaluate(context)
        logger.info("Section %s : statut téléphonie=%s", section_code, status.value)
        return SectionDecision(section_code, status, reason, detail=detail)

    def _apply_ticket_channel(self, section_code: str, context: ReportContext) -> SectionDecision:
        """Applique la porte tickets canaux.

        :param section_code: Code section.
        :type section_code: str
        :param context: Contexte KPI.
        :type context: ReportContext
        :return: Décision.
        :rtype: SectionDecision
        """
        status, reason, detail = self._ticket_channel_gate.evaluate(context)
        logger.info("Section %s : statut tickets canaux=%s", section_code, status.value)
        return SectionDecision(section_code, status, reason, detail=detail)

    def _apply_agent_breakdown(self, section_code: str, context: ReportContext) -> SectionDecision:
        """Applique la porte ventilation agents.

        :param section_code: Code section.
        :type section_code: str
        :param context: Contexte KPI.
        :type context: ReportContext
        :return: Décision.
        :rtype: SectionDecision
        """
        status, reason, detail = self._agent_breakdown_gate.evaluate(context)
        logger.info("Section %s : statut ventilation agent=%s", section_code, status.value)
        return SectionDecision(section_code, status, reason, detail=detail)

    def _apply_site_breakdown(self, section_code: str, context: ReportContext) -> SectionDecision:
        """Applique la porte ventilation sites.

        :param section_code: Code section.
        :type section_code: str
        :param context: Contexte KPI.
        :type context: ReportContext
        :return: Décision.
        :rtype: SectionDecision
        """
        status, reason, detail = self._site_breakdown_gate.evaluate(context)
        logger.info("Section %s : statut ventilation site=%s", section_code, status.value)
        return SectionDecision(section_code, status, reason, detail=detail)

    def _attention_section_decision(
        self,
        section_code: str,
        context: ReportContext,
    ) -> SectionDecision:
        """Section vigilance uniquement si signaux détectés.

        :param section_code: Code section.
        :type section_code: str
        :param context: Contexte KPI.
        :type context: ReportContext
        :return: Décision.
        :rtype: SectionDecision
        """
        assessment = self._attention_analyzer.analyze(context)
        if assessment.has_attention_points:
            detail = SectionEligibilityDetail(
                codes=frozenset(assessment.signal_codes),
                notes=assessment.notes,
            )
            logger.info("Section %s : vigilance incluse (signaux détectés)", section_code)
            return SectionDecision(
                section_code,
                SectionStatus.INCLUDED,
                reason="signaux d'anomalie détectés dans les indicateurs",
                detail=detail,
            )
        detail = SectionEligibilityDetail(
            codes=frozenset(assessment.signal_codes),
            notes=assessment.notes,
        )
        logger.info("Section %s : vigilance exclue (aucun signal)", section_code)
        return SectionDecision(
            section_code,
            SectionStatus.EXCLUDED,
            reason="aucun point d'attention détecté dans les KPI",
            detail=detail,
        )

    def _evaluate_by_prefix_gate(
        self,
        section: EditorialSectionDefinition,
        context: ReportContext,
    ) -> SectionDecision:
        """Porte historique par préfixes et obligation de conserver la section.

        :param section: Définition.
        :type section: EditorialSectionDefinition
        :param context: Contexte KPI.
        :type context: ReportContext
        :return: Décision.
        :rtype: SectionDecision
        """
        rule = section.visibility_rule
        prefixes = rule.kpi_prefixes
        section_code = section.section_code
        if not prefixes:
            detail = SectionEligibilityDetail(
                codes=frozenset({SectionEligibilityCodes.ALWAYS_VISIBLE}),
                notes=("aucun prérequis KPI (porte générique).",),
            )
            return SectionDecision(
                section_code,
                SectionStatus.INCLUDED,
                reason="aucun prérequis KPI",
                detail=detail,
            )

        codes = context.kpi_codes()
        matched = any(any(code.startswith(prefix) for prefix in prefixes) for code in codes)
        if matched:
            detail = SectionEligibilityDetail(
                codes=frozenset({SectionEligibilityCodes.PREFIX_GATE_PASSED}),
                notes=("correspondance préfixe.",),
            )
            return SectionDecision(
                section_code,
                SectionStatus.INCLUDED,
                detail=detail,
            )

        if rule.mandatory_in_report:
            detail = SectionEligibilityDetail(
                codes=frozenset({SectionEligibilityCodes.MANDATORY_DEGRADED}),
                notes=("section obligatoire sans KPI correspondant.",),
            )
            return SectionDecision(
                section_code,
                SectionStatus.DEGRADED,
                reason="données KPI absentes pour une section obligatoire",
                detail=detail,
            )

        prefix_list = ", ".join(sorted(prefixes))
        detail = SectionEligibilityDetail(
            codes=frozenset({SectionEligibilityCodes.PREFIX_GATE_FAILED}),
            notes=(f"préfixes: {prefix_list}",),
        )
        return SectionDecision(
            section_code,
            SectionStatus.EXCLUDED,
            reason=f"aucun KPI pour les préfixes requis: {prefix_list}",
            detail=detail,
        )

    def _route_legacy_prefixes(
        self,
        section_code: str,
        required_kpi_prefixes: frozenset[str],
        context: ReportContext,
    ) -> tuple[SectionStatus, str | None, SectionEligibilityDetail] | None:
        """Tente une évaluation stricte pour les triplets legacy connus.

        :param section_code: Code section.
        :type section_code: str
        :param required_kpi_prefixes: Préfixes du triplet legacy.
        :type required_kpi_prefixes: frozenset[str]
        :param context: Contexte KPI.
        :type context: ReportContext
        :return: Décision si routée, sinon ``None``.
        :rtype: tuple[SectionStatus, str | None, SectionEligibilityDetail] | None
        """
        if required_kpi_prefixes == frozenset({"telephony."}):
            return self._telephony_gate.evaluate(context)
        if required_kpi_prefixes == frozenset({"tickets.channel."}):
            return self._ticket_channel_gate.evaluate(context)
        if required_kpi_prefixes == frozenset({"agent."}):
            return self._agent_breakdown_gate.evaluate(context)
        if required_kpi_prefixes == frozenset({"site."}):
            return self._site_breakdown_gate.evaluate(context)
        _ = section_code
        return None
