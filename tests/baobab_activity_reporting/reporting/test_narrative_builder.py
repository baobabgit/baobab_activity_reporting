"""Tests unitaires pour NarrativeBuilder."""

from datetime import date

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.reporting.narrative_builder import NarrativeBuilder
from baobab_activity_reporting.reporting.report_context import ReportContext


class TestNarrativeBuilder:
    """Tests pour la classe NarrativeBuilder."""

    def test_lead_paragraph(self) -> None:
        """Vérifie l'introduction globale."""
        p = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        ctx = ReportContext(p, [{"code": "x", "value": 1.0}])
        text = NarrativeBuilder().lead_paragraph(ctx, "Titre")
        assert "2026-01-01" in text
        assert "2026-01-31" in text

    def test_section_intro_zero_kpi(self) -> None:
        """Intro sans indicateur."""
        nb = NarrativeBuilder().section_intro("c", "Titre", 0)
        assert "aucun indicateur" in nb.lower()
