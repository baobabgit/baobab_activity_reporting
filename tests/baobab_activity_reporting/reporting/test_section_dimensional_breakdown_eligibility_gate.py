"""Tests pour SectionDimensionalBreakdownEligibilityGate."""

from datetime import date

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.reporting.report_context import ReportContext
from baobab_activity_reporting.reporting.section_dimensional_breakdown_eligibility_gate import (
    SectionDimensionalBreakdownEligibilityGate,
)


class TestSectionDimensionalBreakdownEligibilityGate:
    """Ventilation agent / site."""

    def test_agent_excluded_single_entity(self) -> None:
        """Un seul agent : pas de répartition fiable."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 7))
        ctx = ReportContext(
            p,
            [{"code": "agent.A.telephony.incoming.count", "value": 1.0}],
        )
        status, _, _ = SectionDimensionalBreakdownEligibilityGate("agent").evaluate(ctx)
        assert status == SectionStatus.EXCLUDED

    def test_agent_included_two_entities(self) -> None:
        """Deux agents : ventilation OK."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 7))
        ctx = ReportContext(
            p,
            [
                {"code": "agent.A.telephony.incoming.count", "value": 1.0},
                {"code": "agent.B.telephony.incoming.count", "value": 2.0},
            ],
        )
        status, _, _ = SectionDimensionalBreakdownEligibilityGate("agent").evaluate(ctx)
        assert status == SectionStatus.INCLUDED

    def test_site_gate_symmetric(self) -> None:
        """Même logique pour les sites."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 7))
        ctx = ReportContext(
            p,
            [
                {"code": "site.Paris.telephony.incoming.count", "value": 1.0},
                {"code": "site.Lyon.telephony.incoming.count", "value": 1.0},
            ],
        )
        status, _, _ = SectionDimensionalBreakdownEligibilityGate("site").evaluate(ctx)
        assert status == SectionStatus.INCLUDED
