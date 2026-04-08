"""Tests pour BusinessNumericRounding."""

from baobab_activity_reporting.reporting.presentation.business_numeric_rounding import (
    BusinessNumericRounding,
)


class TestBusinessNumericRounding:
    """Arrondis d'affichage."""

    def test_finite(self) -> None:
        """Nombre fini formaté."""
        assert "," in BusinessNumericRounding.display_float(1.234, decimals=2)

    def test_non_finite(self) -> None:
        """Non fini → tiret."""
        assert BusinessNumericRounding.display_float(float("nan")) == "—"
