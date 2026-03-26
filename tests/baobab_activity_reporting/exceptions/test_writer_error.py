"""Tests unitaires pour WriterError."""

import pytest

from baobab_activity_reporting.exceptions.reporting_error import (
    ReportingError,
)
from baobab_activity_reporting.exceptions.writer_error import WriterError


class TestWriterError:
    """Tests pour la classe WriterError."""

    def test_inherits_from_reporting_error(self) -> None:
        """Vérifie l'héritage depuis ReportingError."""
        assert issubclass(WriterError, ReportingError)

    def test_creation_with_message_only(self) -> None:
        """Vérifie la création avec un message seul."""
        exc = WriterError("export échoué")
        assert exc.message == "export échoué"
        assert exc.output_format is None
        assert exc.details is None

    def test_creation_with_output_format(self) -> None:
        """Vérifie la création avec un format de sortie."""
        exc = WriterError("erreur", output_format="docx")
        assert exc.output_format == "docx"
        assert exc.details == "format: docx"

    def test_creation_with_format_and_details(self) -> None:
        """Vérifie la création avec format et détails."""
        exc = WriterError(
            "erreur",
            output_format="docx",
            details="style manquant",
        )
        assert exc.details == "format: docx, style manquant"

    def test_creation_with_details_only(self) -> None:
        """Vérifie la création avec détails sans format."""
        exc = WriterError("erreur", details="info")
        assert exc.output_format is None
        assert exc.details == "info"

    def test_str_with_format(self) -> None:
        """Vérifie __str__ avec format."""
        exc = WriterError("erreur", output_format="html")
        assert str(exc) == "erreur — format: html"

    def test_can_be_raised_and_caught(self) -> None:
        """Vérifie que l'exception peut être levée et capturée."""
        with pytest.raises(WriterError, match="erreur"):
            raise WriterError("erreur")

    def test_can_be_caught_as_reporting_error(self) -> None:
        """Vérifie la capture comme ReportingError."""
        with pytest.raises(ReportingError):
            raise WriterError("erreur")
