"""Tests pour DisplayRules."""

from baobab_activity_reporting.reporting.editorial.display_rules import DisplayRules


class TestDisplayRules:
    """Tests pour la classe DisplayRules."""

    def test_default(self) -> None:
        """Fabrique par défaut."""
        d = DisplayRules.default()
        assert d.show_metric_tables is True
