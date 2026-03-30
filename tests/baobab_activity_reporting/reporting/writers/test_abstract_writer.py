"""Tests unitaires pour AbstractWriter."""

import pytest

from baobab_activity_reporting.reporting.writers.abstract_writer import (
    AbstractWriter,
)


class TestAbstractWriter:
    """Tests pour la classe AbstractWriter."""

    def test_cannot_instantiate(self) -> None:
        """Une classe abstraite non implémentée ne s'instancie pas."""
        with pytest.raises(TypeError):
            AbstractWriter()
