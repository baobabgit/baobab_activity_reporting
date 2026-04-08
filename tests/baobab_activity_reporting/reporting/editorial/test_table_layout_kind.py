"""Tests pour TableLayoutKind."""

from baobab_activity_reporting.reporting.editorial.table_layout_kind import (
    TableLayoutKind,
)


class TestTableLayoutKind:
    """Valeurs d'énumération."""

    def test_str_values(self) -> None:
        """Chaînes stables."""
        assert TableLayoutKind.KEY_FIGURES.value == "key_figures"
        assert TableLayoutKind.CHANNEL_DISTRIBUTION.value == "channel_distribution"
