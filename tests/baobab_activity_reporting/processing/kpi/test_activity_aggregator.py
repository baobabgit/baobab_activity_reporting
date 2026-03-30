"""Tests unitaires pour ActivityAggregator."""

import pandas as pd
import pytest

from baobab_activity_reporting.exceptions.kpi_computation_error import (
    KpiComputationError,
)
from baobab_activity_reporting.processing.kpi.activity_aggregator import (
    ActivityAggregator,
)


class TestActivityAggregator:
    """Tests pour la classe ActivityAggregator."""

    def test_count_by_site(self) -> None:
        """Vérifie le comptage par site."""
        df = pd.DataFrame({"Site": ["A", "A", "B"], "x": [1, 2, 3]})
        agg = ActivityAggregator()
        s = agg.count_by_site(df)
        assert int(s.loc["A"]) == 2
        assert int(s.loc["B"]) == 1

    def test_count_by_agent(self) -> None:
        """Vérifie le comptage par agent."""
        df = pd.DataFrame({"Agent": ["u1", "u1"], "Site": ["S", "S"]})
        agg = ActivityAggregator()
        s = agg.count_by_agent(df)
        assert int(s.loc["u1"]) == 2

    def test_count_by_channel(self) -> None:
        """Vérifie le comptage par canal."""
        df = pd.DataFrame({"Canal": ["EFI", "EDI"], "Site": ["S", "S"]})
        agg = ActivityAggregator()
        s = agg.count_by_channel(df)
        assert int(s.loc["EFI"]) == 1
        assert int(s.loc["EDI"]) == 1

    def test_resolve_site_raises(self) -> None:
        """Vérifie l'absence de colonne site."""
        df = pd.DataFrame({"x": [1]})
        agg = ActivityAggregator()
        with pytest.raises(KpiComputationError):
            agg.resolve_site_column(df)

    def test_combine_series(self) -> None:
        """Vérifie la fusion de séries."""
        agg = ActivityAggregator()
        left = pd.Series([1.0, 2.0], index=["a", "b"])
        right = pd.Series([10.0], index=["b"])
        merged = agg.combine_series(left, right, lambda a, b: a + b)
        assert float(merged.loc["a"]) == 1.0
        assert float(merged.loc["b"]) == 12.0
