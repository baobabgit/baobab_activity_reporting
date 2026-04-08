"""Tests unitaires pour ReportDefinition."""

import pytest

from baobab_activity_reporting.exceptions.report_generation_error import (
    ReportGenerationError,
)
from baobab_activity_reporting.reporting.report_definition import (
    ReportDefinition,
    _editorial_from_legacy,
)


class TestReportDefinition:
    """Tests pour la classe ReportDefinition."""

    def test_activity_telephony(self) -> None:
        """Vérifie la fabrique téléphonie."""
        d = ReportDefinition.activity_telephony()
        assert d.report_type == "activity_telephony"
        assert len(d.sections) == 2
        assert len(d.editorial_sections) == 2

    def test_activity_by_site(self) -> None:
        """Vérifie la fabrique site."""
        d = ReportDefinition.activity_by_site()
        assert d.report_type == "activity_by_site"
        assert d.sections[0][0] == "site_breakdown"
        assert d.editorial_sections[0].section_code == "site_breakdown"

    def test_activity_by_agent(self) -> None:
        """Vérifie la fabrique agent."""
        d = ReportDefinition.activity_by_agent()
        assert d.report_type == "activity_by_agent"

    def test_weekly_agent_has_six_sections(self) -> None:
        """Rapport hebdomadaire agent : six sections éditoriales."""
        d = ReportDefinition.weekly_activity_by_agent()
        assert d.report_type == "weekly_activity_by_agent"
        assert len(d.editorial_sections) == 6
        codes = [s.section_code for s in d.editorial_sections]
        assert codes[-1] == "weekly_conclusion"
        assert "weekly_agent_contribution" in codes

    def test_weekly_site_has_site_workload_section(self) -> None:
        """Rapport hebdomadaire site : section charge site."""
        d = ReportDefinition.weekly_activity_by_site()
        assert d.report_type == "weekly_activity_by_site"
        codes = [s.section_code for s in d.editorial_sections]
        assert "weekly_site_workload" in codes

    def test_empty_report_type_raises(self) -> None:
        """Vérifie la validation du type."""
        with pytest.raises(ReportGenerationError):
            ReportDefinition(
                "  ",
                "Titre {period_start}",
                (_editorial_from_legacy("a", "A", frozenset()),),
            )

    def test_empty_title_raises(self) -> None:
        """Vérifie le titre obligatoire."""
        with pytest.raises(ReportGenerationError):
            ReportDefinition(
                "x",
                "   ",
                (_editorial_from_legacy("a", "A", frozenset()),),
            )

    def test_no_sections_raises(self) -> None:
        """Vérifie qu'au moins une section est requise."""
        with pytest.raises(ReportGenerationError):
            ReportDefinition("x", "{period_start}", ())
