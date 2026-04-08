"""Tests d'éligibilité sur définitions éditoriales."""

from datetime import date

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.reporting.editorial.display_rules import DisplayRules
from baobab_activity_reporting.reporting.editorial.editorial_section_definition import (
    EditorialSectionDefinition,
)
from baobab_activity_reporting.reporting.editorial.section_visibility_rule import (
    SectionVisibilityRule,
)
from baobab_activity_reporting.reporting.editorial.table_policy import TablePolicy
from baobab_activity_reporting.reporting.editorial.writing_style import WritingStyle
from baobab_activity_reporting.reporting.report_context import ReportContext
from baobab_activity_reporting.reporting.section_eligibility_evaluator import (
    SectionEligibilityEvaluator,
)


class TestSectionEligibilityEditorial:
    """Tests pour evaluate_editorial_section."""

    def _minimal_editorial(
        self,
        code: str,
        prefixes: frozenset[str],
        *,
        mandatory: bool,
    ) -> EditorialSectionDefinition:
        """Construit une section minimale pour les tests.

        :param code: Code de section.
        :type code: str
        :param prefixes: Préfixes KPI.
        :type prefixes: frozenset[str]
        :param mandatory: Section obligatoire.
        :type mandatory: bool
        :return: Définition éditoriale.
        :rtype: EditorialSectionDefinition
        """
        return EditorialSectionDefinition(
            section_code=code,
            section_title="Titre",
            section_objective="",
            required_data=frozenset(),
            optional_data=frozenset(),
            display_rules=DisplayRules.default(),
            writing_style=WritingStyle.default(),
            visibility_rule=SectionVisibilityRule.from_prefixes(
                prefixes,
                mandatory_in_report=mandatory,
            ),
            table_policy=TablePolicy.default(),
        )

    def test_mandatory_degraded_without_kpi(self) -> None:
        """Obligatoire sans KPI : statut dégradé."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        ctx = ReportContext(p, [])
        ev = SectionEligibilityEvaluator()
        ed = self._minimal_editorial(
            "s",
            frozenset({"telephony."}),
            mandatory=True,
        )
        d = ev.evaluate_editorial_section(ed, ctx)
        assert d.status == SectionStatus.DEGRADED
        assert d.is_included

    def test_optional_excluded_without_kpi(self) -> None:
        """Optionnelle sans KPI : exclue."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        ctx = ReportContext(p, [])
        ev = SectionEligibilityEvaluator()
        ed = self._minimal_editorial(
            "s",
            frozenset({"telephony."}),
            mandatory=False,
        )
        d = ev.evaluate_editorial_section(ed, ctx)
        assert d.status == SectionStatus.EXCLUDED
        assert not d.is_included
