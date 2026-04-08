"""Tests pour PercentageFormatter."""

from baobab_activity_reporting.reporting.presentation.percentage_formatter import (
    PercentageFormatter,
)


class TestPercentageFormatter:
    """Pourcentages."""

    def test_decimal_comma(self) -> None:
        """Virgule décimale française."""
        assert "%" in PercentageFormatter.format_percent(12.3)
        assert "," in PercentageFormatter.format_percent(12.3)
