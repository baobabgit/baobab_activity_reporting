"""Tests pour KpiValuePresentationFormatter."""

from baobab_activity_reporting.reporting.presentation.kpi_value_presentation_formatter import (
    KpiValuePresentationFormatter,
)


class TestKpiValuePresentationFormatter:
    """Cellule valeur présentée."""

    def test_appels_volume(self) -> None:
        """Unité appels → volume formaté."""
        fmt = KpiValuePresentationFormatter()
        cell = fmt.format_value_cell(
            {"code": "x.count", "value": 42.0, "unit": "appels"},
        )
        assert "42" in cell.replace(" ", "")

    def test_placeholder_value(self) -> None:
        """Valeur absente."""
        fmt = KpiValuePresentationFormatter()
        assert fmt.format_value_cell({"code": "x", "value": None}) == "—"
