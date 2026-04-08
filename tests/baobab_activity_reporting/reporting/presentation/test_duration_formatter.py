"""Tests pour DurationFormatter."""

from baobab_activity_reporting.reporting.presentation.duration_formatter import (
    DurationFormatter,
)


class TestDurationFormatter:
    """Formatage des durées."""

    def test_seconds_short(self) -> None:
        """Moins d'une minute : secondes."""
        assert DurationFormatter.format_seconds(45.0) == "45 s"

    def test_minutes_medium(self) -> None:
        """Minutes avec décimale si court."""
        text = DurationFormatter.format_seconds(125.0)
        assert "min" in text
        assert "125" not in text

    def test_hours_long(self) -> None:
        """Longue durée : heures et minutes."""
        text = DurationFormatter.format_seconds(7500.0)
        assert "h" in text
        assert "min" in text

    def test_invalid(self) -> None:
        """Valeur non finie."""
        assert DurationFormatter.format_seconds(float("nan")) == "—"
