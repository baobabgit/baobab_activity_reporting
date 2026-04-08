"""Sous-package des objets de résultat techniques.

Regroupe les structures de données utilisées pour transporter
les résultats intermédiaires du pipeline de reporting.
"""

from baobab_activity_reporting.domain.results.data_availability import (
    DataAvailability,
)
from baobab_activity_reporting.domain.results.extraction_result import (
    ExtractionResult,
)
from baobab_activity_reporting.domain.results.section_attention_assessment import (
    SectionAttentionAssessment,
)
from baobab_activity_reporting.domain.results.section_decision import (
    SectionDecision,
)
from baobab_activity_reporting.domain.results.section_eligibility_codes import (
    SectionEligibilityCodes,
)
from baobab_activity_reporting.domain.results.section_eligibility_detail import (
    SectionEligibilityDetail,
)
from baobab_activity_reporting.domain.results.validation_result import (
    ValidationResult,
)

__all__: list[str] = [
    "DataAvailability",
    "ExtractionResult",
    "SectionAttentionAssessment",
    "SectionDecision",
    "SectionEligibilityCodes",
    "SectionEligibilityDetail",
    "ValidationResult",
]
