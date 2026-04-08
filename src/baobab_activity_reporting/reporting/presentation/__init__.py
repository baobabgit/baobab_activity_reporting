"""Couche de présentation métier des métriques (hors writers)."""

from baobab_activity_reporting.reporting.presentation.business_numeric_rounding import (
    BusinessNumericRounding,
)
from baobab_activity_reporting.reporting.presentation.dimension_anomaly_checker import (
    DimensionAnomalyChecker,
)
from baobab_activity_reporting.reporting.presentation.duration_formatter import (
    DurationFormatter,
)
from baobab_activity_reporting.reporting.presentation.kpi_value_presentation_formatter import (
    KpiValuePresentationFormatter,
)
from baobab_activity_reporting.reporting.presentation.percentage_formatter import (
    PercentageFormatter,
)
from baobab_activity_reporting.reporting.presentation.section_kpi_table_projector import (
    SectionKpiTableProjector,
)
from baobab_activity_reporting.reporting.presentation.technical_label_sanitizer import (
    TechnicalLabelSanitizer,
)
from baobab_activity_reporting.reporting.presentation.volume_formatter import (
    VolumeFormatter,
)

__all__: list[str] = [
    "BusinessNumericRounding",
    "DimensionAnomalyChecker",
    "DurationFormatter",
    "KpiValuePresentationFormatter",
    "PercentageFormatter",
    "SectionKpiTableProjector",
    "TechnicalLabelSanitizer",
    "VolumeFormatter",
]
