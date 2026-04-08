"""Tests unitaires pour ReportPlanner."""

from datetime import date

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.reporting.report_context import ReportContext
from baobab_activity_reporting.reporting.report_definition import ReportDefinition
from baobab_activity_reporting.reporting.report_planner import ReportPlanner


class TestReportPlanner:
    """Tests pour la classe ReportPlanner."""

    def test_drops_section_without_data(self) -> None:
        """La section tickets disparaît sans KPI canaux."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        ctx = ReportContext(
            p,
            [{"code": "telephony.incoming.count", "value": 1.0}],
        )
        included, decisions = ReportPlanner().plan(
            ReportDefinition.activity_telephony(),
            ctx,
        )
        codes = [ed.section_code for ed, _ in included]
        assert codes == ["telephony_overview"]
        assert len(decisions) == 2

    def test_keeps_multiple_sections(self) -> None:
        """Plusieurs sections si les données sont là."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        ctx = ReportContext(
            p,
            [
                {"code": "telephony.incoming.count", "value": 1.0},
                {"code": "tickets.channel.EFI.count", "value": 2.0},
            ],
        )
        included, _ = ReportPlanner().plan(
            ReportDefinition.activity_telephony(),
            ctx,
        )
        assert len(included) == 2
