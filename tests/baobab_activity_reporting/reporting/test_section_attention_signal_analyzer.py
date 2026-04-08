"""Tests pour SectionAttentionSignalAnalyzer."""

from datetime import date

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.domain.results.section_eligibility_codes import (
    SectionEligibilityCodes,
)
from baobab_activity_reporting.reporting.report_context import ReportContext
from baobab_activity_reporting.reporting.section_attention_signal_analyzer import (
    SectionAttentionSignalAnalyzer,
)


class TestSectionAttentionSignalAnalyzer:
    """Signaux de vigilance."""

    def test_no_signals_when_balanced(self) -> None:
        """Pas de déséquilibre marquant : aucun point d'attention."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 7))
        ctx = ReportContext(
            p,
            [
                {"code": "telephony.incoming.count", "value": 10.0},
                {"code": "telephony.outgoing.count", "value": 10.0},
            ],
        )
        a = SectionAttentionSignalAnalyzer().analyze(ctx)
        assert a.has_attention_points is False
        assert SectionEligibilityCodes.EXCLUDED_NO_ATTENTION_SIGNALS in a.signal_codes

    def test_telephony_imbalance_detected(self) -> None:
        """Ratio entrants/sortants élevé : signal."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 7))
        ctx = ReportContext(
            p,
            [
                {"code": "telephony.incoming.count", "value": 50.0},
                {"code": "telephony.outgoing.count", "value": 5.0},
            ],
        )
        a = SectionAttentionSignalAnalyzer().analyze(ctx)
        assert a.has_attention_points is True
        assert SectionEligibilityCodes.ATTENTION_IMBALANCE_TELEPHONY in a.signal_codes

    def test_ticket_channel_dominance(self) -> None:
        """Un canal domine : signal."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 7))
        ctx = ReportContext(
            p,
            [
                {"code": "tickets.channel.A.count", "value": 90.0},
                {"code": "tickets.channel.B.count", "value": 10.0},
            ],
        )
        a = SectionAttentionSignalAnalyzer().analyze(ctx)
        assert a.has_attention_points is True
        assert SectionEligibilityCodes.ATTENTION_TICKET_CHANNEL_DOMINANCE in a.signal_codes
