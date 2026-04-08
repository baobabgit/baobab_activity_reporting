"""Tests pour ReportLeadNarrativeWriter."""

from datetime import date

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.reporting.report_context import ReportContext
from baobab_activity_reporting.reporting.report_lead_narrative_writer import (
    ReportLeadNarrativeWriter,
)


class TestReportLeadNarrativeWriter:
    """Tests unitaires pour ReportLeadNarrativeWriter."""

    def test_weekly_partial_data(self) -> None:
        """Hebdo sans agrégats : formulation sur données partielles."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 7))
        ctx = ReportContext(p, [])
        text = ReportLeadNarrativeWriter().write(ctx, "Titre", "weekly_activity_by_agent")
        assert "2026-01-01" in text
        assert "partiels" in text.lower()
