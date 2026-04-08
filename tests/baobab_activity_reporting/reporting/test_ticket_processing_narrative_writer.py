"""Tests pour TicketProcessingNarrativeWriter."""

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
from baobab_activity_reporting.reporting.section_editorial_context import (
    SectionEditorialContext,
)
from baobab_activity_reporting.reporting.ticket_processing_narrative_writer import (
    TicketProcessingNarrativeWriter,
)


class TestTicketProcessingNarrativeWriter:
    """Tests unitaires pour TicketProcessingNarrativeWriter."""

    def test_multi_channel(self) -> None:
        """Plusieurs canaux : pas de liste exhaustive."""
        ed = EditorialSectionDefinition(
            section_code="weekly_ticket_processing",
            section_title="Tickets",
            section_objective="",
            required_data=frozenset(),
            optional_data=frozenset(),
            display_rules=DisplayRules.default(),
            writing_style=WritingStyle.default(),
            visibility_rule=SectionVisibilityRule.from_prefixes(
                frozenset({"tickets."}),
                mandatory_in_report=False,
            ),
            table_policy=TablePolicy.default(),
        )
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 7))
        kpis = [
            {"code": "tickets.channel.A.count", "label": "A", "value": 20.0},
            {"code": "tickets.channel.B.count", "label": "B", "value": 80.0},
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
        paras = TicketProcessingNarrativeWriter().write(ctx)
        assert len(paras) >= 1
        assert "tickets.channel" not in " ".join(paras)
