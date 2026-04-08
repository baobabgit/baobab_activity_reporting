"""Tests pour TablePolicy."""

from baobab_activity_reporting.reporting.editorial.table_policy import TablePolicy


class TestTablePolicy:
    """Tests pour la classe TablePolicy."""

    def test_default(self) -> None:
        """Politique par défaut."""
        p = TablePolicy.default()
        assert p.max_rows is None
