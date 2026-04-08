"""Tests d'intégration des rapports hebdomadaires."""

from datetime import date

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.reporting.report_builder import ReportBuilder
from baobab_activity_reporting.reporting.report_context import ReportContext
from baobab_activity_reporting.reporting.report_definition import ReportDefinition


class TestWeeklyReportBuilder:
    """Construction de rapports hebdomadaires."""

    def test_weekly_agent_minimum_sections_without_kpi(self) -> None:
        """Synthèse et conclusion obligatoires même sans KPI."""
        p = ReportingPeriod(date(2026, 4, 1), date(2026, 4, 7))
        ctx = ReportContext(p, [])
        model = ReportBuilder().build(ReportDefinition.weekly_activity_by_agent(), ctx)
        assert model.report_type == "weekly_activity_by_agent"
        assert len(model.sections) >= 2
        codes = [str(s.get("section_code", "")) for s in model.sections]
        assert "weekly_synthesis" in codes
        assert "weekly_conclusion" in codes

    def test_weekly_site_with_mixed_kpi(self) -> None:
        """Hebdomadaire site avec téléphonie et site."""
        p = ReportingPeriod(date(2026, 4, 1), date(2026, 4, 7))
        ctx = ReportContext(
            p,
            [
                {"code": "telephony.incoming.count", "value": 1.0},
                {"code": "site.Paris.telephony.incoming.count", "value": 1.0},
            ],
        )
        model = ReportBuilder().build(ReportDefinition.weekly_activity_by_site(), ctx)
        assert model.report_type == "weekly_activity_by_site"
        assert len(model.sections) >= 3
