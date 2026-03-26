"""Tests unitaires pour ResolutionError."""

import pytest

from baobab_activity_reporting.exceptions.reporting_error import (
    ReportingError,
)
from baobab_activity_reporting.exceptions.resolution_error import (
    ResolutionError,
)


class TestResolutionError:
    """Tests pour la classe ResolutionError."""

    def test_inherits_from_reporting_error(self) -> None:
        """Vérifie l'héritage depuis ReportingError."""
        assert issubclass(ResolutionError, ReportingError)

    def test_creation_with_message_only(self) -> None:
        """Vérifie la création avec un message seul."""
        exc = ResolutionError("agent non trouvé")
        assert exc.message == "agent non trouvé"
        assert exc.entity_type is None
        assert exc.details is None

    def test_creation_with_entity_type(self) -> None:
        """Vérifie la création avec un type d'entité."""
        exc = ResolutionError("erreur", entity_type="Agent")
        assert exc.entity_type == "Agent"
        assert exc.details == "entité: Agent"

    def test_creation_with_entity_and_details(self) -> None:
        """Vérifie la création avec entité et détails."""
        exc = ResolutionError(
            "erreur",
            entity_type="Agent",
            details="homonyme détecté",
        )
        assert exc.details == "entité: Agent, homonyme détecté"

    def test_creation_with_details_only(self) -> None:
        """Vérifie la création avec détails sans entité."""
        exc = ResolutionError("erreur", details="info")
        assert exc.entity_type is None
        assert exc.details == "info"

    def test_str_with_entity(self) -> None:
        """Vérifie __str__ avec entité."""
        exc = ResolutionError("erreur", entity_type="Site")
        assert str(exc) == "erreur — entité: Site"

    def test_can_be_raised_and_caught(self) -> None:
        """Vérifie que l'exception peut être levée et capturée."""
        with pytest.raises(ResolutionError, match="erreur"):
            raise ResolutionError("erreur")

    def test_can_be_caught_as_reporting_error(self) -> None:
        """Vérifie la capture comme ReportingError."""
        with pytest.raises(ReportingError):
            raise ResolutionError("erreur")
