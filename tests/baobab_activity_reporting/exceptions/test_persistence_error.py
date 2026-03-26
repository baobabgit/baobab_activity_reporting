"""Tests unitaires pour PersistenceError."""

import pytest

from baobab_activity_reporting.exceptions.persistence_error import (
    PersistenceError,
)
from baobab_activity_reporting.exceptions.reporting_error import (
    ReportingError,
)


class TestPersistenceError:
    """Tests pour la classe PersistenceError."""

    def test_inherits_from_reporting_error(self) -> None:
        """Vérifie l'héritage depuis ReportingError."""
        assert issubclass(PersistenceError, ReportingError)

    def test_creation_with_message_only(self) -> None:
        """Vérifie la création avec un message seul."""
        exc = PersistenceError("écriture impossible")
        assert exc.message == "écriture impossible"
        assert exc.operation is None
        assert exc.details is None

    def test_creation_with_operation(self) -> None:
        """Vérifie la création avec une opération."""
        exc = PersistenceError("erreur", operation="insert")
        assert exc.operation == "insert"
        assert exc.details == "opération: insert"

    def test_creation_with_operation_and_details(self) -> None:
        """Vérifie la création avec opération et détails."""
        exc = PersistenceError(
            "erreur",
            operation="insert",
            details="contrainte violée",
        )
        assert exc.details == "opération: insert, contrainte violée"

    def test_creation_with_details_only(self) -> None:
        """Vérifie la création avec détails sans opération."""
        exc = PersistenceError("erreur", details="info")
        assert exc.operation is None
        assert exc.details == "info"

    def test_str_with_operation(self) -> None:
        """Vérifie __str__ avec opération."""
        exc = PersistenceError("erreur", operation="select")
        assert str(exc) == "erreur — opération: select"

    def test_can_be_raised_and_caught(self) -> None:
        """Vérifie que l'exception peut être levée et capturée."""
        with pytest.raises(PersistenceError, match="erreur"):
            raise PersistenceError("erreur")

    def test_can_be_caught_as_reporting_error(self) -> None:
        """Vérifie la capture comme ReportingError."""
        with pytest.raises(ReportingError):
            raise PersistenceError("erreur")
