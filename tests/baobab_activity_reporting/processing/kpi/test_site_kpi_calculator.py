"""Tests unitaires pour SiteKpiCalculator."""

import pandas as pd

from baobab_activity_reporting.processing.kpi.activity_aggregator import (
    ActivityAggregator,
)
from baobab_activity_reporting.processing.kpi.site_kpi_calculator import (
    SiteKpiCalculator,
)
from baobab_activity_reporting.processing.kpi.telephony_kpi_calculator import (
    TelephonyKpiCalculator,
)


class TestSiteKpiCalculator:
    """Tests pour la classe SiteKpiCalculator."""

    def test_site_telephony_and_tickets(self) -> None:
        """Vérifie les KPI par site pour appels et tickets."""
        inc = pd.DataFrame(
            {
                "Site": ["S1", "S1"],
                "Durée": [10.0, 20.0],
            }
        )
        tickets = pd.DataFrame(
            {
                "Site": ["S1"],
                "Canal": ["EFI"],
            }
        )
        calc = SiteKpiCalculator(ActivityAggregator(), TelephonyKpiCalculator())
        rows = calc.compute(inc, pd.DataFrame(), tickets)
        codes = [t[0].code for t in rows]
        assert any("site.S1.telephony.incoming" in c for c in codes)
        assert any("EFI" in c for c in codes)
