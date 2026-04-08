"""Tests pour DimensionAnomalyChecker."""

from baobab_activity_reporting.reporting.presentation.dimension_anomaly_checker import (
    DimensionAnomalyChecker,
)


class TestDimensionAnomalyChecker:
    """Placeholders et dimensions."""

    def test_site_placeholder(self) -> None:
        """Site vide ou tiret : anomalie."""
        text, bad = DimensionAnomalyChecker.normalize_dimension("")
        assert bad is True
        assert text == "—"

    def test_placeholder_value(self) -> None:
        """Valeur placeholder."""
        assert DimensionAnomalyChecker.is_placeholder_value("—") is True
        assert DimensionAnomalyChecker.is_placeholder_value(5.0) is False
