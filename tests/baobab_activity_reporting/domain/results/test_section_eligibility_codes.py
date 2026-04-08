"""Tests pour SectionEligibilityCodes."""

from baobab_activity_reporting.domain.results.section_eligibility_codes import (
    SectionEligibilityCodes,
)


class TestSectionEligibilityCodes:
    """Constantes stables."""

    def test_sample_codes_distinct(self) -> None:
        """Échantillon de codes distincts et non vides."""
        a = SectionEligibilityCodes.MIN_DATA_SATISFIED
        b = SectionEligibilityCodes.PREFIX_GATE_FAILED
        assert a != b
        assert len(a) > 0 and len(b) > 0
