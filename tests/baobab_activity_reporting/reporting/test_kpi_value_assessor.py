"""Tests pour KpiValueAssessor."""

from datetime import date

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.reporting.kpi_value_assessor import KpiValueAssessor
from baobab_activity_reporting.reporting.report_context import ReportContext


class TestKpiValueAssessor:
    """Lecture numérique des KPI."""

    def test_numeric_for_code(self) -> None:
        """Retrouve la valeur par code exact."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 7))
        ctx = ReportContext(p, [{"code": "k.a", "value": 2.5}])
        assert KpiValueAssessor.numeric_for_code(ctx, "k.a") == 2.5
        assert KpiValueAssessor.numeric_for_code(ctx, "missing") is None

    def test_sum_channel_tickets(self) -> None:
        """Somme les volumes canaux."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 7))
        ctx = ReportContext(
            p,
            [
                {"code": "tickets.channel.A.count", "value": 1.0},
                {"code": "tickets.channel.B.count", "value": 2.0},
            ],
        )
        total, ok = KpiValueAssessor.sum_channel_ticket_counts(ctx)
        assert ok is True
        assert total == 3.0
