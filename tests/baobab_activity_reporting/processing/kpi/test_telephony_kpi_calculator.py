"""Tests unitaires pour TelephonyKpiCalculator."""

from datetime import date

import pandas as pd
import pytest

from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.exceptions.kpi_computation_error import (
    KpiComputationError,
)
from baobab_activity_reporting.processing.kpi.telephony_kpi_calculator import (
    TelephonyKpiCalculator,
)


class TestTelephonyKpiCalculator:
    """Tests pour la classe TelephonyKpiCalculator."""

    def test_compute_counts(self) -> None:
        """Vérifie les compteurs globaux."""
        inc = pd.DataFrame({"Durée": [10.0, 20.0]})
        out = pd.DataFrame({"Durée": [5.0]})
        period = ReportingPeriod(date(2026, 1, 1), date(2026, 1, 31))
        calc = TelephonyKpiCalculator()
        rows = calc.compute(inc, out, period)
        codes = {t[0].code for t in rows}
        assert "telephony.incoming.count" in codes
        assert "telephony.outgoing.count" in codes

    def test_duration_seconds_parsing_hh_mm_ss(self) -> None:
        """Vérifie la conversion HH:MM:SS."""
        s = pd.Series(["00:00:10", "00:01:05"])
        out = TelephonyKpiCalculator.duration_series_to_seconds(s)
        assert abs(float(out.iloc[0]) - 10.0) < 0.01
        assert abs(float(out.iloc[1]) - 65.0) < 0.01

    def test_resolve_duration_column_raises(self) -> None:
        """Vérifie l'erreur si pas de colonne durée."""
        df = pd.DataFrame({"x": [1]})
        calc = TelephonyKpiCalculator()
        with pytest.raises(KpiComputationError):
            calc.resolve_duration_column(df)
