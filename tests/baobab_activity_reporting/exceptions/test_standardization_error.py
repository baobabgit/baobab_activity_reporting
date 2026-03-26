"""Tests unitaires pour StandardizationError."""

import pytest

from baobab_activity_reporting.exceptions.reporting_error import (
    ReportingError,
)
from baobab_activity_reporting.exceptions.standardization_error import (
    StandardizationError,
)


class TestStandardizationError:
    """Tests pour la classe StandardizationError."""

    def test_inherits_from_reporting_error(self) -> None:
        """Vérifie l'héritage depuis ReportingError."""
        assert issubclass(StandardizationError, ReportingError)

    def test_creation_with_message_only(self) -> None:
        """Vérifie la création avec un message seul."""
        exc = StandardizationError("conversion impossible")
        assert exc.message == "conversion impossible"
        assert exc.column_name is None
        assert exc.details is None

    def test_creation_with_column_name(self) -> None:
        """Vérifie la création avec un nom de colonne."""
        exc = StandardizationError("erreur", column_name="date")
        assert exc.column_name == "date"
        assert exc.details == "colonne: date"

    def test_creation_with_column_and_details(self) -> None:
        """Vérifie la création avec colonne et détails."""
        exc = StandardizationError(
            "erreur",
            column_name="date",
            details="format invalide",
        )
        assert exc.details == "colonne: date, format invalide"

    def test_creation_with_details_only(self) -> None:
        """Vérifie la création avec détails sans colonne."""
        exc = StandardizationError("erreur", details="info")
        assert exc.column_name is None
        assert exc.details == "info"

    def test_str_with_column(self) -> None:
        """Vérifie __str__ avec colonne."""
        exc = StandardizationError("erreur", column_name="col")
        assert str(exc) == "erreur — colonne: col"

    def test_can_be_raised_and_caught(self) -> None:
        """Vérifie que l'exception peut être levée et capturée."""
        with pytest.raises(StandardizationError, match="erreur"):
            raise StandardizationError("erreur")

    def test_can_be_caught_as_reporting_error(self) -> None:
        """Vérifie la capture comme ReportingError."""
        with pytest.raises(ReportingError):
            raise StandardizationError("erreur")
