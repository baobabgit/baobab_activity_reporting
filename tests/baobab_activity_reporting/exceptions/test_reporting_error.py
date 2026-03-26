"""Tests unitaires pour ReportingError."""

import pytest

from baobab_activity_reporting.exceptions.application_exception import (
    ApplicationException,
)
from baobab_activity_reporting.exceptions.reporting_error import (
    ReportingError,
)


class TestReportingError:
    """Tests pour la classe ReportingError."""

    def test_inherits_from_application_exception(self) -> None:
        """Vérifie l'héritage depuis ApplicationException."""
        assert issubclass(ReportingError, ApplicationException)

    def test_inherits_from_exception(self) -> None:
        """Vérifie l'héritage transitif depuis Exception."""
        assert issubclass(ReportingError, Exception)

    def test_creation_with_message_only(self) -> None:
        """Vérifie la création avec un message seul."""
        exc = ReportingError("erreur reporting")
        assert exc.message == "erreur reporting"
        assert exc.details is None

    def test_creation_with_details(self) -> None:
        """Vérifie la création avec message et détails."""
        exc = ReportingError("erreur", details="contexte")
        assert exc.message == "erreur"
        assert exc.details == "contexte"

    def test_str_without_details(self) -> None:
        """Vérifie __str__ sans détails."""
        exc = ReportingError("erreur reporting")
        assert str(exc) == "erreur reporting"

    def test_str_with_details(self) -> None:
        """Vérifie __str__ avec détails."""
        exc = ReportingError("erreur", details="info")
        assert str(exc) == "erreur — info"

    def test_can_be_raised_and_caught(self) -> None:
        """Vérifie que l'exception peut être levée et capturée."""
        with pytest.raises(ReportingError, match="erreur"):
            raise ReportingError("erreur")

    def test_can_be_caught_as_application_exception(self) -> None:
        """Vérifie la capture comme ApplicationException."""
        with pytest.raises(ApplicationException):
            raise ReportingError("erreur")

    def test_repr(self) -> None:
        """Vérifie __repr__."""
        exc = ReportingError("erreur", details="det")
        result = repr(exc)
        assert "ReportingError(" in result
        assert "message='erreur'" in result
