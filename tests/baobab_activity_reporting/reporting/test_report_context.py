"""Tests unitaires pour ReportContext."""

from datetime import date

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.reporting.report_context import ReportContext


class TestReportContext:
    """Tests pour la classe ReportContext."""

    def test_kpi_codes(self) -> None:
        """Vérifie l'agrégation des codes."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        ctx = ReportContext(
            p,
            [
                {"code": "a"},
                {"code": "telephony.incoming.count"},
            ],
        )
        assert ctx.kpi_codes() == {"a", "telephony.incoming.count"}

    def test_kpis_matching_prefixes(self) -> None:
        """Vérifie le filtrage par préfixe."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        ctx = ReportContext(
            p,
            [
                {"code": "agent.a.tickets.count", "value": 1.0},
                {"code": "telephony.incoming.count", "value": 2.0},
            ],
        )
        rows = ctx.kpis_matching_prefixes(frozenset({"agent."}))
        assert len(rows) == 1
        assert str(rows[0]["code"]).startswith("agent.")

    def test_empty_prefixes_returns_all(self) -> None:
        """Si aucun préfixe, toutes les lignes sont retournées."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        ctx = ReportContext(p, [{"code": "a"}, {"code": "b"}])
        assert len(ctx.kpis_matching_prefixes(frozenset())) == 2

    def test_period_iso_bounds(self) -> None:
        """Vérifie les bornes ISO."""
        p = ReportingPeriod(date(2026, 6, 1), date(2026, 6, 30))
        ctx = ReportContext(p, [])
        assert ctx.period_iso_bounds() == ("2026-06-01", "2026-06-30")
