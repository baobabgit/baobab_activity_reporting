"""Tests pour AgentContributionNarrativeWriter."""

from datetime import date

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.reporting.agent_contribution_narrative_writer import (
    AgentContributionNarrativeWriter,
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


class TestAgentContributionNarrativeWriter:
    """Tests unitaires pour AgentContributionNarrativeWriter."""

    def test_concentration(self) -> None:
        """Deux agents : lecture de concentration."""
        ed = EditorialSectionDefinition(
            section_code="weekly_agent_contribution",
            section_title="Agents",
            section_objective="",
            required_data=frozenset(),
            optional_data=frozenset(),
            display_rules=DisplayRules.default(),
            writing_style=WritingStyle.default(),
            visibility_rule=SectionVisibilityRule.from_prefixes(
                frozenset({"agent."}),
                mandatory_in_report=False,
            ),
            table_policy=TablePolicy.default(),
        )
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 7))
        kpis = [
            {"code": "agent.Alice.x", "value": 9.0},
            {"code": "agent.Bob.x", "value": 1.0},
        ]
        full = ReportContext(p, kpis)
        ctx = SectionEditorialContext.from_editorial(
            ed,
            "weekly_activity_by_agent",
            "2026-01-01",
            "2026-01-07",
            SectionStatus.INCLUDED,
            kpis,
            full,
        )
        paras = AgentContributionNarrativeWriter().write(ctx)
        assert "Alice" in " ".join(paras)
        assert "agent.Alice" not in " ".join(paras)
