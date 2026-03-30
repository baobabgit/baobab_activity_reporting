"""Tests unitaires pour ReportDefinition."""

import pytest

from baobab_activity_reporting.exceptions.report_generation_error import (
    ReportGenerationError,
)
from baobab_activity_reporting.reporting.report_definition import ReportDefinition


class TestReportDefinition:
    """Tests pour la classe ReportDefinition."""

    def test_activity_telephony(self) -> None:
        """Vérifie la fabrique téléphonie."""
        d = ReportDefinition.activity_telephony()
        assert d.report_type == "activity_telephony"
        assert len(d.sections) == 2

    def test_activity_by_site(self) -> None:
        """Vérifie la fabrique site."""
        d = ReportDefinition.activity_by_site()
        assert d.report_type == "activity_by_site"
        assert d.sections[0][0] == "site_breakdown"

    def test_activity_by_agent(self) -> None:
        """Vérifie la fabrique agent."""
        d = ReportDefinition.activity_by_agent()
        assert d.report_type == "activity_by_agent"

    def test_empty_report_type_raises(self) -> None:
        """Vérifie la validation du type."""
        with pytest.raises(ReportGenerationError):
            ReportDefinition(
                "  ",
                "Titre {period_start}",
                (("a", "A", frozenset()),),
            )

    def test_empty_title_raises(self) -> None:
        """Vérifie le titre obligatoire."""
        with pytest.raises(ReportGenerationError):
            ReportDefinition(
                "x",
                "   ",
                (("a", "A", frozenset()),),
            )

    def test_no_sections_raises(self) -> None:
        """Vérifie qu'au moins une section est requise."""
        with pytest.raises(ReportGenerationError):
            ReportDefinition("x", "{period_start}", ())
