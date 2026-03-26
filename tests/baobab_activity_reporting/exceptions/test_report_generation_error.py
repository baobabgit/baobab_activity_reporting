"""Tests unitaires pour ReportGenerationError."""

import pytest

from baobab_activity_reporting.exceptions.report_generation_error import (
    ReportGenerationError,
)
from baobab_activity_reporting.exceptions.reporting_error import (
    ReportingError,
)


class TestReportGenerationError:
    """Tests pour la classe ReportGenerationError."""

    def test_inherits_from_reporting_error(self) -> None:
        """Vérifie l'héritage depuis ReportingError."""
        assert issubclass(ReportGenerationError, ReportingError)

    def test_creation_with_message_only(self) -> None:
        """Vérifie la création avec un message seul."""
        exc = ReportGenerationError("données insuffisantes")
        assert exc.message == "données insuffisantes"
        assert exc.report_type is None
        assert exc.details is None

    def test_creation_with_report_type(self) -> None:
        """Vérifie la création avec un type de rapport."""
        exc = ReportGenerationError("erreur", report_type="téléphonie")
        assert exc.report_type == "téléphonie"
        assert exc.details == "rapport: téléphonie"

    def test_creation_with_report_type_and_details(self) -> None:
        """Vérifie la création avec type et détails."""
        exc = ReportGenerationError(
            "erreur",
            report_type="téléphonie",
            details="section vide",
        )
        assert exc.details == "rapport: téléphonie, section vide"

    def test_creation_with_details_only(self) -> None:
        """Vérifie la création avec détails sans type."""
        exc = ReportGenerationError("erreur", details="info")
        assert exc.report_type is None
        assert exc.details == "info"

    def test_str_with_report_type(self) -> None:
        """Vérifie __str__ avec type de rapport."""
        exc = ReportGenerationError("erreur", report_type="agent")
        assert str(exc) == "erreur — rapport: agent"

    def test_can_be_raised_and_caught(self) -> None:
        """Vérifie que l'exception peut être levée et capturée."""
        with pytest.raises(ReportGenerationError, match="erreur"):
            raise ReportGenerationError("erreur")

    def test_can_be_caught_as_reporting_error(self) -> None:
        """Vérifie la capture comme ReportingError."""
        with pytest.raises(ReportingError):
            raise ReportGenerationError("erreur")
