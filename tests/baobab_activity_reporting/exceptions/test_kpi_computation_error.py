"""Tests unitaires pour KpiComputationError."""

import pytest

from baobab_activity_reporting.exceptions.kpi_computation_error import (
    KpiComputationError,
)


class TestKpiComputationError:
    """Tests pour la classe KpiComputationError."""

    def test_message_only(self) -> None:
        """Vérifie le message sans détails."""
        err = KpiComputationError("Échec calcul")
        assert "Échec calcul" in str(err)

    def test_with_details(self) -> None:
        """Vérifie message et détails."""
        err = KpiComputationError("Échec", details="colonne manquante")
        assert "Échec" in str(err)
        assert "colonne manquante" in str(err)

    def test_raises(self) -> None:
        """Vérifie que l'exception peut être levée et capturée."""
        with pytest.raises(KpiComputationError):
            raise KpiComputationError("x")
