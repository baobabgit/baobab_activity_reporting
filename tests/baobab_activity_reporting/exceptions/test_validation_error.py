"""Tests unitaires pour ValidationError."""

import pytest

from baobab_activity_reporting.exceptions.reporting_error import (
    ReportingError,
)
from baobab_activity_reporting.exceptions.validation_error import (
    ValidationError,
)


class TestValidationError:
    """Tests pour la classe ValidationError."""

    def test_inherits_from_reporting_error(self) -> None:
        """Vérifie l'héritage depuis ReportingError."""
        assert issubclass(ValidationError, ReportingError)

    def test_creation_with_message_only(self) -> None:
        """Vérifie la création avec un message seul."""
        exc = ValidationError("colonne manquante")
        assert exc.message == "colonne manquante"
        assert exc.field_name is None
        assert exc.details is None

    def test_creation_with_field_name(self) -> None:
        """Vérifie la création avec un nom de champ."""
        exc = ValidationError("erreur", field_name="date_appel")
        assert exc.field_name == "date_appel"
        assert exc.details == "champ: date_appel"

    def test_creation_with_field_and_details(self) -> None:
        """Vérifie la création avec champ et détails."""
        exc = ValidationError(
            "erreur",
            field_name="date_appel",
            details="type incorrect",
        )
        assert exc.details == "champ: date_appel, type incorrect"

    def test_creation_with_details_only(self) -> None:
        """Vérifie la création avec détails sans champ."""
        exc = ValidationError("erreur", details="info")
        assert exc.field_name is None
        assert exc.details == "info"

    def test_str_with_field(self) -> None:
        """Vérifie __str__ avec champ."""
        exc = ValidationError("erreur", field_name="col")
        assert str(exc) == "erreur — champ: col"

    def test_can_be_raised_and_caught(self) -> None:
        """Vérifie que l'exception peut être levée et capturée."""
        with pytest.raises(ValidationError, match="erreur"):
            raise ValidationError("erreur")

    def test_can_be_caught_as_reporting_error(self) -> None:
        """Vérifie la capture comme ReportingError."""
        with pytest.raises(ReportingError):
            raise ValidationError("erreur")
