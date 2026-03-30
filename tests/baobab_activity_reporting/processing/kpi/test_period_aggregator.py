"""Tests unitaires pour PeriodAggregator."""

from datetime import date

import pandas as pd
import pytest

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.exceptions.kpi_computation_error import (
    KpiComputationError,
)
from baobab_activity_reporting.processing.kpi.period_aggregator import (
    PeriodAggregator,
)


class TestPeriodAggregator:
    """Tests pour la classe PeriodAggregator."""

    def test_filter_for_period(self) -> None:
        """Vérifie le filtrage par bornes."""
        period = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        df = pd.DataFrame(
            {
                "Date": ["2026-01-05", "2026-02-01"],
                "v": [1, 2],
            }
        )
        agg = PeriodAggregator()
        out = agg.filter_for_period(df, period)
        assert len(out) == 1
        assert int(out["v"].iloc[0]) == 1

    def test_empty_dataframe(self) -> None:
        """Vérifie qu'un DataFrame vide reste vide."""
        period = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        df = pd.DataFrame()
        agg = PeriodAggregator()
        out = agg.filter_for_period(df, period)
        assert len(out) == 0

    def test_resolve_date_column_raises(self) -> None:
        """Vérifie l'erreur si aucune colonne date."""
        df = pd.DataFrame({"x": [1]})
        agg = PeriodAggregator()
        with pytest.raises(KpiComputationError):
            agg.resolve_date_column(df)

    def test_period_to_iso_bounds(self) -> None:
        """Vérifie les bornes ISO."""
        period = ReportingPeriod(date(2026, 3, 1), date(2026, 3, 30))
        start, end = PeriodAggregator.period_to_iso_bounds(period)
        assert start == "2026-03-01"
        assert end == "2026-03-30"
