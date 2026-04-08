"""Tests pour VolumeFormatter."""

from baobab_activity_reporting.reporting.presentation.volume_formatter import (
    VolumeFormatter,
)


class TestVolumeFormatter:
    """Volumes entiers lisibles."""

    def test_thousands_separator_space(self) -> None:
        """Séparateur d'espaces pour grands nombres."""
        assert " " in VolumeFormatter.format_count(1234.0)
        assert "1234" in VolumeFormatter.format_count(1234.0).replace(" ", "")
