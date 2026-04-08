"""Tests unitaires pour TableBuilder."""

from baobab_activity_reporting.reporting.editorial.table_layout_kind import (
    TableLayoutKind,
)
from baobab_activity_reporting.reporting.editorial.table_policy import TablePolicy
from baobab_activity_reporting.reporting.table_builder import TableBuilder


class TestTableBuilder:
    """Tests pour la classe TableBuilder."""

    def test_no_kpi_code_column(self) -> None:
        """Les tableaux métier n'exposent pas le code KPI."""
        rows = [
            {
                "code": "telephony.incoming.count",
                "label": "Appels entrants",
                "value": 10.0,
                "unit": "appels",
            },
        ]
        tbl = TableBuilder().from_kpi_rows(
            "Caption",
            rows,
            table_policy=TablePolicy(
                max_rows=4,
                layout_kind=TableLayoutKind.KEY_FIGURES,
            ),
        )
        assert "Code" not in tbl["headers"]
        assert tbl["headers"] == ["Indicateur", "Valeur"]
        assert "telephony" not in str(tbl["rows"]).lower()

    def test_duration_formatted_not_raw_seconds(self) -> None:
        """Durée longue : heures et minutes, pas secondes brutes seules."""
        rows = [
            {
                "code": "telephony.incoming.duration_seconds.sum",
                "label": "Durée",
                "value": 7500.0,
                "unit": "s",
            },
        ]
        tbl = TableBuilder().from_kpi_rows(
            "T",
            rows,
            table_policy=TablePolicy(
                max_rows=4,
                layout_kind=TableLayoutKind.KEY_FIGURES,
            ),
        )
        val_cell = str(tbl["rows"][0][1])
        assert "7500" not in val_cell
        assert "h" in val_cell or "min" in val_cell

    def test_channel_layout_limited(self) -> None:
        """Répartition canaux : deux colonnes, pas de code."""
        rows = [
            {
                "code": "tickets.channel.A.count",
                "label": "A",
                "value": 5.0,
                "unit": "tickets",
            },
            {
                "code": "tickets.channel.B.count",
                "label": "B",
                "value": 3.0,
                "unit": "tickets",
            },
        ]
        tbl = TableBuilder().from_kpi_rows(
            "Canaux",
            rows,
            table_policy=TablePolicy(
                max_rows=1,
                layout_kind=TableLayoutKind.CHANNEL_DISTRIBUTION,
            ),
        )
        assert tbl["headers"] == ["Canal", "Volume"]
        assert len(tbl["rows"]) == 1

    def test_skipped_when_empty_projection(self) -> None:
        """Aucune ligne projetée : tableau ignoré."""
        tbl = TableBuilder().from_kpi_rows(
            "Vide",
            [],
            table_policy=TablePolicy.default(),
        )
        assert tbl.get("skipped") is True
        assert tbl["rows"] == []

    def test_agent_ventilation_no_code_in_cells(self) -> None:
        """Ventilation agent : colonnes métier."""
        rows = [
            {
                "code": "agent.Jean.telephony.incoming.count",
                "label": "Entrants",
                "value": 2.0,
                "unit": "appels",
                "agent": "Jean",
            },
        ]
        tbl = TableBuilder().from_kpi_rows(
            "Agents",
            rows,
            table_policy=TablePolicy(
                max_rows=4,
                layout_kind=TableLayoutKind.AGENT_VENTILATION,
            ),
        )
        assert tbl["headers"] == ["Agent", "Indicateur", "Valeur"]
        assert tbl["rows"][0][0] == "Jean"

    def test_site_ventilation_headers(self) -> None:
        """Ventilation site : trois colonnes métier."""
        rows = [
            {
                "code": "site.Lyon.telephony.incoming.count",
                "label": "Entrants",
                "value": 3.0,
                "unit": "appels",
                "site": "Lyon",
            },
        ]
        tbl = TableBuilder().from_kpi_rows(
            "Sites",
            rows,
            table_policy=TablePolicy(
                max_rows=4,
                layout_kind=TableLayoutKind.SITE_VENTILATION,
            ),
        )
        assert tbl["headers"] == ["Site", "Indicateur", "Valeur"]
        assert tbl["rows"][0][0] == "Lyon"
