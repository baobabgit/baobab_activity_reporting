"""Tests pour SectionKpiTableProjector."""

from baobab_activity_reporting.reporting.editorial.table_layout_kind import (
    TableLayoutKind,
)
from baobab_activity_reporting.reporting.presentation.section_kpi_table_projector import (
    SectionKpiTableProjector,
)


class TestSectionKpiTableProjector:
    """Projection des lignes par layout."""

    def test_key_figures_priority(self) -> None:
        """Ordre des codes clés."""
        rows = [
            {"code": "z.other", "value": 99.0},
            {"code": "telephony.incoming.count", "value": 1.0},
        ]
        out, _ = SectionKpiTableProjector().project(
            TableLayoutKind.KEY_FIGURES,
            rows,
            max_rows=4,
        )
        assert out[0]["code"] == "telephony.incoming.count"

    def test_agent_missing_field_triggers_alert(self) -> None:
        """Agent absent en dimension mais présent dans le code : alerte."""
        rows = [
            {
                "code": "agent.Marie.telephony.incoming.count",
                "value": 1.0,
                "unit": "appels",
                "agent": None,
            },
        ]
        _, alerts = SectionKpiTableProjector().project(
            TableLayoutKind.AGENT_VENTILATION,
            rows,
            max_rows=4,
        )
        assert len(alerts) >= 1

    def test_site_label_from_code(self) -> None:
        """Libellé site dérivé du code si colonne absente."""
        row = {
            "code": "site.Paris.telephony.incoming.count",
            "value": 1.0,
            "site": None,
        }
        assert SectionKpiTableProjector.site_label_for_row(row) == "Paris"
