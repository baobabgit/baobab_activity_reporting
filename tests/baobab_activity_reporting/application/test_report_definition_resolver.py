"""Tests pour resolve_report_definition."""

import pytest

from baobab_activity_reporting.application.report_definition_resolver import (
    resolve_report_definition,
)
from baobab_activity_reporting.exceptions.configuration_exception import (
    ConfigurationException,
)


class TestReportDefinitionResolver:
    """Tests du résolveur de type de rapport."""

    def test_activity_telephony(self) -> None:
        """Résout le rapport téléphonie."""
        d = resolve_report_definition("activity_telephony")
        assert d.report_type == "activity_telephony"

    def test_unknown_raises(self) -> None:
        """Valeur inconnue : ConfigurationException."""
        with pytest.raises(ConfigurationException, match="inconnu"):
            resolve_report_definition("activity_unknown")
