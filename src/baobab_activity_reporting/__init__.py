"""Package racine de baobab_activity_reporting.

Ce package fournit l'ossature du projet de reporting d'activité Baobab.
"""

from baobab_activity_reporting.core.package_metadata import PackageMetadata
from baobab_activity_reporting.domain.models.agent import Agent
from baobab_activity_reporting.domain.models.kpi import Kpi
from baobab_activity_reporting.domain.models.reporting_period import (
    ReportingPeriod,
)
from baobab_activity_reporting.domain.models.site import Site
from baobab_activity_reporting.domain.results.data_availability import (
    DataAvailability,
)
from baobab_activity_reporting.domain.results.extraction_result import (
    ExtractionResult,
)
from baobab_activity_reporting.domain.results.section_decision import (
    SectionDecision,
)
from baobab_activity_reporting.domain.results.validation_result import (
    ValidationResult,
)
from baobab_activity_reporting.exceptions.application_exception import (
    ApplicationException,
)
from baobab_activity_reporting.exceptions.configuration_exception import (
    ConfigurationException,
)
from baobab_activity_reporting.exceptions.extraction_error import (
    ExtractionError,
)
from baobab_activity_reporting.exceptions.kpi_computation_error import (
    KpiComputationError,
)
from baobab_activity_reporting.exceptions.persistence_error import (
    PersistenceError,
)
from baobab_activity_reporting.exceptions.report_generation_error import (
    ReportGenerationError,
)
from baobab_activity_reporting.exceptions.reporting_error import (
    ReportingError,
)
from baobab_activity_reporting.exceptions.resolution_error import (
    ResolutionError,
)
from baobab_activity_reporting.exceptions.standardization_error import (
    StandardizationError,
)
from baobab_activity_reporting.exceptions.validation_error import (
    ValidationError,
)
from baobab_activity_reporting.exceptions.writer_error import WriterError
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
from baobab_activity_reporting.reporting.insight_builder import InsightBuilder
from baobab_activity_reporting.reporting.narrative_builder import NarrativeBuilder
from baobab_activity_reporting.reporting.report_builder import ReportBuilder
from baobab_activity_reporting.reporting.report_context import ReportContext
from baobab_activity_reporting.reporting.report_definition import ReportDefinition
from baobab_activity_reporting.reporting.report_model import ReportModel
from baobab_activity_reporting.reporting.report_planner import ReportPlanner
from baobab_activity_reporting.reporting.section_eligibility_evaluator import (
    SectionEligibilityEvaluator,
)
from baobab_activity_reporting.reporting.table_builder import TableBuilder

__all__: list[str] = [
    "ActivityAggregator",
    "Agent",
    "AgentKpiCalculator",
    "ApplicationException",
    "ConfigurationException",
    "ConsolidatedDataSchema",
    "DataAvailability",
    "ExtractionError",
    "ExtractionResult",
    "InsightBuilder",
    "Kpi",
    "KpiComputationError",
    "KpiComputationPipeline",
    "NarrativeBuilder",
    "PackageMetadata",
    "PeriodAggregator",
    "PersistenceError",
    "ReportBuilder",
    "ReportContext",
    "ReportDefinition",
    "ReportGenerationError",
    "ReportModel",
    "ReportPlanner",
    "ReportingError",
    "ReportingPeriod",
    "ResolutionError",
    "SectionDecision",
    "SectionEligibilityEvaluator",
    "Site",
    "SiteKpiCalculator",
    "StandardizationError",
    "TableBuilder",
    "TelephonyKpiCalculator",
    "ValidationError",
    "ValidationResult",
    "WriterError",
]
