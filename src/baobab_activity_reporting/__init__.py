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

__all__: list[str] = [
    "Agent",
    "ApplicationException",
    "ConfigurationException",
    "DataAvailability",
    "ExtractionError",
    "ExtractionResult",
    "Kpi",
    "PackageMetadata",
    "PersistenceError",
    "ReportGenerationError",
    "ReportingError",
    "ReportingPeriod",
    "ResolutionError",
    "SectionDecision",
    "Site",
    "StandardizationError",
    "ValidationError",
    "ValidationResult",
    "WriterError",
]
