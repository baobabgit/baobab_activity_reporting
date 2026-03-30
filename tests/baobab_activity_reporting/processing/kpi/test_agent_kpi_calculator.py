"""Tests unitaires pour AgentKpiCalculator."""

import pandas as pd

from baobab_activity_reporting.processing.kpi.activity_aggregator import (
    ActivityAggregator,
)
from baobab_activity_reporting.processing.kpi.agent_kpi_calculator import (
    AgentKpiCalculator,
)
from baobab_activity_reporting.processing.kpi.telephony_kpi_calculator import (
    TelephonyKpiCalculator,
)


class TestAgentKpiCalculator:
    """Tests pour la classe AgentKpiCalculator."""

    def test_agent_metrics(self) -> None:
        """Vérifie les KPI par agent."""
        inc = pd.DataFrame(
            {
                "Agent": ["A1"],
                "Durée": [30.0],
            }
        )
        tickets = pd.DataFrame(
            {
                "Agent": ["A1", "A1"],
            }
        )
        calc = AgentKpiCalculator(ActivityAggregator(), TelephonyKpiCalculator())
        rows = calc.compute(inc, pd.DataFrame(), tickets)
        codes = [t[0].code for t in rows]
        assert any("agent.A1.telephony.incoming" in c for c in codes)
        assert any("agent.A1.tickets.count" in c for c in codes)
