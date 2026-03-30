"""Tests unitaires pour TableBuilder."""

from baobab_activity_reporting.reporting.table_builder import TableBuilder


class TestTableBuilder:
    """Tests pour la classe TableBuilder."""

    def test_from_kpi_rows(self) -> None:
        """Vérifie l'assemblage colonnes / lignes."""
        rows = [
            {
                "code": "c",
                "label": "L",
                "value": 1.5,
                "unit": "u",
                "site": "S",
                "agent": None,
                "channel": None,
            }
        ]
        tbl = TableBuilder().from_kpi_rows("Caption", rows)
        assert tbl["caption"] == "Caption"
        assert tbl["headers"][0] == "Code"
        assert len(tbl["rows"]) == 1
        assert tbl["rows"][0][2] == 1.5
