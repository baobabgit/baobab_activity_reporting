"""Calcul des KPI et agrégations à partir des données préparées."""

from baobab_activity_reporting.processing.kpi.activity_aggregator import (
    ActivityAggregator,
)
from baobab_activity_reporting.processing.kpi.agent_kpi_calculator import (
    AgentKpiCalculator,
)
from baobab_activity_reporting.processing.kpi.consolidated_data_schema import (
    ConsolidatedDataSchema,
)
from baobab_activity_reporting.processing.kpi.kpi_computation_pipeline import (
    KpiComputationPipeline,
)
from baobab_activity_reporting.processing.kpi.period_aggregator import (
    PeriodAggregator,
)
from baobab_activity_reporting.processing.kpi.site_kpi_calculator import (
    SiteKpiCalculator,
)
from baobab_activity_reporting.processing.kpi.telephony_kpi_calculator import (
    TelephonyKpiCalculator,
)

__all__: list[str] = [
    "ActivityAggregator",
    "AgentKpiCalculator",
    "ConsolidatedDataSchema",
    "KpiComputationPipeline",
    "PeriodAggregator",
    "SiteKpiCalculator",
    "TelephonyKpiCalculator",
]
