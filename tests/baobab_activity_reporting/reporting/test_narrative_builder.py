"""Tests unitaires pour NarrativeBuilder."""

from datetime import date

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.domain.results.section_decision import SectionStatus
from baobab_activity_reporting.reporting.narrative_builder import NarrativeBuilder
from baobab_activity_reporting.reporting.report_context import ReportContext
from baobab_activity_reporting.reporting.report_definition import ReportDefinition


class TestNarrativeBuilder:
    """Tests pour la classe NarrativeBuilder."""

    def test_lead_paragraph_activity_telephony(self) -> None:
        """Introduction contextualisée pour le rapport téléphonie."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        ctx = ReportContext(
            p,
            [
                {"code": "telephony.incoming.count", "value": 5.0},
                {"code": "telephony.outgoing.count", "value": 5.0},
            ],
        )
        text = NarrativeBuilder().lead_paragraph(ctx, "Titre", "activity_telephony")
        assert "2026-01-01" in text
        assert "2026-01-31" in text
        assert "téléphonie" in text.lower()

    def test_section_narrative_delegates_to_writer(self) -> None:
        """Les blocs narratifs proviennent du moteur par section."""
        definition = ReportDefinition.activity_telephony()
        editorial = definition.editorial_sections[0]
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 7))
        ctx = ReportContext(
            p,
            [
                {"code": "telephony.incoming.count", "value": 3.0},
                {"code": "telephony.outgoing.count", "value": 1.0},
            ],
        )
        blocks = NarrativeBuilder().section_narrative_blocks(
            editorial,
            ctx.kpi_records,
            SectionStatus.INCLUDED,
            definition.report_type,
            ctx,
        )
        assert len(blocks) >= 1
        joined = " ".join(blocks)
        assert "telephony.incoming" not in joined
