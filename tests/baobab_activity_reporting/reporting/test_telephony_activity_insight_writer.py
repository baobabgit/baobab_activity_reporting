"""Tests pour TelephonyActivityInsightWriter."""

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
from baobab_activity_reporting.reporting.telephony_activity_insight_writer import (
    TelephonyActivityInsightWriter,
)


class TestTelephonyActivityInsightWriter:
    """Tests unitaires pour TelephonyActivityInsightWriter."""

    def test_balance_insight(self) -> None:
        """Constat d'équilibre sans liste de compteurs."""
        ed = EditorialSectionDefinition(
            section_code="weekly_telephony",
            section_title="Tél",
            section_objective="",
            required_data=frozenset(),
            optional_data=frozenset(),
            display_rules=DisplayRules.default(),
            writing_style=WritingStyle.default(),
            visibility_rule=SectionVisibilityRule.from_prefixes(
                frozenset({"telephony."}),
                mandatory_in_report=False,
            ),
            table_policy=TablePolicy.default(),
        )
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 7))
        kpis = [
            {"code": "telephony.incoming.count", "value": 10.0},
            {"code": "telephony.outgoing.count", "value": 10.0},
        ]
        full = ReportContext(p, kpis)
        ctx = SectionEditorialContext.from_editorial(
            ed,
            "weekly_activity_by_site",
            "2026-01-01",
            "2026-01-07",
            SectionStatus.INCLUDED,
            kpis,
            full,
        )
        lines = TelephonyActivityInsightWriter().write(ctx)
        assert len(lines) >= 1
        assert "Volume total" not in " ".join(lines)
