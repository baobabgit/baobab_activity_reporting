"""Tests unitaires et d'intégration pour ReportBuilder."""

from datetime import date

import pytest

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.exceptions.report_generation_error import (
    ReportGenerationError,
)
from baobab_activity_reporting.reporting.report_builder import ReportBuilder
from baobab_activity_reporting.reporting.report_context import ReportContext
from baobab_activity_reporting.reporting.report_definition import ReportDefinition


class TestReportBuilder:
    """Tests pour la classe ReportBuilder."""

    def test_build_telephony_report(self) -> None:
        """Intégration téléphonie + canaux."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        ctx = ReportContext(
            p,
            [
                {
                    "code": "telephony.incoming.count",
                    "label": "Entrants",
                    "value": 5.0,
                    "unit": "appels",
                },
                {
                    "code": "tickets.channel.EFI.count",
                    "label": "EFI",
                    "value": 3.0,
                    "unit": "tickets",
                },
            ],
        )
        model = ReportBuilder().build(ReportDefinition.activity_telephony(), ctx)
        assert len(model.sections) == 2
        assert "2026-01-01" in model.title
        assert model.report_type == "activity_telephony"
        tree = model.to_document_tree()
        assert len(tree["sections"]) == 2

    def test_build_site_report(self) -> None:
        """Rapport site."""
        p = ReportingPeriod(date(2026, 2, 1), date(2026, 2, 28))
        ctx = ReportContext(
            p,
            [{"code": "site.Paris.telephony.incoming.count", "value": 1.0}],
        )
        model = ReportBuilder().build(ReportDefinition.activity_by_site(), ctx)
        assert model.section_codes == ["site_breakdown"]

    def test_build_agent_report(self) -> None:
        """Rapport agent."""
        p = ReportingPeriod(date(2026, 3, 1), date(2026, 3, 31))
        ctx = ReportContext(
            p,
            [{"code": "agent.Jean.tickets.count", "value": 4.0}],
        )
        model = ReportBuilder().build(ReportDefinition.activity_by_agent(), ctx)
        assert model.section_codes == ["agent_breakdown"]

    def test_raises_when_no_section_eligible(self) -> None:
        """Aucune donnée : erreur métier."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        ctx = ReportContext(p, [])
        with pytest.raises(ReportGenerationError):
            ReportBuilder().build(ReportDefinition.activity_telephony(), ctx)
