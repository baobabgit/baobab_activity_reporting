"""Tests unitaires pour ExtractionError."""

import pytest

from baobab_activity_reporting.exceptions.application_exception import (
    ApplicationException,
)
from baobab_activity_reporting.exceptions.extraction_error import (
    ExtractionError,
)
from baobab_activity_reporting.exceptions.reporting_error import (
    ReportingError,
)


class TestExtractionError:
    """Tests pour la classe ExtractionError."""

    def test_inherits_from_reporting_error(self) -> None:
        """Vérifie l'héritage depuis ReportingError."""
        assert issubclass(ExtractionError, ReportingError)

    def test_inherits_from_application_exception(self) -> None:
        """Vérifie l'héritage transitif depuis ApplicationException."""
        assert issubclass(ExtractionError, ApplicationException)

    def test_creation_with_message_only(self) -> None:
        """Vérifie la création avec un message seul."""
        exc = ExtractionError("fichier introuvable")
        assert exc.message == "fichier introuvable"
        assert exc.source_name is None
        assert exc.details is None

    def test_creation_with_source_name(self) -> None:
        """Vérifie la création avec un nom de source."""
        exc = ExtractionError("erreur", source_name="appels.csv")
        assert exc.source_name == "appels.csv"
        assert exc.details == "source: appels.csv"

    def test_creation_with_source_and_details(self) -> None:
        """Vérifie la création avec source et détails."""
        exc = ExtractionError(
            "erreur",
            source_name="appels.csv",
            details="encodage invalide",
        )
        assert exc.details == "source: appels.csv, encodage invalide"

    def test_creation_with_details_only(self) -> None:
        """Vérifie la création avec détails sans source."""
        exc = ExtractionError("erreur", details="info")
        assert exc.source_name is None
        assert exc.details == "info"

    def test_str_with_source(self) -> None:
        """Vérifie __str__ avec source."""
        exc = ExtractionError("erreur", source_name="f.csv")
        assert str(exc) == "erreur — source: f.csv"

    def test_can_be_raised_and_caught(self) -> None:
        """Vérifie que l'exception peut être levée et capturée."""
        with pytest.raises(ExtractionError, match="erreur"):
            raise ExtractionError("erreur")

    def test_can_be_caught_as_reporting_error(self) -> None:
        """Vérifie la capture comme ReportingError."""
        with pytest.raises(ReportingError):
            raise ExtractionError("erreur")
