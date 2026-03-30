"""Module de planification de l'ordre et du contenu éditorial."""

import logging

from baobab_activity_reporting.domain.results.section_decision import (
    SectionDecision,
)
from baobab_activity_reporting.reporting.report_context import ReportContext
from baobab_activity_reporting.reporting.report_definition import ReportDefinition
from baobab_activity_reporting.reporting.section_eligibility_evaluator import (
    SectionEligibilityEvaluator,
)

logger = logging.getLogger(__name__)


class ReportPlanner:
    """Construit le plan : sections conservées et décisions associées.

    :param evaluator: Évalueur d'éligibilité injectable (tests).
    :type evaluator: SectionEligibilityEvaluator | None

    :Example:
        >>> from datetime import date
        >>> from baobab_activity_reporting.domain.models.reporting_period import (
        ...     ReportingPeriod,
        ... )
        >>> from baobab_activity_reporting.reporting.report_context import (
        ...     ReportContext,
        ... )
        >>> from baobab_activity_reporting.reporting.report_definition import (
        ...     ReportDefinition,
        ... )
        >>> from baobab_activity_reporting.reporting.report_planner import (
        ...     ReportPlanner,
        ... )
        >>> p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        >>> ctx = ReportContext(p, [{"code": "telephony.incoming.count", "value": 1.0}])
        >>> plan, dec = ReportPlanner().plan(ReportDefinition.activity_telephony(), ctx)
        >>> any(c == "telephony_overview" for c, _, _ in plan)
        True
    """

    def __init__(
        self,
        evaluator: SectionEligibilityEvaluator | None = None,
    ) -> None:
        """Initialise le planificateur.

        :param evaluator: Évalueur personnalisé ou instance par défaut.
        :type evaluator: SectionEligibilityEvaluator | None
        """
        self._evaluator: SectionEligibilityEvaluator = (
            evaluator if evaluator is not None else SectionEligibilityEvaluator()
        )

    def plan(
        self,
        definition: ReportDefinition,
        context: ReportContext,
    ) -> tuple[
        list[tuple[str, str, frozenset[str]]],
        list[SectionDecision],
    ]:
        """Produit la liste des sections retenues et toutes les décisions.

        Les sections exclues ne figurent pas dans le premier tuple.

        :param definition: Définition métier du rapport.
        :type definition: ReportDefinition
        :param context: KPI et période disponibles.
        :type context: ReportContext
        :return: ``(sections_incluses, décisions_pour_toutes_les_sections)``.
        :rtype: tuple[list[tuple[str, str, frozenset[str]]], list[SectionDecision]]
        """
        included: list[tuple[str, str, frozenset[str]]] = []
        decisions: list[SectionDecision] = []
        for section_code, title, prefixes in definition.sections:
            decision = self._evaluator.evaluate(section_code, prefixes, context)
            decisions.append(decision)
            if decision.is_included:
                included.append((section_code, title, prefixes))
        logger.info(
            "Plan de rapport %s : %d section(s) incluse(s) sur %d",
            definition.report_type,
            len(included),
            len(definition.sections),
        )
        return included, decisions
