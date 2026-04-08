"""Tests unitaires pour InsightBuilder."""

from datetime import date

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.reporting.insight_builder import InsightBuilder
from baobab_activity_reporting.reporting.report_context import ReportContext
from baobab_activity_reporting.reporting.report_definition import ReportDefinition


class TestInsightBuilder:
    """Tests pour la classe InsightBuilder."""

    def test_telephony_insights_not_a_kpi_list(self) -> None:
        """Insights téléphonie : constat analytique, pas inventaire."""
        definition = ReportDefinition.activity_telephony()
        telephony_ed = definition.editorial_sections[0]
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        ctx = ReportContext(
            p,
            [
                {"code": "telephony.incoming.count", "value": 10.0},
                {"code": "telephony.outgoing.count", "value": 10.0},
            ],
        )
        out = InsightBuilder().insights_for_section(
            telephony_ed,
            ctx.kpi_records,
            SectionStatus.INCLUDED,
            definition.report_type,
            ctx,
        )
        assert len(out) >= 1
        assert "telephony.incoming.count" not in " ".join(out)

    def test_channel_insights_synthesized(self) -> None:
        """Mix canaux : au plus deux phrases, sans une ligne par canal."""
        definition = ReportDefinition.activity_telephony()
        ticket_ed = definition.editorial_sections[1]
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        ctx = ReportContext(
            p,
            [
                {"code": "tickets.channel.EFI.count", "label": "EFI", "value": 30.0},
                {"code": "tickets.channel.EDI.count", "label": "EDI", "value": 70.0},
            ],
        )
        lines = InsightBuilder().insights_for_section(
            ticket_ed,
            ctx.kpi_records,
            SectionStatus.INCLUDED,
            definition.report_type,
            ctx,
        )
        assert len(lines) <= 2
        assert not all("Canal " in line and "%" in line for line in lines)

    def test_fallback_empty_insights(self) -> None:
        """Section inconnue : pas de liste mécanique de KPI."""
        definition = ReportDefinition.activity_by_agent()
        editorial = definition.editorial_sections[0]
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        ctx = ReportContext(p, [{"code": "agent.X.y", "value": 1.0}])
        custom = InsightBuilder(
            section_writers={},
        )
        g = custom.insights_for_section(
            editorial,
            ctx.kpi_records,
            SectionStatus.INCLUDED,
            definition.report_type,
            ctx,
        )
        assert g == []
