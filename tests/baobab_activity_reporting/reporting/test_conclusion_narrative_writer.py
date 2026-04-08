"""Tests pour ConclusionNarrativeWriter."""

from datetime import date

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.reporting.conclusion_narrative_writer import (
    ConclusionNarrativeWriter,
)
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
from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)


class TestConclusionNarrativeWriter:
    """Tests unitaires pour ConclusionNarrativeWriter."""

    def _ctx(self, report_type: str) -> SectionEditorialContext:
        """Contexte conclusion minimal."""
        ed = EditorialSectionDefinition(
            section_code="weekly_conclusion",
            section_title="Conclusion",
            section_objective="Clore.",
            required_data=frozenset(),
            optional_data=frozenset(),
            display_rules=DisplayRules.default(),
            writing_style=WritingStyle.default(),
            visibility_rule=SectionVisibilityRule.from_prefixes(
                frozenset(),
                mandatory_in_report=True,
            ),
            table_policy=TablePolicy.default(),
        )
        p = ReportingPeriod(date(2026, 4, 1), date(2026, 4, 7))
        full = ReportContext(p, [])
        return SectionEditorialContext.from_editorial(
            ed,
            report_type,
            "2026-04-01",
            "2026-04-07",
            SectionStatus.INCLUDED,
            [],
            full,
        )

    def test_conclusion_agent_weekly(self) -> None:
        """Conclusion rapport hebdo agent."""
        text = " ".join(ConclusionNarrativeWriter().write(self._ctx("weekly_activity_by_agent")))
        assert "agent" in text.lower()

    def test_conclusion_site_weekly(self) -> None:
        """Conclusion rapport hebdo site."""
        text = " ".join(ConclusionNarrativeWriter().write(self._ctx("weekly_activity_by_site")))
        assert "site" in text.lower()

    def test_conclusion_non_weekly_template(self) -> None:
        """Autres types de rapport : formulation générique."""
        text = " ".join(ConclusionNarrativeWriter().write(self._ctx("activity_telephony")))
        assert "indicateurs" in text.lower()
