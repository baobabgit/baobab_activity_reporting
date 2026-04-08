"""Tests pour SectionTelephonyEligibilityGate."""

from datetime import date

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.reporting.report_context import ReportContext
from baobab_activity_reporting.reporting.section_telephony_eligibility_gate import (
    SectionTelephonyEligibilityGate,
)


class TestSectionTelephonyEligibilityGate:
    """Porte téléphonie globale."""

    def test_excluded_when_both_counts_zero(self) -> None:
        """Volumes nuls : pas de section exploitable."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 7))
        ctx = ReportContext(
            p,
            [
                {"code": "telephony.incoming.count", "value": 0.0},
                {"code": "telephony.outgoing.count", "value": 0.0},
            ],
        )
        status, reason, _ = SectionTelephonyEligibilityGate().evaluate(ctx)
        assert status == SectionStatus.EXCLUDED
        assert reason is not None

    def test_degraded_single_leg(self) -> None:
        """Une jambe seule : mode dégradé."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 7))
        ctx = ReportContext(
            p,
            [
                {"code": "telephony.incoming.count", "value": 5.0},
                {"code": "telephony.outgoing.count", "value": 0.0},
            ],
        )
        status, _, _ = SectionTelephonyEligibilityGate().evaluate(ctx)
        assert status == SectionStatus.DEGRADED

    def test_included_both_legs(self) -> None:
        """Entrants et sortants actifs : inclus."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 7))
        ctx = ReportContext(
            p,
            [
                {"code": "telephony.incoming.count", "value": 1.0},
                {"code": "telephony.outgoing.count", "value": 1.0},
            ],
        )
        status, _, _ = SectionTelephonyEligibilityGate().evaluate(ctx)
        assert status == SectionStatus.INCLUDED
