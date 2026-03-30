"""Tests unitaires pour SectionEligibilityEvaluator."""

from datetime import date

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.domain.results.section_decision import (
    SectionStatus,
)
from baobab_activity_reporting.reporting.report_context import ReportContext
from baobab_activity_reporting.reporting.section_eligibility_evaluator import (
    SectionEligibilityEvaluator,
)


class TestSectionEligibilityEvaluator:
    """Tests pour la classe SectionEligibilityEvaluator."""

    def test_included_when_prefix_matches(self) -> None:
        """Une section est incluse si un KPI correspond."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        ctx = ReportContext(p, [{"code": "telephony.incoming.count"}])
        ev = SectionEligibilityEvaluator()
        d = ev.evaluate("s", frozenset({"telephony."}), ctx)
        assert d.status == SectionStatus.INCLUDED

    def test_excluded_when_no_match(self) -> None:
        """Section exclue si aucun préfixe ne correspond."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        ctx = ReportContext(p, [{"code": "agent.x.tickets.count"}])
        ev = SectionEligibilityEvaluator()
        d = ev.evaluate("s", frozenset({"telephony."}), ctx)
        assert d.status == SectionStatus.EXCLUDED

    def test_always_included_when_no_prefix(self) -> None:
        """Ensemble de préfixes vide : toujours incluse."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        ctx = ReportContext(p, [])
        d = SectionEligibilityEvaluator().evaluate("intro", frozenset(), ctx)
        assert d.is_included is True
