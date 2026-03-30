"""Sous-package des exceptions du projet.

Regroupe la hiérarchie d'exceptions applicatives.
"""

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

__all__: list[str] = [
    "ApplicationException",
    "ConfigurationException",
    "ExtractionError",
    "KpiComputationError",
    "PersistenceError",
    "ReportGenerationError",
    "ReportingError",
    "ResolutionError",
    "StandardizationError",
    "ValidationError",
    "WriterError",
]
