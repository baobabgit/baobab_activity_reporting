"""Tests pour TablePolicy."""

from baobab_activity_reporting.reporting.editorial.table_layout_kind import (
    TableLayoutKind,
)
from baobab_activity_reporting.reporting.editorial.table_policy import TablePolicy


class TestTablePolicy:
    """Tests pour la classe TablePolicy."""

    def test_default(self) -> None:
        """Politique synthèse : chiffres clés limités."""
        p = TablePolicy.default()
        assert p.max_rows == 6
        assert p.layout_kind == TableLayoutKind.KEY_FIGURES

    def test_factory_compact(self) -> None:
        """Instanciation compacte par défaut de dataclass."""
        p = TablePolicy()
        assert p.max_rows == 8
        assert p.layout_kind == TableLayoutKind.COMPACT_METRICS
