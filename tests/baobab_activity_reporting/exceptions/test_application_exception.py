"""Tests unitaires pour ApplicationException."""

import pytest

from baobab_activity_reporting.exceptions.application_exception import (
    ApplicationException,
)


class TestApplicationException:
    """Tests pour la classe ApplicationException."""

    def test_inherits_from_exception(self) -> None:
        """Vérifie que ApplicationException hérite de Exception."""
        assert issubclass(ApplicationException, Exception)

    def test_creation_with_message_only(self) -> None:
        """Vérifie la création avec un message seul."""
        exc = ApplicationException("erreur test")
        assert exc.message == "erreur test"
        assert exc.details is None

    def test_creation_with_message_and_details(self) -> None:
        """Vérifie la création avec un message et des détails."""
        exc = ApplicationException("erreur test", details="info")
        assert exc.message == "erreur test"
        assert exc.details == "info"

    def test_str_without_details(self) -> None:
        """Vérifie __str__ sans détails."""
        exc = ApplicationException("erreur test")
        assert str(exc) == "erreur test"

    def test_str_with_details(self) -> None:
        """Vérifie __str__ avec détails."""
        exc = ApplicationException("erreur test", details="info")
        assert str(exc) == "erreur test — info"

    def test_repr_without_details(self) -> None:
        """Vérifie __repr__ sans détails."""
        exc = ApplicationException("erreur test")
        expected = "ApplicationException(message='erreur test', details=None)"
        assert repr(exc) == expected

    def test_repr_with_details(self) -> None:
        """Vérifie __repr__ avec détails."""
        exc = ApplicationException("erreur test", details="info")
        expected = "ApplicationException(message='erreur test', details='info')"
        assert repr(exc) == expected

    def test_can_be_raised_and_caught(self) -> None:
        """Vérifie que l'exception peut être levée et capturée."""
        with pytest.raises(ApplicationException, match="erreur test"):
            raise ApplicationException("erreur test")

    def test_can_be_caught_as_exception(self) -> None:
        """Vérifie que l'exception peut être capturée comme Exception."""
        with pytest.raises(Exception, match="erreur test"):
            raise ApplicationException("erreur test")

    def test_args_contains_full_message(self) -> None:
        """Vérifie que args contient le message complet."""
        exc = ApplicationException("msg", details="det")
        assert exc.args == ("msg — det",)

    def test_args_without_details(self) -> None:
        """Vérifie que args contient le message sans détails."""
        exc = ApplicationException("msg")
        assert exc.args == ("msg",)

    def test_empty_message(self) -> None:
        """Vérifie le comportement avec un message vide."""
        exc = ApplicationException("")
        assert exc.message == ""
        assert str(exc) == ""

    def test_details_none_explicitly(self) -> None:
        """Vérifie que details=None est le défaut."""
        exc = ApplicationException("msg", details=None)
        assert exc.details is None
        assert str(exc) == "msg"
