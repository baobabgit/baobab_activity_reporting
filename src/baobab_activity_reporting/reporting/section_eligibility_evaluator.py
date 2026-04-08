"""Module d'évaluation de l'éligibilité des sections."""

import logging

from baobab_activity_reporting.domain.results.section_decision import (
    SectionDecision,
    SectionStatus,
)
from baobab_activity_reporting.reporting.editorial.editorial_section_definition import (
    EditorialSectionDefinition,
)
from baobab_activity_reporting.reporting.report_context import ReportContext

logger = logging.getLogger(__name__)


class SectionEligibilityEvaluator:
    """Décide si une section peut être incluse selon les KPI disponibles.

    Règle : si aucun préfixe n'est requis (ensemble vide), la section est
    ``INCLUDED``. Sinon, au moins un code KPI du contexte doit commencer
    par l'un des préfixes ; sinon la section est ``EXCLUDED``.

    :Example:
        >>> from datetime import date
        >>> from baobab_activity_reporting.domain.models.reporting_period import (
        ...     ReportingPeriod,
        ... )
        >>> from baobab_activity_reporting.reporting.report_context import (
        ...     ReportContext,
        ... )
        >>> from baobab_activity_reporting.reporting.section_eligibility_evaluator import (
        ...     SectionEligibilityEvaluator,
        ... )
        >>> p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        >>> ctx = ReportContext(p, [{"code": "telephony.incoming.count", "value": 1.0}])
        >>> ev = SectionEligibilityEvaluator()
        >>> d = ev.evaluate("s", frozenset({"telephony."}), ctx)
        >>> d.is_included
        True
    """

    def evaluate(
        self,
        section_code: str,
        required_kpi_prefixes: frozenset[str],
        context: ReportContext,
    ) -> SectionDecision:
        """Évalue l'éligibilité d'une section.

        :param section_code: Identifiant de section dans la définition.
        :type section_code: str
        :param required_kpi_prefixes: Préfixes à satisfaire ; vide = toujours incluse.
        :type required_kpi_prefixes: frozenset[str]
        :param context: Contexte courant.
        :type context: ReportContext
        :return: Décision structurée.
        :rtype: SectionDecision
        """
        if not required_kpi_prefixes:
            logger.info(
                "Section %s : aucun prérequis KPI, inclusion systématique",
                section_code,
            )
            return SectionDecision(
                section_code,
                SectionStatus.INCLUDED,
                reason="aucun prérequis KPI",
            )

        codes = context.kpi_codes()
        matched = any(
            any(code.startswith(prefix) for prefix in required_kpi_prefixes) for code in codes
        )
        if matched:
            logger.info("Section %s : incluse (au moins un KPI correspond)", section_code)
            return SectionDecision(
                section_code,
                SectionStatus.INCLUDED,
            )

        logger.info(
            "Section %s : exclue (préfixes requis non satisfaits)",
            section_code,
        )
        prefix_list = ", ".join(sorted(required_kpi_prefixes))
        return SectionDecision(
            section_code,
            SectionStatus.EXCLUDED,
            reason=f"aucun KPI pour les préfixes requis: {prefix_list}",
        )

    def evaluate_editorial_section(
        self,
        section: EditorialSectionDefinition,
        context: ReportContext,
    ) -> SectionDecision:
        """Évalue une section à partir de sa définition éditoriale.

        Applique la porte sur préfixes KPI et le caractère obligatoire
        (section dégradée si données manquantes mais obligatoire).

        :param section: Définition éditoriale complète.
        :type section: EditorialSectionDefinition
        :param context: Contexte KPI.
        :type context: ReportContext
        :return: Décision d'inclusion, exclusion ou mode dégradé.
        :rtype: SectionDecision
        """
        rule = section.visibility_rule
        prefixes = rule.kpi_prefixes
        section_code = section.section_code
        if not prefixes:
            logger.info(
                "Section %s : aucun prérequis KPI, inclusion systématique",
                section_code,
            )
            return SectionDecision(
                section_code,
                SectionStatus.INCLUDED,
                reason="aucun prérequis KPI",
            )

        codes = context.kpi_codes()
        matched = any(any(code.startswith(prefix) for prefix in prefixes) for code in codes)
        if matched:
            logger.info("Section %s : incluse (au moins un KPI correspond)", section_code)
            return SectionDecision(
                section_code,
                SectionStatus.INCLUDED,
            )

        if rule.mandatory_in_report:
            logger.info(
                "Section %s : incluse en mode dégradé (obligatoire, KPI absents)",
                section_code,
            )
            return SectionDecision(
                section_code,
                SectionStatus.DEGRADED,
                reason="données KPI absentes pour une section obligatoire",
            )

        logger.info(
            "Section %s : exclue (préfixes requis non satisfaits)",
            section_code,
        )
        prefix_list = ", ".join(sorted(prefixes))
        return SectionDecision(
            section_code,
            SectionStatus.EXCLUDED,
            reason=f"aucun KPI pour les préfixes requis: {prefix_list}",
        )
