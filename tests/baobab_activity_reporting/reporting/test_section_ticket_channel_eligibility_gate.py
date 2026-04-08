"""Tests pour SectionTicketChannelEligibilityGate."""

from datetime import date

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.reporting.report_context import ReportContext
from baobab_activity_reporting.reporting.section_ticket_channel_eligibility_gate import (
    SectionTicketChannelEligibilityGate,
)


class TestSectionTicketChannelEligibilityGate:
    """Porte tickets par canal."""

    def test_excluded_when_no_channel_kpis(self) -> None:
        """Sans KPI canal : exclusion."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 7))
        ctx = ReportContext(p, [{"code": "agent.x.tickets.count", "value": 1.0}])
        status, _, _ = SectionTicketChannelEligibilityGate().evaluate(ctx)
        assert status == SectionStatus.EXCLUDED

    def test_excluded_when_zero_total(self) -> None:
        """Volumes nuls : exclusion."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 7))
        ctx = ReportContext(
            p,
            [{"code": "tickets.channel.X.count", "value": 0.0}],
        )
        status, _, _ = SectionTicketChannelEligibilityGate().evaluate(ctx)
        assert status == SectionStatus.EXCLUDED

    def test_included_positive_volume(self) -> None:
        """Volume positif : inclus."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 7))
        ctx = ReportContext(
            p,
            [{"code": "tickets.channel.X.count", "value": 4.0}],
        )
        status, _, _ = SectionTicketChannelEligibilityGate().evaluate(ctx)
        assert status == SectionStatus.INCLUDED
