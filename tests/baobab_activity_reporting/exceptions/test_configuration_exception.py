"""Tests unitaires pour ConfigurationException."""

import pytest

from baobab_activity_reporting.exceptions.application_exception import (
    ApplicationException,
)
from baobab_activity_reporting.exceptions.configuration_exception import (
    ConfigurationException,
)


class TestConfigurationException:
    """Tests pour la classe ConfigurationException."""

    def test_inherits_from_application_exception(self) -> None:
        """Vérifie l'héritage depuis ApplicationException."""
        assert issubclass(ConfigurationException, ApplicationException)

    def test_inherits_from_exception(self) -> None:
        """Vérifie l'héritage transitif depuis Exception."""
        assert issubclass(ConfigurationException, Exception)

    def test_creation_with_message_only(self) -> None:
        """Vérifie la création avec un message seul."""
        exc = ConfigurationException("erreur config")
        assert exc.message == "erreur config"
        assert exc.parameter_name is None
        assert exc.details is None

    def test_creation_with_parameter_name(self) -> None:
        """Vérifie la création avec un nom de paramètre."""
        exc = ConfigurationException("erreur config", parameter_name="db_url")
        assert exc.message == "erreur config"
        assert exc.parameter_name == "db_url"
        assert exc.details == "paramètre: db_url"

    def test_creation_with_parameter_and_details(self) -> None:
        """Vérifie la création avec paramètre et détails."""
        exc = ConfigurationException(
            "erreur config",
            parameter_name="db_url",
            details="valeur invalide",
        )
        assert exc.parameter_name == "db_url"
        assert exc.details == "paramètre: db_url, valeur invalide"

    def test_creation_with_details_only(self) -> None:
        """Vérifie la création avec des détails sans paramètre."""
        exc = ConfigurationException("erreur config", details="fichier absent")
        assert exc.parameter_name is None
        assert exc.details == "fichier absent"

    def test_str_with_parameter(self) -> None:
        """Vérifie __str__ avec un paramètre."""
        exc = ConfigurationException("erreur config", parameter_name="db_url")
        assert str(exc) == "erreur config — paramètre: db_url"

    def test_str_without_parameter(self) -> None:
        """Vérifie __str__ sans paramètre ni détails."""
        exc = ConfigurationException("erreur config")
        assert str(exc) == "erreur config"

    def test_repr(self) -> None:
        """Vérifie __repr__ avec tous les attributs."""
        exc = ConfigurationException(
            "erreur config",
            parameter_name="db_url",
            details="invalide",
        )
        result = repr(exc)
        assert "ConfigurationException(" in result
        assert "message='erreur config'" in result
        assert "parameter_name='db_url'" in result

    def test_can_be_raised_and_caught(self) -> None:
        """Vérifie que l'exception peut être levée et capturée."""
        with pytest.raises(ConfigurationException, match="erreur"):
            raise ConfigurationException("erreur")

    def test_can_be_caught_as_application_exception(self) -> None:
        """Vérifie la capture comme ApplicationException."""
        with pytest.raises(ApplicationException, match="erreur"):
            raise ConfigurationException("erreur")

    def test_can_be_caught_as_exception(self) -> None:
        """Vérifie la capture comme Exception."""
        with pytest.raises(Exception, match="erreur"):
            raise ConfigurationException("erreur")

    def test_empty_parameter_name(self) -> None:
        """Vérifie le comportement avec un paramètre vide."""
        exc = ConfigurationException("msg", parameter_name="")
        assert exc.parameter_name == ""
        assert exc.details == "paramètre: "

    def test_repr_without_parameter(self) -> None:
        """Vérifie __repr__ sans paramètre."""
        exc = ConfigurationException("msg")
        result = repr(exc)
        assert "parameter_name=None" in result
